# Base Command Palette Components

Production-ready, copy-paste command palette components with keyboard navigation, fuzzy search, and full accessibility support.

## Overview

This directory contains four foundational command palette components:

1. **BaseCommandPalette** - Shared component logic (internal use)
2. **CommandPaletteModal** - Modal dialog variant (⌘K standard)
3. **CommandPaletteEmbedded** - Floating palette with smart positioning
4. **CommandPaletteDrawer** - Slide-in panel from any edge

## Features

- ✅ **Keyboard Navigation** - Arrow keys, Enter, Escape
- ✅ **Fuzzy Search** - Built-in with cmdk
- ✅ **Focus Management** - Auto-focus, focus trap, restore focus
- ✅ **Accessibility** - ARIA labels, screen reader support
- ✅ **Theming** - Dark/light mode via CSS variables
- ✅ **Responsive** - Mobile-friendly with touch support
- ✅ **Animations** - Smooth fade/slide with reduced motion support
- ✅ **TypeScript** - Full type safety, no any types

## Installation

```bash
npm install cmdk @floating-ui/react
```

## Quick Start

### Modal Variant (⌘K Pattern)

```tsx
import { useState } from 'react';
import { CommandPaletteModal, useCommandPaletteShortcut } from './base';

const commands = [
  {
    id: 'create-task',
    label: 'Create Task',
    description: 'Create a new task',
    icon: '✅',
    shortcut: 'command+n',
    group: 'Actions',
  },
  {
    id: 'navigate-home',
    label: 'Go to Home',
    description: 'Navigate to home page',
    icon: '🏠',
    group: 'Navigation',
  },
];

export function App() {
  const [isOpen, setIsOpen] = useState(false);

  // Trigger with ⌘K
  useCommandPaletteShortcut(() => setIsOpen(true));

  const handleSelect = (command) => {
    console.log('Selected:', command);
    // Execute command action
  };

  return (
    <CommandPaletteModal
      isOpen={isOpen}
      onOpenChange={setIsOpen}
      commands={commands}
      onSelect={handleSelect}
      placeholder="Search commands..."
    />
  );
}
```

### Embedded Variant (Floating)

```tsx
import { CommandPaletteEmbedded, useEmbeddedPalette } from './base';

export function ToolbarWithPalette() {
  const { triggerRef, isOpen, setIsOpen } = useEmbeddedPalette();

  return (
    <>
      <button ref={triggerRef} onClick={() => setIsOpen(true)}>
        Commands ⌘K
      </button>

      <CommandPaletteEmbedded
        triggerRef={triggerRef}
        isOpen={isOpen}
        onOpenChange={setIsOpen}
        placement="bottom-start"
        commands={commands}
        onSelect={handleSelect}
      />
    </>
  );
}
```

### Drawer Variant (Slide-in Panel)

```tsx
import { CommandPaletteDrawer, useDrawer } from './base';

export function AppWithDrawer() {
  const drawer = useDrawer();

  return (
    <>
      <button onClick={drawer.open}>
        Open Commands
      </button>

      <CommandPaletteDrawer
        isOpen={drawer.isOpen}
        onOpenChange={drawer.setIsOpen}
        position="right" // left, right, top, bottom
        commands={commands}
        onSelect={handleSelect}
      />
    </>
  );
}
```

## Component API

### CommandItem

```typescript
interface CommandItem {
  id: string;              // Unique identifier
  label: string;           // Display label
  description?: string;    // Optional muted description
  icon?: React.ReactNode;  // Icon component or emoji
  shortcut?: string;       // e.g., "command+s"
  group?: string;          // Group name for organization
  keywords?: string[];     // Search keywords
  badge?: string;          // Optional badge (e.g., "New")
}
```

### CommandPaletteModal

Modal dialog centered on screen with backdrop.

```typescript
interface CommandPaletteModalProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  commands?: CommandItem[];
  groups?: CommandGroup[];
  onSelect: (command: CommandItem) => void;
  placeholder?: string;
  footer?: React.ReactNode;
  emptyState?: React.ReactNode;
  isLoading?: boolean;
  maxHeight?: string;
  showKeyboardLegend?: boolean;
  backdropBlur?: boolean;
  animationDuration?: number;
}
```

**Props:**
- `isOpen` - Control open state
- `onOpenChange` - Callback when state changes
- `commands` - Flat array of commands
- `groups` - Alternative: grouped commands
- `onSelect` - Called when command selected
- `showKeyboardLegend` - Show footer legend (default: true)
- `backdropBlur` - Blur effect on backdrop (default: true)
- `animationDuration` - Animation duration ms (default: 300)

### CommandPaletteEmbedded

Floating palette with smart positioning via Floating UI.

```typescript
interface CommandPaletteEmbeddedProps extends BaseProps {
  triggerRef?: React.RefObject<HTMLElement>;
  placement?: Placement; // e.g., "bottom-start"
  offsetDistance?: number;
  showArrow?: boolean;
  maxWidth?: number;
}
```

**Props:**
- `triggerRef` - Ref to trigger element
- `placement` - Position relative to trigger (default: "bottom-start")
- `offsetDistance` - Distance from trigger (default: 8px)
- `showArrow` - Show arrow pointer (default: true)
- `maxWidth` - Maximum width in pixels (default: 400)

### CommandPaletteDrawer

Slide-in panel from any edge.

```typescript
type DrawerPosition = 'left' | 'right' | 'top' | 'bottom';

interface CommandPaletteDrawerProps extends BaseProps {
  position?: DrawerPosition;
  width?: string;
  height?: string;
  showCloseButton?: boolean;
  showDragHandle?: boolean;
}
```

