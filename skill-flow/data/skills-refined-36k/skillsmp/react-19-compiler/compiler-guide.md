# React Compiler Guide

## What Does React Compiler Do?

React Compiler automatically optimizes your React application at build time by handling memoization that would otherwise need to be done manually.

**Key benefits:**
- Eliminates need for manual `useMemo()`, `useCallback()`, `React.memo()`
- Applies optimizations automatically during build
- Reduces boilerplate and maintenance burden
- Prevents dependency-related bugs in manual implementations

## Before and After

### Without Compiler (Manual Memoization)

```typescript
import { memo, useCallback, useMemo } from "react";

interface Props {
  data: Item[];
  onClick: (id: string) => void;
}

const ExpensiveComponent = memo(function ExpensiveComponent({
  data,
  onClick
}: Props) {
  const processedData = useMemo(
    () => expensiveProcessing(data),
    [data]
  );

  const handleClick = useCallback(
    (item: Item) => onClick(item.id),
    [onClick]
  );

  return (
    <div>
      {processedData.map(item => (
        <Item
          key={item.id}
          onClick={() => handleClick(item)}
        />
      ))}
    </div>
  );
});
```

### With Compiler (Automatic Optimization)

```typescript
interface Props {
  data: Item[];
  onClick: (id: string) => void;
}

// ✅ Clean, simple code - compiler handles optimization
function ExpensiveComponent({ data, onClick }: Props) {
  const processedData = expensiveProcessing(data);

  const handleClick = (item: Item) => {
    onClick(item.id);
  };

  return (
    <div>
      {processedData.map(item => (
        <Item
          key={item.id}
          onClick={() => handleClick(item)}
        />
      ))}
    </div>
  );
}
```

## How It Works

React Compiler runs at build time and:

1. **Analyzes components** - Understands data flow and dependencies
2. **Identifies opportunities** - Finds values and callbacks that benefit from memoization
3. **Applies optimizations** - Inserts memoization automatically
4. **Ensures correctness** - Uses the same semantics as manual memoization

## What Gets Optimized

The compiler optimizes:

| Pattern | Manual Code | Compiler Handles |
|---------|-------------|------------------|
| Expensive computations | `useMemo(() => compute(a), [a])` | ✅ Automatically |
| Callback references | `useCallback((x) => fn(x), [fn])` | ✅ Automatically |
| Component re-renders | `memo(Component)` | ✅ Automatically |
| Object/array literals | `useMemo(() => ({ a, b }), [a, b])` | ✅ Automatically |

## Verifying Compiler Is Active

### Check in Development

In the browser console, you should see React DevTools indicating the compiler is active. Components will show optimization status.

### Check Build Output

```bash
npm run build
# Look for compiler transformation messages in output
```

## ESLint Integration

The compiler comes with ESLint rules to help migration:

```javascript
// eslint.config.js
import reactCompiler from "eslint-plugin-react-compiler";

export default [
  {
    plugins: {
      "react-compiler": reactCompiler
    },
    rules: {
      "react-compiler/react-compiler": "error"
    }
  }
];
```

### Key Lint Rules

| Rule | Purpose |
|------|---------|
| `preserve-manual-memoization` | Warns when manual memoization is unnecessary |
| `rules-of-hooks` | Ensures hooks are used correctly |

## Common Patterns

### Sorting and Filtering

```typescript
// ✅ Let compiler optimize
function ProductList({ products, sortBy, filterBy }: Props) {
  const filtered = products.filter(p => p.category === filterBy);
  const sorted = [...filtered].sort((a, b) => a[sortBy] - b[sortBy]);

  return (
    <ul>
      {sorted.map(product => (
        <ProductItem key={product.id} product={product} />
      ))}
    </ul>
  );
}
```

### Event Handlers

```typescript
// ✅ Inline handlers are fine with compiler
function ButtonGroup({ items, onSelect }: Props) {
  return (
    <div>
      {items.map(item => (
        <button
          key={item.id}
          onClick={() => onSelect(item.id)}  // ✅ No useCallback needed
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}
```

### Derived State

```typescript
// ✅ Computed values are automatically memoized
function Dashboard({ data }: Props) {
  const total = data.reduce((sum, item) => sum + item.value, 0);
  const average = total / data.length;
  const max = Math.max(...data.map(d => d.value));

  return (
    <div>
      <Stat label="Total" value={total} />
      <Stat label="Average" value={average} />
      <Stat label="Max" value={max} />
    </div>
  );
}
```

## Debugging Optimization

If you suspect the compiler isn't optimizing something:

1. **Check React DevTools** - Shows if component is memoized
2. **Add console.log** - See if computation runs unnecessarily
3. **Check ESLint** - Look for compiler warnings

```typescript
function Component({ data }: Props) {
  console.log("Component render");  // Debug: Check render frequency

  const processed = expensiveProcess(data);
  console.log("Processing done");   // Debug: Should not run every render

  return <div>{processed}</div>;
}
```

## Limitations

The compiler cannot optimize:

1. **External state managers** with non-React state (MobX, etc.)
2. **Imperative DOM manipulation** using refs
3. **Code that breaks Rules of Hooks**
4. **Dynamic hook calls** (conditional hooks)

For these cases, you may still need manual optimization.

## Best Practices

1. **Write clean, simple code first** - Don't pre-optimize
2. **Trust the compiler** - It handles most cases
3. **Profile before optimizing** - Only add manual memoization when proven needed
4. **Document exceptions** - When manual memoization is needed, explain why
5. **Keep components small** - Smaller components = better optimization opportunities
