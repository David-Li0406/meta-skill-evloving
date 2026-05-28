# Command Palette Layouts

Detailed implementation guides for all five layout patterns with responsive strategies and code examples.

## Layout Selection Guide

| Layout | Best For | Performance | Complexity |
|--------|----------|-------------|------------|
| Single-Column | Basic commands, mobile, simplicity | Excellent (2k-3k items) | Low |
| Two-Column | Files, docs, preview needed | Good (1k-2k items) | Medium |
| Multi-Panel | Filters, tables, admin panels | Good (500-1k items) | High |
| Card Grid | Extensions, visual content | Fair (100-500 items) | Medium |
| Horizontal Cards | Mixed content types | Good (1k items) | High |

Choose based on:
1. **Data richness** - Text-only → Single column; Rich metadata → Cards
2. **Preview needs** - Need details → Two-column; No preview → Single
3. **Filtering** - Complex filters → Multi-panel; Simple search → Single
4. **Mobile support** - Must work on mobile → Single column
5. **Item count** - 1000+ items → Enable virtual scrolling

## Single-Column List

### When to Use

- **Primary use case:** Simple action palette, navigation commands
- **Best for:** Text-heavy commands without rich metadata
- **Mobile:** Excellent (works well on all screen sizes)
- **Examples:** VS Code command palette, basic GitHub search

### Structure

```tsx
<Command>
  <Command.Input placeholder="Search commands..." />
  <Command.List>
    <Command.Group heading="Recent">
      <Command.Item>Create Task</Command.Item>
      <Command.Item>Navigate Home</Command.Item>
    </Command.Group>
    <Command.Group heading="Actions">
      <Command.Item>Deploy Production</Command.Item>
      <Command.Item>Run Tests</Command.Item>
    </Command.Group>
  </Command.List>
</Command>
```

### Styling Approach

```css
/* Single column takes full palette width */
.command-list {
  width: 100%;
  max-height: 400px;
  overflow-y: auto;
}

.command-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
}

.command-item[aria-selected="true"] {
  background: var(--palette-selection-bg);
}
```

### Generator Command

```bash
./scripts/create-palette-layout.sh \
  --layout single-column \
  --name ActionPalette
```

### Virtual Scrolling

For 1,000+ items, enable virtual scrolling:

```bash
./scripts/create-palette-layout.sh \
  --layout single-column \
  --name ActionPalette \
  --virtualized
```

See `references/virtual-scrolling.md` for performance details.

## Two-Column with Preview

### When to Use

- **Primary use case:** File browsers, document search, repository pickers
- **Best for:** Items with rich details needing preview
- **Mobile:** Poor (collapses to single column on mobile)
- **Examples:** Raycast file search, GitHub repository picker, VS Code file switcher

### Structure

```tsx
<div className="two-column-palette">
  <Command className="left-pane">
    <Command.Input />
    <Command.List>
      <Command.Item onSelect={(item) => setPreview(item)}>
        File.tsx
      </Command.Item>
    </Command.List>
  </Command>

  <div className="right-pane preview-panel">
    {preview ? (
      <FilePreview file={preview} />
    ) : (
      <div className="empty-preview">
        Select a file to preview
      </div>
    )}
  </div>
</div>
```

### Sizing Strategy

**Desktop (≥768px):**
- Left pane: 320-400px fixed width
- Right pane: Flex grow (remaining space)
- Total width: 800-1000px

**Tablet (≥640px, <768px):**
- Left pane: 40% width
- Right pane: 60% width
- Total width: 600-800px

**Mobile (<640px):**
- Collapse to single column
- Show preview as modal on item select
- Or: Show preview below list

```css
.two-column-palette {
  display: flex;
  gap: 1px; /* Separator line */
  width: 900px;
  max-width: 90vw;
}

.left-pane {
  flex: 0 0 380px;
  border-right: 1px solid var(--palette-border);
}

.right-pane {
  flex: 1;
  min-width: 400px;
  padding: 16px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .two-column-palette {
    flex-direction: column;
  }

  .left-pane {
    flex: 0 0 auto;
    border-right: none;
    border-bottom: 1px solid var(--palette-border);
  }

  .right-pane {
    flex: 0 0 300px;
  }
}
```

### Preview Update Pattern

```typescript
const [selectedItem, setSelectedItem] = useState<Item | null>(null);
const [preview, setPreview] = useState<PreviewData | null>(null);

// Update preview when selection changes
useEffect(() => {
  if (!selectedItem) {
    setPreview(null);
    return;
  }

  // Lazy load preview data
  loadPreview(selectedItem.id).then(setPreview);
}, [selectedItem]);

// Or for instant preview of cached data:
function handleSelect(item: Item) {
  setSelectedItem(item);
  setPreview(item.cachedPreview || null);
}
```

### Generator Command

```bash
./scripts/create-palette-layout.sh \
  --layout two-column \
  --name FileSearch \
  --with-preview
```

## Multi-Panel Layout

