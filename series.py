import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException, NoSuchWindowException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities
import re

import os
import json

def get_serie(driver: uc.Chrome, paywall: False, output_dir):
    output_dir += './output/series'
    os.makedirs(output_dir, exist_ok=True)

    if paywall:
        output_dir += './paywall'
    else:
        output_dir += './free'

    try: 

        manga_data = {
            "informations": {
                "title": "",
                "authors": [],
                "providers": [],
                "description": "",
            },
            "links": []
            }
        

        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "seriesContents"))
            )

        # Get manga infos
        try:
            manga_info = driver.find_element(By.XPATH, '//*[@id="seriesContents"]/div[2]/div[1]')
            manga_name = manga_info.find_element(By.XPATH, './/h2')
            manga_authors = manga_info.find_elements(By.XPATH, './/ul/li[1]/a')
            manga_providers = manga_info.find_elements(By.XPATH, './/ul/li[2]/a')
            title = manga_name.text
            manga_data["informations"]["title"] = title
            for e in manga_authors:
                manga_data["informations"]["authors"].append(e.text)
            for e in manga_providers:
                manga_data["informations"]["providers"].append(e.text)
        except NoSuchElementException:
            print("Can't find author data")
        
        try:
            manga_data["informations"]["description"] = driver.find_element(By.CSS_SELECTOR, 'p.wordbreak').text
        except NoSuchElementException:
            print("Can't find description")

        # Get chapter list
        chapter_list = driver.find_elements(By.CSS_SELECTOR, 'li.item.series_sort')
        counter = 1
        for li in chapter_list[::-1]:
            manga_data["links"].append({
                "number": li.find_element(By.XPATH, './/a[2]/span').text + (f'_{str(counter)}' if not li.find_element(By.XPATH, './/a[2]/span').text.isdigit() else '') if li.find_element(By.XPATH, './/a[2]/span').text != "" else str(counter),
                "link": li.find_element(By.TAG_NAME, "a").get_attribute("href"),
                "reader_link": "https://vw.mangaz.com/virgo/view/" + li.find_element(By.TAG_NAME, "a").get_attribute("href").rpartition('/')[-1] + "/i:0",
            })
            counter += 1

        urlnbr = driver.current_url.split('/')[-1]
        sanitized_title = re.sub(r'[<>:"/\\|?*]', '', title).strip()
        if sanitized_title == "":
            sanitized_title += urlnbr
        output_dir += f"/{sanitized_title}"
        os.makedirs(output_dir, exist_ok=True)

        if os.path.exists(f"{output_dir}/{sanitized_title}_data.json"):
            print('Serie already exist')
            with open(f"{output_dir}/{sanitized_title}_data.json", 'r', encoding='utf-8') as file:
                existing_json = json.load(file)
            if (existing_json["links"][0]["link"] == manga_data["links"][0]["link"]) or (existing_json["links"][-1]["link"] == manga_data["links"][0]["link"]):
                print('Same link')
            else:
                print('Different link')
                output_dir += f'_{urlnbr}'
                sanitized_title += urlnbr
                os.makedirs(output_dir, exist_ok=True)
                file = open(f"{output_dir}/{sanitized_title}_{urlnbr}_data.json", "x", encoding='utf8')
                json.dump(manga_data, file, ensure_ascii=False, indent=4)
                file.close()
        else:
            file = open(f"{output_dir}/{sanitized_title}_data.json", "x", encoding='utf8')
            json.dump(manga_data, file, ensure_ascii=False, indent=4)
            file.close()

        return f'{output_dir}/{sanitized_title}_data.json', output_dir


    except TimeoutException:
        print("Website not loading (502 or 504) - Run again")
