---
name: react-useeffect-best-practices
description: Use this skill when writing, reviewing, or refactoring React components that utilize useEffect, useState, or handle side effects, particularly for data fetching and state synchronization.
---

# React useEffect Best Practices

Effects are an escape hatch from React for synchronizing with external systems. Removing unnecessary Effects makes code easier to follow, faster to run, and less error-prone.

## When to Use Effects

- Synchronizing with external systems (non-React widgets, network, browser DOM)
- Analytics on component display
- Data fetching (with cleanup for race conditions)
- Subscriptions to external stores (use `useSyncExternalStore` when possible)

## When NOT to Use Effects

1. **Transforming data for rendering** - Calculate during render.
2. **Handling user events** - Use event handlers directly.
3. **Deriving state from props/state** - Compute it directly.
4. **Chaining state updates** - Calculate all next state in the event handler.
5. **Resetting state on prop change** - Use the `key` prop on components.

## Decision Tree

```
Need to respond to something?
├── User interaction (click, submit, drag)?
│   └── Use EVENT HANDLER
├── Component appeared on screen?
│   └── Use EFFECT (external sync, analytics)
├── Props/state changed and need derived value?
│   └── CALCULATE DURING RENDER
│       └── Expensive? Use useMemo
└── Need to reset state when prop changes?
    └── Use KEY PROP on component
```

## Anti-Patterns and Solutions

### 1. Derived State

```jsx
// ❌ Bad
const [fullName, setFullName] = useState("");
useEffect(() => {
   setFullName(firstName + " " + lastName);
}, [firstName, lastName]);

// ✅ Good - calculate during render
const fullName = firstName + " " + lastName;
```

### 2. Expensive Calculations

```jsx
// ❌ Bad
const [visibleTodos, setVisibleTodos] = useState([]);
useEffect(() => {
   setVisibleTodos(getFilteredTodos(todos, filter));
}, [todos, filter]);

// ✅ Good - useMemo for expensive operations
const visibleTodos = useMemo(
   () => getFilteredTodos(todos, filter),
   [todos, filter],
);
```

### 3. Reset State on Prop Change

```jsx
// ❌ Bad
useEffect(() => {
   setComment("");
}, [userId]);

// ✅ Good - use key to reset
<Profile userId={userId} key={userId} />;
```

### 4. Event-Specific Logic

```jsx
// ❌ Bad
useEffect(() => {
   if (product.isInCart) {
      showNotification("Added " + product.name + "!");
   }
}, [product]);

// ✅ Good - in event handler
function handleBuyClick() {
   addToCart(product);
   showNotification("Added " + product.name + "!");
}
```

### 5. Data Fetching with Race Conditions

```jsx
// ✅ Correct - cleanup ignores stale responses
useEffect(() => {
   let ignore = false;
   fetchResults(query).then((json) => {
      if (!ignore) setResults(json);
   });
   return () => {
      ignore = true;
   };
}, [query]);
```

## Quick Reference

| Scenario                | Solution                             |
| ----------------------- | ------------------------------------ |
| Transform data          | Calculate during render              |
| Expensive calculation   | `useMemo`                            |
| Reset all state on prop | `key` attribute                      |
| Adjust state on prop    | Derive during render                 |
| Share event logic       | Extract function, call from handlers |
| User events             | Event handlers                       |
| External system sync    | Effect                               |
| Notify parent           | Update in handler or lift state      |
| Init once               | Module-level or guard variable       |
| External store          | `useSyncExternalStore`               |
| Fetch data              | Effect with cleanup                  |