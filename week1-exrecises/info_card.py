"""
根据格式，输出个人信息卡生成器

"""

info = input("请输入姓名 年龄 城市（用空格分开）：")

numbers = info.split()

# output way1
#print("name:%s | age:%s | from:%s" % (numbers[0], numbers[1], numbers[2]))
# output way2
#print('name:{0:s}|age:{1:s}|from:{2:s}'.format(numbers[0], numbers[1], numbers[2]))
# output way3
print(f'name:{numbers[0]:s}|age:{numbers[1]:s}|from:{numbers[2]:s}')
