SELECT l.state 
	  ,CASE WHEN( 
		      COUNT(CASE s.internet_service WHEN 'Fiber Optic' THEN 1 ELSE NULL END)  
		    > COUNT(CASE s.internet_service WHEN 'DSL' THEN 1 ELSE NULL END) 
	  	  )  
		  THEN 'More Fiber' ELSE 'More DSL' END AS MoreServiceOf 
 
FROM customer AS c 
	INNER JOIN location AS l ON l.location_id = c.location_id 
	  INNER JOIN service AS s ON s.customer_id = c.customer_id 
WHERE s.internet_service IN ('Fiber Optic', 'DSL') 
GROUP BY l.state 
ORDER BY l.state; 