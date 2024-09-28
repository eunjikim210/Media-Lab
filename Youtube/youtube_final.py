import requests
import csv
import re

# API key
API_KEY = 'yourAPIkey'

# 2020
urls = [
    "https://www.youtube.com/channel/UCUtloyZ_Iu4BJekIqPLc_fQ",
    "https://www.youtube.com/channel/UCXOnt8cnv1Ot3nLbXgNCFqw",
    "https://www.youtube.com/channel/UC81rC6q9s1km-wh68i335pg/about",
    "https://www.youtube.com/channel/UCamLstJyCa-t5gfZegxsFMw",
    "https://www.youtube.com/channel/UCzgyo1MvMJwmsr3T0mblNZg",
    "https://www.youtube.com/user/Hallease",
    "https://www.youtube.com/c/HowtoADHD/videos",
    "https://www.youtube.com/user/jouelzy/about",

    # "https://www.youtube.com/watch?v=tYCscdR-CTY",
    'https://www.youtube.com/channel/UCLA7mHQtzSiU2MUEmdHyXsg',

    "https://www.youtube.com/user/KatiMorton",
    "https://www.youtube.com/user/ItsKingsleyBitch/about",
    "https://www.youtube.com/user/Destiny",
    "https://www.youtube.com/c/TraeCrowderLiberalRedneck/videos",
    "https://www.youtube.com/channel/UCwwlXnq03-NDZH49HxKNcvA",
    "https://www.youtube.com/channel/UCFnMWABu-7dXfCXj8HukNpA",
    "https://www.youtube.com/channel/UCvtO-Hj_GczqSNY6X8yVn8g",

    # "https://www.youtube.com/doddleoddle",
    'https://www.youtube.com/channel/UCKVfKr96Ifr3Dnhb6mhDAdw',

    "https://www.youtube.com/channel/UCCPHeV_9kyViBufLwBl9b5g",

    "https://www.youtube.com/channel/UCtQ7zqr9cWlvnPLq2GSS-1AA",

    "https://www.youtube.com/channel/UCErKUCncCyBgEdxWAtrj5hg",

    # "https://www.youtube.com/jameshenry",
    'https://www.youtube.com/channel/UCVCVOSRs51V0nkCe4rVcVnw',

    "https://www.youtube.com/user/lifewithJc",
    "https://www.youtube.com/user/FunForLouis",
    "https://www.youtube.com/channel/UCP1N9j-Jl890PHJjD3VnhLg/videos",
    "https://www.youtube.com/user/RayaWasHere",

    # "https://www.youtube.com/watch?v=BgsevvaEQww&feature=emb_title",
    'https://www.youtube.com/channel/UC_e3Ux8JX8HvD5dwHDRZEWA',

    "https://www.youtube.com/user/Whatstrending",
    "https://www.youtube.com/channel/UCky4B_P_AJ9QST2RDdXODWw",
    "https://www.youtube.com/user/PracProcrastination",
    "https://www.youtube.com/c/MikeCorey",

    # "https://www.youtube.com/watch?v=SUGO7KMkHRs",
    'https://www.youtube.com/channel/UCw8_yg1camlWnYfX_0tfECw',

    "https://www.youtube.com/channel/UCRCuTkGoYEqfKllcIEahxhw",
    "https://www.youtube.com/channel/UCfpvDwxlR_VeApVep4hhwUA"
]


def extract_channel_url(youtube_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(youtube_url, headers=headers)
    match = re.search(r'<link rel="canonical" href="(https://www.youtube.com/channel/[^"]+)', response.text)
    return match.group(1) if match else None


urls = [extract_channel_url(url) if "/c/" in url or "/@" in url else url for url in urls]

def get_channel_data(query_type, query_value):
    if query_type == "forUsername":
        endpoint = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&forUsername={query_value}&key={API_KEY}'
    else:  # "id"
        endpoint = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={query_value}&key={API_KEY}'
    
    response = requests.get(endpoint)
    return response.json()

with open('youtubers_data_2020.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Subscriber Count', 'Video Count', 'View Count'])

    failed_urls = urls.copy()

    for url in urls:
        data = {}
        if '/c/' in url:
            username = url.split('/c/')[1].split('/')[0]
            data = get_channel_data("forUsername", username)
            if not data.get('items'):
                data = get_channel_data("id", username)
        elif '/channel/' in url:
            channel_id = url.split('/channel/')[1].split('/')[0]
            data = get_channel_data("id", channel_id)
        elif '/user/' in url:
            username = url.split('/user/')[1].split('/')[0]
            data = get_channel_data("forUsername", username)

        if 'items' in data and len(data['items']) > 0:
            item = data['items'][0]
            name = item['snippet']['title']
            subscriber_count = item['statistics']['subscriberCount']
            video_count = item['statistics']['videoCount']
            view_count = item['statistics']['viewCount']

            writer.writerow([name, subscriber_count, video_count, view_count])
            failed_urls.remove(url)


if failed_urls:
    print("The following URLs failed to write to the file:")
    for url in failed_urls:
        print(url)