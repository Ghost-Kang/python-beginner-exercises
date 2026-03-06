"""
把从jason api 读取的数据 保存到 csv文件

"""

__author__ = 'wangxukang'
__date__ = '2026-03-26'

import pandas as pd
import json
from pathlib import Path

#─────────────────────────────────────────
# 模拟 API 返回的 JSON 数据
# ─────────────────────────────────────────

MOCK_API_RESPONSE = {
    "code": 200,
    "message": "success",
    "total": 12,
    "data": [
        {
            "id": 1, "name": "张伟", "email": "zhangwei@company.com",
            "department": "研发部", "position": "高级工程师", "salary": 28000,
            "join_date": "2020-03-15", "active": True,
            "skills": ["Python", "Go", "Docker"],
            "address": {"city": "北京", "district": "海淀区"}
        },
        {
            "id": 2, "name": "李娜", "email": "lina@company.com",
            "department": "产品部", "position": "产品经理", "salary": 25000,
            "join_date": "2021-06-01", "active": True,
            "skills": ["Axure", "Figma"],
            "address": {"city": "上海", "district": "浦东新区"}
        },
        {
            "id": 3, "name": "王芳", "email": "wangfang@company.com",
            "department": "市场部", "position": "市场总监", "salary": 35000,
            "join_date": "2019-11-20", "active": True,
            "skills": ["SEO", "SEM", "数据分析"],
            "address": {"city": "广州", "district": "天河区"}
        },
        {
            "id": 4, "name": "赵磊", "email": "zhaolei@company.com",
            "department": "研发部", "position": "测试工程师", "salary": 20000,
            "join_date": "2022-04-10", "active": False,
            "skills": ["Selenium", "JMeter"],
            "address": {"city": "深圳", "district": "南山区"}
        },
        {
            "id": 5, "name": "陈静", "email": "chenjing@company.com",
            "department": "人事部", "position": "HR经理", "salary": 22000,
            "join_date": "2020-09-05", "active": True,
            "skills": ["招聘", "绩效管理"],
            "address": {"city": "北京", "district": "朝阳区"}
        },
        {
            "id": 6, "name": "刘洋", "email": "liuyang@company.com",
            "department": "财务部", "position": "财务主管", "salary": 26000,
            "join_date": "2018-07-22", "active": True,
            "skills": ["Excel", "SAP", "税务"],
            "address": {"city": "成都", "district": "武侯区"}
        },
        {
            "id": 7, "name": "孙丽", "email": "sunli@company.com",
            "department": "研发部", "position": "前端工程师", "salary": 23000,
            "join_date": "2021-12-08", "active": True,
            "skills": ["Vue", "React", "TypeScript"],
            "address": {"city": "杭州", "district": "西湖区"}
        },
        {
            "id": 8, "name": "周强", "email": "zhouqiang@company.com",
            "department": "运维部", "position": "运维工程师", "salary": 21000,
            "join_date": "2023-02-14", "active": True,
            "skills": ["Linux", "K8s", "CI/CD"],
            "address": {"city": "武汉", "district": "洪山区"}
        },
        {
            "id": 9, "name": "吴敏", "email": "wumin@company.com",
            "department": "产品部", "position": "UI设计师", "salary": 19000,
            "join_date": "2022-08-30", "active": False,
            "skills": ["Figma", "Sketch", "PS"],
            "address": {"city": "南京", "district": "鼓楼区"}
        },
        {
            "id": 10, "name": "郑浩", "email": "zhenghao@company.com",
            "department": "研发部", "position": "后端工程师", "salary": 27000,
            "join_date": "2020-05-18", "active": True,
            "skills": ["Java", "Spring", "MySQL"],
            "address": {"city": "北京", "district": "西城区"}
        },
        {
            "id": 11, "name": "冯雪", "email": "fengxue@company.com",
            "department": "市场部", "position": "内容运营", "salary": 16000,
            "join_date": "2023-07-01", "active": True,
            "skills": ["文案", "新媒体", "短视频"],
            "address": {"city": "上海", "district": "静安区"}
        },
        {
            "id": 12, "name": "韩磊", "email": "hanlei@company.com",
            "department": "销售部", "position": "销售经理", "salary": 18000,
            "join_date": "2019-03-11", "active": True,
            "skills": ["客户关系", "谈判", "CRM"],
            "address": {"city": "重庆", "district": "渝中区"}
        }
    ]
}

