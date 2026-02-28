"""
diary_program

在日志本文件中添加时间一行
主要练习 文件的io

"""


from datetime import datetime

def get_timestamp():
    now = datetime.now()
    weekdays =["mon","tue","wed","thu","fri","sat","sun"]
    ws = weekdays[now.weekday()]
    return now.strftime(f"%Y年-%m月-%d日 {ws} %H:%M:%S")

def  write_to_content():
    print("-"*50)
    print("请输入你的日记：")
    print("支持多行输入，空行及回车键后完成！")
    print('-'*50)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "exit":
            break
        lines.append(line)
        return '\n'.join(lines)

def write_to_diary():
    timestamp = get_timestamp()
    cnt = write_to_content()
    enties = (
        f"\n{"="*50}\n"
        f"{timestamp}\n"
        f"{"="*50}\n"
        f"{cnt}\n"
    )

    with open("diary_program.txt", "a", encoding="utf-8") as f:
        f.write(enties)

if __name__ == '__main__':
    write_to_diary()