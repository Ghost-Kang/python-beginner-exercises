"""
读取config.txt文件，把里面的配置信息形成一个dictionary
"""

__author__ = 'wangxukang'
__date__ = '2026-03-02'

import os
import sys

def parse_config(pathfile):
    config = {}
    try:
        with open(pathfile, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"): #空行跟注视行
                    continue
                if "=" not in line: #检查行的信息是否正确
                    raise ValueError(f"第{line_num}录入的信息缺少=，此行内容是：{line}!")

                #key, _,value = line.partition("=")
                key, value = line.split("=", maxsplit=1)
                key,value = key.strip(),value.strip()
                if not key:
                    continue
                config[key] = value

        return config
    except FileNotFoundError:
        print(f"please check{pathfile} agin, program cannot find the file!")
    except ValueError as e:
        print(f"the value error is:{e}")


if __name__ == '__main__':

    if len(sys.argv) > 1:
        file = os.path.join(os.path.dirname(__file__), sys.argv[1])
        parse_config(file)
        print(f"环境变量是：{os.environ.get('PATH')}")

    configs = parse_config(os.path.join(os.path.dirname(__file__), "09_config.txt"))
    print(configs)

    os.listdir()