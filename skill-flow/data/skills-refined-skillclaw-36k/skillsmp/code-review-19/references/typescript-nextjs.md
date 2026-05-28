# Next.js Code Review Guide

Review points specific to Next.js App Router (14+).

## Server vs Client Components

### Default: Server Components

```typescript
// Server Component (default) - no directive needed
// Can be async, can fetch data directly
async function UserList() {
  const users = await fetchUsers();  // Direct data fetching

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Client Components

```typescript
'use client';  // Required for client interactivity

import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);  // Uses React state

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

### When to Use Client Components

Use `'use client'` when:
- Using React hooks (`useState`, `useEffect`, etc.)
- Using browser APIs (`window`, `document`)
- Adding event listeners (`onClick`, `onChange`)
- Using React Context

### Composition Pattern

```typescript
// Server Component - fetches data
async function UserProfile({ userId }: { userId: string }) {
  const user = await fetchUser(userId);

  return (
    <div>
      <UserHeader user={user} />
      <UserActions userId={user.id} />  {/* Client component */}
    </div>
  );
}

// Client Component - handles interactivity
'use client';

function UserActions({ userId }: { userId: string }) {
  return (
    <button onClick={() => follow(userId)}>
      Follow
    </button>
  );
}
```

## Data Fetching

### Server-Side Fetching

```typescript
// In Server Components - recommended
async function ProductPage({ params }: { params: { id: string } }) {
  const product = await fetch(`/api/products/${params.id}`, {
    cache: 'force-cache',  // Cache by default
  }).then((r) => r.json());

  return <ProductDetails product={product} />;
}
```

### Caching Options

```typescript
// Cache forever (default for GET requests)
fetch(url, { cache: 'force-cache' });

// Revalidate every 60 seconds
fetch(url, { next: { revalidate: 60 } });

// No caching
fetch(url, { cache: 'no-store' });

// Tag-based revalidation
fetch(url, { next: { tags: ['products'] } });
```

### Parallel Data Fetching

```typescript
// Sequential - slower
async function Page() {
  const user = await fetchUser();
  const posts = await fetchPosts();  // Waits for user
}

// Parallel - faster
async function Page() {
  const [user, posts] = await Promise.all([
    fetchUser(),
    fetchPosts(),
  ]);
}
```

## Route Handlers

### API Routes

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('query');

  const users = await fetchUsers(query);

  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  // Validate body
  if (!isValidUserInput(body)) {
    return NextResponse.json(
      { error: 'Invalid input' },
      { status: 400 }
    );
  }

  const user = await createUser(body);

  return NextResponse.json(user, { status: 201 });
}
```

### Dynamic Route Params

```typescript
// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await fetchUser(params.id);

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(user);
}
```

## Loading and Error States

### Loading UI

```typescript
// app/users/loading.tsx
export default function Loading() {
  return <div>Loading users...</div>;
}

// Or with Suspense boundary
import { Suspense } from 'react';

function Page() {
  return (
    <Suspense fallback={<Loading />}>
      <UserList />
    </Suspense>
  );
}
```

### Error Handling

```typescript
// app/users/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

## Server Actions

### Form Handling

```typescript
// Server Action
async function createUser(formData: FormData) {
  'use server';

  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  await db.user.create({ data: { name, email } });

  revalidatePath('/users');
  redirect('/users');
}

// Usage in form
function CreateUserForm() {
  return (
    <form action={createUser}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

### With Client State

```typescript
'use client';

import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Saving...' : 'Save'}
    </button>
  );
}
```

## Review Checklist

### Component Classification
- [ ] Server Components used by default
- [ ] `'use client'` only where needed
- [ ] No hooks in Server Components
- [ ] Data fetching in Server Components

### Data Fetching
- [ ] Parallel fetching where possible
- [ ] Appropriate caching strategy
- [ ] Error handling for fetches
- [ ] Loading states defined

### Route Handlers
- [ ] Input validation
- [ ] Proper status codes
- [ ] Error responses

### Server Actions
- [ ] Proper validation
- [ ] Revalidation after mutations
- [ ] Appropriate redirects

### Performance
- [ ] No unnecessary client bundles
- [ ] Static generation where possible
- [ ] Dynamic imports for large components

## Common Issues

### 1. Using Hooks in Server Components

```typescript
// WRONG - Server Component can't use hooks
async function UserList() {
  const [users, setUsers] = useState([]);  // Error!
}

// CORRECT - Use Client Component for state
'use client';
function UserList() {
  const [users, setUsers] = useState([]);
}

// OR - Fetch in Server Component
async function UserList() {
  const users = await fetchUsers();  // No state needed
}
```

### 2. Fetching on Client When Server Would Work

```typescript
// INEFFICIENT - Client-side fetch
'use client';
function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers);
  }, []);
}

// BETTER - Server Component
async function UserList() {
  const users = await fetchUsers();
  return <UserListClient users={users} />;
}
```

### 3. Overly Large Client Bundles

```typescript
// BAD - Entire component tree is client
'use client';
function Page() {
  return (
    <div>
      <Header />
      <Navigation />
      <Content />  {/* Only this needs interactivity */}
      <Footer />
    </div>
  );
}

// GOOD - Only interactive part is client
function Page() {
  return (
    <div>
      <Header />
      <Navigation />
      <InteractiveContent />  {/* 'use client' in this file */}
      <Footer />
    </div>
  );
}
```