### When to Use

- **Primary use case:** Complex filtering, data tables, admin dashboards
- **Best for:** Many filter options + results + detailed view
- **Mobile:** Poor (requires desktop)
- **Examples:** AWS console, admin panels, advanced search interfaces

### Structure

```tsx
<div className="multi-panel-palette">
  {/* Left: Filters/Categories */}
  <aside className="filter-panel">
    <FilterGroup title="Category">
      <FilterOption>All</FilterOption>
      <FilterOption>Users</FilterOption>
      <FilterOption>Posts</FilterOption>
    </FilterGroup>
    <FilterGroup title="Status">
      <FilterOption>Active</FilterOption>
      <FilterOption>Pending</FilterOption>
    </FilterGroup>
  </aside>

  {/* Center: Search + Results */}
  <Command className="results-panel">
    <Command.Input />
    <Command.List>
      {/* Filtered results */}
    </Command.List>
  </Command>

  {/* Right: Details */}
  <aside className="details-panel">
    <DetailView item={selected} />
  </aside>
</div>
```

### Panel Sizing

**Desktop:**
- Left (filters): 220-260px fixed
- Center (results): Flex grow, min 400px
- Right (details): 320-400px fixed
- Total: 1200-1400px

**Responsive collapse:**
```
Desktop (≥1200px): [Filters] [Results] [Details]
Tablet (≥768px):   [Results with toggle filters] [Details]
Mobile (<768px):   [Results only, modals for filters/details]
```

```css
.multi-panel-palette {
  display: grid;
  grid-template-columns: 240px 1fr 360px;
  gap: 1px;
  width: 1280px;
  max-width: 95vw;
  background: var(--palette-separator);
}

@media (max-width: 1200px) {
  .multi-panel-palette {
    grid-template-columns: 1fr 360px;
  }

  .filter-panel {
    display: none; /* Show as overlay/drawer */
  }
}

@media (max-width: 768px) {
  .multi-panel-palette {
    grid-template-columns: 1fr;
  }

  .details-panel {
    display: none; /* Show as modal on select */
  }
}
```

### State Management

```typescript
interface MultiPanelState {
  filters: {
    category: string[];
    status: string[];
    dateRange: [Date, Date] | null;
  };
  selectedItem: Item | null;
  resultsView: 'list' | 'grid';
}

function useMultiPanel() {
  const [state, setState] = useState<MultiPanelState>({
    filters: { category: [], status: [], dateRange: null },
    selectedItem: null,
    resultsView: 'list',
  });

  const filteredResults = useMemo(() => {
    return items.filter(item => {
      if (state.filters.category.length &&
          !state.filters.category.includes(item.category)) {
        return false;
      }
      // Apply other filters...
      return true;
    });
  }, [items, state.filters]);

  return { state, setState, filteredResults };
}
```

### Generator Command

```bash
./scripts/create-palette-layout.sh \
  --layout multi-panel \
  --name AdminSearch
```

## Card Grid Layout

### When to Use

- **Primary use case:** Extensions store, plugin browser, visual galleries
- **Best for:** Items with images, rich metadata, badges
- **Mobile:** Fair (responsive grid)
- **Examples:** Raycast Store, Figma plugins, Chrome extensions

### Structure

```tsx
<Command>
  <Command.Input />
  <Command.List className="card-grid">
    <Command.Item value="plugin-1" asChild>
      <div className="card">
        <img src={icon} className="card-icon" />
        <h3 className="card-title">Plugin Name</h3>
        <p className="card-description">Description text</p>
        <div className="card-metadata">
          <Badge>80.9k downloads</Badge>
          <Badge>★ 4.8</Badge>
        </div>
      </div>
    </Command.Item>
  </Command.List>
</Command>
```

### Grid Responsive Behavior

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  padding: 16px;
  max-height: 600px;
  overflow-y: auto;
}

@media (max-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
}

@media (max-width: 640px) {
  .card-grid {
    grid-template-columns: 1fr; /* Single column on mobile */
  }
}
```

### Card Component

```tsx
interface CardProps {
  icon: string;
  title: string;
  description: string;
  downloads?: number;
  rating?: number;
  isNew?: boolean;
}

