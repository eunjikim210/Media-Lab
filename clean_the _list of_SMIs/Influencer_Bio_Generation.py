import pandas as pd
import openai
import os


openai.api_key = '********************'  


file_path = '/Users/zhangjunyi/Desktop/Top3Influencers_updated3.xlsx'
output_file_path = '/Users/zhangjunyi/Desktop/Top3Influencers_with_bio.csv'

df = pd.read_excel(file_path, sheet_name='工作表 1')

print(df.columns)

official_name_col = 'Unnamed: 2'  # 替换列
description_col = 'Unnamed: 3'    # 替换列

def generate_bio(social_links):
    try:
        # 调用OpenAI API生成简短bio
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

# 保存进度
def save_progress(df, path):
    df.to_csv(path, index=False, encoding='utf-8')

# 迭代每一行并生成bio
for index, row in df.iterrows():
    # 如果社交媒体链接存在，且描述为空，则生成bio
    if pd.notna(row[official_name_col]) and pd.isna(row[description_col]):
        social_links = row[official_name_col]
        bio = generate_bio(social_links)
        
        if bio:
            df.at[index, description_col] = bio  # 填入bio

        # 保存进度
        save_progress(df, output_file_path)

    # 每处理150行，输出提示
    if (index + 1) % 150 == 0:
        print(f"Completed {index + 1} rows.")

# 最终保存一次
save_progress(df, output_file_path)