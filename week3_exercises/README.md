# 豆瓣 Top250 深度分析报告
 使用 Week 2 的数据，用 Jupyter 做可视化分析。

- 分析维度（至少 5 个）
- 评分分布直方图
- 看评分集中在哪个区间

- 年代趋势折线图
- 每个年代有多少部高分电影

- 导演作品数 Top10
- 哪些导演上榜最多

- 类型词云图
- 哪些类型最受欢迎（动作/爱情/科幻）

- 评价人数 vs 评分散点图
- 冷门神作 vs 热门大片的分布

- TOP10 电影卡片展示
- 表格 + 海报图片

### notebook转换html文件命令
- jupyter nbconvert --to html analysis.ipynb

##项目结构

```bash
📁 movie-analysis/
├── analysis.ipynb       # 主分析文件
├── data
｜   ｜douban_top250.csv    # 数据源
├── images/              # 图表导出
│   ├── 01_***.png
│   ├── 02_***.png
│   └── ...
└── README.md