import requests
from bs4 import BeautifulSoup
import json
import pymongo
import datetime
try: 
    client = pymongo.MongoClient("mongodb://planitadmin:planitadmin123@ds011331.mlab.com:11331/heroku_kmsgdv8f?retryWrites=false")
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB") 

# database 
db = client['heroku_kmsgdv8f']

collection = db['park']

x = collection.delete_many({})

print(x.deleted_count, " documents deleted.") 

mongoDBPark = db.park

total_pages = 396
first_page = 1

for x in range(1, total_pages + 1):
    URL = 'https://www.chicagoparkdistrict.com/parks-facilities/?title=&page='+str(x)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id='main-page-content')

    
    parks = results.find_all('article', class_= 'thumbnail-object')

    for park in parks:
        photo = park.find('img', class_='img-responsive')
        name = park.find('a')
        address = park.find('p', class_='address')
        phone = park.find('div', class_='field field--name-field-phone-number field--type-string field--label-hidden field--item')

        stripped_name = ""
        stripped_address = ""
        stripped_phone = ""

        if name != None:
            stripped_name = name.text.strip()


        if address != None:
            stripped_address = address.text.strip()

        if phone != None:
            stripped_phone = phone.text.strip()

        

        park_from_web = {
            "name": stripped_name,
            "address": stripped_address,
            "phone": stripped_phone,
            "photo": "" if photo == None else photo.get('src')
        }

        mongoDBPark.insert_one(park_from_web)

print("Script completed")









