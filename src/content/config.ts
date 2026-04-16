import { defineCollection, z } from 'astro:content';

const postSchema = z.object({
  title: z.string(),
  date: z.coerce.date(),
  tags: z.array(z.string()).default([]),
  difficulty: z.string().default('中级'),
  summary: z.string().optional(),
  cover: z.string().optional(),
});

const postsZh = defineCollection({ type: 'content', schema: postSchema });
const postsEn = defineCollection({ type: 'content', schema: postSchema });

const toolSchema = z.object({
  name: z.string(),
  url: z.string(),
  tag: z.string(),
  category: z.string(),
  longDesc: z.string(),
  features: z.array(z.string()).default([]),
  pricing: z.string().default(''),
  pros: z.array(z.string()).default([]),
  cons: z.array(z.string()).default([]),
  relatedPosts: z.array(z.string()).default([]),
});

const toolsZh = defineCollection({ type: 'content', schema: toolSchema });
const toolsEn = defineCollection({ type: 'content', schema: toolSchema });

export const collections = { 'posts-zh': postsZh, 'posts-en': postsEn, 'tools-zh': toolsZh, 'tools-en': toolsEn };
