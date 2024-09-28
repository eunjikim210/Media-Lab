import json
import os
import random
import time
import copyheaders
import pandas
import requests
from lxml import etree

headers = copyheaders.headers_raw_to_dict(b"""
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
dpr:1
priority:u=0, i
sec-ch-prefers-color-scheme:light
sec-ch-ua:"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"
sec-ch-ua-full-version-list:"Chromium";v="128.0.6535.2", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6535.2"
sec-ch-ua-mobile:?0
sec-ch-ua-model:""
sec-ch-ua-platform:"Windows"
sec-ch-ua-platform-version:"15.0.0"
sec-fetch-dest:document
sec-fetch-mode:navigate
sec-fetch-site:same-origin
sec-fetch-user:?1
upgrade-insecure-requests:1
user-agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36
viewport-width:1009
""")

def send_get(url,headers,params):
    while 1:
        try:
            response = requests.get(
                url,headers=headers,params=params,timeout=(4,5)
            )
            time.sleep(.1)
            return response
        except Exception as e:
            print(f'some error:{e}')
            time.sleep(1)




def mian(iurl):

    for count in range(1,10):
        response = send_get(iurl, headers, {}).text

        document = etree.HTML(response)

        saveitem = {}
        saveitem["post_url"] = iurl
        saveitem["post_id"] = \
        "".join(document.xpath(".//meta[@property='al:ios:url']/@content")).split("id=")[-1].split("&")[0]

        print(saveitem)
        if saveitem["post_id"] == "":
            print(saveitem["post_id"])
        if saveitem["post_id"] != "":
            with open("./config/post.txt", 'a', encoding='utf-8') as f:
                f.write(json.dumps(saveitem))
                f.write('\n')

            return




if __name__ == "__main__":
    # os.environ["http_proxy"] = "http://127.0.0.1:7890"
    # os.environ["https_proxy"] = "http://127.0.0.1:7890"


    with open("./config/all_link.txt",'r',encoding='utf-8') as f:
        all_urls = [i.strip() for i in f.readlines() if i.strip() != '']


    for iurl in all_urls:

        mian(iurl)

    with open("./config/post.txt",'r',encoding='utf-8') as f:
        lines= [json.loads(i.strip()) for i in f.readlines()]
    df = pandas.DataFrame(lines)

    writer = pandas.ExcelWriter(r'post.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
    df.to_excel(writer)
    writer.save()
