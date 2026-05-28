# Build and Bundling

Optimizing your build process is crucial for fast load times and good developer experience.

## Vite Configuration

Modern build tool with fast HMR and optimal production builds:

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [
    react({
      // Enable React Compiler (React 19+)
      babel: {
        plugins: [['babel-plugin-react-compiler', {}]],
      },
    }),
  ],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },

  build: {
    // Output directory
    outDir: 'dist',

    // Generate sourcemaps for production debugging
    sourcemap: true,

    // Rollup options
    rollupOptions: {
      output: {
        // Manual chunk splitting
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui-vendor': ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
        },
      },
    },

    // Minification
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.logs in production
      },
    },
  },

  // Dev server
  server: {
    port: 3000,
    open: true,
  },
});
```

## Code Splitting Strategies

### Route-Based Splitting

```tsx
const Dashboard = lazy(() => import('./routes/Dashboard'));
const Settings = lazy(() => import('./routes/Settings'));
```

### Vendor Chunking

Separate third-party code for better caching:

```ts
manualChunks(id) {
  if (id.includes('node_modules')) {
    if (id.includes('react') || id.includes('react-dom')) {
      return 'react-vendor';
    }
    return 'vendor';
  }
}
```

## Tree Shaking

Ensure dead code elimination:

```tsx
// ✅ Good - tree-shakeable
import { debounce } from 'es-toolkit';

// ❌ Bad - imports entire library
import _ from 'lodash';
```

## Bundle Analysis

```bash
# Vite
npx vite-bundle-visualizer

# Analyze output
npm run build
npx vite-bundle-visualizer dist/stats.html
```

Target optimizations:
- Large dependencies (replace or code-split)
- Duplicate code across chunks
- Unused exports

## Production Optimizations

- Enable compression (gzip/brotli)
- Use CDN for static assets
- Implement HTTP/2
- Set proper cache headers
- Minimize third-party scripts
