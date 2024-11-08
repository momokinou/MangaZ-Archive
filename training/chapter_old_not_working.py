# BIG THANKS TO u/Rythemeius

import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException, NoSuchWindowException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import DesiredCapabilities

import os
import json
from urllib.request import urlretrieve
import time
import requests



driver_path = r'./chromedriver-win64/chromedriver.exe'
brave = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
option = uc.ChromeOptions()
option.binary_location = brave
option.set_capability("goog:loggingPrefs", {"performance": "ALL"})
option.add_experimental_option("prefs", {
    "download.default_directory": "E:\Dev\mangaz-downloader\downloads",  # Répertoire de téléchargement
    "download.prompt_for_download": False,  # Ne pas demander de confirmation pour chaque téléchargement
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "disable-features": "LockProfileCookieDatabase"
})
driver = uc.Chrome(driver_executable_path=driver_path, options=option)

page_list = dict()

try: 
    url = "https://vw.mangaz.com/virgo/view/226311/i:1"
    driver.get(url)

    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "contents"))
        )

    html = driver.find_element(By.XPATH, '/html')
    first_page_url = driver.find_element(By.XPATH, '//*[@id="book"]/div[1]/img').get_attribute("src")

    # image_data = requests.get(first_page_url).content
    # with open("./downloads/1.webp", "wb") as file:  # Spécifiez le nom et l'extension de fichier souhaités
    #     file.write(image_data)

    next_page = driver.find_element(By.XPATH, '//*[@id="book"]/div[5]/div[2]/a')

    html.send_keys(Keys.PAGE_UP)
    time.sleep(0.5)
    html.send_keys(Keys.PAGE_DOWN)

    try:
        # Not secure, I'll have to find a better solution
        while True:
            left_page = driver.find_element(By.XPATH, '//*[@id="book"]/div[2]/div[2]/img')
            right_page = driver.find_element(By.XPATH, '//*[@id="book"]/div[3]/div[2]/img')
            old_value = left_page.get_attribute('src')

            page_list[left_page.get_attribute('no')] = left_page.get_attribute('src')
            page_list[right_page.get_attribute('no')] = right_page.get_attribute('src')
            print(left_page.get_attribute('src'))

            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            left_page = driver.find_element(By.XPATH, '//*[@id="book"]/div[2]/div[2]/img')
            if left_page.get_attribute('src') == old_value:
                break
    except TimeoutException:
        print('Chapter downloaded')
    except NoSuchElementException:
        print('Back to chapter selection')

except TimeoutException:
    print("Website not loading (502 or 504) - Run again")

# Fermeture du navigateur
input("Enter to close...")
driver.quit()