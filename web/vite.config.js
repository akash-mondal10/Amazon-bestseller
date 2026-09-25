import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// base './' keeps every asset path relative, so the site works at any address,
// including a GitHub Pages project URL like /Amazon-bestseller/.
export default defineConfig({
  plugins: [react()],
  base: './',
  build: { outDir: '../docs', emptyOutDir: true },
});
