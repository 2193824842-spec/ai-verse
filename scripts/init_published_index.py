#!/usr/bin/env python3
"""
从 src/content/posts-en/ 读取所有文章 frontmatter，
生成 _ops/data/published_index.json 初始索引。
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
POSTS_DIR = ROOT / "src" / "content" / "posts-en"
INDEX_PATH = ROOT / "_ops" / "data" / "published_index.json"


def parse_frontmatter(text: str) -> dict:
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    result = {}

    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"')
        result[key] = val

    # 解析 tags 数组
    tags_m = re.search(r'^tags:\s*\[(.+?)\]', block, re.MULTILINE)
    if tags_m:
        result["tags"] = [t.strip().strip('"').strip("'") for t in tags_m.group(1).split(",")]

    return result


def extract_slug(filename: str, frontmatter: dict) -> str:
    # 优先用 frontmatter 里的 slug，否则从文件名提取
    if frontmatter.get("slug"):
        return frontmatter["slug"]
    name = Path(filename).stem
    # 去掉日期前缀 YYYY-MM-DD-
    return re.sub(r'^\d{4}-\d{2}-\d{2}-', '', name)


def main():
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    for md_file in sorted(POSTS_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        if not fm.get("title"):
            print(f"  skip (no title): {md_file.name}")
            continue

        slug = extract_slug(md_file.name, fm)
        entry = {
            "slug": slug,
            "title": fm.get("title", ""),
            "article_type": fm.get("article_type") or fm.get("category", ""),
            "tags": fm.get("tags", []),
            "summary": fm.get("summary") or fm.get("excerpt", ""),
            "date": fm.get("date", ""),
        }
        entries.append(entry)
        print(f"  + {slug} | {entry['title'][:50]}")

    INDEX_PATH.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\nDone: {len(entries)} articles → {INDEX_PATH}")


if __name__ == "__main__":
    main()
