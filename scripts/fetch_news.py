#!/usr/bin/env python3
"""
每日 AI 资讯抓取脚本
从多个 RSS 源抓取最新 AI 资讯，输出到 src/data/news.json
"""
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import quote
import xml.etree.ElementTree as ET

OUTPUT        = Path(__file__).parent.parent / "src" / "data" / "news.json"
MAX_TOTAL     = 350
TOP_TRANSLATE = 25
TIER_LIMITS   = {1: 5, 2: 10, 3: 5, 4: 3}

FEEDS = [
    # Tier 1 — 官方实验室
    {"name": "OpenAI",          "url": "https://openai.com/news/rss.xml",                                     "tier": 1},
    {"name": "Anthropic",       "url": "https://www.anthropic.com/rss.xml",                                   "tier": 1},
    {"name": "Google DeepMind", "url": "https://deepmind.google/blog/rss.xml",                                "tier": 1},
    {"name": "Meta AI",         "url": "https://ai.meta.com/blog/feed/",                                      "tier": 1},
    {"name": "Microsoft AI",    "url": "https://blogs.microsoft.com/ai/feed/",                                "tier": 1},
    {"name": "Google Research", "url": "https://research.google/blog/rss/",                                   "tier": 1},
    # Tier 2 — 专注 AI 媒体
    {"name": "量子位",           "url": "https://www.qbitai.com/feed",                                         "tier": 2},
    {"name": "机器之心",         "url": "https://www.jiqizhixin.com/rss",                                      "tier": 2},
    {"name": "极客公园",         "url": "https://www.geekpark.net/rss",                                        "tier": 2},
    {"name": "新智元",           "url": "https://xinzhiyuan.com/feed",                                         "tier": 2},
    {"name": "Hugging Face",    "url": "https://huggingface.co/blog/feed.xml",                                "tier": 2},
    {"name": "TechCrunch AI",   "url": "https://techcrunch.com/category/artificial-intelligence/feed/",       "tier": 2},
    {"name": "The Verge AI",    "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",   "tier": 2},
    {"name": "VentureBeat AI",  "url": "https://venturebeat.com/category/ai/feed/",                           "tier": 2},
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed", "tier": 2},
    {"name": "Wired AI",        "url": "https://www.wired.com/feed/tag/artificial-intelligence/rss",          "tier": 2},
    # Tier 3 — 综合科技媒体
    {"name": "36Kr",   "url": "https://36kr.com/feed",            "tier": 3, "ai_only": True},
    {"name": "虎嗅",   "url": "https://www.huxiu.com/rss/0.xml",  "tier": 3, "ai_only": True},
    {"name": "钛媒体", "url": "https://www.tmtpost.com/rss.xml",  "tier": 3, "ai_only": True},
    {"name": "少数派", "url": "https://sspai.com/feed",           "tier": 3, "ai_only": True},
    {"name": "爱范儿", "url": "https://www.ifanr.com/feed",       "tier": 3, "ai_only": True},
    {"name": "IT之家", "url": "https://www.ithome.com/rss/",      "tier": 3, "ai_only": True},
    {"name": "雷锋网", "url": "https://www.leiphone.com/feed",    "tier": 3, "ai_only": True},
    {"name": "InfoQ",  "url": "https://www.infoq.cn/feed",        "tier": 3, "ai_only": True},
    # Tier 4 — 学术 / 云厂商
    {"name": "arXiv cs.AI", "url": "https://arxiv.org/rss/cs.AI",                        "tier": 4},
    {"name": "arXiv cs.LG", "url": "https://arxiv.org/rss/cs.LG",                        "tier": 4},
    {"name": "AWS ML Blog", "url": "https://aws.amazon.com/blogs/machine-learning/feed/", "tier": 4},
]

