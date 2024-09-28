import pandas as pd
import os

os.chdir('tiktok_influencer_data')

files = ['tiktoker_data_2020_22.csv', 'tiktoker_data_2023.csv']

dfs = [pd.read_csv(f) for f in files]

merged_df = pd.concat(dfs, ignore_index=True)

merged_df.drop_duplicates(inplace=True)

merged_df.to_csv('merged_tiktok.csv', index=False)