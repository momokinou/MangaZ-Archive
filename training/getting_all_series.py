import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException, NoSuchWindowException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

import os
import json

driver_path = r'./chromedriver-win64/chromedriver.exe'
brave = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
option = uc.ChromeOptions()

option.binary_location = brave
# option.set_capability("goog:loggingPrefs", {"performance": "ALL"})
driver = uc.Chrome(driver_executable_path=driver_path, options=option)
try: 
    url = "https://r18.mangaz.com/title/"
    driver.get(url)

    manga_data = []


    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "itemListMod"))
        )

    html = driver.find_element(By.XPATH, '/html')
    start_time = time.time()
    duration = 120 # Durée en secondes

    while time.time() - start_time < duration:
        html.send_keys(Keys.ARROW_DOWN)  # Envoyer la commande

    # Get manga infos
    manga_info = driver.find_element(By.CLASS_NAME, 'itemListMod')
    manga_info_li = driver.find_elements(By.XPATH, '//*[@id="contentsLeft"]/div[2]/ul/li')

    for li in manga_info_li:
        manga_data.append({
            'title':  li.find_element(By.XPATH, './/div/div[2]/h4/a').text,
            'link': li.find_element(By.XPATH, './/div/div[2]/h4/a').get_attribute("href"),
        })


    file = open(f"allr18series.json", "x", encoding='utf8')
    # file.write(src)
    json.dump(manga_data, file, ensure_ascii=False, indent=4)
    file.close()

    # get_blob_content_chrome(driver, 'blob_url')


except TimeoutException:
    print("Website not loading (502 or 504) - Run again")

# Fermeture du navigateur
driver.quit()
