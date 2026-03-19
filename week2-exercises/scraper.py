"""
提取数据并形成格式化的内容
"""

__author__ = 'wangxukang'
__date__ = '2016-03-19'

import os
import time
from typing import List, Dict, Set

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from config import (
        BASE_URL,
        OUTPUT_FILE,
        HEADERS,
        RETRY_TIMES,
        REQUEST_DELAY,
        REQUEST_TIMEOUT,
        PAGE_SIZE,
        TOTAL_COUNT
)

from utils import set_logger, create_session, ensure_dir_exists


logger = set_logger(__name__)

class DoubanScraper(object):
    def __init__(self, output_file:str=OUTPUT_FILE):
        self.output_file = output_file
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.session = create_session(RETRY_TIMES)

    def fetch_page(self, start:int)-> str:
        params={"start":start}
        try:
            response = self.session.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            logger.info("页面抓起成功 start=%s", start)
            return response.text
        except Exception as e:
            logger.info("页面抓取失败： start=%s, e=%s", start, e)
            return ""


    def parse_page(self, page:str)->List[Dict]:
        if not page:
            return []

        soup = BeautifulSoup(page, 'lxml')

        items = soup.select('ol.grid_view li')
        movie=[]
        for item in items:
            try:
                rank_tag = item.select_one("em")
                rank = rank_tag.get_text(strip=True) if rank_tag else ""

                title_tags = item.select("span.title")
                title = title_tags[0].get_text(strip=True) if title_tags else ""

                rating_tag = item.select_one("span.rating_num")
                rating = rating_tag.get_text(strip=True) if rating_tag else ""

                quote_tag = item.select_one("span.inq")
                quote = quote_tag.get_text(strip=True) if quote_tag else ""

                link_tag = item.select_one("div.hd a")
                link = link_tag["href"].strip() if link_tag and link_tag.has_attr("href") else ""

                img_tag = item.select_one("div.pic img")
                image = img_tag["src"].strip() if img_tag and img_tag.has_attr("src") else ""

                comment_count = ""
                spans = item.select("div.star span")
                for span in spans:
                    text = span.get_text(strip=True)
                    if "人评价" in text:
                        comment_count = text.replace("人评价", "")
                        break

                info_tag = item.select_one("div.bd p")
                info_text = info_tag.get_text(separator=" ", strip=True) if info_tag else ""

                movie.append({
                    "排名": rank,
                    "电影名": title,
                    "评分": rating,
                    "评价人数": comment_count,
                    "短评": quote,
                    "影片信息": info_text,
                    "详情链接": link,
                    "图片链接": image
                })

            except Exception as e:
                logger.warning("单条数据解析失败: %s", e)
                continue

        logger.info("当前页解析完成，共 %s 条", len(movie))
        return movie

    def load_existing_links(self)->Set[str]:
       if not os.path.exists(self.output_file):
           logger.info("未发现历史数据，执行全量抓取")
           return set()

       try:
           df = pd.read_csv(self.output_file,encoding="utf-8-sig")
           if "详情链接" in df.columns:
               existing_links = set(df["详情链接"].dropna().astype(str))
               logger.info("已经加载历史链接%s条", len(existing_links))
               return existing_links

           logger.warning("历史文件缺少 '详情链接' 字段")
           return set()
       except Exception as e:
           logger.warning("读取历史文件失败：%s",e)
           return set()


    def save_data(self, movies:List[Dict]) -> None:
        if not movies:
            logger.info("no increase data")
            return
        ensure_dir_exists(self.output_file)
        new_df = pd.DataFrame(movies)
        try:
            if  os.path.exists(self.output_file):
                old_df = pd.read_csv(self.output_file,encoding="utf-8-sig")
                df = pd.concat([old_df, new_df], ignore_index=True)
            else:
                df = new_df

            df.drop_duplicates(subset=["详情链接"], inplace=True)

            if "排名" in df.columns:
                df["排名"] = pd.to_numeric(df["排名"], errors="coerce")
                df.sort_values(by="排名", inplace=True)

            df.to_csv(self.output_file,encoding="utf-8-sig",index=False)
            logger.info("数据保存成功：输出文件：%s", self.output_file)
        except Exception as e:
            logger.warning("cvs保存失败：%s",e)

    def run(self):
        logger.info("开始抓取豆瓣电影 top250")
        existing_links = self.load_existing_links()
        all_movies = []

        page_starter = range(0, TOTAL_COUNT, PAGE_SIZE)

        for start in tqdm(page_starter,desc="抓取进度",unit="页"):
            html = self.fetch_page(start)
            movies = self.parse_page(html)

            new_movies = []
            for movie in movies:
                if movie["详情链接"] not in existing_links:
                    new_movies.append(movie)

            all_movies.extend(new_movies)
            time.sleep(REQUEST_DELAY)

        self.save_data(all_movies)
        logger.info("任务完成，新增%s数据", len(all_movies))