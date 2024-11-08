import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException, NoSuchWindowException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities

import os
import json

def get_book(driver: uc.Chrome, paywall: False):
    output_dir = './output/books'
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
        manga_authors = manga_info.find_elements(By.XPATH, './/ul[2]/li/span/a')
        # manga_providers = manga_info.find_elements(By.XPATH, './/ul/li[2]/a')
        title = manga_name.text
        manga_data["informations"]["title"] = title
        for e in manga_authors:
            manga_data["informations"]["authors"].append(e.text)
        # for e in manga_providers:
        #     manga_data["title]["informations"]["providers"].append(e.text)//*[@id="contents"]/div[1]/div/div[2]/div[4]/div[1]/p
        
        manga_data["informations"]["description"] = driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div/div[2]/div[3]/div[1]/p').text

        # Get chapter list
        chapter_list = driver.find_elements(By.XPATH, '//*[@id="seriesContents"]/div[2]/div[2]/div/ul/li')
        manga_data["links"].append({
            "number": '1',
            "link": manga_info.find_element(By.XPATH, ".//div[1]/p[2]/button").get_attribute("data-url"),
            "reader_link": "https://vw.mangaz.com/virgo/view/" + driver.current_url.split('/')[-1] + "/i:0",
        })

        output_dir += f"/{title}"
        os.makedirs(output_dir, exist_ok=True)

        if os.path.exists(f"{output_dir}/{title}_data.json"):
            print('Book already exist')
        else:
            file = open(f"{output_dir}/{title}_data.json", "x", encoding='utf8')
            json.dump(manga_data, file, ensure_ascii=False, indent=4)
            file.close()

        return f'{output_dir}/{title}_data.json', output_dir


    except TimeoutException:
        print("Website not loading (502 or 504) - Run again")