# Working Lovable Configuration Examples

Reference files for diagnosing Lovable issues. Compare user's files against these patterns.

## Critical Files Checklist

When debugging, check these files exist and match patterns:

| File | Purpose | Common Issues |
|------|---------|---------------|
| `src/AppEntry.tsx` | Lovable's dynamic import entry | Re-export syntax, missing file |
| `vite.config.ts` | Build configuration | Missing optimizeDeps, wrong aliases |
| `package.json` (root) | Monorepo scripts & deps | Missing delegation scripts, deps only in app |
| `package.json` (app) | App dependencies | Missing workspace deps |
| `tsconfig.json` | TypeScript paths | Paths don't match Vite aliases |
| `postcss.config.js` | Tailwind/PostCSS | Wrong location (should be in app) |

---

## AppEntry.tsx (CRITICAL)

Lovable dynamically imports this file. Must use explicit import/export pattern.

```tsx
// apps/[app-name]/src/AppEntry.tsx
// ✅ CORRECT - explicit import and export
import App from "./App";
export default App;
```

```tsx
// ❌ WRONG - re-export syntax causes dynamic import failures
export { default } from "./App";
```

---

## vite.config.ts

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

export default defineConfig(({ mode }) => ({
  plugins: [
    react(),
    mode === "development" && componentTagger(),
  ].filter(Boolean),

  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      // Workspace packages - adjust paths for your structure
      "@ui": path.resolve(__dirname, "../../packages/ui/src"),
      "@shared-auth": path.resolve(__dirname, "../../packages/shared-auth/src"),
    },
  },

  // CRITICAL: Pre-bundle dependencies to avoid 504 timeouts
  optimizeDeps: {
    include: [
      "react",
      "react-dom",
      "react/jsx-runtime",
      "framer-motion",
      // Add any package that causes 504 Gateway Timeout
    ],
  },

  build: {
    // Handle workspace package CommonJS
    commonjsOptions: {
      include: [/packages\/.*/, /node_modules/],
    },
  },

  server: {
    host: "0.0.0.0",  // Required for Lovable container
    port: 5173,
  },
}));
```

### Key Points
- `optimizeDeps.include` - Add packages that timeout (504 errors)
- `host: "0.0.0.0"` - Required, not `localhost`
- `componentTagger` - Only in development mode

---

## package.json (Root - Monorepo)

```json
{
  "name": "your-monorepo",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev": "npm run dev --workspace=apps/your-app",
    "build": "npm run build --workspace=apps/your-app",
    "build:dev": "npm run build:dev --workspace=apps/your-app",
    "preview": "npm run preview --workspace=apps/your-app",
    "test": "npm run test --workspace=apps/your-app"
  },
  "dependencies": {
    "framer-motion": "^12.0.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "vite": "^7.0.0",
    "typescript": "^5.0.0"
  }
}
```

### Key Points
- Scripts delegate to workspace with `--workspace=apps/[name]`
- Dependencies in ROOT, not just in app (Lovable installs from root)
- `build:dev` script required by Lovable

---

## package.json (App)

```json
{
  "name": "your-app",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite --host 0.0.0.0 --port 5173",
    "build": "vite build --mode production",
    "build:dev": "vite build --mode development",
    "preview": "vite preview --host 0.0.0.0 --port 4173",
    "test": "vitest run"
  },
  "dependencies": {
    "@your-org/shared-auth": "*",
    "@your-org/ui": "*",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  }
}
```

### Key Points
- `--host 0.0.0.0` in dev/preview scripts
- Workspace packages listed as dependencies with `"*"`

---

## tsconfig.json

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@ui/*": ["../../packages/ui/src/*"],
      "@shared-auth/*": ["../../packages/shared-auth/src/*"]
    },
    "skipLibCheck": true,
    "allowJs": true
  }
}
```

### Key Points
- Paths must match Vite aliases exactly
- `baseUrl: "."` required for paths to work

---

## postcss.config.js

Must be in **app directory**, not root.

```javascript
// apps/[app-name]/postcss.config.js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

Location check:
- ✅ `apps/your-app/postcss.config.js`
- ❌ `./postcss.config.js` (root - will fail)

---

## Diff Checklist

When comparing user files to these examples, check:

### AppEntry.tsx
- [ ] Uses `import X from "./App"` then `export default X`
- [ ] NOT using `export { default } from "./App"`

### vite.config.ts
- [ ] Has `optimizeDeps.include` with react packages
- [ ] Has `host: "0.0.0.0"` in server config
- [ ] Aliases use correct relative paths (`../../packages/...`)

### Root package.json
- [ ] Has delegation scripts (`--workspace=apps/[name]`)
- [ ] Has `build:dev` script
- [ ] Dependencies needed by app are in root deps

### App package.json
- [ ] Scripts have `--host 0.0.0.0`
- [ ] Workspace packages in dependencies with `"*"`

### tsconfig.json
- [ ] Paths match vite.config.ts aliases
- [ ] Has `baseUrl: "."`

### postcss.config.js
- [ ] Located in app directory, not root
