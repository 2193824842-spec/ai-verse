import re, os

SRC = 'D:/seo-farm/site/zh/posts'
DST = 'D:/ai-verse/src/content/posts-zh'

FILES = [
    ('openai-122b-agentic-workflows-gpt54.html',              '2026-03-31-openai-122b-agentic-workflows-.md'),
    ('generative-ai-chip-design-ml-semiconductor.html',       '2026-04-03-generative-ai-chip-design-ml-s.md'),
    ('ai-startup-funding-trends-2026.html',                   '2026-04-07-ai-startup-funding-trends-2026.md'),
    ('how-to-evaluate-ai-companies-framework.html',           '2026-04-08-how-to-evaluate-ai-companies-f.md'),
    ('ai-company-revenue-comparison-2026.html',               '2026-04-09-ai-company-revenue.md'),
    ('ai-2027-scenario-realistic-infrastructure-impact.html', '2026-04-10-ai-2027-scenario-realistic-inf.md'),
    ('ai-agent-market-consolidation-2026-frameworks.html',    '2026-04-10-ai-agent-market-consolidation-.md'),
    ('ai-regulations-compliance-trends-2026.html',            '2026-04-10-ai-regulations-compliance.md'),
    ('ai-unicorn-bubble-reality-check-2026-startup-failure.html', '2026-04-10-ai-unicorn-bubble-reality-chec.md'),
    ('ai-venture-capital-trends-2026.html',                   '2026-04-10-ai-venture-capital-trends-2026.md'),
]

def get_meta(html, prop):
    m = re.search(r'<meta\s+(?:property|name)=["\']' + re.escape(prop) + r'["\'][^>]*content=["\']([^"\']+)["\']', html)
    if m: return m.group(1).strip()
    m = re.search(r'<meta\s+content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\']' + re.escape(prop) + r'["\']', html)
    return m.group(1).strip() if m else ''

def get_difficulty(html):
    m = re.search(r'<span class="post-level">([^<]+)</span>', html)
    return m.group(1).strip() if m else 'Intermediate'

def extract_body(html):
    m = re.search(r'<div class="article-body">(.*?)</div>\s*</article>', html, re.DOTALL)
    if m: return m.group(1).strip()
    m = re.search(r'<div class="article-body">(.*?)(?=<footer|<script\s+src)', html, re.DOTALL)
    return m.group(1).strip() if m else ''

def html_to_md(html):
    # h2 with id preserved, others converted
    html = re.sub(r'<h2([^>]*)>(.*?)</h2>',
        lambda m: f'<h2{m.group(1)}>{m.group(2)}</h2>' if 'id=' in m.group(1)
                  else f'## {re.sub(r"<[^>]+>","",m.group(2)).strip()}',
        html, flags=re.DOTALL)
    html = re.sub(r'<h3[^>]*>(.*?)</h3>',
        lambda m: f'### {re.sub(r"<[^>]+>","",m.group(1)).strip()}',
        html, flags=re.DOTALL)
    # bold/italic
    html = re.sub(r'<strong>(.*?)</strong>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<b>(.*?)</b>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<em>(.*?)</em>', r'*\1*', html, flags=re.DOTALL)
    # links
    html = re.sub(r'<a\s+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', html, flags=re.DOTALL)
    # tables
    def convert_table(m):
        table_html = m.group(0)
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.DOTALL)
        md_rows = []
        for i, row in enumerate(rows):
            cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, re.DOTALL)
            cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
            if not any(cells): continue
            md_rows.append('| ' + ' | '.join(cells) + ' |')
            if i == 0:
                md_rows.append('| ' + ' | '.join(['---'] * len(cells)) + ' |')
        return '\n'.join(md_rows)
    html = re.sub(r'<(?:div[^>]*)>\s*<table.*?</table>\s*(?:</div>)?', convert_table, html, flags=re.DOTALL)
    html = re.sub(r'<table.*?</table>', convert_table, html, flags=re.DOTALL)
    # paragraphs
    html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n', html, flags=re.DOTALL)
    # lists
    html = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', html, flags=re.DOTALL)
    html = re.sub(r'<[uo]l[^>]*>', '', html)
    html = re.sub(r'</[uo]l>', '', html)
    # blockquote
    html = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1', html, flags=re.DOTALL)
    # remove remaining non-structural tags (keep div, h2, h3)
    html = re.sub(r'<(?!/?(?:div|h2|h3))[^>]+>', '', html)
    # clean whitespace
    html = re.sub(r'\n{3,}', '\n\n', html)
    html = re.sub(r'[ \t]+\n', '\n', html)
    return html.strip()

def get_cover_slug(src_file):
    slug = src_file.replace('.html', '')
    return f'/covers/{slug}.jpg'

for src_file, dst_file in FILES:
    src_path = os.path.join(SRC, src_file)
    dst_path = os.path.join(DST, dst_file)
    if os.path.exists(dst_path):
        print(f'SKIP (exists): {dst_file}')
        continue
    with open(src_path, encoding='utf-8') as f:
        html = f.read()
    title = get_meta(html, 'og:title')
    summary = get_meta(html, 'og:description')
    date_str = get_meta(html, 'article:published_time')
    tags_raw = get_meta(html, 'article-tags')
    tags = [t.strip() for t in tags_raw.split(',') if t.strip()] if tags_raw else []
    difficulty = get_difficulty(html)
    cover = get_cover_slug(src_file)
    body_html = extract_body(html)
    body_md = html_to_md(body_html)
    tags_yaml = '\n'.join(f'  - "{t}"' for t in tags)
    frontmatter = f'''---
title: "{title}"
date: {date_str}
tags:
{tags_yaml}
summary: "{summary}"
cover: "{cover}"
difficulty: "{difficulty}"
---

'''
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + body_md + '\n')
    print(f'OK: {dst_file}')

print('Done.')
