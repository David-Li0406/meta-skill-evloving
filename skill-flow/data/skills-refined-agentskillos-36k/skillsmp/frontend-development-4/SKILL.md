---
name: frontend-development
description: Comprehensive frontend development skill for building robust, responsive, and maintainable web applications and mobile apps. Use this for all UI/UX implementation, component building, styling, and client-side logic.
---

# Frontend Development Expert Skill

## Core Principles

### 1. Code Quality & Architecture
- **Write semantic, accessible HTML** - Use proper tags (`<nav>`, `<main>`, `<article>`, `<section>`, `<button>` not `<div>` with click handlers)
- **Component-driven architecture** - Break UI into reusable, single-responsibility components
- **Separation of concerns** - Keep logic, styling, and markup cleanly separated
- **DRY (Don't Repeat Yourself)** - Abstract repeated patterns into reusable utilities/components
- **KISS (Keep It Simple, Stupid)** - Avoid over-engineering; choose the simplest solution that works

### 2. Responsive Design (Mobile-First)
- **Always start with mobile** (320px) and scale up
- **Breakpoint strategy**:
  ```css
  /* Mobile first - no media query needed */
  .element { /* base styles */ }
  
  /* Tablet */
  @media (min-width: 640px) { }
  
  /* Desktop */
  @media (min-width: 1024px) { }
  
  /* Large desktop */
  @media (min-width: 1280px) { }
  ```
- **Fluid typography**: Use `clamp()` for responsive font sizes
  ```css
  font-size: clamp(1rem, 2vw + 0.5rem, 1.5rem);
  ```
- **Flexible layouts**: Use `flexbox` and `grid` instead of fixed widths
- **Test on real devices** - Emulators don't catch everything

## DO's ✅

### HTML
- ✅ Use semantic HTML5 elements
- ✅ Add ARIA labels for screen readers when needed
- ✅ Include `alt` text for all images
- ✅ Use `<button>` for actions, `<a>` for navigation
- ✅ Properly nest heading levels (h1 → h2 → h3)
- ✅ Add `lang` attribute to `<html>` tag
- ✅ Use `<form>` with proper `label` associations

### CSS
- ✅ Use CSS variables for theming
  ```css
  :root {
    --primary-color: #007bff;
    --spacing-unit: 8px;
  }
  ```
- ✅ Employ BEM or consistent naming convention
  ```css
  .card { }
  .card__title { }
  .card--featured { }
  ```
- ✅ Use modern layout tools (Grid, Flexbox)
- ✅ Implement responsive images
  ```html
  <img srcset="image-320w.jpg 320w, image-640w.jpg 640w"
       sizes="(max-width: 640px) 100vw, 640px"
       src="image-640w.jpg" alt="Description">
  ```
- ✅ Use relative units (`rem`, `em`, `%`, `vw`, `vh`) over `px`
- ✅ Add `:focus` styles for keyboard navigation
- ✅ Use CSS Grid for 2D layouts, Flexbox for 1D

### JavaScript/TypeScript
- ✅ Use `const` by default, `let` when reassignment needed, never `var`
- ✅ Prefer modern ES6+ syntax (arrow functions, destructuring, spread operator)
- ✅ Use optional chaining and nullish coalescing
  ```javascript
  const name = user?.profile?.name ?? 'Guest';
  ```
- ✅ Implement error boundaries (React) or try-catch blocks
- ✅ Debounce/throttle expensive operations (scroll, resize, input)
  ```javascript
  const debouncedSearch = debounce((query) => {
    // API call
  }, 300);
  ```
- ✅ Use async/await over promise chains for readability
- ✅ Validate user input on client AND server
- ✅ Use TypeScript for type safety (when possible)

### React/Component Frameworks
- ✅ Use functional components with hooks
- ✅ Keep components small (< 250 lines ideally)
- ✅ Memoize expensive computations with `useMemo`
- ✅ Use `useCallback` for functions passed as props
- ✅ Implement proper key props in lists (unique, stable IDs)
- ✅ Lift state only when necessary
- ✅ Use context API **only** for truly global state (theme, auth, locale)
- ✅ Implement code splitting and lazy loading
  ```javascript
  const HeavyComponent = lazy(() => import('./HeavyComponent'));
  ```

### Performance
- ✅ Lazy load images and components
- ✅ Minimize bundle size (tree shaking, code splitting)
- ✅ Use CDN for static assets
- ✅ Implement virtual scrolling for long lists
- ✅ Optimize images (WebP, proper sizing, compression)
- ✅ Cache API responses appropriately
- ✅ Use lighthouse/web vitals for monitoring

### Accessibility (a11y)
- ✅ Ensure keyboard navigation works (Tab, Enter, Escape, Arrow keys)
- ✅ Maintain 4.5:1 contrast ratio for text
- ✅ Add skip-to-content links
- ✅ Test with screen readers (NVDA, JAWS, VoiceOver)
- ✅ Use proper heading hierarchy
- ✅ Provide text alternatives for non-text content

## DON'Ts ❌

### HTML
- ❌ Don't use tables for layout (only for tabular data)
- ❌ Don't use `<div>` or `<span>` when semantic elements exist
- ❌ Don't omit closing tags (even optional ones)
- ❌ Don't use inline styles (use CSS classes)
- ❌ Don't use deprecated tags (`<center>`, `<font>`, `<marquee>`)

### CSS
- ❌ Don't use `!important` (except for utility classes)
- ❌ Don't use absolute pixel values for responsive elements
- ❌ Don't use deep nesting (max 3-4 levels)
- ❌ Don't use IDs for styling (reserve for JS hooks)
- ❌ Don't forget vendor prefixes for modern features (use autoprefixer)
- ❌ Don't use floats for layout (use flexbox/grid)
- ❌ Don't use fixed widths that break on small screens
- ❌ Don't animate `width`, `height`, or `top/left` (use `transform` instead)
  ```css
  /* Bad - causes reflow */
  .box { transition: width 0.3s; }
  
  /* Good - GPU accelerated */
  .box { transition: transform 0.3s; }
  ```

### JavaScript
- ❌ Don't mutate state directly (use immutable patterns)
  ```javascript
  // Bad
  state.items.push(newItem);
  
  // Good
  setState({ items: [...state.items, newItem] });
  ```
- ❌ Don't use `eval()` or `innerHTML` with user input (XSS vulnerability)
- ❌ Don't ignore error handling
- ❌ Don't make synchronous API calls (blocks UI)
- ❌ Don't use global variables
- ❌ Don't compare with `==` (use strict `===`)
- ❌ Don't forget to clean up event listeners/subscriptions
  ```javascript
  useEffect(() => {
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  ```
- ❌ Don't use `any` type in TypeScript (defeats the purpose)
- ❌ Don't use array index as key in React lists (causes bugs)

### Performance
- ❌ Don't load entire libraries for one function (use tree-shaking or alternatives)
- ❌ Don't make unnecessary re-renders
- ❌ Don't fetch data in loops
- ❌ Don't block the main thread with heavy computations (use Web Workers)
- ❌ Don't ignore bundle size (keep < 200KB initial load)

### Security
- ❌ Don't store sensitive data in localStorage (use httpOnly cookies)
- ❌ Don't trust user input
- ❌ Don't expose API keys in frontend code
- ❌ Don't use outdated dependencies (security vulnerabilities)

## Responsive Patterns

### Container Queries (Modern Approach)
```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}
```

### Fluid Grids
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}
```

### Responsive Typography
```css
html {
  font-size: 16px;
}

