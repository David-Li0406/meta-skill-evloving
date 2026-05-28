---
name: frontend-patterns
description: React component patterns, state management, accessibility, and frontend best practices. Use when building UI components or implementing client-side features.
---

# Frontend Patterns

Comprehensive patterns for React components, state management, accessibility, and modern frontend development.

## When to Use

- Building React components
- Managing client state
- Implementing user interactions
- Handling forms and validation
- Optimizing performance
- Ensuring accessibility

## Component Patterns

### Component Structure

```typescript
// ✅ CORRECT: Well-structured component
'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/Button'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'

interface MarketCardProps {
  id: string
  name: string
  description: string
  endDate: Date
  onBet?: (marketId: string, outcome: string) => void
}

export function MarketCard({
  id,
  name,
  description,
  endDate,
  onBet
}: MarketCardProps) {
  const [isLoading, setIsLoading] = useState(false)

  const handleBet = async (outcome: string) => {
    setIsLoading(true)
    try {
      await onBet?.(id, outcome)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="border rounded-lg p-4" data-testid="market-card">
      <h3 className="text-xl font-bold">{name}</h3>
      <p className="text-gray-600">{description}</p>
      <div className="mt-4 flex gap-2">
        <Button
          onClick={() => handleBet('yes')}
          disabled={isLoading}
          aria-label={`Bet yes on ${name}`}
        >
          {isLoading ? <LoadingSpinner /> : 'Yes'}
        </Button>
        <Button
          onClick={() => handleBet('no')}
          disabled={isLoading}
          aria-label={`Bet no on ${name}`}
        >
          {isLoading ? <LoadingSpinner /> : 'No'}
        </Button>
      </div>
    </div>
  )
}
```

### Compound Component Pattern

```typescript
// Flexible, composable components
interface TabsContextValue {
  activeTab: string
  setActiveTab: (tab: string) => void
}

const TabsContext = createContext<TabsContextValue | null>(null)

export function Tabs({ children, defaultTab }: {
  children: React.ReactNode
  defaultTab: string
}) {
  const [activeTab, setActiveTab] = useState(defaultTab)

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  )
}

export function TabList({ children }: { children: React.ReactNode }) {
  return <div className="tab-list" role="tablist">{children}</div>
}

export function Tab({ value, children }: {
  value: string
  children: React.ReactNode
}) {
  const context = useContext(TabsContext)
  if (!context) throw new Error('Tab must be used within Tabs')

  const { activeTab, setActiveTab } = context
  const isActive = activeTab === value

  return (
    <button
      role="tab"
      aria-selected={isActive}
      className={isActive ? 'tab-active' : 'tab'}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  )
}

export function TabPanel({ value, children }: {
  value: string
  children: React.ReactNode
}) {
  const context = useContext(TabsContext)
  if (!context) throw new Error('TabPanel must be used within Tabs')

  if (context.activeTab !== value) return null

  return <div role="tabpanel">{children}</div>
}

// Usage
<Tabs defaultTab="markets">
  <TabList>
    <Tab value="markets">Markets</Tab>
    <Tab value="portfolio">Portfolio</Tab>
    <Tab value="history">History</Tab>
  </TabList>

  <TabPanel value="markets">
    <MarketsList />
  </TabPanel>
  <TabPanel value="portfolio">
    <Portfolio />
  </TabPanel>
  <TabPanel value="history">
    <TransactionHistory />
  </TabPanel>
</Tabs>
```

### Custom Hooks Pattern

```typescript
// Reusable logic extraction
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}

// Usage
function SearchMarkets() {
  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounce(query, 500)

  useEffect(() => {
    if (debouncedQuery) {
      searchMarkets(debouncedQuery)
    }
  }, [debouncedQuery])

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="Search markets"
    />
  )
}
```

### Async State Management

```typescript
// useAsync hook for data fetching
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error }

export function useAsync<T>(asyncFn: () => Promise<T>, deps: any[] = []) {
  const [state, setState] = useState<AsyncState<T>>({ status: 'idle' })

  useEffect(() => {
    let cancelled = false

    setState({ status: 'loading' })

    asyncFn()
      .then(data => {
        if (!cancelled) {
          setState({ status: 'success', data })
        }
      })
      .catch(error => {
        if (!cancelled) {
          setState({ status: 'error', error })
        }
      })

    return () => {
      cancelled = true
    }
  }, deps)

  return state
}

// Usage
function MarketDetails({ id }: { id: string }) {
  const state = useAsync(() => fetchMarket(id), [id])

  if (state.status === 'loading') {
    return <LoadingSpinner />
  }

  if (state.status === 'error') {
    return <ErrorMessage error={state.error.message} />
  }

  if (state.status === 'success') {
    return <MarketCard {...state.data} />
  }

  return null
}
```

