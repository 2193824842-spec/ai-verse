#!/usr/bin/env python3
"""
发布新文章后追加到 _ops/data/published_index.json。
用法：
  python scripts/update_published_index.py \
    --slug "biggest-ai-acquisitions-2026" \
    --title "Biggest AI Acquisitions 2026: The $1.2T Land Grab" \
    --article-type "Industry Insights" \
    --tags "enterprise-ai,ai-research,generative-ai" \
    --summary "Q1 2026 saw $1.22T in AI-driven M&A..." \
    --date "2026-04-21"
"""

import json
import argparse
from pathlib import Path

INDEX_PATH = Path(__file__).parent.parent / "_ops" / "data" / "published_index.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug",         required=True)
    parser.add_argument("--title",        required=True)
    parser.add_argument("--article-type", required=True)
    parser.add_argument("--tags",         required=True, help="Comma-separated tags")
    parser.add_argument("--summary",      required=True)
    parser.add_argument("--date",         required=True)
    args = parser.parse_args()

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8")) if INDEX_PATH.exists() else []

    # 同 slug 已存在则替换
    index = [a for a in index if a.get("slug") != args.slug]

    index.insert(0, {
        "slug": args.slug,
        "title": args.title,
        "article_type": args.article_type,
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
        "summary": args.summary,
        "date": args.date,
    })

    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"INDEX_UPDATED: {args.slug} ({len(index)} total)")


if __name__ == "__main__":
    main()
