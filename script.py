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

'''The constants to use in the script.'''
# DRIVER = 'driver/chromedriver.exe' # note that the relative path to the driver is used
LINK = 'https://cr.minzdrav.gov.ru/archive'
START = '//*[@id="app"]/div/div/main/div/div/div[3]/div[2]/div[1]/div/div/div/div[4]/i'
END = '//*[@id="v-menu-21"]/div/div/div[7]/div[2]/div'
ANCHOR = '//*[@id="app"]/div/div/main/div/div/div[3]/div[1]/table/tbody[1]/tr[377]/td[1]/span' # note that the value can be changed eventually
INDICES = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=(\d{1,4}_\d{1,4})'
URL = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=\d{1,4}_\d{1,4}'
TITLES = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=\d{1,4}_\d{1,4}"\sclass="">(.*?)<\/a><\/td><td>'

class Page():

    """The class contains functions to find an element on the page to parse the page afterwards."""

    def __init__(self):
        pass

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

class Title():

    """The class contains functions to change the names of the articles to download them under new names."""

    def __init__(self):
        pass

    def replace_character(self, titles: list) -> list:

        """The function accepts a list of article titles to remove invalid characters."""

        titles_revised = [    
            title.replace(':', '_').replace('/', '_').replace('<', '_').replace('>', '_') 
            for title in titles
            ]

        return titles_revised

    def add_character(self, ids: list, links: list) -> tuple:

        """The function accepts a list of IDs and a list of links to change and replace a character."""

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

    '''This HTML page contains the URLs of the articles and some indices used as their names.'''    
    indices = page.parse_page(INDICES, html)
    url = page.parse_page(URL, html)
    
    '''We must replace some symbols in the articles titles themselves.'''
    titles_revised = title.replace_character(page.parse_page(TITLES, html))

    '''And change the indices of the articles and their URLs due to the files naming restrictions on Windows 10.'''
    indices_revised, url_revised = title.add_character(indices, url)    

    '''We must be sure that we are going to download the same amount of articles as the number of indices and titles.'''
    assert len(url_revised) == len(indices_revised) == len(titles_revised)

    '''Finally, we have a list of article names to use.'''
    results = [prefix + title for prefix, title in zip(indices_revised, titles_revised)]

    return results, url_revised

if __name__ == "__main__":

    '''Here we're creating all used classes instances to operate them afterwards.'''
    title = Title()
    options = Options()
    page = Page()    
    service = Service()

    '''We are using the '--headless' option not to open the browser window.'''
    options.add_argument('--headless')

    '''We are calling the browser with the option in hand and its driver as well.'''
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(LINK)

    '''We must be sure of the website we are going to parse.'''
    TITLE = "Архив клинических рекомендаций"
    assert TITLE in driver.title

    '''Here we are opening the drop-down menu of the articles list.
    And choosing the 'Все' value to see a full list of articles.'''
    page.find_element(START)
    page.find_element(END)

    '''Here we are waiting just in case the page is not loaded completely.'''
    try:
        wait = WebDriverWait(driver, 1000)
        e = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, ANCHOR)))
    except:
        print('An unexpected error occured.\nPlease, restart the program.')
        driver.quit()
        sys.exit(1)

    '''We must get a raw HTML page first.'''
    html_text = driver.page_source
    results, urls = get_urls_list(html_text)
    
    '''The rest is to send a GET request to each URL to save an article under a title from the list.'''
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
