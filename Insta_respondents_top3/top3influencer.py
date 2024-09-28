import pandas as pd
import requests
import time

# Google Custom Search API call function with retry for connection errors
def google_search(query, api_key, cse_id, retries=5):
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}"
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                results = response.json()
                return results.get('items', [])
            elif response.status_code == 429:
                print("Error: 429 - Too Many Requests. Waiting for 5 seconds...")
                time.sleep(5)
            else:
                print(f"Error: {response.status_code}")
                return []
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}. Retrying in 10 seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(10) 
    print(f"Failed to retrieve data after {retries} attempts.")
    return []

# Function to extract social media links
def extract_social_links(search_results, max_links=3): 
    social_links = []
    for result in search_results:
        link = result.get('link', '')
        if 'youtube.com' in link or 'instagram.com' in link or 'tiktok.com' in link:
            social_links.append(link)
        if len(social_links) >= max_links:
            break
    return social_links

# Load the data
df = pd.read_excel('Top3Influencers.xlsx')

# API key and CSE ID (replace with your own)
API_KEY = 'KEY'
CSE_ID = 'ID'

# Function to update the officialname columns based on TEXT columns
def update_officialname(row, text_col, officialname_col, index):
    print(f"Processing row {index + 1}/{len(df)}...")
    if pd.notna(row[text_col]) and pd.isna(row[officialname_col]):
        query = f"{row[text_col]} site:youtube.com OR site:instagram.com OR site:tiktok.com"
        search_results = google_search(query, API_KEY, CSE_ID)
        if search_results:
            social_links = extract_social_links(search_results)
            if social_links:
                return "|".join(social_links)  # Convert the list to a string separated by |
        return "No social media links found"
    return row[officialname_col]

# Function to save progress
def save_progress(df, file_name):
    df.to_csv(file_name, index=False)
    print(f"Progress saved to '{file_name}'")

# Apply the function to update the three officialname columns
batch_size = 500
total_rows = len(df)
file_name = 'Top3Influencers_updated.csv'

try:
    for i in range(0, total_rows, batch_size):
        for j in range(i, min(i + batch_size, total_rows)):  # Iterate through the rows in the batch
            df.loc[j, 'top_smis_1_officialname '] = update_officialname(df.loc[j], 'top_smis_1_TEXT', 'top_smis_1_officialname ', j)
            time.sleep(0.7)
            df.loc[j, 'top_smis_2_officialname '] = update_officialname(df.loc[j], 'top_smis_2_TEXT', 'top_smis_2_officialname ', j)
            time.sleep(0.7)
            df.loc[j, 'top_smis_3_officialname '] = update_officialname(df.loc[j], 'top_smis_3_TEXT', 'top_smis_3_officialname ', j)
            time.sleep(0.7)

        # Save every 500 rows, or whatever batch size you define
        save_progress(df, file_name)

except Exception as e:
    print(f"An error occurred: {e}. Saving current progress...")
    save_progress(df, file_name)

print("All data processed and saved.")
