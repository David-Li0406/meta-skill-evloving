# Performance Reference

## Contents
- Current Optimization Status
- Animation Patterns
- Hydration Handling
- Memoization Patterns
- Bundle Considerations

## Current Optimization Status

| Optimization | Status | Notes |
|--------------|--------|-------|
| React.memo | Not used | Marketing site, not needed |
| useMemo | Not used | No expensive calculations |
| useCallback | Not used | No callback prop drilling |
| Code splitting | Not used | Small site |
| Image optimization | Disabled | `unoptimized: true` in next.config |

This is appropriate for a small marketing site with static content.

## Animation Patterns

### Staggered Animation Delays

```tsx
{services.map((service, index) => (
  <div
    key={index}
    className="animate-fadeIn"
    style={{ animationDelay: `${(index + 1) * 0.1}s` }}
  >
    {/* Card content */}
  </div>
))}
```

### Custom Animations (globals.css)

```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.animate-fadeIn { animation: fadeIn 0.6s ease-out forwards; }
.animate-float { animation: float 3s ease-in-out infinite; }
.animate-pulse-slow { animation: pulse 3s ease-in-out infinite; }
```

## Hydration Handling

Prevents hydration mismatch in Next.js App Router:

```tsx
const [mounted, setMounted] = useState(false)

useEffect(() => {
  setMounted(true)
}, [])

if (!mounted) return null
```

**When to use:**
- Components with client-only rendering
- Third-party widgets (Calendly, chat widgets)
- Content that differs between server and client

## Memoization Patterns

When to add memoization (if needed):

### React.memo for Expensive Components

```tsx
// GOOD - When child re-renders are expensive
const ServiceCard = React.memo(function ServiceCard({ service, onToggle }) {
  return (
    <div onClick={() => onToggle(service.id)}>
      {/* Complex rendering */}
    </div>
  )
})
```

### useMemo for Expensive Calculations

```tsx
// GOOD - When calculation is expensive
const sortedPosts = useMemo(() => {
  return posts.sort((a, b) => new Date(b.date) - new Date(a.date))
}, [posts])
```

### useCallback for Stable References

```tsx
// GOOD - When passing callbacks to memoized children
const handleToggle = useCallback((id: number) => {
  setExpanded(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id])
}, [])
```

## WARNING: Unnecessary Optimization Anti-Pattern

**The Problem:**

```tsx
// BAD - Premature optimization
const MemoizedCard = React.memo(({ title }) => <div>{title}</div>)

const Component = () => {
  const items = useMemo(() => ['a', 'b', 'c'], []) // Static array
  const handleClick = useCallback(() => console.log('click'), []) // Simple callback
  return items.map(i => <MemoizedCard key={i} title={i} onClick={handleClick} />)
}
```

**Why This Is Wrong:**
1. Static arrays don't need useMemo
2. Simple callbacks don't need useCallback unless passed to memoized children
3. React.memo has comparison overhead
4. Adds complexity without measurable benefit

**The Fix:**

Only add memoization when you measure a performance problem:
1. Use React DevTools Profiler
2. Identify slow renders
3. Add targeted memoization
4. Measure improvement

## Bundle Considerations

### Current Dependencies

Small bundle - no heavy libraries:
- React 19
- Next.js 15
- lucide-react (tree-shakeable icons)
- resend (server-only)

### If Adding Libraries

```tsx
// GOOD - Dynamic import for heavy components
const CalendlyWidget = dynamic(() => import('./CalendlyWidget'), {
  loading: () => <Spinner />,
  ssr: false
})

// GOOD - Lazy loading for routes
const BlogPost = lazy(() => import('./BlogPost'))
```

See the **nextjs** skill for dynamic imports and route loading.