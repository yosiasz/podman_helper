import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from dotenv import load_dotenv

import os
sure=load_dotenv()
TOKEN = os.getenv('INFLUX_TOKEN')
URL = os.getenv('INFLUX_URL')
ORG = os.getenv('INFLUX_ORG')
#print(TOKEN,URL,ORG)
print(datetime.utcnow().timestamp()*10**9)
bucket = "speedo"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["_time","_value","DeviceID","_field","_measurement","host","topic"]
df = pd.read_csv("./data/wakanda.csv", usecols=col_list)
for index, row in df.iterrows():
    _time =  row['_time']
    _field =  row['_field']
    _value =  row['_value']
    DeviceID = row['DeviceID']
    _measurement = row['_measurement']
    host = row['host']
    topic = row['topic']
    
    point = Point(_measurement) \
                .tag("tag1", "statuses") \
                .field(_field, _value) \
                .field("DeviceID", DeviceID) \
                .field("host", host) \
                .field("topic", topic) \
                .time(_time, WritePrecision.NS)

    print(point)
    #write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()