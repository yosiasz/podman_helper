""" import prestodb
conn=prestodb.dbapi.connect(
    host='localhost',
    port=8080,
    user='root',
    catalog='tpch',
    schema='sf1',
    #http_scheme='https',
    #auth=prestodb.auth.BasicAuthentication("root", ""),
)
cur = conn.cursor()
cur.execute('select *, now() from tpch.sf1.orders limit 10')
rows = cur.fetchall() """

import pymongo
import json

url = "mongodb://root:example@mongo:27017/"
client = pymongo.MongoClient("mongodb://root:example@127.0.0.1:27017/")
db = client["grafana"]
col = db["customers"]

mydata = { "name": "John", "address": "Highway 37" }

fp = open('customers.json')

data = json.load(fp)

print(data)

x = col.insert_one(data)