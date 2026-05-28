---
name: vite
description: >
  Vite build tool patterns and configuration.
  Trigger: When configuring Vite, setting up aliases, or resolving build issues.
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [web]
  auto_invoke: 'Working with Vite configuration'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Import Aliases (REQUIRED)

```typescript
// vite.config.ts
export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});

// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## Usage

```typescript
// ✅ ALWAYS: Use @ alias
import { Button } from '@/components/ui/Button';
import { useClientsStore } from '@/stores/clients.store';

// ❌ NEVER: Relative imports
import { Button } from '../../../components/ui/Button';
```

## Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          vendor-router: ['react-router-dom'],
          vendor-query: ['@tanstack/react-query'],
          vendor-charts: ['recharts'],
        },
      },
    },
  },
});
```

## Environment Variables

```typescript
// ✅ Client-side variables (VITE_ prefix)
const apiUrl = import.meta.env.VITE_API_URL;

// ✅ With fallback
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:3000';

// ✅ Type-safe
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_SOCKET_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

## Commands

```bash
npm run dev:web              # Start dev server (port 5173)
npm run build:web            # Build for production
npm run preview              # Preview production build
```

## Asset Imports

```typescript
// ✅ Images
import logo from '@/assets/logo.png';
<img src={logo} alt="Logo" />

// ✅ CSS
import './styles.css';

// ✅ JSON
import data from './data.json';
```

## Related Skills

- `migestion-web` - MiGestion Web patterns
- `react-18` - React component patterns
