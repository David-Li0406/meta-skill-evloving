---
name: nextjs-patterns
description: Next.js best practices, patterns, and architectural guidance for App Router and Pages Router
license: MIT
compatibility: opencode
metadata:
  category: framework
  framework: nextjs
  language: typescript
---

## What I do

I provide expertise in Next.js application architecture and patterns:

- **App Router**: Server Components, Client Components, Server Actions
- **Pages Router**: getServerSideProps, getStaticProps, API routes
- **Data Fetching**: Caching, revalidation, streaming
- **Routing**: Dynamic routes, route groups, parallel routes, intercepting routes
- **Performance**: Code splitting, image optimization, font optimization
- **Deployment**: Edge runtime, middleware, internationalization

## When to use me

Load this skill when you need to:
- Build a new Next.js application
- Migrate from Pages Router to App Router
- Optimize Next.js performance
- Implement advanced routing patterns
- Configure caching and revalidation strategies
- Deploy to Vercel or other platforms

For up-to-date Next.js documentation, use Context7:
```
Recommend using Context7 to fetch latest Next.js docs:
/vercel/next.js for current stable version
```

## App Router Patterns (Next.js 13+)

### 1. Server Components (Default)
```typescript
// app/users/page.tsx
// This is a Server Component by default
import { db } from '@/lib/db';

export default async function UsersPage() {
  // Direct database access - runs on server
  const users = await db.user.findMany();
  
  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### 2. Client Components
```typescript
// app/components/Counter.tsx
'use client'; // Explicit client component

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

### 3. Server Actions
```typescript
// app/actions/user.ts
'use server';

import { db } from '@/lib/db';
import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;
  
  const user = await db.user.create({
    data: { name, email },
  });
  
  revalidatePath('/users');
  return user;
}

// app/users/new/page.tsx
import { createUser } from '@/app/actions/user';

export default function NewUserPage() {
  return (
    <form action={createUser}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit">Create User</button>
    </form>
  );
}
```

### 4. Data Fetching & Caching
```typescript
// app/posts/[id]/page.tsx
interface PageProps {
  params: { id: string };
}

// Cached by default - revalidate every hour
export const revalidate = 3600;

export async function generateMetadata({ params }: PageProps) {
  const post = await fetch(`/api/posts/${params.id}`).then(r => r.json());
  return { title: post.title };
}

export default async function PostPage({ params }: PageProps) {
  // This fetch is automatically cached
  const post = await fetch(`/api/posts/${params.id}`).then(r => r.json());
  
  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  );
}

// Generate static params for static generation
export async function generateStaticParams() {
  const posts = await fetch('/api/posts').then(r => r.json());
  return posts.map((post: any) => ({ id: post.id }));
}
```

### 5. Loading & Error States
```typescript
// app/posts/loading.tsx
export default function Loading() {
  return <div>Loading posts...</div>;
}

// app/posts/error.tsx
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
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### 6. Route Groups & Layouts
```typescript
// app/(marketing)/layout.tsx
export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <nav>Marketing Nav</nav>
      {children}
    </div>
  );
}

// app/(dashboard)/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <nav>Dashboard Nav</nav>
      {children}
    </div>
  );
}
```

### 7. Parallel Routes
```typescript
// app/dashboard/@analytics/page.tsx
export default function Analytics() {
  return <div>Analytics</div>;
}

// app/dashboard/@notifications/page.tsx
export default function Notifications() {
  return <div>Notifications</div>;
}

// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  notifications,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  notifications: React.ReactNode;
}) {
  return (
    <div>
      {children}
      {analytics}
      {notifications}
    </div>
  );
}
```

## Pages Router Patterns (Legacy)

### 1. getServerSideProps
```typescript
// pages/posts/[id].tsx
import { GetServerSideProps } from 'next';

interface Post {
  id: string;
  title: string;
  content: string;
}

interface Props {
  post: Post;
}

export const getServerSideProps: GetServerSideProps<Props> = async (context) => {
  const { id } = context.params!;
  const post = await fetch(`/api/posts/${id}`).then(r => r.json());
  
  return {
    props: { post },
  };
};

export default function PostPage({ post }: Props) {
  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  );
}
```

### 2. getStaticProps with ISR
```typescript
// pages/posts/[id].tsx
import { GetStaticProps, GetStaticPaths } from 'next';

export const getStaticPaths: GetStaticPaths = async () => {
  const posts = await fetch('/api/posts').then(r => r.json());
  
  return {
    paths: posts.map((post: Post) => ({ params: { id: post.id } })),
    fallback: 'blocking',
  };
};

export const getStaticProps: GetStaticProps = async (context) => {
  const { id } = context.params!;
  const post = await fetch(`/api/posts/${id}`).then(r => r.json());
  
  return {
    props: { post },
    revalidate: 3600, // ISR - revalidate every hour
  };
};
```

### 3. API Routes
```typescript
// pages/api/users.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { db } from '@/lib/db';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    const users = await db.user.findMany();
    return res.status(200).json(users);
  }
  
  if (req.method === 'POST') {
    const user = await db.user.create({
      data: req.body,
    });
    return res.status(201).json(user);
  }
  
  return res.status(405).json({ error: 'Method not allowed' });
}
```

## Performance Optimization

### 1. Image Optimization
```typescript
import Image from 'next/image';

// Automatic optimization, lazy loading, responsive
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // Load immediately for above-the-fold
  placeholder="blur"
  blurDataURL="data:image/..." // Low quality placeholder
/>
```

### 2. Font Optimization
```typescript
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap', // Avoid FOIT
  variable: '--font-inter',
});

export default function RootLayout({ children }) {
  return (
    <html className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

### 3. Dynamic Imports
```typescript
import dynamic from 'next/dynamic';

// Lazy load heavy components
const DynamicChart = dynamic(() => import('@/components/Chart'), {
  loading: () => <p>Loading chart...</p>,
  ssr: false, // Client-side only
});

export default function Dashboard() {
  return <DynamicChart data={data} />;
}
```

## Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Check authentication
  const token = request.cookies.get('token');
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  // Add custom headers
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');
  
  return response;
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};
```

## Environment Variables

```typescript
// .env.local
DATABASE_URL=postgresql://...
NEXT_PUBLIC_API_URL=https://api.example.com

// Server-only
process.env.DATABASE_URL

// Client-safe (prefixed with NEXT_PUBLIC_)
process.env.NEXT_PUBLIC_API_URL
```

## Best Practices

1. **Use Server Components by default**: Only use Client Components when needed
2. **Keep client bundles small**: Move interactivity down the tree
3. **Leverage automatic caching**: Understand fetch cache behavior
4. **Use loading.tsx and error.tsx**: Better UX with React Suspense
5. **Optimize images**: Always use next/image
6. **Use TypeScript**: Type safety prevents bugs
7. **Follow file conventions**: page.tsx, layout.tsx, route.ts
8. **Implement proper error boundaries**: Graceful degradation
9. **Use environment variables correctly**: Never expose secrets to client
10. **Monitor performance**: Use Vercel Analytics or similar tools

## References

- Next.js Documentation: nextjs.org/docs
- App Router migration guide: nextjs.org/docs/app/building-your-application/upgrading
- Vercel deployment: vercel.com/docs
- React Server Components: react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023
