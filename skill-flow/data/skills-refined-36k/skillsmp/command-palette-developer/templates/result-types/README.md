# Result Type Components

Specialized, production-ready result components for command palettes. Each component handles a specific data type with consistent UX patterns, accessibility support, and dark/light theme compatibility.

## Components Overview

| Component | Purpose | Height | Key Features |
|-----------|---------|--------|--------------|
| **PersonResult** | User/contact selection | 56px | Avatar, status indicator, metadata |
| **FileResult** | File browser/search | 56px | Type icons, size formatting, relative time |
| **ActionResult** | Command execution | 48-56px | Icons, shortcuts, disabled/destructive states |
| **CardResult** | Visual content | Variable | Images, tags, starred items |
| **NavigationResult** | Route navigation | 56px | Breadcrumbs, recent indicator, external links |

## Installation

All components require:

```bash
pnpm add lucide-react date-fns
```

Ensure your project has:
- `@/lib/utils` with `cn()` utility
- Tailwind CSS v4 configured
- Dark/light theme support

## Usage Examples

### PersonResult

Search and select users, team members, or contacts.

```tsx
import { PersonResult } from './result-types';

<PersonResult
  person={{
    name: "Sarah Chen",
    role: "Senior Engineer",
    avatar: "/avatars/sarah.jpg",
    status: "online",
    metadata: {
      email: "sarah@company.com",
      department: "Engineering",
      location: "San Francisco"
    }
  }}
  selected={selectedIndex === index}
  onClick={() => handleSelect(person)}
/>
```

**Features:**
- Avatar with automatic initials fallback
- Status indicator (online/offline/away) with color-coded dots
- Optional metadata display (email, department, location)
- Gradient background for initials when no avatar provided

**Use cases:**
- Team member picker
- Contact search
- User mentions (@mentions)
- Assignment dialogs

### FileResult

Browse files, documents, or search results.

```tsx
import { FileResult } from './result-types';

<FileResult
  file={{
    name: "UserService.ts",
    path: "/src/services/user/UserService.ts",
    type: "ts",
    size: 12458, // bytes
    modified: new Date("2025-01-13T10:30:00"),
    thumbnail: "/thumbnails/preview.png" // optional
  }}
  selected={selectedIndex === index}
  onClick={() => openFile(file)}
/>
```

**Features:**
- Smart file type icons (code, images, documents, archives)
- Automatic file size formatting (B, KB, MB, GB)
- Relative timestamps ("2 hours ago")
- Path truncation from middle for long paths
- Optional thumbnail preview support
- Lazy loading for thumbnail images

**Supported file types:**
- Code: `.js`, `.ts`, `.py`, `.rs`, `.go`, `.java`
- Config: `.json`, `.yaml`, `.toml`, `.xml`
- Images: `.png`, `.jpg`, `.svg`, `.webp`
- Video: `.mp4`, `.mov`, `.webm`
- Archives: `.zip`, `.tar`, `.gz`
- Documents: `.txt`, `.md`, `.pdf`

**Use cases:**
- File picker/browser
- Recent files list
- Search results
- Document finder

### ActionResult

Execute commands and actions with keyboard shortcuts.

```tsx
import { ActionResult } from './result-types';
import { Save, Trash2 } from 'lucide-react';

<ActionResult
  action={{
    icon: Save,
    name: "Save Document",
    description: "Save current changes to file",
    shortcut: "Cmd+S",
    disabled: !hasChanges,
    destructive: false
  }}
  selected={selectedIndex === index}
  onClick={() => executeAction(action)}
/>

// Destructive action example
<ActionResult
  action={{
    icon: Trash2,
    name: "Delete Project",
    description: "Permanently delete this project",
    shortcut: "Cmd+Shift+D",
    destructive: true
  }}
  selected={selectedIndex === index}
  onClick={() => confirmDelete()}
/>
```

