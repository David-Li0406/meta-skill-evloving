# State Management Patterns

## Critical: Immutable State Updates

React requires new object references to detect state changes. **Always create new arrays/objects** when updating state.

### ❌ Common Mistakes

```tsx
// Direct mutation - won't trigger re-render
containers.items.push(newItem);

// Modifying existing object - won't trigger re-render
const container = containers.find(c => c.id === targetId);
container.items.push(newItem);
```

### ✅ Correct Patterns

```tsx
// Create new array reference
setContainers(prev => prev.map(c =>
  c.id === targetId
    ? { ...c, items: [...c.items, newItem] }
    : c
));
```

## Complete DragEnd Handler

```tsx
const handleDragEnd = (event: DragEndEvent) => {
  const { active, over } = event;
  
  if (!over) return;

  const activeId = active.id.toString();
  const overId = over.id.toString();

  // Case 1: Reordering containers
  if (activeId.startsWith('container-') && overId.startsWith('container-')) {
    setContainers(prev => {
      const oldIndex = prev.findIndex(c => c.id === activeId);
      const newIndex = prev.findIndex(c => c.id === overId);
      return arrayMove(prev, oldIndex, newIndex);
    });
    return;
  }

  // Case 2: Reordering items within same container
  if (activeId.startsWith('item-') && overId.startsWith('item-')) {
    setContainers(prev => prev.map(container => {
      const activeItem = container.items.find(item => item.id === activeId);
      const overItem = container.items.find(item => item.id === overId);
      
      // Both items in this container
      if (activeItem && overItem) {
        const oldIndex = container.items.findIndex(i => i.id === activeId);
        const newIndex = container.items.findIndex(i => i.id === overId);
        
        return {
          ...container,
          items: arrayMove(container.items, oldIndex, newIndex)
        };
      }
      
      return container;
    }));
    return;
  }

  // Case 3: Moving item to different container
  if (activeId.startsWith('item-') && overId.startsWith('container-')) {
    setContainers(prev => {
      let itemToMove: Item | null = null;
      
      // Remove item from source container
      const afterRemoval = prev.map(container => {
        const item = container.items.find(i => i.id === activeId);
        if (item) {
          itemToMove = item;
          return {
            ...container,
            items: container.items.filter(i => i.id !== activeId)
          };
        }
        return container;
      });
      
      if (!itemToMove) return prev;
      
      // Add item to target container
      return afterRemoval.map(container => 
        container.id === overId
          ? { ...container, items: [...container.items, itemToMove!] }
          : container
      );
    });
  }
};
```

## State Structure Recommendations

### Basic Structure

```tsx
interface Item {
  id: string;
  content: string;
  // Additional item properties
}

interface Container {
  id: string;
  title: string;
  items: Item[];
  // Additional container properties
}

// State
const [containers, setContainers] = useState<Container[]>([]);
```

### With Optimistic Updates

```tsx
const [containers, setContainers] = useState<Container[]>([]);
const [isDragging, setIsDragging] = useState(false);

const handleDragStart = () => setIsDragging(true);
const handleDragEnd = (event: DragEndEvent) => {
  setIsDragging(false);
  // Handle state updates
};
```

## Performance Optimization

### Memoize Expensive Computations

```tsx
const containerIds = useMemo(
  () => containers.map(c => c.id),
  [containers]
);

const itemsByContainer = useMemo(
  () => containers.reduce((acc, container) => {
    acc[container.id] = container.items;
    return acc;
  }, {} as Record<string, Item[]>),
  [containers]
);
```

### Avoid Re-renders with React.memo

```tsx
const SortableItem = React.memo(({ item }: { item: Item }) => {
  // Component implementation
});

const SortableDroppableContainer = React.memo(({ 
  container 
}: { 
  container: Container 
}) => {
  // Component implementation
});
```

## Common Pitfalls

1. **Forgetting to spread arrays**: `[...container.items, newItem]` not `container.items.push(newItem)`
2. **Mutating nested objects**: Always spread objects at every level `{ ...container, items: [...container.items] }`
3. **Not checking for null**: Always verify `over` exists before accessing `over.id`
4. **Incorrect ID type checking**: Use `.toString().startsWith()` for reliable prefix checking

## Testing State Updates

```tsx
// Verify new reference is created
const beforeUpdate = containers;
setContainers(/* update */);
expect(containers).not.toBe(beforeUpdate); // Different reference

// Verify item was moved
expect(containers[0].items.length).toBe(2);
expect(containers[1].items.length).toBe(1);
expect(containers[1].items[0].id).toBe('item-1');
```
