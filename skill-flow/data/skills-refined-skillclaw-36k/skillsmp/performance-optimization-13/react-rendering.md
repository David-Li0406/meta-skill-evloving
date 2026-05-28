# React Rendering Optimization

## React Compiler (Project Default)

This project has React Compiler enabled. The compiler automatically:
- Memoizes components
- Optimizes re-renders
- Handles dependency tracking

**Manual optimization is only needed for:**
1. External library callbacks
2. Complex context values
3. Computations > 100ms
4. Third-party integrations

## Identifying Re-render Issues

### Using React DevTools Profiler

1. Open React DevTools
2. Go to Profiler tab
3. Record an interaction
4. Look for:
   - Components rendering > 16ms
   - Components re-rendering unnecessarily
   - Deep component trees updating

### Common Re-render Causes

| Cause | Detection | Solution |
|-------|-----------|----------|
| New object/array each render | Profiler shows unnecessary renders | Move outside or memoize |
| Context changes | All consumers re-render | Split context, memoize value |
| Parent re-render | Children re-render | Use composition, memo |
| State too high | Unrelated siblings re-render | Lift state down |

## Optimization Patterns

### Pattern 1: Avoid Inline Objects

```typescript
// ❌ Bad: New object every render
function Button() {
  return <div style={{ color: "red" }}>Click</div>;
}

// ✅ Good: Stable reference
const buttonStyle = { color: "red" };

function Button() {
  return <div style={buttonStyle}>Click</div>;
}

// ✅ Good: Tailwind (no object)
function Button() {
  return <div className="text-red-500">Click</div>;
}
```

### Pattern 2: Avoid Inline Functions

```typescript
// ❌ Bad: New function every render (problem with external libs)
<ExternalLibComponent onEvent={() => doSomething()} />

// ✅ Good: Stable callback for external libraries
const handleEvent = useCallback(() => {
  doSomething();
}, []);

<ExternalLibComponent onEvent={handleEvent} />
```

### Pattern 3: Derived State

```typescript
// ❌ Bad: Filtering in render
function List({ items }) {
  const filtered = items.filter(x => x.active);  // Every render!
  return <ul>{filtered.map(...)}</ul>;
}

// ✅ Good: With React Compiler - usually automatic
// Manual only if verified slow:
function List({ items }) {
  const filtered = useMemo(
    () => items.filter(x => x.active),
    [items]
  );
  return <ul>{filtered.map(...)}</ul>;
}
```

### Pattern 4: Context Optimization

```typescript
// ❌ Bad: Everything re-renders on any change
const AppContext = createContext({ user: null, theme: "light", locale: "en" });

// ✅ Good: Split by update frequency
const UserContext = createContext(null);
const ThemeContext = createContext("light");
const LocaleContext = createContext("en");

// ✅ Good: Memoize context value
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState("light");

  const value = useMemo(() => ({
    theme,
    setTheme
  }), [theme]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}
```

### Pattern 5: Component Composition

```typescript
// ❌ Bad: Parent state causes all children to re-render
function Parent() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <ExpensiveChild />  {/* Re-renders on count change! */}
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
    </div>
  );
}

// ✅ Good: Isolate state
function Parent() {
  return (
    <div>
      <ExpensiveChild />  {/* Doesn't re-render */}
      <Counter />
    </div>
  );
}

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### Pattern 6: List Virtualization

For lists with 50+ items:

```typescript
import { useVirtualizer } from "@tanstack/react-virtual";

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,  // Row height
    overscan: 5  // Render 5 extra items for smooth scrolling
  });

  return (
    <div
      ref={parentRef}
      className="h-[400px] overflow-auto"
    >
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: "relative"
        }}
      >
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.key}
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`
            }}
          >
            <ListItem item={items[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Pattern 7: Defer Non-Urgent Updates

```typescript
import { startTransition, useDeferredValue } from "react";

function SearchResults({ query }) {
  // Defer the expensive filtering
  const deferredQuery = useDeferredValue(query);
  const results = useSearchResults(deferredQuery);

  return (
    <div>
      {query !== deferredQuery && <LoadingIndicator />}
      <ResultsList results={results} />
    </div>
  );
}

// Or with startTransition
function handleSearch(query: string) {
  // Urgent: Update input immediately
  setInputValue(query);

  // Non-urgent: Update results with lower priority
  startTransition(() => {
    setSearchResults(filterResults(query));
  });
}
```

## Server Components Optimization

### Stream Heavy Components

```typescript
import { Suspense } from "react";

export default function Page() {
  return (
    <div>
      {/* Immediate */}
      <Header />

      {/* Streamed */}
      <Suspense fallback={<TableSkeleton />}>
        <DataTable />
      </Suspense>

      {/* Streamed independently */}
      <Suspense fallback={<ChartSkeleton />}>
        <Analytics />
      </Suspense>
    </div>
  );
}
```

### Parallel Data Fetching

```typescript
// ❌ Bad: Sequential (waterfall)
async function Page() {
  const user = await getUser();
  const posts = await getPosts(user.id);
  const comments = await getComments(posts[0].id);
  return <Content user={user} posts={posts} comments={comments} />;
}

// ✅ Good: Parallel where possible
async function Page() {
  const user = await getUser();

  // These can run in parallel
  const [posts, notifications] = await Promise.all([
    getPosts(user.id),
    getNotifications(user.id)
  ]);

  return <Content user={user} posts={posts} notifications={notifications} />;
}
```

## Anti-Patterns

### Don't Over-Memoize

```typescript
// ❌ Bad: Memoizing cheap operations
const formatted = useMemo(() => date.toLocaleDateString(), [date]);

// ✅ Good: Just compute it (React Compiler handles this)
const formatted = date.toLocaleDateString();
```

### Don't Premature Optimize

```typescript
// ❌ Bad: Optimizing without measuring
const MemoizedComponent = memo(SimpleComponent);

// ✅ Good: Profile first, optimize verified bottlenecks
// Use React DevTools Profiler to identify slow components
```

### Don't Nest Providers Unnecessarily

```typescript
// ❌ Bad: Deep nesting
<Provider1>
  <Provider2>
    <Provider3>
      <Provider4>
        <App />
      </Provider4>
    </Provider3>
  </Provider2>
</Provider1>

// ✅ Good: Compose providers
function Providers({ children }) {
  return (
    <Provider1>
      <Provider2>
        {children}
      </Provider2>
    </Provider1>
  );
}
```