**Props:**
- `position` - Edge to slide from (default: "right")
- `width` - Width for left/right (default: "400px")
- `height` - Height for top/bottom (default: "60vh")
- `showCloseButton` - Show X button (default: true)
- `showDragHandle` - Show drag handle (default: true)

## Keyboard Shortcuts

All variants support:

| Key | Action |
|-----|--------|
| ⌘K / Ctrl+K | Toggle open/close |
| ↑ / ↓ | Navigate results |
| Enter | Execute selected command |
| ESC | Close palette |
| Tab / Shift+Tab | Navigate interactive elements |

## Theming

Components use CSS variables for theming. Define these in your global CSS:

```css
:root {
  /* Backgrounds */
  --palette-bg: #ffffff;
  --palette-bg-secondary: #f9fafb;
  --palette-selection-bg: #eff6ff;
  --palette-hover-bg: #f3f4f6;

  /* Text */
  --palette-text: #111827;
  --palette-text-muted: #6b7280;
  --palette-text-placeholder: #9ca3af;

  /* Borders */
  --palette-border: #e5e7eb;
  --palette-separator: #f3f4f6;

  /* Accents */
  --palette-accent: #3b82f6;
  --palette-accent-hover: #2563eb;

  /* Shadows */
  --palette-shadow: rgba(0, 0, 0, 0.1);
  --palette-shadow-lg: rgba(0, 0, 0, 0.15);

  /* Shortcuts */
  --palette-shortcut-bg: #f3f4f6;
  --palette-shortcut-text: #374151;
  --palette-shortcut-border: #d1d5db;
}

[data-theme="dark"] {
  --palette-bg: #1f2937;
  --palette-bg-secondary: #111827;
  --palette-selection-bg: #374151;
  --palette-hover-bg: #2d3748;
  --palette-text: #f9fafb;
  --palette-text-muted: #9ca3af;
  --palette-border: #374151;
  --palette-accent: #60a5fa;
  --palette-shadow: rgba(0, 0, 0, 0.3);
  --palette-shortcut-bg: #374151;
  --palette-shortcut-text: #d1d5db;
  --palette-shortcut-border: #4b5563;
}
```

## Accessibility

- **ARIA Labels** - All interactive elements labeled
- **Keyboard Navigation** - Full keyboard support
- **Focus Management** - Focus trap, auto-focus input
- **Screen Readers** - Status announcements for results
- **Reduced Motion** - Respects `prefers-reduced-motion`
- **Color Contrast** - WCAG AA compliant

## Advanced Usage

### Grouped Commands

```tsx
const groups = [
  {
    id: 'actions',
    label: 'Actions',
    commands: [
      { id: 'create', label: 'Create Task', icon: '✅' },
      { id: 'delete', label: 'Delete Task', icon: '🗑️' },
    ],
  },
  {
    id: 'navigation',
    label: 'Navigation',
    commands: [
      { id: 'home', label: 'Go to Home', icon: '🏠' },
      { id: 'settings', label: 'Settings', icon: '⚙️' },
    ],
  },
];

<CommandPaletteModal
  groups={groups}
  onSelect={handleSelect}
/>
```

### Custom Empty State

```tsx
const emptyState = (
  <div style={{ padding: '24px', textAlign: 'center' }}>
    <p>No commands found</p>
    <button onClick={clearFilters}>Clear filters</button>
  </div>
);

<CommandPaletteModal
  emptyState={emptyState}
  onSelect={handleSelect}
/>
```

### Loading State

```tsx
<CommandPaletteModal
  isLoading={isLoadingCommands}
  commands={commands}
  onSelect={handleSelect}
/>
```

### Custom Footer

```tsx
const footer = (
  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
    <span>↑↓ navigate</span>
    <span>↵ select</span>
    <button onClick={openHelp}>Help</button>
  </div>
);

<CommandPaletteModal
  footer={footer}
  onSelect={handleSelect}
/>
```

## Testing

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CommandPaletteModal } from './base';

test('opens on command+k', async () => {
  const user = userEvent.setup();
  const { container } = render(<App />);

  await user.keyboard('{Meta>}k{/Meta}');

  expect(screen.getByRole('dialog')).toBeInTheDocument();
});

test('filters commands by search', async () => {
  const user = userEvent.setup();
  render(<CommandPaletteModal isOpen commands={commands} />);

  const input = screen.getByPlaceholderText('Search commands...');
  await user.type(input, 'create');

  expect(screen.getByText('Create Task')).toBeInTheDocument();
  expect(screen.queryByText('Delete Task')).not.toBeInTheDocument();
});
```

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- iOS Safari 14+
- Chrome Android 90+

## Dependencies

- `cmdk` - Command palette primitive with fuzzy search
- `@floating-ui/react` - Smart positioning for embedded variant
- `react` 18+
- `react-dom` 18+

## File Structure

```
base/
├── BaseCommandPalette.tsx      # Shared logic (internal)
├── CommandPaletteModal.tsx     # Modal variant
├── CommandPaletteEmbedded.tsx  # Floating variant
├── CommandPaletteDrawer.tsx    # Drawer variant
├── index.ts                    # Barrel exports
└── README.md                   # This file
```

## Related Documentation

- [Design Principles](../../references/design-principles.md)
- [Keyboard Navigation](../../references/keyboard-navigation.md)
- [Theming Guide](../../references/theming.md)
- [Floating Positioning](../../references/floating-positioning.md)

## License

MIT - Free for personal and commercial use
