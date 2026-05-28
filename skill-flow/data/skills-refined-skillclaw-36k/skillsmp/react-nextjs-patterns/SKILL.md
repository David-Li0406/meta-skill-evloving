---
name: react-nextjs-patterns
description: Best practices for React 19 and Next.js 16 App Router. Use when creating components, hooks, or pages. Enforces server-first rendering, proper client boundaries, and modern React patterns.
---

# React 19 & Next.js 16 Best Practices

This skill enforces modern React and Next.js patterns for this project. Follow these guidelines to ensure optimal performance, proper server/client boundaries, and idiomatic code.

---

## 🎯 Core Principles

1. **Server-First**: Default to Server Components
2. **Minimal Client**: Add `"use client"` only at leaf components
3. **No Legacy Patterns**: Use App Router conventions, not Pages Router
4. **Modern React**: Use React 19 features (use hook, actions, etc.)

---

## 📦 Server Components (Default)

### ✅ When to Use Server Components

- Data fetching
- Accessing backend resources
- Rendering static content
- SEO-critical content
- Any component that doesn't need:
  - `useState`
  - `useEffect`
  - Browser APIs
  - Event handlers (onClick, onChange, etc.)

### Example: Server Component (Default)

```typescript
// app/[place]/page.tsx - Server Component by default
import { fetchEvents } from "@lib/api/events";
import { EventList } from "@components/ui/events/EventList";

export default async function PlacePage({
  params,
}: {
  params: { place: string };
}) {
  const events = await fetchEvents({ place: params.place });

  return (
    <main>
      <h1 className="heading-1">{params.place}</h1>
      <EventList events={events} />
    </main>
  );
}
```

**Key Points:**

- No `"use client"` directive
- Can use `async/await` directly
- Data fetching at component level
- Pass data down to children

---

## 🖥️ Client Components (Minimal)

### ✅ When to Add `"use client"`

**ONLY add `"use client"` when you need:**

- `useState`, `useReducer`
- `useEffect`, `useLayoutEffect`
- Browser APIs (`window`, `document`, `localStorage`)
- Event handlers (onClick, onChange, onSubmit)
- Third-party libraries that require client-side

### ✅ Pattern: Small Client Boundaries

```typescript
// ❌ WRONG: Large client component
"use client";

export function EventPage({ events }) {
  const [filter, setFilter] = useState("all");

  return (
    <div>
      <h1>Events</h1> {/* Could be server-rendered */}
      <p>Description...</p> {/* Could be server-rendered */}
      <FilterSelect value={filter} onChange={setFilter} /> {/* Needs client */}
      <EventList events={events} filter={filter} /> {/* Could be partially server */}
    </div>
  );
}
```

```typescript
// ✅ CORRECT: Small client boundary at leaf
// components/ui/filters/FilterSelect.tsx
"use client";

import type { FilterSelectProps } from "types/props";

export function FilterSelect({ value, onChange }: FilterSelectProps) {
  return (
    <select value={value} onChange={(e) => onChange(e.target.value)}>
      <option value="all">All</option>
      <option value="free">Free</option>
    </select>
  );
}

// app/[place]/page.tsx - Server Component
import { FilterSelect } from "@components/ui/filters/FilterSelect";

export default async function PlacePage() {
  const events = await fetchEvents();

  return (
    <div>
      <h1>Events</h1> {/* Server-rendered */}
      <p>Description...</p> {/* Server-rendered */}
      <FilterSelect /> {/* Client island */}
      <EventList events={events} /> {/* Server-rendered */}
    </div>
  );
}
```

---

## 🔗 Link Component (i18n)

### ⚠️ CRITICAL: Always Use i18n Link

```typescript
// ❌ WRONG: Using next/link directly
import Link from "next/link";

<Link href="/barcelona">Barcelona</Link>; // Loses locale!

// ✅ CORRECT: Using i18n routing Link
import { Link } from "@i18n/routing";

<Link href="/barcelona">Barcelona</Link>; // Auto locale handling
```

**ESLint warns** on `import Link from 'next/link'` - use `@i18n/routing` instead.

---

## 🪝 Hooks Best Practices

### useRef vs useState for Flags

```typescript
// ❌ WRONG: useState for tracking flags (causes re-render)
const [hasTracked, setHasTracked] = useState(false);

useEffect(() => {
  if (!hasTracked) {
    trackAnalytics();
    setHasTracked(true); // Causes unnecessary re-render!
  }
}, [hasTracked]);

// ✅ CORRECT: useRef for tracking flags (no re-render)
const hasTracked = useRef(false);

useEffect(() => {
  if (!hasTracked.current) {
    trackAnalytics();
    hasTracked.current = true; // No re-render
  }
}, []); // Refs don't need to be in dependencies
```

### Dependency Arrays

```typescript
// ❌ WRONG: Missing dependencies
useEffect(() => {
  fetchData(userId); // userId missing from deps!
}, []);

// ✅ CORRECT: Complete dependencies
useEffect(() => {
  fetchData(userId);
}, [userId]);

// ✅ CORRECT: Refs don't need to be in deps
const isMounted = useRef(true);
useEffect(() => {
  if (isMounted.current) {
    fetchData();
  }
}, []); // isMounted is stable, not needed in deps
```

### Memoization (Don't Over-Optimize)

```typescript
// ❌ WRONG: Premature optimization
const formattedDate = useMemo(() => date.toLocaleDateString(), [date]);

// ✅ CORRECT: Only memoize expensive computations
const sortedEvents = useMemo(
  () => events.sort((a, b) => new Date(a.date) - new Date(b.date)),
  [events]
);

// ✅ CORRECT: useCallback for callbacks passed to children
const handleClick = useCallback(() => {
  setCount((c) => c + 1);
}, []); // Stable reference for memoized children
```

