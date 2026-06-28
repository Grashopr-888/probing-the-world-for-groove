// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// Project site on GitHub Pages → served under /probing-the-world-for-groove/.
// All internal links/assets must respect `base` (use withBase() / import.meta.env.BASE_URL).
// https://astro.build/config
export default defineConfig({
  site: 'https://grashopr-888.github.io',
  base: '/probing-the-world-for-groove',
  trailingSlash: 'ignore',
  integrations: [mdx(), sitemap()],
  build: { format: 'directory' },
});
