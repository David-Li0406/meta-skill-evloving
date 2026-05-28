---
title: Re-render Prevention
impact: HIGH
impactDescription: 2-10x render performance improvement
tags: performance, react, hooks, memo
---

# Re-render Prevention

Minimize unnecessary component re-renders.

## Rule 1: Memoize Expensive Computations

```typescript
// ❌ INCORRECT - sorts on every render
function UserList({ users }) {
  const sortedUsers = users.sort((a, b) => a.name.localeCompare(b.name))
  return <List items={sortedUsers} />
}

// ✅ CORRECT - only sorts when users change
function UserList({ users }) {
  const sortedUsers = useMemo(
    () => [...users].sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <List items={sortedUsers} />
}
```

## Rule 2: Stable Callback References

```typescript
// ❌ INCORRECT - new function every render, child re-renders
function Parent({ id }) {
  return <Child onClick={() => handleClick(id)} />
}

// ✅ CORRECT - stable reference
function Parent({ id }) {
  const handleChildClick = useCallback(() => handleClick(id), [id])
  return <Child onClick={handleChildClick} />
}
```

## Rule 3: Extract Static JSX

```typescript
// ❌ INCORRECT - header recreated every render
function Dashboard({ data }) {
  return (
    <div>
      <header>
        <h1>Dashboard</h1>
        <nav>...</nav>
      </header>
      <Content data={data} />
    </div>
  )
}

// ✅ CORRECT - static header extracted
const DashboardHeader = () => (
  <header>
    <h1>Dashboard</h1>
    <nav>...</nav>
  </header>
)

function Dashboard({ data }) {
  return (
    <div>
      <DashboardHeader />
      <Content data={data} />
    </div>
  )
}
```

## Rule 4: Use React.memo for Pure Components

```typescript
// ❌ INCORRECT - re-renders when parent re-renders
function ExpensiveList({ items }) {
  return items.map(item => <ExpensiveItem key={item.id} item={item} />)
}

// ✅ CORRECT - only re-renders when items change
const ExpensiveList = memo(function ExpensiveList({ items }) {
  return items.map(item => <ExpensiveItem key={item.id} item={item} />)
})
```

## Rule 5: Avoid Object/Array Literals in JSX

```typescript
// ❌ INCORRECT - new object every render
<Component style={{ color: 'red' }} />
<Component items={[1, 2, 3]} />

// ✅ CORRECT - stable references
const style = { color: 'red' }
const items = [1, 2, 3]
<Component style={style} />
<Component items={items} />

// ✅ OR use useMemo for dynamic values
const style = useMemo(() => ({ color: theme.primary }), [theme.primary])
```

## Rule 6: Use Children Pattern for Stable References

```typescript
// ❌ INCORRECT - content re-renders when Provider updates
function App() {
  return (
    <ThemeProvider>
      <ExpensiveComponent />
    </ThemeProvider>
  )
}

// ✅ CORRECT - children don't re-render on context change
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light')
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}
```
