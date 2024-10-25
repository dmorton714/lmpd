import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import chi2_contingency


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

# Example usage
# visualization = Visualization(louisville_census_percent, employee_df, citation_df)
# visualization.gender_comparison_pie()
# visualization.chi_squared_test()
# visualization.radar_plots()
