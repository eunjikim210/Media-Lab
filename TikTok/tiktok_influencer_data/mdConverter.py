import pandas as pd
import os
os.chdir('tiktok_influencer_data')


def csv_to_md(input_csv, output_md):
    df = pd.read_csv(input_csv)
    
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = df[col].apply(lambda x: '{:,.0f}'.format(x))

    # Convert DataFrame to markdown
    markdown_string = df.to_markdown()

    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(markdown_string)

input_csv = 'merged_tiktok.csv'
output_md = 'Tiktok_Influencer.md'
csv_to_md(input_csv, output_md)