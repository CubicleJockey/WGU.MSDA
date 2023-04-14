CREATE TABLE service(
    customer_id TEXT NOT NULL   
    ,internet_service TEXT NOT NULL   
    ,phone BOOLEAN NOT NULL DEFAULT FALSE   
    ,multiple BOOLEAN NOT NULL DEFAULT FALSE   
    ,online_security BOOLEAN NOT NULL DEFAULT FALSE   
    ,online_backup BOOLEAN NOT NULL DEFAULT FALSE   
    ,device_protection BOOLEAN NOT NULL DEFAULT FALSE 
    ,tech_support BOOLEAN NOT NULL DEFAULT FALSE   
    ,FOREIGN KEY(customer_id) REFERENCES customer(customer_id) 
);