this is the original influxdb accessed only via cli



# DDL

CREATE DATABASE NOAA_water_database
<<<<<<< HEAD
CREATE DATABASE boombam
=======
>>>>>>> 0291f04b7301dbe09a72c1acfbf79523e10ffb99

# DML

# CONTEXT-DATABASE: NOAA_water_database
h2o_feet is measurement
location is tag (indexed)
water_level and level description are fields

h2o_feet,location=coyote_creek water_level=8.120,level\ description="between 6 and 9 feet" 1566000000
h2o_feet,location=coyote_creek water_level=8.005,level\ description="between 6 and 9 feet" 1566000360
h2o_feet,location=coyote_creek water_level=7.887,level\ description="between 6 and 9 feet" 1566000720
h2o_feet,location=coyote_creek water_level=7.762,level\ description="between 6 and 9 feet" 1566001080
h2o_feet,location=coyote_creek water_level=7.635,level\ description="between 6 and 9 feet" 1566001440
h2o_feet,location=coyote_creek water_level=7.500,level\ description="between 6 and 9 feet" 1566001800
h2o_feet,location=coyote_creek water_level=7.372,level\ description="between 6 and 9 feet" 1566002160
h2o_feet,location=coyote_creek water_level=7.234,level\ description="between 6 and 9 feet" 1566002520