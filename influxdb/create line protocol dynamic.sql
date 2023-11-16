use grafana
go

declare @date2 varchar(200) =  convert(varchar(200), GETUTCDATE(), 127 )

DECLARE @date datetime
    SELECT @date = '2/11/1990 12:03:25.310 AM'

select CAST(DATEDIFF(Second,@date,GETDATE()) AS DECIMAL) * 1000000000 AS NanoSeconds

select concat('sensors,device=',state,
' location_tracker_latitude=', lat,' 1698083957'), *
From us_states
union all
select concat('sensors,device=',state,
' location_tracker_longitude=', lon, ' 1698083957'), *
From us_states
union all
select concat('sensors,device=',state,
' odometer=', 132, ' 1698083957'), *
From us_states