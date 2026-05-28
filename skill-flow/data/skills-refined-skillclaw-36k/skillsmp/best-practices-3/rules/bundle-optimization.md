---
title: Bundle Optimization
impact: CRITICAL
impactDescription: 200-800ms load time reduction
tags: bundle, vite, performance, imports
---

# Bundle Optimization

Minimize bundle size and optimize loading performance.

## Rule 1: Avoid Barrel File Imports

Barrel files (`index.ts` that re-exports) can cause entire modules to be bundled.

```typescript
// ❌ INCORRECT - may import 50+ unused components
import { Button } from '@/components'

// ✅ CORRECT - imports only Button
import { Button } from '@/components/Button'
```

### Why It Matters
- Tree-shaking doesn't work well with barrel files
- Increases initial bundle by 100-500KB
- Slows build times significantly

## Rule 2: Dynamic Imports for Route Components

```typescript
// ❌ INCORRECT - all routes in main bundle
import Dashboard from './pages/Dashboard'
import Settings from './pages/Settings'
import Analytics from './pages/Analytics'

// ✅ CORRECT - routes loaded on demand
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))
const Analytics = lazy(() => import('./pages/Analytics'))
```

## Rule 3: Lazy Load Heavy Libraries

```typescript
// ❌ INCORRECT - chart library in main bundle (400KB+)
import { Chart } from 'chart.js'

// ✅ CORRECT - load when needed
const loadChart = async () => {
  const { Chart } = await import('chart.js')
  return Chart
}
```

## Rule 4: Use Subpath Exports

```typescript
// ❌ INCORRECT - imports entire lodash
import { debounce } from 'lodash'

// ✅ CORRECT - imports only debounce
import debounce from 'lodash/debounce'

// ✅ ALSO CORRECT - use lodash-es for better tree-shaking
import { debounce } from 'lodash-es'
```

## Rule 5: Preload Critical Assets

```typescript
// In main.tsx or route definition
import { prefetch } from 'vite'

// Preload critical route when likely to navigate
const preloadDashboard = () => {
  import('./pages/Dashboard')
}

<Link onMouseEnter={preloadDashboard} to="/dashboard">
  Dashboard
</Link>
```

## Vite Configuration

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor chunks
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui-vendor': ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
          // Feature chunks
          'charts': ['chart.js', 'recharts'],
        }
      }
    }
  }
})
```