AI_KEYWORDS = [
    "AI", "人工智能", "大模型", "ChatGPT", "GPT", "Claude", "Gemini",
    "DeepSeek", "Kimi", "豆包", "通义", "文心", "讯飞", "智谱",
    "机器学习", "深度学习", "神经网络", "LLM", "Agent", "多模态",
    "Sora", "Midjourney", "Stable Diffusion", "DALL", "文生图",
    "自动驾驶", "具身智能", "生成式", "OpenAI", "Anthropic",
    "Google DeepMind", "Meta AI", "Mistral", "Cursor", "Copilot",
]

NS = {
    "atom":  "http://www.w3.org/2005/Atom",
    "dc":    "http://purl.org/dc/elements/1.1/",
    "media": "http://search.yahoo.com/mrss/",
}

STOPWORDS = {
    "的", "了", "在", "是", "和", "与", "将", "为", "对", "从", "到", "中",
    "a", "an", "the", "is", "in", "of", "to", "and", "for", "on", "with",
}


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def is_ai_related(title: str, summary: str) -> bool:
    text = (title + " " + summary).lower()
    return any(kw.lower() in text for kw in AI_KEYWORDS)


def is_english(text: str) -> bool:
    if not text:
        return False
    return sum(1 for c in text if ord(c) < 128) / len(text) > 0.8


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def parse_date(text: str) -> datetime:
    if not text:
        return datetime.now(timezone.utc)
    fmts = [
        "%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S GMT",
        "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d",
    ]
    for fmt in fmts:
        try:
            dt = datetime.strptime(text.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            continue
    return datetime.now(timezone.utc)


def extract_rss_image(el) -> str:
    for tag in ["media:content", "media:thumbnail"]:
        for m in el.findall(tag, NS):
            url = m.get("url", "")
            if url.startswith("http"):
                return url
    enc = el.find("enclosure")
    if enc is not None and enc.get("type", "").startswith("image/"):
        url = enc.get("url", "")
        if url.startswith("http"):
            return url
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', el.findtext("description") or "")
    if m and m.group(1).startswith("http"):
        return m.group(1)
    return ""


def fetch_og_image(url: str) -> str:
    try:
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml",
        })
        with urlopen(req, timeout=8) as resp:
            chunk = resp.read(32768).decode("utf-8", errors="ignore")
        for pat in [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\'>\s]+)',
            r'<meta[^>]+content=["\']([^"\'>\s]+)["\'][^>]+property=["\']og:image["\']',
            r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\'>\s]+)',
        ]:
            m = re.search(pat, chunk, re.I)
            if m and m.group(1).startswith("http"):
                return m.group(1).strip()
    except Exception:
        pass
    return ""


def title_keywords(title: str) -> set[str]:
    words = re.findall(r"[a-zA-Z0-9]+|[\u4e00-\u9fff]", title.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 1}


# ── RSS 抓取 ──────────────────────────────────────────────────────────────────

