# 项目简介

这是一个 **Markdown 目录生成器**，可以自动扫描 `.md` 文件中的标题，生成带跳转链接的目录结构。

> 支持 Python 3.8+，无需安装任何第三方库。

---

## 功能特性

- ✅ 自动识别 `#` `##` `###` 标题
- ✅ 生成 GitHub 兼容的锚点链接
- ✅ 自动跳过代码块中的 `#` 符号
- ✅ 支持中文标题
- ✅ 按层级缩进，结构清晰

---

## 安装

### 环境要求

- Python 3.8 或更高版本
- 无需安装第三方依赖

### 获取代码

```bash
git clone https://github.com/example/md-toc-generator.git
cd md-toc-generator
```

---

## 使用方法

### 基础用法

```bash
python md_toc_simple.py README.md
```

### 保存到文件

```bash
python md_toc_simple.py README.md > toc.md
```

---

## 代码说明

### 目录结构

```
md-markdonw-toc/
├── md_toc_simple.py
├── README.md
└── test.md
```

### 核心函数

| 函数 | 功能 |
|------|------|
| `make_anchor(text)` | 标题转 GitHub 锚点 |
| `generate_toc(filename)` | 解析标题，生成目录 |

---

## 常见问题

### 中文标题能正常生成锚点吗？
### 代码块里的 `#` 会被误识别吗？
### 支持几级标题？

---

## 更新日志

### v1.1.0 / v1.0.0

---

## 贡献指南

### 提交规范 / 开发流程

---

## 许可证

MIT License
