import re

DST = 'D:/ai-verse/src/content/posts-zh'

FILES = [
    '2026-04-07-ai-startup-funding-trends-2026.md',
    '2026-04-08-how-to-evaluate-ai-companies-f.md',
    '2026-04-10-ai-regulations-compliance.md',
    '2026-04-03-generative-ai-chip-design-ml-s.md',
    '2026-04-10-ai-unicorn-bubble-reality-chec.md',
    '2026-04-09-ai-company-revenue.md',
]

def fix_faq_section(content):
    """Fix faq-section: split Q+A merged in h3, fix empty p tags."""
    def fix_item(m):
        h3_content = m.group(1)
        # Split on first ？ (full-width question mark)
        parts = re.split(r'(？)', h3_content, maxsplit=1)
        if len(parts) == 3:
            q = parts[0] + parts[1]
            a = parts[2].strip()
            return f'<h3>{q}</h3>\n<p>{a}</p>'
        return m.group(0)  # no change if no ？ found
    content = re.sub(r'<h3>(.*?？.*?)</h3>\s*<p></p>', fix_item, content, flags=re.DOTALL)
    return content

def fix_refs(content):
    """Fix refs: remove trailing </div>, fix merged ref links."""
    # Fix merged reference links (no newline between them)
    content = re.sub(r'(\])\s*-\s*\[', r']\n- [', content)
    # Remove trailing </div> after last ref
    content = re.sub(r'\n\s*</div>\s*$', '\n', content)
    return content

def fix_refs_formatting(content):
    """Fix refs section: ensure blank line after ## 参考资料, fix merged links."""
    content = re.sub(r'(## 参考资料)\n(-)', r'\1\n\n\2', content)
    return content

for fname in FILES:
    path = f'{DST}/{fname}'
    with open(path, encoding='utf-8') as f:
        content = f.read()

    content = fix_faq_section(content)
    content = fix_refs(content)
    content = fix_refs_formatting(content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {fname}')

print('Done.')
