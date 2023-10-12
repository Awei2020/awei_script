import requests
import re
from redis_download import Redis, download
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

apk_url = 'http://zhushou.360.cn/list/index/cid/1?page='


def get_apk_url(url, page):
    url_list = []
    for num in range(1, page):
        print(num)
        ua = UserAgent()
        headers = {
            "User-agent": ua.random,
            "Host": "zhushou.360.cn"
        }

        html = BeautifulSoup(requests.get(apk_url + str(num), headers=headers).text, 'html.parser')

        app_box = html.find(id="iconList")
        last_a_hrefs = app_box.select('li > a:last-child')

        for hf in last_a_hrefs:
            href = hf.get('href')
            down_load_url = re.search(r"(?<=&url=).*?apk.*?apk", href).group()
            url_list.append(down_load_url)
    return url_list


l = get_apk_url(apk_url, 10)

r = Redis('118.31.8.73', 26379, 'zzhaoAI888', 0)

for url in l:
    r.push('apk', url)
