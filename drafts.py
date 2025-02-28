import os
import re
import requests
import sys
from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait

service = Service()
driver = webdriver.Chrome(service=service) #, options=options)

driver.get('https://cr.minzdrav.gov.ru/archive')
driver.maximize_window()

title = "Архив клинических рекомендаций"
assert title in driver.title

start = '//*[@id="app"]/div/div/main/div/div/div[3]/div[2]/div[1]/div/div/div/div[3]/div'

end = '//*[@id="v-menu-21"]/div/div/div[7]/div[2]/div'
# end = '//*[@id="input-19"]'

anchor = '//*[@id="app"]/div/div/main/div/div/div[3]/div[1]/table/tbody[1]/tr[377]/td[1]/span'

try:
    driver.find_element(By.XPATH, start).click()
    # driver.implicitly_wait(10)
except:
    print('Please, restart the program')
    driver.quit()
    sys.exit(1)

try:
    driver.find_element(By.XPATH, end).click()
    # driver.implicitly_wait(10)
except:
    print('Please, restart the program')
    driver.quit()
    sys.exit(1)

try:
    wait = WebDriverWait(driver, 1000)
    e = wait.until(EC.visibility_of_element_located((By.XPATH, anchor)))
except:
   print('Please, restart the program')
   driver.quit()
   sys.exit(1)
