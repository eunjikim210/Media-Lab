'''
Step 1: Merge the library crosswalk result with the works_by_library_v12024.csv by libraryid

Outcome: merge_step1.xlsx
'''

import pandas as pd

zip_final_df = pd.read_excel('zip_final.xlsx')
works_by_library_df = pd.read_csv('works_by_library_v12024.csv')

# drop na
works_by_library_df_cleaned = works_by_library_df.dropna(subset=['cl_libraryid'])
zip_final_df_cleaned = zip_final_df[zip_final_df['zip'] != "missing"]

# left join
merged_df = pd.merge(zip_final_df_cleaned, works_by_library_df_cleaned, left_on="libraryid", right_on="cl_libraryid", how="left")

merged_df.to_excel('merge_step1.xlsx', index=False)