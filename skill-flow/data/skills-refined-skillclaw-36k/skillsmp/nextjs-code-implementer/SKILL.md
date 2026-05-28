---
name: nextjs-code-implementer
description: Practical guidelines for implementing Next.js 15 applications with App Router
---

# Next.js Code Implementation

## App Router Fundamentals

### File Structure

File-based routing with app directory:

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── about/
│   └── page.tsx        # /about route
├── blog/
│   ├── page.tsx        # /blog route
│   └── [slug]/
│       └── page.tsx    # /blog/[slug] dynamic route
└── api/
    └── users/
        └── route.ts    # API route handler
```

### Special Files

| File | Purpose |
|------|---------|
| layout | Shared UI for route segment and its children |
| page | Unique UI for a route |
| loading | Loading UI with Suspense |
| error | Error boundary for route segment |
| not-found | 404 UI for route segment |
| route | API endpoint handler |

## Page Implementation

### Server Component Page

Default - fetches data on server:

```tsx
// app/blog/page.tsx
import { BlogList } from '@/components/blog/BlogList';

interface BlogPageProps {
  searchParams: { page?: string };
}

export default async function BlogPage({ searchParams }: BlogPageProps) {
  const page = Number(searchParams.page) || 1;
  const posts = await fetchBlogPosts(page);

  return (
    <div>
      <h1>Blog</h1>
      <BlogList posts={posts} />
    </div>
  );
}

// Generate static params for static generation
export async function generateStaticParams() {
  return [{ page: '1' }, { page: '2' }];
}

// Generate metadata
export async function generateMetadata(): Promise<Metadata> {
  return {
    title: 'Blog - My Site',
    description: 'Latest blog posts',
  };
}
```

### Client Component Page

Use when interactivity needed at root:

```tsx
'use client';

import { useState } from 'react';
import { useSearchParams } from 'next/navigation';

export default function InteractivePage() {
  const [filter, setFilter] = useState('all');
  const searchParams = useSearchParams();

  return (
    <div>
      <FilterControls value={filter} onChange={setFilter} />
      <ContentList filter={filter} />
    </div>
  );
}
```

### Dynamic Routes

```tsx
// app/blog/[slug]/page.tsx
interface PageProps {
  params: { slug: string };
}

export default async function BlogPost({ params }: PageProps) {
  const post = await fetchPost(params.slug);

  if (!post) {
    notFound(); // Shows not-found.tsx
  }

  return <article>{/* render post */}</article>;
}

// Generate static paths
export async function generateStaticParams() {
  const posts = await fetchAllPosts();
  return posts.map((post) => ({ slug: post.slug }));
}
```

## Layout Implementation

### Root Layout

Required at app root - wraps all pages:

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google';
import { Providers } from './providers';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'My App',
  description: 'App description',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <Header />
          <main>{children}</main>
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
```

### Nested Layout

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="dashboard">
      <Sidebar />
      <main>{children}</main>
    </div>
  );
}
```

## Data Fetching

### Server Components

Direct async/await in component:

```tsx
async function UserProfile({ userId }: { userId: string }) {
  // Fetch happens on server
  const user = await db.user.findUnique({ where: { id: userId } });

  return <div>{user.name}</div>;
}
```

**Parallel Fetching:**
```tsx
async function Page() {
  const [users, posts] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
  ]);

  return <Dashboard users={users} posts={posts} />;
}
```

**Sequential Fetching:**
```tsx
async function Page({ params }: { params: { id: string } }) {
  const user = await fetchUser(params.id);
  const posts = await fetchUserPosts(user.id);

  return <UserProfile user={user} posts={posts} />;
}
```

### Client Components

Use React Query for client-side fetching:

```tsx
'use client';

import { useQuery } from '@tanstack/react-query';

export function UserList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const res = await fetch('/api/users');
      if (!res.ok) throw new Error('Failed to fetch');
      return res.json();
    },
  });

  if (isLoading) return <LoadingSkeleton />;
  if (error) return <ErrorMessage error={error} />;

  return <ul>{data.map(user => <UserItem key={user.id} user={user} />)}</ul>;
}
```

### Caching Strategies

| Strategy | Usage |
|----------|-------|
| `fetch(url, { cache: 'force-cache' })` | Cache forever (default) |
| `fetch(url, { cache: 'no-store' })` | Never cache, always fresh |
| `fetch(url, { next: { revalidate: 3600 } })` | Cache for 3600s |

## Loading States

### Loading File

Automatic loading UI with Suspense:

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
      <div className="h-64 bg-gray-200 rounded" />
    </div>
  );
}
```

### Suspense Boundaries

Granular loading states:

```tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <Statistics />
      </Suspense>
      <Suspense fallback={<ChartSkeleton />}>
        <Chart />
      </Suspense>
    </div>
  );
}
```

## Error Handling

### Error File

Error boundary for route segment:

```tsx
'use client'; // Error components must be Client Components

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Not Found

```tsx
// app/blog/[slug]/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>Post Not Found</h2>
      <p>Could not find the requested blog post.</p>
    </div>
  );
}
```

## API Routes

### Route Handlers

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const page = searchParams.get('page') || '1';

  const users = await db.user.findMany({
    skip: (Number(page) - 1) * 10,
    take: 10,
  });

  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  const user = await db.user.create({
    data: body,
  });

  return NextResponse.json(user, { status: 201 });
}
```

### Dynamic Routes

```tsx
// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await db.user.findUnique({
    where: { id: params.id },
  });

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(user);
}
```

## Server Actions

Server-side mutations:

```tsx
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  const post = await db.post.create({
    data: { title, content },
  });

  revalidatePath('/blog');
  return { success: true, post };
}
```

**Usage in Form:**
```tsx
// app/blog/new/page.tsx
import { createPost } from '@/app/actions';

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

## Metadata

### Static Metadata

```tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'My Page',
  description: 'Page description',
  openGraph: {
    title: 'My Page',
    description: 'Page description',
    images: ['/og-image.jpg'],
  },
};
```

### Dynamic Metadata

```tsx
export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Promise<Metadata> {
  const post = await fetchPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  };
}
```

## Image Optimization

```tsx
import Image from 'next/image';

<Image
  src="/profile.jpg"
  alt="Profile picture"
  width={500}
  height={500}
  priority // Load immediately for LCP
/>

// Remote images
<Image
  src="https://example.com/image.jpg"
  alt="Remote image"
  width={800}
  height={600}
  // Configure remote patterns in next.config.js
/>
```

## Middleware

```tsx
// middleware.ts (at project root)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Authentication check
  const token = request.cookies.get('token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: '/dashboard/:path*',
};
```

## Internationalization

### next-intl Setup

```tsx
// app/[locale]/layout.tsx
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

export default async function LocaleLayout({
  children,
  params: { locale },
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  const messages = await getMessages();

  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      {children}
    </NextIntlClientProvider>
  );
}
```

### Usage

```tsx
'use client';

import { useTranslations } from 'next-intl';

export function Welcome() {
  const t = useTranslations('HomePage');

  return <h1>{t('title')}</h1>;
}
```

## Best Practices Checklist

- [ ] Use Server Components by default
- [ ] Add 'use client' only when necessary
- [ ] Implement loading.tsx for loading states
- [ ] Implement error.tsx for error handling
- [ ] Use generateMetadata for SEO
- [ ] Optimize images with next/image
- [ ] Use server actions for mutations
- [ ] Implement proper caching strategies
- [ ] Handle not-found cases
- [ ] Use TypeScript for type safety
