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
 
client = pymongo.MongoClient("mongodb+srv://planitadmin:GSEpFwQ6WNMNwxqv@cluster-kmsgdv8f.jyaej.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
 
# database 
db = client['TestingDatabase']

collection = db['parks']

x = collection.delete_many({})

print(x.deleted_count, " documents deleted.") 

mongoDBPark = db.parks

total_pages = 404
first_page = 1

## There are 404 total pages of data to scrape from the Park District of Chicago Website 
for x in range(first_page, total_pages + 1):

     URL = 'https://www.chicagoparkdistrict.com/parks-facilities/?title=&page='+str(x)
     
     page = requests.get(URL)
     
     ## Gets the html content of the page
     soup = BeautifulSoup(page.content, 'html.parser')
    
     ## Within the page source, we find the the main-page-content div with id
     ## main-page-content
     results = soup.find(id='main-page-content')
     
     ## returns all of the HTML article tags where the class name is thumbnail-object 
     parks = results.find_all('article', class_= 'thumbnail-object')

     for park in parks:
        
         ## pulls the image url if one exists
         photo = park.find('img', class_='img-responsive')
         
         ## pull the name if one exists
         name = park.find('a')

         ## pulls the address if one exists
         address = park.find('p', class_='address')

        ## pulls the phone number if one exists
         phone = park.find('div', class_='field field--name-field-phone-number field--type-string field--label-hidden field--item')

         driver = webdriver.Firefox(options=options)

         driver.get(URL)
         elm = driver.find_element_by_xpath('//a[@href="'+name['href']+'"]')
         elm.click()

         parkUrl = driver.current_url
        
         ## Gets the park page after clicking
         parkPage = requests.get(parkUrl)
         
         ## Parses the specific park content
         parkSoup = BeautifulSoup(parkPage.content, 'html.parser')
 
        ## Gets the hours of the park
         parkResult = parkSoup.find_all('tr', class_='office-hours__item odd')

        ## Declares an empty dictionary for the JSON to be stored
         parkDict = {}
         for foo in parkResult:
            dayRes = foo.find('td', class_='office-hours__item-label').text.strip()
            hourRes = foo.find('td', class_='office-hours__item-slots').text.strip()
            parkDict[dayRes] = hourRes
         driver.quit()
         stripped_name = ""
         stripped_address = ""
         stripped_phone = ""

         if name != None:
            stripped_name = name.text.strip()
         if address != None:
            stripped_address = address.text.strip()

         if phone != None:
            stripped_phone = phone.text.strip()
        
         ## Finalized JSON object for upload into MongoDB 
         park_from_web = {
             "name": stripped_name,
             "address": stripped_address,
             "phone": stripped_phone,
             "photo": "" if photo == None else photo.get('src'), 
             "hoursOfOperation": parkDict
         }

         print(park_from_web)
         mongoDBPark.insert_one(park_from_web)

# print("Script completed")










