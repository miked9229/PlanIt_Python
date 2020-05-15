import requests
from bs4 import BeautifulSoup
import json
import pymongo
import datetime
# try: 
#     client = pymongo.MongoClient("mongodb://planitadmin:planitadmin123@ds011331.mlab.com:11331/heroku_kmsgdv8f?retryWrites=false")
#     print("Connected successfully!!!") 
# except:   
#     print("Could not connect to MongoDB") 

current_page = 0

# # database 
# db = client['heroku_kmsgdv8f']

# collection = db['restaurant_name']

# x = collection.delete_many({})

# print(x.deleted_count, " documents deleted.") 




while current_page != 9200:

    url = 'https://www.opentable.com/chicago-illinois-restaurant-listings?covers=3&currentview=list&datetime=2020-05-15+19%3A00&from='+str(current_page)+'&latitude=41.879449&longitude=-87.85107&metroid=3&size=100&sort=Popularity'
    print(url)
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    print(soup)

    result = soup.find(id="search_results_container")

    restaurant_names = result.find_all('span', class_='rest-row-name-text')

    stripped_name = ""

           
    for restaurant in restaurant_names:

        if restaurant != None:
            stripped_name = restaurant.text.strip()
            print(stripped_name)


    current_page+= 100