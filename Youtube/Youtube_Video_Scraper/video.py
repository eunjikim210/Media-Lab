import re
import csv
from googleapiclient.discovery import build

API_KEY = 'key'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def extract_video_id(link):
    short_pattern = r"shorts/([\w\-_]+)"
    long_pattern = r"v=([\w\-_]+)"
    if "shorts" in link:
        match = re.search(short_pattern, link)
    else:
        match = re.search(long_pattern, link)
    return match.group(1) if match else None

def fetch_video_details(video_id):
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()
    if not response['items']:
        print(f"No data returned for video ID: {video_id}")
        return None
    item = response['items'][0]
    snippet = item['snippet']
    stats = item['statistics']
    return {
        "title": snippet['title'],
        "published_at": snippet['publishedAt'],
        "channel_title": snippet['channelTitle'],
        "like_count": stats.get('likeCount', 0),
        # Add more fields if necessary
    }

def fetch_comments(video_id):
    comments = []
    page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=page_token
        )
        response = request.execute()
        
        for item in response['items']:
            snippet = item['snippet']['topLevelComment']['snippet']
            comments.append({
                "comment": snippet['textDisplay'],
                "commenter_id": snippet['authorChannelId']['value'],
                "comment_published_at": snippet['publishedAt']
            })

        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return comments

def write_to_csv(data, filename="testoutput.csv"):
    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["title", "published_at", "channel_title", "like_count", "comment", "commenter_id", "comment_published_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    links = ["https://youtube.com/shorts/z-O3oyae_40?feature=share", "https://www.youtube.com/watch?app=desktop&v=B_-kjctRjUs&feature=youtu.be"]
    all_data = []

    for link in links:
        video_id = extract_video_id(link)
        if not video_id:
            print(f"Unable to extract video ID from link: {link}")
            continue
        details = fetch_video_details(video_id)
        comments = fetch_comments(video_id)
        
        first_comment = True
        for comment in comments:
            if first_comment:
                all_data.append({**details, **comment})
                first_comment = False
            else:
                # Only add comment details, and omit video details
                all_data.append({
                    "title": "",
                    "published_at": "",
                    "channel_title": "",
                    "like_count": "",
                    **comment
                })

    write_to_csv(all_data)