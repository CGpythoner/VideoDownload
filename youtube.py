# -*- coding:utf-8 -*-
import json
import random
import time
import os
import re
import requests
from myLogger import my_logger
from utils import random_useragent
from settings import proxy_list
# 关闭安全请求警告
requests.packages.urllib3.disable_warnings()

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': random_useragent(),
}


def get_cookie():
    url = 'https://www.youtube.com/'
    proxies = None
    if proxy_list:
        proxy = random.choice(proxy_list)
        proxies = {'http': proxy, 'https': proxy}
    response = requests.get(url, headers=headers, proxies=proxies, verify=False, timeout=10)
    cookie_value = ''
    for key, value in response.cookies.items():
        cookie_value += key + '=' + value + ';'
    cookie_info = {'cookie': cookie_value, 'update_time': int(time.time()), 'expire': 7}
    with open('config/ytb_cookie.json', 'w', encoding='utf-8')as f:
        f.write(json.dumps(cookie_info, ensure_ascii=False))
    return cookie_info


def get_page(url):
    if not os.path.exists('config/ytb_cookie.json'):
        get_cookie()  # 首次更新
    with open('config/ytb_cookie.json', 'r', encoding='utf-8')as f:
        data = f.read()
    if data:
        data = json.loads(data)
        expire = data.get('expire', 1)
        update_time = data.get('update_time', int(time.time()))
        if int(time.time()) >= update_time + expire * 86400:
            data = get_cookie()  # 过期更新
        cookie = data.get('cookie')
        headers.update({'cookie': cookie})
        proxies = None
        if proxy_list:
            proxy = random.choice(proxy_list)
            proxies = {'http': proxy, 'https': proxy}
        resp = requests.get(url=url, headers=headers, verify=False, proxies=proxies)
        my_logger.info(f'youtube page status_code: {resp.status_code}')
        return resp.text
    return None


def get_youtube_video_url(url):
    """解析出video_url"""
    video_url_list = []
    page_source = get_page(url)
    player_response_unnormal = re.search('streamingData":(\{.*?\}\]\})', page_source)
    player_response = re.search('streamingData":(\{.*?\}),"playerAds"', page_source)
    if player_response or player_response_unnormal:
        try:
            player_response = json.loads(player_response.group(1))
            formats = player_response.get('formats')
            for mat in formats:
                url = mat.get('url')
                video_url_list.append(url)
            # adaptiveFormats = player_response.get('adaptiveFormats')
            # for adamats in adaptiveFormats:
            #     url = adamats.get('url')
        except:
            try:
                if player_response_unnormal:
                    player_response = json.loads(player_response_unnormal.group(1))
                    formats = player_response.get('formats')
                    for mat in formats:
                        url = mat.get('url')
                        video_url_list.append(url)
                    # adaptiveFormats = player_response.get('adaptiveFormats')
                    # for adamats in adaptiveFormats:
                    #     url = adamats.get('url')
            except Exception as e:
                my_logger.error(f'Error: youtube parse video url error: {e.args}')
    else:
        my_logger.info('player_response不存在')
    my_logger.info(f'youtube video list: {video_url_list}')
    return video_url_list[:1]

