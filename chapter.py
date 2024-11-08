import os
import requests
import base64
import json
from bs4 import BeautifulSoup
from PIL import Image

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
 
# Function to download an image from a URL
def download_image(url, path):
    img_response = session.get(url)
    if img_response.status_code == 200:
        with open(path, 'wb') as img_file:
            img_file.write(img_response.content)
        # print(f"Downloaded: {os.path.basename(path)}")
    else:
        print(f"Failed to download {os.path.basename(path)}, status code: {img_response.status_code}")
 
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


def download_chapter(url, save_dir):
    
    # URL of the manga page
    #page_url = 'https://vw.mangaz.com/virgo/view/210862/i:3'
    
    # Fetch the page content
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the base64-encoded JSON data
    doc_element = soup.find(id='doc')
    if not doc_element:
        raise ValueError("Could not find the element with id 'doc' containing JSON data.")
    
    encoded_json = doc_element.text.strip()
    decoded_json = base64.b64decode(encoded_json).decode('utf-8')
    data = json.loads(decoded_json)
    
    # Extract necessary information
    base_url = data['Location']['base']  # e.g., "https://mangaz-books.j-comi.jp/Books/210/210862/"
    scramble_dir = data['Location']['scramble_dir']  # e.g., "anne_D42df"
    orders = data['Orders']  # List of orders containing image filenames and scramble data
    
    # Directory to save images
    os.makedirs(save_dir, exist_ok=True)

    # Sort orders based on the numerical prefix in the 'name' field
    orders_sorted = sorted(orders, key=extract_page_number)

    # Process each order in the sorted list to download and scramble images
    for order in orders_sorted:
        image_name = order['name']
        image_url = construct_image_url(base_url, scramble_dir, image_name, verkey)
        
        # Extract page number for prefixing
        page_number = extract_page_number(order)
        
        # Validate scramble data
        if not validate_scramble(order['scramble']):
            print(f"Invalid scramble data for {image_name}, skipping.")
            continue
        

        os.path.exists(os.path.join(save_dir, f"{page_number}.jpg"))
        # Download the image
        image_path = os.path.join(save_dir, image_name)
        download_image(image_url, image_path)
        
        # Scramble the downloaded image and save it
        scramble_image(image_path, order['scramble'], page_number, save_dir)
        # Clearing useless files
        os.remove(image_path)