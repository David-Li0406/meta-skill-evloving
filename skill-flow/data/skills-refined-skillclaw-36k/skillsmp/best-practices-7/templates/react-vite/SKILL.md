---
name: best-practices
description: React + Vite performance optimization and best practices guidelines
license: MIT
metadata:
  author: devnogari
  project_type: react-vite
  extends: vercel-react-best-practices
---

# React + Vite Best Practices

Performance optimization and best practices for React applications using Vite.

## Primary Reference

**This skill extends `/vercel-react-best-practices`** - Vercel's official 45-rule guide for React performance.

When working on React code, **always invoke `/vercel-react-best-practices` first** for comprehensive patterns, then apply Vite-specific optimizations below.

## Activation Triggers

This skill activates when:
- Writing new React components or hooks
- Implementing state management patterns
- Optimizing bundle size or load times
- Reviewing or refactoring React code
- Debugging performance issues

## Routing to Vercel Best Practices

For these patterns, use `/vercel-react-best-practices`:
- Eliminating async waterfalls → `async-*` rules
- Bundle optimization → `bundle-*` rules
- Re-render prevention → `rerender-*` rules
- JavaScript performance → `js-*` rules

## Rule Categories

### Priority Order

| # | Category | Priority | Typical Impact |
|---|----------|----------|----------------|
| 1 | Bundle Optimization | CRITICAL | 200-800ms load time reduction |
| 2 | Re-render Prevention | HIGH | 2-10x render performance |
| 3 | State Management | HIGH | Memory & render efficiency |
| 4 | Async Patterns | MEDIUM | Network efficiency |
| 5 | Component Patterns | MEDIUM | Maintainability & performance |

## Quick Reference

### Bundle Optimization (CRITICAL)

**Avoid barrel imports:**
```typescript
// ❌ INCORRECT - imports entire library
import { Button, Input } from '@/components'

// ✅ CORRECT - imports only what's needed
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
```

**Dynamic imports for large components:**
```typescript
// ❌ INCORRECT - loads immediately
import { HeavyChart } from './HeavyChart'

// ✅ CORRECT - loads on demand
const HeavyChart = lazy(() => import('./HeavyChart'))
```

### Re-render Prevention (HIGH)

**Memoize expensive computations:**
```typescript
// ❌ INCORRECT - recalculates every render
const sortedItems = items.sort((a, b) => a.name.localeCompare(b.name))

// ✅ CORRECT - only recalculates when items change
const sortedItems = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
)
```

**Stable callback references:**
```typescript
// ❌ INCORRECT - new function every render
<Button onClick={() => handleClick(id)} />

// ✅ CORRECT - stable reference
const handleButtonClick = useCallback(() => handleClick(id), [id])
<Button onClick={handleButtonClick} />
```

### State Management (HIGH)

**Colocate state with usage:**
```typescript
// ❌ INCORRECT - state too high in tree
function App() {
  const [modalOpen, setModalOpen] = useState(false)
  return <DeepChild modalOpen={modalOpen} />
}

// ✅ CORRECT - state near usage
function ModalContainer() {
  const [modalOpen, setModalOpen] = useState(false)
  return <Modal open={modalOpen} />
}
```

**Split state by update frequency:**
```typescript
// ❌ INCORRECT - unrelated state together
const [state, setState] = useState({ user: null, theme: 'dark', count: 0 })

// ✅ CORRECT - independent state
const [user, setUser] = useState(null)
const [theme, setTheme] = useState('dark')
const [count, setCount] = useState(0)
```

## Detailed Rules

See individual rule files in `rules/` directory:
- `bundle-optimization.md`
- `rerender-prevention.md`
- `state-management.md`
- `async-patterns.md`
- `component-patterns.md`
- `vite-specific.md`

## Integration with Development Workflow

When writing or reviewing React code:

1. **Before implementation**: Check relevant rule categories
2. **During development**: Apply patterns from quick reference
3. **Code review**: Verify against rule checklist
4. **Performance issues**: Consult detailed rules for solutions

## Vite-Specific Optimizations (Supplement to Vercel Rules)

These patterns are **Vite-specific** and extend the Vercel best practices:

**Configure optimizeDeps:**
```typescript
// vite.config.ts
export default defineConfig({
  optimizeDeps: {
    include: ['react', 'react-dom', 'lodash-es'],
    exclude: ['@my-org/heavy-lib']
  }
})
```

**Use manual chunks for code splitting:**
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu']
        }
      }
    }
  }
})
```

## Workflow Integration

When implementing React features:

1. **First**: Invoke `/vercel-react-best-practices` for comprehensive React patterns
2. **Then**: Apply Vite-specific optimizations from this file
3. **Review**: Check against Vercel's `bundle-*` and `async-*` rules

```
/vercel-react-best-practices → React patterns (45 rules)
     ↓
This skill → Vite-specific config & chunking
```
