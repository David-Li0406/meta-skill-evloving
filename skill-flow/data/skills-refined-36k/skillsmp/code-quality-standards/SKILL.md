---
name: code-quality-standards
description: Coding conventions and best practices for TypeScript, React 19, and Next.js 15. Use when writing new code, reviewing code quality, or ensuring consistency with Airbnb style guides and project-specific patterns.
---

# Code Quality Standards

Coding conventions for the Y-Not Radio site codebase. These standards align with Airbnb style guides and are enforced through ESLint configuration.

## TypeScript & React Patterns

### Function Components

Use arrow function components with TypeScript interfaces:

```typescript
// ✅ Good: Arrow function with interface
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ label, onClick, disabled = false }) => {
  return <button onClick={onClick} disabled={disabled}>{label}</button>;
};

// ❌ Bad: Function declaration, PropTypes
export function Button({ label, onClick }) {
  return <button onClick={onClick}>{label}</button>;
}
```

### Hooks

**Naming**: Always use `use` prefix
**Dependencies**: Always specify complete dependency arrays

```typescript
// ✅ Good: Proper hook naming and dependencies
export const useArtistSearch = (query: string) => {
  const [results, setResults] = useState<Artist[]>([]);

  useEffect(() => {
    if (!query) return;
    fetchArtists(query).then(setResults);
  }, [query]); // Complete dependencies

  return results;
};

// ❌ Bad: Missing prefix, incomplete dependencies
export const artistSearch = (query: string) => {
  useEffect(() => {
    fetchArtists(query).then(setResults);
  }, []); // Missing query dependency
};
```

### Component Composition

**Max prop depth**: 2 levels
**Max props per component**: 7 props (use composition pattern beyond this)

```typescript
// ✅ Good: Composition pattern
interface ArtistCardProps {
  artist: Artist;
  actions: React.ReactNode;
}

export const ArtistCard: React.FC<ArtistCardProps> = ({ artist, actions }) => (
  <div>
    <h3>{artist.name}</h3>
    {actions}
  </div>
);

// Usage
<ArtistCard
  artist={artist}
  actions={<ArtistActions onEdit={...} onDelete={...} />}
/>

// ❌ Bad: Too many props (prop drilling)
interface ArtistCardProps {
  name: string;
  genre: string;
  country: string;
  onEdit: () => void;
  onDelete: () => void;
  onShare: () => void;
  onFavorite: () => void;
  showDetails: boolean; // 8 props - too many!
}
```

### File Size Limits

- **Components**: Max 300 lines (excluding blank lines and comments)
- **Utilities**: Max 200 lines
- **Test files**: No strict limit (but keep focused)

Split large files into smaller, focused modules.

### Single Responsibility Principle

Strive to give components a single responsibility. When a component grows too complex, decompose it:

1. **Business logic**: Extract into custom hooks (e.g., `useArtistData`)
2. **CSS Styles**: Keep focused on presentation (consider utility classes)
3. **Content**: Separate data fetching from rendering

```typescript
// ✅ Good: Single responsibility - presentation only
interface ArtistCardProps {
  artist: Artist;
  onSelect: () => void;
}

export const ArtistCard: React.FC<ArtistCardProps> = ({ artist, onSelect }) => {
  return (
    <div className="artist-card" onClick={onSelect}>
      <h3>{artist.name}</h3>
      <p>{artist.genre}</p>
    </div>
  );
};

// ✅ Good: Business logic extracted to hook
export const useArtistData = (artistId: string) => {
  const [artist, setArtist] = useState<Artist | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchArtist(artistId).then((data) => {
      setArtist(data);
      setLoading(false);
    });
  }, [artistId]);

  return { artist, loading };
};

// ✅ Good: Component uses hook for logic
export const ArtistCardContainer: React.FC<{ artistId: string }> = ({ artistId }) => {
  const { artist, loading } = useArtistData(artistId);

  if (loading) return <LoadingSpinner />;
  if (!artist) return null;

  return <ArtistCard artist={artist} onSelect={() => handleSelect(artist)} />;
};

// ❌ Bad: Component doing too much
export const ArtistCard: React.FC<{ artistId: string }> = ({ artistId }) => {
  // Business logic mixed in
  const [artist, setArtist] = useState<Artist | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(false);

  useEffect(() => {
    fetchArtist(artistId).then(setArtist);
  }, [artistId]);

  // Complex styling logic
  const cardStyle = {
    backgroundColor: selected ? '#blue' : '#white',
    border: '1px solid gray',
    // ... many more style properties
  };

  // Too many responsibilities in one component
  return <div style={cardStyle}>{/* ... */}</div>;
};
```

## Next.js 15 Specific

### Server vs Client Components

**Default**: Server Components (no "use client")
**Client Components**: Only when necessary (interactivity, browser APIs, hooks)

```typescript
// ✅ Good: Server Component (default)
// app/artists/[id]/page.tsx
export default async function ArtistPage({ params }: { params: { id: string } }) {
  const artist = await fetchArtist(params.id);
  return <ArtistDetails artist={artist} />;
}

// ✅ Good: Client Component (when needed)
// components/SearchInput.tsx
'use client';

export const SearchInput: React.FC = () => {
  const [query, setQuery] = useState('');
  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
};

// ❌ Bad: Unnecessary "use client"
'use client';

export default function StaticPage() {
  return <div>This doesn't need client-side JS</div>;
}
```

### App Router Conventions

**File structure**:

