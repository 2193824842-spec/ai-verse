import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import fs from 'fs';
import path from 'path';

const BASE = 'https://2193824842-spec.github.io/ai-verse';

// 从文章 frontmatter 中读取 date，构建 URL → lastmod 映射
function buildDateMap() {
  const map = {};
  const contentDirs = [
    { dir: 'src/content/posts-zh', urlPrefix: '/zh/posts/' },
    { dir: 'src/content/posts-en', urlPrefix: '/en/posts/' },
  ];
  for (const { dir, urlPrefix } of contentDirs) {
    const dirPath = path.join(process.cwd(), dir);
    if (!fs.existsSync(dirPath)) continue;
    const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.md'));
    for (const file of files) {
      const content = fs.readFileSync(path.join(dirPath, file), 'utf-8');
      const match = content.match(/^date:\s*(.+)$/m);
      if (!match) continue;
      const date = new Date(match[1].trim());
      if (isNaN(date)) continue;
      const slug = file.replace('.md', '');
      map[`${BASE}${urlPrefix}${slug}/`] = date.toISOString();
    }
  }
  return map;
}

const dateMap = buildDateMap();

export default defineConfig({
  site: 'https://2193824842-spec.github.io',
  base: '/ai-verse',
  trailingSlash: 'always',
  integrations: [
    sitemap({
      // 排除旧路径（重定向页，不应被收录）
      filter: (page) =>
        !page.includes(`${BASE}/posts/`) &&
        !page.includes(`${BASE}/tags/`) &&
        !page.includes(`${BASE}/search/`) &&
        !page.includes(`${BASE}/about/`) &&
        page !== `${BASE}/`,
      // 为中英文页面添加 hreflang
      customPages: [],
      serialize(item) {
        // 注入 lastmod：文章用 frontmatter date，其余用今天
        item.lastmod = dateMap[item.url] ?? new Date().toISOString().split('T')[0];
        // 中文页面 → 添加英文 alternate
        if (item.url.includes('/zh/posts/')) {
          const enUrl = item.url.replace('/zh/posts/', '/en/posts/');
          item.links = [
            { lang: 'zh-CN', url: item.url },
            { lang: 'en',    url: enUrl },
            { lang: 'x-default', url: item.url },
          ];
        }
        // 英文页面 → 添加中文 alternate
        if (item.url.includes('/en/posts/')) {
          const zhUrl = item.url.replace('/en/posts/', '/zh/posts/');
          item.links = [
            { lang: 'zh-CN', url: zhUrl },
            { lang: 'en',    url: item.url },
            { lang: 'x-default', url: zhUrl },
          ];
        }
        return item;
      },
    }),
  ],
  markdown: {
    shikiConfig: {
      themes: {
        light: 'github-light',
        dark: 'github-dark',
      },
    },
  },
});
