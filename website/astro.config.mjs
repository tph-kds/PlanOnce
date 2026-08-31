import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://tph-kds.github.io',
  base: '/PlanOnce/',
  integrations: [mdx()],
  output: 'static',
  trailingSlash: 'ignore',
  build: {
    assets: '_assets'
  }
});
