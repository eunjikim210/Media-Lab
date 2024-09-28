import requests
import re

def extract_channel_url(youtube_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(youtube_url, headers=headers)
    # Extract channel URL
    match = re.search(r'<link rel="canonical" href="(https://www.youtube.com/channel/[^"]+)', response.text)
    return match.group(1) if match else None

def extract_channels_from_urls(url_list):
    return [extract_channel_url(url) for url in url_list]


url_list = [
    "https://www.youtube.com/c/AkeebaMaze/featured",
    "https://www.youtube.com/@ItsRadishTime",
    # more urls
]
print(extract_channels_from_urls(url_list))
