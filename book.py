import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException, NoSuchWindowException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities
import re
from datetime import datetime

import os
import json

def get_book(driver: uc.Chrome, paywall: False, output_dir):
    output_dir += './output/books'
    os.makedirs(output_dir, exist_ok=True)

    if paywall:
        output_dir += './paywall'
    else:
        output_dir += './free'

    try: 

        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]/div[1]'))
            )

        manga_data = {
            "informations": {
                "title": "",
                "authors": [],
                "providers": [],
                "description": "",
            },
            "links": []
            }
        

        # Get manga infos
        manga_info = driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div/div[2]')
        manga_name = manga_info.find_element(By.XPATH, './/h1')
        try:
            manga_authors = manga_info.find_elements(By.XPATH, './/ul[2]/li/span/a')
                    # manga_providers = manga_info.find_elements(By.XPATH, './/ul/li[2]/a')
            title = manga_name.text
            manga_data["informations"]["title"] = title
            for e in manga_authors:
                manga_data["informations"]["authors"].append(e.text)
                # for e in manga_providers:
                # manga_data["title]["informations"]["providers"].append(e.text)//*[@id="contents"]/div[1]/div/div[2]/div[4]/div[1]/p
        except NoSuchElementException:
            print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} Can't find author data")

        try:
            manga_data["informations"]["description"] = driver.find_element(By.CSS_SELECTOR, 'p.wordbreak').text
        except NoSuchElementException:
            print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} Can't find description")

        try:
            # Get chapter list
            manga_data["links"].append({
                "number": '1',
                "link": driver.find_element(By.CSS_SELECTOR, "button.open-viewer.book-begin.ga").get_attribute("data-url"),
                "reader_link": "https://vw.mangaz.com/virgo/view/" + driver.current_url.split('/')[-1] + "/i:0",
            })
        except NoSuchElementException:
            print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} No content available for {title}. MangaZ does not have the license")
            manga_data["links"].append({
                "number": 'No content available. MangaZ does not have the license',
                "link": "MangaZ does not have the license",
                "reader_link": "",
            })

        urlnbr = driver.current_url.split('/')[-1]
        sanitized_title = re.sub(r'[<>:"/\\|?*]', '', title).strip()
        if sanitized_title == "":
            sanitized_title += urlnbr
        output_dir += f"/{sanitized_title}"
        os.makedirs(output_dir, exist_ok=True)

        if os.path.exists(f"{output_dir}/{sanitized_title}_data.json"):
            print(f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} Book already exist. Verifying if same link')
            with open(f"{output_dir}/{sanitized_title}_data.json", 'r', encoding='utf-8') as file:
                existing_json = json.load(file)
            if existing_json["links"][0]["link"] == manga_data["links"][0]["link"]:
                print(f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} Same link')
            else:
                print(f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} Different link')
                output_dir += f'_{urlnbr}'
                os.makedirs(output_dir, exist_ok=True)
                file = open(f"{output_dir}/{sanitized_title}_data.json", "x", encoding='utf8')
                json.dump(manga_data, file, ensure_ascii=False, indent=4)
                file.close()
        else:
            file = open(f"{output_dir}/{sanitized_title}_data.json", "x", encoding='utf8')
            json.dump(manga_data, file, ensure_ascii=False, indent=4)
            file.close()

        return f'{output_dir}/{sanitized_title}_data.json', output_dir


    except TimeoutException:
        print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} Website not loading (502 or 504) - Run again")