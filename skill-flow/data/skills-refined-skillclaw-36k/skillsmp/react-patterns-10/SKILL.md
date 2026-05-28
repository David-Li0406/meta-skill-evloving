---
name: react-patterns
description: Modern React patterns including hooks, state management, and performance
license: MIT
---

# React Patterns Skill

Modern React development patterns focusing on hooks, composition, state management, and performance optimization.

## When to Use

- Building React applications
- Implementing complex state logic
- Optimizing component performance
- Structuring React projects

## Component Patterns

### Composition over Props

```tsx
// Bad: Prop drilling and rigid structure
<Card
  title="User"
  subtitle="Admin"
  image="/avatar.png"
  footer={<Button>Edit</Button>}
/>

// Good: Composable structure
<Card>
  <Card.Header>
    <Card.Title>User</Card.Title>
    <Card.Subtitle>Admin</Card.Subtitle>
  </Card.Header>
  <Card.Image src="/avatar.png" />
  <Card.Footer>
    <Button>Edit</Button>
  </Card.Footer>
</Card>
```

### Compound Components

```tsx
import { createContext, useContext, useState, ReactNode } from 'react'

interface AccordionContextType {
  openItems: Set<string>
  toggle: (id: string) => void
}

const AccordionContext = createContext<AccordionContextType | null>(null)

function useAccordion() {
  const context = useContext(AccordionContext)
  if (!context) throw new Error('Must be used within Accordion')
  return context
}

export function Accordion({ children }: { children: ReactNode }) {
  const [openItems, setOpenItems] = useState<Set<string>>(new Set())

  const toggle = (id: string) => {
    setOpenItems(prev => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

  return (
    <AccordionContext.Provider value={{ openItems, toggle }}>
      <div className="divide-y">{children}</div>
    </AccordionContext.Provider>
  )
}

function Item({ id, children }: { id: string; children: ReactNode }) {
  return <div data-accordion-item={id}>{children}</div>
}

function Trigger({ id, children }: { id: string; children: ReactNode }) {
  const { openItems, toggle } = useAccordion()
  const isOpen = openItems.has(id)

  return (
    <button onClick={() => toggle(id)} aria-expanded={isOpen}>
      {children}
      <span>{isOpen ? '−' : '+'}</span>
    </button>
  )
}

function Content({ id, children }: { id: string; children: ReactNode }) {
  const { openItems } = useAccordion()
  if (!openItems.has(id)) return null
  return <div>{children}</div>
}

Accordion.Item = Item
Accordion.Trigger = Trigger
Accordion.Content = Content
```

### Render Props

```tsx
interface MousePosition {
  x: number
  y: number
}

interface MouseTrackerProps {
  children: (position: MousePosition) => ReactNode
}

function MouseTracker({ children }: MouseTrackerProps) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 })

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY })
    }
    window.addEventListener('mousemove', handler)
    return () => window.removeEventListener('mousemove', handler)
  }, [])

  return <>{children(position)}</>
}

// Usage
<MouseTracker>
  {({ x, y }) => (
    <div>Mouse: {x}, {y}</div>
  )}
</MouseTracker>
```

## Custom Hooks

### useAsync

```tsx
interface AsyncState<T> {
  data: T | null
  error: Error | null
  isLoading: boolean
}

function useAsync<T>(asyncFn: () => Promise<T>, deps: any[] = []) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    error: null,
    isLoading: true,
  })

  useEffect(() => {
    let cancelled = false
    setState(s => ({ ...s, isLoading: true }))

    asyncFn()
      .then(data => {
        if (!cancelled) setState({ data, error: null, isLoading: false })
      })
      .catch(error => {
        if (!cancelled) setState({ data: null, error, isLoading: false })
      })

    return () => { cancelled = true }
  }, deps)

  return state
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, error, isLoading } = useAsync(
    () => fetchUser(userId),
    [userId]
  )

  if (isLoading) return <Spinner />
  if (error) return <Error message={error.message} />
  return <Profile user={user} />
}
```

### useDebounce

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])

  return debouncedValue
}

// Usage
function Search() {
  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounce(query, 300)

  useEffect(() => {
    if (debouncedQuery) {
      searchAPI(debouncedQuery)
    }
  }, [debouncedQuery])

  return <input value={query} onChange={e => setQuery(e.target.value)} />
}
```

### useLocalStorage

```tsx
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch {
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(error)
    }
  }

  return [storedValue, setValue] as const
}

// Usage
const [theme, setTheme] = useLocalStorage('theme', 'light')
```

### usePrevious

```tsx
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>()

  useEffect(() => {
    ref.current = value
  }, [value])

  return ref.current
}

// Usage
function Counter() {
  const [count, setCount] = useState(0)
  const prevCount = usePrevious(count)

  return (
    <div>
      Now: {count}, Before: {prevCount}
    </div>
  )
}
```

### useClickOutside

```tsx
function useClickOutside<T extends HTMLElement>(
  handler: () => void
): RefObject<T> {
  const ref = useRef<T>(null)

  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      if (!ref.current || ref.current.contains(event.target as Node)) {
        return
      }
      handler()
    }

    document.addEventListener('mousedown', listener)
    document.addEventListener('touchstart', listener)

    return () => {
      document.removeEventListener('mousedown', listener)
      document.removeEventListener('touchstart', listener)
    }
  }, [handler])

  return ref
}

