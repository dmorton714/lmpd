import os
import pandas as pd
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import chi2_contingency
from api_key import api_key


def process_data():
    citation_file = 'data/citation.csv'
    employee_file = 'data/employee.csv'
    census_file = 'data/census.csv'

    citation_df = pd.DataFrame()
    employee_df = pd.DataFrame()
    census_df = pd.DataFrame()

    if os.path.exists(citation_file) and os.path.exists(employee_file) and os.path.exists(census_file):
        print("Files already exist. Loading from CSV.")
        citation_df = pd.read_csv(citation_file)
        employee_df = pd.read_csv(employee_file)
        census_df = pd.read_csv(census_file)
    else:
        print("Files do not exist. Fetching data from API.")
        builder = DataBuilder(api_key)
        builder.run_all()

        citation_df = pd.read_csv(citation_file)
        employee_df = pd.read_csv(employee_file)
        census_df = pd.read_csv(census_file)

    return citation_df, employee_df, census_df


class DataBuilder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.citation_url = 'https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/LMPD_STOP_DATA_2019_(2)/FeatureServer/0'
        self.employee_url = 'https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/LMPD_Demographics/FeatureServer/0'
        self.census_url = f"https://api.census.gov/data/2020/acs/acs5?get=NAME,B01001_001E,B01001_002E,B01001_026E,B02001_001E,B02001_002E,B02001_003E,B02001_004E,B02001_005E,B02001_006E,B02001_007E,B02001_008E&for=county:111&in=state:21&key={api_key}"

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
            return pd.DataFrame()  # Return an empty DataFrame on error

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
        expected_cols_citation = [
            'TYPE_OF_STOP', 'CITATION_CONTROL_NUMBER', 'ACTIVITY_RESULTS',
            'OFFICER_GENDER', 'OFFICER_RACE', 'OFFICER_AGE_RANGE',
            'ACTIVITY_DATE', 'ACTIVITY_TIME', 'ACTIVITY_LOCATION',
            'ACTIVITY_DIVISION', 'ACTIVITY_BEAT', 'DRIVER_GENDER',
            'DRIVER_RACE', 'DRIVER_AGE_RANGE', 'NUMBER_OF_PASSENGERS',
            'WAS_VEHCILE_SEARCHED', 'REASON_FOR_SEARCH', 'ObjectId'
        ]
        self.fetch_api_data(self.citation_url, expected_cols_citation, 'citation.csv')

        expected_cols_employee = [
            'AOC_CODE', 'RANK_TITLE', 'OFFICER_SEX', 'OFFICER_RACE',
            'OFFICER_AGE_RANGE', 'OFFICER_AGE', 'OFFICER_DIVISION',
            'OFFICER_ASSIGNMENT', 'OFFICER_YEARS_SWORN', 'ObjectId'
        ]
        self.fetch_api_data(self.employee_url, expected_cols_employee, 'employee.csv')

        self.fetch_census_data()


