import os
import shutil
import csv
from collections import defaultdict


DEST_PATH = "/Users/kang/github/python-beginner-exercises/week1-exercises"


def copy_src_to_dst():
    files = [x for x in os.listdir(os.path.dirname(__file__)) if not x.startswith(".")]
    for file in files:
        if file not in os.listdir(DEST_PATH):
            shutil.copy(file, DEST_PATH)
            print(f"copying {file} to {DEST_PATH}/{file}")


def load_csv(path)->list[dict]:
    results = []
    with open(path, newline='',encoding="utf-8-sig") as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            results.append({
                "date": row["日期"],
                "product":  row["产品名称"],
                "quantity": int(row["销售数量"]),
                "price":    float(row["单价"]),
                "amount":   float(row["销售额"]),
            })
    return results

def total_revenue(records: list[dict]) -> float:
    return sum(x for x in records)

def  top_sell_products(records: list[dict]) -> list[dict]:
    qty_by_product = defaultdict(int)
    rev_by_product = defaultdict(float)

    for r in records:
        qty_by_product[r["product"]] += r["quantity"]
        rev_by_product[r["product"]] += r["amount"]

    ranked = sorted(qty_by_product.items(), key=lambda x: x[1], reverse=True)

    results = []
    for r,(name,qty) in enumerate(ranked, start=1):
        results.append({
            "rank": r,
            "product": name,
            "quantity": qty,
            "revenue": rev_by_product[name],
        })

    return results

SEP_THICK = "═" * 60
SEP_THIN  = "─" * 60

def fmt_money(v: float) -> str:
    return f"¥{v:>12,.2f}"

def fmt_bar(value: float, max_val: float, width: int = 24) -> str:
    filled = int(value / max_val * width)
    return "█" * filled + "░" * (width - filled)


# ─────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────
def main():
    filepath = "12_sales_data.csv"

    print(f"\n{SEP_THICK}")
    print("        📊  销售数据统计分析报告")
    print(SEP_THICK)

    # 读取数据
    records = load_csv(filepath)
    print(f"\n📂 数据文件：{filepath}")
    print(f"   读取记录数：{len(records):,} 条")
    print(f"   日期范围：{records[0]['date']}  →  {records[-1]['date']}")

    # ── ① 总销售额 ──────────────────────────────
    total = total_revenue(records)
    total_qty = sum(r["quantity"] for r in records)
    total_orders = len(records)

    print(f"\n{SEP_THIN}")
    print("  ① 总体业绩概览")
    print(SEP_THIN)
    print(f"  {'总销售额':<12} {fmt_money(total)}")
    print(f"  {'总销售数量':<12} {total_qty:>12,} 件")
    print(f"  {'总订单数':<12} {total_orders:>12,} 单")
    print(f"  {'平均客单价':<12} {fmt_money(total / total_orders)}")

    # ── ② 销量最高的产品 ───────────────────────
    product_rank = top_sell_products(records)
    max_qty      = product_rank[0]["qty"]

    print(f"\n{SEP_THIN}")
    print("  ② 产品销量排行榜（按销售数量）")
    print(SEP_THIN)
    print(f"  {'排名':<4} {'产品名称':<14} {'销售数量':>8} {'销售额':>14}  图示")
    print(f"  {'----':<4} {'----------':<14} {'--------':>8} {'----------':>14}  {'------------------------'}")

    for item in product_rank:
        bar = fmt_bar(item["qty"], max_qty)
        marker = " 🏆" if item["rank"] == 1 else ""
        print(
            f"  {item['rank']:<4} {item['product']:<14} "
            f"{item['qty']:>8,} {fmt_money(item['revenue'])}  {bar}{marker}"
        )

    champion = product_rank[0]
    print(f"\n  🥇 销量冠军：{champion['product']}")
    print(f"     累计售出 {champion['qty']:,} 件，销售额 {fmt_money(champion['revenue'])}")



if __name__ == "__main__":
    copy_src_to_dst()
