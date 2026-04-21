#!/usr/bin/env python3
"""
每日 AI 资讯抓取脚本 v2
抓取过去24h → 聚类去重（保留权威来源）→ Claude评分 → Top30 → 合并7天历史
"""
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET

OUTPUT        = Path(__file__).parent.parent / "public" / "data" / "news.json"
MAX_PER_DAY   = 20
MIN_SCORE     = 4.0
TOP_TRANSLATE = 25
HISTORY_DAYS  = 7
TIER_LIMITS   = {1: 10, 2: 10, 3: 8, 4: 5}
TIER_BONUS    = {1: 1.5, 2: 1.0, 3: 0.5, 4: 0.0}

FEEDS = [
    {"name": "OpenAI",          "url": "https://openai.com/news/rss.xml",                                     "tier": 1},
    {"name": "Anthropic",       "url": "https://www.anthropic.com/rss.xml",                                   "tier": 1},
    {"name": "Google DeepMind", "url": "https://deepmind.google/blog/rss.xml",                                "tier": 1},
    {"name": "Meta AI",         "url": "https://ai.meta.com/blog/feed/",                                      "tier": 1},
    {"name": "Microsoft AI",    "url": "https://blogs.microsoft.com/ai/feed/",                                "tier": 1},
    {"name": "Google Research", "url": "https://research.google/blog/rss/",                                   "tier": 1},
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
    {"name": "36Kr",   "url": "https://36kr.com/feed",            "tier": 3, "ai_only": True},
    {"name": "虎嗅",   "url": "https://www.huxiu.com/rss/0.xml",  "tier": 3, "ai_only": True},
    {"name": "钛媒体", "url": "https://www.tmtpost.com/rss.xml",  "tier": 3, "ai_only": True},
    {"name": "少数派", "url": "https://sspai.com/feed",           "tier": 3, "ai_only": True},
    {"name": "爱范儿", "url": "https://www.ifanr.com/feed",       "tier": 3, "ai_only": True},
    {"name": "IT之家", "url": "https://www.ithome.com/rss/",      "tier": 3, "ai_only": True},
    {"name": "雷锋网", "url": "https://www.leiphone.com/feed",    "tier": 3, "ai_only": True},
    {"name": "InfoQ",  "url": "https://www.infoq.cn/feed",        "tier": 3, "ai_only": True},
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


def title_keywords(title: str) -> set:
    words = re.findall(r"[a-zA-Z0-9]+|[\u4e00-\u9fff]", title.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 1}


def extract_json_array(text: str):
    m = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    m = re.search(r"\[.*\]", text, re.DOTALL)
    if m:
        return json.loads(m.group())
    return []


# ── RSS 抓取 ──────────────────────────────────────────────────────────────────

def fetch_feed(feed: dict) -> list:
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


# ── 聚类去重（保留最权威来源）────────────────────────────────────────────────────

def cluster_items(items: list) -> list:
    groups = []
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
        group.sort(key=lambda x: x.get("tier", 99))  # tier1 最权威
        rep = group[0]
        rep["duplicate_count"] = len(group) - 1
        rep["duplicate"] = False
        result.append(rep)
        for dup in group[1:]:
            dup["duplicate"] = True
            dup["duplicate_count"] = 0
            result.append(dup)

    return result


# ── Claude 过滤 + 评分 + 翻译 ─────────────────────────────────────────────────

def claude_filter(items: list, api_key: str, base_url: str) -> list:
    try:
        from anthropic import Anthropic
    except ImportError:
        return items

    client = Anthropic(api_key=api_key, base_url=base_url)
    candidates = [i for i in items if not i.get("duplicate")]
    if not candidates:
        return items

    print(f"\n-> Claude 过滤 {len(candidates)} 条...")
    lines = "\n".join(f'[{j+1}] {i["title"]}' for j, i in enumerate(candidates))
    prompt = f"""以下是从科技媒体抓取的文章标题，判断每条是否与 AI/人工智能直接相关。
只保留主题是 AI 的文章，排除消费电子、耳机、手机、汽车、游戏、娱乐、纯商业财经等与 AI 无关的内容。
返回 JSON 数组，只包含需要保留的序号：[1, 3, 5]

{lines}"""
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        keep_indices = set(extract_json_array(resp.content[0].text.strip()))
        print(f"  → 保留 {len(keep_indices)}/{len(candidates)} 条")
    except Exception as e:
        print(f"  [WARN] 过滤失败: {e}")
        return items

    for j, item in enumerate(candidates):
        if (j + 1) not in keep_indices:
            item["duplicate"] = True

    return items


def score_items(items: list, api_key: str, base_url: str) -> None:
    try:
        from anthropic import Anthropic
    except ImportError:
        return

    client = Anthropic(api_key=api_key, base_url=base_url)
    reps = [i for i in items if not i.get("duplicate")]
    if not reps:
        return

    print(f"\n-> 评分 {len(reps)} 条...")
    lines = "\n".join(
        f'[{j+1}] tier{i["tier"]} | {i["source"]} | 重复:{i["duplicate_count"]}家 | {i["title"]}'
        for j, i in enumerate(reps)
    )
    prompt = f"""对以下 AI 资讯打重要性分（1-10），返回 JSON 数组。
每条格式：{{"index":1,"score":8,"tag":"model"}}
tag 从 model/product/research/industry 选一个。

评分标准：
- 新模型/算法发布（GPT/Claude/Gemini/Llama等）：+4
- 重要产品上线或重大功能更新：+3
- 顶会/顶刊学术突破：+3
- 行业大事件（监管、大额融资、并购）：+2
- 知名机构官方发布：+1

排除规则（直接给1分）：
- 纯营销软文、产品推广
- 与AI无直接关联的科技新闻
- arXiv纯理论/综述论文

{lines}"""
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        results = extract_json_array(resp.content[0].text.strip())
        for s in results:
            idx = s.get("index", 0) - 1
            if 0 <= idx < len(reps):
                base = float(s.get("score", 5))
                tier = reps[idx].get("tier", 4)
                dup  = reps[idx].get("duplicate_count", 0)
                reps[idx]["score"] = round(base + TIER_BONUS.get(tier, 0) + min(dup * 0.5, 2), 1)
                reps[idx]["tag"]   = s.get("tag", "industry")
        print("  评分完成")
    except Exception as e:
        print(f"  [WARN] 评分失败: {e}")


def translate_items(items: list, api_key: str, base_url: str) -> None:
    try:
        from anthropic import Anthropic
    except ImportError:
        return

    client = Anthropic(api_key=api_key, base_url=base_url)
    to_translate = [i for i in items if not i.get("title_zh") and not i.get("duplicate")]
    to_translate.sort(key=lambda x: x.get("score", 0), reverse=True)
    to_translate = to_translate[:TOP_TRANSLATE]

    if not to_translate:
        return

    print(f"\n-> 翻译 {len(to_translate)} 条...")
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
        results = extract_json_array(resp.content[0].text.strip())
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


def fetch_images_concurrent(items: list) -> None:
    need = [i for i in items if not i.get("image")]
    if not need:
        return
    print(f"\n-> 抓取封面图 {len(need)} 条...")
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch_og_image, i["url"]): i for i in need}
        for future in as_completed(futures):
            img = future.result()
            if img:
                futures[future]["image"] = img
    print("  封面图完成")


