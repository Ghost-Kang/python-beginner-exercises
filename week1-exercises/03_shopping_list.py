"""
使用list实现 添加购物清单，删除购物清单，计算总价
 item = {name: name,
        price: float(price),
        quantity: int(quantity)
        )
每一个商品包含这些内容，通过 list.append 添加到购物列表，通过list.revemove or pop 删除，计算商品的总价格
"""

__author__ = 'wangxukang'
__date__ = '2026-02-25'


items = []

def add_item(name, price, quantity):
    item = {
        'name': name,
        'price': float(price),
        'quantity': int(quantity)
    }
    items.append(item)
    print(f"添加商品:{name}*数量:{quantity}-单价：{price:.2f}")

def remove_item(name):
    if len(items) == 0:
        print("没有添加任何产品")
        return
    for item in items:
        if item['name'] == name:
            items.remove(item)
            print(f"删除产品:{name}")
            return

def total_price():
    total = 0
    if not items:
        print("列表是空，请添加商品")
        return

    for i, item in enumerate(items,start=1):
        total += item['price'] * item['quantity']

    print(f"添加产品的总价格是:{total:.2f}")

def main_menu():
    print("\n欢迎使用购物清单系统")
    while True:
        print("\n请选择下面的操作")
        print("1.添加产品")
        print("2.删除产品")
        print("3.显示总价")
        print("0.退出")

        selection = input("\n请选择你需要的操作0-3：").strip()

        if selection == '1':
            name = input("请输入产品的名字").strip()
            try:
                price = float(input("价格是：").strip())
                quantity = int(input("数量是：").strip() or 1)
                add_item(name, price, quantity)
            except ValueError:
                print("请输入正确的价格及数量")

        elif selection == '2':
            name = input("输入要删除产品的名字").strip()
            remove_item(name)
        elif selection == '3':
            total_price()
        elif selection == '0':
            print("感谢使用系统！")
            break
        else:
            print("请选择正确的操作，0-3")

if __name__ == '__main__':
    import sys
    if len(sys.argv) >1 and sys.argv[1] == 'demo':
        pass
    else:
        main_menu()

