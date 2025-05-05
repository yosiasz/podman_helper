--CONVERT(varchar(50), GETUTCDATE(), 127)
select  CAST(DATEDIFF(Second,{d '1970-01-01'},'2016-05-11 00:01:02.000') AS DECIMAL) * 1000000000 AS NanoSeconds
--1465839830100400200 
declare @date datetime = '2016-05-11 00:01:02.000'
select DATEDIFF(second,{d '1970-01-01'},@date)

SELECT DATEADD(S, CONVERT(int,LEFT(1462924862735870900, 10)), '1970-01-01')
SELECT dateadd(S, @date, '1970-01-01 00:00:00') 

data = from(bucket: "crypto")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "ethusd")
  |> filter(fn: (r) => r["_field"] == "price")
  |> filter(fn: (r) => r["currency"] == "usd")

  low = data
  |> min()

 high = data
|> max()

  open = data
  |> first()

  close = data
    |> last()

union(tables: [low, open, close, high])
|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")  
 |> drop(columns: ["_start", "_stop", "_measurement", "type"])
 |> map(fn: (r) => ({ r with newColumn: r._value * 2 }))
 
 )

  low = data
  |> min()

 high = data
|> max()

  open = data
  |> first()

  close = data
    |> last()

union(tables: [low, open, close, high])
 |> map(
 fn: (r) => ({time: r._time, open: r._value})
 )
select dateadd(S, @date, '1970-01-01')
select concat(
'ethusd,',
'currency=usd price=', object_id * 0.75, ' ',
cast(DATEDIFF(second,{d '1970-01-01'},dateadd(hh,object_id*-1,getutcdate())) as decimal) * 1000000000
) , dateadd(hh,object_id*-1,getutcdate()),
concat(
'ethusd,',
'currency=usd price=', object_id * 0.75, 'd ',
CONVERT(varchar(50),dateadd(hh,object_id*-1,getutcdate()), 127)
) , dateadd(hh,object_id*-1,getutcdate())
from sys.objects
where object_id between 1 and 30
--ethusd,symbol=usd price=2.25 1699205981
--measurement,tag1=val1,tag2=val2 field1="v1",field2=1i 0000000000000000000
--sensors,device=AK location_tracker_latitude=63.5888 1698083957
/*
#datatype measurement,dateTime:RFC3339,double,integer,double,double,double
name,Date,Close,Volume,Open,High,Low
gold,11/03/2023,176.65,79829250,174.24,176.82,173.35
gold,11/02/2023,177.57,77334750,175.52,177.78,175.46
gold,11/01/2023,173.97,56934910,171.00,174.23,170.12
gold,10/31/2023,170.77,44846020,169.35,170.90,167.90
gold,10/30/2023,170.29,51130960,169.02,171.17,168.87
gold,10/27/2023,168.22,58499130,166.91,168.96,166.83
gold,10/26/2023,166.89,70625260,170.37,171.3775,165.67
gold,10/25/2023,171.10,57156960,171.88,173.06,170.65
gold,10/24/2023,173.44,43816640,173.05,173.67,171.45
gold,10/23/2023,173.00,55980110,170.91,174.01,169.93
gold,10/20/2023,172.88,64244030,175.31,175.42,172.64
gold,10/19/2023,175.46,59302860,176.04,177.84,175.19
gold,10/18/2023,175.84,54764380,175.58,177.575,175.11
gold,10/17/2023,177.15,57549350,176.645,178.42,174.80
gold,10/16/2023,178.72,52516980,176.75,179.075,176.51
gold,10/13/2023,178.85,51456080,181.42,181.93,178.14
gold,10/12/2023,180.71,56743120,180.07,182.34,179.04
gold,10/11/2023,179.80,47551100,178.20,179.85,177.60
gold,10/10/2023,178.39,43698020,178.10,179.72,177.95
gold,10/09/2023,178.99,42390770,176.81,179.05,175.80
gold,10/06/2023,177.49,57266680,173.80,177.99,173.18
gold,10/05/2023,174.91,48527920,173.79,175.45,172.68

*/