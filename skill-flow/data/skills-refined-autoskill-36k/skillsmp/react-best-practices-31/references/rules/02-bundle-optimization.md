# Bundle Size Optimization

**Impact: CRITICAL** | Reducing initial bundle size improves Time to Interactive and Largest Contentful Paint.

---

## 1. Avoid Barrel File Imports

Import directly from source files. Barrel files can have 10,000+ re-exports causing **200-800ms import cost**.

```tsx
// BAD: imports entire library
import { Check, X, Menu } from 'lucide-react'
import { Button } from '@mui/material'

// GOOD: imports only what you need
import Check from 'lucide-react/dist/esm/icons/check'
import Button from '@mui/material/Button'

// ALTERNATIVE: Next.js 13.5+ config
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: ['lucide-react', '@mui/material']
  }
}
```

**Affected libraries:** lucide-react, @mui/material, react-icons, lodash, date-fns, rxjs, @radix-ui/react-*

---

## 2. Dynamic Imports for Heavy Components

Use `next/dynamic` to lazy-load large components not needed on initial render.

```tsx
// BAD: Monaco (~300KB) bundles with main chunk
import { MonacoEditor } from './monaco-editor'

// GOOD: Monaco loads on demand
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(
  () => import('./monaco-editor').then(m => m.MonacoEditor),
  { ssr: false }
)
```

---

## 3. Defer Non-Critical Third-Party Libraries

Analytics, logging, error tracking don't block user interaction - load after hydration.

```tsx
// BAD: blocks initial bundle
import { Analytics } from '@vercel/analytics/react'

// GOOD: loads after hydration
import dynamic from 'next/dynamic'

const Analytics = dynamic(
  () => import('@vercel/analytics/react').then(m => m.Analytics),
  { ssr: false }
)
```

---

## 4. Conditional Module Loading

Load large modules only when features are activated.

```tsx
function AnimationPlayer({ enabled }: { enabled: boolean }) {
  const [frames, setFrames] = useState<Frame[] | null>(null)

  useEffect(() => {
    if (enabled && !frames && typeof window !== 'undefined') {
      import('./animation-frames.js').then(mod => setFrames(mod.frames))
    }
  }, [enabled, frames])

  if (!frames) return <Skeleton />
  return <Canvas frames={frames} />
}
```

---

## 5. Preload Based on User Intent

Preload heavy bundles on hover/focus to reduce perceived latency.

```tsx
function EditorButton({ onClick }: { onClick: () => void }) {
  const preload = () => {
    if (typeof window !== 'undefined') {
      void import('./monaco-editor')
    }
  }

  return (
    <button onMouseEnter={preload} onFocus={preload} onClick={onClick}>
      Open Editor
    </button>
  )
}
```
