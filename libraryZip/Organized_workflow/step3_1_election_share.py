'''
Step 3_1: Election data collecting and cleaning

This step collected and cleaned the presidential election data

Columns: 

Outcome: county_vote_share_2000-2020.xlsx

Resources: 
Election data: https://www.nature.com/articles/s41597-023-02792-x

'''

import pandas as pd
file_path = 'countypres_2000-2020.csv'
data = pd.read_csv(file_path)
years_of_interest = [2000, 2004, 2008, 2012, 2016, 2020]
filtered_data = data[data['year'].isin(years_of_interest)]

filtered_data['vote_share'] = filtered_data['candidatevotes'] / filtered_data['totalvotes']

pivot_data = filtered_data.pivot_table(index=['year', 'state', 'state_po', 'county_name', 'county_fips'],
                                       columns='party', values='vote_share', aggfunc='sum').reset_index()

pivot_data = pivot_data.fillna(0)

pivot_data.columns = [col.upper() + ' vote share' if col not in ['year', 'state', 'state_po', 'county_name', 'county_fips'] else col for col in pivot_data.columns]

output_path = 'county_vote_share_2000-2020.xlsx'
excel_writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

for year in years_of_interest:
    year_data = pivot_data[pivot_data['year'] == year]
    year_data.to_excel(excel_writer, sheet_name=str(year), index=False)

excel_writer.save()