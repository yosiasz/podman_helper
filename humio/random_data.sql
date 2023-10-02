with randowvalues
    as(
		select 1 id, CAST(RAND(CHECKSUM(NEWID()))*10000 as int) randomnumber
		union  all
		select id + 1, CAST(RAND(CHECKSUM(NEWID()))*10000 as int)  randomnumber
		from randowvalues
		where 
          id < 1000
      )
 
 
 
    select concat('(''', convert(varchar(50), dateadd(dd, id, GETUTCDATE()), 121),  ''' ,', 
	
	case 
	   when id % 2 = 0 then 1000
	   else id
	   end
	
	, ', ', randomnumber/100 * 1.33, '),')
    from randowvalues
    OPTION(MAXRECURSION 0)