"""
清洗数据

"""

__author__="wangxukang"
__date__="2026-03-19"

import pandas as pd

from config import OUTPUT_FILE
from utils import set_logger, ensure_dir_exists

logger = set_logger(__name__)

def clean_douban_data(input_file:str = OUTPUT_FILE, output_file:str = OUTPUT_FILE):
    logger.info("开始清洗的文件：%s", input_file)

    try:
        df = pd.read_csv(input_file,encoding="utf-8-sig")

    except FileNotFoundError:
        logger.error("文件不存在：%s", input_file)

    except Exception as e:
        logger.error("读取文件失败：%s", e)
        return

    try:
        df["电影名"] = df["电影名"].fillna("").astype(str).str.strip()
        df["短评"] = df["短评"].fillna("").astype(str).str.strip()
        df["影片信息"] = df["影片信息"].fillna("").astype(str).str.strip()
        df["详情链接"] = df["详情链接"].fillna("").astype(str).str.strip()
        df["图片链接"] = df["图片链接"].fillna("").astype(str).str.strip()

        df["排名"] = pd.to_numeric(df["排名"], errors="coerce")
        df["评分"] = pd.to_numeric(df["评分"], errors="coerce")
        df["评价人数"] = pd.to_numeric(df["评价人数"], errors="coerce")

        df["年份"] = df["影片信息"].str.extract(r"(\d{4})")

        before_count = len(df)

        df.drop_duplicates(subset=["详情链接"], inplace=True)
        after_dedup_count = len(df)

        df.dropna(subset=["排名", "电影名", "评分"], inplace=True)
        after_clean_count = len(df)

        df.sort_values(by="排名", inplace=True)
        df.reset_index(drop=True, inplace=True)

        ensure_dir_exists(output_file)
        df.to_csv(output_file, index=False, encoding="utf-8-sig")

        logger.info(
            "清洗完成，原始 %s 条，去重后 %s 条，最终 %s 条",
            before_count,
            after_dedup_count,
            after_clean_count
        )
        logger.info("输出文件: %s", output_file)

    except Exception as e:
        logger.error("清洗过程发生错误: %s", e)
