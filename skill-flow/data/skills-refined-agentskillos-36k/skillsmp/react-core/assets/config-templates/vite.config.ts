import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react({
      // Enable React Compiler (React 19+)
      // Uncomment when using React 19
      // babel: {
      //   plugins: [['babel-plugin-react-compiler', {}]],
      // },
    }),
  ],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },

  build: {
    outDir: 'dist',
    sourcemap: true,

    rollupOptions: {
      output: {
        manualChunks: {
          // Separate React vendor bundle
          'react-vendor': ['react', 'react-dom'],

          // Separate router bundle if using React Router
          'router-vendor': ['react-router-dom'],

          // Separate data fetching bundle if using React Query
          'query-vendor': ['@tanstack/react-query'],
        },
      },
    },

    // Minification
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.logs in production
        drop_debugger: true,
      },
    },

    // Chunk size warnings
    chunkSizeWarningLimit: 1000,
  },

  server: {
    port: 3000,
    open: true,
    // Proxy API requests during development
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },

  preview: {
    port: 4173,
  },
});
