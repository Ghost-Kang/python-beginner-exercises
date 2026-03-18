"""
统计每个月的消费情况
"""

__author__ = "wangxuknag"
__date__ = "2026-03-16"

from datetime import datetime
import pandas as pd
import os
import matplotlib.pyplot as plot
# 解决中文显示问题
plot.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plot.rcParams['axes.unicode_minus'] = False

FILE_NAME = 'account_book.xlsx'
COLUMNS = ['日期','类型','金额','分类','备注']

def init_file():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(FILE_NAME, index=False)

def load_file():
    if not os.path.exists(FILE_NAME):
        init_file()
    df = pd.read_excel(FILE_NAME)
    if df.empty:
        return pd.DataFrame(columns=COLUMNS)
    return df

def save_file(df):
    df.to_excel(FILE_NAME, index=False)

def normalize_data(df):
    df = load_file()
    if df.empty:
        return df

    df = df.copy()

    df['日期'] = pd.to_datetime(df['日期'], errors='coerce')
    df['金额'] = pd.to_numeric(df['金额'], errors='coerce').fillna(0)
    df['类型'] = df['类型'].astype(str).str.strip()
    df['分类'] = df['分类'].astype(str).fillna('')
    df['备注'] = df['备注'].astype(str).fillna('')
    return df

def add_record():
    df = load_file()

    date_str = input('请输入日期，格式 %Y-%m-%d,如果是今天就按回车键：').strip()

    if not date_str:
        date_str = datetime.today().strftime('%Y-%m-%d')

    record_type = input('请输入消费类型（收入/支出）：').strip()

    if record_type not in ['收入', '支出']:
        print('输入的正确的消费类型，（收入/支出）！')
        return
    try:
        amount = float(input('请输入金额：').strip())
    except ValueError:
        print('输入的数据有误\n')
        return

    category = input('请输入分类（消费/餐饮/交通）：').strip()
    note = input('请输入备注：').strip()

    new_item = pd.DataFrame([{
        '日期': date_str,
        '类型': record_type,
        '金额': amount,
        '分类': category,
        '备注': note
    }])

    df = pd.concat([df, new_item],ignore_index=True)
    save_file(df)
    print('记录添加完成\n')

def show_records():

    df = normalize_data(load_file())

    if df.empty:
        print('没有任何数据\n')
        return

    display_df = df.copy()
    display_df['日期'] = display_df['日期'].dt.strftime('%Y-%m-%d')
    display_df.index = range(1, len(display_df)+1)

    print('打印所有的数据\n')
    print(display_df.to_string())


def calculate_balance():
    df = normalize_data(load_file())
    if df.empty:
        print('没任何数据\n')
        return

    income = df.loc[df['类型']=='收入', '金额'].sum()
    expense = df.loc[df['类型']=='支出', '金额'].sum()
    balance = income - expense

    print('当前余额的情况：\n')
    print(f'总收入：{income:.2f}\n')
    print(f'总支出：{expense:.2f}\n')
    print(f'余额：{balance:.2f}\n')



def month_report():
    df = normalize_data(load_file())
    if df.empty:
        print('没有任何数据\n')
        return

    month = input('请收入要统计的月 %Y-%m').strip()
    month_df = df[df['日期'].dt.strftime('%Y-%m') == month]

    incomes = month_df.loc[month_df['类型']=='收入', '金额'].sum()
    expenses = month_df.loc[month_df['类型']=='支出', '金额'].sum()
    balance = incomes - expenses

    print('当前余额的情况：\n')
    print(f'总收入：{incomes:.2f}\n')
    print(f'总支出：{expenses:.2f}\n')
    print(f'余额：{balance:.2f}\n')

    expense_by_category =(
        month_df[month_df['类型'] == '支出'].
        groupby('分类')['金额'].sum()
        .sort_values(ascending=False)
    )

    if expense_by_category.empty:
        print('本月无支出\n')
        return
    else:
        print(expense_by_category.to_string())

    print("\n-- 本月明细 --")
    display_df = month_df.copy()
    display_df["日期"] = display_df["日期"].dt.strftime("%Y-%m-%d")
    display_df.index = range(1, len(display_df) + 1)
    print(display_df.to_string())


def delete_record():
    df = normalize_data(load_file())
    if df.empty:
        print('没有任何数据\n')
        return

    show_records()
    try:
        index = int(input('输出要删除的index：').strip())
    except ValueError:
        print('请输入正确的号码\n')
        return

    if index < 1 or index > len(df):
        print('编号超范围\n')
        return

    df = df.drop(df.index[index-1]).reset_index(drop=True)
    save_file(df)
    print('删除成功\n')

def category_report():
    df = normalize_data(load_file())
    if df.empty:
        print('没有任何数据\n')
        return

    category_df = df[df['类型'] == '支出']

    if category_df.empty:
        print('没有支出信息\n')
        return

    categorys = (
        category_df.groupby('分类')['金额'].sum()
        .sort_values(ascending=False)
    )

    print('分类统计\n')
    print(categorys.to_string())


