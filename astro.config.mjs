import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://find-aiverse.com',
  base: '/',
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
