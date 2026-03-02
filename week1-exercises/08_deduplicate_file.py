"""
根据输入的文件的内容，删除重复的内容

主要是文件的读写操作
"""

__author__ = 'wangxukang'
__date__ = '2026-03-02'

from pathlib import Path

duplicate = set()
linenumber = set()
deduplicate_result = []

def deduplicate_file():

    try:
        with open("08_sample.txt", 'r', encoding="utf-8") as f:
            for lineno, raw in enumerate(f,start=1):
                if raw not in duplicate:
                    duplicate.add(raw)
                    linenumber.add(lineno)
                    deduplicate_result.append(raw)

    except FileNotFoundError:
        print("please check your soruce file path!")


    #写入内容的格式

    enties=(
        f"\n{"-"*50}\n"
        f"重复行数是：{linenumber}\n内容的{duplicate}\n"
        f"{"-"*50}\n"
        f"{deduplicate_result}"
    )

    with open("08_output.txt", 'w', encoding ='utf-8') as f:
        f.write(enties)


if __name__ == '__main__':
    deduplicate_file()
