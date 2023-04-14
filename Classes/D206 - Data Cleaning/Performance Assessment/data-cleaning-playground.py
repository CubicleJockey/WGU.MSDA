import numpy as np
import pandas as pd
import sys
import os
import missingno as msno
import matplotlib.pyplot as plt
import pprint

from pathlib import Path

print(f"Current Python Version: {sys.version}")

path = Path(__file__).parent.resolve()
print(path)
file = os.path.join(path, './medical_raw_data.csv')

use_columns = range(1, 53) #Skip first column
medical_data = pd.read_csv(file, header = 0, usecols = use_columns)

convert_to_category = {
    'City': 'category',
    'State': 'category',
    'County': 'category',
    'Area': 'category',
    'Timezone': 'category',
    'Job': 'category',
    'Education': 'category',
    'Employment': 'category',
    'Marital': 'category',
    'Gender': 'category',
    'Initial_admin': 'category',
    'Complication_risk': 'category',
    'Services': 'category'
}
medical_data = medical_data.astype(convert_to_category)

medical_data.hist(column='Income')


print(medical_data[['Overweight', 'Anxiety', 'Soft_drink']].mode())


# #Interquartile Range (IQR)
# #Outliers are values falling outside the 25th and 75th percentile
# #https://www.vedantu.com/maths/interquartile-range
# def getOutliers_IQR(dataframe, columnName):
#     variableOfInterest = dataframe[columnName]

#     quantile1 = variableOfInterest.quantile(0.25)
#     quantile3 = variableOfInterest.quantile(0.75)

#     interquartile_range = quantile3 - quantile1

#     below_25_select = variableOfInterest < (quantile1 - 1.5 * interquartile_range)
#     above_75_select = variableOfInterest > (quantile3 + 1.5 * interquartile_range)

#     outliers = variableOfInterest[below_25_select | above_75_select]

#     summary = {
#         'Variable': [columnName],
#         'Total_Outliers': [outliers.count()],
#         'Min_Value': [outliers.min()],
#         'Max_Value': [outliers.max()]
#     }
#     summary_dataframe = pd.DataFrame(summary)
    
#     summary_dataframe.fillna(value = 0)

#     return summary_dataframe

# result = getOutliers_IQR(medical_data, 'Children')
# print(result)

# big_populations = medical_data['Population'] > 120000
# print(medical_data[big_populations][['State', 'City', 'Population']])




#print(medical_data.info(verbose=True))

# def updateCategoryCasingToLower(series, columnName):
#     series[columnName] = series[columnName].str.lower()
#     series[columnName] = series[columnName].str.strip()

#     return series[columnName]

# for key in convert_to_category.keys():
#     medical_data[key] = updateCategoryCasingToLower(medical_data, key)

#print(medical_data)

# def findDuplicatesIgnoreCase(series, columnName):
#     tempColumn = 'AsLower'
#     df = pd.DataFrame(series[columnName])
#     df[tempColumn] = df[columnName].astype(str).str.lower()

#     description = df[tempColumn].describe()
    
#     if (description['count'] > description['unique']):
#         print('Duplicate Values found.')
#     else:
#         print('No duplicates found.')
        

#     columns = {
#         columnName: df[columnName].unique(),
#         tempColumn: df[tempColumn].unique()
#     }
#     #distinct_values = series[columnName].unique() #returns a Numpy Array
#     return columns


# area_corrected_casing = updateCategoryCasingToLower(medical_data, 'Area')
# print(area_corrected_casing)
# pprint.pprint(areaDuplicates)

# medical_data['AreaAsLower'] = medical_data['Area'].astype(str).str.lower()
# print(medical_data[['Area', 'AreaAsLower']])

#areaDuplicates = findDuplicatesIgnoreCase(medical_data, 'Area')
# #print(f"NumPy array datatype '{areaDuplicates.dtype}'")
# print(type(areaDuplicates))
# print(areaDuplicates)


# test = {
#     'A': ['hi', 'Hi', 'there', 'their', "they're"],
#     'B': ['a','B','c','C', 'd']
# }

# test = pd.DataFrame(test)

# print(test)


# pprint.pprint(dupsA)
# pprint.pprint(dupsB)


# areaCounts = getValueCount(medical_data, 'Area')
# print(type(areaCounts))
# print(areaCounts)

# countyCounts = getValueCount(medical_data, 'County')
# keys = countyCounts.keys()
# print(type(keys))
# for key in keys:
#     print(key)

#print(medical_data.head())

# def checkForMissingValues(series, columnName):
#     naCount = 0
#     try:
#         naInfo = series[columnName].isna()
#         naCount = naInfo.sum()
#         #print(f'{columnName} total missing count: {naCount}\n')

#         assert naCount == 0
#     except AssertionError:
#         print(f'Missing data detected for {columnName} column of Data Frame')
#     except:
#         print(f'Unknown column found {columnName}')

#     return naCount

# def checkForMissingValuesByColumns(series, columns = []):
#     naCounts = []
#     for column in columns:
#         naCount = checkForMissingValues(series, column)
#         naCounts.append(naCount)
        
#     missingValuesResult = {
#         'Column' : columns,
#         'NA_Count': naCounts
#     }

#     naDataFrame = pd.DataFrame(missingValuesResult)

#     return naDataFrame

# def visualizeMissingData(series, columnName):
#     #try:
#     data = series[columnName];
#     msno.matrix(data)
#     plt.show()
    #except:
        #print(f"Problem finding column '{columnName}' in ther series.")

#missing data
#print('\nChecking for missing data in each column. \n')

# medicalColumns = [
#     'Customer_id', 'Interaction', 'State', 'City', 
#     'County', 'Zip', 'Lat', 'Lng', 'Population', 
#     'Area', 'Timezone', 'Job', 'Children', 'Age',
#     'Education', 'Employment', 'Income', 'Marital',
#     'Gender', 'ReAdmis', 'VitD_levels', 'Doc_visits',
#     'Full_meals_eaten', 'VitD_supp', 'Soft_drink', 'Initial_admin',
#     'HighBlood', 'Stroke', 'Complication_risk', 'Overweight', 'Arthritis',
#     'Diabetes', 'Hyperlipidemia', 'BackPain', 'Anxiety', 'Allergic_rhinitis',
#     'Reflux_esophagitis', 'Asthma', 'Services', 'Initial_days', 'TotalCharge',
#     'Additional_charges', 'Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6',
#     'Item7', 'Item8'
#     ]

# naReport = checkForMissingValuesByColumns(medical_data, medicalColumns)
# missing_data = naReport[naReport['NA_Count'] > 0]
# missing_data_columns = missing_data['Column']

# msno.matrix(medical_data[missing_data_columns])
# plt.show()

#missing_data_columns = missing_data['Column']
#for column in missing_data_columns:
#    visualizeMissingData(medical_data, str(column))