def fetch_feed(feed: dict) -> list[dict]:
    name  = feed["name"]
    limit = TIER_LIMITS[feed["tier"]]
    try:
        req = Request(feed["url"], headers={"User-Agent": "Mozilla/5.0 (compatible; news-bot/1.0)"})
        with urlopen(req, timeout=15) as resp:
            raw = resp.read()
        root = ET.fromstring(raw)
    except Exception as e:
        print(f"  [SKIP] {name}: {e}", file=sys.stderr)
        return []

    items = []

    for el in root.findall(".//item")[:limit]:
        title = (el.findtext("title") or "").strip()
        link  = (el.findtext("link")  or "").strip()
        if not title or not link:
            continue
        desc = strip_html(el.findtext("description") or "")
        pub  = el.findtext("pubDate") or el.findtext("dc:date", namespaces=NS) or ""
        items.append({
            "title": title, "url": link, "source": name, "tier": feed["tier"],
            "summary": desc[:200] + ("…" if len(desc) > 200 else ""),
            "date": parse_date(pub).strftime("%Y-%m-%d"),
            "_ts":  parse_date(pub).timestamp(),
            "image": extract_rss_image(el),
        })

    if not items:
        for el in root.findall("atom:entry", NS)[:limit]:
            title = (el.findtext("atom:title", namespaces=NS) or "").strip()
            link  = ""
            for le in el.findall("atom:link", NS):
                if le.get("rel", "alternate") == "alternate" and le.get("href"):
                    link = le.get("href"); break
            if not link:
                le = el.find("atom:link", NS)
                link = (le.get("href") if le is not None else "") or ""
            if not title or not link:
                continue
            se = el.find("atom:summary", NS) or el.find("atom:content", NS)
            desc = strip_html(se.text if se is not None else "")
            pub  = el.findtext("atom:published", namespaces=NS) or el.findtext("atom:updated", namespaces=NS) or ""
            items.append({
                "title": title, "url": link, "source": name, "tier": feed["tier"],
                "summary": desc[:200] + ("…" if len(desc) > 200 else ""),
                "date": parse_date(pub).strftime("%Y-%m-%d"),
                "_ts":  parse_date(pub).timestamp(),
                "image": extract_rss_image(el),
            })

    print(f"  [OK] {name}: {len(items)} items")
    return items


# ── 聚类去重 ──────────────────────────────────────────────────────────────────

def cluster_items(items: list[dict]) -> list[dict]:
    groups: list[list[dict]] = []
    for item in items:
        kws = title_keywords(item["title"])
        matched = None
        for group in groups:
            rep_kws = title_keywords(group[0]["title"])
            if not rep_kws or not kws:
                continue
            overlap = len(kws & rep_kws) / min(len(kws), len(rep_kws))
            if overlap >= 0.5:
                matched = group
                break
        if matched:
            matched.append(item)
        else:
            groups.append([item])

    result = []
    for group in groups:
        group.sort(key=lambda x: x["tier"])
        rep = group[0]
        rep["duplicate_count"] = len(group) - 1
        rep["duplicate"] = False
        result.append(rep)
        for dup in group[1:]:
            dup["duplicate"] = True
            dup["duplicate_count"] = 0
            result.append(dup)

    return result


# ── Claude 评分 + 翻译 + 抓图 ─────────────────────────────────────────────────

