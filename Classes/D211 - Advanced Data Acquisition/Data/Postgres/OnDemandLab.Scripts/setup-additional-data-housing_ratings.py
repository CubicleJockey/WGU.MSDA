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
from collections import namedtuple


try:
    import psycopg2
    print('[psycopg2] is already installed')
except ImportError:
    print('[psycopg2] is not installed, installing now...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'])

try:
    import pandas as pd
    print('[pandas] is already installed')
except ImportError:
    print('[pandas] is not installed, installing now...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
    
try:
    import numpy as np
    print('[numpy] is already installed')
except ImportError:
    print('[numpy] is not installed, installing now...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])

'''
    Helper Functions
'''
assert len(sys.argv) >  2, 'PostgreSQL Username and Password must be supplied'

def extract_user_paramters(userArgs: List[str]) -> Tuple[str, str]:
     for param in userArgs:
         if 'u:' in param:
             user = param.split(':')[1]
         
         if 'p:' in param:
             password = param.split(':')[1]
             
     return user, password
        
def create_database(user: str, password: str) -> None:
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
    
def extract_csv_to_table(user: str, password: str) -> None:
    #Skip header, we will use smaller better names for columns
    ratings = pd.read_csv('./Hospital_General_Information_2016_2020.csv')
    ratings['ZIP Code'] = ratings['ZIP Code'].astype('str').str.zfill(5)
    ratings['Year'] = ratings['Year'].astype('str')

    #print(match_ratings.info())

    #move columns
    ehr_column = 'Meets criteria for promoting interoperability of EHRs'

    #remove footnote columns
    remove_footnote_columns = [column_name for column_name in ratings.columns if 'footnote' in column_name]
    print(remove_footnote_columns)
    ratings.drop(columns=remove_footnote_columns, inplace=True)

    ratings[ehr_column].fillna('N', inplace=True)

    ratings[ehr_column] = ratings[ehr_column].map({'Y': True, 'N': False }).astype(np.bool_)
    ratings['Emergency Services'] = ratings['Emergency Services'].map({'Yes': True, 'No': False}).astype(np.bool_)

    #print(ratings.info())

    conn = psycopg2.connect(
        dbname="hospital_ratings",
        user=user,
        password=password,
        host="localhost",  # or another hostname if your DB isn't on your local machine
        port="5432"  # default postgres port
    )

    # Open a cursor to perform database operations
    conn.autocommit = True
    cur = conn.cursor()

    table_name = 'ratings'

    dataframe_columns = ratings.columns.tolist()

    ColumnInfo = namedtuple('ColumnInfo', ['Column', 'DataType'])
    table_columns = [
        ColumnInfo('FacilityID', 'VARCHAR(50) NOT NULL'),
        ColumnInfo('FacilityName', 'VARCHAR(500) NOT NULL'),
        ColumnInfo('Address', 'VARCHAR(250) NOT NULL'),
        ColumnInfo('City', 'VARCHAR(100) NOT NULL'),
        ColumnInfo('State', 'VARCHAR(2) NOT NULL'),
        ColumnInfo('ZipCode', 'VARCHAR(10) NOT NULL'),
        ColumnInfo('CountyName', 'VARCHAR(50) NULL'),
        ColumnInfo('Phone', 'VARCHAR(15) NOT NULL'),
        ColumnInfo('HospitalType', 'VARCHAR(250) NOT NULL'),
        ColumnInfo('HospitalOwnership', 'VARCHAR(250) '),
        ColumnInfo('EmergencyServices', 'BOOLEAN NOT NULL'),
        ColumnInfo('MeetsCriteriaForInteropEHRs', 'BOOLEAN NOT NULL'),
        ColumnInfo('HospitalOverallRating', 'VARCHAR(14) NOT NULL'),
        ColumnInfo('MortalityNationalComparison', 'VARCHAR(30) NOT NULL'),
        ColumnInfo('SafetyOfCareNationalComparison', 'VARCHAR(30) NOT NULL'),
        ColumnInfo('ReadmissionNationalComparison', 'VARCHAR(30) NOT NULL'),
        ColumnInfo('PatientExperienceNationalComparison', 'VARCHAR(30) NOT NULL'),
        ColumnInfo('EffectivenessOfCareNationalComparison', 'VARCHAR(30) NOT NULL'),
        ColumnInfo('TimelinessOfCareNationalComparison', 'VARCHAR(30) NOT NULL'),
        ColumnInfo('EfficientUseOfMedicalImagingNationalComparison', 'VARCHAR(30) NOT NULL'),
        ColumnInfo('Year', 'VARCHAR(4)'),
    ]


    adjusted_columns = []
    for index, df_column in enumerate(dataframe_columns):
        ratings.rename(columns={df_column: table_columns[index].Column}, inplace=True)
        adjusted_columns.append(table_columns[index].Column)

    print(ratings.info())

    drop_table_statement = f'DROP TABLE IF EXISTS {table_name};'
    cur.execute(drop_table_statement)
    #conn.commit()

    formatted_table_create_columns = ', \n'.join([f'"{column_info.Column}" {column_info.DataType}' for column_info in table_columns])
    #print(formatted_columns)

    create_table_statement = f"CREATE TABLE {table_name}({formatted_table_create_columns});"
    #print(create_table_statement)
    cur.execute(create_table_statement)
    #conn.commit()


    for _, row in ratings.iterrows():
        insert_statement = f'''
        INSERT INTO ratings({', '.join(adjusted_columns)})
        VALUES('{row['FacilityID']}', '{row['FacilityName']}', '{row['Address']}', '{row['City']}', '{row['State']}',
               '{row['ZipCode']}', '{row['CountyName']}', '{row['Phone']}', '{row['HospitalType']}', '{row['HospitalOwnership']}',
                {row['EmergencyServices']}, {row['MeetsCriteriaForInteropEHRs']}, '{row['HospitalOverallRating']}', '{row['MortalityNationalComparison']}',
               '{row['SafetyOfCareNationalComparison']}', '{row['ReadmissionNationalComparison']}', '{row['PatientExperienceNationalComparison']}',
               '{row['EffectivenessOfCareNationalComparison']}', '{row['TimelinessOfCareNationalComparison']}', '{row['EfficientUseOfMedicalImagingNationalComparison']}',
               '{row['Year']}'
        );
        '''

        print(insert_statement)

        cur.execute(insert_statement)


    cur.close()
    conn.close()
    
'''
Execute Program    
'''
user, password = extract_user_paramters(sys.argv)
create_database(user, password)
extract_csv_to_table(user, password)
#execute_pgcsv(user, password)