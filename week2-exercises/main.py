"""
统一入口
"""
__author__ = 'wangxukang'
__date__ = '2026-03-19'

from cleaner import clean_douban_data
from scraper import DoubanScraper
from utils import set_logger

logger = set_logger(__name__)

def main():
    logger.info("程序启动")
    scraper = DoubanScraper()
    scraper.run()

    clean_douban_data()

    logger.info("程序执行完成")


if __name__ == '__main__':
    main()
