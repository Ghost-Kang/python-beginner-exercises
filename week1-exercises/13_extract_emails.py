"""
从文件中抽取所有的邮件
正则表达式练习

"""

__author__ = 'wangxuknag'
__date__ = '2026-03-06'

import re

def extract_emails(text:str)->list:
    pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)


def extract_emails_unique(text:str)->list:
        emails = extract_emails(text)
        seen= set()
        result = []
        for email in emails:
            lowercase = email.lower()
            if lowercase not in seen:
                seen.add(lowercase)
                result.append(email)
        return result


def extract_emails_with_positions(text:str)->list[dict]:
        pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
        result = []
        for r in re.finditer(pattern, text):
            result.append({
                "email":r.group(),
                "start":r.start(),
                "end":r.end(),
                "line": text[:r.start()].count("\n") + 1,
            })

        return result

def group_by_domain(email:list[str])->dict[str,list[str]]:

    domains: dict[str,list[str]] = {}
    for email in email:
        domain=email.split("@")[1].lower()
        domains.setdefault(domain,[]).append(email)
    return domains

def print_section(title: str, char: str = '─', width: int = 52):
    print(f"\n{'─' * width}")
    print(f"  {title}")
    print('─' * width)


def print_results(label: str, emails: list[str]):
    print(f"\n  📌 {label}（共 {len(emails)} 个）:")
    for i, email in enumerate(emails, 1):
        print(f"     {i:>2}. {email}")


def main():
    try:
        with open('13_email_sample.txt', 'r', encoding='utf-8') as f:
            sample_text = f.read()
    except FileNotFoundError:
        print("not find '13_email_sample.txt'")


    print(f"\n📄 原始文本预览：\n{'─' * 52}")
    print(sample_text)

    # ── 1. 提取所有邮箱（含重复） ─────────
    print_section("① 提取所有邮箱（含重复）")
    all_emails = extract_emails(sample_text)
    print_results("全部邮箱", all_emails)

    # ── 2. 去重提取 ───────────────────────
    print_section("② 去重后的邮箱")
    unique_emails = extract_emails_unique(sample_text)
    print_results("唯一邮箱", unique_emails)

    # ── 3. 显示位置信息 ───────────────────
    print_section("③ 邮箱位置信息（行号 & 字符位置）")
    positioned = extract_emails_with_positions(sample_text)
    print(f"\n  {'序号':<4} {'邮箱地址':<35} {'行号':>4}  {'位置范围'}")
    print(f"  {'─' * 4} {'─' * 35} {'─' * 4}  {'─' * 12}")
    for i, item in enumerate(positioned, 1):
        pos_range = f"{item['start']}~{item['end']}"
        print(f"  {i:<4} {item['email']:<35} 第{item['line']:>2}行  {pos_range}")

    # ── 4. 按域名分组 ─────────────────────
    print_section("④ 按域名分组")
    domain_groups = group_by_domain(unique_emails)
    for domain, emails in sorted(domain_groups.items()):
        print(f"\n  🌐 {domain}（{len(emails)} 个）:")
        for email in emails:
            print(f"       • {email}")


if __name__ == '__main__':
    main()