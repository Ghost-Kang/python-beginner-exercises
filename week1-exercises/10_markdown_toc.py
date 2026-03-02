#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 目录生成器

"""
__author__ = "wangxukang"
__date__ = "2026-03-02"

import re

def make_anchor(text):
    text = re.sub(r'[`*_]', '', text)
    text = text.lower()
    text = re.sub(r'[^\w\u4e00-\u9fff-]', '', text)
    text = re.sub(r'-+', '-', text)
    return text

def generate_toc(filename):
    toc=[]
    is_code_block = False
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("```"):
                is_code_block = not is_code_block
                continue
            if is_code_block:
                continue

            m = re.match(r'^(#{1,3})\s+(.*)',line)
            if m:
                level = len(m.group(1))
                text = m.group(2).strip()
                anchor = make_anchor(text)
                indent = level * "    "
                toc.append(f"{indent}- [{text}](#{anchor})")
        return '\n'.join(toc)

if __name__ == "__main__":

    result = generate_toc("10_markdown_toc.md")
    print(result)


