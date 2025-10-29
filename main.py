'''
The repository contains a Python code to parse the archive from https://cr.minzdrav.gov.ru/archive.
The main idea of the programm is to download PDF files.
The files are downloaded with their indices used as prefixes to their titles.
Note that there are several files having the same titles.
When manually downloading a file from the website, you get only its index (but not a name).
The examples of the files are given in the "examples" folder. 
Note that the Windows files and folders naming rules are quite strict.
That's why some additional methods were given to save the files under new names.
'''


import logging
import os
import re
import sys
from configparser import ConfigParser
import requests
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
    '''The class contains methods to work with a web page elements.'''

    def __init__(self):
        '''The initialization of the class is empty'''

    def parse_page(self, regex: str, html: str) -> list:
        '''The method is used to parse a web page.'''
        items = re.findall(regex, html)
        return items

    def find_element(self, chrome_driver, point: str) -> None:
        '''The method is used to find a specific element of the page to click.'''
        try:
            element = WebDriverWait(chrome_driver, 30).until(
                expected_conditions.element_to_be_clickable((By.XPATH, point))
                )
            element.click()
        except (NoSuchElementException, TimeoutException) as e:
            logging.error('Element not found: %s - %s.', point, e)
            chrome_driver.quit()
            sys.exit(1)

class Title:
    '''The class contains methods to work with the articles titles.'''

    def replace_character(self, titles: list) -> list:
        '''The method is used to replace forbidden characters in the articles titles.'''

        characters = r'<>:"/\|?*'
        title = []
        for t in titles:
            cleaned_title = ''.join('_' if character in characters
                                        else character for character in t)
            title.append(cleaned_title)
        return title

    def create_index(self, ids: list) -> list:
        '''The method is used to create an index for each article.'''
        indices_revised = [i + "_" for i in ids]
        return indices_revised

    def add_character(self, links: list) -> list:
        '''The method is used to swap the & symbol in each article's title.'''
        url_revised = [url.replace('&amp;', '&') for url in links]
        return url_revised


def get_urls_list(html: str) -> tuple:

    '''The function is used to create a tuple of URLs and titles to download the articles.'''

    page = Page()
    ids = page.parse_page(INDICES, html)
    url = page.parse_page(URL, html)

    title = Title()
    titles_revised = title.replace_character(page.parse_page(TITLES, html))
    indices_revised = title.create_index(ids)
    url_revised = title.add_character(url)

    assert len(url_revised) == len(indices_revised) == len(titles_revised)

    results = [prefix + title for prefix, title in zip(indices_revised, titles_revised)]

    return results, url_revised


def start_driver():

    '''The function is used to start the driver.'''

    options = Options()
    options.add_argument('--headless')
    chrome_driver = webdriver.Chrome(service=Service(), options=options)

    return chrome_driver


def get_logs():

    '''The function is used to get logs.'''

    return logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler('scrapper.log'), logging.StreamHandler()]
        )


def main(chrome_driver):

    '''The main() function of the script.'''

    chrome_driver.get(LINK)
    page = Page()
    assert "Архив клинических рекомендаций" in chrome_driver.title

    page.find_element(chrome_driver, START)
    page.find_element(chrome_driver, END)

    try:
        wait = WebDriverWait(chrome_driver, 1000)
        e = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, ANCHOR)))
    except ConnectionRefusedError:
        chrome_driver.quit()
        sys.exit(1)

    html_text = chrome_driver.page_source
    results, urls = get_urls_list(html_text)

    for url, result in zip(urls, results):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                filepath = os.path.join(os.getcwd(), result + '.pdf')
                with open(filepath, 'wb') as pdf_object:
                    pdf_object.write(r.content)
                print(f"Downloaded: {result}.pdf")
        except ConnectionRefusedError as e:
            print(f"Failed to download {result}: {str(e)}")


if __name__ == "__main__":
    get_logs()
    driver = start_driver()
    try:
        main(driver)
    except RuntimeError:
        driver.quit()