**Features:**
- Platform-aware keyboard shortcuts (⌘ on Mac, Ctrl on Windows)
- Disabled state styling
- Destructive action highlighting (red accent)
- Icon-based visual identification
- Shortcut key display with proper formatting

**Keyboard shortcut formatting:**
- Automatically converts: `Cmd` → `⌘`, `Ctrl` → `Ctrl` (or `^` on Mac)
- Supports: `Alt` (`⌥`), `Shift` (`⇧`), arrow keys, special keys
- Example: `"Cmd+Shift+P"` → `⌘ + ⇧ + P`

**Use cases:**
- Command palette actions
- Context menus
- Quick actions panel
- Editor commands

### CardResult

Display visual content with rich metadata.

```tsx
import { CardResult } from './result-types';

<CardResult
  card={{
    image: "/thumbnails/project-preview.jpg",
    title: "E-commerce Dashboard",
    description: "Modern analytics dashboard for online stores with real-time metrics and customizable widgets.",
    tags: ["React", "TypeScript", "Analytics"],
    starred: true,
    author: {
      name: "Alex Johnson",
      avatar: "/avatars/alex.jpg"
    }
  }}
  selected={selectedIndex === index}
  onClick={() => openProject(card)}
/>
```

**Features:**
- Image lazy loading with loading state
- Fallback for failed image loads
- Multi-line description truncation (2-3 lines)
- Tag display with overflow handling (+N indicator)
- Star/favorite indicator
- Author metadata with avatar
- Vertical card layout optimized for visual content

**Layout:**
- Image: 160px height, full width
- Content padding: 12px
- Tags: Maximum 3 visible, remaining count shown
- Responsive image sizing

**Use cases:**
- Project browser
- Template gallery
- Content picker
- Design system showcase

### NavigationResult

Navigate routes and pages with breadcrumb context.

```tsx
import { NavigationResult } from './result-types';
import { Home } from 'lucide-react';

<NavigationResult
  route={{
    icon: Home,
    name: "Dashboard",
    path: "/app/dashboard",
    section: "Main",
    recent: true,
    external: false
  }}
  selected={selectedIndex === index}
  onClick={() => navigate(route.path)}
/>

// External link example
<NavigationResult
  route={{
    name: "API Documentation",
    path: "https://docs.api.com",
    section: "Documentation",
    external: true
  }}
  selected={selectedIndex === index}
  onClick={() => window.open(route.path)}
/>
```

**Features:**
- Automatic breadcrumb generation from path
- Path truncation for long URLs
- Recent visit indicator
- External link icon
- Optional icon or auto-generated initial
- Responsive breadcrumb trail (hidden on mobile)

**Breadcrumb formatting:**
- Auto-capitalizes path segments
- Replaces hyphens/underscores with spaces
- Example: `/app/user-settings/profile` → `App / User Settings / Profile`

**Use cases:**
- Page navigation
- Quick jumper
- Recent pages
- External resources

## Shared Features

### Accessibility

All components include:

- `role="option"` for proper ARIA semantics
- `aria-selected` state management
- Keyboard navigation support
- Focus management with visual indicators
- Sufficient color contrast (WCAG AA compliant)

### Theme Support

Automatic dark/light mode support using Tailwind CSS semantic colors:

- `bg-background` / `text-foreground` (base)
- `bg-muted` / `text-muted-foreground` (secondary)
- `bg-primary` / `text-primary` (selected state)
- `bg-destructive` / `text-destructive` (destructive actions)

### Loading States

Each component includes a skeleton loading variant:

```tsx
import { PersonResultSkeleton, FileResultSkeleton } from './result-types';

{isLoading ? (
  <>
    <PersonResultSkeleton />
    <PersonResultSkeleton />
    <PersonResultSkeleton />
  </>
) : (
  results.map((result, index) => (
    <PersonResult key={result.id} person={result} {...props} />
  ))
)}
```

### Responsive Design

