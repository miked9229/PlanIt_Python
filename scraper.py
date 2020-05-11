import requests
from bs4 import BeautifulSoup

URL = 'https://www.chicagoparkdistrict.com/parks-facilities/?title=&page=1'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='main-page-content')

parks = results.find_all('article', class_= 'thumbnail-object')

for park in parks:
    name = park.find('a')
    address = park.find('p', class_='address')
    phone = park.find('div', class_='field field--name-field-phone-number field--type-string field--label-hidden field--item')



    if None in (name, address, phone):
        continue

try:
    print(name.text.strip())
except:
    print("")

try:
    print(address.text.strip())
except:
    print("")
try:
    print(phone.text.strip())

except:
    print("")
 
