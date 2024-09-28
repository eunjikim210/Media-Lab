'''
Before you start, open a new terminal and do the following: 
1. Enter: 
    pip install tiktokapipy pandas openpyxl
    python -m playwright install
2. Get the full url from the vedio you are about to extract:
    e.g. Get url such as: https://www.tiktok.com/@ecofreako/video/7280262760120847662?_r=1&_t=8aqWjyexFtu

3. Start using the following code to extract data. 

Attention: This scraper is not used for comment extraction. 
'''

from tiktokapipy.api import TikTokAPI
import pandas as pd

def get_video(video_url):
    with TikTokAPI() as api:
        video = api.video(video_url)
        
        data = {
            "id": [video.id],
            "unique_id": [video.author.unique_id],
            "comment_count": [video.stats.comment_count],
            "play_count": [video.stats.play_count],
            "collect_count": [video.stats.collect_count],
            "digg_count": [video.stats.digg_count],
            "share_count": [video.stats.share_count],
            "desc": [video.desc]
        }
        
        df = pd.DataFrame(data)
        df.to_csv("output.csv", index=False)

get_video("https://www.tiktok.com/@ecofreako/video/7280262760120847662?_r=1&_t=8aqWjyexFtu")