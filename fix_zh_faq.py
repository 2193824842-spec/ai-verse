import re

DST = 'D:/ai-verse/src/content/posts-zh'

FILES = [
    '2026-03-31-openai-122b-agentic-workflows-.md',
    '2026-04-03-generative-ai-chip-design-ml-s.md',
    '2026-04-07-ai-startup-funding-trends-2026.md',
    '2026-04-08-how-to-evaluate-ai-companies-f.md',
    '2026-04-09-ai-company-revenue.md',
    '2026-04-10-ai-agent-market-consolidation-.md',
    '2026-04-10-ai-regulations-compliance.md',
    '2026-04-10-ai-unicorn-bubble-reality-chec.md',
    '2026-04-10-ai-venture-capital-trends-2026.md',
]

def extract_faq_items(faq_block):
    """Extract FAQ items from the messy callout-faq block."""
    items = re.findall(r'<div class="faq-item">(.*?)</div>', faq_block, re.DOTALL)
    result = []
    for item in items:
        item = item.strip()
        # Try <h3>...</h3><p>...</p> format
        h3 = re.search(r'<h3>(.*?)</h3>', item, re.DOTALL)
        p = re.search(r'<p>(.*?)</p>', item, re.DOTALL)
        if h3 and p:
            result.append((h3.group(1).strip(), p.group(1).strip()))
            continue
        # Try ### heading format: "### Q text\nA text"
        m = re.match(r'###\s+(.+?)(?:\n|$)(.*)', item, re.DOTALL)
        if m:
            q = m.group(1).strip()
            a = m.group(2).strip()
            result.append((q, a))
            continue
        # Try inline ### format: "### Q text A text" (no newline)
        m = re.match(r'###\s+(.+)', item)
        if m:
            text = m.group(1).strip()
            # Split on first sentence ending with ？ or ？
            split = re.split(r'(？)', text, maxsplit=1)
            if len(split) >= 3:
                q = split[0] + split[1]
                a = split[2].strip()
                result.append((q, a))
    return result

def build_faq_html(items):
    lines = ['<div class="faq-section">',
             '<h2 id="frequently-asked-questions">常见问题</h2>',
             '<div class="faq-grid">']
    for q, a in items:
        lines.append('<div class="faq-item">')
        lines.append(f'<h3>{q}</h3>')
        lines.append(f'<p>{a}</p>')
        lines.append('</div>')
    lines.append('</div>')
    lines.append('</div>')
    return '\n'.join(lines)

for fname in FILES:
    path = f'{DST}/{fname}'
    with open(path, encoding='utf-8') as f:
        content = f.read()

    # Find the callout-faq block (if any)
    faq_match = re.search(
        r'<div class=["\']callout-card callout-faq["\'].*?</div>\s*</div>',
        content, re.DOTALL
    )
    faq_items = []
    if faq_match:
        faq_items = extract_faq_items(faq_match.group(0))

    # Find references section
    ref_match = re.search(r'\n## 参考资料\n', content)
    if not ref_match:
        print(f'SKIP (no refs): {fname}')
        continue

    # Extract references list (lines starting with - or blank, until author-box or end)
    ref_start = ref_match.start()
    after_refs = content[ref_match.end():]
    # Cut at author-box or callout-faq or end
    cut = re.search(r'\n\s*<div class=["\'](?:author-box|callout)', after_refs)
    if cut:
        refs_body = after_refs[:cut.start()].rstrip()
    else:
        # Also cut at trailing HTML junk
        cut2 = re.search(r'\n\s*</div>', after_refs)
        refs_body = after_refs[:cut2.start()].rstrip() if cut2 else after_refs.rstrip()

    # Build new ending
    new_end = ''
    if faq_items:
        new_end += '\n' + build_faq_html(faq_items) + '\n'
    new_end += '\n## 参考资料\n' + refs_body + '\n'

    # Replace everything from ## 参考资料 onwards
    new_content = content[:ref_start] + new_end
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'OK ({len(faq_items)} FAQ items): {fname}')

print('Done.')
