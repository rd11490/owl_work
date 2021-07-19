import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)


url = 'https://overwatchleague.com/en-us/power-rankings'

driver.get(url)

time.sleep(5)



html = driver.page_source
print(html)


soup = BeautifulSoup(html)