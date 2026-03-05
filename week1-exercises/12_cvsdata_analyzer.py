"""
销售数据统计分析系统
=========================================
功能：
  1. 用 pandas 读取 CSV 销售数据
  2. 计算总销售额
  3. 找出销量最高的产品（完整排行榜）
  4. 按月份分组统计（含环比增长率）
"""

import pandas as pd


SEP_THICK = "═" * 65
SEP_THIN  = "─" * 65

def fmt_money(v: float) -> str:
    return f"¥{v:>13,.2f}"

def bar(value: float, max_val: float, width: int = 22) -> str:
    filled = round(value / max_val * width)
    return "█" * filled + "░" * (width - filled)


def load_cvs(path:str)->pd.DataFrame:
    df = pd.read_csv(
            path,
            encoding="utf-8-sig",
            parse_dates=["日期"],
            dtype={
                "产品名称": "string",
                "销售数量": "int64",
                "单价": "float64",
                "销售额": "float64",
            },
    )

    df = df.sort_values("日期").reset_index(drop=True)
    df['年月'] = df['日期'].dt.to_period("M")

    print(f"📂 文件：{path}")
    print(f"   行数：{len(df):,}  列数：{df.shape[1]}")
    print(f"   日期范围：{df['日期'].min().date()}  →  {df['日期'].max().date()}")
    print(f"   列信息：\n{df.dtypes.to_string()}\n")
    return df


def show_result(df:pd.DataFrame)->None:
    total_sum = df["销售额"].sum()
    total_qty = df["销售数量"].sum()
    total_orders =len(df)
    average_ord = total_sum / total_orders
    sum_max = df["销售额"].max()
    sum_min = df["销售额"].min()

    print(SEP_THIN)
    print("  ① 总体业绩概览")
    print(SEP_THIN)
    print(f"  {'总销售额':<12} {fmt_money(total_sum)}")
    print(f"  {'总销售数量':<12} {total_qty:>14,} 件")
    print(f"  {'总订单数':<12} {total_orders:>14,} 单")
    print(f"  {'平均客单价':<12} {fmt_money(average_ord)}")
    print(f"  {'最大单笔':<12} {fmt_money(sum_max)}")
    print(f"  {'最小单笔':<12} {fmt_money(sum_min)}")


def product_ranking(df:pd.DataFrame)->None:
    grp = (
        df.groupby("产品名称", as_index=False)
          .agg(
              销售数量=("销售数量", "sum"),
              销售额=("销售额",  "sum"),
              订单数=("销售额",  "count"),
          )
          .sort_values("销售数量", ascending=False)
          .reset_index(drop=True)
    )
    grp["排名"] = grp.index + 1
    grp["均单价"] = grp["销售额"]/grp["订单数"]
    max_qty = grp["销售额"].max()

    print(f"\n{SEP_THIN}")
    print("  ② 产品销量排行榜（按销售数量降序）")
    print(SEP_THIN)
    print(f"  {'排名':<4} {'产品名称':<14} {'销售数量':>8} {'销售额':>15} {'均单价':>13}  趋势图")
    print(f"  {'----':<4} {'----------':<14} {'--------':>8} {'-----------':>15} {'---------':>13}  {'----------------------'}")

    for _, row in grp.iterrows():
        medal = {1: " 🥇", 2: " 🥈", 3: " 🥉"}.get(row["排名"], "")
        b = bar(row["销售数量"], max_qty)
        print(
            f"  {int(row['排名']):<4} {row['产品名称']:<14} "
            f"{int(row['销售数量']):>8,} {fmt_money(row['销售额'])} "
            f"{fmt_money(row['均单价'])}  {b}{medal}"
        )

    champ = grp.iloc[0]
    print(f"\n  🏆 销量冠军：{champ['产品名称']}")
    print(f"     累计售出 {int(champ['销售数量']):,} 件  |  销售额 {fmt_money(champ['销售额'])}")

    # 用 pandas 描述性统计
    print(f"\n  📌 销售额描述性统计（产品维度）：")
    desc = grp["销售额"].describe().rename({
        "count": "产品数", "mean": "均值", "std": "标准差",
        "min": "最小", "25%": "25%分位", "50%": "中位数",
        "75%": "75%分位", "max": "最大",
    })
    for k, v in desc.items():
        print(f"     {k:<8} {fmt_money(v)}")


def monthly_report(df:pd.DataFrame)->None:
    monthly = (df.groupby( "年月", as_index=False)
               .agg(
                    销售数量 =( "销售数量", "sum"),
                    销售额 =( "销售额", "sum"),
                    订单数 =( "销售额", "count"),
                )
                .sort_values("年月")
                .reset_index(drop=True)
    )
    monthly["均单价"] = monthly["销售额"] / monthly["销售数量"]
    max_res = monthly["销售额"].max()

    print(f"\n{SEP_THIN}")
    print("  ③ 月度销售统计")
    print(SEP_THIN)
    print(f"  {'月份':<9} {'销售额':>14} {'数量':>7} {'订单':>6} {'均单价':>13}  趋势")
    print(f"  {'-------':<9} {'----------':>14} {'-----':>7} {'----':>6} {'---------':>13}  {'----------------------'}")

    for _, row in monthly.iterrows():
        b = bar(row["销售额"], max_res)
        peak = " ⭐" if row["销售额"] == max_res else ""
        print(
            f"  {str(row['年月']):<9} {fmt_money(row['销售额'])} "
            f"{int(row['销售数量']):>7,} {int(row['订单数']):>6,} "
            f"{fmt_money(row['均单价'])}  {b}{peak}"
        )

    best = monthly.loc[monthly["销售额"].idxmax()]
    worst = monthly.loc[monthly["销售额"].idxmin()]
    print(f"\n  📈 最佳月份：{best['年月']}   销售额 {fmt_money(best['销售额'])}")
    print(f"  📉 最淡月份：{worst['年月']}   销售额 {fmt_money(worst['销售额'])}")

def main():
    print(f"\n{SEP_THICK}")
    print("        📊  销售数据统计分析报告  （pandas 版）")
    print(SEP_THICK + "\n")

    cvs= load_cvs("12_sales_data.csv")

    show_result(cvs)
    product_ranking(cvs)
    monthly_report(cvs)

    print(f"\n{SEP_THICK}")
    print("  ✅ 分析完成")
    print(SEP_THICK + "\n")


if __name__ == '__main__':
    main()
