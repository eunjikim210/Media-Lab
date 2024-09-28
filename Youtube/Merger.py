import pandas as pd
import os

os.chdir('Youtube')

files = ['youtubers_data_2020.csv', 'youtubers_data_2021.csv', 'youtubers_data_2022.csv', 'youtubers_data_2023.csv']

dfs = [pd.read_csv(f) for f in files]

merged_df = pd.concat(dfs, ignore_index=True)

merged_df.drop_duplicates(inplace=True)

merged_df.to_csv('merged_output.csv', index=False)