---

## 🚫 Forbidden Patterns

### ❌ No `next/dynamic` with `ssr: false` in Server Components

```typescript
// ❌ WRONG: Dynamic import in Server Component
import dynamic from "next/dynamic";

const ClientComponent = dynamic(() => import("./ClientComponent"), {
  ssr: false,
});

export default function ServerPage() {
  return <ClientComponent />; // ERROR!
}

// ✅ CORRECT: Import client component directly
import { ClientComponent } from "./ClientComponent"; // Has "use client"

export default function ServerPage() {
  return <ClientComponent />; // Works!
}
```

### ❌ No Reading `searchParams` in Listing Pages

```typescript
// ❌ WRONG: Reading searchParams makes page dynamic ($300 cost spike!)
export default function PlacePage({
  params,
  searchParams, // FORBIDDEN in app/[place]/*
}: {
  params: { place: string };
  searchParams: { search?: string };
}) {
  const events = await fetchEvents({ search: searchParams.search });
  // Creates DynamoDB entry for EVERY unique URL+query!
}

// ✅ CORRECT: Handle query params client-side with SWR
// app/[place]/page.tsx (Server Component)
export default async function PlacePage({
  params,
}: {
  params: { place: string };
}) {
  const events = await fetchEvents({ place: params.place }); // Static (ISR)
  return <EventsPageClient initialEvents={events} />;
}

// components/EventsPageClient.tsx
("use client");

export function EventsPageClient({ initialEvents }) {
  const searchParams = useSearchParams();
  const { data } = useSWR(
    `/api/events?search=${searchParams.get("search") || ""}`,
    fetcher
  );
  return <EventList events={data || initialEvents} />;
}
```

### ❌ No Legacy Pages Router Patterns

```typescript
// ❌ WRONG: getServerSideProps (Pages Router)
export async function getServerSideProps() {
  const events = await fetchEvents();
  return { props: { events } };
}

// ✅ CORRECT: Direct data fetching (App Router)
export default async function Page() {
  const events = await fetchEvents();
  return <EventList events={events} />;
}
```

---

## 📝 Component Structure Template

```typescript
// components/ui/feature/MyComponent.tsx

// 1. Client directive FIRST (only if needed - must be before any imports)
"use client";

// 2. Imports (grouped)
import type { MyComponentProps } from "types/props";
import { useCallback, useState } from "react";
import { Link } from "@i18n/routing";
import { formatDate } from "@utils/date-helpers";

// 3. Component
export function MyComponent({ title, items, onSelect }: MyComponentProps) {
  // 4. State/hooks at top
  const [selected, setSelected] = useState<string | null>(null);

  // 5. Callbacks (memoized if passed to children)
  const handleSelect = useCallback(
    (id: string) => {
      setSelected(id);
      onSelect?.(id);
    },
    [onSelect]
  );

  // 6. Early returns for edge cases
  if (items.length === 0) {
    return <p className="body-normal text-foreground/60">No items</p>;
  }

  // 7. Main render
  return (
    <div className="card-bordered">
      <h2 className="heading-3">{title}</h2>
      <ul className="stack">
        {items.map((item) => (
          <li key={item.id}>
            <button onClick={() => handleSelect(item.id)}>{item.name}</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 🔄 Data Fetching Patterns

### Server Component (Recommended)

```typescript
// Direct async/await in component
export default async function EventsPage() {
  const events = await fetchEvents(); // Server-side
  return <EventList events={events} />;
}
```

### Client Component with SWR

```typescript
"use client";

import useSWR from "swr";
import { getInternalApiUrl } from "@utils/api-helpers";

export function EventsFeed({ place }: { place: string }) {
  const { data, error, isLoading } = useSWR(
    getInternalApiUrl("/api/events", { place }),
    fetcher
  );

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage />;

  return <EventList events={data?.content || []} />;
}
```

### Hybrid Pattern (SSR + Client Enhancement)

```typescript
// Server Component fetches initial data
export default async function PlacePage({ params }) {
  const events = await fetchEvents({ place: params.place });

  return (
    <>
      {/* Static SSR list */}
      <EventList events={events} />

      {/* Client enhancement for infinite scroll */}
      <ClientInfiniteScroll initialEvents={events} place={params.place} />
    </>
  );
}
```

---

## ✅ Checklist Before Committing

- [ ] Server Components by default (no `"use client"` unless necessary)
- [ ] Client boundaries at smallest possible scope
- [ ] Using `Link` from `@i18n/routing` (not `next/link`)
- [ ] No `searchParams` in `app/[place]/*` pages
- [ ] `useRef` for tracking flags (not `useState`)
- [ ] Complete dependency arrays in hooks
- [ ] No premature memoization
- [ ] Props types in `types/props.ts`
- [ ] Following design system classes (see `design-system-conventions` skill)

---

## 🆕 React 19 Features (Use When Appropriate)

### `use` Hook (Suspense Integration)

```typescript
import { use } from "react";

function EventDetails({ eventPromise }) {
  const event = use(eventPromise); // Suspends until resolved
  return <h1>{event.title}</h1>;
}
```

### Server Actions

```typescript
// actions.ts
"use server";

export async function createEvent(formData: FormData) {
  const title = formData.get("title");
  await db.events.create({ title });
  revalidatePath("/events");
}

// component
<form action={createEvent}>
  <input name="title" />
  <button type="submit">Create</button>
</form>;
```

---

**Remember**: Server-first, minimal client boundaries, modern patterns.

**Last Updated**: January 15, 2026