def edit_record():
    df = normalize_data(load_file())
    if df.empty:
        print('没有任何数据\n')
        return

    show_records()

    try:
        idx = int(input('选一下你要编辑的行号').strip())
    except ValueError:
        print('输入的编号异常\n')
        return

    if idx < 1 or idx > len(df):
        print('超出范围\n')
        return

    row_id = idx -1
    old = df.loc(row_id)

    new_date = input(f'日期：[{old["日期"].strftime('%Y-%m-%d')}]:').strip()
    new_type = input(f'类型[{old["类型"]}]:').strip()
    new_amount = input(f'金额[{old["金额"]}]:').strip()
    new_category = input(f'分类[{old["分类"]}]:').strip()
    new_note = input(f'备注[{old["备注"]}]:').strip()

    if new_date:
        df.at[row_id, '日期'] = new_date
    if new_type:
        if new_type not in ['支出', '收入']:
            print('输入的类型有误\n')
            return
        df.at[row_id, '类型'] = new_type

    if new_amount:
        try:
            df.at[row_id, '金额'] = float(new_amount)
        except ValueError:
            print('输入的金额有误\n')
            return

    if new_category:
        df.at[row_id, '分类'] = new_category

    if new_note:
        df.at[row_id, '备注'] = new_note

    save_file(df)
    print('<UNK>\n')


def plot_category_bar():
    df = normalize_data(load_file())
    type_df = df[df['类型'] == '支出']
    if type_df.empty:
        print('no data\n')
        return

    category = (
        type_df.groupby('类型')['金额'].sum()
        .sort_values(ascending=False)
    )

    plot.figure(figsize = (10, 6))
    plot.barh(category.index, category.values)
    plot.title('out bar')
    plot.xlabel('type')
    plot.ylabel('incomes')
    plot.xticks(rotation = 45)
    plot.tight_layout()
    plot.show()


def plot_category_pie():
    df = normalize_data(load_file())
    type_df = df[df['类型'] == '支出']
    if type_df.empty:
        print('no data\n')
        return

    result=(
        type_df.groupby('分类')['金额'].sum()
        .sort_values(ascending=False)
    )

    plot.figure(figsize = (8, 8))
    plot.pie(result.values,labels=result.index, autopct='%1.0f%%')
    plot.title('支出饼图')
    plot.tight_layout()
    plot.show()


def plot_monthly_trend():
    df = normalize_data(load_file())
    type_df = df[df['类型'] == '支出']
    if type_df.empty:
        print('no data\n')
        return

    monthly_df = type_df.copy()
    monthly_df['月份'] = monthly_df['日期'].dt.strftime('%Y-%m')
    monthly_expense = (
        monthly_df.groupby('月份')['金额'].sum()
        .sort_index()
    )

    plot.figure(figsize = (12, 8))
    plot.plot(monthly_expense.index,monthly_expense.values, marker='o')
    plot.title('月度支出')
    plot.xlabel('月份')
    plot.ylabel('金额')
    plot.xticks(rotation = 45)
    plot.tight_layout()
    plot.show()


def export_monthly_data():
    df = normalize_data(load_file())
    if df.empty:
        print('no data\n')
        return

    month = input('请输入你要导出的年月给是 yyyy-mm').strip()
    month_df = df[df['日期'].dt.strftime('%Y-%m') == month]
    if month_df.empty:
        print(f'{month}no datas\n')
        return
    out_file = f"{month}_月度统计.xlsx"

    total = pd.DataFrame({
        '项目': ["总收入","总支持","剩余"],
        "金额":[
            month_df.loc[df["类型"] == "收入", '金额'].sum(),
            month_df.loc[df["类型"] == "支出", '金额'].sum(),
            month_df.loc[df["类型"] == "收入", '金额'].sum()-
            month_df.loc[df["类型"] == "收入", '金额'].sum(),
        ]
    } )

    category_stat =(
        month_df[month_df["分类"] == "支出"]
            .groupby('类型')['金额'].sum()
                .reset_index()
                    .sort_values('金额', ascending=False)
    )

    export = month_df.copy()
    export['日期'] = export['日期'].dt.strftime('%Y-%m-%d')

    with pd.ExcelWriter(out_file) as writer:
        total.to_excel(writer, sheet_name='总计', index=False)
        category_stat.to_excel(writer, sheet_name='分类统计', index=False)
        export.to_excel(writer, sheet_name='明细', index=False)

    print(f'内容已经导入{out_file}\n')


def main():
        init_file()

        while True:
            print("===== 个人消费记账本 =====")
            print("1. 添加记录")
            print("2. 查看所有记录")
            print("3. 查看当前余额")
            print("4. 生成月度报表")
            print("5. 分类支出统计")
            print("6. 删除记录")
            print("7. 修改记录")
            print("8. 分类支出柱状图")
            print("9. 分类支出饼图")
            print("10. 每月支出趋势图")
            print("11. 导出月度报表")
            print("12. 退出")

            choice = input("请选择功能：").strip()

            if choice == "1":
                add_record()
            elif choice == "2":
                show_records()
            elif choice == "3":
                calculate_balance()
            elif choice == "4":
                month_report()
            elif choice == "5":
                category_report()
            elif choice == "6":
                delete_record()
            elif choice == "7":
                edit_record()
            elif choice == "8":
                plot_category_bar()
            elif choice == "9":
                plot_category_pie()
            elif choice == "10":
                plot_monthly_trend()
            elif choice == "11":
                export_monthly_data()
            elif choice == "12":
                print("已退出记账本。")
                break
            else:
                print("输入无效，请重新选择。\n")


if __name__ == '__main__':
    main()