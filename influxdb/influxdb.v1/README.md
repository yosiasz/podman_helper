This is the original influxdb accessed only via cli

py -m pip install influxdb

# DDL

CREATE DATABASE NOAA_water_database
CREATE DATABASE boombam

# DML

# CONTEXT-DATABASE: NOAA_water_database

h2o_feet is measurement
location is tag (indexed)
water_level and level description are fields
the last numeric bit is timestamp ns

h2o_feet,location=coyote_creek water_level=7.234,level\ description="between 6 and 9 feet" 1566002520

# How to add data to influxdbv1