Breakpoints:
- `sm`: 640px - Show additional metadata
- `md`: 768px - Expand breadcrumbs
- `lg`: 1024px - Full feature set
- `xl`: 1280px - Optimized spacing

Mobile considerations:
- Touch-friendly hit areas (minimum 48px)
- Truncated text with tooltips
- Hidden secondary information on small screens

## Customization

### Styling

Override with Tailwind classes using `cn()`:

```tsx
<PersonResult
  {...props}
  className="hover:bg-accent" // Custom hover color
/>
```

### Icons

Replace Lucide React icons with your preferred icon library:

```tsx
import { CustomIcon } from '@/components/icons';

<ActionResult
  action={{
    icon: CustomIcon, // Must accept className prop
    // ...
  }}
  {...props}
/>
```

### Formatting

Customize formatters by modifying utility functions:

```tsx
// FileResult.tsx - Change date formatting
const formatRelativeTime = (date: Date): string => {
  return format(date, 'MMM d, yyyy'); // Absolute dates
};

// ActionResult.tsx - Customize shortcut symbols
const formatShortcut = (shortcut: string): string => {
  return shortcut.replace(/Cmd/g, 'Command'); // Spell out
};
```

## Performance Considerations

### Virtual Scrolling

For large lists (>100 items), use with Tanstack Virtual:

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

const parentRef = useRef<HTMLDivElement>(null);

const virtualizer = useVirtualizer({
  count: results.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 56, // Match component height
  overscan: 5
});

<div ref={parentRef} className="h-96 overflow-auto">
  <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
    {virtualizer.getVirtualItems().map((virtualRow) => (
      <div
        key={virtualRow.index}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          transform: `translateY(${virtualRow.start}px)`
        }}
      >
        <FileResult file={results[virtualRow.index]} {...props} />
      </div>
    ))}
  </div>
</div>
```

### Image Loading

FileResult and CardResult implement lazy loading:

- Uses native `loading="lazy"` attribute
- Handles load failures gracefully
- Shows loading states during fetch

### Memoization

Wrap in `React.memo` for large lists:

```tsx
export const MemoizedPersonResult = React.memo(PersonResult, (prev, next) => {
  return prev.selected === next.selected && prev.person.id === next.person.id;
});
```

## Testing

Example test with React Testing Library:

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { PersonResult } from './PersonResult';

test('calls onClick when person result is clicked', async () => {
  const handleClick = vi.fn();
  const user = userEvent.setup();

  render(
    <PersonResult
      person={{
        name: "John Doe",
        role: "Developer",
        status: "online"
      }}
      selected={false}
      onClick={handleClick}
    />
  );

  await user.click(screen.getByRole('option'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});

test('shows selected state', () => {
  render(
    <PersonResult
      person={{ name: "John Doe", role: "Developer" }}
      selected={true}
      onClick={() => {}}
    />
  );

  expect(screen.getByRole('option')).toHaveAttribute('aria-selected', 'true');
});
```

## Integration with Command Palettes

Use with `cmdk` library:

```tsx
import { Command } from 'cmdk';
import { PersonResult } from './result-types';

<Command.List>
  <Command.Group heading="People">
    {people.map((person) => (
      <Command.Item key={person.id} value={person.name}>
        <PersonResult
          person={person}
          selected={false} // cmdk handles selection
          onClick={() => selectPerson(person)}
        />
      </Command.Item>
    ))}
  </Command.Group>
</Command.List>
```

## Browser Support

- Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Progressive enhancement for older browsers
- Graceful degradation of animations and effects

## License

Part of the creating-command-palettes skill templates.

## Related Documentation

- [Design Principles](../../references/design-principles.md)
- [Keyboard Navigation](../../references/keyboard-navigation.md)
- [State Management](../../references/state-management.md)
- [File Search Example](../../examples/file-search/)
- [Action Palette Example](../../examples/action-palette/)