## State Management Patterns

### React Context for Global State

```typescript
// Context setup
interface AppContextValue {
  user: User | null
  setUser: (user: User | null) => void
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const AppContext = createContext<AppContextValue | null>(null)

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  useEffect(() => {
    // Persist theme
    localStorage.setItem('theme', theme)
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  return (
    <AppContext.Provider value={{ user, setUser, theme, toggleTheme }}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within AppProvider')
  }
  return context
}
```

### Zustand for Complex State

```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface CartStore {
  items: CartItem[]
  addItem: (item: CartItem) => void
  removeItem: (id: string) => void
  clearCart: () => void
  total: number
}

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (item) => set((state) => ({
        items: [...state.items, item]
      })),

      removeItem: (id) => set((state) => ({
        items: state.items.filter(item => item.id !== id)
      })),

      clearCart: () => set({ items: [] }),

      get total() {
        return get().items.reduce((sum, item) => sum + item.price, 0)
      }
    }),
    {
      name: 'cart-storage'
    }
  )
)

// Usage
function Cart() {
  const { items, removeItem, total } = useCartStore()

  return (
    <div>
      <h2>Cart Total: ${total}</h2>
      {items.map(item => (
        <div key={item.id}>
          <span>{item.name}</span>
          <button onClick={() => removeItem(item.id)}>Remove</button>
        </div>
      ))}
    </div>
  )
}
```

### React Query for Server State

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// Fetch markets
export function useMarkets() {
  return useQuery({
    queryKey: ['markets'],
    queryFn: async () => {
      const res = await fetch('/api/markets')
      if (!res.ok) throw new Error('Failed to fetch markets')
      return res.json()
    },
    staleTime: 1000 * 60 * 5 // 5 minutes
  })
}

// Create market mutation
export function useCreateMarket() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (market: MarketInput) => {
      const res = await fetch('/api/markets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(market)
      })
      if (!res.ok) throw new Error('Failed to create market')
      return res.json()
    },
    onSuccess: () => {
      // Invalidate markets query to refetch
      queryClient.invalidateQueries({ queryKey: ['markets'] })
    }
  })
}

// Usage
function MarketsList() {
  const { data, isLoading, error } = useMarkets()
  const createMarket = useCreateMarket()

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage error={error.message} />

  return (
    <div>
      <button onClick={() => createMarket.mutate({ name: 'New Market' })}>
        Create Market
      </button>
      {data.markets.map(market => (
        <MarketCard key={market.id} {...market} />
      ))}
    </div>
  )
}
```

## Form Patterns

### React Hook Form with Zod

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const CreateMarketSchema = z.object({
  name: z.string().min(3, 'Name must be at least 3 characters'),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  category: z.enum(['politics', 'sports', 'entertainment']),
  endDate: z.string().refine((date) => new Date(date) > new Date(), {
    message: 'End date must be in the future'
  })
})

type CreateMarketForm = z.infer<typeof CreateMarketSchema>

export function CreateMarketForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<CreateMarketForm>({
    resolver: zodResolver(CreateMarketSchema)
  })

  const onSubmit = async (data: CreateMarketForm) => {
    const res = await fetch('/api/markets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })

    if (!res.ok) {
      throw new Error('Failed to create market')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="name">Market Name</label>
        <input
          id="name"
          {...register('name')}
          aria-invalid={!!errors.name}
          aria-describedby={errors.name ? 'name-error' : undefined}
        />
        {errors.name && (
          <span id="name-error" className="error">
            {errors.name.message}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          {...register('description')}
          aria-invalid={!!errors.description}
        />
        {errors.description && (
          <span className="error">{errors.description.message}</span>
        )}
      </div>

      <div>
        <label htmlFor="category">Category</label>
        <select id="category" {...register('category')}>
          <option value="politics">Politics</option>
          <option value="sports">Sports</option>
          <option value="entertainment">Entertainment</option>
        </select>
      </div>

      <div>
        <label htmlFor="endDate">End Date</label>
        <input
          id="endDate"
          type="datetime-local"
          {...register('endDate')}
        />
        {errors.endDate && (
          <span className="error">{errors.endDate.message}</span>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating...' : 'Create Market'}
      </button>
    </form>
  )
}
```