class DataCleaner:
    def __init__(self, citation_df, employee_df, census_df):
        self.citation_df = citation_df
        self.employee_df = employee_df
        self.census_df = census_df

    def citation_cleaning(self):
        citation_df = self.citation_df.copy()
        citation_cols_to_drop = [
            'CITATION_CONTROL_NUMBER', 'ACTIVITY_RESULTS',
            'ACTIVITY_DATE', 'ACTIVITY_TIME', 'ACTIVITY_LOCATION',
            'ACTIVITY_DIVISION', 'ACTIVITY_BEAT', 'NUMBER_OF_PASSENGERS',
            'WAS_VEHCILE_SEARCHED', 'REASON_FOR_SEARCH', 'ObjectId'
        ]
        citation_df = citation_df[~((citation_df['OFFICER_RACE'] == 'UNKNOWN') | # noqa
                                    (citation_df['DRIVER_RACE'] == 'UNKNOWN'))]
        citation_df = citation_df.drop(citation_cols_to_drop, axis=1, errors='ignore') # noqa
        return citation_df

    def employee_cleaning(self):
        employee_df = self.employee_df.copy()
        employee_cols_to_drop = [
            'AOC_CODE', 'RANK_TITLE', 'OFFICER_DIVISION',
            'OFFICER_ASSIGNMENT', 'OFFICER_YEARS_SWORN'
        ]
        employee_df = employee_df.drop(employee_cols_to_drop, axis=1, errors='ignore') # noqa

        race_mapping = {
            'W': 'WHITE',
            'B': 'BLACK',
            'H': 'HISPANIC',
            'A': 'ASIAN',
            'U': 'UNKNOWN'
        }
        employee_df['OFFICER_RACE'] = employee_df['OFFICER_RACE'].str.strip().map(race_mapping) # noqa
        employee_df = employee_df[~(employee_df['OFFICER_RACE'] == 'UNKNOWN')]
        return employee_df

    def census_to_percent(self):
        race_percentage_cols = [
            'Total_population', 'Total_male_population',
            'Total_female_population', 'Total_population_for_race',
            'White_alone', 'Black', 'Native_American',
            'Asian', 'Hawaiian_Pacific_Islander', 'Other_race_alone',
            'Two_or_more'
        ]

        louisville_census_percent = pd.DataFrame()

        for col in race_percentage_cols:
            louisville_census_percent[col + " (%)"] = self.census_df[col].apply(
                lambda x: (x / self.census_df["Total_population"]) * 100
            )
        return louisville_census_percent


