import os
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of URLs
urls = [
    "https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/LMPD_STOPS_DATA_(2)/FeatureServer/0/query",
    "https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/LMPD_STOP_DATA_202/FeatureServer/0/query",
    "https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/LMPD_STOP_DATA_2023/FeatureServer/0/query"
]

batch_size = 1000
data_list = []


def fetch_data(url):
    offset = 0
    local_data_list = []

    while True:
        params = {
            'where': '1=1',
            'outFields': '*',
            'returnGeometry': 'false',
            'resultOffset': offset,
            'resultRecordCount': batch_size,
            'f': 'json'
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        query_result = response.json()
        features = query_result.get('features', [])

        for feature in features:
            local_data_list.append(feature['attributes'])

        if len(features) == 0:
            break

        offset += batch_size

    return local_data_list


# Use ThreadPoolExecutor to fetch data concurrently
with ThreadPoolExecutor(max_workers=len(urls)) as executor:
    future_to_url = {executor.submit(fetch_data, url): url for url in urls}

    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            data_list.extend(data)
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data_list)

# Create output directory if it doesn't exist
output_directory = 'data'
os.makedirs(output_directory, exist_ok=True)

# Save DataFrame to CSV file
output_path = os.path.join(output_directory, 'citation_09_23.csv')
df.to_csv(output_path, index=False)

print(f"Data saved to {output_path}")
