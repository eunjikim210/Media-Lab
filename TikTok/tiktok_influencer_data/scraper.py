# format: <meta data-rh="true" name="description" content="Dr. Jess | ecommjess (@ecommjess) on TikTok | 11.3M Likes. 737K Followers. 💸 Doctorate trained &amp; teaching you MONEY! 📫 business@ecommjess.com.Watch the latest video from Dr. Jess | ecommjess (@ecommjess).">

import requests
from bs4 import BeautifulSoup
import csv
import re

def extract_tiktok_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    meta_tag = soup.find('meta', {'name': 'description'})
    
    if not meta_tag:
        print("Meta tag with description not found!")
        return None
    
    content = meta_tag['content']
    username, likes, followers = extract_info_from_meta(content)
    
    return {
        'username': username,
        'likes': likes,
        'followers': followers
    }

def extract_info_from_meta(content):
    # Extract username
    username_pattern = r"@(\w+)"
    username_match = re.search(username_pattern, content)
    if not username_match:
        print("Username not found!")
        username = None
    else:
        username = username_match.group(1)

    # Extract likes
    likes_pattern = r"(\d+(\.\d+)?[MK]?) Likes"
    likes_match = re.search(likes_pattern, content)
    if not likes_match:
        print("Likes not found!")
        likes = None
    else:
        likes = convert_to_number(likes_match.group(1))

    # Extract followers
    followers_pattern = r"(\d+(\.\d+)?[MK]?) Followers"
    followers_match = re.search(followers_pattern, content)
    if not followers_match:
        print("Followers not found!")
        followers = None
    else:
        followers = convert_to_number(followers_match.group(1))

    return username, likes, followers

def convert_to_number(value):
    if 'M' in value:
        return int(float(value.replace('M', '')) * 1_000_000)
    elif 'K' in value:
        return int(float(value.replace('K', '')) * 1_000)
    else:
        return int(value)

# def save_to_csv(data, filename="output.csv"):
#     with open(filename, 'w', newline='') as csvfile:
#         fieldnames = ['username', 'likes', 'followers']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
#         writer.writeheader()
#         writer.writerow(data)

def save_to_csv(data_list, filename="tiktoker_data_2023.csv"):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['username', 'likes', 'followers']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in data_list:
            writer.writerow(data)

# urls
urls = [
    "https://www.tiktok.com/@ecommjess",
    "https://www.tiktok.com/@kahlilgreene",
    "https://www.tiktok.com/@kareemrahma?lang=en",
    "https://www.tiktok.com/@trashcaulin",
    "https://www.tiktok.com/@taylorcassidyj?",
    "https://www.tiktok.com/@eco_tok?lang=en",
    "https://www.tiktok.com/@imtiffanyyu?lang=en",
    "https://www.tiktok.com/@workanywhere.org",
    "https://www.tiktok.com/@ecofreako?_t=8aqWjyexFtu&_r=1",
    "https://www.tiktok.com/@newlifestyleabb",
    "https://www.tiktok.com/@amiemariah",
    "https://www.tiktok.com/@eco.amical?lang=en",
    "https://www.tiktok.com/@theconsciouslee",
    "https://www.tiktok.com/@theshadyecologist",
    "https://www.tiktok.com/@eco_og?lang=en",
    "https://www.tiktok.com/@jasonrodelo",
    "https://www.tiktok.com/@anania00",
    "https://tiktok.com/@cheesedaily?lang=en",
    "https://www.tiktok.com/@daisyfoko",
    "https://www.tiktok.com/@elinayael_",
    "https://www.tiktok.com/@typical_democrat",
    "https://www.tiktok.com/@famousblonde",
    "https://www.tiktok.com/@laysieeeb",
    "https://www.tiktok.com/@samvicchiollo",
    "https://www.tiktok.com/@underthedesknews"
]


all_data = []
for url in urls:
    info = extract_tiktok_info(url)
    if info:
        all_data.append(info)

if all_data:
    save_to_csv(all_data)
    print("Data saved to output.csv")
else:
    print("Failed to extract data from any URL.")
