import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
#from dotenv import load_dotenv

import os
#sure=load_dotenv()
TOKEN = 'WlnO0H0bDTkdskSHPmIc9Y49XXZkxqyJWzLjeamMvl3kez0JexEspvJ16DP3kRNBHwK7ehD0RC-jJaMpqKfqrg=='
#os.getenv('INFLUX_TOKEN')
URL = 'localhost:8086'
#os.getenv('INFLUX_URL')
ORG = 'research'
#os.getenv('INFLUX_ORG')

#,
def load_lidar_vertices():
    bucket = "lidar_vertices"

    """
    Write data into InfluxDB
    """
    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
    write_api = client.write_api(write_options=SYNCHRONOUS)  
    #_time,_value,_field,_measurement,machine,name
    #2024-10-08T01:53:52.953284608Z,"[{""x"": -18.27, ""y"": 10.88}, {""x"": -10.69, ""y"": 10.88}, {""x"": -11.02, ""y"": 6.87}, {""x"": -18.6, ""y"": 6.76}, {""x"": -18.27, ""y"": 10.88}]",
    # vertices,zones,apache2-NUC9i9,Zone-1
    col_list = ["_time","_value","_field","_measurement","machine","name"]
    df = pd.read_csv("./data/lidar_vertices.csv", usecols=col_list)
    for index, row in df.iterrows():
        _time =  row['_time']
        _field =  row['_field']
        _value =  row['_value']
        _measurement = row['_measurement']
        machine = row['machine']
        name = row['name']
        
        point = Point(_measurement) \
                    .field(_field, _value) \
                    .field('machine',machine) \
                    .field('name',name) \
                    .time(_time, WritePrecision.NS)

        print(point)
        #write_api.write(bucket, ORG, point) 
    write_api.__del__()

    """
    Close client
    """
    client.__del__()

def load_bie():
    bucket = "bie"

    """
    Write data into InfluxDB
    """
    client = InfluxDBClient(url=URL, token=TOKEN, org=ORG, debug=True)
    write_api = client.write_api(write_options=SYNCHRONOUS)  
    #result,table,_time,_value,baseline
    #0,2024-04-11T08:28:42.073Z,3339,cspcd.cis_master.10189
    col_list = ["table","_time","_value","baseline"]
    df = pd.read_csv("./data/bobo.csv", usecols=col_list)
    for index, row in df.iterrows():
        _time =  row['_time']
        _field =  row['baseline']
        _value =  float(row['_value'])
        
        point = Point('bie_bie') \
                    .tag("tag1", "bie") \
                    .field(_field, _value) \
                    .time(_time, WritePrecision.NS)

        print(point)
        write_api.write(bucket, ORG, point) 
    write_api.__del__()

    """
    Close client
    """
    client.__del__()
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
    #load_parking_lat()
    #load_parking_lon()
    #load_bie()
    load_lidar_vertices()

if __name__ == '__main__':
    main()