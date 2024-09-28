import json
import os
import time
import pandas
import redis
import requests


class Com(object):
    start_count = 0

    def     __init__(self):
        pass



    def _download(self,item):

        media_id = item.get("post_id")
        comment_id = item.get("comment_id")
        api = f'https://www.instagram.com/api/v1/media/{media_id}/comments/{comment_id}/child_comments/'

        params = {
            "max_id":'',
        }


        media_count_page = item.get("comment_reply_count") // 10 + 2

        for page in range(media_count_page):

            while 1:
                try:

                    all_cookirs = [i.decode() for i in redis_map.lrange('ins', 0, -1)]

                    if len(all_cookirs) == 0:
                        print(f'>>> No available cookie ==》 Please add')
                        time.sleep(10)
                        continue
                    Cookirstr = all_cookirs[-1]
                    Csrftoken = Cookirstr.split("csrftoken=")[-1].split(";")[0]

                    self.headers = {
                        "Accept": "*/*",
                        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                        "Cookie": Cookirstr,
                        "Priority": "u=1, i",
                        "Referer": item.get("post_url"),
                        "Sec-Ch-Prefers-Color-Scheme": "light",
                        "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                        "Sec-Ch-Ua-Full-Version-List": "\"Chromium\";v=\"124.0.6367.118\", \"Microsoft Edge\";v=\"124.0.2478.80\", \"Not-A.Brand\";v=\"99.0.0.0\"",
                        "Sec-Ch-Ua-Mobile": "?0",
                        "Sec-Ch-Ua-Model": "\"\"",
                        "Sec-Ch-Ua-Platform": "\"Windows\"",
                        "Sec-Ch-Ua-Platform-Version": "\"15.0.0\"",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
                        "X-Asbd-Id": "129477",
                        "X-Csrftoken": Csrftoken,
                        "X-Ig-App-Id": "936619743392459",
                        "X-Ig-Www-Claim": "hmac.AR21dPSJwNbCtC6NJO5PGIenoMwX2uEkwqg_7b-8vH-1yrRE",
                        "X-Requested-With": "XMLHttpRequest"
                    }
                    res = requests.get(
                        api,
                        headers=self.headers,
                        params=params,
                        timeout=(4,5)
                    )

                    if 'checkpoint_required' in res.text:
                        print(f'checkpoint_required ==>{res.text}')
                        redis_map.lrem("ins", 1, Cookirstr)
                        time.sleep(1)
                        continue
                    if 'Media is unavailable' in res.text:
                        print(f"Media is unavailable ==》 {res.text}")
                        res = res.json()

                        break

                    if res.status_code == 400:
                        print(f'Risk control ===> Please help us verify your identity {res.text}!')
                        redis_map.lrem("ins", 1, Cookirstr)
                        time.sleep(1)
                        continue
                    if res.text.startswith('<!DOCTYPE html><html class="'):
                        print(f"Risk control ===> <!DOCTYPE html><html class=")
                        redis_map.lrem("ins", 1, Cookirstr)
                        time.sleep(1)
                        continue

                    if '请稍等几分钟再试' in res.text:
                        print(f'Risk control ===> Please wait a few minutes and try again!')
                        redis_map.lrem("ins", 1, Cookirstr)
                        time.sleep(1)
                        continue
                    if '<title>Instagram</title>' in res.text:
                        print(f'Risk control ===> <title>Instagram</title> >>= The current account has been forcibly logged out!')
                        redis_map.lrem("ins", 1, Cookirstr)
                        time.sleep(1)
                        continue

                    if "id='has-finished-comet-page'" in res.text:
                        print(f"Have to login!")
                        time.sleep(10)
                        continue

                    break
                except Exception as e:
                    print(f">>> Internet: {e}")
                    time.sleep(1)
            print(res.json())
            try:
                edges = res.json().get("child_comments",[])
            except Exception as e:
                print(f"parse  edges error:{e}")
                edges = []
            for comment in edges:
                try:
                    # Post details page: replier's nickname, replier's profile link, replier's verification status, number of likes for the reply, reply time, reply count, and ideally, associate the reply and the relationship between the reply and sub-replies.
                    #
                    saveitem = {}
                    saveitem["post_url"] = item['post_url']
                    saveitem["post_id"] = item['post_id']
                    saveitem["comment_user_id"] = comment.get("user").get("id")
                    saveitem["comment_username"] = comment.get("user").get("username")
                    saveitem["is_commenter_verified"] = comment.get("user").get("is_verified")
                    saveitem["comment_id"] = comment.get("pk")
                    saveitem["comment_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment["created_at"]))
                    saveitem["comment_content"] = comment.get("text")
                    saveitem["comment_like_count"] = comment.get("comment_like_count")
                    saveitem["comment_reply_count"] = '-'
                    print(f"Post No.: {self.start_count}, Page No.: {page}, Comment: ", saveitem["comment_content"], saveitem)
                    with open(f"temp{db_number}.txt", 'a', encoding='utf-8') as f:
                        f.write(json.dumps(saveitem))
                        f.write('\n')





                except Exception as e:
                    print(f">>>error: cms {e}")


            if res.json().get("has_more_head_child_comments") is False:
                break

            try:
                next_min_id = res.json()['next_min_child_cursor']
                params["min_id"] = next_min_id
                print(f">>> Next Page:{params}")


            except Exception as e:
                print(f">>> Fail to load next page:{e}")
                time.sleep(5)
                # return

    def parse(self):
        df = pandas.read_csv(f"comments{db_number}.csv")
        self.records = sorted(df.to_dict(orient='records'),key=lambda x:x.get("comment_reply_count"),reverse=True)[468:]
        for rec in self.records:
            self.start_count += 1

            print(f">>> Visiting:{rec['comment_id'] }  {self.start_count} ")
            if rec.get("comment_reply_count") <=0 :
                continue
            try:
                self._download(rec)
            except Exception as e:
                print(f">>> error: {e}")
                time.sleep(10)


if __name__ == "__main__":
    # os.environ["http_proxy"] = "http://127.0.0.1:7890"
    # os.environ["https_proxy"] = "http://127.0.0.1:7890"

    Cookirstr = 'cookie'

    db_number = 10
    redis_map = redis.Redis(db=db_number)

    Com().parse()



