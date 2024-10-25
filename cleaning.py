import pandas as pd


class DataCleaner:
    def __init__(self, citation_file, employee_file, census_file):
        self.citation_df = pd.read_csv(citation_file)
        self.employee_df = pd.read_csv(employee_file)
        self.census_df = pd.read_csv(census_file)

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

        louisville_census = pd.DataFrame()

        for col in race_percentage_cols:
            louisville_census[col + " (%)"] = self.census_df[col].apply(
                lambda x: (x / self.census_df["Total_population"]) * 100
            )
        return louisville_census
