# Result Types Implementation Guide

This guide walks through implementing specialized result components in your command palette project.

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
pnpm add lucide-react date-fns cmdk
```

### 2. Copy Components

Copy all `.tsx` files from this directory to your project:

```bash
cp -r .claude/skills/creating-command-palettes/templates/result-types/* \
  src/components/command-palette/result-types/
```

### 3. Set Up Utilities

Ensure you have the `cn()` utility in `@/lib/utils`:

```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### 4. Use in Your Palette

```tsx
import { PersonResult, FileResult, ActionResult } from '@/components/command-palette/result-types';

// In your command palette component
<Command.Item value={item.id}>
  {({ selected }) => (
    <PersonResult
      person={item}
      selected={selected}
      onClick={() => handleSelect(item)}
    />
  )}
</Command.Item>
```

## Component Selection Guide

Choose the right component for your data:

| You Have | Use Component | Why |
|----------|---------------|-----|
| Users, contacts, team members | **PersonResult** | Shows avatar, status, role |
| Files, documents, attachments | **FileResult** | File icons, size, timestamps |
| Commands, menu items | **ActionResult** | Icons, shortcuts, states |
| Projects, templates, galleries | **CardResult** | Visual preview, tags |
| Routes, pages, links | **NavigationResult** | Breadcrumbs, path info |

## Step-by-Step Implementation

### Step 1: Define Your Data Types

Create TypeScript interfaces for your data:

```typescript
// types/search.ts
export interface SearchPerson {
  id: string;
  name: string;
  role: string;
  avatar?: string;
  status?: 'online' | 'offline' | 'away';
  metadata?: {
    email?: string;
    department?: string;
  };
}

export interface SearchFile {
  id: string;
  name: string;
  path: string;
  type: string;
  size: number;
  modified: Date;
}

export interface SearchAction {
  id: string;
  icon: LucideIcon;
  name: string;
  description: string;
  shortcut?: string;
  onExecute: () => void;
}
```

### Step 2: Create Data Fetchers

Implement hooks or functions to fetch your data:

```typescript
// hooks/useSearch.ts
import { useQuery } from '@tanstack/react-query';

export function useSearchPeople(query: string) {
  return useQuery({
    queryKey: ['search', 'people', query],
    queryFn: () => searchPeopleAPI(query),
    enabled: query.length > 0,
  });
}

export function useSearchFiles(query: string) {
  return useQuery({
    queryKey: ['search', 'files', query],
    queryFn: () => searchFilesAPI(query),
    enabled: query.length > 0,
  });
}
```

### Step 3: Build Your Palette Component

Create a command palette that uses the result components:

```tsx
// components/CommandPalette.tsx
import * as React from 'react';
import { Command } from 'cmdk';
import { PersonResult, FileResult, ActionResult } from './result-types';
import { useSearchPeople, useSearchFiles } from '@/hooks/useSearch';

export function CommandPalette() {
  const [open, setOpen] = React.useState(false);
  const [search, setSearch] = React.useState('');

  const { data: people, isLoading: loadingPeople } = useSearchPeople(search);
  const { data: files, isLoading: loadingFiles } = useSearchFiles(search);

  // Keyboard shortcut
  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, []);

  return (
    <Command.Dialog open={open} onOpenChange={setOpen}>
      <Command.Input
        value={search}
        onValueChange={setSearch}
        placeholder="Search anything..."
      />

      <Command.List>
        {/* People results */}
        {people && people.length > 0 && (
          <Command.Group heading="People">
            {people.map((person) => (
              <Command.Item key={person.id} value={person.name}>
                {({ selected }) => (
                  <PersonResult
                    person={person}
                    selected={selected}
                    onClick={() => handleSelectPerson(person)}
                  />
                )}
              </Command.Item>
            ))}
          </Command.Group>
        )}

        {/* File results */}
        {files && files.length > 0 && (
          <Command.Group heading="Files">
            {files.map((file) => (
              <Command.Item key={file.id} value={file.name}>
                {({ selected }) => (
                  <FileResult
                    file={file}
                    selected={selected}
                    onClick={() => handleOpenFile(file)}
                  />
                )}
              </Command.Item>
            ))}
          </Command.Group>
        )}

        <Command.Empty>No results found</Command.Empty>
      </Command.List>
    </Command.Dialog>
  );
}
```

### Step 4: Add Loading States

Show skeletons while data loads:

```tsx
import { PersonResultSkeleton, FileResultSkeleton } from './result-types';

{loadingPeople && (
  <Command.Group heading="People">
    <PersonResultSkeleton />
    <PersonResultSkeleton />
    <PersonResultSkeleton />
  </Command.Group>
)}
```

### Step 5: Handle Selection

Implement handlers for each result type:

```typescript
const handleSelectPerson = (person: SearchPerson) => {
  console.log('Selected person:', person);
  // Navigate to profile, start chat, etc.
  setOpen(false);
};

const handleOpenFile = (file: SearchFile) => {
  console.log('Opening file:', file);
  // Open file viewer, editor, etc.
  setOpen(false);
};

const handleExecuteAction = (action: SearchAction) => {
  action.onExecute();
  setOpen(false);
};
```

## Advanced Patterns

### Unified Search with Multiple Types

Combine different result types in a single search:

```tsx
type SearchResultType = 'person' | 'file' | 'action';

interface SearchResult {
  type: SearchResultType;
  data: SearchPerson | SearchFile | SearchAction;
}

function renderResult(result: SearchResult, selected: boolean) {
  switch (result.type) {
    case 'person':
      return <PersonResult person={result.data} selected={selected} />;
    case 'file':
      return <FileResult file={result.data} selected={selected} />;
    case 'action':
      return <ActionResult action={result.data} selected={selected} />;
  }
}
```

### Tab-Based Filtering

Add tabs to filter by result type:

```tsx
const [activeTab, setActiveTab] = useState<'all' | 'people' | 'files'>('all');