// Usage
function Dropdown() {
  const [isOpen, setIsOpen] = useState(false)
  const ref = useClickOutside<HTMLDivElement>(() => setIsOpen(false))

  return (
    <div ref={ref}>
      <button onClick={() => setIsOpen(true)}>Open</button>
      {isOpen && <div>Dropdown content</div>}
    </div>
  )
}
```

## State Management Patterns

### useReducer for Complex State

```tsx
interface State {
  items: Item[]
  isLoading: boolean
  error: string | null
  filter: 'all' | 'active' | 'completed'
}

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: Item[] }
  | { type: 'FETCH_ERROR'; payload: string }
  | { type: 'ADD_ITEM'; payload: Item }
  | { type: 'TOGGLE_ITEM'; payload: string }
  | { type: 'SET_FILTER'; payload: State['filter'] }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, isLoading: true, error: null }
    case 'FETCH_SUCCESS':
      return { ...state, isLoading: false, items: action.payload }
    case 'FETCH_ERROR':
      return { ...state, isLoading: false, error: action.payload }
    case 'ADD_ITEM':
      return { ...state, items: [...state.items, action.payload] }
    case 'TOGGLE_ITEM':
      return {
        ...state,
        items: state.items.map(item =>
          item.id === action.payload
            ? { ...item, completed: !item.completed }
            : item
        ),
      }
    case 'SET_FILTER':
      return { ...state, filter: action.payload }
    default:
      return state
  }
}
```

### Context + useReducer

```tsx
interface TodoContextType {
  state: State
  dispatch: Dispatch<Action>
}

const TodoContext = createContext<TodoContextType | null>(null)

export function TodoProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, initialState)

  return (
    <TodoContext.Provider value={{ state, dispatch }}>
      {children}
    </TodoContext.Provider>
  )
}

export function useTodos() {
  const context = useContext(TodoContext)
  if (!context) throw new Error('useTodos must be used within TodoProvider')
  return context
}

// Usage
function TodoList() {
  const { state, dispatch } = useTodos()

  return (
    <ul>
      {state.items.map(item => (
        <li
          key={item.id}
          onClick={() => dispatch({ type: 'TOGGLE_ITEM', payload: item.id })}
        >
          {item.text}
        </li>
      ))}
    </ul>
  )
}
```

## Performance Patterns

### React.memo

```tsx
// Only re-renders when props change
const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
  return <div>{/* expensive render */}</div>
})

// Custom comparison
const UserCard = memo(
  function UserCard({ user }) {
    return <div>{user.name}</div>
  },
  (prevProps, nextProps) => prevProps.user.id === nextProps.user.id
)
```

### useMemo

```tsx
function DataTable({ data, sortKey }) {
  // Only recalculate when data or sortKey changes
  const sortedData = useMemo(() => {
    return [...data].sort((a, b) => a[sortKey].localeCompare(b[sortKey]))
  }, [data, sortKey])

  return (
    <table>
      {sortedData.map(row => (
        <tr key={row.id}>...</tr>
      ))}
    </table>
  )
}
```

### useCallback

```tsx
function ParentComponent() {
  const [count, setCount] = useState(0)

  // Stable reference - won't cause child re-renders
  const handleClick = useCallback(() => {
    console.log('clicked')
  }, [])

  // This callback depends on count
  const handleIncrement = useCallback(() => {
    setCount(c => c + 1)
  }, [])

  return (
    <>
      <ExpensiveChild onClick={handleClick} />
      <button onClick={handleIncrement}>Increment</button>
    </>
  )
}
```

### Code Splitting

```tsx
import { lazy, Suspense } from 'react'

// Lazy load components
const Dashboard = lazy(() => import('./Dashboard'))
const Settings = lazy(() => import('./Settings'))

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  )
}
```

### Virtualization

```tsx
import { useVirtualizer } from '@tanstack/react-virtual'

function VirtualList({ items }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  })

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            {items[virtualRow.index]}
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Error Handling

### Error Boundary

```tsx
import { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught:', error, errorInfo)
    // Send to error reporting service
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <DefaultErrorFallback error={this.state.error} />
    }
    return this.props.children
  }
}

// Usage
<ErrorBoundary fallback={<ErrorPage />}>
  <App />
</ErrorBoundary>
```

## Testing Patterns

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

describe('Counter', () => {
  it('increments count on click', async () => {
    const user = userEvent.setup()
    render(<Counter />)

    expect(screen.getByText('Count: 0')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: /increment/i }))

    expect(screen.getByText('Count: 1')).toBeInTheDocument()
  })

  it('fetches and displays data', async () => {
    render(<UserProfile userId="1" />)

    expect(screen.getByText(/loading/i)).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument()
    })
  })
})
```

## Best Practices

1. **Lift state up only when necessary** - colocate state with components that need it
2. **Prefer composition over prop drilling** - use compound components or context
3. **Memoize expensive computations** - but don't premature optimize
4. **Keep components focused** - single responsibility
5. **Use TypeScript** - for type safety and better DX
6. **Test behavior, not implementation** - use Testing Library

## Anti-Patterns to Avoid

```tsx
// Bad: useEffect for derived state
const [items, setItems] = useState([])
const [filteredItems, setFilteredItems] = useState([])
useEffect(() => {
  setFilteredItems(items.filter(i => i.active))
}, [items])

// Good: derive during render
const filteredItems = useMemo(
  () => items.filter(i => i.active),
  [items]
)

// Bad: Object/array as dependency
useEffect(() => {
  // Runs every render because {} !== {}
}, [{ id: 1 }])

// Bad: Fetching in useEffect without cleanup
useEffect(() => {
  fetchData().then(setData)
}, [])

// Good: With cleanup
useEffect(() => {
  let cancelled = false
  fetchData().then(data => {
    if (!cancelled) setData(data)
  })
  return () => { cancelled = true }
}, [])
```
