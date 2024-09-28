'''
Step 3 - Demographical Data (partial)

This step merged the outcome of election vote share and the county level demographical data extracted 
from American Local Government Elections Database.

New columns added: percent_women, percent_white, percent_black, percent_hispanic, percent_asian_american

Outcome: cleaned_counties_historical_demographics.xlsx

Data source: https://osf.io/mv5e6/
'''

import pandas as pd

# percent_women, percent_white, percent_black, percent_hispanic, percent_asian_american data by years
file_path = 'counties_historical_demographics.xlsx'
df = pd.read_excel(file_path)

years_to_keep = [2000, 2004, 2008, 2012, 2016, 2020]

filtered_df = df[df['year'].isin(years_to_keep)]

output_file_path = 'cleaned_counties_historical_demographics.xlsx'
filtered_df.to_excel(output_file_path, index=False)

print("County level demographic data has been extracted by election years")

