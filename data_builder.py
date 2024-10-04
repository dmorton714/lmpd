import requests
import pandas as pd
import os
from api_key import api_key

class DataBuilder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.citation_url = 'https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/LMPD_STOP_DATA_2019_(2)/FeatureServer/0'
        self.employee_url = 'https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/LMPD_Demographics/FeatureServer/0'
        self.census_url = f"https://api.census.gov/data/2020/acs/acs5?get=NAME,B01001_001E,B01001_002E,B01001_026E,B02001_001E,B02001_002E,B02001_003E,B02001_004E,B02001_005E,B02001_006E,B02001_007E,B02001_008E&for=county:111&in=state:21&key={api_key}"
        
        # Directory to save data
        self.output_directory = 'data'
        os.makedirs(self.output_directory, exist_ok=True)
        
    def fetch_api_data(self, url, expected_cols, filename):
        params = {
            'where': '1=1',
            'outFields': '*',
            'returnGeometry': 'false',
            'resultOffset': 0,
            'resultRecordCount': 10,
            'f': 'json'
        }

        try:
            response = requests.get(f"{url}/query", params=params)
            response.raise_for_status()
            data_list = [feature['attributes'] for feature in response.json().get('features', [])]
            df = pd.DataFrame(data_list)

            if set(expected_cols).issubset(df.columns):
                print(f"Data structure matches for {filename}")
                df_full = self.fetch_full_data(url)
                df_full.to_csv(os.path.join(self.output_directory, filename), index=False)
                print(f"Data saved to {filename}")
            else:
                print(f"Data structure has changed for {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
    
    def fetch_full_data(self, url, batch_size=1000):
        data_list = []
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

        return pd.DataFrame(data_list)

    def fetch_census_data(self):
        try:
            response = requests.get(self.census_url)

            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data[1:], columns=data[0])

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
                df.rename(columns=column_mapping, inplace=True)
                df.to_csv(os.path.join(self.output_directory, 'census.csv'), index=False)
                print("Census data saved to census.csv")
            else:
                print(f"Error fetching census data: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching census data: {e}")

    def run_all(self):
        # Citation data fetch
        expected_cols_citation = [
            'TYPE_OF_STOP', 'CITATION_CONTROL_NUMBER', 'ACTIVITY_RESULTS',
            'OFFICER_GENDER', 'OFFICER_RACE', 'OFFICER_AGE_RANGE', 'ACTIVITY_DATE',
            'ACTIVITY_TIME', 'ACTIVITY_LOCATION', 'ACTIVITY_DIVISION',
            'ACTIVITY_BEAT', 'DRIVER_GENDER', 'DRIVER_RACE', 'DRIVER_AGE_RANGE',
            'NUMBER_OF_PASSENGERS', 'WAS_VEHCILE_SEARCHED', 'REASON_FOR_SEARCH',
            'ObjectId'
        ]
        self.fetch_api_data(self.citation_url, expected_cols_citation, 'citation.csv')

        # Employee data fetch
        expected_cols_employee = [
            'AOC_CODE', 'RANK_TITLE', 'OFFICER_SEX', 'OFFICER_RACE',
            'OFFICER_AGE_RANGE', 'OFFICER_AGE', 'OFFICER_DIVISION',
            'OFFICER_ASSIGNMENT', 'OFFICER_YEARS_SWORN', 'ObjectId'
        ]
        self.fetch_api_data(self.employee_url, expected_cols_employee, 'employee.csv')

        # Census data fetch
        self.fetch_census_data()


# Example usage
data_builder = DataBuilder(api_key)
data_builder.run_all()
