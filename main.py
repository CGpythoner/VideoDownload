# -*- coding:utf-8 -*-
import os
import click
import settings
from utils import read_file
from concurrent.futures import ThreadPoolExecutor, as_completed
from video_download import download_video
from youtube import get_youtube_video_url
from facebook import get_facebook_video_url
from twitter import get_twitter_video_url


@click.command()
@click.option('--r', default='', help='指定读取文件')
@click.option('--u', default='', help='输入对应url')
@click.option('--out', default='', help='指定输出目录')
def main(r, u, out):
    tasks = []
    url_list = []
    if r:
        datas = read_file(r)
        tasks.extend([url.strip('\n') for url in datas])
    if u:
        tasks.append(u)
    if out:
        if not os.path.exists(out):
            os.makedirs(out)
    for task in tasks:
        if task.find('youtube') != -1:
            video_url = get_youtube_video_url(task)  # 返回列表
            url_list.extend(video_url)
        elif task.find('facebook') != -1:
            video_url = get_facebook_video_url(task)
            url_list.append(video_url)
        elif task.find('twitter') != -1:
            video_url = get_twitter_video_url(task)
            url_list.append(video_url)
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = [ex.submit(download_video, url, out) for url in url_list]
        for future in as_completed(futures):
            result = future.result()


if __name__ == '__main__':
    main()