@media (min-width: 640px) {
  html { font-size: 18px; }
}

h1 { font-size: clamp(1.5rem, 5vw, 3rem); }
```

### Touch-Friendly Targets
```css
.button {
  min-height: 44px; /* iOS recommendation */
  min-width: 44px;
  padding: 12px 24px;
}
```

## Refactoring Guidelines

### When to Refactor
1. **Code duplication** - Extract into reusable component/utility
2. **Component > 250 lines** - Split into smaller components
3. **Props drilling > 3 levels** - Use context or state management
4. **Complex conditional rendering** - Extract into separate components
5. **Performance issues** - Profile and optimize

### Refactoring Process
1. **Write/ensure tests exist** - Don't refactor without safety net
2. **One change at a time** - Small, incremental changes
3. **Commit frequently** - Easy to rollback if needed
4. **Test after each change** - Catch regressions early
5. **Update documentation** - Keep comments/docs in sync

### Extract Component Pattern
```javascript
// Before - monolithic component
function UserProfile() {
  return (
    <div>
      {/* 200 lines of JSX */}
    </div>
  );
}

// After - composed components
function UserProfile() {
  return (
    <div>
      <UserHeader />
      <UserStats />
      <UserPosts />
    </div>
  );
}
```

### Extract Hook Pattern (with TanStack Query)
```typescript
// ❌ BAD - useState for server data
function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    // This causes race conditions, no caching, no deduping
    fetch(`/api/search?q=${query}`).then(...);
  }, [query]);
}

