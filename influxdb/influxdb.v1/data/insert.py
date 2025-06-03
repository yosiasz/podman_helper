from influxdb import InfluxDBClient

# Connect to InfluxDB 1.8
client = InfluxDBClient(
    host='localhost',
    port=8086,
    username='admin',  # remove or comment out if no auth
    password='TechOps!'   # remove or comment out if no auth
)

# Create database if it doesn't exist
db_name = 'moongoo'
if db_name not in [db['name'] for db in client.get_list_database()]:
    client.create_database(db_name)

client.switch_database(db_name)

# Define data point in InfluxDB 1.x format
json_body = [
    {
        "measurement": "SensorData",
        "tags": {
            "sensorID": "office",
            "station": "Pumping Station H"
        },
        "fields": {
            "leak_status": 23.5
        }
    }
]

# Write the data
client.write_points(json_body)

# Query the data
result = client.query('SELECT * FROM SensorData')
for point in result.get_points():
    print(point)
