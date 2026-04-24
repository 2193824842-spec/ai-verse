import re

DST = 'D:/ai-verse/src/content/posts-zh'

# (filename, tags_zh, category)
POSTS = [
    ('2026-03-31-openai-122b-agentic-workflows-.md',
     ['OpenAI', 'AI融资', '智能体AI', '企业AI'],
     'trending'),
    ('2026-04-03-generative-ai-chip-design-ml-s.md',
     ['AI芯片', '半导体', '生成式AI', '机器学习'],
     'industry-insights'),
    ('2026-04-07-ai-startup-funding-trends-2026.md',
     ['AI创业公司', 'AI融资', '风险投资', 'AI投资'],
     'trending'),
    ('2026-04-08-how-to-evaluate-ai-companies-f.md',
     ['AI投资', 'AI估值', '企业AI', 'AI创业公司'],
     'industry-insights'),
    ('2026-04-09-ai-company-revenue.md',
     ['AI营收', 'OpenAI', 'Anthropic', 'AI投资', '企业AI'],
     'industry-insights'),
    ('2026-04-10-ai-2027-scenario-realistic-inf.md',
     ['AI 2027', 'AI基础设施', 'AI行业', 'AI投资'],
     'industry-insights'),
    ('2026-04-10-ai-agent-market-consolidation-.md',
     ['AI智能体', 'AI框架', 'LangChain', 'AI投资'],
     'industry-insights'),
    ('2026-04-10-ai-regulations-compliance.md',
     ['AI监管', 'EU AI法案', 'AI合规', '企业AI', 'AI投资'],
     'industry-insights'),
    ('2026-04-10-ai-unicorn-bubble-reality-chec.md',
     ['AI独角兽', 'AI创业公司', 'AI投资', '创业失败'],
     'trending'),
    ('2026-04-10-ai-venture-capital-trends-2026.md',
     ['风险投资', 'AI投资', 'AI融资', 'AI创业公司'],
     'industry-insights'),
]

for fname, tags, category in POSTS:
    path = f'{DST}/{fname}'
    with open(path, encoding='utf-8') as f:
        content = f.read()

    tags_yaml = '[' + ', '.join(f'"{t}"' for t in tags) + ']'

    # replace tags block (handles both "tags: []" and "tags:\n  - ..." forms)
    content = re.sub(
        r'^tags:.*?(?=\n\w)',
        f'tags: {tags_yaml}',
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # add or replace category
    if re.search(r'^category:', content, re.MULTILINE):
        content = re.sub(r'^category:.*$', f'category: "{category}"', content, flags=re.MULTILINE)
    else:
        content = re.sub(r'^(difficulty:)', f'category: "{category}"\n\\1', content, flags=re.MULTILINE)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {fname}')

print('Done.')
