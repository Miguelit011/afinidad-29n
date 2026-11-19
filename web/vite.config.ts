/// <reference types="vitest" />
import { defineConfig, type Plugin } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

// En producción, una Content-Security-Policy estricta garantiza que la página no
// puede enviar datos a ningún servidor (connect-src 'none') ni cargar recursos de
// terceros. En desarrollo no se aplica porque rompería la recarga en caliente.
const csp: Plugin = {
  name: 'csp-privacidad',
  apply: 'build',
  transformIndexHtml(html) {
    const politica = [
      "default-src 'self'",
      "script-src 'self'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data:",
      "connect-src 'none'",
      "form-action 'none'",
      "base-uri 'self'",
    ].join('; ');
    return html.replace(
      '<head>',
      `<head>\n    <meta http-equiv="Content-Security-Policy" content="${politica}" />`,
    );
  },
};

export default defineConfig({
  base: '/afinidad-29n/',
  plugins: [svelte(), csp],
  server: {
    // Los datos viven en ../data (fuera de web/).
    fs: { allow: ['..'] },
  },
  test: {
    include: ['src/**/*.test.ts'],
  },
});
