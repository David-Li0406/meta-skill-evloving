# Performance Optimization

## FlashList (Recommended for Large Lists)

FlashList uses cell recycling instead of virtualization—up to 10x faster than FlatList.

```tsx
import { FlashList } from '@shopify/flash-list';

function ProductList({ products }: { products: Product[] }) {
  const handlePress = (id: string) => console.log('Pressed:', id);

  return (
    <FlashList
      data={products}
      renderItem={({ item }) => <ProductItem item={item} onPress={handlePress} />}
      estimatedItemSize={80}
      keyExtractor={(item) => item.id}
    />
  );
}

function ProductItem({ item, onPress }: ProductItemProps) {
  return (
    <TouchableOpacity onPress={() => onPress(item.id)}>
      <Text>{item.name}</Text>
    </TouchableOpacity>
  );
}
```

## FlatList Optimization

When FlashList isn't needed:
```tsx
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={(item) => item.id}
  initialNumToRender={10}
  maxToRenderPerBatch={5}
  windowSize={5}
  removeClippedSubviews={true}
  getItemLayout={(_, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>
```

## Legacy Memoization

With React Compiler enabled, manual memoization is rarely needed. Use only for:
- External side effects not visible to the compiler
- Third-party libraries requiring referential equality
- Explicit performance control in critical paths

```tsx
// Memoize components (usually not needed)
const MemoizedItem = React.memo(({ item }: { item: Item }) => (
  <View><Text>{item.name}</Text></View>
));

// Memoize callbacks (usually not needed)
const handlePress = useCallback((id: string) => {
  // handler logic
}, []);

// Memoize expensive computations (usually not needed)
const processedData = useMemo(() => 
  data.filter(item => item.active).sort((a, b) => a.order - b.order),
[data]);
```

## Best Practices
- Enable React Compiler for automatic optimization
- Use FlashList for 500+ items or complex layouts
- Default to no manual memoization
- Use `getItemLayout` when item heights are fixed
- Profile first—only add manual memoization for measured issues
