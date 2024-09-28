'''
Step 2: Merge the outcome of step 1 with corresponding fips, county name and cbsacode by zipcode

Outcome: merge_step2.xlsx
'''

import pandas as pd

excel1_df = pd.read_csv('zipcode_FIPS_cbsa_crosswalk_2015.csv')
excel2_df = pd.read_excel('merged_step1.xlsx')

# maximum length of zipcode
max_zipcode_length = 5

# standardize zipcode format to ensure zipcodes in both DataFrames are strings,
# and prepend zeros to match the length
excel1_df['zipcode'] = excel1_df['zipcode'].apply(lambda x: str(x).zfill(max_zipcode_length))
excel2_df['zipcode'] = excel2_df['zipcode'].apply(lambda x: str(x).zfill(max_zipcode_length))

# merge the two DataFrames based on 'zipcode' column
# how='left' ensures all rows from excel2_df are retained, even if no matching zipcode is found in excel1_df
merged_df = pd.merge(excel2_df, excel1_df[['zipcode', 'FIPS', 'CountyName', 'cbsacode']], on='zipcode', how='left')

merged_df.to_excel('merged_step2.xlsx', index=False)