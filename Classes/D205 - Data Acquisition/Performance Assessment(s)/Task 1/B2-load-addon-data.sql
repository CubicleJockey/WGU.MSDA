COPY public.service ( 
	 customer_id 
	,internet_service 
     ,phone 
    ,multiple 
	,online_security 
    ,online_backup 
    ,device_protection 
	,tech_support)  
FROM 'C:\LabFiles\Services.csv'  
DELIMITER ','  
CSV  
HEADER  
QUOTE '"'  
ESCAPE ''''  
FORCE NOT NULL customer_id 
              ,internet_service 
              ,phone 
              ,multiple 
              ,online_security 
              ,online_backup 
              ,device_protection 
              ,tech_support; 