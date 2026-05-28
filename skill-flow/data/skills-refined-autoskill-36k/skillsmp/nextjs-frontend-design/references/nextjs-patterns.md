# Next.js App Router Patterns

Technical patterns for Next.js applications with TypeScript.

## Project Architecture

### Directory Structure (App Router)

```
src/
├── app/                    # App Router
│   ├── layout.tsx          # Root layout with fonts
│   ├── page.tsx            # Homepage
│   ├── globals.css         # Global styles + CSS variables
│   ├── (routes)/           # Route groups
│   └── api/                # API routes (when needed)
├── components/
│   ├── ui/                 # Reusable UI primitives
│   └── features/           # Feature-specific components
├── lib/                    # Utilities (cn, constants, validations)
├── hooks/                  # Custom React hooks
├── types/                  # TypeScript definitions
├── actions/                # Server Actions
└── services/               # External API integrations
```

---

## TypeScript Essentials

**Type everything explicitly**—avoid `any`:

```typescript
// Explicit interfaces
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

// Zod for runtime validation
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
});

type User = z.infer<typeof UserSchema>;
```

---

## Server vs Client Components

**Default to Server Components** unless you need:
- Event handlers (onClick, onChange)
- useState, useEffect, useReducer
- Browser APIs

```typescript
// Server Component (default) - async data fetching
async function UserProfile({ userId }: { userId: string }) {
  const user = await fetchUser(userId);
  return <ProfileCard user={user} />;
}

// Client Component - only when needed
'use client';
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

---

## Server Actions

```typescript
// actions/user.ts
'use server';
import { revalidatePath } from 'next/cache';
import { z } from 'zod';
import { auth } from '@/lib/auth'; // Your auth solution

const UpdateUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export async function updateUser(formData: FormData) {
  // CRITICAL: Always authenticate before processing
  const session = await auth();
  if (!session?.user) {
    return { error: 'Unauthorized' };
  }

  const validated = UpdateUserSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
  });

  if (!validated.success) {
    return { error: validated.error.flatten() };
  }

  await db.user.update({
    where: { id: session.user.id },
    data: validated.data
  });
  revalidatePath('/profile');
  return { success: true };
}
```

---

## Streaming & Suspense

Use `loading.tsx` and `<Suspense>` for instant navigation and progressive loading:

```typescript
// app/dashboard/loading.tsx - Automatic streaming boundary
export default function Loading() {
  return <DashboardSkeleton />;
}

// app/dashboard/page.tsx - Suspense for granular loading
import { Suspense } from 'react';

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <DashboardStats />
      </Suspense>
      <Suspense fallback={<TableSkeleton />}>
        <RecentActivity />
      </Suspense>
    </div>
  );
}

// Async server component - streams when ready
async function DashboardStats() {
  const stats = await fetchStats(); // Slow data fetch
  return <StatsGrid data={stats} />;
}
```

**Key patterns:**
- `loading.tsx` wraps entire route segment
- `<Suspense>` enables parallel data fetching with independent loading states
- Nest Suspense boundaries for progressive reveal

---

## Caching Strategy

Next.js has 4 cache layers—understand when to use each:

| Cache | Scope | Duration | Invalidate |
|-------|-------|----------|------------|
| Request Memoization | Single request | Request lifetime | Automatic |
| Data Cache | Server | Persistent | `revalidatePath`, `revalidateTag` |
| Full Route Cache | Server | Persistent (static) | Redeploy or revalidate |
| Router Cache | Client | Session | `router.refresh()` |

```typescript
// Static: cached indefinitely (default for static routes)
const data = await fetch('https://api.example.com/data');

// Revalidate every 60 seconds
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 60 }
});

// No cache: always fresh
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store'
});

// Tag-based invalidation
const data = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] }
});

// In a Server Action:
'use server';
import { revalidateTag, revalidatePath } from 'next/cache';

export async function createPost() {
  await db.post.create({ ... });
  revalidateTag('posts');      // Invalidate by tag
  revalidatePath('/posts');    // Invalidate by path
}
```

---

## Error Boundaries

Handle errors gracefully at route segment level:

```typescript
// app/dashboard/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 p-8">
      <h2 className="text-xl font-semibold">Something went wrong</h2>
      <p className="text-muted-foreground">{error.message}</p>
      <button onClick={reset} className="btn-primary">
        Try again
      </button>
    </div>
  );
}

// app/not-found.tsx - Custom 404
export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh]">
      <h1 className="text-4xl font-bold">404</h1>
      <p className="text-muted-foreground">Page not found</p>
    </div>
  );
}
```

---

## Accessibility Patterns

Distinctive design must be accessible.

### Keyboard Navigation

```typescript
// Focus management for modals/dialogs
'use client';
import { useEffect, useRef } from 'react';

function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousFocus.current = document.activeElement as HTMLElement;
      modalRef.current?.focus();
    }
    return () => {
      previousFocus.current?.focus(); // Restore focus on close
    };
  }, [isOpen]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') onClose();
  };

  if (!isOpen) return null;
  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={handleKeyDown}
    >
      {children}
    </div>
  );
}
```

### ARIA Patterns

```typescript
// Live regions for dynamic content
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {notification}
</div>

// Form error association
<label htmlFor="email">Email</label>
<input
  id="email"
  aria-invalid={!!error}
  aria-describedby={error ? 'email-error' : undefined}
/>
{error && <p id="email-error" role="alert">{error}</p>}

// Skip link for keyboard users
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

### Reduced Motion

```css
/* Always include */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Use primitives**: For complex interactions (dialogs, dropdowns, tabs), use [Radix UI](https://radix-ui.com) or [React Aria](https://react-spectrum.adobe.com/react-aria/) which handle keyboard, focus, and ARIA correctly.
