import os
import re
import requests
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait

from constants import Constants

class Parse():

    def find_element(self, point: str) -> None:

        """The function accepts an element of a website to click."""

        try:
            driver.find_element(By.XPATH, point).click()
        except:
            print('An unexpected error occured.\nPlease, restart the program.')
            driver.quit()
            sys.exit(1)

    def parse_page(self, regex: str, html: str) -> list:

        """The function accepts a raw string to parse and returns a list of parsed elements."""

        items = re.findall(regex, html)
        return items

    def replace_character(self, names: list) -> list:

        """The function accepts a list of article titles to remove invalid characters."""

        titles_revised = [    
            name.replace(':', '_').replace('/', '_').replace('<', '_').replace('>', '_') 
            for name in names
            ]

        return titles_revised

    def add_character(self, ids: list, links: list) -> tuple:

        """The function accepts a list of IDs and list of links to change/replace a character."""

        indices_revised = []
        url_revised = []

        for i in ids:
            index = i + "_"
            indices_revised.append(index)
    
        for url in links:
            s = url.replace('&amp;', '&')
            url_revised.append(s)

        return indices_revised, url_revised

if __name__ == "__main__":

    constants = Constants()
    options = Options()
    parse = Parse()
    service = Service()

    options.add_argument('--headless')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(constants.constants_to_store(1))

    TITLE = "Архив клинических рекомендаций"
    assert TITLE in driver.title

    '''Here we open the drop-down menu of the articles list.'''
    parse.find_element(constants.constants_to_store(2))

    '''Here we choose the 'Все' value.'''
    parse.find_element(constants.constants_to_store(3))

    '''Here we are waiting just in case the page is not loaded completely.'''
    try:
        wait = WebDriverWait(driver, 1000)
        e = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, constants.constants_to_store(4))))
    except:
        print('An unexpected error occured.\nPlease, restart the program.')
        driver.quit()
        sys.exit(1)

    html_text = driver.page_source

    indices = parse.parse_page(constants.constants_to_store(5), html_text)
    url = parse.parse_page(constants.constants_to_store(6), html_text)

    indices_revised, url_revised = parse.add_character(indices, url)
    
    titles_revised = parse.replace_character(parse.parse_page(constants.constants_to_store(7), html_text))

    assert len(url_revised) == len(indices_revised) == len(titles_revised)

    results = [prefix + name for prefix, name in zip(indices_revised, titles_revised)]

    for link, result in zip(url_revised, results):
        r = requests.get(link)
        if r.status_code == 200:
            # time.sleep(len(url_revised) // 10)
            filepath = os.path.join(os.getcwd(), result + '.pdf')
            with open(filepath, 'wb') as pdf_object:
                pdf_object.write(r.content)
