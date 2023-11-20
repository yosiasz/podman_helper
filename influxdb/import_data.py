import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
from dotenv import load_dotenv

import os
sure=load_dotenv()
TOKEN = ''
#os.getenv('INFLUX_TOKEN')
URL = os.getenv('INFLUX_URL')
ORG = os.getenv('INFLUX_ORG')


def load_speed():
    #print(datetime.utcnow().timestamp()*10**9)
    bucket = "gpstracking_db"

    """
    Write data into InfluxDB
    """
    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
    write_api = client.write_api(write_options=SYNCHRONOUS)  

    #col_list = ["_time","_value","DeviceID","_field","_measurement","host","topic"]
    col_list = ["_time","_value","_field","_measurement"]
    df = pd.read_csv("./data/clem1.csv", usecols=col_list)
    for index, row in df.iterrows():
        _time =  row['_time']
        _field =  row['_field']
        _value =  float(row['_value'])
        _measurement = row['_measurement']
        
        point = Point(_measurement) \
                    .tag("tag1", "geo") \
                    .field(_field, _value) \
                    .time(_time, WritePrecision.NS)

        print(point)
        write_api.write(bucket, ORG, point) 
    write_api.__del__()

    """
    Close client
    """
    client.__del__()

def load_parking_lon():
#print(datetime.utcnow().timestamp()*10**9)
    bucket = "parking"

    """
    Write data into InfluxDB
    """
    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
    write_api = client.write_api(write_options=SYNCHRONOUS)  

    col_list = ["measurement","tag1","location",".parking-position.longitude","time"]
    df = pd.read_csv("./data/parking_lon.csv", sep=',', usecols=col_list, encoding='latin-1')
    for index, row in df.iterrows():
        _measurement = row['measurement']
        tag1 =  row['tag1']        
        location =  row['location']
        _value =  float(row['.parking-position.longitude'])
        _time =  row['time']
        
        point = Point(_measurement) \
                    .tag("tag1", tag1) \
                    .field("location", location) \
                    .field("value", _value) \
                    .time(_time, WritePrecision.NS)

        print(point)
        write_api.write(bucket, ORG, point) 
    write_api.__del__()

    """
    Close client
    """
    client.__del__()

def load_parking_lat():
#print(datetime.utcnow().timestamp()*10**9)
    bucket = "parking"

    """
    Write data into InfluxDB
    """
    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
    write_api = client.write_api(write_options=SYNCHRONOUS)  

    col_list = ["measurement","tag1","location",".parking-position.latitude","time"]
    df = pd.read_csv("./data/parking_lat.csv", sep=',', usecols=col_list, encoding='latin-1')
    for index, row in df.iterrows():
        _measurement = row['measurement']
        tag1 =  row['tag1']        
        location =  row['location']
        _value =  float(row['.parking-position.latitude'])
        _time =  row['time']
        
        point = Point(_measurement) \
                    .tag("tag1", tag1) \
                    .field("location", location) \
                    .field("value", _value) \
                    .time(_time, WritePrecision.NS)

        print(point)
        write_api.write(bucket, ORG, point) 
    write_api.__del__()

    """
    Close client
    """
    client.__del__()    
def main():
    load_parking_lat()
    load_parking_lon()

if __name__ == '__main__':
    main()