<div className="flex gap-2 px-3 pt-3 border-b">
  <button onClick={() => setActiveTab('all')}>All</button>
  <button onClick={() => setActiveTab('people')}>People</button>
  <button onClick={() => setActiveTab('files')}>Files</button>
</div>
```

### Virtual Scrolling for Large Lists

Optimize performance with virtual scrolling:

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

const parentRef = useRef<HTMLDivElement>(null);

const virtualizer = useVirtualizer({
  count: results.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 56, // Height of result component
  overscan: 5,
});

<div ref={parentRef} className="h-96 overflow-auto">
  {virtualizer.getVirtualItems().map((virtualRow) => (
    <div
      key={virtualRow.index}
      style={{
        height: `${virtualRow.size}px`,
        transform: `translateY(${virtualRow.start}px)`,
      }}
    >
      <PersonResult {...results[virtualRow.index]} />
    </div>
  ))}
</div>
```

### Recent Items Tracking

Track and display recently selected items:

```typescript
// hooks/useRecent.ts
import { useLocalStorage } from '@/hooks/useLocalStorage';

export function useRecentPeople() {
  const [recent, setRecent] = useLocalStorage<SearchPerson[]>('recent-people', []);

  const addRecent = (person: SearchPerson) => {
    setRecent((prev) => {
      const filtered = prev.filter((p) => p.id !== person.id);
      return [person, ...filtered].slice(0, 10); // Keep 10 most recent
    });
  };

  return { recent, addRecent };
}

// Usage
const { recent, addRecent } = useRecentPeople();

const handleSelectPerson = (person: SearchPerson) => {
  addRecent(person);
  // ... rest of handler
};

// Show recent when search is empty
{search.length === 0 && recent.length > 0 && (
  <Command.Group heading="Recent">
    {recent.map((person) => (
      <Command.Item key={person.id}>
        <PersonResult person={person} {...props} />
      </Command.Item>
    ))}
  </Command.Group>
)}
```

## Customization Examples

### Custom Styling

Override default styles:

```tsx
<PersonResult
  person={person}
  selected={selected}
  onClick={onClick}
  className="border-l-4 border-l-blue-500" // Add custom border
/>
```

### Custom Icons

Replace default icons:

```tsx
// Create custom icon mapping
const customFileIcons = {
  ts: MyCustomTypeScriptIcon,
  js: MyCustomJavaScriptIcon,
  // ...
};

// Modify FileResult component to use custom icons
```

### Custom Formatters

Change how data is displayed:

```tsx
// In FileResult.tsx
const formatFileSize = (bytes: number): string => {
  // Your custom formatting logic
  return `${(bytes / 1024).toFixed(0)}kb`;
};

const formatRelativeTime = (date: Date): string => {
  // Show absolute dates instead of relative
  return format(date, 'MMM d, yyyy');
};
```

## Testing

Example tests for result components:

```tsx
// PersonResult.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { PersonResult } from './PersonResult';

describe('PersonResult', () => {
  const mockPerson = {
    name: 'John Doe',
    role: 'Developer',
    status: 'online' as const,
  };

  it('displays person information', () => {
    render(
      <PersonResult
        person={mockPerson}
        selected={false}
        onClick={() => {}}
      />
    );

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Developer')).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();

    render(
      <PersonResult
        person={mockPerson}
        selected={false}
        onClick={handleClick}
      />
    );

    await user.click(screen.getByRole('option'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('shows selected state', () => {
    render(
      <PersonResult
        person={mockPerson}
        selected={true}
        onClick={() => {}}
      />
    );

    expect(screen.getByRole('option')).toHaveAttribute('aria-selected', 'true');
  });

  it('generates initials when no avatar provided', () => {
    render(
      <PersonResult
        person={mockPerson}
        selected={false}
        onClick={() => {}}
      />
    );

    expect(screen.getByText('JD')).toBeInTheDocument();
  });
});
```

## Troubleshooting

### Common Issues

**Components not styled correctly:**
- Ensure Tailwind CSS is properly configured
- Check that semantic color tokens exist in your theme
- Verify `cn()` utility is working

**Icons not displaying:**
- Confirm `lucide-react` is installed
- Check icon imports in your components
- Verify icon components receive `className` prop

**Date formatting errors:**
- Ensure `date-fns` is installed
- Check that date values are valid Date objects
- Handle timezone issues for server-sent dates

**Performance issues with large lists:**
- Implement virtual scrolling (see Advanced Patterns)
- Add memoization with `React.memo`
- Debounce search input

**TypeScript errors:**
- Ensure all prop types match component interfaces
- Check that data shapes match expected types
- Verify icon types (`LucideIcon`) are correct

## Next Steps

1. **Review the UnifiedPaletteExample.tsx** - See all components working together
2. **Check README.md** - Detailed API documentation for each component
3. **Customize for your needs** - Modify styling, formatting, behavior
4. **Add virtual scrolling** - For large datasets (>100 items)
5. **Implement tracking** - Recent items, favorites, frequency
6. **Write tests** - Ensure components work correctly

## Resources

- [cmdk Documentation](https://cmdk.paco.me/)
- [Lucide Icons](https://lucide.dev/)
- [date-fns Documentation](https://date-fns.org/)
- [Tanstack Virtual](https://tanstack.com/virtual/latest)
- [Design Principles](../../references/design-principles.md)
- [Full Examples](../../examples/)

## Support

For issues or questions:
1. Check the README.md for API documentation
2. Review the UnifiedPaletteExample.tsx for usage patterns
3. Refer to design-principles.md for UX guidance
4. See examples/ directory for complete implementations
