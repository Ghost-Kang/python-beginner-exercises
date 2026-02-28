"""
读取score.txt 文档 读取姓名跟分数，找出最高分，最低分，平均分
score={"name":name,"score":score}


"""

__author__ = ('wangxukang')
__date__= '2026/02/28'

import os
import sys

#---------ansi颜色常量
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

score_file = "score.txt"
info_list = []

def grade_label(score):
    """根据分数返回等级标签"""
    if score >= 90:
        return f"{GREEN}优秀 ★{RESET}"
    elif score >= 80:
        return f"{CYAN}良好 ◆{RESET}"
    elif score >= 70:
        return f"{YELLOW}中等 ●{RESET}"
    elif score >= 60:
        return f"{YELLOW}及格 ○{RESET}"
    else:
        return f"{RED}不及格 ✗{RESET}"

def score_analyzer():
    try:
        with open(score_file, "r", encoding="utf-8") as f:
            for lineno, raw  in enumerate(f,start=1):
                if not raw.strip():
                    continue
                cnt = raw.strip().split(",")
                if len(cnt) != 2:
                    print(f"socre.txt文件的第{lineno}格式不对，请check内容{raw}！")
                    continue
                info = (cnt[0].strip(),float(cnt[1].strip()))
                info_list.append(info)
    except FileNotFoundError:
        print("file not exist, please check file path!")

def analyzer():
    score = [s for _, s in info_list]
    max_score = max(score)
    min_score = min(score)
    avg_score = sum(score) / len(score)
    top = [(n,s) for n,s in info_list if s == max_score]
    low = [(n,s) for n,s in info_list if s == min_score]
    fail = [(n,s) for n,s in info_list if s <= 60]
    return avg_score,max_score,min_score,top,low,fail

def show_result():
    print(f"\n{BOLD}{CYAN}{'═'*48}{RESET}")
    print(f"{BOLD}{CYAN}        📊  成 绩 单 分 析 报 告        {RESET}")
    print(f"{BOLD}{CYAN}{'═'*48}{RESET}\n")
    score_analyzer()
    if not info_list:
        print(f"{RED}没有有效数据，程序退出。{RESET}")
        sys.exit(1)
    avg_score1,max_score1,min_score1,top1,low1,fail1 = analyzer()
    total = len(info_list)
    print(f"  总人数  : {BOLD}{total}{RESET} 人")
    print(f"  平均分  : {BOLD}{YELLOW}{avg_score1:.2f}{RESET} 分")
    print(f"  最高分  : {BOLD}{GREEN}{max_score1:.0f}{RESET} 分  → " +
          "、".join(f"{n}" for n, _ in top1))
    print(f"  最低分  : {BOLD}{RED}{min_score1:.0f}{RESET} 分  → " +
          "、".join(f"{n}" for n, _ in low1))

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "score.txt")
    if not os.path.exists(file_path):
        print(f"{RED}错误：找不到文件 {file_path}{RESET}")
        sys.exit(1)

    show_result()