## Accessibility Patterns

### Keyboard Navigation

```typescript
// ✅ CORRECT: Keyboard accessible dropdown
export function Dropdown({ items }: { items: string[] }) {
  const [isOpen, setIsOpen] = useState(false)
  const [activeIndex, setActiveIndex] = useState(0)

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'Escape':
        setIsOpen(false)
        break
      case 'ArrowDown':
        e.preventDefault()
        setActiveIndex((prev) => Math.min(prev + 1, items.length - 1))
        break
      case 'ArrowUp':
        e.preventDefault()
        setActiveIndex((prev) => Math.max(prev - 1, 0))
        break
      case 'Enter':
        e.preventDefault()
        // Select active item
        break
    }
  }

  return (
    <div onKeyDown={handleKeyDown}>
      <button
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        onClick={() => setIsOpen(!isOpen)}
      >
        Select Option
      </button>

      {isOpen && (
        <ul role="listbox" tabIndex={-1}>
          {items.map((item, index) => (
            <li
              key={item}
              role="option"
              aria-selected={index === activeIndex}
              className={index === activeIndex ? 'active' : ''}
            >
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
```

### ARIA Patterns

```typescript
// Modal with proper ARIA
export function Modal({ isOpen, onClose, children }: {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
}) {
  const modalRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (isOpen) {
      // Trap focus in modal
      modalRef.current?.focus()

      // Prevent body scroll
      document.body.style.overflow = 'hidden'
    }

    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      ref={modalRef}
      tabIndex={-1}
      onClick={onClose}
    >
      <div onClick={(e) => e.stopPropagation()}>
        <h2 id="modal-title">Modal Title</h2>
        <button
          onClick={onClose}
          aria-label="Close modal"
        >
          ×
        </button>
        {children}
      </div>
    </div>
  )
}
```

### Screen Reader Support

```typescript
// Loading state announcement
export function DataTable({ data, isLoading }: {
  data: any[]
  isLoading: boolean
}) {
  return (
    <div>
      {/* Screen reader announcement */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {isLoading ? 'Loading data...' : `${data.length} items loaded`}
      </div>

      <table>
        <caption className="sr-only">Data table</caption>
        <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Value</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id}>
              <td>{row.name}</td>
              <td>{row.value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

## Performance Patterns

### Code Splitting

```typescript
// Lazy load components
import dynamic from 'next/dynamic'

const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <LoadingSpinner />,
  ssr: false // Don't render on server
})

// Usage
export function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <HeavyChart data={data} />
    </div>
  )
}
```

### Memoization

```typescript
import { memo, useMemo, useCallback } from 'react'

// Memoize expensive computations
function MarketsList({ markets }: { markets: Market[] }) {
  const sortedMarkets = useMemo(() => {
    return [...markets].sort((a, b) =>
      b.createdAt.getTime() - a.createdAt.getTime()
    )
  }, [markets])

  const handleFilter = useCallback((category: string) => {
    // Filter logic
  }, [])

  return (
    <div>
      {sortedMarkets.map(market => (
        <MemoizedMarketCard key={market.id} {...market} />
      ))}
    </div>
  )
}

// Memoize component
const MemoizedMarketCard = memo(MarketCard, (prev, next) => {
  return prev.id === next.id && prev.updatedAt === next.updatedAt
})
```

### Virtual Scrolling

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'

export function VirtualList({ items }: { items: any[] }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Estimated height of each item
    overscan: 5 // Render 5 extra items
  })

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative'
        }}
      >
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualRow.start}px)`
            }}
          >
            {items[virtualRow.index].name}
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Best Practices

- **Component Design**: Small, focused, reusable components
- **State Management**: Use appropriate tool (Context, Zustand, React Query)
- **Accessibility**: ARIA labels, keyboard navigation, screen reader support
- **Performance**: Memoization, code splitting, virtual scrolling
- **Forms**: React Hook Form + Zod for validation
- **Testing**: Unit tests with React Testing Library
- **TypeScript**: Strict types, no `any`
- **CSS**: Tailwind for utility-first styling
- **Error Boundaries**: Catch React errors gracefully
- **Loading States**: Always show loading/error states
