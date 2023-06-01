Go into container
	podman exec -u 0 -it 9d74ff2cde89  /bin/bash
	root@9d74ff2cde89:/# cqlsh

	
CREATE KEYSPACE IF NOT EXISTS homeassistant WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'datacenter1' : 3 };

USE homeassistant;

CREATE TABLE temperature (
    sensor_id uuid,
    registered_at timestamp,
    temperature int,
    location text,
    PRIMARY KEY ((sensor_id), registered_at)
);


insert into temperature (sensor_id, registered_at, temperature, location) values (99051fe9-6a9c-46c2-b949-38ef78858dd0, '2020-04-01T11:21:59.001+0000', 18, 'kitchen');
insert into temperature (sensor_id, registered_at, temperature, location) values (99051fe9-6a9c-46c2-b949-38ef78858dd0, '2020-04-01T11:22:59.001+0000', 19, 'kitchen');
insert into temperature (sensor_id, registered_at, temperature, location) values (99051fe9-6a9c-46c2-b949-38ef78858dd0, '2020-04-01T11:23:59.001+0000', 20, 'kitchen');


SELECT sensor_id, CAST(temperature as double), registered_at FROM homeassistant.temperature WHERE sensor_id IN (99051fe9-6a9c-46c2-b949-38ef78858dd1, 99051fe9-6a9c-46c2-b949-38ef78858dd0) AND registered_at > $__timeFrom and registered_at < $__timeTo
