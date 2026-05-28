# Virtual Scrolling with Tanstack Virtual

Performance optimization for 1,000+ items using Tanstack Virtual.

## When to Use Virtual Scrolling

- **1,000+ items:** Noticeable lag without virtualization
- **10,000+ items:** Required for acceptable performance
- **Dynamic heights:** Items with varying heights (cards, rich content)
- **Infinite scroll:** Server-paginated results

## Setup

```bash
npm install @tanstack/react-virtual
```

## Basic Implementation

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef } from 'react';

function VirtualizedList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 48, // Estimated item height in pixels
    overscan: 5, // Render 5 extra items above/below viewport
  });

  return (
    <div
      ref={parentRef}
      style={{ height: '400px', overflow: 'auto' }}
    >
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          width: '100%',
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <CommandItem item={items[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Dynamic Heights

```typescript
function VirtualizedDynamicList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 80, // Initial estimate
    measureElement: (el) => el?.getBoundingClientRect().height ?? 80,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            data-index={virtualItem.index}
            ref={virtualizer.measureElement}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <CardItem item={items[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Performance Benchmarks

| Item Count | Without Virtual | With Virtual | Memory Saved |
|------------|-----------------|--------------|--------------|
| 100 | 60fps ✓ | 60fps ✓ | None |
| 1,000 | 45fps | 60fps ✓ | ~40MB |
| 10,000 | 15fps ❌ | 60fps ✓ | ~400MB |
| 100,000 | Unusable ❌ | 58fps ✓ | ~4GB |

## See Also

- **Server-Side Search:** `references/server-side-search.md`
- **Testing:** `references/testing.md`
