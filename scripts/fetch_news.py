#!/usr/bin/env python3
"""
每日 AI 资讯抓取脚本
从多个 RSS 源抓取最新 AI 资讯，输出到 src/data/news.json
英文条目自动翻译为中文（Google Translate 免费接口）
"""
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import quote
import xml.etree.ElementTree as ET

OUTPUT = Path(__file__).parent.parent / "src" / "data" / "news.json"
MAX_PER_FEED = 30
MAX_TOTAL = 500   # 累积上限

# 量子位/机器之心 是纯 AI 媒体，不过滤
# 少数派/36Kr/爱范儿 是综合科技媒体，需要关键词过滤
FEEDS = [
    # 国内 AI 媒体（纯 AI，不过滤）
    {"name": "量子位",   "url": "https://www.qbitai.com/feed",                              "ai_only": False},
    {"name": "机器之心", "url": "https://www.jiqizhixin.com/rss",                           "ai_only": False},
    {"name": "极客公园", "url": "https://www.geekpark.net/rss",                             "ai_only": False},
    {"name": "新智元",   "url": "https://xinzhiyuan.com/feed",                              "ai_only": False},
    # 国内综合科技媒体（需过滤 AI 相关）
    {"name": "少数派",   "url": "https://sspai.com/feed",                                   "ai_only": True},
    {"name": "36Kr",    "url": "https://36kr.com/feed",                                    "ai_only": True},
    {"name": "爱范儿",  "url": "https://www.ifanr.com/feed",                               "ai_only": True},
    {"name": "虎嗅",    "url": "https://www.huxiu.com/rss/0.xml",                          "ai_only": True},
    {"name": "钛媒体",  "url": "https://www.tmtpost.com/rss.xml",                          "ai_only": True},
    {"name": "IT之家",  "url": "https://www.ithome.com/rss/",                              "ai_only": True},
    # 国际 AI 媒体（英文，需过滤）
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "ai_only": False},
    {"name": "The Verge AI",  "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "ai_only": False},
    {"name": "VentureBeat AI","url": "https://venturebeat.com/category/ai/feed/",          "ai_only": False},
    {"name": "MIT Tech Review","url": "https://www.technologyreview.com/topic/artificial-intelligence/feed", "ai_only": False},
    # 官方博客（纯 AI，不过滤）
    {"name": "Hugging Face",  "url": "https://huggingface.co/blog/feed.xml",               "ai_only": False},
]

# AI 相关关键词（命中任意一个即保留）
AI_KEYWORDS = [
    "AI", "人工智能", "大模型", "ChatGPT", "GPT", "Claude", "Gemini",
    "DeepSeek", "Kimi", "豆包", "通义", "文心", "讯飞", "智谱",
    "机器学习", "深度学习", "神经网络", "LLM", "Agent", "多模态",
    "Sora", "Midjourney", "Stable Diffusion", "DALL", "文生图",
    "自动驾驶", "具身智能", "向量", "推理", "生成式", "OpenAI",
    "Anthropic", "Google DeepMind", "Meta AI", "Mistral",
    "Cursor", "Copilot", "代码助手", "AI助手", "AI工具",
]

def is_ai_related(title: str, summary: str) -> bool:
    text = (title + " " + summary).lower()
    return any(kw.lower() in text for kw in AI_KEYWORDS)


def is_english(text: str) -> bool:
    """判断文本是否主要为英文（ASCII 字符占比 > 80%）"""
    if not text:
        return False
    ascii_count = sum(1 for c in text if ord(c) < 128)
    return ascii_count / len(text) > 0.8


def translate(text: str, src: str, tgt: str) -> str:
    """用 Google Translate 免费接口翻译，失败返回原文"""
    if not text:
        return text
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={src}&tl={tgt}&dt=t&q={quote(text)}"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        translated = "".join(seg[0] for seg in data[0] if seg[0])
        return translated.strip() or text
    except Exception:
        return text

NS = {
    "atom":    "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc":      "http://purl.org/dc/elements/1.1/",
}


