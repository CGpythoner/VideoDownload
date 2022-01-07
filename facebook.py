# -*- coding:utf-8 -*-
import json
import random
import re
import html
import requests
from myLogger import my_logger
from utils import get_cookie_from_file, random_useragent
from settings import proxy_list, fb_cookie_filename_path
# 关闭安全请求警告
requests.packages.urllib3.disable_warnings()


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def get_page(url):
    message_id = ''
    try:
        message_id_str = re.search('\/videos\/([0-9]+)[\/]?', url)
        share_message_id_str = re.search('story_fbid=([0-9]+)&', url)
        post_message_id_str = re.search('\/posts\/([0-9]+[\/]?)', url)
        watch_message_id_str = re.search('watch\/\?v=([0-9]+)&?', url)
        if message_id_str:
            message_id = message_id_str.group(1)
        elif share_message_id_str:
            message_id = share_message_id_str.group(1)
        elif post_message_id_str:
            message_id = post_message_id_str.group(1)
        elif watch_message_id_str:
            message_id = watch_message_id_str.group(1)
        my_logger.info(f'facebook message_id:{message_id}')
        cookie = get_cookie_from_file(fb_cookie_filename_path)
        if cookie:
            headers.update({'cookie': cookie})
        page_url = f'https://m.facebook.com/story.php?story_fbid={message_id}&id=1&_rdr'
        if proxy_list:
            proxy = random.choice(proxy_list)
            proxies = {'http': proxy, 'https': proxy}
        resp = requests.get(url=page_url, headers=headers, verify=False, allow_redirects=False, proxies=proxies, timeout=15)
        my_logger.info(f'facebook get_page status_code: {resp.status_code}')
        return resp.text
    except Exception as e:
        my_logger.error(f'Error Facebook get_page error: {e.args}')


def get_facebook_video_url(url):
    """解析出video_url"""
    video_url = ''
    page_source = get_page(url)
    if page_source:
        page_source = html.unescape(page_source)
        video_info = re.search('data-store="(\{"videoID.*?\})"', page_source)
        if video_info:
            try:
                video_info = html.unescape(video_info.group(1))
                video_info = json.loads(video_info)
                video_url = video_info.get('src')
                video_url = video_url.replace('\\', '')
                my_logger.info(f'facebook video_url: {video_url}')
            except Exception as e:
                my_logger.error(f'Error parse facebook video url error: {e.args}')
    return video_url