# ── 历史合并 ──────────────────────────────────────────────────────────────────

def merge_and_save(today_items: list, today_str: str) -> None:
    existing = []
    if OUTPUT.exists():
        try:
            data = json.loads(OUTPUT.read_text(encoding="utf-8"))
            existing = data.get("items", [])
        except Exception:
            pass

    cutoff = (datetime.now(timezone.utc).timestamp() - HISTORY_DAYS * 86400)
    cutoff_str = datetime.fromtimestamp(cutoff, tz=timezone.utc).strftime("%Y-%m-%d")

    # Remove today's entries and entries older than HISTORY_DAYS
    kept_history = [
        i for i in existing
        if i.get("date", "") != today_str and i.get("date", "") >= cutoff_str
    ]

    all_items = today_items + kept_history

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "items":   all_items,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDone: {len(today_items)} today + {len(kept_history)} history = {len(all_items)} total → {OUTPUT}")


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    cutoff_ts = datetime.now(timezone.utc).timestamp() - 86400
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    all_items: list = []
    for feed in FEEDS:
        raw = fetch_feed(feed)
        raw = [i for i in raw if i.get("_ts", 0) >= cutoff_ts]
        if feed.get("ai_only"):
            before = len(raw)
            raw = [i for i in raw if is_ai_related(i["title"], i["summary"])]
            print(f"       → AI过滤后: {len(raw)}/{before}")
        all_items.extend(raw)

    seen: set = set()
    unique = []
    for item in all_items:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)

    print(f"\n-> 聚类去重（共 {len(unique)} 条）...")
    unique = cluster_items(unique)
    reps = [i for i in unique if not i.get("duplicate")]
    print(f"  → {len(reps)} 个独立事件，{len(unique) - len(reps)} 条重复")

    api_key  = os.environ.get("ANTHROPIC_API_KEY", "")
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://aiapi.tnt-pub.com/")

    if api_key:
        unique = claude_filter(unique, api_key, base_url)
        score_items(unique, api_key, base_url)
        translate_items(unique, api_key, base_url)
        top_reps = sorted(
            [i for i in unique if not i.get("duplicate") and i.get("score", 0) >= MIN_SCORE],
            key=lambda x: x.get("score", 0), reverse=True
        )[:MAX_PER_DAY]
        fetch_images_concurrent(top_reps)
    else:
        print("\n  [WARN] 未设置 ANTHROPIC_API_KEY，跳过评分和翻译")
        top_reps = sorted(
            [i for i in unique if not i.get("duplicate")],
            key=lambda x: x.get("_ts", 0), reverse=True
        )[:MAX_PER_DAY]

    for item in top_reps:
        item.pop("_ts", None)
        item["date"] = today_str

    merge_and_save(top_reps, today_str)


if __name__ == "__main__":
    main()
