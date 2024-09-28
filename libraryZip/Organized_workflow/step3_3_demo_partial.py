'''
Step 3 - Demographical Data (partial)

This step merged the outcome of election vote share and the county level demographical data extracted 
from American Local Government Elections Database.

New columns added: percent_women, percent_white, percent_black, percent_hispanic, percent_asian_american

Outcome: merged_step3.xlsx

Data source: https://osf.io/mv5e6/
'''

import pandas as pd

file1_path = 'county_vote_share_2000-2020.xlsx'
xls = pd.ExcelFile(file1_path)

file2_path = 'cleaned_counties_historical_demographics.xlsx'
df2 = pd.read_excel(file2_path)

new_file_path = 'merged_step3.xlsx'

with pd.ExcelWriter(new_file_path, engine='openpyxl') as writer:
    # iterate through all the sheets in the first Excel file
    for sheet_name in xls.sheet_names:
        # load the current sheet
        df1 = pd.read_excel(xls, sheet_name=sheet_name)
        
        # filter rows in the second table where the year matches the current sheet name
        matching_rows = df2[df2['year'] == int(sheet_name)]
        
        for index, row in matching_rows.iterrows():
            # find rows in the current sheet where fips match
            match_index = df1[df1['fips'] == row['fips']].index
            # if a matching row is found, add the row from the second table to the corresponding row in the first table
            if not match_index.empty:
                for col in df2.columns:
                    df1.at[match_index[0], col] = row[col]
        
        df1.to_excel(writer, sheet_name=sheet_name, index=False)