function Card({ icon, title, description, downloads, rating, isNew }: CardProps) {
  return (
    <div className="card">
      <div className="card-header">
        <img src={icon} alt="" className="card-icon" />
        {isNew && <Badge variant="success">New</Badge>}
      </div>

      <h3 className="card-title">{title}</h3>
      <p className="card-description">{description}</p>

      <div className="card-footer">
        {downloads && (
          <span className="card-stat">
            <DownloadIcon /> {formatNumber(downloads)}
          </span>
        )}
        {rating && (
          <span className="card-stat">
            <StarIcon /> {rating.toFixed(1)}
          </span>
        )}
      </div>
    </div>
  );
}
```

### Virtual Scrolling for Card Grids

For 100+ cards, enable virtual scrolling with dynamic column count:

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualCardGrid({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const columnCount = useColumnCount(); // Responsive: 1, 2, 3, or 4

  const rowVirtualizer = useVirtualizer({
    count: Math.ceil(items.length / columnCount),
    getScrollElement: () => parentRef.current,
    estimateSize: () => 280, // Card height + gap
  });

  return (
    <div ref={parentRef} className="virtual-card-grid">
      <div style={{ height: `${rowVirtualizer.getTotalSize()}px` }}>
        {rowVirtualizer.getVirtualItems().map((virtualRow) => {
          const startIndex = virtualRow.index * columnCount;
          const rowItems = items.slice(startIndex, startIndex + columnCount);

          return (
            <div key={virtualRow.key} className="card-row">
              {rowItems.map(item => <Card key={item.id} {...item} />)}
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

### Generator Command

```bash
./scripts/create-palette-layout.sh \
  --layout card-grid \
  --name StorePalette \
  --virtualized
```

## Horizontal Cards + Lists

### When to Use

- **Primary use case:** Mixed content types, contextual grouped results
- **Best for:** Combining recent items (cards) with all results (list)
- **Mobile:** Good (cards scroll horizontally, list stacks)
- **Examples:** Linear command palette, Notion's recent + all pages

### Structure

```tsx
<Command>
  <Command.Input />
  <Command.List>
    {/* Horizontal scrolling cards section */}
    <div className="horizontal-section">
      <h3 className="section-title">Pending Requests (10)</h3>
      <div className="horizontal-scroll">
        <Card />
        <Card />
        <Card />
      </div>
    </div>

    {/* Vertical list section */}
    <Command.Group heading="Shortcuts">
      <Command.Item>Go to Dashboard</Command.Item>
      <Command.Item>Go to Team</Command.Item>
    </Command.Group>

    <Command.Group heading="Actions">
      <Command.Item>Assign Task</Command.Item>
      <Command.Item>View Report</Command.Item>
    </Command.Group>
  </Command.List>
</Command>
```

### Horizontal Scroll Implementation

```css
.horizontal-section {
  padding: 8px 16px;
  border-bottom: 1px solid var(--palette-border);
}

.horizontal-scroll {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 8px 0 12px 0;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch; /* Smooth iOS scroll */
}

.horizontal-scroll::-webkit-scrollbar {
  height: 6px;
}

.horizontal-card {
  flex: 0 0 280px;
  scroll-snap-align: start;
  border: 1px solid var(--palette-border);
  border-radius: 8px;
  padding: 16px;
}

@media (max-width: 640px) {
  .horizontal-card {
    flex: 0 0 240px; /* Narrower on mobile */
  }
}
```

### Keyboard Navigation Challenge

**Problem:** Mixing horizontal (cards) and vertical (list) navigation.

**Solution 1:** Tab key switches between sections:
```
Tab          → Enter cards section
Arrow Right  → Navigate cards
Tab          → Enter list section
Arrow Down   → Navigate list
```

**Solution 2:** Cards are non-interactive until selected:
```
Arrow Down  → Skip over card section entirely
Enter       → Expand card section for navigation
```

**Recommended:** Solution 1 with visual focus indicators.

### Generator Command

```bash
./scripts/create-palette-layout.sh \
  --layout horizontal-cards \
  --name MixedPalette
```

## Responsive Strategy Summary

| Layout | Desktop | Tablet | Mobile |
|--------|---------|--------|--------|
| Single-Column | Full width | Full width | Full width |
| Two-Column | Side-by-side | Side-by-side | Stacked |
| Multi-Panel | 3 panels | 2 panels | 1 panel + modals |
| Card Grid | 3-4 columns | 2 columns | 1 column |
| Horizontal | Cards + List | Cards + List | Cards scroll |

### Breakpoint Recommendations

```typescript
const breakpoints = {
  mobile: 640,
  tablet: 768,
  desktop: 1024,
  wide: 1280,
};

function useLayout() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  if (width < breakpoints.mobile) return 'mobile';
  if (width < breakpoints.tablet) return 'tablet';
  if (width < breakpoints.desktop) return 'desktop';
  return 'wide';
}
```

## Performance Benchmarks

| Layout | Rendering (60fps) | Virtual Scroll Threshold | Memory Impact |
|--------|-------------------|--------------------------|---------------|
| Single-Column | 2,000-3,000 items | >1,000 items | Low |
| Two-Column | 1,000-2,000 items | >800 items | Medium |
| Multi-Panel | 500-1,000 items | >500 items | High |
| Card Grid | 100-500 items | >100 items | High |
| Horizontal | 1,000 items | >500 items | Medium |

Enable virtual scrolling when approaching threshold.

See `references/virtual-scrolling.md` for implementation.

## Additional Resources

- **Virtual Scrolling:** `references/virtual-scrolling.md`
- **Theming:** `references/theming.md`
- **Keyboard Navigation:** `references/keyboard-navigation.md`
- **State Management:** `references/state-management.md`
