'''
Student: André Davis
Student ID: 010630641
Student Email: ada1962@wgu.edu
Class: D211 - Advanced Data Acquisition

Script:
    1. Create PostgreSQL database hospital_ratings
    2. Install pgcsv to perform CSV import into hospital_ratings
'''
import subprocess
import sys
from typing import List, Tuple

try:
    import psycopg2
    print('psycopg2 is already installed')
except ImportError:
    print('psycopg2 is not installed, installing now...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'])
    
'''
    Helper Functions
'''
assert len(sys.argv) >  2, 'PostgreSQL Username and Password must be supplied'+

def extract_user_paramters(userArgs: List[str]) -> Tuple[str, str]:
     for param in userArgs:
         if 'u:' in param:
             user = param.split(':')[1]
         
         if 'p:' in param:
             password = param.split(':')[1]
             
     return user, password
        
def CreateDatabase(user: str, password: str) -> None:       
    conn = psycopg2.connect(
        #dbname="your_dbname", 
        user=user, 
        password=password, 
        host="localhost",  # or another hostname if your DB isn't on your local machine
        port="5432"  # default postgres port
    )
    
    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    # Configure database table
    conn.autocommit = True
    cur.execute('DROP DATABASE IF EXISTS hospital_ratings;')
    
    cur.execute('''
    CREATE DATABASE hospital_ratings
        WITH
        OWNER = postgres
        ENCODING = 'UTF8'
        LC_COLLATE = 'English_United States.1252'
        LC_CTYPE = 'English_United States.1252'
        TABLESPACE = pg_default
        CONNECTION LIMIT = -1
        IS_TEMPLATE = False;
    ''')
    
    # Retrieve query results
    #records = cur.fetchall()
        #print(records)
    
    # Close the cursor and connection
    cur.close()
    conn.close()
    
    
'''
Execute Program    
'''
user, password = extract_user_paramters(sys.argv)
CreateDatabase(user, password)