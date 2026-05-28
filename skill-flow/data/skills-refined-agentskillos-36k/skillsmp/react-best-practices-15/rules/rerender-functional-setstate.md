---
title: Use Functional setState Updates
impact: MEDIUM
impactDescription: prevents stale closures and unnecessary callback recreations
tags: rerender, setstate, closures, hooks
---

## Use Functional setState Updates

When updating state based on the current state value, use the functional update form of setState instead of directly referencing the state variable. This prevents stale closures, eliminates unnecessary dependencies, and creates stable callback references.

**Incorrect (requires state as dependency):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  const addItems = useCallback((newItems: Item[]) => {
    setItems([...items, ...newItems])
  }, [items])
  
  const removeItem = useCallback((id: string) => {
    setItems(items.filter(item => item.id !== id))
  }, [])
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

The first callback is recreated every time `items` changes, which can cause child components to re-render unnecessarily. The second callback has a stale closure bug—it will always reference the initial `items` value.

**Correct (stable callbacks, no stale closures):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  const addItems = useCallback((newItems: Item[]) => {
    setItems(prev => [...prev, ...newItems])
  }, [])
  
  const removeItem = useCallback((id: string) => {
    setItems(prev => prev.filter(item => item.id !== id))
  }, [])
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

**Benefits:**

1. **Stable callback references** - Callbacks don't need to be recreated when state changes
2. **No stale closures** - Always operates on the latest state value
3. **Fewer dependencies** - Simplifies dependency arrays and reduces memory leaks
4. **Prevents bugs** - Eliminates the most common source of React closure bugs

**When to use functional updates:**

- Any setState that depends on the current state value
- Inside useCallback/useMemo when state is needed
- Event handlers that reference state
- Async operations that update state

**When direct updates are fine:**

- Setting state to a static value: `setCount(0)`
- Setting state from props/arguments only: `setName(newName)`
- State doesn't depend on previous value
