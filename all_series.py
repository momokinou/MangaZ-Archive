import time
from typing import Any
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException, NoSuchWindowException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities

import os
import json
import book
from chapter import download_chapter
import series


def read_json_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data

def book_management(driver: uc.Chrome, output_dir):
    paywall = False
    try:
        paywall_management = driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div/div[2]/div[1]/div')
        if 'detailR18mod' in paywall_management.get_attribute('class'):
            paywall = True
    
    except NoSuchElementException:
        paywall = False
    
    return book.get_book(driver, paywall, output_dir)

def series_management(driver: uc.Chrome, output_dir):
    paywall = False
    try:
        paywall_management = driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div/div[2]/div[1]/div')
        if 'detailR18mod' in paywall_management.get_attribute('class'):
            paywall = True
    
    except NoSuchElementException:
        paywall = False
    
    return series.get_serie(driver, paywall, output_dir)


######################################################################################

driver_path = r'./chromedriver-win64/chromedriver.exe'
brave = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
option = uc.ChromeOptions()
option.binary_location = brave
option.add_argument("--headless")  # Active le mode headless
option.add_argument("--no-sandbox")  # Option recommandée en mode headless
option.add_argument("--disable-dev-shm-usage")  # Réduit l'utilisation de la mémoire partagée
# option.set_capability("goog:loggingPrefs", {"performance": "ALL"})
driver = uc.Chrome(driver_executable_path=driver_path, options=option)


input_file = './test_multi_series.json'
series_list = read_json_file(input_file)

for serie in series_list:
    print(f"Title: {serie['title']}, Link: {serie['link']}")
    url = serie['link']
    driver.get(url)
    chapters_file = ''
    output_dir = ''

    # r18 management
    if driver.current_url == 'https://r18.mangaz.com/attention/r18':
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="loginMainColumn"]/div/form/div/input[1]'))
            )
        driver.find_element(By.XPATH, '//*[@id="loginMainColumn"]/div/form/div/input[1]').click()
        time.sleep(2)
    
    if 'r18' in driver.current_url:
        output_dir += './r18'

    if 'book' in driver.current_url:
        chapters_file, new_dir = book_management(driver, output_dir)
        output_dir = new_dir

    if 'series' in driver.current_url:
        chapters_file, new_dir = series_management(driver, output_dir)
        output_dir = new_dir

    manga = read_json_file(chapters_file)
    for chapter in manga['links']:
        if os.path.exists(f'{output_dir}/{chapter["number"]}'):
            print(f'Chapter {chapter["number"]} already exist')
        else:
            if chapter['reader_link'] == "":
                print('Empty book. Nothing to download')
            else:
                print(f'Creating chapter {chapter["number"]}')
                download_chapter(chapter['reader_link'], f'{output_dir}/{chapter["number"]}')

# Fermeture du navigateur
driver.close()