// ✅ GOOD - TanStack Query handles everything
import { useQuery } from '@tanstack/react-query';
import { useDebouncedValue } from '@/hooks/use-debounce';

function useSearch(query: string) {
  const debouncedQuery = useDebouncedValue(query, 300);
  
  return useQuery({
    queryKey: ['search', debouncedQuery],
    queryFn: () => searchApi(debouncedQuery),
    enabled: debouncedQuery.length > 2,
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
  });
}

function SearchPage() {
  const [query, setQuery] = useState('');
  const { data: results, isLoading, error } = useSearch(query);
  // Clean, handles caching, deduping, race conditions automatically
}
```

## Testing Best Practices

### What to Test
- ✅ User interactions (clicks, form submissions)
- ✅ Conditional rendering
- ✅ Edge cases and error states
- ✅ Accessibility (keyboard navigation, screen reader output)
- ✅ Responsive behavior (viewport changes)

### Testing Pattern
```javascript
// React Testing Library example
test('submits form with user data', async () => {
  const handleSubmit = jest.fn();
  render(<SignupForm onSubmit={handleSubmit} />);
  
  await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
  await userEvent.type(screen.getByLabelText(/password/i), 'password123');
  await userEvent.click(screen.getByRole('button', { name: /sign up/i }));
  
  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'password123'
  });
});
```

## State Management Rules

### Local State (useState)
- Use for: UI state, form inputs, toggles
- Keep state close to where it's used

### Context API
- Use for: Theme, auth, localization
- Don't overuse - causes unnecessary re-renders

### External State (Redux, Zustand, Jotai)
- Use for: Complex app state, data shared across many components
- Keep actions pure and predictable

### Server State (React Query, SWR)
- Use for: API data, caching, background updates
- Let library handle loading/error states

## Mobile App Considerations (React Native / PWA)

### React Native Specific
- ✅ Use `StyleSheet.create()` for performance
- ✅ Use `FlatList` for long lists (not `ScrollView`)
- ✅ Optimize images with `resizeMode`
- ✅ Handle keyboard properly with `KeyboardAvoidingView`
- ❌ Don't use web-specific CSS
- ❌ Don't forget platform-specific code when needed

### PWA Best Practices
- ✅ Register service worker for offline support
- ✅ Add web app manifest
- ✅ Implement proper caching strategies
- ✅ Handle offline state gracefully
- ✅ Add install prompt

## File Structure (Scalable)

```
src/
├── components/
│   ├── common/          # Reusable UI components
│   ├── features/        # Feature-specific components
│   └── layout/          # Layout components
├── hooks/               # Custom hooks
├── utils/               # Helper functions
├── services/            # API calls
├── store/               # State management
├── styles/              # Global styles, themes
├── types/               # TypeScript types
├── constants/           # Configuration
└── tests/               # Test utilities
```

## Code Review Checklist

Before submitting code, verify:
- [ ] Works on mobile (< 640px) and desktop (> 1280px)
- [ ] Accessible (keyboard navigation, screen reader tested)
- [ ] No console errors/warnings
- [ ] Performance acceptable (< 3s load, 60fps interactions)
- [ ] Code follows project conventions
- [ ] No hardcoded values (use constants/config)
- [ ] Error handling implemented
- [ ] Loading states implemented
- [ ] Tests written/passing
- [ ] No sensitive data exposed

## Common Pitfalls to Avoid

1. **Premature optimization** - Profile first, then optimize
2. **Over-abstraction** - Don't abstract until pattern emerges 3+ times
3. **Ignoring browser compatibility** - Check caniuse.com for newer features
4. **Not testing on real devices** - Emulators miss important issues
5. **Skipping accessibility** - Bake it in from the start
6. **Tight coupling** - Keep components loosely coupled
7. **Magic numbers** - Use named constants
8. **Inconsistent naming** - Follow a convention strictly

## Performance Optimization Checklist

- [ ] Images optimized and lazy loaded
- [ ] Code split by route
- [ ] Tree shaking enabled
- [ ] Expensive computations memoized
- [ ] Virtualization for long lists
- [ ] Debounced/throttled event handlers
- [ ] Proper caching headers
- [ ] Minified and compressed assets
- [ ] Critical CSS inlined
- [ ] Fonts optimized (woff2, preload, display: swap)

## Quick Reference: Modern CSS Features

```css
/* Container Queries */
@container (min-width: 400px) { }

