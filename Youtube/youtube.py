import requests
import csv

# api key
API_KEY = ''

urls = [
    # 'https://www.youtube.com/@AkeebaMaze/featured',
    'https://www.youtube.com/channel/UC1SnW7mEHTTbEVcbLI2hUhg',

    'https://www.youtube.com/channel/UC81rC6q9s1km-wh68i335pg',
    'https://www.youtube.com/user/Hallease',
    'https://www.youtube.com/user/yovistobueno',
    'https://www.youtube.com/channel/UCEzpZObez51nBnI6E1TQRwg',

    # 'https://www.youtube.com/c/DustinBurtonRaisingBuffaloes/videos',
    'https://www.youtube.com/channel/UCYwWKeuYRQDluXYdS4FkRMA',


    'https://www.youtube.com/channel/UCHcK_QIEM0KECFzYUym497A',
    'https://www.youtube.com/user/AmbersCloset33',
    'https://www.youtube.com/user/FunForLouis/videos',
    'https://www.youtube.com/channel/UCbKSQfo4v5L8duzw3bXBKqw',
    'https://www.youtube.com/user/Whatstrending',
    'https://www.youtube.com/channel/UC_a_lMvQaHyltSWfkB3ymmQ',
    'https://www.youtube.com/channel/UCPf55sis3jNICWi3K1NsJMQ',

    # 'https://www.youtube.com/c/TazzyPhe',
    'https://www.youtube.com/channel/UCnltgt0ihG-sHJ501xX39ug',

    # 'https://www.youtube.com/@ItsRadishTime',
    'https://www.youtube.com/channel/UCL3IRp9f41q4hu15T3oPFqg',

    # 'https://www.youtube.com/@JamiePerkins',
    'https://www.youtube.com/channel/UChbmgfBOmMLKHiTOIjDyEkg',

    # 'https://www.youtube.com/@LilyPetals',
    'https://www.youtube.com/channel/UCDmpY3ukz9BI4zS56fG-Y7Q',

    # 'https://www.youtube.com/c/ElenaTaber',
    'https://www.youtube.com/channel/UCDBroOWVP4aN8SYM0br6sJQ',

    # 'https://www.youtube.com/@Fabsocialism/videos',
    'https://www.youtube.com/channel/UCLloRmz8n7qDOOG1gocQsfQ',

    # 'https://www.youtube.com/c/Wheelsnoheels/videos',
    'https://www.youtube.com/channel/UCNP1tYcve1MtivJtDjHsO-g',

    'https://www.youtube.com/channel/UCgaKAH-PAvm2wlBk3XbsRLQ',

    # 'https://www.youtube.com/c/jnaydaily',
    'https://www.youtube.com/channel/UCBBAQpm8VQqBIAF3e8F1lWw',

    'https://www.youtube.com/channel/UCy6Qlkv2hif7KPtmMmNUGUw',
    'https://www.youtube.com/channel/UCnBAQgJqnO5tVDbPCskcP8A',

    # 'https://www.youtube.com/c/shallonlester'
    'https://www.youtube.com/channel/UCygmWL3k4EpxBmWGGBs5ldw',

    # 'https://www.youtube.com/@BeliefItOrNot',
    'https://www.youtube.com/channel/UCC_w8GsmIp-6dHhdVHqcVgg',

    # 'https://www.youtube.com/c/briantylercohen',
    'https://www.youtube.com/channel/UCQANb2YPwAtK-IQJrLaaUFw',

    # 'https://www.youtube.com/c/DomoWilsonIsBae',
    'https://www.youtube.com/channel/UCwwlXnq03-NDZH49HxKNcvA',

    'https://www.youtube.com/channel/UCSHff31HSK0VVPOzGTz8dPg',
    'https://www.youtube.com/user/thebeautyfashionbabe',

    # 'https://www.youtube.com/c/NoisyImagesOfficial/videos',
    'https://www.youtube.com/channel/UCVHeqpJWysWdIevel7_znyQ',

    # 'https://www.youtube.com/jaclyn',
    'https://www.youtube.com/channel/UCravYcv6C0CopL2ukVzhzNw',

    # 'https://www.youtube.com/c/JennaLarson/videos',
    'https://www.youtube.com/channel/UCUAtOr0iCXAMIO54d94NYtQ',

    # 'https://www.youtube.com/watch?v=U4MXL6whmNA',
    'https://www.youtube.com/channel/UCV17e-wyxjzZEzRxH8j1rdQ',

    # 'https://www.youtube.com/c/lauralaura88leelee/videos',
    'https://www.youtube.com/channel/UCKMugoa0uHpjUuq14yOpagw',

    'https://www.youtube.com/channel/UCQ0gG42bXPBi7yHx9UJyexQ',
    'https://www.youtube.com/channel/UC5ruRwcN1khpjFxr58oIxqA',
    'https://www.youtube.com/channel/UCwujpQY0MBpwpNMzPMO3Z5w',
    'https://www.youtube.com/channel/UCE91wUZaPq7M3uKgJlp9oag',
    'https://www.youtube.com/channel/UCgF7YFF8z-J4nygkVhavWrQ',
    'https://www.youtube.com/user/Smilebuddiesxoxo',
    'https://www.youtube.com/channel/UCphTF9wHwhCt-BzIq-s4V-g'
]

def get_channel_data(query_type, query_value):
    if query_type == "forUsername":
        endpoint = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&forUsername={query_value}&key={API_KEY}'
    else:  # "id"
        endpoint = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={query_value}&key={API_KEY}'
    
    response = requests.get(endpoint)
    return response.json()

with open('youtubers_data.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Subscriber Count', 'Video Count', 'View Count'])

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
