import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig(async () => ({
  plugins: [react()],

  // Path aliases
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@types': path.resolve(__dirname, './src/types'),
      '@stores': path.resolve(__dirname, './src/stores'),
      codemap: path.resolve(__dirname, './src/types/codemap'),
    },
  },

  // Tauri expects a fixed port, fail if that port is not available
  server: {
    port: 1420,
    strictPort: true,
    watch: {
      ignored: ['**/src-tauri/**'],
    },
    hmr: {
      overlay: false,
    },
  },

  // Environment variables
  envPrefix: ['VITE_', 'TAURI_'],

  // Dependencies pre-bundling
  optimizeDeps: {
    include: ['react', 'react-dom', 'reactflow', 'd3', 'mermaid', 'marked', 'zustand'],
    exclude: ['@tauri-apps/api'],
  },

  // Build options
  build: {
    target: process.env.TAURI_PLATFORM === 'windows' ? 'chrome105' : 'safari13',
    minify: !process.env.TAURI_DEBUG ? 'esbuild' : false,
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          'monaco-editor': ['monaco-editor', '@monaco-editor/react'],
          'reactflow-core': ['reactflow', 'd3'],
          markdown: ['mermaid', 'marked', 'react-markdown'],
          'ui-components': [
            '@radix-ui/react-dialog',
            '@radix-ui/react-select',
            '@radix-ui/react-tabs',
          ],
        },
        onwarn(warning, warn) {
          if (warning.code === 'MODULE_NOT_FOUND' && warning.message.includes('monaco-editor')) {
            return;
          }
          warn(warning);
        },
      },
    },
    chunkSizeWarningLimit: 1000,
  },

  // Performance optimizations
  css: {
    devSourcemap: false,
  },

  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version || '0.1.0'),
  },
}));
