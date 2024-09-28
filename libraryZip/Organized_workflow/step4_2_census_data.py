'''
Step 4: This step merged the data from step 3 with more county level census data. 

New columns added: ageover65, collegeOrHigher, totalResidents

Years covered: 2012, 2016, 2020

Outcome: merge_step4.xlsx

Census data:  https://www.census.gov/data/developers/data-sets/acs-5year.html. (five year estimates data - The 2018-2022 ACS 5-Year)
'''

import pandas as pd

# census data files
files = [
    "2012_B01001", "2012_B06009",
    "2016_B01001", "2016_B06009",
    "2020_B01001", "2020_B06009"
]

output_file = 'merged_step4.xlsx'

for file in files:
    # extract year
    year, _ = file.split('_') 
    df_current = pd.read_excel(f"{file}.xlsx")
    
    with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:

        if year in writer.book.sheetnames:
            df_target = pd.read_excel(output_file, sheet_name=year)
            # left join by fips
            merged = pd.merge(df_target, df_current, on='fips', how='left')
            merged.to_excel(writer, sheet_name=year, index=False)