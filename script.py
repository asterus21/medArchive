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

        """
        The function accepts an element of a website to click, e.g. a button or a drop-down menu. 
        Such an element is found by its XPath. Whether there are any errors, an exception will be raised.
        """

        try:
            driver.find_element(By.XPATH, point).click()
        except:
            print('An unexpected error occured.\nPlease, restart the program.')
            driver.quit()
            sys.exit(1)

    def parse_page(self, regex: str, html: str) -> list:

        """
        The function accepts a raw string to parse and returns a list of parsed elements. 
        Such a string can contain a regular expression as well.
        """

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

    '''Here we're creating all used classes instances to operate them afterwards.'''
    constants = Constants()
    options = Options()
    parse = Parse()
    service = Service()

    '''We are using the '--headless' option not to open the browser window.'''
    options.add_argument('--headless')

    '''We are calling the browser with the option in hand and its driver as well.'''
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(constants.constants_to_store(1))

    '''We must be sure of the website we are going to parse.'''
    TITLE = "Архив клинических рекомендаций"
    assert TITLE in driver.title

    '''Here we are opening the drop-down menu of the articles list.'''
    parse.find_element(constants.constants_to_store(2))

    '''And choosing the 'Все' value to see a full list of articles.'''
    parse.find_element(constants.constants_to_store(3))

    '''Here we are waiting just in case the page is not loaded completely.'''
    try:
        wait = WebDriverWait(driver, 1000)
        e = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, constants.constants_to_store(4))))
    except:
        print('An unexpected error occured.\nPlease, restart the program.')
        driver.quit()
        sys.exit(1)

    '''We must get a raw HTML page first.'''
    html_text = driver.page_source

    '''This HTML page contains the URLs of the articles and some indices used as their names.'''
    indices = parse.parse_page(constants.constants_to_store(5), html_text)
    url = parse.parse_page(constants.constants_to_store(6), html_text)

    '''We must change the indices of the articles and their URLs due to the files naming restrictions on Windows 10.'''
    indices_revised, url_revised = parse.add_character(indices, url)
    
    '''And replace some symbols in the articles titles themselves.'''
    titles_revised = parse.replace_character(parse.parse_page(constants.constants_to_store(7), html_text))

    '''We must be sure that we are going to download the same amount of articles as the number of indices and titles.'''
    assert len(url_revised) == len(indices_revised) == len(titles_revised)

    '''Finally, we have a list of article names to use.'''
    results = [prefix + name for prefix, name in zip(indices_revised, titles_revised)]

    '''The rest is to send a GET request to each URL to save an article under a name from the list.'''
    for link, result in zip(url_revised, results):
        r = requests.get(link)
        if r.status_code == 200:
            # time.sleep(len(url_revised) // 10)
            filepath = os.path.join(os.getcwd(), result + '.pdf')
            with open(filepath, 'wb') as pdf_object:
                pdf_object.write(r.content)
