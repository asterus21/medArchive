import logging
import os
import re
import requests
import sys

from configparser import ConfigParser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait

data = ConfigParser()
data.read('data.ini')

LINK = data.get('LINKS', 'LINK')
START = data.get('PATHS', 'START')
END = data.get('PATHS', 'END')
ANCHOR = data.get('PATHS', 'ANCHOR')
INDICES = data.get('REGEX', 'INDICES')
URL = data.get('REGEX', 'URL')
TITLES = data.get('REGEX', 'TITLES')

class Page:

    def __init__(self):
        pass

    def find_element(self, driver, point: str) -> None:
        try:
            element = WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.XPATH, point)))
            element.click()
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f'Element not found: {point} - {str(e)}.')
            driver.quit()
            sys.exit(1)

    def parse_page(self, regex: str, html: str) -> list:
        items = re.findall(regex, html)
        return items

class Title:
    
    def __init__(self):
        pass

    def replace_character(self, titles: list) -> list:

        INVALID_CHARACTERS = r'<>:"/\|?*'

        def get_clear_string(string: str) -> str:
            return ''.join('_' if character in INVALID_CHARACTERS else character for character in string)
        
        return [get_clear_string(title) for title in titles]

    def add_character(self, ids: list, links: list) -> tuple:

        indices_revised = []
        url_revised = []

        for i in ids:
            index = i + "_"
            indices_revised.append(index)
    
        for url in links:
            s = url.replace('&amp;', '&')
            url_revised.append(s)

        return indices_revised, url_revised

def get_urls_list(html: str) -> tuple:
    
    title = Title()
    page = Page()

    indices = page.parse_page(INDICES, html)
    url = page.parse_page(URL, html)
     
    titles_revised = title.replace_character(page.parse_page(TITLES, html))

    indices_revised, url_revised = title.add_character(indices, url)    

    assert len(url_revised) == len(indices_revised) == len(titles_revised)

    results = [prefix + title for prefix, title in zip(indices_revised,titles_revised)]

    return results, url_revised

def start_driver():
    
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(), options=options)

    return driver

def get_logs():
    logs = logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler('scrapper.log'), logging.StreamHandler()]
        )
    
    return logs

def main(driver):

    driver.get(LINK)
    page = Page()

    TITLE = "Архив клинических рекомендаций"
    assert TITLE in driver.title

    page.find_element(driver, START)
    page.find_element(driver, END)

    try:
        wait = WebDriverWait(driver, 1000)
        e = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, ANCHOR)))
    except:
        print('An unexpected error occured.\nPlease, restart the program.')
        driver.quit()
        sys.exit(1)

    html_text = driver.page_source
    results, urls = get_urls_list(html_text)

    for url, result in zip(urls, results):
        try: 
            r = requests.get(url)
            if r.status_code == 200:
                filepath = os.path.join(os.getcwd(), result + '.pdf')
                with open(filepath, 'wb') as pdf_object:
                    pdf_object.write(r.content)
                print(f"Downloaded: {result}.pdf")
        except Exception as e:
            print(f"Failed to download {result}: {str(e)}")

if __name__ == "__main__":
    main(start_driver())
