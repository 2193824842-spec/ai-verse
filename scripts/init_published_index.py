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
BASE_URL = "https://2193824842-spec.github.io/ai-verse"


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


def extract_slug(filename: str, fm: dict) -> str:
    # 优先从 cover 字段提取（最准确，无截断）
    cover = fm.get("cover", "")
    m = re.search(r'/covers/(.+?)\.(?:png|jpg|webp)$', cover)
    if m:
        return m.group(1)
    # 其次用 frontmatter slug 字段
    if fm.get("slug"):
        return fm["slug"]
    # 最后从文件名去掉日期前缀
    return re.sub(r'^\d{4}-\d{2}-\d{2}-', '', Path(filename).stem)


def extract_keywords(text: str, fm: dict) -> tuple[str, list[str]]:
    """从正文提取 primary_keyword 和 secondary_keywords（frontmatter 无此字段时降级推断）"""
    primary = fm.get("primary_keyword", "")
    secondary = []
    sec_raw = fm.get("secondary_keywords", "")
    if sec_raw:
        secondary = [k.strip().strip('"') for k in sec_raw.strip("[]").split(",") if k.strip()]

    # 降级：用 tags 前两个作为 secondary
    if not secondary:
        secondary = fm.get("tags", [])[:3]

    return primary, secondary


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
        primary_keyword, secondary_keywords = extract_keywords(text, fm)

        entry = {
            "slug": slug,
            "title": fm.get("title", ""),
            "article_type": fm.get("article_type") or fm.get("category", ""),
            "tags": fm.get("tags", []),
            "primary_keyword": primary_keyword,
            "secondary_keywords": secondary_keywords,
            "summary": fm.get("summary") or fm.get("excerpt", ""),
            "url": f"{BASE_URL}/en/articles/{slug}",
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
