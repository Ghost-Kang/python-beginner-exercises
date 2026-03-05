"""
合并两个csv文件
使用 pandas库中的函数
"""
__author__ = 'wangxukang'
__date__ = '2026-03-04'

import pandas as pd

df1 = pd.read_csv("11_file1.csv")
df2 = pd.read_csv("11_file2.csv")

df_merged = pd.concat([df1, df2],ignore_index=True)

df_merged.to_csv("file.csv", index=False)

print(f"合并完成！共 {len(df_merged)} 行")
print(df_merged.head())


