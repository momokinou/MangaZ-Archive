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

    # driver_path = r'./chromedriver-win64/chromedriver.exe'
    # brave = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
    # option = uc.ChromeOptions()
    # # option.add_experimental_option("prefs", {
    # #   "download.default_directory": r"./downloads",
    # #   "download.prompt_for_download": False,
    # #   "download.directory_upgrade": True,
    # #   "safebrowsing.enabled": True
    # # })
    # option.binary_location = brave
    # option.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    # driver = uc.Chrome(driver_executable_path=driver_path, options=option)
    try: 
        # url = "https://www.mangaz.com/series/detail/223511"
        # driver.get(url)

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
        
        manga_data["informations"]["description"] = driver.find_element(By.CSS_SELECTOR, 'p.wordbreak').text

        # Get chapter list
        chapter_list = driver.find_elements(By.CSS_SELECTOR, 'li.item.series_sort')
        for li in chapter_list:
            manga_data["links"].append({
                "number": li.find_element(By.XPATH, './/a[2]/span').text,
                "link": li.find_element(By.TAG_NAME, "a").get_attribute("href"),
                "reader_link": "https://vw.mangaz.com/virgo/view/" + li.find_element(By.TAG_NAME, "a").get_attribute("href").rpartition('/')[-1] + "/i:0",
            })
            # print('Number: ' + li.find_element(By.XPATH, './/a[2]/span').text)
            # print('Link: ' + li.find_element(By.TAG_NAME, "a").get_attribute("href"))

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
