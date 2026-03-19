import logging
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

"""
这是一个公共的接口调用定义实现文件

"""
__author__ = 'wangxukang'
__date__ = '2026-03-19'

def set_logger(name:str = __name__) -> logging.Logger:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(name)

def create_session(retry_times:int = 3) -> requests.Session:
    session = requests.Session()
    retry_strategy = Retry(
        total=retry_times,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def ensure_dir_exists(path:str) -> None:
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name,exist_ok=True)