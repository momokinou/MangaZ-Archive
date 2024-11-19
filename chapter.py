# Multiprocess thanks to partyball

import os
import requests
import base64
import json
import threading
from bs4 import BeautifulSoup
from PIL import Image
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize a session
session = requests.Session()

# Version key
verkey = "5e404c"
 
# Function to construct image URL
def construct_image_url(base, scramble_dir, image_name, verkey):
    return f"{base}{scramble_dir}/{image_name}?{verkey}="
 
# Function to extract page number from image name
def extract_page_number(order):
    try:
        # Assuming the first 3 characters of 'name' indicate the page number
        return int(order['name'].split('.')[0][:3])
    except (ValueError, IndexError):
        return 0  # Default to 0 if extraction fails
 
# Create a shared flag to signal when an error is encountered
stop_download_flag = threading.Event()

class ChapterNotFoundError(Exception):
    """Image not found. Skipping."""
    pass
    
# Function to download an image from a URL
def download_image(url, path):
    # Check if the stop flag is set, and stop if it is
    if stop_download_flag.is_set():
        return

    try:
        img_response = session.get(url)
        if img_response.status_code == 200:
            with open(path, 'wb') as img_file:
                img_file.write(img_response.content)
        elif img_response.status_code == 404:
            # Set the stop flag and raise an exception
            stop_download_flag.set()
            raise ChapterNotFoundError(f"Chapter not found (404) at {url}")
        else:
            print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} Failed to download {os.path.basename(path)}, status code: {img_response.status_code}")
            time.sleep(5)
            download_image(url, path)  # Retry the download
    except requests.exceptions.RequestException as e:
        print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} Request error: {e} for {url}")
        time.sleep(5)
        download_image(url, path)  # Retry the download
    except Exception as e:
        print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} Unexpected error: {e} for {url}")
        time.sleep(5)
        download_image(url, path)  # Retry the download


 
# Function to unscramble and save the image based on given crops data
def scramble_image(image_path, crops, page_number, save_dir):
    original = Image.open(image_path)
    scrambled = Image.new('RGB', (crops['w'], crops['h']))
    
    # Apply each crop to scramble the image
    for crop in crops['crops']:
        box = (crop['x2'], crop['y2'], crop['x2'] + crop['w'], crop['y2'] + crop['h'])
        region = original.crop(box)
        scrambled.paste(region, (crop['x'], crop['y'], crop['x'] + crop['w'], crop['y'] + crop['h']))
    
    # Save the scrambled image with page number prefix
    scrambled.save(os.path.join(save_dir, f"{page_number}.jpg"), 'JPEG', quality=95)
 
# Function to validate scramble data
def validate_scramble(crops):
    # Simple validation to check if crop coordinates are positive
    for crop in crops['crops']:
        if any(coord < 0 for coord in [crop['x'], crop['y'], crop['x2'], crop['y2']]):
            return False
    return True

#Setting the max number of workers to download concurrently
def download_images_concurrently(orders_sorted, base_url, scramble_dir, save_dir):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []

        for order in orders_sorted:
            # Check if the stop flag is set before submitting a new task
            if stop_download_flag.is_set():
                break

            future = executor.submit(download_and_scramble_image, order, base_url, scramble_dir, save_dir)
            futures.append(future)

        for future in as_completed(futures):
            if stop_download_flag.is_set():
                break

            try:
                future.result()  # This will raise any exceptions from the workers
            except ChapterNotFoundError as e:
                print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} {e}")
                break  # Exit the loop if a ChapterNotFoundError is raised
            except Exception as e:
                print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} Error processing image: {e}")



def download_and_scramble_image(order, base_url, scramble_dir, save_dir):
    image_name = order['name']
    image_url = construct_image_url(base_url, scramble_dir, image_name, verkey)
    page_number = extract_page_number(order)

    if not validate_scramble(order['scramble']):
        print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} Invalid scramble data for {image_name}, skipping.")
        return

    image_path = os.path.join(save_dir, image_name)
    download_image(image_url, image_path)
    scramble_image(image_path, order['scramble'], page_number, save_dir)
    os.remove(image_path)


def download_chapter(url, save_dir):
    # Reset the stop flag at the beginning of each chapter
    stop_download_flag.clear()

    try:
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        doc_element = soup.find(id='doc')
        if not doc_element:
            raise ValueError("Could not find the element with id 'doc' containing JSON data.")

        encoded_json = doc_element.text.strip()
        decoded_json = base64.b64decode(encoded_json).decode('utf-8')
        data = json.loads(decoded_json)
    except ValueError as e:
        print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} Error: {e}")
        return  # Skip if JSON data is missing
    except Exception as e:
        print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} Unexpected error: {e}")
        return  # Skip if there's any unexpected error

    base_url = data['Location']['base']
    scramble_dir = data['Location']['scramble_dir']
    orders = data['Orders']
    os.makedirs(save_dir, exist_ok=True)
    orders_sorted = sorted(orders, key=extract_page_number)

    # Use the concurrent downloader
    download_images_concurrently(orders_sorted, base_url, scramble_dir, save_dir)