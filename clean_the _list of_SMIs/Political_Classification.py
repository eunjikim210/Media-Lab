import pandas as pd
import openai
import os

openai.api_key = '**********************'  

# 读取Excel文件
file_path = '/Users/zhangjunyi/Desktop/Top3Influencers_updated3.xlsx'
output_file_path = '/Users/zhangjunyi/Desktop/Top3Influencers_with_politics.csv'

df = pd.read_excel(file_path, sheet_name='工作表 1')

print(df.columns)

official_name_col = 'Unnamed: 5'  # 替换列
description_col = 'Unnamed: 6'    # 替换列

# 添加"Politics"和"Explanation"列
if 'Politics' not in df.columns:
    df['Politics'] = None
if 'Explanation' not in df.columns:
    df['Explanation'] = None

def classify_politics_and_explanation(social_links):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=[
                {"role": "user", "content": f"Based on the content from these social media links: {social_links}, "
                                            "determine if their content focuses on political topics like government, policies, or social justice. "
                                            "Respond with 'Yes', 'No', or 'Unclear'. Provide a brief explanation of no more than 30 words."}
            ],
            max_tokens=60
        )
        result = response['choices'][0]['message']['content'].strip()

        # 分析结果并提取政治分类和解释
        if "Yes" in result:
            politics = "Yes"
        elif "No" in result:
            politics = "No"
        else:
            politics = "Unclear"

        explanation = result  
        return politics, explanation
    except Exception as e:
        print(f"Error generating politics and explanation for {social_links}: {e}")
        return None, None

# 保存进度
def save_progress(df, path):
    df.to_csv(path, index=False, encoding='utf-8')

start_row = 5375

for index, row in df.iterrows():
    # 跳过之前已处理的行
    if index < start_row:
        continue

    # 如果社交媒体链接存在，则生成政治分类和解释
    if pd.notna(row[official_name_col]):
        social_links = row[official_name_col]
        
    
        politics, explanation = classify_politics_and_explanation(social_links)
        if politics and explanation:
            df.at[index, 'Politics'] = politics
            df.at[index, 'Explanation'] = explanation

        # 每处理150行，输出提示并保存进度
        if (index + 1) % 150 == 0:
            print(f"Completed {index + 1} rows.")
            save_progress(df, output_file_path)

# 最终保存一次
save_progress(df, output_file_path)