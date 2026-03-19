"""
这是一个配置文件

"""
__author__ = 'wangxukang'
__date__ = '2026-03-19'

import os

BASE_URL = "https://movie.douban.com/top250"

DATA_DIR = "data"

OUTPUT_FILE = os.path.join(DATA_DIR, "douban_top250.csv")

HEADERS = {
    "User-Agent":(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Referer":"https://movie.douban.com/",
    "Accept-Language":"zh-CN,zh;q=0.9"
}

REQUEST_TIMEOUT=10
RETRY_TIMES=3
REQUEST_DELAY=1
PAGE_SIZE=25
TOTAL_COUNT=250
