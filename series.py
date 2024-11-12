import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException, NoSuchWindowException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities

import os
import json

def get_serie(driver: uc.Chrome, paywall: False):
    output_dir = './output/series'
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
        for li in chapter_list:
            manga_data["links"].append({
                "number": li.find_element(By.XPATH, './/a[2]/span').text,
                "link": li.find_element(By.TAG_NAME, "a").get_attribute("href"),
                "reader_link": "https://vw.mangaz.com/virgo/view/" + li.find_element(By.TAG_NAME, "a").get_attribute("href").rpartition('/')[-1] + "/i:0",
            })

        output_dir += f"/{title}"
        os.makedirs(output_dir, exist_ok=True)

        if os.path.exists(f"{output_dir}/{title}_data.json"):
            print('Serie already exist')
        else:
            file = open(f"{output_dir}/{title}_data.json", "x", encoding='utf8')
            json.dump(manga_data, file, ensure_ascii=False, indent=4)
            file.close()

        return f'{output_dir}/{title}_data.json', output_dir


    except TimeoutException:
        print("Website not loading (502 or 504) - Run again")
