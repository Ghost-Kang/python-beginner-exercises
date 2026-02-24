"""
根据输入的身高 体重 计算 BMI

1️⃣ BMI 计算
根据公式：BMI = 体重(kg) / 身高²(m)
自动保留2位小数
2️⃣ 健康状态分类（国际标准）
BMI 范围	健康状态
< 18.5	体重过轻
18.5 - 23.9	正常体重 ✅
24 - 27.9	超重
28 - 29.9	肥胖（轻度）
≥ 30	肥胖（重度）

"""

__author__ = 'wangxukang'
__date__ = '2026-02-24'

weight = float(input("请输入体重(kg)："))
height = float(input("请输入身高(m)："))

BMI = weight / (height * height)

if BMI < 18.5:
    print("你的BMI指数是: %.2f, 标准：体重过轻" % BMI)
elif 18.5 <= BMI < 23.9:
    print("你的BMI指数是: {0:.2f},标准：正常体重".format(BMI))
elif 23.9 <= BMI < 27.9:
    print(f"你的BMI指数是: {BMI:.2f},标准：超重")
elif 27.9 <= BMI < 29.9:
    print("你的BMI指数是: {0:.2f},标准：肥胖（轻度）".format(BMI))
elif BMI >= 30:
    print(f"你的BMI指数是: {BMI:.2f},标准：肥胖（严重）")
