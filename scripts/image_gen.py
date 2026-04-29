#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
封面图生成脚本
用法: python scripts/image_gen.py --slug <slug> --title <title> --prompt <og_image_prompt>

生成封面图保存到 public/covers/<slug>.png
成功时 stdout 打印: COVER_GENERATED: /covers/<slug>.png
"""

import os
import sys
import json
import re
import base64
import argparse
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).parent.parent
COVERS_DIR = ROOT / "public" / "covers"
STYLE_USAGE_FILE = ROOT / "_ops" / "data" / "cover_style_usage.json"

_API_KEY   = "sk-Hzh1VsUKXeTj7PX3HKnUvcQrOvvQjh4nLZSfdF2nQuZD5Gsn"
_BASE_URL  = "https://aiapi.tnt-pub.com"
_LLM_MODEL = "claude-sonnet-4-6"
_IMG_MODEL = "gemini-3.1-flash-image-preview"


# article_type → preferred style (deterministic, LLM only writes the description)
STYLE_MAP = {
    "Industry Insights":    "financial_dashboard",
    "Industry Analysis":    "financial_dashboard",
    "Trending":             "editorial_magazine",
    "News":                 "news_bold",
    "Opinion":              "dark_minimal",
    "Research & Innovation":"tech_abstract",
    "Tool Guide":           "tech_abstract",
    "Product Comparison":   "corporate_infographic",
    "Model Comparison":     "corporate_infographic",
    "Tutorial":             "tech_abstract",
    "Product Review":       "cinematic_photo",
}
_DEFAULT_STYLE = "editorial_magazine"

STYLE_DESCRIPTIONS = {
    "financial_dashboard": (
        "Financial data dashboard aesthetic: glowing line charts, bar graphs, and market trend curves "
        "on a deep navy background with gold and cyan accent colors. "
        "Include key numbers and stats from the article (e.g. '$1.2T', '30%', company names) as bold glowing labels on the dashboard. "
        "No watermark."
    ),
    "editorial_magazine": (
        "Bold editorial magazine cover style: strong geometric color blocks in deep teal and warm amber, "
        "dramatic lighting on the central subject, high-contrast composition. "
        "Overlay the key stat or headline number from the article as a large typographic element. "
        "No watermark."
    ),
    "news_bold": (
        "Breaking news broadcast aesthetic: urgent cinematic lighting, sharp focus on the central subject, "
        "deep red and white accent tones on dark background, photojournalistic energy. "
        "Include the key figure or company name from the article as a bold on-screen graphic. "
        "No watermark."
    ),
    "corporate_infographic": (
        "Professional corporate infographic style: clean split-layout with side-by-side visual elements, "
        "cool blue and slate gray palette, structured and authoritative composition. "
        "Label each side with the product or model name being compared. "
        "No watermark."
    ),
    "tech_abstract": (
        "Futuristic tech abstract: flowing particle streams, neural network node graphs, "
        "electric blue and violet glow on near-black background, depth and motion. "
        "Embed the tool name or key concept as a glowing text element in the composition. "
        "No watermark."
    ),
    "dark_minimal": (
        "Ultra-minimal dark composition: single bold subject centered on near-black background, "
        "one strong accent color (gold or electric blue), stark negative space, contemplative mood. "
        "Include one key phrase or number from the article as a minimal typographic accent. "
        "No watermark."
    ),
    "cinematic_photo": (
        "Photorealistic cinematic scene: dramatic three-point lighting, shallow depth of field, "
        "rich color grading in cool teal and warm orange tones. "
        "Depict the product, tool, or scenario described in the article as a real-world scene. "
        "No watermark."
    ),
    "gradient_mesh": (
        "Fluid aurora gradient mesh: organic color blobs in deep purple, electric blue, and emerald green, "
        "soft luminous glow, abstract and forward-looking. "
        "Embed the core concept name as a subtle glowing typographic element. "
        "No watermark."
    ),
}


def _load_style_usage() -> dict:
    if STYLE_USAGE_FILE.exists():
        return json.loads(STYLE_USAGE_FILE.read_text(encoding="utf-8"))
    return {}


def _save_style_usage(usage: dict) -> None:
    STYLE_USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STYLE_USAGE_FILE.write_text(json.dumps(usage, ensure_ascii=False, indent=2), encoding="utf-8")


def _get_recently_used_styles(n: int = 4) -> list[str]:
    usage = _load_style_usage()
    sorted_styles = sorted(usage.items(), key=lambda x: x[1]["last_used"], reverse=True)
    return [s for s, _ in sorted_styles[:n]]


def _record_style_used(style: str) -> None:
    usage = _load_style_usage()
    usage[style] = {
        "last_used": str(__import__("datetime").date.today()),
        "count": usage.get(style, {}).get("count", 0) + 1,
    }
    _save_style_usage(usage)


def _llm_generate_prompt(title: str, og_prompt: str, article_type: str = "") -> str:
    style = STYLE_MAP.get(article_type, _DEFAULT_STYLE)
    style_desc = STYLE_DESCRIPTIONS.get(style, STYLE_DESCRIPTIONS["editorial_magazine"])

    user = f"""You are an expert at writing image generation prompts for blog cover images.

