# 豆瓣电影 Top250 数据采集器

一个基于 Python 的爬虫实战项目，用于抓取豆瓣电影 Top250 数据，并进行清洗、去重后保存为 CSV 文件。

---

## 项目结构

```bash
douban-scraper/
├── main.py             # 统一入口
├── scraper.py          # 爬虫主程序
├── cleaner.py          # 数据清洗脚本
├── utils.py            # 工具模块：日志配置、Session 创建
├── config.py           # 配置文件
├── requirements.txt    # 项目依赖
├── README.md
└── data/
    └── douban_top250.csv

