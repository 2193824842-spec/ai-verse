#!/usr/bin/env python3
"""One-shot: backfill missing title_zh/title_en/summary_zh/summary_en in news.json"""
import json, os, re
from pathlib import Path

OUTPUT  = Path(__file__).parent.parent / "public" / "data" / "news.json"
API_KEY  = os.environ.get("ANTHROPIC_API_KEY", "sk-Hzh1VsUKXeTj7PX3HKnUvcQrOvvQjh4nLZSfdF2nQuZD5Gsn")
BASE_URL = "https://aiapi.tnt-pub.com"

def is_english(text):
    if not text: return False
    return sum(1 for c in text if ord(c) < 128) / len(text) > 0.8

def extract_json_array(text):
    for pat in [r"```(?:json)?\s*(\[.*?\])\s*```", r"(\[.*\])"]:
        m = re.search(pat, text, re.DOTALL)
        if not m: continue
        raw = m.group(1)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # strip control chars and retry
            raw2 = re.sub(r'[\x00-\x1f]', ' ', raw)
            try:
                return json.loads(raw2)
            except Exception:
                pass
    return []

def translate_one(item, client):
    title = item["title"]
    summary = item.get("summary", "")[:150]
    direction = "ZH→EN" if not is_english(title) else "EN→ZH"
    prompt = f"""Translate this news item ({direction}). Return ONLY a JSON object, no markdown.
Format: {{"title_translated":"...","summary_translated":"..."}}
Title limit: 60 chars. Summary limit: 120 chars.

Title: {title}
Summary: {summary}"""
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text.strip()
    m = re.search(r'\{[^{}]+\}', text, re.DOTALL)
    if m:
        return json.loads(m.group())
    return {}

def main():
    from anthropic import Anthropic
    client = Anthropic(api_key=API_KEY, base_url=BASE_URL)

    data = json.loads(OUTPUT.read_text(encoding="utf-8"))
    items = data["items"]

    def needs_translation(i):
        title = i.get("title", "")
        if is_english(title):
            # EN source: needs zh translation
            return not i.get("title_zh") or i.get("title_zh") == title
        else:
            # ZH source: needs en translation
            return not i.get("title_en") or i.get("title_en") == title

    need = [i for i in items if needs_translation(i)]
    print(f"Missing translations: {len(need)}/{len(items)}")
    if not need:
        print("Nothing to fix.")
        return

    for idx, item in enumerate(need):
        try:
            w = translate_one(item, client)
            if is_english(item["title"]):
                item["title_en"]   = item["title"]
                item["summary_en"] = item.get("summary", "")
                item["title_zh"]   = w.get("title_translated") or item["title"]
                item["summary_zh"] = w.get("summary_translated") or item.get("summary", "")
            else:
                item["title_zh"]   = item["title"]
                item["summary_zh"] = item.get("summary", "")
                item["title_en"]   = w.get("title_translated") or item["title"]
                item["summary_en"] = w.get("summary_translated") or item.get("summary", "")
            print(f"[{idx+1}/{len(need)}] OK")
        except Exception as e:
            print(f"[{idx+1}/{len(need)}] FAIL: {e}")

    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved → {OUTPUT}")

if __name__ == "__main__":
    main()
