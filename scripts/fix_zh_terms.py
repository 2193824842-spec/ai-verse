#!/usr/bin/env python3
"""
对中文 Markdown 文件做术语强制替换 + 格式后处理。
用法：python scripts/fix_zh_terms.py <file.md>
"""

import re
import sys
from pathlib import Path

# (pattern, replacement) — 按顺序执行，顺序有意义
REPLACEMENTS = [
    # AI agent 系列
    (r"Agentic\s*AI", "智能体 AI"),
    (r"Agentic\s*工作流", "智能体工作流"),
    (r"agentic\s*工作流", "智能体工作流"),
    (r"AI\s*[Aa]gent(?!ic)", "AI 智能体"),
    (r"AI代理", "AI 智能体"),
    (r"多代理系统", "多智能体系统"),
    (r"代理工作流", "智能体工作流"),
    # 翻译腔词汇
    (r"正越来越多地", "越来越"),
    (r"进行了([^，。！？\s]{1,6})", r"\1了"),
    (r"实现了([^，。！？\s]{1,6})", r"\1了"),
    (r"具有([^，。！？\s]{1,8}的能力)", r"能\1"),
    (r"提供了([^，。！？\s]{1,6})的能力", r"能\1"),
    # 数字格式（兜底）
    (r"\$(\d+(?:\.\d+)?)T\b", lambda m: f"{float(m.group(1)):.0f}万亿美元" if float(m.group(1)) >= 1 else f"{float(m.group(1))*10000:.0f}亿美元"),
]

# 不替换 SEO_METADATA 块内的内容
METADATA_PATTERN = re.compile(r"(---\nSEO_METADATA:.*)", re.DOTALL)

EM_DASH = "——"
EM_DASH_LIMIT = 3


def fix_em_dashes(body: str) -> tuple[str, list[str]]:
    """超过限制的破折号从第4个起替换为逗号。标题行（## 开头）一律不允许破折号。"""
    changes = []

    # 标题行破折号全部替换
    def replace_heading_dashes(m):
        original = m.group(0)
        replaced = original.replace(EM_DASH, "，")
        if replaced != original:
            changes.append(f"  [heading] 标题破折号 → 逗号")
        return replaced

    body = re.sub(r"^#{1,6} .*$", replace_heading_dashes, body, flags=re.MULTILINE)

    # 正文：超过限制的从第4个起替换
    count = body.count(EM_DASH)
    if count > EM_DASH_LIMIT:
        excess = count - EM_DASH_LIMIT
        # 找到第4个及之后的破折号位置，逐一替换
        replaced = 0
        result = []
        i = 0
        found = 0
        while i < len(body):
            if body[i:i+2] == EM_DASH:
                found += 1
                if found > EM_DASH_LIMIT:
                    result.append("，")
                    replaced += 1
                else:
                    result.append(EM_DASH)
                i += 2
            else:
                result.append(body[i])
                i += 1
        body = "".join(result)
        changes.append(f"  [{replaced}x] 破折号超限（共{count}个，限{EM_DASH_LIMIT}个）→ 逗号")

    return body, changes


def fix_half_width_quotes(body: str) -> tuple[str, list[str]]:
    """将正文中的半角英文引号替换为中文全角引号。
    仅替换包裹中文内容的引号，跳过代码块和链接 URL。
    """
    changes = []

    # 跳过代码块
    code_blocks = []
    def save_code(m):
        code_blocks.append(m.group(0))
        return f"\x00CODE{len(code_blocks)-1}\x00"
    body = re.sub(r"```[\s\S]*?```|`[^`]+`", save_code, body)

    # 跳过 Markdown 链接的 URL 部分 [text](url)
    urls = []
    def save_url(m):
        urls.append(m.group(0))
        return f"\x00URL{len(urls)-1}\x00"
    body = re.sub(r"\]\([^)]+\)", save_url, body)

    # 替换包裹中文字符的半角引号
    # 匹配：" 开头，内含至少一个中文字符，" 结尾
    def replace_quotes(m):
        inner = m.group(1)
        changes.append(f"  [quote] \"{inner}\" → \u201c{inner}\u201d")
        return f"\u201c{inner}\u201d"

    body = re.sub(r'"([^"]*[\u4e00-\u9fff][^"]*)"', replace_quotes, body)

    # 还原占位符
    for i, url in enumerate(urls):
        body = body.replace(f"\x00URL{i}\x00", url)
    for i, code in enumerate(code_blocks):
        body = body.replace(f"\x00CODE{i}\x00", code)

    return body, changes


def fix_internal_links(text: str) -> tuple[str, list[str]]:
    """将 /en/posts/ 内链替换为 /zh/posts/（全文包括 SEO_METADATA）。"""
    new_text, count = re.subn(r"\(/en/posts/", "(/zh/posts/", text)
    changes = []
    if count:
        changes.append(f"  [{count}x] /en/posts/ → /zh/posts/")
    return new_text, changes


def fix_terms(text: str) -> tuple[str, list[str]]:
    meta_match = METADATA_PATTERN.search(text)
    body = text[:meta_match.start()] if meta_match else text
    meta = text[meta_match.start():] if meta_match else ""

    all_changes = []

    # 术语替换（仅正文）
    for pattern, repl in REPLACEMENTS:
        new_body, count = re.subn(pattern, repl, body)
        if count:
            all_changes.append(f"  [{count}x] {pattern!r} → {repl!r}")
            body = new_body

    # 破折号后处理（仅正文）
    body, changes = fix_em_dashes(body)
    all_changes.extend(changes)

    # 半角引号（仅正文）
    body, changes = fix_half_width_quotes(body)
    all_changes.extend(changes)

    # 内链替换（全文）
    full_text = body + meta
    full_text, changes = fix_internal_links(full_text)
    all_changes.extend(changes)

    return full_text, all_changes


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_zh_terms.py <file.md>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    fixed, changes = fix_terms(text)

    if not changes:
        print("No changes needed.")
        return

    path.write_text(fixed, encoding="utf-8")
    print(f"Fixed {len(changes)} pattern(s) in {path.name}:")
    for c in changes:
        print(c)


if __name__ == "__main__":
    main()
