import { defineConfig } from 'astro/config';
import icon from 'astro-icon';

export default defineConfig({
  site: 'https://avanness213.github.io',
  output: 'static',
  integrations: [icon()],
});
