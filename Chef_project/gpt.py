import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import sys

load_dotenv()

file_path = 'postdat_10percent.csv'
output_file = 'postdat_with_bias_10percent.csv'
data = pd.read_csv(file_path, encoding='utf-8')

data['caption'] = data['caption'].fillna('')
data['caption'] = data['caption'].astype(str)
data['political_bias'] = None

prompt_template = """
We have an Instagram post from a famous chef. Please analyze the content to determine whether it expresses political bias and classify it as either neutral, pro-Palestine, or pro-Israel. If the post does not mention politics or conflict, classify it as neutral. If it references the Israeli-Palestinian conflict, war, or violence, follow these guidelines:

- **Pro-Palestine**: The post expresses sympathy or support for Palestinians, highlights Palestinian suffering, or advocates for Palestinian rights. Indicators include phrases like *occupation, Israeli military actions, children of Gaza, Free Palestine*, or hashtags like:
    - #chefsforpalestine
    - #childrenofpalestinedeservelife
    - #speakupforgaza
    - #stopbombinggaza
    - #stopkillingjournalists
    - #stopkillingpalestinians
    - #stopthegenocideinpalestine
    - #freepalestine
    - #ceasefirenow
    - #gazaunderattack
    - #genocide
    - #apartheidisrael
    
    Mentions of Gaza that focus on Palestinian suffering, Israeli military actions in Gaza, or Palestinian sovereignty should be classified as pro-Palestine.
    
- **Pro-Israel**: The post expresses sympathy or support for Israel, mentions Israeli security, or advocates for Israel’s right to defend itself. Indicators include phrases like *terrorism, Hamas attacks, Israel's right to self-defense*, or any of the following hashtags:
    - #cookforisrael
    - #cookingforisrael
    - #israelunderattack
    - #standwithisrael
    - #bringthemhomenow
    - #amisraelchai
    - #antisemitism
    - #westandwithisrael
    
    Mentions of Gaza that emphasize Hamas, rocket attacks on Israel, or Israeli civilian suffering should be classified as pro-Israel.
    
- **Neutral**: The post does not take a clear stance on the conflict, or it balances both perspectives without favoring one side. Also classify it as neutral if the post is apolitical or focuses only on food or non-political topics.

Analyze both hashtags and the text for implicit references. If the political bias is unclear, mark it as neutral.

Here is the text of the post:
"""
total_rows = len(data)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def save_data(data, output_file):
    data.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")


MAX_RETRIES = 5
RETRY_DELAY = 5

try:
    for index, row in data.iterrows():
        caption = row['caption']

        if not caption.strip():
            print(f"Skipping row {index} due to empty caption")
            continue

        prompt = prompt_template + caption

        retries = 0

        while retries < MAX_RETRIES:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-2024-08-06",
                    messages=[
                        {"role": "system", "content": "You are a content classifier. You must return only one of the following categories: Neutral, Pro-Palestine, or Pro-Israel"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=50
                )
                result = response.choices[0].message.content.strip()

                data.at[index, 'political_bias'] = result
                break

            except Exception as e:
                retries += 1
                print(f"Error processing row {index} on attempt {retries}: {e}")

                if retries == MAX_RETRIES:
                    print(f"Failed after {MAX_RETRIES} retries, exiting program.")
                    data.at[index, 'political_bias'] = "Error"
                    save_data(data, output_file)
                    sys.exit(1) 

                else:
                    # Retry after 5 seconds
                    time.sleep(RETRY_DELAY)

        if (index + 1) % 5 == 0:
            print(f"Processed {index + 1}/{total_rows} rows")

    save_data(data, output_file)

except Exception as e:
    print(f"Fatal error occurred: {e}")
    save_data(data, output_file)