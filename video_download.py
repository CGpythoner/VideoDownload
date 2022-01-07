# -*- coding:utf-8 -*-

import requests, os
import time
from tqdm import tqdm
from myLogger import my_logger
from settings import download_path


def download_video(video_url, save_path=''):
    """Download the video in HD or SD quality"""
    try:
        time.sleep(1)
        if not save_path:
            save_path = download_path
        file_size_request = requests.get(video_url, stream=True)
        file_size = int(file_size_request.headers['Content-Length'])
        block_size = 1024
        filename = str(int(time.time() * 1000))
        t = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
        file_path = os.path.join(save_path, filename)
        with open(file_path + '.mp4', 'wb') as f:
            for data in file_size_request.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
        my_logger.info(f'Video:{video_url} download successfully.')
    except Exception as e:
        my_logger.error(f'Error: Video:{video_url} download error: {e}')