class Visualization:
    def __init__(self, louisville_census_percent, employee_df, citation_df):
        self.louisville_census_percent = louisville_census_percent
        self.employee_df = employee_df
        self.citation_df = citation_df

    def gender_comparison_pie(self):
        # Extract percentages for males and females from census data
        male_percentage = self.louisville_census_percent['Total_male_population (%)'][0]
        female_percentage = self.louisville_census_percent['Total_female_population (%)'][0]

        # For employee_df
        employee_gender_counts = self.employee_df['OFFICER_SEX'].value_counts()
        employee_male = employee_gender_counts.get('M', 0)
        employee_female = employee_gender_counts.get('F', 0)

        # For citation_df
        citation_gender_counts = self.citation_df['DRIVER_GENDER'].value_counts()
        citation_male = citation_gender_counts.get('M', 0)
        citation_female = citation_gender_counts.get('F', 0)

        # Prepare the subplot
        fig = make_subplots(rows=1, cols=3, 
                            subplot_titles=('Louisville Population', 'LMPD', 'Drivers Race From Citations'),
                            specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]])

        # Data preparation
        datasets = ['Louisville Population', 'LMPD', 'Drivers Race From Citations']
        data_values = [
            [male_percentage, female_percentage],
            [employee_male, employee_female],
            [citation_male, citation_female]
        ]

        # Custom colors for male and female
        colors = ['#D1E8F2', '#FF69B4']  # Blue for Male, Pink for Female

        # Add each pie chart to a subplot using a loop
        for i, values in enumerate(data_values):
            fig.add_trace(go.Pie(labels=['Male', 'Female'], values=values, 
                                 marker=dict(colors=colors)),  # Set custom colors here
                          row=1, col=i + 1)  # `i + 1` since rows and columns are 1-indexed

        # Update layout
        fig.update_layout(title_text='Gender Comparison', template='plotly_white')

        # Show the figure
        fig.show()

    def chi_squared_test(self):
        # Step 1: Create a contingency table
        contingency_table = pd.crosstab(self.citation_df['OFFICER_RACE'], self.citation_df['DRIVER_RACE'])

        # Step 2: Perform chi-squared test
        chi2, p, dof, expected = chi2_contingency(contingency_table)

        # Step 3: Print the results
        print("Chi-squared Test:")
        print(f"Chi2 Statistic: {chi2:.4f}, P-value: {p:.4f}")

    def radar_plots(self):
        # Create a subplot grid (1 row, 4 columns)
        fig = make_subplots(rows=1, cols=4, specs=[[{'type': 'polar'}]*4],
                            subplot_titles=('Louisville Population', 'LMPD Force', 'Officer Citations', 'Drivers Race'))

        # Ensure OFFICER_RACE and DRIVER_RACE categories align with louisville_population_categories
        self.employee_df['OFFICER_RACE'] = self.employee_df['OFFICER_RACE'].str.strip().str.title()
        self.citation_df['OFFICER_RACE'] = self.citation_df['OFFICER_RACE'].str.strip().str.title()
        self.citation_df['DRIVER_RACE'] = self.citation_df['DRIVER_RACE'].str.strip().str.title()

        # Louisville Population Radar with combined 'Other' category
        other_categories = ['Hawaiian_Pacific_Islander (%)', 'Other_race_alone (%)', 'Two_or_more (%)']
        louisville_population_values = [
            self.louisville_census_percent['White_alone (%)'].values[0],
            self.louisville_census_percent['Black (%)'].values[0],
            self.louisville_census_percent['Asian (%)'].values[0],
            self.louisville_census_percent[other_categories].sum(axis=1).values[0]  # Sum of 'Other' categories
        ]
        louisville_population_categories = ['White', 'Black', 'Asian', 'Other']

        # Plot Louisville Population
        fig.add_trace(
            go.Scatterpolar(r=louisville_population_values, theta=louisville_population_categories, fill='toself', name='Louisville Population'),
            row=1, col=1
        )

        # LMPD Force Radar
        lmpd_force_counts = self.employee_df.groupby('OFFICER_RACE').size().reindex(louisville_population_categories, fill_value=0)
        lmpd_force_percentages = (lmpd_force_counts / lmpd_force_counts.sum()) * 100
        fig.add_trace(
            go.Scatterpolar(r=lmpd_force_percentages.values, theta=louisville_population_categories, fill='toself', name='LMPD Force'),
            row=1, col=2
        )

        # LMPD Officer Citations Radar
        officer_citation_counts = self.citation_df.groupby('OFFICER_RACE').size().reindex(louisville_population_categories, fill_value=0)
        officer_citation_percentages = (officer_citation_counts / officer_citation_counts.sum()) * 100
        fig.add_trace(
            go.Scatterpolar(r=officer_citation_percentages.values, theta=louisville_population_categories, fill='toself', name='Officer Citations'),
            row=1, col=3
        )

        # Drivers Race From Citations Radar
        driver_citation_counts = self.citation_df.groupby('DRIVER_RACE').size().reindex(louisville_population_categories, fill_value=0)
        driver_citation_percentages = (driver_citation_counts / driver_citation_counts.sum()) * 100
        fig.add_trace(
            go.Scatterpolar(r=driver_citation_percentages.values, theta=louisville_population_categories, fill='toself', name='Drivers Race'),
            row=1, col=4
        )

        # Update layout
        # Adjust polar subplot layouts for better visibility
        for i in range(1, 5):
            fig.update_layout(**{f'polar{i}': {'angularaxis': {'rotation': 45, 'direction': 'clockwise'}}})

        # Final layout adjustments
        fig.update_layout(height=600, width=1200, title_text="Radar Subplots for Louisville Data", showlegend=False)
        fig.show()


if __name__ == '__main__':
    # Process data and load DataFrames
    citation_df, employee_df, census_df = process_data()

    # Create an instance of DataCleaner
    cleaner = DataCleaner(citation_df, employee_df, census_df)

    # Clean the data using the defined cleaning methods
    cleaned_citation_df = cleaner.citation_cleaning()
    cleaned_employee_df = cleaner.employee_cleaning()
    louisville_census_percent = cleaner.census_to_percent()  # You need to call this to get the percent DataFrame

    # Create an instance of Visualization
    visualization = Visualization(louisville_census_percent, cleaned_employee_df, cleaned_citation_df)

    # Generate visualizations
    visualization.gender_comparison_pie()
    visualization.chi_squared_test()
    visualization.radar_plots()
