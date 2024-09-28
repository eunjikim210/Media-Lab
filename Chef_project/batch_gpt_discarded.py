import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import tiktoken

load_dotenv()

file_path = 'postdat_5rows_astest.csv'
data = pd.read_csv(file_path)

prompt_template = """
We have an Instagram post from a famous chef. Please analyze the content to determine whether it expresses political bias and classify it as either neutral, pro-Palestine, or pro-Israel. If the post does not mention politics or conflict, classify it as neutral. If it references the Israeli-Palestinian conflict, war, or violence, follow these guidelines:

[The rest of your prompt template]

Here is the text of the post: """

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def process_batch(batch):
    messages = [
        {
            "role": "system",
            "content": "You are a content classifier. You must return only one of the following categories: \"Neutral\", \"Pro-Palestine\", or \"Pro-Israel\""
        }
    ]
    
    for caption in batch:
        messages.append({"role": "user", "content": prompt_template + caption})
        messages.append({"role": "assistant", "content": "Analyzing..."})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=50 * len(batch)
        )
        
        results = [choice.message.content.strip() for choice in response.choices]
        return results
    except Exception as e:
        print(f"Error processing batch: {e}")
        return ["Error"] * len(batch)

# Fixed batch processing with handling for the last batch
batch_size = 5
data['political_bias'] = None

for i in range(0, len(data), batch_size):
    batch = data['caption'].iloc[i:i+batch_size].tolist()
    results = process_batch(batch)
    
    # Ensure we only assign as many results as we have in this batch
    end_index = min(i + batch_size, len(data))
    data.loc[data.index[i:end_index], 'political_bias'] = results[:end_index-i]
    
    # Add a small delay to respect rate limits
    time.sleep(1)

output_file = 'postdat_with_bias.csv'
data.to_csv(output_file, index=False)

print(f"结果已保存到 {output_file}")

# Print the token count of the prompt template
print(f"Token count of prompt template: {num_tokens_from_string(prompt_template)}")

# Print an estimate of tokens per batch
avg_caption_tokens = data['caption'].apply(num_tokens_from_string).mean()
system_message_tokens = num_tokens_from_string("You are a content classifier. You must return only one of the following categories: \"Neutral\", \"Pro-Palestine\", or \"Pro-Israel\"")
prompt_template_tokens = num_tokens_from_string(prompt_template)
estimated_tokens_per_batch = system_message_tokens + batch_size * (prompt_template_tokens + avg_caption_tokens + num_tokens_from_string("Analyzing..."))
print(f"Estimated average tokens per full batch: {estimated_tokens_per_batch:.0f}")