Article title: {title}
Article subject: {og_prompt}
Article type: {article_type}

Visual style to use: [{style}]
Style description: {style_desc}

TASK:
Write a single vivid image generation prompt that:
1. Uses the [{style}] visual style exactly as described
2. Directly visualizes the specific subject of THIS article (not a generic scene)
3. Embeds key numbers, stats, or names from the article as bold visual text elements (e.g. "$1.2T", "GPT-5", "30%")
4. Matches brand colors where applicable (Claude = violet, ChatGPT = teal-green, Gemini = blue-purple, OpenAI = black/white)

RULES:
- Include relevant numbers and key terms as part of the visual design
- No watermarks
- 2-3 sentences max, English only
- Start with [{style}] then the prompt

Reply with ONLY the image prompt, nothing else."""

    body = json.dumps({
        "model": _LLM_MODEL,
        "messages": [{"role": "user", "content": user}],
        "max_tokens": 200,
        "temperature": 0.9,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{_BASE_URL}/v1/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {_API_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read())
        prompt = resp["choices"][0]["message"]["content"].strip()
        m = re.match(r'\[(\w+)\]', prompt)
        if m:
            _record_style_used(m.group(1))
        return prompt
    except Exception as e:
        print(f"  [image_gen] LLM prompt failed, using fallback: {e}", file=sys.stderr)
        return f"Direct visualization of {title}, professional blog cover, cinematic lighting, no text, no watermark, 16:9"


def _gemini_generate_image(prompt: str) -> bytes | None:
    body = json.dumps({
        "model": _IMG_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{_BASE_URL}/v1/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {_API_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            resp = json.loads(r.read())
        content = resp["choices"][0]["message"]["content"]
        m = re.search(r'data:image/(?:jpeg|png|webp);base64,([A-Za-z0-9+/=]+)', content)
        if not m:
            print("  [image_gen] no base64 image data in response", file=sys.stderr)
            return None
        return base64.b64decode(m.group(1))
    except urllib.error.HTTPError as e:
        print(f"  [image_gen] HTTP {e.code}: {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [image_gen] generation failed: {e}", file=sys.stderr)
        return None


def generate_cover(slug: str, title: str, og_prompt: str, article_type: str = "") -> str | None:
    """生成封面图，返回 /covers/<slug>.png，失败返回 None。"""
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = COVERS_DIR / f"{slug}.png"

    if out_path.exists() and out_path.stat().st_size > 1024:
        print(f"  [image_gen] exists, skip: {out_path}", file=sys.stderr)
        return f"/covers/{slug}.png"

    style = STYLE_MAP.get(article_type, _DEFAULT_STYLE)
    print(f"  [image_gen] generating cover for: {slug} (type={article_type}, style={style})", file=sys.stderr)
    prompt = _llm_generate_prompt(title, og_prompt, article_type)
    print(f"  [image_gen] prompt: {prompt[:100]}...", file=sys.stderr)

    img_data = _gemini_generate_image(prompt)
    if not img_data:
        return None

    out_path.write_bytes(img_data)
    print(f"  [image_gen] saved: {out_path} ({len(img_data)//1024} KB)", file=sys.stderr)
    return f"/covers/{slug}.png"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug",         required=True)
    parser.add_argument("--title",        required=True)
    parser.add_argument("--prompt",       required=True, help="og_image_prompt from seo-optimizer")
    parser.add_argument("--article-type", default="", help="article_type from SEO_METADATA")
    args = parser.parse_args()

    result = generate_cover(args.slug, args.title, args.prompt, args.article_type)
    if result:
        print(f"COVER_GENERATED: {result}")
        sys.exit(0)
    else:
        print("COVER_FAILED", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
