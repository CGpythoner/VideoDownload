# -*- coding:utf-8 -*-
import json
import random
import re
import requests
from myLogger import my_logger
from settings import proxy_list
from utils import random_useragent
from urllib import parse
# 关闭安全请求警告
requests.packages.urllib3.disable_warnings()


headers = {
        'accept-language': 'zh-CN,zh;q=0.9',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',
        'referer': 'https://twitter.com/',
        'user-agent': random_useragent()
    }


def get_guest_token():
    """获取token"""
    url = 'https://api.twitter.com/1.1/guest/activate.json'
    proxies = None
    if proxy_list:
        proxy = random.choice(proxy_list)
        proxies = {'http': proxy, 'https': proxy}
    resp = requests.post(url, headers=headers, proxies=proxies, verify=False)
    if resp.status_code == 200:
        data = json.loads(resp.text)
        guest_token = data.get('guest_token', '')
        return guest_token
    return


def get_twitter_video_url(url):
    """解析出video_url"""
    video_url = ''
    proxies = None
    guest_token = get_guest_token()
    if guest_token:
        my_logger.info(f'guest_token:{guest_token}')
        headers.update({'x-guest-token': guest_token})
        tweet_id = re.search('status\/([0-9]*)\/?', url)
        if tweet_id:
            tweet_id = tweet_id.group(1)
            base_url = "https://twitter.com/i/api/graphql/8svRea_Lc0_mdhwP6dqe0Q/TweetDetail?"
            params_dict = {"focalTweetId": tweet_id, "with_rux_injections": False,
                           "includePromotedContent": True, "withCommunity": True,
                           "withQuickPromoteEligibilityTweetFields": True, "withTweetQuoteCount": True,
                           "withBirdwatchNotes": False, "withSuperFollowsUserFields": True,
                           "withBirdwatchPivots": False, "withDownvotePerspective": False,
                           "withReactionsMetadata": False, "withReactionsPerspective": False,
                           "withSuperFollowsTweetFields": True, "withVoice": True, "withV2Timeline": False}
            status_url = base_url + 'variables=' + parse.quote(json.dumps(params_dict))
            headers.update({'referer': url})

            if proxy_list:
                proxy = random.choice(proxy_list)
                proxies = {'http': proxy, 'https': proxy}
            try:
                req = requests.get(url=status_url, headers=headers, verify=False, proxies=proxies)
                if req.status_code == 200:
                    variants = re.search('variants":(\[\{.*?\}\])', req.text)
                    if variants:
                        variants = json.loads(variants.group(1))
                        for variant in variants:
                            video_url = variant.get('url')
                            if variant.get('content_type') == 'video/mp4':
                                my_logger.info(f'video_url:{video_url}')
                                return video_url
                        my_logger.info(f'video_url:{video_url}')
                        return video_url
                    my_logger.info('have not video url!')
                my_logger.info(f'request failed status_code: {req.status_code}')
            except Exception as e:
                my_logger.error(f'Error: get twitter video url error! {e.args}')
        return





