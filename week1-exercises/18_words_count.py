"""
统计文章top20的文字

"""

__author__ = 'wangxukang'
__date__ = '2026-03-16'

from collections import Counter
import re
import jieba

STOPWORDS_EN = {
    "the", "is", "a", "an", "of", "and", "to", "in", "on", "for", "with",
    "that", "this", "it", "as", "at", "by", "from", "be", "are", "was",
    "were", "or", "but", "not", "have", "has", "had", "you", "he", "she",
    "they", "we", "i", "his", "her", "their", "our", "your"
}

STOPWORDS_CN = {
    "的", "了", "和", "是", "在", "我", "有", "也", "就", "都", "而", "及",
    "与", "着", "或", "一个", "没有", "我们", "你", "你们", "他们", "它们",
    "这", "那", "啊", "吗", "呢", "吧"
}


def english_count(text, top_n = 20):
    text= text.lower()
    words = re.findall(r"[a-z]+", text)
    words =[ word for word in words if word not in STOPWORDS_EN]
    return Counter(words).most_common(top_n)

def chinese_count(text, top_n = 20):
    words = jieba.cut(text)
    words = [words.strip() for words in words if words.strip()]
    words = [w for w in words if w not in STOPWORDS_CN and len(w) > 1]
    return Counter(words).most_common(top_n)


def main():
    filepath = input("请输入文件的路径：").strip()
    lang = input("请输入需要查的语言（cn/en):").strip().lower()

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    if lang == "cn":
        result = chinese_count(text)
    elif lang == "en":
        result = english_count(text)
    else:
        print("请输入你的查询的(cn/en)")
        return


    print("\n输出top20语句查询结果")
    for word, count in result:
        print(f"{word}:{count}")



if __name__ == "__main__":
    main()