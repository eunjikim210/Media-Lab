import json
import os
import random
import re
import time
import pandas
import requests


def send_get(url, params):
    while 1:
        try:
            time.sleep(random.uniform(1,3))
            if len(all_cookie) == 0:
                print(f'>>> No available cookie ==》 Please add')
                time.sleep(10)
                continue
            else:
                print(f">>> Number of available accounts: {len(all_cookie)}")
            Cookirstr = random.choice(all_cookie)
            Csrftoken = Cookirstr.split("csrftoken=")[-1].split(";")[0]

            headers = {
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "Cookie": Cookirstr,
                "Priority": "u=1, i",
                "Referer": "https://www.instagram.com/p/C6rviEtrTXD/",
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
                "X-Ig-Www-Claim": "hmac.AR3r_aBH0OOOH-paTUByGVuKJuWaVO9kRso1bxOA84n1GL8m",
                "X-Requested-With": "XMLHttpRequest"
            }

            response = requests.get(
                url, headers=headers, timeout=(10, 10), params=params,
            )
            # Handle the response texts
            if '请稍等几分钟再试' in response.text:
                print(f'>>>',response.text)
                continue


            if 'Rate limit exceeded' in response.text:
                print(f'>>>', response.text)
                time.sleep(10)
                all_cookie.remove(Cookirstr)
                continue

            if '似乎你过度使用了此功能' in response.text:
                print(f'>>>', f'It seems you have overused this feature')
                time.sleep(10)
                all_cookie.remove(Cookirstr)

                continue

            if 'https://www.instagram.com/challenge/?next=' in response.text:
                print(f'>>>', f'https://www.instagram.com/challenge/?next=', 'Account issue')
                time.sleep(1)
                all_cookie.remove(Cookirstr)
                continue

            if '<title>Instagram</title>' in response.text:
                print(f'>>> Cookie has expired:', Cookirstr)
                time.sleep(1)
                all_cookie.remove(Cookirstr)

                continue

            if '<title>Log in · Instagram</title>' in response.text:
                print(f'>>> Cookie has expired:', Cookirstr)
                time.sleep(1)
                all_cookie.remove(Cookirstr)
                continue

            if '"message":"请稍等几分钟再试。"' in response.text:
                print(f'>>> Cookie has expired', Cookirstr, response.text)
                time.sleep(1)
                all_cookie.remove(Cookirstr)
                continue
            if response.status_code != 200:
                print(f">>> Error status code: {response.text}")
                time.sleep(1)
                all_cookie.remove(Cookirstr)
                continue
            return response
        except Exception as e:
            print(f'>>>', f'Some error: {e}')


def parse_user_id(user_link):
    while 1:
        home_response = send_get(user_link, {})

        user_id = "".join(re.findall(r'"profile_id":"(\d+)",', home_response.text)[:1])
        if user_id == "":
            print(f'>>> Could not retrieve user ID, trying again: {user_link}')
            time.sleep(.5)
            continue

        return user_id



def following_list_scraper(user_link):
    user_id = parse_user_id(user_link)

    if user_id == "":
        return print(f"{flag}>>> Could not retrieve user ID, {user_link} {user_id}")

    print(f'>>> Parsed user ID: {user_id}')

    list_api = f'https://www.instagram.com/api/v1/friendships/{user_id}/following/'

    list_params = {
        "count": 12,
    }
    for page in range(1, 1000):

        response = send_get(list_api, list_params)

        results = response.json().get("users", [])

        if page == 1 and len(results) <= 0:
            return print(f"{flag}>>> Could not retrieve follow list for this user [It might be zero or unable to access]: {user_link}")

        print(f'{flag}>>>', user_link, page, f'>>> Followers on current page: ', len(results))

        for iml in results:
            saveinfo = {}
            saveinfo["User_link"] = user_link
            saveinfo["User_ID"] = user_id

            saveinfo["Following_name"] = iml.get("full_name")
            saveinfo["Following_ID"] = iml.get("id")
            saveinfo["Following_username"] = iml.get("username")
            saveinfo["Following_profile_picture"] = iml.get("profile_pic_url")
            saveinfo["Is_following_verified"] = iml.get("is_verified")
            saveinfo["timestamp"] = int(time.time())
            print(f'{flag}>>>', page, saveinfo)
            with open("./account/temp_data.txt", 'a', encoding='utf-8') as f:
                f.write(json.dumps(saveinfo))
                f.write('\n')

        if len(results) < 2:
            break

        list_params["max_id"] = response.json().get("next_max_id")
        if list_params["max_id"] is None:
            break
        else:

            print(f"{flag}>>> Next page: {list_params['max_id']}")


def parse_cookie():
    with open("./account/cookie.txt", 'r', encoding='utf-8') as f:
        txt = f.read()
    Cookirstrs = [
        "".join([i for i in i.strip().split("|") if "csrftoken" in i])
        for i in txt.split("\n")
        if 'csrftoken' in i
    ]
    return Cookirstrs


def parse_userlink():
    with open("./account/userlink.txt", 'r', encoding='utf-8') as f:
        all_lines = [i.strip() for i in f.readlines()]

    return all_lines


if __name__ == "__main__":

    ## VPN address
    # os.environ["http_proxy"] = "http://127.0.0.1:7890"
    # os.environ["https_proxy"] = "http://127.0.0.1:7890"

    all_cookie = parse_cookie()

    all_user_link = parse_userlink()

    ## Collect the follow list for each user link
    for user_link_index,user_link in list(enumerate(all_user_link))[425:]:
        flag = f'[{user_link_index}/{len(all_user_link)}]'
        following_list_scraper(user_link=user_link)

    if os.path.exists("./account/temp_data.txt"):
        with open("./account/temp_data.txt", 'r', encoding='utf-8') as f:
            lines = [json.loads(i.strip()) for i in f.readlines()]
        df = pandas.DataFrame([i for i in lines])
        writer = pandas.ExcelWriter(fr'Follow_List.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
        df.to_excel(writer)
        writer.save()
        os.remove("./account/temp_data.txt")
