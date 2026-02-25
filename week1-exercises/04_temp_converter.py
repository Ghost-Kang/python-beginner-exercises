""""
摄氏度celsius to 华氏度fahrenheit f 之间相互转化

转换	公式
°C → °F	C × 9/5 + 32
°F → °C	(F - 32) × 5/9
"""

__author__ = 'wangxukang'
__data__ = '2026-02-25'

def c_to_fah(c):
    return c*9/5 + 32

def f_to_cel(f):
    return (f-32)*5/9

def main_menu():
    print("\n"+"="*50)
    print("celsius to fahrenheit converter".center(50))
    print("="*50)

    while True:
        print("\n请选择你要进行的操作0-4:")
        print("1.摄氏度转华氏度")
        print("2.华氏度转设制度")
        print("3.摄氏度转华氏度 批量")
        print("4.华氏度转摄氏度 批量")
        print("0.退出系统")

        choice = int(input("请输入你选择的操作0-4:").strip())
        if choice == 1:
            c = float(input("请输入摄氏度（°C):"))
            print(f"{c}°C={c_to_fah(c):.2f}°F ")
        elif choice == 2:
            f = float(input("请输入摄氏度°F:"))
            print(f"{f}°F={f_to_cel(f):.2f}°C")
        elif choice == 3:
            nums = input("批量摄氏度转华氏度(用逗号隔开）：").split(',')
            for num in nums:
                c= float(num.strip())
                print(f"{c}°C={c_to_fah(c):.2f}°F")
        elif choice == 4:
            nums = input("批量华氏度转摄氏度（用逗号隔开）").split(',')
            for num in nums:
                f= float(num.strip())
                print(f"{f}°F={f_to_cel(f):.2f}°C")
        elif choice == 0:
            print("退出转化系统")
            break
        else:
            print("请选择正确操作序号0-4")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        pass
    else:
        main_menu()