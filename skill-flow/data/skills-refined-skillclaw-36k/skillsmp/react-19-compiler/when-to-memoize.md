# When to Manually Memoize (With React Compiler)

## Overview

With React Compiler enabled, **you can remove most manual memoization**. However, there are specific scenarios where manual optimization is still beneficial or necessary.

## Decision Tree

```
Does React Compiler handle this case?
│
├─ YES (most cases) → Remove manual memoization
│
└─ NO → Consider manual memoization:
    │
    ├─ External library requiring stable reference?
    │   → useCallback with dependency comment
    │
    ├─ Context value causing cascade re-renders?
    │   → useMemo for context value
    │
    └─ Extremely expensive computation (>100ms)?
        → useMemo with performance comment
```

## When to Keep Manual Memoization

### 1. External Library Callbacks

Non-React code may depend on stable function references:

```typescript
import { useCallback, useEffect } from "react";
import { externalLibrary } from "some-library";

function MapComponent({ markers, onMarkerClick }: Props) {
  // ✅ Keep: External library expects stable callback
  const handleMarkerClick = useCallback(
    (marker: Marker) => {
      onMarkerClick(marker.id);
    },
    [onMarkerClick]
  );

  useEffect(() => {
    // External library that doesn't integrate with React
    externalLibrary.setMarkerClickHandler(handleMarkerClick);
  }, [handleMarkerClick]);

  return <div id="map" />;
}
```

### 2. Complex Context Values

When context updates frequently and triggers many re-renders:

```typescript
import { createContext, useMemo, useState } from "react";

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>("light");
  const [fontSize, setFontSize] = useState<number>(16);

  // ✅ Keep: Prevents all consumers from re-rendering
  const contextValue = useMemo(
    () => ({
      theme,
      fontSize,
      setTheme,
      setFontSize,
      toggleTheme: () => setTheme(t => t === "light" ? "dark" : "light")
    }),
    [theme, fontSize]
  );

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
}
```

### 3. Extremely Expensive Computations

When computation takes >100ms and runs frequently:

```typescript
import { useMemo } from "react";

function DataVisualization({ rawData }: Props) {
  // ✅ Keep: Complex statistical analysis (documented reason)
  const analysis = useMemo(() => {
    // This takes ~200ms for large datasets
    return performComplexStatisticalAnalysis(rawData);
  }, [rawData]);

  return <Chart data={analysis} />;
}
```

### 4. Subscription Handlers

When subscribing to external stores:

```typescript
import { useCallback, useEffect } from "react";
import { websocket } from "~/lib/websocket";

function LiveFeed({ channelId, onMessage }: Props) {
  // ✅ Keep: Prevents re-subscription on every render
  const handleMessage = useCallback(
    (message: Message) => {
      onMessage(message);
    },
    [onMessage]
  );

  useEffect(() => {
    const unsubscribe = websocket.subscribe(channelId, handleMessage);
    return unsubscribe;
  }, [channelId, handleMessage]);

  return <Feed channelId={channelId} />;
}
```

## When to Remove Manual Memoization

### 1. Simple Event Handlers

```typescript
// ❌ Remove: Compiler handles this
function Button({ onClick }: Props) {
  const handleClick = useCallback(() => {
    onClick();
  }, [onClick]);

  return <button onClick={handleClick}>Click</button>;
}

// ✅ Better: Clean code
function Button({ onClick }: Props) {
  return <button onClick={onClick}>Click</button>;
}
```

### 2. Derived Values

```typescript
// ❌ Remove: Compiler handles this
function ProductCard({ product }: Props) {
  const formattedPrice = useMemo(
    () => formatCurrency(product.price),
    [product.price]
  );

  return <Card>{formattedPrice}</Card>;
}

// ✅ Better: Clean code
function ProductCard({ product }: Props) {
  const formattedPrice = formatCurrency(product.price);
  return <Card>{formattedPrice}</Card>;
}
```

### 3. Sorting and Filtering

```typescript
// ❌ Remove: Compiler handles this
function List({ items, sortBy }: Props) {
  const sorted = useMemo(
    () => [...items].sort((a, b) => a[sortBy] - b[sortBy]),
    [items, sortBy]
  );

  return <ul>{sorted.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}

// ✅ Better: Clean code
function List({ items, sortBy }: Props) {
  const sorted = [...items].sort((a, b) => a[sortBy] - b[sortBy]);
  return <ul>{sorted.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}
```

### 4. React.memo Wrappers

```typescript
// ❌ Remove: Compiler handles component memoization
const ExpensiveList = memo(function ExpensiveList({ items }: Props) {
  return (
    <ul>
      {items.map(item => <ListItem key={item.id} item={item} />)}
    </ul>
  );
});

// ✅ Better: Let compiler decide
function ExpensiveList({ items }: Props) {
  return (
    <ul>
      {items.map(item => <ListItem key={item.id} item={item} />)}
    </ul>
  );
}
```

## Documentation Pattern

When you keep manual memoization, document why:

```typescript
import { useMemo, useCallback } from "react";

function AdvancedComponent({ data, externalHandler }: Props) {
  // Manual memoization: Required for external D3.js library
  // that expects stable callback reference
  const handleDataPoint = useCallback(
    (point: DataPoint) => externalHandler(point),
    [externalHandler]
  );

  // Manual memoization: Computation takes ~150ms for datasets
  // larger than 10,000 items
  const processedData = useMemo(
    () => heavyDataProcessing(data),
    [data]
  );

  return <D3Chart data={processedData} onPointClick={handleDataPoint} />;
}
```

## Performance Profiling

Before adding manual memoization, profile first:

```typescript
import { Profiler } from "react";

function App() {
  const handleRender = (
    id: string,
    phase: "mount" | "update",
    actualDuration: number
  ) => {
    console.log(`${id} ${phase}: ${actualDuration}ms`);
  };

  return (
    <Profiler id="MyComponent" onRender={handleRender}>
      <MyComponent />
    </Profiler>
  );
}
```

**Rule of thumb**: Only add manual memoization if profiling shows a component:
- Renders frequently (>10 times per second)
- Takes >16ms to render (blocking frame)
- Has expensive computations (>100ms)

## Summary Table

| Scenario | Keep Memoization? | Reason |
|----------|-------------------|--------|
| Simple derived values | ❌ No | Compiler handles |
| Event handlers | ❌ No | Compiler handles |
| Sorting/filtering arrays | ❌ No | Compiler handles |
| React.memo wrappers | ❌ No | Compiler handles |
| External library callbacks | ✅ Yes | Non-React code |
| Context provider values | ✅ Yes | Prevents cascading re-renders |
| Computations >100ms | ✅ Yes | Documented performance need |
| Subscription handlers | ✅ Yes | Prevents re-subscription |
