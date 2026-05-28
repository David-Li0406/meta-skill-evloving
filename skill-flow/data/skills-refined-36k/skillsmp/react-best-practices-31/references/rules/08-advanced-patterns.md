# Advanced Patterns

**Impact: LOW** | Specialized patterns for specific cases requiring careful implementation.

---

## 1. Store Event Handlers in Refs

Store callbacks in refs when used in effects that shouldn't re-subscribe on callback changes.

```tsx
// BAD: re-subscribes on every render
function useWindowEvent(event: string, handler: () => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler]) // handler changes every render
}

// GOOD: stable subscription
function useWindowEvent(event: string, handler: () => void) {
  const handlerRef = useRef(handler)

  useEffect(() => {
    handlerRef.current = handler
  }, [handler])

  useEffect(() => {
    const listener = () => handlerRef.current()
    window.addEventListener(event, listener)
    return () => window.removeEventListener(event, listener)
  }, [event])
}
```

---

## 2. useLatest for Stable Callback Refs

Access latest values in callbacks without adding to dependency arrays. Prevents effect re-runs while avoiding stale closures.

```typescript
function useLatest<T>(value: T) {
  const ref = useRef(value)
  useEffect(() => { ref.current = value }, [value])
  return ref
}
```

**Usage:**

```tsx
// BAD: effect re-runs on every callback change
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')

  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300)
    return () => clearTimeout(timeout)
  }, [query, onSearch]) // onSearch causes re-runs
}

// GOOD: stable effect, fresh callback
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')
  const onSearchRef = useLatest(onSearch)

  useEffect(() => {
    const timeout = setTimeout(() => onSearchRef.current(query), 300)
    return () => clearTimeout(timeout)
  }, [query]) // only query triggers effect
}
```
