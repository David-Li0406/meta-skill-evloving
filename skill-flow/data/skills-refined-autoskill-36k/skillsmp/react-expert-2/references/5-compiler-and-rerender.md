# 5. React Compiler & Re-render Optimization

**Impact: MEDIUM-HIGH**

The React Compiler (Forget) automates most memoization, but it requires code to follow specific safety rules to work effectively.

## 5.1 The React Compiler "Forget-Friendly" Rules

**Impact: CRITICAL (enables auto-memoization)**

The compiler automatically applies `useMemo` and `useCallback` logic. To ensure it works:
1.  **Keep Components Pure**: Don't mutate objects/arrays passed as props.
2.  **No Side Effects in Render**: `console.log` is fine, but don't set timeouts or change global state during render.
3.  **Explicit Hook Order**: Hooks must follow the same order on every render.

**Check if the compiler is working**: Use the "React DevTools" and look for the "Memo ✨" badge next to components.

## 5.2 Manual Optimization (When the Compiler Fails)

Even with the compiler, some patterns are still needed for extreme performance.

### 5.2.1 Defer State Reads to Usage Point

Don't subscribe to dynamic state if you only read it inside callbacks.

**Incorrect: re-renders on every query change**

```tsx
function SearchButton() {
  const [query] = useAtom(searchAtom); // Subscribes to changes
  
  const handleClick = () => {
    goToSearch(query);
  };

  return <button onClick={handleClick}>Search</button>;
}
```

**Correct: reads on demand, no subscription**

```tsx
function SearchButton() {
  const handleClick = () => {
    // Read from the store's non-reactive getter
    const query = searchStore.get(); 
    goToSearch(query);
  };

  return <button onClick={handleClick}>Search</button>;
}
```

### 5.2.2 Transitions for Non-Urgent Updates

Use `startTransition` for updates that don't need immediate feedback (like filtering a long list).

```tsx
const [isPending, startTransition] = useTransition();

const handleFilter = (e) => {
  startTransition(() => {
    setFilter(e.target.value);
  });
};
```

## 5.3 Narrow Effect Dependencies

Specify primitive dependencies instead of objects to minimize effect re-runs if the compiler cannot verify object stability.

```tsx
// Better
useEffect(() => {
  track(user.id);
}, [user.id]);

// Worse
useEffect(() => {
  track(user.id);
}, [user]);
```
