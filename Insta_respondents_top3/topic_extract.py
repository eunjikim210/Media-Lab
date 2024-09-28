import pandas as pd
import openai
import os

openai.api_key = 'KEY'

file_path = 'Top3Influencers_updated3.xlsx'
output_file_path = 'Top3Influencers_with_bio_column2.csv'

df = pd.read_excel(file_path, sheet_name='Sheet 1')

print(df.columns)

official_name_col = 'Unnamed: 5' 
description_col = 'Unnamed: 6'

def generate_bio(social_links):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=[
                {"role": "user", "content": f"Write a short biography for an influencer based on these social media links: {social_links}. Keep it under 90 words"}
            ],
            max_tokens=200
        )
        bio = response['choices'][0]['message']['content'].strip()
        return bio
    except Exception as e:
        print(f"Error generating bio for {social_links}: {e}")
        return None

# Save progress
def save_progress(df, path):
    df.to_csv(path, index=False, encoding='utf-8')

# Iterate through each row and generate bio
for index, row in df.iterrows():
    # If social media links exist and description is empty, generate bio
    if pd.notna(row[official_name_col]) and pd.isna(row[description_col]):
        social_links = row[official_name_col]
        bio = generate_bio(social_links)
        
        if bio:
            df.at[index, description_col] = bio  # Fill in the bio

        # Save progress
        save_progress(df, output_file_path)

    # Print progress message every 150 rows
    if (index + 1) % 150 == 0:
        print(f"Completed {index + 1} rows.")

# Final save
save_progress(df, output_file_path)
