"""
 关键节日倒计时
功能：
支持 多个事件倒计时
支持 用户输入新事件
显示 天 / 小时 / 分钟
自动排序 最近事件
可以做成长期使用的小工具
"""

__author__ = 'wangxuknag'
__date__ = '2026-03-16'

from datetime import datetime

events ={
    "高考": "2026-06-07 09:00:00",
    "考研": "2026-12-20 09:00:00",
    "春节": "2027-02-03 00:00:00",
}


def cal_countdown(target_time):
    now = datetime.now()

    remaining = target_time - now
    if remaining.total_seconds() <= 0:
        print("finished")
        return

    day = remaining.days
    hour = remaining.seconds // 3600
    minute = (remaining.seconds % 3600) // 60

    return f"{day}天{hour}小时{minute}分钟"


def show_events():

    print(f"\n========倒计时小工具======\n")
    events_list = []
    for name, event in events.items():
        target_time = datetime.strptime(event, "%Y-%m-%d %H:%M:%S")
        target = cal_countdown(target_time)
        events_list.append((name, target_time, target))


    events_list.sort(key=lambda x: x[1])

    for name, target_time, target in events_list:
        print(f"{name}: ({target_time.date()}):{target}")


    print("\n==================\n")



def add_event():

    name = input("请输入关键日程：").strip()
    timestamp = input("输入日期的格式 %Y-%m-%d %H:%M:%D").strip()
    events[name] = timestamp
    print("事件添加成功！")


def main():
    while True:
        show_events()
        print(f"1 添加事件\n")
        print(f"2 退出程序！")

        choice = input("选择你要做的操作：").strip()

        if choice == "1":
            add_event()
        elif choice == "2":
            break


if __name__ == "__main__":
    main()