- `page.tsx` - Route pages
- `layout.tsx` - Shared layouts
- `loading.tsx` - Loading UI
- `error.tsx` - Error boundaries
- `not-found.tsx` - 404 pages

**Route handlers**: `route.ts` for API routes

```typescript
// app/api/artists/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const artists = await fetchArtists();
  return NextResponse.json(artists);
}
```

### Metadata API

Use the Metadata API for SEO:

```typescript
// app/artists/[id]/page.tsx
import { Metadata } from 'next';

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const artist = await fetchArtist(params.id);
  return {
    title: artist.name,
    description: `${artist.name} - ${artist.genre}`,
  };
}
```

## Naming Conventions

### Files and Directories

- **Components**: `PascalCase.tsx` (e.g., `ArtistCard.tsx`)
- **Hooks**: `useHookName.ts` (e.g., `useArtistSearch.ts`)
- **Utilities**: `kebab-case.ts` (e.g., `format-date.ts`)
- **Test files**: Match component name exactly (e.g., `ArtistCard.test.tsx`)
- **Story files**: Match component name exactly (e.g., `ArtistCard.stories.tsx`)

### Variables and Functions

```typescript
// ✅ Good: camelCase for variables and functions
const artistName = 'Miles Davis';
const formatDate = (date: Date) => date.toLocaleDateString();

// ✅ Good: PascalCase for types and interfaces
interface ArtistProps {
  name: string;
}

type ArtistId = string;

// ✅ Good: UPPER_SNAKE_CASE for constants
const MAX_RESULTS = 100;
const API_BASE_URL = 'https://api.example.com';
```

## Import Organization

Use ESLint `plugin:import` for automatic sorting. Manual order:

```typescript
// 1. External packages (React, Next.js, third-party)
import React, { useState, useEffect } from 'react';
import { NextResponse } from 'next/server';
import axios from 'axios';

// 2. Internal absolute imports (@/...)
import { Button } from '@/components/ui/Button';
import { useArtistSearch } from '@/hooks/useArtistSearch';
import { formatDate } from '@/utils/format-date';

// 3. Relative imports
import { ArtistCard } from './ArtistCard';
import styles from './ArtistList.module.css';

// Group and sort alphabetically within groups
```

## Code Style

### Airbnb Patterns

Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) and [Airbnb React Style Guide](https://github.com/airbnb/javascript/tree/master/react):

- Use `const` for all references, `let` if you must reassign
- Use template strings for string concatenation
- Use arrow functions for anonymous functions
- Use destructuring for objects and arrays
- Always use semicolons
- Use single quotes for strings (enforced by Prettier)

### TypeScript Specific

```typescript
// ✅ Good: Type inference where clear
const count = 42; // inferred as number

// ✅ Good: Explicit types for function parameters and returns
function fetchArtist(id: string): Promise<Artist> {
  return fetch(`/api/artists/${id}`).then((res) => res.json());
}

// ✅ Good: Use interfaces for object shapes
interface Artist {
  id: string;
  name: string;
  genre?: string; // Optional with ?
}

// ❌ Bad: Using `any`
function processData(data: any) {
  // Avoid any!
  return data.someProperty;
}

// ✅ Good: Use proper types or unknown
function processData(data: Artist) {
  return data.name;
}
```

### Avoid Common Pitfalls

```typescript
// ❌ Bad: Index files that re-export (barrel files)
// index.ts
export { Button } from './Button';
export { Card } from './Card';

// ✅ Good: Import directly from source
import { Button } from '@/components/ui/Button';

// ❌ Bad: Prop spreading for large objects
<Component {...hugeObject} />

// ✅ Good: Explicit props (or controlled spreading)
<Component name={obj.name} id={obj.id} />
```

## Performance Best Practices

### Code Splitting

```typescript
// ✅ Good: Dynamic imports for heavy components
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <p>Loading chart...</p>,
});
```

### Image Optimization

```typescript
// ✅ Good: Next.js Image component
import Image from 'next/image';

<Image
  src="/artist.jpg"
  alt="Artist name"
  width={400}
  height={300}
  priority={false} // Lazy load by default
/>

// ❌ Bad: Standard img tag
<img src="/artist.jpg" alt="Artist name" />
```

### Memoization

```typescript
// ✅ Good: Memoize expensive computations
const sortedArtists = useMemo(
  () => artists.sort((a, b) => a.name.localeCompare(b.name)),
  [artists],
);

// ✅ Good: Memoize callbacks passed to children
const handleClick = useCallback(() => {
  console.log('Clicked');
}, []);
```

## Accessibility

Follow WCAG AA standards:

```typescript
// ✅ Good: Semantic HTML and ARIA
<button
  onClick={handleClick}
  aria-label="Close dialog"
  aria-pressed={isActive}
>
  Close
</button>

// ✅ Good: Keyboard navigation
<div
  role="button"
  tabIndex={0}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>
  Click me
</div>

// ❌ Bad: Non-semantic, no keyboard support
<div onClick={handleClick}>Click me</div>
```

## Testing Requirements

See `test-story-coupling` skill for detailed testing patterns.

**Coverage targets** (from `vitest.config.ts`):

- Statements: 80%
- Branches: 80%
- Functions: 80%
- Lines: 80%

## Additional Resources

- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Airbnb React Style Guide](https://github.com/airbnb/javascript/tree/master/react)
- [Next.js Documentation](https://nextjs.org/docs)
- [React 19 Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
