import requests
import time
import json
import re

ua = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }


def get_data():
    url = "https://www.toutiao.com/api/pc/feed/?min_behot_time=0&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&as=A1856D8CAA7AD50&cp=5DCA5AFDB5B0CE1&_signature=UD2DNgAgEBKiErFxt-IdO1A9gyAAA34"
    base_rul = "https://www.toutiao.com/a{}/"
    comment_url = "https://www.toutiao.com/api/pc/article/v4/tab_comments/?aid=24&app_name=toutiao-web&group_id={}&item_id={}&offset=0&count=5"
    response = requests.get(url=url,headers=ua)
    js = json.loads(response.text)
    news_list = js["data"]
    for news in news_list:
        comments_count = int(news.get("comments_count",-1))
        item_id = news["item_id"]
        group_id = news["group_id"]
        if comments_count > 0:
            response_detail = requests.get(comment_url.format(group_id,item_id),headers = ua)
            cmt_js = json.loads(response_detail.text)
            comment(cmt_js["data"])



def comment(cmt_dict):
    for _cmt in cmt_dict:
        cmt = _cmt["comment"]
        user_verified = cmt["user_verified"]
        user_name = cmt["user_name"]
        user_id = cmt["user_id"]
        req_user(user_id)
        print(user_id,":",user_name,user_verified)

def req_user(user_id):
    url = "https://www.toutiao.com/c/user/{}/".format(user_id)
    res = requests.get(url,headers=ua)
    guanzhu = re.findall("guanzhu:\'(.*?)\',",res.text)
    fensi = re.findall("fensi:\'(.*?)\',",res.text)
    print(guanzhu,fensi)


if __name__ == "__main__":
    get_data()
    #comment()