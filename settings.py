# -*- coding:utf-8 -*-
import os

proxy_list = []

file_path = os.path.dirname(os.path.realpath(__file__))

config_path = os.path.join(file_path, 'config')
if not os.path.exists(config_path):
    os.makedirs(config_path)

log_path = os.path.join(file_path, 'log')
if not os.path.exists(log_path):
    os.makedirs(log_path)

download_path = os.path.join(file_path, 'result')
if not os.path.exists(download_path):
    os.makedirs(download_path)


fb_cookie_filename = 'fb_cookie.json'
ytb_cookie_filename = 'ytb_cookie.json'
tw_cookie_filename = 'tw_cookie.json'


fb_cookie_filename_path = os.path.join(config_path, fb_cookie_filename)
ytb_cookie_filename = os.path.join(config_path, ytb_cookie_filename)
tw_cookie_filename = os.path.join(config_path, tw_cookie_filename)

