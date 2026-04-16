import { getCollection } from 'astro:content';

export async function GET() {
  const zh = await getCollection('posts-zh');
  const en = await getCollection('posts-en');
  const index = [
    ...zh.map(p => ({
      slug: p.slug,
      lang: 'zh',
      title: p.data.title,
      summary: p.data.summary ?? '',
      tags: p.data.tags,
      cover: p.data.cover ?? '',
    })),
    ...en.map(p => ({
      slug: p.slug,
      lang: 'en',
      title: p.data.title,
      summary: p.data.summary ?? '',
      tags: p.data.tags,
      cover: p.data.cover ?? '',
    })),
  ];
  return new Response(JSON.stringify(index), {
    headers: { 'Content-Type': 'application/json' },
  });
}
