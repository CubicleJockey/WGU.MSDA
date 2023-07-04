'''
Student: André Davis
Student ID: 010630641
Student Email: ada1962@wgu.edu
Class: D211 - Advanced Data Acquisition

Script:
    1. Create PostgreSQL database hospital_ratings
    2. Create database table ratings
    3. Read CSV data with Pandas, cleanup
    4. Use psycopg2 to execute SQL to insert data from CSV into ratings table

Example Execution on WGU OnDemand Lab Environment (Windows PowerShell ISE):


'''
import subprocess, sys, os
from typing import List, Tuple
from collections import namedtuple

# upgrade the pip installer to make sure this script completely works
# python.exe -m pip install --upgrade pip
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])

try:
    import psycopg2

    print('[psycopg2] is already installed')
except ImportError:
    print('[psycopg2] is not installed, installing now...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'])
    import psycopg2

    print('[psycopg2] is now installed and being used ')

try:
    import pandas as pd

    print('[pandas] is already installed')
except ImportError:
    print('[pandas] is not installed, installing now...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
    import pandas as pd

    print('[pandas] is now installed and being used')

try:
    import numpy as np

    print('[numpy] is already installed')
except ImportError:
    print('[numpy] is not installed, installing now...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
    import numpy as np

    print('[numpy] is now installed and being used')

'''
    Helper Functions
'''
assert len(sys.argv) > 2, 'PostgreSQL Username and Password must be supplied'

script_name = os.path.basename(__file__)
generated_sql = [f'''\*

D211 - Generated SQL from script {script_name}

*/
''']


def extract_user_parameters(inputs: List[str]) -> Tuple[str, str]:
    for param in inputs:
        if 'u:' in param:
            user = param.split(':')[1]

        if 'p:' in param:
            password = param.split(':')[1]

    return user, password


def create_database(postgres_username: str, postgres_password: str) -> None:
    conn = psycopg2.connect(
        # dbname="your_dbname",
        user=postgres_username,
        password=postgres_password,
        host="localhost",  # or another hostname if your DB isn't on your local machine
        port="5432"  # default postgres port
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Configure database table
    conn.autocommit = True
    drop_database_statement = 'DROP DATABASE IF EXISTS hospital_ratings;'
    generated_sql.append(f'{drop_database_statement}\n')

    cur.execute(drop_database_statement)

    create_database_statement = '''
CREATE DATABASE hospital_ratings
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

    '''

    generated_sql.append(create_database_statement)

    cur.execute(create_database_statement)

    # Retrieve query results
    # records = cur.fetchall()
    # print(records)

    # Close the cursor and connection
    cur.close()
    conn.close()


def extract_csv_to_table(postgres_username: str, postgres_password: str) -> None:
    # Skip header, we will use smaller better names for columns
    ratings = pd.read_csv('./Hospital_General_Information_2016_2020.csv')
    ratings['ZIP Code'] = ratings['ZIP Code'].astype('str').str.zfill(5)
    ratings['Year'] = ratings['Year'].astype('str')

    # print(match_ratings.info())

    # move columns
    ehr_column = 'Meets criteria for promoting interoperability of EHRs'

    # remove footnote columns
    remove_footnote_columns = [column_name for column_name in ratings.columns if 'footnote' in column_name]
    # print(remove_footnote_columns)
    ratings.drop(columns=remove_footnote_columns, inplace=True)

    ratings[ehr_column].fillna('N', inplace=True)

    ratings[ehr_column] = ratings[ehr_column].map({'Y': True, 'N': False}).astype(np.bool_)
    ratings['Emergency Services'] = ratings['Emergency Services'].map({'Yes': True, 'No': False}).astype(np.bool_)

    # print(ratings.info())

    conn = psycopg2.connect(
        dbname="hospital_ratings",
        user=postgres_username,
        password=postgres_password,
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
    generated_sql.append(f'{drop_table_statement}\n')

    cur.execute(drop_table_statement)
    # conn.commit()

    formatted_table_create_columns = ', \n'.join(
        [f'"{column_info.Column}" {column_info.DataType}' for column_info in table_columns])
    # print(formatted_columns)

    create_table_statement = f"CREATE TABLE {table_name}({formatted_table_create_columns});"
    generated_sql.append(f'{create_table_statement}\n')

    # print(create_table_statement)
    cur.execute(create_table_statement)
    # conn.commit()

    insert_columns = ', '.join([f'"{column}"' for column in adjusted_columns])
    for _, row in ratings.iterrows():
        insert_statement = f'''
        INSERT INTO ratings({insert_columns})
        VALUES(%s, %s, %s, %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s);
        '''

        insert_values = (row['FacilityID'], row['FacilityName'], row['Address'], row['City'], row['State'],
                         row['ZipCode'], row['CountyName'], row['Phone'], row['HospitalType'], row['HospitalOwnership'],
                         row['EmergencyServices'], row['MeetsCriteriaForInteropEHRs'], row['HospitalOverallRating'],
                         row['MortalityNationalComparison'], row['SafetyOfCareNationalComparison'],
                         row['ReadmissionNationalComparison'],
                         row['PatientExperienceNationalComparison'], row['EffectivenessOfCareNationalComparison'],
                         row['TimelinessOfCareNationalComparison'],
                         row['EfficientUseOfMedicalImagingNationalComparison'], row['Year'])

        adjusted_values_for_output = tuple(s.replace("'", "''") if isinstance(s, str) else s for s in insert_values)

        generated_sql.append(f'''INSERT INTO ratings({insert_columns})
VALUES(%s, '%s', '%s', '%s',  '%s', %s,  '%s',  '%s',  '%s',  '%s',  %s,  %s,  '%s',  '%s',  '%s',  '%s',  '%s',  '%s',  '%s',  '%s',  %s);
        ''' % adjusted_values_for_output)

        cur.execute(insert_statement, insert_values)

    cur.close()
    conn.close()


'''
Execute Program    
'''
user, password = extract_user_parameters(sys.argv)
create_database(user, password)
extract_csv_to_table(user, password)

generated_sql_file = '.\wgu-generated-sql-for-additional-dataset.sql'

with open(generated_sql_file, 'w') as file:
    for statement in generated_sql:
        file.write(f'{str(statement)}\n')

print(f'The PostgreSQL that was generated during this script run can be found at: {generated_sql_file}')

# print(generated_sql)

# execute_pgcsv(user, password)
