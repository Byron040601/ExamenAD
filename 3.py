import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
import bson
import json
from bson.raw_bson import RawBSONDocument
from pymongo.errors import ConnectionFailure

Client = MongoClient('mongodb://localhost:27017/')
try:
    Client.admin.command('ismaster')
    print('MongoDB connection: Succes')
except ConnectionFailure as cf:
    print('MongoDB connection: Succes', cf)

def find_2nd(string, substring):
    return string.find(substring, string.find(substring) + 1)


def find_1st(string, substring):
    return string.find(substring, string.find(substring))


response = requests.get('https://olympics.com/tokyo-2020/es/')
soup = BeautifulSoup(response.content, "lxml")

span = []

post_span = soup.find_all("span", class_="sr-only")

extracted = []

for element in post_span:
    # print(element)
    element = str(element)
    limpio = str(element[find_1st(element, '>') + 1:find_2nd(element, '<')])
    # print (limpio)
    span.append(limpio.strip())

print(post_span)
print(span)

archivo = pd.DataFrame({'destacadas': span})
archivo.to_json('datos.json')

db = Client["ejemploE"]
Collection = db["ejemploExamen"]

with open('datos.json') as file:
    file_data = json.load(file)

if isinstance(file_data, list):
    Collection.insert_many(file_data)
else:
    Collection.insert_one(file_data)
