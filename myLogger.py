# -*- coding:utf-8 -*-

import os
from datetime import datetime
from loguru import logger

file_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(file_path, 'log')
if not os.path.exists(log_path):
    os.makedirs(log_path)


def trace():
    # 创建日志文件， 每天0点创建新的日志文件， 文件保存10天
    filename = datetime.strftime(datetime.now(), '%Y-%m-%d')
    log_file_path = os.path.join(log_path, f'runtime_{filename}.log')
    logger.add(log_file_path, format="{time} {level} {message}", level="INFO", rotation='00:00',
                       retention='7 days')
    return logger


my_logger = trace()
