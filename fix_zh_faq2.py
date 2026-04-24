import re

DST = 'D:/ai-verse/src/content/posts-zh'

# Each entry: (filename, cut_marker)
# cut_marker is a unique string just before the junk starts
FILES = [
    '2026-03-31-openai-122b-agentic-workflows-.md',
    '2026-04-09-ai-company-revenue.md',
    '2026-04-10-ai-agent-market-consolidation-.md',
]

def extract_faq_items(block):
    items = re.findall(r'<div[^>]*class=["\'][^"\']*faq-item[^"\']*["\'][^>]*>(.*?)</div>', block, re.DOTALL)
    result = []
    for item in items:
        item = item.strip()
        h3 = re.search(r'<h3>(.*?)</h3>', item, re.DOTALL)
        p = re.search(r'<p>(.*?)</p>', item, re.DOTALL)
        if h3 and p:
            result.append((h3.group(1).strip(), p.group(1).strip()))
            continue
        # ### Q\nA format
        m = re.match(r'###\s+(.+?)(?:\n)(.*)', item, re.DOTALL)
        if m:
            result.append((m.group(1).strip(), m.group(2).strip()))
            continue
        # inline ### Q？A format
        m = re.match(r'###\s+(.+)', item)
        if m:
            text = m.group(1).strip()
            split = re.split(r'(？)', text, maxsplit=1)
            if len(split) >= 3:
                result.append((split[0] + split[1], split[2].strip()))
    return result

def build_faq_html(items):
    lines = ['<div class="faq-section">',
             '<h2 id="frequently-asked-questions">常见问题</h2>',
             '<div class="faq-grid">']
    for q, a in items:
        lines += ['<div class="faq-item">', f'<h3>{q}</h3>', f'<p>{a}</p>', '</div>']
    lines += ['</div>', '</div>']
    return '\n'.join(lines)

for fname in FILES:
    path = f'{DST}/{fname}'
    with open(path, encoding='utf-8') as f:
        content = f.read()

    # Find FAQ block
    faq_match = re.search(
        r'<div[^>]*class=["\'][^"\']*callout-faq[^"\']*["\'][^>]*>.*?</div>\s*</div>\s*</div>',
        content, re.DOTALL
    )
    faq_items = extract_faq_items(faq_match.group(0)) if faq_match else []

    # Find refs section (may have leading spaces)
    ref_match = re.search(r'\n\s*## 参考资料\n', content)

    # Find the last real content before author-box junk
    author_match = re.search(r'\n\s*</div>\s*\n\s*<div[^>]*class=["\']author-box', content)
    if not author_match:
        author_match = re.search(r'\n\s*<div[^>]*class=["\']author-box', content)

    if ref_match:
        # Extract refs body
        after_refs = content[ref_match.end():]
        cut = re.search(r'\n\s*(?:</div>|<div[^>]*class=["\']author-box)', after_refs)
        refs_body = after_refs[:cut.start()].rstrip() if cut else after_refs.rstrip()
        # Normalize indented list items
        refs_body = re.sub(r'^\s+- ', '- ', refs_body, flags=re.MULTILINE)
        cut_pos = ref_match.start()
    elif author_match:
        cut_pos = author_match.start()
        refs_body = None
    else:
        print(f'SKIP (no cut point): {fname}')
        continue

    new_end = '\n'
    if faq_items:
        new_end += build_faq_html(faq_items) + '\n\n'
    if refs_body is not None:
        new_end += '## 参考资料\n' + refs_body + '\n'

    new_content = content[:cut_pos] + new_end
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'OK ({len(faq_items)} FAQ): {fname}')

print('Done.')
