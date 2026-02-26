"""
主要是使用re模块，正则表达式来判断密码是否安全
检测：是否包含数字，是否包含小写字母，是否包含大写字母，是否包含特殊字母
输出：密码的强度及安全建议

检测项	满足条件	得分
密码长度	< 6 位	0分
密码长度	6~7 位	+1
密码长度	8~11 位	+2
密码长度	≥ 12 位	+3
小写字母	含 a-z	+1
大写字母	含 A-Z	+1
数　　字	含 0-9	+1
特殊字符	含 !@#$ 等	+1
常见弱密码	命中列表	归零
连续重复	如 aaa	-1

score

等级	分数	说明
💀 非常弱	0 ~ 1	极易被破解
🔴 弱	2 ~ 3	存在风险
🟡 中等	4 ~ 5	基本安全
🟢 强	6	较为安全
🔵 非常强	7	推荐使用
"""
__author__ = 'wangxukang'
__data__ = '2026-02-26'

import re


def check_password_strength(password):
    score = 0
    passed=[]
    feedback=[]
    length = len(password)
    if length == 0:
        print("用户的密码必须大于0！")
        return
    elif length < 6:
        feedback.append("用户的密码必须大于6位（当前密码的位{}!)".format(length))
    elif length < 8:
        score += 1
        passed.append("用户的密码建议大于8位（当前密码的位{}!)".format(length))
        feedback.append("建议用户的密码超过8位！")
    elif length < 12:
        score += 2
        passed.append("用户当前密码的位{}!".format(length))
    else:
        score += 3
        passed.append("用户当前密码的位{}!".format(length))

    # check lower letters

    if re.search(r"[a-z]", password):
        score += 1
        passed.append("用户密码包含小写字母！")
    else:
        feedback.append("用户密码未包含小写字母！")

    #check upper letter

    if re.search(r"[A-Z]", password):
        score += 1
        passed.append("用户密码包含大写字母！")
    else:
        feedback.append("用户密码未包含大写字母！")

    # check numbers
    if re.search(r"[0-9]", password):
        score += 1
        passed.append("用户密码包含数字！")
    else:
        feedback.append("用户密码未包含数字！")

    # check special string
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\":\\|,.<>\/?`~]', password):
        score += 1
        passed.append("用户密码包含特殊字符！")
    else:
        feedback.append("用户密码未包含特殊字符！")

    # check weak password

    weak_password =  [
        "123456", "password", "12345678", "qwerty",
        "abc123", "111111", "123123", "admin", "letmein"
    ]

    if password.lower() in weak_password:
        score  = 0
        feedback.append("用的常见密码，比较容易攻破！")

    #check repeated string
    if re.search(r"(.)\1{2,}", password):
        score = max(0, score -1)
        feedback.append("密码中存在连续的字符，降低密码的安全性")

    if score <=1:
        level = "密码非常弱"
        hint= "建议尽快更换密码！"
    elif score <=3:
        level = "密码弱"
        hint = "密码存在一定风险"
    elif score <=5:
        level = "中等"
        hint = "密码基本安全"
    elif score <=7:
        level = "强"
        hint = "密码较安全"
    else:
        level = "非常强"
        hint = "密码非常安全"

    # show the result

    print("="*45)
    print("密码检测报告".center(45))
    print("="*45)
    print(f"密码是：{'*'* len(password)},密码的长度是：{length}!")
    print(f"密码的安全等级是：{level}!")
    print(f"密码的具体提示是：{hint}!")
    print("-"*45)

    if passed:
        print("[检测通过项]：")
        for item in passed:
            print(f"{item}")

    if feedback:
        print("[建议项]：")
        for item in feedback:
            print(f"{item}")

    return score

if __name__ == '__main__':
    print("欢迎使用密码强度检测系统！")

    while True:
        print("输入quit退出系统！")
        password = input("请输出你要检测的密码：").strip()
        if password.lower() == "quit":
            print("退出检测系统！")
            break
        check_password_strength(password)
        print()
