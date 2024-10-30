#from influxdb_client import InfluxDBClient, WriteOptions
from influxdb import InfluxDBClient
import pandas as pd

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'boombam')

""" json_body = [
    {
        "measurement": "cpu_load_short",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
        }
    }
]
client.write_points(json_body) """
#Time,AntLat,AntLong,DraghSBLat,DraghSBLong,Total
col_list = ["time","value"]
df = pd.read_csv('data.csv', usecols=col_list)

for index, row in df.iterrows():
    time =  row['time']
    value = row['value']
    print(time,value)
    json_body = [
    {
        "measurement": "cpu_load_short",
        "time": time,
        "fields": {
            "value": value
        }
    }
    ]
    client.write_points(json_body)

""" with InfluxDBClient.from_env_properties() as client:
    for df in pd.read_csv("data.csv", chunksize=1_000):
        with client.write_api() as write_api:
            try:
                write_api.write(
                    record=df,
                    bucket="boombam",
                    data_frame_measurement_name="stocks",
                    data_frame_tag_columns=["symbol"],
                    data_frame_timestamp_column="date",
                )
            except InfluxDBError as e:
                print(e) """