/* CSS Grid */
grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));

/* Flexbox Gap */
display: flex;
gap: 1rem;

/* Aspect Ratio */
aspect-ratio: 16 / 9;

/* Clamp */
font-size: clamp(1rem, 2.5vw, 2rem);

/* Custom Properties with Fallback */
color: var(--primary-color, #007bff);

/* Logical Properties */
margin-inline: auto; /* Instead of margin-left/right */
padding-block: 2rem; /* Instead of padding-top/bottom */

/* Modern Selectors */
:is(header, footer) a { } /* Instead of header a, footer a */
:where(nav) a { } /* Zero specificity */
:has(img) { } /* Parent selector */
```

---

## Data Fetching

### Current State (Migration in Progress)

**This project has TanStack Query installed and hooks ready in `use-event-crud.ts`, but components currently use `useEffect` + `useState` patterns. New code should use the TanStack Query hooks.**

### Available TanStack Query Hooks (use-event-crud.ts)

```typescript
// These hooks are READY TO USE - import from '@/hooks/use-event-crud'
import { 
  useEvents,        // Fetch events with filters
  useEvent,         // Fetch single event by ID
  useCreateEvent,   // Create new event (mutation)
  useUpdateEvent,   // Update event (mutation)
  useDeleteEvent,   // Soft delete (mutation)
  useEventSearch,   // Search events
  useNearbyEvents,  // Location-based query
} from '@/hooks/use-event-crud';

// Example usage
function EventList() {
  const { data, isLoading, error } = useEvents({
    filters: { status: 'published' },
    limit: 100,
  });

  if (isLoading) return <EventListSkeleton />;
  if (error) return <ErrorState error={error} />;
  return <EventGrid events={data?.events} />;
}
```

### Legacy Pattern (Current - To Be Migrated)

```typescript
// ⚠️ LEGACY - Components like EventsContainer.tsx currently use this
// This pattern works but lacks caching, deduping, and automatic refetch
const [events, setEvents] = useState<EventType[]>([]);
const [isLoading, setIsLoading] = useState(true);

useEffect(() => {
  const fetchEventsData = async () => {
    setIsLoading(true);
    try {
      const response = await fetchEvents(queryParams);
      setEvents(response.events);
    } finally {
      setIsLoading(false);
    }
  };
  fetchEventsData();
}, [dependencies]);
```

### Target Pattern (For New Code)

```typescript
// ✅ USE THIS for new components
import { useEvents, useCreateEvent } from '@/hooks/use-event-crud';

function EventsContainer({ filters }: Props) {
  // Automatic caching, deduping, background refetch
  const { data, isLoading, error, refetch } = useEvents({
    filters,
    limit: 100,
  });

  // Mutations with optimistic updates built-in
  const createMutation = useCreateEvent({
    onSuccess: () => {
      toast.success('Event created!');
    },
  });

  if (isLoading) return <EventListSkeleton />;
  if (error) return <ErrorState error={error} />;
  return <EventGrid events={data?.events} />;
}
```

### Why TanStack Query is Better

| Feature | useEffect + useState | TanStack Query |
|---------|---------------------|----------------|
| Caching | Manual | Automatic |
| Deduplication | None | Built-in |
| Race conditions | Must handle | Handled |
| Background refetch | Manual | Automatic |
| Optimistic updates | Complex | Simple API |
| Loading/Error states | Manual | Built-in |
| DevTools | None | Excellent |

### Migration Priority

1. **High**: `EventsContainer.tsx` - Main events display
2. **Medium**: `LocationListingPage.tsx` - Location-based events
3. **Low**: `UnifiedSearch.tsx` - Search component

### Deprecated Hooks (Do Not Use)

```typescript
// ❌ DO NOT USE - Legacy hooks in use-supabase.ts
// These will be removed after migration
import { useEvents, useEvent, useCreateEvent } from '@/hooks/use-supabase';
```

---

## Form Handling (React Hook Form + Zod)

**RULE: Never use `useState` for complex forms. Use React Hook Form with Zod validation.**

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Define schema ONCE - used for validation AND types
const eventSchema = z.object({
  title: z.string().min(3, 'Title must be at least 3 characters'),
  description: z.string().max(500),
  date: z.string().datetime(),
  location: z.object({
    lat: z.number(),
    lng: z.number(),
  }),
  foodType: z.enum(['veg', 'non-veg', 'vegan', 'other']),
});

type EventFormData = z.infer<typeof eventSchema>;

function EventForm({ onSubmit }: { onSubmit: (data: EventFormData) => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<EventFormData>({
    resolver: zodResolver(eventSchema),
    defaultValues: {
      title: '',
      description: '',
    },
  });

  const submitHandler = async (data: EventFormData) => {
    try {
      await onSubmit(data);
      reset();
      showSuccessToast('Event created!');
    } catch (error) {
      showErrorToast('Failed to create event');
    }
  };

  return (
    <form onSubmit={handleSubmit(submitHandler)}>
      <div>
        <label htmlFor="title">Title</label>
        <input id="title" {...register('title')} />
        {errors.title && <span role="alert">{errors.title.message}</span>}
      </div>
      
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating...' : 'Create Event'}
      </button>
    </form>
  );
}
```

---

## Next.js Specific Patterns

### Always Use `<Image />`, Never `<img>`
```typescript
import Image from 'next/image';

// ❌ BAD - Causes CLS, no optimization
<img src="/hero.jpg" alt="Hero" />

// ✅ GOOD - Optimized, no CLS
<Image 
  src="/hero.jpg" 
  alt="Hero"
  width={1200}
  height={600}
  priority // For above-the-fold images
  placeholder="blur"
  blurDataURL={blurHash}
/>
```

### Server vs Client Components
```typescript
// Server Component (default) - NO "use client" directive
// ✅ Use for: Data fetching, static content, SEO
async function EventPage({ params }: { params: { id: string } }) {
  const event = await fetchEvent(params.id); // Direct DB/API call
  return <EventDetails event={event} />;
}

// Client Component - Add "use client" directive
// ✅ Use for: Interactivity, hooks, browser APIs
"use client";

function LikeButton({ eventId }: { eventId: string }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>Like</button>;
}
```

### Keep Client Boundaries Small
```typescript
// ❌ BAD - Entire page is client component
"use client";
export default function EventPage() {
  // Everything here is client-side
}

// ✅ GOOD - Only interactive parts are client
export default async function EventPage() {
  const event = await fetchEvent();
  return (
    <div>
      <EventHeader event={event} />  {/* Server */}
      <EventDetails event={event} /> {/* Server */}
      <LikeButton eventId={event.id} /> {/* Client - "use client" inside */}
    </div>
  );
}
```

### URL State with nuqs (Not useState)
```typescript
import { useQueryState, parseAsInteger } from 'nuqs';

// ❌ BAD - State lost on refresh
const [page, setPage] = useState(1);

// ✅ GOOD - State in URL, shareable, persistent
const [page, setPage] = useQueryState('page', parseAsInteger.withDefault(1));
```

---

## Loading States (Skeletons, Not Spinners)

**RULE: Never use a single spinner for the whole page. Use skeleton loaders that match the layout.**

```typescript
// ❌ BAD - Spinner blocks entire UI
function EventList() {
  if (isLoading) return <Spinner />;
  return <div>...</div>;
}

// ✅ GOOD - Skeleton matches actual layout
function EventListSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="animate-pulse">
          <div className="bg-gray-200 h-48 rounded-lg" />
          <div className="mt-4 h-4 bg-gray-200 rounded w-3/4" />
          <div className="mt-2 h-4 bg-gray-200 rounded w-1/2" />
        </div>
      ))}
    </div>
  );
}

function EventList() {
  const { data, isLoading } = useQuery({ ... });
  
  if (isLoading) return <EventListSkeleton />;
  return <EventGrid events={data} />;
}
```

### Next.js Loading States
```typescript
// app/events/loading.tsx - Automatic loading UI
export default function Loading() {
  return <EventListSkeleton />;
}
```

---

## Error Boundaries

**RULE: Wrap risky components so errors don't crash the entire app.**

```typescript
"use client";
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('Error boundary caught:', error, info);
    // Send to error tracking service (Sentry, etc.)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div role="alert" className="p-4 bg-red-50 text-red-800 rounded">
          <h2>Something went wrong</h2>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<EventErrorFallback />}>
  <EventDetails event={event} />
</ErrorBoundary>
```

### Next.js Error Handling
```typescript
// app/events/error.tsx - Automatic error UI
"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div role="alert">
      <h2>Failed to load events</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

---

## Third-Party Library DOM Integration (Critical)

**RULE: Never put React children inside a container that a third-party library (Google Maps, D3, Three.js, etc.) will manipulate.**

### The Problem
Third-party libraries take ownership of their container's DOM. If React also tries to manage children inside that container, you get `removeChild` errors and crashes.

```typescript
// ❌ FORBIDDEN - Will cause removeChild errors
function BadMap() {
  const mapRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Google Maps takes over mapRef container
    new google.maps.Map(mapRef.current!, { ... });
  }, []);

  return (
    <div ref={mapRef}>
      {/* React children inside third-party container = CRASH */}
      {loading && <Spinner />}
      {error && <ErrorMessage />}
    </div>
  );
}
```

### The Solution - Empty Container with Absolute Siblings

```typescript
// ✅ CORRECT - Empty container, React overlays as siblings
function GoodMap() {
  const mapRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    new google.maps.Map(mapRef.current!, { ... });
    setLoading(false);
  }, []);

  return (
    <div className="relative w-full h-full">
      {/* Empty self-closing container - library owns this completely */}
      <div ref={mapRef} className="absolute inset-0" />
      
      {/* React-managed states as SIBLINGS with absolute positioning */}
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/80 z-10">
          <Spinner />
        </div>
      )}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-red-50 z-10">
          <ErrorMessage error={error} />
        </div>
      )}
    </div>
  );
}
```

### Rules for Third-Party Integration

1. **Empty container**: Library containers MUST be self-closing `<div ref={ref} />`
2. **No React children**: Never put conditional renders inside the container
3. **Absolute siblings**: UI overlays must be siblings with `position: absolute`
4. **Parent relative**: Wrapper needs `position: relative` for positioning context
5. **Z-index layers**: Use `z-10` or higher for overlays to appear above library content
6. **Single ownership**: Each DOM subtree has ONE owner (React OR third-party, never both)

### When This Applies

- Google Maps (`@googlemaps/js-api-loader`)
- Leaflet maps
- D3.js visualizations
- Three.js / React Three Fiber (for custom DOM overlays)
- Any library that calls `appendChild`, `removeChild`, or `innerHTML`

---

## Toast Notifications (Never `window.alert`)

**RULE: Never use `window.alert()`. Always use toast notifications.**

```typescript
// Using Sonner (recommended)
import { toast } from 'sonner';

