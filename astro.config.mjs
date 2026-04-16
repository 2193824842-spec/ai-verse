import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://2193824842-spec.github.io',
  base: '/ai-verse',
  trailingSlash: 'always',
  integrations: [],
  markdown: {
    shikiConfig: {
      themes: {
        light: 'github-light',
        dark: 'github-dark',
      },
    },
  },
});
