
import json
from argparse import ArgumentParser
import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import json_util, ObjectId

client = MongoClient('mongodb://localhost:27017')
try:
    client.admin.command('ismaster')
    print('MongoDB connection: Success')
except ConnectionFailure as cf:
    print('MongoDB connection: failed', cf)

DBS = ['ejemploE']

client2 = MongoClient('mongodb+srv://byron04:magooscuro@cluster0.dte47.mongodb.net/test')
try:
    client2.admin.command('ismaster')
    print('MongoDB connection atlas: Success')
except ConnectionFailure as cf:
    print('MongoDB connection atlas: failed', cf)

mongoDB = client2.get_database('examen')
db2 = mongoDB.coleccionesExa

for db in DBS:
    if db in ('examen'):
        cols = client[db].list_collection_names()
        for col in cols:
            print('Querying documents from collection {} in database {}'.format(col, db))
            for x in client[db][col].find():
                try:
                    documents = json.loads(json_util.dumps(x))
                    db2.insert_many(documents)
                    print("SAVE")
                    print(documents)
                except Exception as error:
                    print ("Error saving data: %s" % str(error))
