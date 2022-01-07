# -*- coding:utf-8 -*-
import json
import os
import faker


def random_useragent():
    ua = faker.Faker()
    return ua.user_agent()


def get_cookie_from_file(filename):
    """获取cookie editor导出格式的 cookie"""
    with open(filename, 'r', encoding='utf-8')as f:
        data = json.loads(f.read())
    cookie_value = ''
    cookie_list = data.get('cookie', [])
    for cookie in cookie_list:
        key = cookie.get('name', '')
        value = cookie.get('value', '')
        cookie_value += key + '=' + value + ';'
    return cookie_value


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8')as f:
        data = f.readlines()
    return data