def score_and_translate(items: list[dict], api_key: str, base_url: str) -> None:
    try:
        from anthropic import Anthropic
    except ImportError:
        print("  [WARN] anthropic 未安装，跳过评分和翻译")
        return

    client = Anthropic(api_key=api_key, base_url=base_url)
    today  = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Step 1: 评分
    today_reps = [i for i in items if i.get("date", "")[:10] == today and not i.get("duplicate")]
    if today_reps:
        print(f"\n-> 评分今日代表条目 {len(today_reps)} 条...")
        lines = "\n".join(
            f'[{j+1}] tier{i["tier"]} | 来源:{i["source"]} | 重复报道:{i["duplicate_count"]}家 | {i["title"]}'
            for j, i in enumerate(today_reps)
        )
        prompt = f"""对以下 AI 资讯打重要性分（1-10），返回 JSON 数组。
每条格式：{{"index":1,"score":8}}

评分标准：
- 主流模型发布/重大更新：8-10
- 重要产品上线/大功能更新：6-8
- 融资/并购/监管大事件：5-7
- 学术突破：4-6
- 一般资讯/工具更新：1-4

加权规则：
- tier1 来源同等内容 +1 分
- 重复报道每多1家 +0.5 分（上限 +2）

{lines}"""
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip()
            m = re.search(r"\[.*\]", raw, re.DOTALL)
            for s in (json.loads(m.group()) if m else []):
                idx = s.get("index", 0) - 1
                if 0 <= idx < len(today_reps):
                    today_reps[idx]["score"] = round(s.get("score", 5), 1)
            print("  评分完成")
        except Exception as e:
            print(f"  [WARN] 评分失败: {e}")

    # Step 2: 翻译 Top 25
    to_translate = [i for i in items if not i.get("title_zh") and not i.get("duplicate")]
    to_translate.sort(key=lambda x: x.get("score", 0), reverse=True)
    to_translate = to_translate[:TOP_TRANSLATE]

    if to_translate:
        print(f"\n-> 翻译 Top {len(to_translate)} 条...")
        lines = "\n".join(
            f'[{j+1}] {"EN" if is_english(i["title"]) else "ZH"} | {i["title"]} | {i["summary"]}'
            for j, i in enumerate(to_translate)
        )
        prompt = f"""将以下资讯标题和摘要互译（EN→ZH 或 ZH→EN），返回 JSON 数组，顺序与输入一致。
每条格式：{{"title_zh":"...","summary_zh":"...","title_en":"...","summary_en":"..."}}
标题不超过30字，摘要不超过80字。

{lines}"""
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip()
            m = re.search(r"\[.*\]", raw, re.DOTALL)
            results = json.loads(m.group()) if m else []
        except Exception as e:
            print(f"  [WARN] 翻译失败: {e}")
            results = []

        for j, item in enumerate(to_translate):
            w = results[j] if j < len(results) else {}
            if is_english(item["title"]):
                item["title_en"]   = item["title"]
                item["summary_en"] = item["summary"]
                item["title_zh"]   = w.get("title_zh") or item["title"]
                item["summary_zh"] = w.get("summary_zh") or item["summary"]
            else:
                item["title_zh"]   = item["title"]
                item["summary_zh"] = item["summary"]
                item["title_en"]   = w.get("title_en") or item["title"]
                item["summary_en"] = w.get("summary_en") or item["summary"]
            item["title"]   = item["title_zh"]
            item["summary"] = item["summary_zh"]
        print("  翻译完成")

    # Step 3: 并发抓取 Top 25 的 og:image
    need_image = [i for i in to_translate if not i.get("image")]
    if need_image:
        print(f"\n-> 抓取封面图 {len(need_image)} 条（并发）...")
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(fetch_og_image, i["url"]): i for i in need_image}
            for future in as_completed(futures):
                img = future.result()
                if img:
                    futures[future]["image"] = img
        print("  封面图抓取完成")


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    all_items: list[dict] = []
    for feed in FEEDS:
        raw = fetch_feed(feed)
        if feed.get("ai_only"):
            before = len(raw)
            raw = [i for i in raw if is_ai_related(i["title"], i["summary"])]
            print(f"       → AI过滤后: {len(raw)}/{before}")
        all_items.extend(raw)

    seen: set[str] = set()
    unique = []
    for item in all_items:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)

    if OUTPUT.exists():
        try:
            old = json.loads(OUTPUT.read_text(encoding="utf-8"))
            for item in old.get("items", []):
                if item.get("url") and item["url"] not in seen:
                    seen.add(item["url"])
                    item["_ts"] = parse_date(item.get("date", "")).timestamp()
                    unique.append(item)
        except Exception:
            pass

    unique.sort(key=lambda x: x.get("_ts", 0), reverse=True)
    unique = unique[:MAX_TOTAL]

    print(f"\n-> 聚类去重（共 {len(unique)} 条）...")
    unique = cluster_items(unique)
    reps = sum(1 for i in unique if not i.get("duplicate"))
    print(f"  → {reps} 个独立事件，{len(unique) - reps} 条重复")

    api_key  = os.environ.get("ANTHROPIC_API_KEY", "")
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://aiapi.tnt-pub.com/")
    if api_key:
        score_and_translate(unique, api_key, base_url)
    else:
        print("\n  [WARN] 未设置 ANTHROPIC_API_KEY，跳过评分和翻译")

    for item in unique:
        item.pop("_ts", None)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "items":   unique,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDone: {len(unique)} items → {OUTPUT}")


if __name__ == "__main__":
    main()