// Success
toast.success('Event created successfully!');

// Error
toast.error('Failed to save changes');

// With action
toast('Event deleted', {
  action: {
    label: 'Undo',
    onClick: () => restoreEvent(eventId),
  },
});

// Promise-based (shows loading, success, error automatically)
toast.promise(createEvent(data), {
  loading: 'Creating event...',
  success: 'Event created!',
  error: 'Failed to create event',
});
```

---

## Related Skills

For foundational principles and backend patterns, see:

- **[Fundamental Principles](../Fundamentals/SKILL.md)** - Core coding principles, error handling, immutability
- **[Backend Patterns](../Backend/Skill.md)** - Database design, RLS, API architecture, Supabase

---

## Summary

**Write code that is:**
- 📱 Responsive (mobile-first, fluid, tested)
- ♿ Accessible (semantic, keyboard-friendly, screen-reader compatible)
- ⚡ Performant (optimized, lazy-loaded, cached)
- 🧪 Testable (small components, pure functions, good separation)
- 📖 Readable (consistent naming, proper comments, self-documenting)
- 🔒 Secure (validated input, no XSS, updated dependencies)
- 🔄 Maintainable (DRY, KISS, proper abstraction)

**When in doubt:**
1. Start simple
2. Make it work
3. Make it right
4. Make it fast (only if needed)
