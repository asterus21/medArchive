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
# import time
from constants import CONST

consts = CONST()

def find(point: str) -> None:

    """The function accepts an element of a website to click."""

    try:
        driver.find_element(By.XPATH, point).click()
    except:
        print('Please, restart the program')
        driver.quit()
        sys.exit(1)

def parse(regex: str) -> list:

    """The function accepts a raw string to parse and returns a list of parsed elements."""

    items = re.findall(regex, html_text)
    return items

def replace(names: list) -> list:

    """The function accepts a list of article names to remove invalid characters."""

    titles_revised = [    
        name.replace(':', '_').replace('/', '_').replace('<', '_').replace('>', '_') 
        for name in names
        ]
        
    return titles_revised

def revise(ids: list, links: list) -> tuple:

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

    options = Options()
    options.add_argument('--headless')

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(consts.cons(1))

    title = "Архив клинических рекомендаций"
    assert title in driver.title

    '''here we open the drop-down menu'''
    find(consts.cons(2))
    '''and here we choose the 'Все' value'''
    find(consts.cons(3))

    '''here we wait in case the page is not loaded'''
    try:
        wait = WebDriverWait(driver, 1000)
        e = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, consts.cons(4))))
    except:
        print('Please, restart the program')
        driver.quit()
        sys.exit(1)

    html_text = driver.page_source
    # print(html_text)

    indices = parse(consts.cons(5))
    # print(indices)

    url = parse(consts.cons(6))
    # print(url)

    indices_revised, url_revised = revise(indices, url)
    # print(url_revised)
    # print(indices_revised)

    titles_revised = replace(parse(consts.cons(7)))
    # print(titles_revised)

    assert len(url_revised) == len(indices_revised) == len(titles_revised)

    results = [prefix + name for prefix, name in zip(indices_revised, titles_revised)]
    # print(results)

    for link, result in zip(url_revised, results):
        r = requests.get(link)
        if r.status_code == 200:
            # time.sleep(len(url_revised) // 10)
            filepath = os.path.join(os.getcwd(), result + '.pdf')
            # print(filepath)
            with open(filepath, 'wb') as pdf_object:
                pdf_object.write(r.content)
