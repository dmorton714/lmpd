# -------------------------------------------------------- #
# Only run the API calls if you dont have the current data #
# -------------------------------------------------------- #

import requests
import pandas as pd
import os
from api_key import api_key

# -------------------------------------------------------- #
# citation Data 2012 - current                             #
# - This is no longer in project scope                     #
# - No longer provides officer datat                       #
# - Takes 16 mins to run returns 1.5 million rows          #
# -------------------------------------------------------- #

urls = [
    'https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/Louisville_Metro_KY_Uniform_Citation_Data_2023/FeatureServer/0', # noqa
    'https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/Louisville_Metro_KY_Uniform_Citation_Data_2022/FeatureServer/0', # noqa
    'https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/Louisville_Metro_KY_Uniform_Citation_Data_2021/FeatureServer/0', # noqa
    'https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/Louisville_Metro_KY_Uniform_Citation_Data_2020/FeatureServer/0', # noqa
    'https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/UniformCitationData_2016_2019/FeatureServer/0', # noqa
    'https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/UniformCitationData_2012_2015/FeatureServer/0' # noqa
]

batch_size = 1000
data_list = []

for url in urls:
    offset = 0

    while True:
        params = {
            'where': '1=1',
            'outFields': '*',
            'returnGeometry': 'false',
            'resultOffset': offset,
            'resultRecordCount': batch_size,
            'f': 'json'
        }

        response = requests.get(f"{url}/query", params=params)
        response.raise_for_status()

        query_result = response.json()
        features = query_result.get('features', [])

        for feature in features:
            data_list.append(feature['attributes'])

        if len(features) == 0:
            break

        offset += batch_size

df = pd.DataFrame(data_list)

output_directory = 'data'

os.makedirs(output_directory, exist_ok=True)

df.to_csv(os.path.join(output_directory, 'citation.csv'), index=False)

print(f"Data saved to {os.path.join(output_directory, 'citation.csv')}") # noqa


# -------------------------------------------------------- #
# LMPD Employee data                                       #
# -------------------------------------------------------- #

https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/Gun_Violence_Data/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson

# -------------------------------------------------------- #
# citation 2019 in old project scope                       #
# -------------------------------------------------------- #

urls = [
    'https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/LMPD_STOP_DATA_2019_(2)/FeatureServer/0'] 

batch_size = 1000
data_list = []

for url in urls:
    offset = 0

    while True:
        params = {
            'where': '1=1',
            'outFields': '*',
            'returnGeometry': 'false',
            'resultOffset': offset,
            'resultRecordCount': batch_size,
            'f': 'json'
        }

        response = requests.get(f"{url}/query", params=params)
        response.raise_for_status()

        query_result = response.json()
        features = query_result.get('features', [])

        for feature in features:
            data_list.append(feature['attributes'])

        if len(features) < batch_size:
            break

        offset += batch_size

df = pd.DataFrame(data_list)

output_directory = 'data'
os.makedirs(output_directory, exist_ok=True)

output_file = os.path.join(output_directory, 'citation_2019.csv')
df.to_csv(output_file, index=False)

print(f"Data saved to {output_file}")


# -------------------------------------------------------- #
# Census data pull                                         #
# -------------------------------------------------------- #


url = f"https://api.census.gov/data/2020/acs/acs5?get=NAME,B01001_001E,B01001_002E,B01001_026E,B02001_001E,B02001_002E,B02001_003E,B02001_004E,B02001_005E,B02001_006E,B02001_007E,B02001_008E&for=county:111&in=state:21&key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # Define the mapping dictionary
    column_mapping = {
        "NAME": "Name",
        "B01001_001E": "Total_population",
        "B01001_002E": "Total_male_population",
        "B01001_026E": "Total_female_population",
        "B02001_001E": "Total_population_for_race",
        "B02001_002E": "White_alone",
        "B02001_003E": "Black",
        "B02001_004E": "Native_American",
        "B02001_005E": "Asian",
        "B02001_006E": "Hawaiian_Pacific_Islander",
        "B02001_007E": "Other_race_alone",
        "B02001_008E": "Two_or_more",
        "state": "State code",
        "county": "County code"
    }
    
    # Rename the DataFrame columns
    df.rename(columns=column_mapping, inplace=True)
    
    # Print the DataFrame
    print(df)
else:
    print(f"Error: {response.status_code}")

df.to_csv('data/census.csv')