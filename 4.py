
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from facebook_scraper import get_posts
import couchdb
import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
import bson
from bson.raw_bson import RawBSONDocument
from pymongo.errors import ConnectionFailure

Client = MongoClient('mongodb://localhost:27017/')
try:
    Client.admin.command('ismaster')
    print('MongoDB connection: Succes')
except ConnectionFailure as cf:
    print('MongoDB connection: Succes', cf)

db = Client["ejemploE"]
Collection = db["facebookOlimpiadas"]

i = 1
for post in get_posts('Olympics', pages=50, extra_info=True, credentials=('EMAIL', 'CONTRASEÑA')):
    print(i)
    i = i + 1
    time.sleep(5)

    id = post['post_id']
    doc = {}

    doc['id'] = id

    mydate = post['time']

    try:
        doc['texto'] = post['text']
        doc['date'] = mydate.timestamp()
        doc['likes'] = post['likes']
        doc['comments'] = post['comments']
        doc['shares'] = post['shares']
        try:
            doc['reactions'] = post['reactions']
        except:
            doc['reactions'] = {}

        doc['post_url'] = post['post_url']
        #db.save(doc)

        archivo = pd.DataFrame({'olimpiadas': doc})
        archivo.to_json('datos.json')

        with open('datos.json') as file:
            file_data = json.load(file)

        if isinstance(file_data, list):
            Collection.insert_many(file_data)
        else:
            Collection.insert_one(file_data)
            
        print("guardado exitosamente")

    except Exception as e:
        print("no se pudo grabar:" + str(e))
