"""
批量生成SEO-Farm工具的MD文件到ai-verse/src/content/tools-zh/
只生成ai-verse中尚未存在的工具
"""
import json
import os
import re
from pathlib import Path

# 加载index.json
with open('D:/seo-farm/site/tools/index.json', 'r', encoding='utf-8') as f:
    seo_tools = json.load(f)

# 获取ai-verse已有的工具slug列表
existing_dir = Path('D:/ai-verse/src/content/tools-zh')
existing_slugs = {p.stem for p in existing_dir.glob('*.md')}
print(f"AI-Verse已有工具数: {len(existing_slugs)}")
print(f"SEO-Farm工具数: {len(seo_tools)}")

# 排除规则：角色扮演/娱乐类 + 低质量/不相关工具
EXCLUDE_NAMES = {
    'AI Dungeon', 'NovelAI', 'CrushOn AI', 'Janitor AI', 'StoryChat',
    'SillyTavern', 'Roleplay AI', 'Xoul.ai', 'Chai', 'Layla', 'Talkie AI',
    'Dreamily', 'GoodBird', 'Image to Prompt Generator', 'Warp Intro Creator',
    'Free AI Video Upscaler', 'RabbitAI', 'Plotica', 'midReal', 'IndexFlow',
    'Sentence 3.0'
}

# 分类映射：seo-farm category → ai-verse categorySlug
CATEGORY_MAP = {
    'AI Writing': 'models',
    'AI Chat': 'models',
    'AI Image': 'image',
    'AI Video': 'video',
    'AI Audio': 'audio',
    'AI Coding': 'coding',
    'AI Design': 'design',
    'AI Developer': 'developer',
    'AI Productivity': 'productivity',
    'AI Search': 'productivity',
}

# 分类中文名映射
CATEGORY_ZH = {
    'models': 'AI大模型',
    'coding': 'AI编程工具',
    'image': 'AI图像工具',
    'video': 'AI视频工具',
    'writing': 'AI写作工具',
    'productivity': 'AI效率工具',
    'audio': 'AI音频工具',
    'design': 'AI设计工具',
    'developer': 'AI开发者工具',
}

# 特殊分类覆盖（根据工具名精确分类）
SPECIAL_CATEGORY = {
    'ChatGPT': 'models',
    'Claude': 'models',
    'Gemini': 'models',
    'Copilot': 'models',
    'DeepSeek': 'models',
    'Jan': 'models',
    'Perplexity': 'productivity',
    'You.com': 'productivity',
    'Notion AI': 'productivity',
    'Jasper': 'writing',
    'Copy.ai': 'writing',
    'Grammarly': 'writing',
    'Canva AI': 'design',
    'Figma AI': 'design',
    'Framer AI': 'design',
    'Gamma': 'productivity',
    'Beautiful.ai': 'productivity',
    'Otter.ai': 'productivity',
    'Fireflies.ai': 'productivity',
    'Zapier AI': 'productivity',
    'Replicate': 'developer',
    'Hugging Face': 'developer',
    'Anthropic Console': 'developer',
    'OpenAI Platform': 'developer',
    'OpenAI Codex': 'coding',
    'Visily': 'design',
    'LogoAI': 'design',
    'Adobe Firefly': 'image',
    'Descript': 'video',
    'Synthesia': 'video',
    'Luma AI': 'video',
}

# slug覆盖映射（seo-farm slug → ai-verse slug）
SLUG_OVERRIDE = {
    'dall-e-3': 'dalle-3',
    'runway-gen-3': 'runway',
    'luma-ai': 'luma-dream-machine',
    'logo-ai': 'logoai',
    'murf-ai': 'murf',
    'fireflies-ai': 'fireflies',
}

def name_to_slug(name):
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug

def pricing_model_to_tag(model):
    mapping = {
        'freemium': '免费/付费',
        'free': '免费',
        'paid': '付费',
    }
    return mapping.get(model, '免费/付费')

def format_pricing_desc(pricing):
    if not pricing:
        return "请访问官网了解最新定价"
    model = pricing.get('model', '')
    plans = pricing.get('plans', [])
    if not plans:
        return pricing_model_to_tag(model)
    parts = []
    for p in plans[:3]:
        name = p.get('name', '')
        price = p.get('price', '')
        if name and price:
            parts.append(f"{name}: {price}")
    return '; '.join(parts) if parts else pricing_model_to_tag(model)

def yaml_str_escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

def yaml_list(items, indent=2):
    if not items:
        return ' []'
    lines = []
    for item in items:
        item_escaped = yaml_str_escape(str(item))
        lines.append(' ' * indent + f'- "{item_escaped}"')
    return '\n' + '\n'.join(lines)

def generate_md(tool):
    name = tool['name']
    url = tool.get('url', '')
    pricing = tool.get('pricing', {})
    tag = pricing_model_to_tag(pricing.get('model', 'freemium'))

    cat_slug = SPECIAL_CATEGORY.get(name) or CATEGORY_MAP.get(tool.get('category', ''), 'productivity')
    cat_zh = CATEGORY_ZH.get(cat_slug, 'AI效率工具')

    desc = tool.get('description', '')
    features = tool.get('features', [])
    pros = tool.get('pros', [])
    cons = tool.get('cons', [])
    pricing_desc = format_pricing_desc(pricing)

    long_desc = desc
    if tool.get('recommended_for'):
        long_desc += f" {tool['recommended_for']}"

    content = f'''---
name: {name}
url: {url}
tag: {tag}
category: {cat_zh}
longDesc: "{yaml_str_escape(long_desc)}"
features:{yaml_list(features)}
pricing: "{yaml_str_escape(pricing_desc)}"
pros:{yaml_list(pros)}
cons:{yaml_list(cons)}
---

## {name}

{desc}

### 核心功能

{chr(10).join(f'- {f}' for f in features) if features else '请访问官网了解详细功能。'}

### 优点

{chr(10).join(f'- {p}' for p in pros) if pros else ''}

### 缺点

{chr(10).join(f'- {c}' for c in cons) if cons else ''}

### 定价

{pricing_desc}
'''
    return content

# 统计
generated = []
skipped_existing = []
skipped_excluded = []

for tool in seo_tools:
    name = tool['name']

    if name in EXCLUDE_NAMES:
        skipped_excluded.append(name)
        continue

    slug = name_to_slug(name)
    slug = SLUG_OVERRIDE.get(slug, slug)

    if slug in existing_slugs:
        skipped_existing.append(f"{name} ({slug})")
        continue

    generated.append((slug, name, tool))

print(f"\n将生成: {len(generated)} 个新MD文件")
print(f"已存在跳过: {len(skipped_existing)} 个")
print(f"排除类别跳过: {len(skipped_excluded)} 个")

print("\n将生成的工具:")
for slug, name, tool in generated:
    cat = SPECIAL_CATEGORY.get(name) or CATEGORY_MAP.get(tool.get('category', ''), 'productivity')
    print(f"  {slug:40} <- {name:25} [{cat}]")

print("\n已存在跳过:")
for s in skipped_existing:
    print(f"  {s}")

# 实际写入文件
if generated:
    print(f"\n开始写入 {len(generated)} 个文件...")
    for slug, name, tool in generated:
        md_content = generate_md(tool)
        out_path = existing_dir / f"{slug}.md"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  ✓ {out_path.name}")
    print(f"\n完成！共生成 {len(generated)} 个文件")
