---
title: State Management
impact: HIGH
impactDescription: Memory efficiency and render optimization
tags: state, react, hooks, context
---

# State Management

Efficient state organization and management patterns.

## Rule 1: Colocate State with Usage

```typescript
// ❌ INCORRECT - state too high, causes unnecessary re-renders
function App() {
  const [isModalOpen, setIsModalOpen] = useState(false)
  return (
    <Layout>
      <Sidebar />
      <Content>
        <DeepChild isModalOpen={isModalOpen} setIsModalOpen={setIsModalOpen} />
      </Content>
    </Layout>
  )
}

// ✅ CORRECT - state near where it's used
function DeepChild() {
  const [isModalOpen, setIsModalOpen] = useState(false)
  return (
    <>
      <Button onClick={() => setIsModalOpen(true)}>Open</Button>
      <Modal open={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </>
  )
}
```

## Rule 2: Split State by Update Frequency

```typescript
// ❌ INCORRECT - all state together, updates everything
const [state, setState] = useState({
  user: null,           // rarely changes
  theme: 'dark',        // rarely changes
  mousePosition: { x: 0, y: 0 }  // changes constantly
})

// ✅ CORRECT - independent state
const [user, setUser] = useState(null)
const [theme, setTheme] = useState('dark')
const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
```

## Rule 3: Use Reducers for Complex State

```typescript
// ❌ INCORRECT - multiple related state updates
const [items, setItems] = useState([])
const [loading, setLoading] = useState(false)
const [error, setError] = useState(null)

const fetchItems = async () => {
  setLoading(true)
  setError(null)
  try {
    const data = await api.getItems()
    setItems(data)
  } catch (e) {
    setError(e)
  } finally {
    setLoading(false)
  }
}

// ✅ CORRECT - reducer for coordinated updates
const [state, dispatch] = useReducer(itemsReducer, { items: [], loading: false, error: null })

const fetchItems = async () => {
  dispatch({ type: 'FETCH_START' })
  try {
    const data = await api.getItems()
    dispatch({ type: 'FETCH_SUCCESS', payload: data })
  } catch (error) {
    dispatch({ type: 'FETCH_ERROR', payload: error })
  }
}
```

## Rule 4: Context Splitting for Performance

```typescript
// ❌ INCORRECT - one context, all consumers re-render
const AppContext = createContext({ user: null, theme: 'dark', notifications: [] })

// ✅ CORRECT - split contexts by update frequency
const UserContext = createContext(null)
const ThemeContext = createContext('dark')
const NotificationsContext = createContext([])

function Providers({ children }) {
  return (
    <UserProvider>
      <ThemeProvider>
        <NotificationsProvider>
          {children}
        </NotificationsProvider>
      </ThemeProvider>
    </UserProvider>
  )
}
```

## Rule 5: Derive State When Possible

```typescript
// ❌ INCORRECT - redundant state
const [items, setItems] = useState([])
const [filteredItems, setFilteredItems] = useState([])
const [filter, setFilter] = useState('')

useEffect(() => {
  setFilteredItems(items.filter(i => i.name.includes(filter)))
}, [items, filter])

// ✅ CORRECT - derive from existing state
const [items, setItems] = useState([])
const [filter, setFilter] = useState('')

const filteredItems = useMemo(
  () => items.filter(i => i.name.includes(filter)),
  [items, filter]
)
```

## Rule 6: Use Refs for Non-Rendering Values

```typescript
// ❌ INCORRECT - state causes re-render
const [renderCount, setRenderCount] = useState(0)
useEffect(() => {
  setRenderCount(c => c + 1)  // triggers another render!
})

// ✅ CORRECT - ref doesn't cause re-render
const renderCount = useRef(0)
useEffect(() => {
  renderCount.current += 1
})
```
