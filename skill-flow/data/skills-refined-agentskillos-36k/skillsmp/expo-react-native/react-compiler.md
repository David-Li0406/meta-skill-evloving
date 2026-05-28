# React Compiler Patterns

## Setup

Enable in `app.json`:
```json
{ "expo": { "experiments": { "reactCompiler": true } } }
```

Or via `babel.config.js`:
```js
module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [['babel-plugin-react-compiler', { target: '19' }]],
  };
};
```

## What It Does

The compiler automatically:
- Memoizes component outputs (replaces `React.memo`)
- Memoizes callback functions (replaces `useCallback`)
- Memoizes computed values (replaces `useMemo`)

## Modern Code Pattern

```tsx
// ✅ No manual memoization needed
export function ProductList({ products }: { products: Product[] }) {
  // Automatically memoized
  const sortedProducts = products
    .filter(p => p.inStock)
    .sort((a, b) => a.price - b.price);

  // Automatically memoized
  const handlePress = (id: string) => console.log('Pressed:', id);

  return (
    <FlashList
      data={sortedProducts}
      renderItem={({ item }) => <ProductItem item={item} onPress={handlePress} />}
      estimatedItemSize={80}
    />
  );
}

// ✅ No React.memo wrapper needed
function ProductItem({ item, onPress }: ProductItemProps) {
  return (
    <TouchableOpacity onPress={() => onPress(item.id)}>
      <Text>{item.name}</Text>
    </TouchableOpacity>
  );
}
```

## When Manual Memoization Is Still Needed

**External dependencies** not visible to the compiler:
```tsx
const fetchData = useCallback(async () => {
  return await api.getData();
}, []);
```

**Referential equality requirements** in third-party libraries:
```tsx
const config = useMemo(() => ({
  apiKey: process.env.API_KEY,
  timeout: 5000
}), []);
```

**Performance-critical computations**:
```tsx
const result = useMemo(() => 
  hugeDataset.map(expensiveTransform),
[hugeDataset]);
```

## Best Practices

- Default to no memoization—let the compiler handle it
- Profile first—only add manual memoization for measured issues
- Use React DevTools Profiler to identify bottlenecks
- Remove unnecessary `React.memo`, `useCallback`, `useMemo` from existing code