def jason_to_dataframe(data:list[dict])->pd.DataFrame:
    cleand = []
    for item in data:
        r = item.copy()
        for k,v in item.items():
            if isinstance(v, list):
                r[k] = (";".join(x for x in v))

        cleand.append(r)


    df = pd.json_normalize(cleand)

    if "join_date" in df.columns:
        df["join_date"] = pd.to_datetime(df["join_date"])

    return df

def dataframe_to_csv(df:pd.DataFrame,path:str)->None:
    df.to_csv(path,index=False,encoding="utf-8-sig")
    size = Path(path).stat().st_size
    print(f"  ✅ 已写入 {len(df)} 行 × {len(df.columns)} 列")
    print(f"  📁 路径: {path}  ({size:,} bytes)")

def print_section(title:str, width:int= 54) -> None:
    print(f"\n{'-'*width}")
    print(f"  {title}")
    print(f"{'-'*width}")



def main():

    out_file = "14_output.csv"

    print_section("step1 get api data")
    raw_data = MOCK_API_RESPONSE["data"]
    print(f"共 {len(raw_data)} 条记录，字段:{list(raw_data[0].keys())}")

    print_section("transform data to dataframe")
    df = jason_to_dataframe(raw_data)
    print(f"  DataFrame 形状: {df.shape[0]} 行 × {df.shape[1]} 列")
    print(f"  列名: {df.columns.tolist()}")
    print(f"\n  数据类型:")
    for col, dtype in df.dtypes.items():
        print(f"    {col:<25} {str(dtype)}")
    # ── Step 3: 预览数据 ──────────────────
    print_section("Step 3  数据预览（前 5 行）")
    print(df.head().to_string(index=False))

    # ── Step 4: 基础统计 ──────────────────
    print_section("Step 4  数值列统计（describe）")
    print(df[["salary"]].describe().to_string())

    print_section("Step 4b  分组统计（按部门平均薪资）")
    dept_stats = (
        df.groupby("department")["salary"]
          .agg(人数="count", 平均薪资="mean", 最高薪资="max")
          .sort_values("平均薪资", ascending=False)
          .astype({"人数": int, "平均薪资": int, "最高薪资": int})
    )
    print(dept_stats.to_string())

    print_section("Step 4c  在职 / 离职 人数")
    print(df["active"].value_counts().rename({True: "在职", False: "离职"}).to_string())

    # ── Step 5: 数据筛选示例 ──────────────
    print_section("Step 5  筛选示例（薪资 ≥ 25000 且在职）")
    filtered = df[(df["salary"] >= 25000) & (df["active"] == True)]
    print(filtered[["name", "department", "position", "salary"]].to_string(index=False))

    # ── Step 6: 写入 CSV ──────────────────
    print_section("Step 6  写入 CSV 文件")
    dataframe_to_csv(df, out_file)

    # ── Step 7: 读回验证 ──────────────────
    print_section("Step 7  读回验证")
    df_verify = pd.read_csv(out_file, encoding="utf-8-sig")
    print(f"  读回行数: {len(df_verify)}，列数: {len(df_verify.columns)}")
    print(f"  列名一致: {df.columns.tolist() == df_verify.columns.tolist()}")
    print(f"\n  前 3 行验证:")
    print(df_verify.head(3).to_string(index=False))

    print("\n" + "=" * 54)
    print("  ✅ 全部完成！")
    print("=" * 54)

if __name__ == "__main__":
    main()