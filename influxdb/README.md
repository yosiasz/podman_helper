podman pull 
podman run -p 8086:8086 -v myInfluxVolume:/var/lib/influxdb2 influxdb:1.8.10-alpine

podman run -p 8086:8086 -v //docker_volumes/influxdb:/var/lib/influxdb influxdb:1.8 

podman run -p 8086:8086 -v $PWD/influxdb/influxdb.conf:/etc/influxdb/influxdb.conf influxdb:1.8

podman run -p 8086:8086 -v $PWD/influxdb:/etc/influxdb/influxdb.conf influxdb:1.8