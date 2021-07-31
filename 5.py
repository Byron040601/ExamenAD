from pymongo import MongoClient
import pandas as pd
import bson
from bson.raw_bson import RawBSONDocument
from pymongo.errors import ConnectionFailure
import sqlite3
con = sqlite3.connect("examen.db")

Client = MongoClient('mongodb://localhost:27017/')
try:
    Client.admin.command('ismaster')
    print('MongoDB connection: Succes')
except ConnectionFailure as cf:
    print('MongoDB connection: Succes', cf)

db = Client["ejemploE"]
Collection = db["facebookOlimpiadas"]

df = pd.read_csv('Oscar.Arr_1627690423990.csv', index_col=0)
df2 = pd.read_csv('olympics_1627690401747.csv', index_col=0)

#df.to_sql('oscar2', con)
df2.to_sql('olympics', con)

print(df)
print(df2)
