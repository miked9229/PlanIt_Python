import requests
from bs4 import BeautifulSoup
import json
import pymongo
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

url = "https://www.starbucks.com/store-locator?map=41.887851,-87.640093,13z&place=Chicago,%20IL,%20UA"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


result = soup.find(id='js-content')

print(result)
