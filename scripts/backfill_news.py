#!/usr/bin/env python3
"""
Backfill news for past dates by fetching RSS with a wider time window.
Usage: python backfill_news.py [--days 5] [--from 2026-04-15] [--to 2026-04-19]
"""
import json, os, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET

# Import shared helpers from fetch_news
sys.path.insert(0, str(Path(__file__).parent))
from fetch_news import (
    FEEDS, AI_KEYWORDS, NS, STOPWORDS, TIER_LIMITS, TIER_BONUS,
    MAX_PER_DAY, TOP_TRANSLATE,
    is_ai_related, is_english, strip_html, parse_date,
    extract_rss_image, fetch_og_image, title_keywords, extract_json_array,
    cluster_items, claude_filter, score_items, translate_items, fetch_images_concurrent,
)

OUTPUT = Path(__file__).parent.parent / "public" / "data" / "news.json"


def fetch_feed_wide(feed: dict, cutoff_ts: float) -> list:
    """Fetch feed with wider time window, no per-feed limit on age."""
    name  = feed["name"]
    limit = TIER_LIMITS[feed["tier"]] * 3  # fetch more items to find older ones
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
        ts   = parse_date(pub).timestamp()
        if ts < cutoff_ts:
            continue
        items.append({
            "title": title, "url": link, "source": name, "tier": feed["tier"],
            "summary": desc[:200] + ("…" if len(desc) > 200 else ""),
            "date": parse_date(pub).strftime("%Y-%m-%d"),
            "_ts":  ts,
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
            ts   = parse_date(pub).timestamp()
            if ts < cutoff_ts:
                continue
            items.append({
                "title": title, "url": link, "source": name, "tier": feed["tier"],
                "summary": desc[:200] + ("…" if len(desc) > 200 else ""),
                "date": parse_date(pub).strftime("%Y-%m-%d"),
                "_ts":  ts,
                "image": extract_rss_image(el),
            })

    if items:
        print(f"  [OK] {name}: {len(items)} items")
    return items


def process_day(date_str: str, day_items: list, api_key: str, base_url: str) -> list:
    print(f"\n=== Processing {date_str} ({len(day_items)} raw items) ===")

    seen: set = set()
    unique = []
    for item in day_items:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)

    unique = cluster_items(unique)
    reps = [i for i in unique if not i.get("duplicate")]
    print(f"  → {len(reps)} unique events after clustering")

    if api_key:
        unique = claude_filter(unique, api_key, base_url)
        score_items(unique, api_key, base_url)
        translate_items(unique, api_key, base_url)
        top = sorted(
            [i for i in unique if not i.get("duplicate")],
            key=lambda x: x.get("score", 0), reverse=True
        )[:MAX_PER_DAY]
        fetch_images_concurrent(top)
    else:
        top = sorted(
            [i for i in unique if not i.get("duplicate")],
            key=lambda x: x.get("_ts", 0), reverse=True
        )[:MAX_PER_DAY]

    for item in top:
        item.pop("_ts", None)
        item["date"] = date_str

    print(f"  → {len(top)} items kept for {date_str}")
    return top


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="date_from", default=None, help="Start date YYYY-MM-DD")
    parser.add_argument("--to",   dest="date_to",   default=None, help="End date YYYY-MM-DD (inclusive)")
    parser.add_argument("--days", type=int, default=5, help="How many days back from today")
    args = parser.parse_args()

    today = datetime.now(timezone.utc).date()

    if args.date_from and args.date_to:
        d_from = datetime.strptime(args.date_from, "%Y-%m-%d").date()
        d_to   = datetime.strptime(args.date_to,   "%Y-%m-%d").date()
    else:
        d_to   = today - timedelta(days=1)
        d_from = today - timedelta(days=args.days)

    target_dates = []
    d = d_from
    while d <= d_to:
        target_dates.append(d.strftime("%Y-%m-%d"))
        d += timedelta(days=1)

    print(f"Backfilling: {target_dates}")

    cutoff_ts = datetime.combine(d_from, datetime.min.time()).replace(tzinfo=timezone.utc).timestamp()

    print("\nFetching RSS feeds...")
    all_items: list = []
    for feed in FEEDS:
        raw = fetch_feed_wide(feed, cutoff_ts)
        if feed.get("ai_only"):
            raw = [i for i in raw if is_ai_related(i["title"], i["summary"])]
        all_items.extend(raw)

    print(f"\nTotal fetched: {len(all_items)} items across all dates")

    # Group by date
    by_date: dict = {d: [] for d in target_dates}
    for item in all_items:
        if item["date"] in by_date:
            by_date[item["date"]].append(item)

    for d, items in by_date.items():
        print(f"  {d}: {len(items)} raw items")

    api_key  = os.environ.get("ANTHROPIC_API_KEY", "")
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://aiapi.tnt-pub.com").rstrip("/")

    if not api_key:
        print("\n[WARN] ANTHROPIC_API_KEY not set — skipping scoring and translation")

    # Process each day
    new_items_by_date: dict = {}
    for date_str in target_dates:
        day_items = by_date[date_str]
        if not day_items:
            print(f"\n=== {date_str}: no items found in RSS feeds ===")
            new_items_by_date[date_str] = []
        else:
            new_items_by_date[date_str] = process_day(date_str, day_items, api_key, base_url)

    # Load existing news.json
    existing = []
    if OUTPUT.exists():
        try:
            data = json.loads(OUTPUT.read_text(encoding="utf-8"))
            existing = data.get("items", [])
        except Exception:
            pass

    # Remove any existing items for target dates (replace them)
    kept = [i for i in existing if i.get("date") not in target_dates]

    # Build new items list: collect all new items
    new_items = []
    for date_str in sorted(target_dates, reverse=True):
        new_items.extend(new_items_by_date[date_str])

    # Merge: new items first (they include today's replacements), then kept history
    # Sort everything by date desc, then score desc
    all_merged = new_items + kept
    all_merged.sort(key=lambda x: (x.get("date", ""), x.get("score", 0)), reverse=True)

    OUTPUT.write_text(json.dumps({
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "items":   all_merged,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    total_new = sum(len(v) for v in new_items_by_date.values())
    print(f"\nDone: added {total_new} backfilled items + {len(kept)} existing = {len(all_merged)} total → {OUTPUT}")


if __name__ == "__main__":
    main()
