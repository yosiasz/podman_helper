import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
#sure=load_dotenv()
#TOKEN = os.getenv('INFLUX_TOKEN')
#URL = os.getenv('INFLUX_URL')
#ORG = os.getenv('INFLUX_ORG')
#print(TOKEN,URL,ORG)
TOKEN='lzrCQpbBXf_0hmrMQVmjnzrrAu4REPp5tqxGW1QLMXbP1jHZvAqXBu1OeEodZ8nhCEB2T9b0bIXr-CrKwUOnaA=='
ORG='research'
URL='localhost:8086'
bucket = "market"

"""
Write data into InfluxDB
"""
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
write_api = client.write_api(write_options=SYNCHRONOUS)  

col_list = ["date","close","volume","open","high","low"]
df = pd.read_csv("./data/gold.csv", usecols=col_list)
for index, row in df.iterrows():
    close =  float(row['close'])
    volume =  float(row['volume'])
    open = float(row['open'])
    _measurement = "market"
    high = float(row['high'])
    low = float(row['low'])
    date=row['date']
    
    #10/31/2023
    real_date = datetime.strptime(row['date'], '%m/%d/%Y').date()
    print(real_date)
    #print( )
    #df['Month'] = row['date'].dt.month 
    utc = datetime(real_date.year, real_date.month, real_date.day).replace(tzinfo=timezone.utc).timestamp()*10**9

    point = Point(_measurement) \
            .tag("tag1", "gold") \
            .field("close", close) \
            .field("volume", volume) \
            .field("open", open) \
            .field("high", high) \
            .field("low", low) \
            .time(real_date, WritePrecision.NS)

    #print(point)
    #write_api.write(bucket, ORG, point) 
write_api.__del__()

"""
Close client
"""
client.__del__()