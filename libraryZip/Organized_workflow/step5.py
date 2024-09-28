'''
Step 5: Merge the outcome of step 4 with the outcome of step 2
'''

import pandas as pd

file1_df = pd.read_excel('merged_step2.xlsx')

writer = pd.ExcelWriter('Merged_File.xlsx', engine='openpyxl')

# list of subsheet names in File2
subsheet_names = ['2000', '2004', '2008', '2012', '2016', '2020']

# loop through each subsheet in File2 and merge with File1
for name in subsheet_names:
    file2_df = pd.read_excel('merged_step4.xlsx', sheet_name=name)
    # merge based on the 'fips' column
    merged_df = pd.merge(file1_df, file2_df, on='fips', how='left')
    merged_df.to_excel(writer, sheet_name=name, index=False)

writer.close()