def fetch_og_image(url: str) -> str:
    """抓取文章页，提取 og:image 或 twitter:image URL"""
    try:
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml",
        })
        with urlopen(req, timeout=6) as resp:
            chunk = resp.read(16384).decode("utf-8", errors="ignore")
        # og:image（两种属性顺序）
        for pat in [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\'>\s]+)',
            r'<meta[^>]+content=["\']([^"\'>\s]+)["\'][^>]+property=["\']og:image["\']',
            r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\'>\s]+)',
            r'<meta[^>]+content=["\']([^"\'>\s]+)["\'][^>]+name=["\']twitter:image["\']',
        ]:
            m = re.search(pat, chunk, re.I)
            if m:
                img = m.group(1).strip()
                if img.startswith("http"):
                    return img
    except Exception:
        pass
    return ""


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_date(text: str) -> datetime:
    """Parse various RSS date formats → UTC datetime."""
    if not text:
        return datetime.now(timezone.utc)
    # RFC 822: "Mon, 13 Apr 2026 08:00:00 +0800"
    fmts = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S GMT",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d",
    ]
    text = text.strip()
    for fmt in fmts:
        try:
            dt = datetime.strptime(text, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            continue
    return datetime.now(timezone.utc)


def fetch_feed(name: str, url: str) -> list[dict]:
    """Fetch and parse one RSS/Atom feed. Returns list of item dicts."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; news-bot/1.0)"}
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=15) as resp:
            raw = resp.read()
    except Exception as e:
        print(f"  [SKIP] {name}: {e}", file=sys.stderr)
        return []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"  [SKIP] {name}: XML parse error: {e}", file=sys.stderr)
        return []

    items = []

    # --- RSS 2.0 ---
    for item in root.findall(".//item")[:MAX_PER_FEED]:
        title = (item.findtext("title") or "").strip()
        link  = (item.findtext("link")  or "").strip()
        desc  = strip_html(item.findtext("description") or "")
        pub   = item.findtext("pubDate") or item.findtext("dc:date", namespaces=NS) or ""
        if not title or not link:
            continue
        items.append({
            "title":   title,
            "url":     link,
            "source":  name,
            "summary": desc[:200] + ("…" if len(desc) > 200 else ""),
            "date":    parse_date(pub).strftime("%Y-%m-%d"),
            "_ts":     parse_date(pub).timestamp(),
        })

    # --- Atom ---
    if not items:
        for entry in root.findall("atom:entry", NS)[:MAX_PER_FEED]:
            title = (entry.findtext("atom:title", namespaces=NS) or "").strip()
            # Prefer rel="alternate" (the article page) over rel="self" or rel="replies"
            link = ""
            for link_el in entry.findall("atom:link", NS):
                rel = link_el.get("rel", "alternate")
                href = link_el.get("href", "")
                if rel == "alternate" and href:
                    link = href
                    break
            if not link:
                link_el = entry.find("atom:link", NS)
                link = (link_el.get("href") if link_el is not None else "") or ""
            summary_el = entry.find("atom:summary", NS) or entry.find("atom:content", NS)
            desc  = strip_html(summary_el.text if summary_el is not None else "")
            pub   = entry.findtext("atom:published", namespaces=NS) or \
                    entry.findtext("atom:updated", namespaces=NS) or ""
            if not title or not link:
                continue
            items.append({
                "title":   title,
                "url":     link,
                "source":  name,
                "summary": desc[:200] + ("…" if len(desc) > 200 else ""),
                "date":    parse_date(pub).strftime("%Y-%m-%d"),
                "_ts":     parse_date(pub).timestamp(),
            })

    print(f"  [OK] {name}: {len(items)} items")
    return items


def main():
    all_items: list[dict] = []
    for feed in FEEDS:
        raw = fetch_feed(feed["name"], feed["url"])
        if feed.get("ai_only"):
            before = len(raw)
            raw = [i for i in raw if is_ai_related(i["title"], i["summary"])]
            print(f"       → AI过滤后: {len(raw)}/{before} items")
        all_items.extend(raw)

    # Deduplicate by URL
    seen: set[str] = set()
    unique = []
    for item in all_items:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)

    # 合并历史数据（已存在的 news.json）
    if OUTPUT.exists():
        try:
            old_data = json.loads(OUTPUT.read_text(encoding="utf-8"))
            for item in old_data.get("items", []):
                if item.get("url") and item["url"] not in seen:
                    seen.add(item["url"])
                    # 用 date 字段重建 _ts 用于排序
                    item["_ts"] = parse_date(item.get("date", "")).timestamp()
                    unique.append(item)
        except Exception:
            pass

    # Sort newest first, cap at MAX_TOTAL
    unique.sort(key=lambda x: x.get("_ts", 0), reverse=True)
    unique = unique[:MAX_TOTAL]

    # 生成双语字段
    print("\n-> 生成双语标题/摘要...")
    for item in unique:
        title   = item["title"]
        summary = item["summary"]
        if is_english(title):
            # 英文来源：原文为 EN，翻译为 ZH
            item["title_en"]   = title
            item["summary_en"] = summary
            item["title_zh"]   = translate(title,   "en", "zh-CN")
            item["summary_zh"] = translate(summary,  "en", "zh-CN")
        else:
            # 中文来源：原文为 ZH，翻译为 EN
            item["title_zh"]   = title
            item["summary_zh"] = summary
            item["title_en"]   = translate(title,   "zh-CN", "en")
            item["summary_en"] = translate(summary,  "zh-CN", "en")
        # 保留 title/summary 作为向后兼容（中文）
        item["title"]   = item["title_zh"]
        item["summary"] = item["summary_zh"]
        time.sleep(0.3)

    # Remove internal sort key
    for item in unique:
        item.pop("_ts", None)

    # 抓取封面图（og:image）
    print("\n-> 抓取文章封面图...")
    for i, item in enumerate(unique):
        img = fetch_og_image(item["url"])
        item["image"] = img
        status = img[:70] if img else "无"
        print(f"  [{i+1}/{len(unique)}] {item['source']}: {status}")
        time.sleep(0.15)

    output = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "items":   unique,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDone: {len(unique)} items → {OUTPUT}")


if __name__ == "__main__":
    main()
