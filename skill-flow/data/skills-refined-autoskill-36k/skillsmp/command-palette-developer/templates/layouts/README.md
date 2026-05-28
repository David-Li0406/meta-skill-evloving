# Command Palette Layout Components

Five flexible, production-ready layout components for organizing command results in command palettes.

## Components Overview

### 1. SingleColumnLayout

**Best for:** Simple action palettes, navigation commands, text-heavy lists

**Features:**
- Full-width command list with group headers
- Item height: 48px with padding
- Hover and selected states
- Keyboard navigation (↑↓, Enter)
- Icons on left, shortcuts on right
- Max height: 400px with auto-scroll
- Optional virtual scrolling for 1000+ items

**Usage:**
```tsx
import { SingleColumnLayout } from './layouts';

const commands = [
  { id: '1', label: 'Create Task', group: 'Actions', icon: <PlusIcon /> },
  { id: '2', label: 'Navigate Home', group: 'Navigation', shortcut: '⌘H' },
];

<SingleColumnLayout
  items={commands}
  onSelect={(item) => console.log('Selected:', item)}
  virtualScroll={false}
/>
```

### 2. TwoColumnLayout

**Best for:** File browsers, document search, repository pickers

**Features:**
- Split view: 40% list | 60% preview (configurable)
- List shows items, preview shows details
- Optional resize handle
- Responsive: stacks on mobile (<768px)
- Smooth transition (150ms) on preview change

**Usage:**
```tsx
import { TwoColumnLayout } from './layouts';

<TwoColumnLayout
  items={files}
  onSelect={(file) => openFile(file)}
  renderPreview={(file) => (
    file ? <FilePreview file={file} /> : <EmptyState />
  )}
  defaultSplit={40}
  resizable={true}
/>
```

### 3. MultiPanelLayout

**Best for:** Complex filtering, data tables, admin dashboards

**Features:**
- Three panels: filters (25%) | results (50%) | details (25%)
- Filter panel with checkboxes and radio groups
- Collapsible side panels
- Responsive: collapses to modals on mobile
- Panel state persisted in localStorage

**Usage:**
```tsx
import { MultiPanelLayout } from './layouts';

const filters = [
  {
    id: 'category',
    label: 'Category',
    type: 'checkbox',
    options: [
      { id: 'users', label: 'Users', count: 45 },
      { id: 'posts', label: 'Posts', count: 123 },
    ],
    value: ['users'],
  },
];

<MultiPanelLayout
  items={results}
  filters={filters}
  onFilterChange={(id, value) => updateFilter(id, value)}
  renderDetails={(item) => item && <ItemDetails item={item} />}
  onSelect={(item) => console.log('Selected:', item)}
/>
```

### 4. CardGridLayout

**Best for:** Extension stores, plugin browsers, visual galleries

**Features:**
- Responsive grid: 1-4 columns based on width
- Card size: min 200px × 180px
- Grid gap: 16px
- Card hover: shadow + scale(1.02)
- Card selected: accent border (2px)
- Grid-aware keyboard navigation (arrow keys)
- Image thumbnail support

**Usage:**
```tsx
import { CardGridLayout } from './layouts';

const plugins = [
  {
    id: '1',
    title: 'ESLint',
    description: 'Find and fix problems in your JavaScript code',
    image: '/icons/eslint.png',
    badges: [<Badge>Popular</Badge>],
    metadata: { downloads: '10M', rating: '4.8' },
  },
];

<CardGridLayout
  items={plugins}
  columns={3} // or omit for auto-responsive
  onSelect={(plugin) => installPlugin(plugin)}
/>
```

### 5. HorizontalCardsLayout

**Best for:** Mixed content types, recent items, contextual results

**Features:**
- Horizontal scrolling cards
- Card width: 280px, height: 120px
- Snap-to-card scrolling
- Navigation dots indicator
- Left/right arrow buttons
- Keyboard: left/right arrows
- Selected card centered in viewport

**Usage:**
```tsx
import { HorizontalCardsLayout } from './layouts';

<HorizontalCardsLayout
  items={recentItems}
  onSelect={(item) => openItem(item)}
  showDots={true}
  showArrows={true}
/>
```

## Type Definitions

### Command (SingleColumnLayout, TwoColumnLayout, MultiPanelLayout)

```typescript
interface Command {
  id: string;
  label: string;
  description?: string;
  group?: string;
  icon?: React.ReactNode;
  shortcut?: string;
  disabled?: boolean;
}
```

### CardItem (CardGridLayout, HorizontalCardsLayout)

```typescript
interface CardItem {
  id: string;
  title: string;
  description?: string;
  image?: string;
  icon?: React.ReactNode;
  badges?: React.ReactNode[];
  metadata?: Record<string, React.ReactNode>;
  disabled?: boolean;
}
```

### Filter (MultiPanelLayout)

```typescript
interface Filter {
  id: string;
  label: string;
  type: 'checkbox' | 'radio';
  options: FilterOption[];
  value?: string | string[];
}

interface FilterOption {
  id: string;
  label: string;
  count?: number;
}
```

## Keyboard Navigation

All layouts support comprehensive keyboard navigation:

| Key | Action |
|-----|--------|
| ↑ / ↓ | Navigate items vertically |
| ← / → | Navigate items horizontally (grid/horizontal layouts) |
| Enter | Select/execute current item |
| Home | Jump to first item |
| End | Jump to last item |
| Tab | Move to next interactive element |

## Accessibility Features

All layouts include:
- ARIA roles and attributes (role="listbox", aria-selected, etc.)
- Keyboard navigation support
- Focus management
- Screen reader announcements
- High contrast support via CSS variables

## CSS Variables

Customize appearance using CSS variables:

```css
:root {
  --palette-bg: #ffffff;
  --palette-bg-secondary: #f9fafb;
  --palette-text: #111827;
  --palette-text-muted: #6b7280;
  --palette-text-disabled: #9ca3af;
  --palette-border: #e5e7eb;
  --palette-separator: #e5e7eb;
  --palette-selection-bg: #eff6ff;
  --palette-selection-text: #1e40af;
  --palette-accent: #3b82f6;
}
```

## Performance Considerations

- **SingleColumnLayout:** Handles 2000-3000 items before virtual scroll needed
- **TwoColumnLayout:** Handles 1000-2000 items efficiently
- **MultiPanelLayout:** Handles 500-1000 items (more complex rendering)
- **CardGridLayout:** Handles 100-500 items (rich cards)
- **HorizontalCardsLayout:** Handles 1000+ items (uses CSS scroll snap)

Enable virtual scrolling for larger datasets when available.

## Browser Support

All components work in:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Mobile Safari and Chrome tested on iOS and Android.

## Examples

See the reference documentation for complete implementation examples:
- `references/layouts.md` - Detailed implementation guides
- `references/design-principles.md` - UX patterns and best practices
- `references/keyboard-navigation.md` - Grid navigation patterns
