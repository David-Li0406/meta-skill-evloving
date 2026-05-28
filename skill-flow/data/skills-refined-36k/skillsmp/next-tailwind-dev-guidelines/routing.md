# Next.js App Router Patterns

## File-Based Routing

Next.js 15 uses the App Router with file-based routing:

```
src/app/
├── layout.tsx          # Root layout (wraps all pages)
├── page.tsx            # Home page (/)
├── bundle/
│   └── page.tsx        # Bundle page (/bundle)
├── not-found.tsx       # 404 page
└── error.tsx           # Error boundary
```

### Route Segments

- `page.tsx`: Page component (required for routes)
- `layout.tsx`: Shared layout wrapper
- `loading.tsx`: Loading UI (automatic Suspense boundary)
- `error.tsx`: Error boundary
- `not-found.tsx`: 404 page

## Layouts

### Root Layout

```typescript
// src/app/layout.tsx
import { QueryProvider } from '@/providers/QueryProvider';
import { SimpleWeb3Provider } from '@/providers/SimpleWeb3Provider';
import { WalletProvider } from '@/providers/WalletProvider';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="bg-gray-950 text-white">
        <QueryProvider>
          <SimpleWeb3Provider>
            <WalletProvider>
              <Header />
              <main className="min-h-screen">{children}</main>
              <Footer />
            </WalletProvider>
          </SimpleWeb3Provider>
        </QueryProvider>
      </body>
    </html>
  );
}
```

### Nested Layouts

```typescript
// src/app/dashboard/layout.tsx
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 p-8">
        {children}
      </div>
    </div>
  );
}
```

## Page Components

### Static Pages

```typescript
// src/app/page.tsx
export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1>Welcome to Zap Pilot</h1>
      <PortfolioOverview />
    </div>
  );
}
```

### Client Components

Use `'use client'` directive for components that need interactivity:

```typescript
// src/app/bundle/page.tsx
'use client';

import { useSearchParams } from 'next/navigation';

export default function BundlePage() {
  const searchParams = useSearchParams();
  const userId = searchParams.get('userId');

  if (!userId) {
    return <div>Invalid bundle URL</div>;
  }

  return <BundlePageClient userId={userId} />;
}
```

## Navigation

### Link Component

```typescript
import Link from 'next/link';

export function Navigation() {
  return (
    <nav>
      <Link
        href="/"
        className="text-purple-400 hover:text-purple-300"
      >
        Home
      </Link>
      <Link href="/bundle">Bundles</Link>
    </nav>
  );
}
```

### Programmatic Navigation

```typescript
'use client';

import { useRouter } from 'next/navigation';

export function CreateBundleButton() {
  const router = useRouter();

  const handleCreate = async () => {
    const bundle = await createBundle();
    router.push(`/bundle?userId=${bundle.userId}`);
  };

  return <button onClick={handleCreate}>Create Bundle</button>;
}
```

### URL Search Params

```typescript
'use client';

import { useSearchParams, usePathname, useRouter } from 'next/navigation';

export function FilterControls() {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();

  const updateFilter = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams);
    params.set(key, value);
    router.push(`${pathname}?${params.toString()}`);
  };

  return (
    <select onChange={(e) => updateFilter('status', e.target.value)}>
      <option value="all">All</option>
      <option value="active">Active</option>
    </select>
  );
}
```

## Dynamic Routes

### Route Parameters

```typescript
// src/app/pool/[id]/page.tsx
interface PoolPageProps {
  params: { id: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default function PoolPage({ params }: PoolPageProps) {
  return <PoolDetails poolId={params.id} />;
}
```

### Catch-All Routes

```typescript
// src/app/docs/[...slug]/page.tsx
interface DocsPageProps {
  params: { slug: string[] };
}

export default function DocsPage({ params }: DocsPageProps) {
  const path = params.slug.join('/');
  return <Documentation path={path} />;
}
```

## Loading States

### loading.tsx

```typescript
// src/app/bundle/loading.tsx
export default function Loading() {
  return (
    <div className="container mx-auto px-4 py-8">
      <BundleSkeleton />
    </div>
  );
}
```

### Streaming with Suspense

```typescript
import { Suspense } from 'react';

export default function BundlePage() {
  return (
    <div>
      <h1>Portfolio Bundle</h1>
      <Suspense fallback={<PortfolioSkeleton />}>
        <PortfolioData />
      </Suspense>
      <Suspense fallback={<PoolsSkeleton />}>
        <PoolsData />
      </Suspense>
    </div>
  );
}
```

## Error Handling

### error.tsx

```typescript
// src/app/error.tsx
'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Application error:', error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
      <p className="text-gray-400 mb-6">{error.message}</p>
      <button
        onClick={reset}
        className="px-4 py-2 bg-purple-600 rounded-lg hover:bg-purple-700"
      >
        Try again
      </button>
    </div>
  );
}
```

### not-found.tsx

```typescript
// src/app/not-found.tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-bold mb-4">404</h1>
      <p className="text-gray-400 mb-6">Page not found</p>
      <Link
        href="/"
        className="px-4 py-2 bg-purple-600 rounded-lg hover:bg-purple-700"
      >
        Return Home
      </Link>
    </div>
  );
}
```

## Metadata

### Static Metadata

```typescript
// src/app/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Zap Pilot - DeFi Portfolio Management',
  description: 'Intelligent portfolio analytics and intent-based trading',
  openGraph: {
    title: 'Zap Pilot',
    description: 'DeFi Portfolio Management',
    images: ['/og-image.png'],
  },
};

export default function HomePage() {
  return <div>...</div>;
}
```

### Dynamic Metadata

```typescript
// src/app/bundle/page.tsx
interface BundlePageProps {
  searchParams: { userId?: string };
}

export async function generateMetadata({ searchParams }: BundlePageProps): Promise<Metadata> {
  const userId = searchParams.userId;

  if (!userId) {
    return { title: "Bundle Not Found" };
  }

  const bundle = await getBundleData(userId);

  return {
    title: `${bundle.name}'s Portfolio | Zap Pilot`,
    description: `View ${bundle.name}'s DeFi portfolio`,
    openGraph: {
      title: `${bundle.name}'s Portfolio`,
      description: `Total Value: ${bundle.totalValue}`,
      images: [bundle.thumbnail],
    },
  };
}
```

## Route Groups

Use `(group)` syntax to organize routes without affecting URL:

```
src/app/
├── (marketing)/
│   ├── layout.tsx      # Marketing layout
│   ├── about/
│   │   └── page.tsx    # /about
│   └── pricing/
│       └── page.tsx    # /pricing
└── (app)/
    ├── layout.tsx      # App layout
    ├── dashboard/
    │   └── page.tsx    # /dashboard
    └── settings/
        └── page.tsx    # /settings
```

## Parallel Routes

```
src/app/
├── @analytics/
│   └── page.tsx
├── @portfolio/
│   └── page.tsx
└── layout.tsx          # Can render both slots
```

```typescript
// src/app/layout.tsx
export default function Layout({
  children,
  analytics,
  portfolio,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  portfolio: React.ReactNode;
}) {
  return (
    <div>
      <div>{analytics}</div>
      <div>{portfolio}</div>
      <div>{children}</div>
    </div>
  );
}
```

## Intercepting Routes

```
src/app/
├── feed/
│   └── page.tsx        # /feed
├── photo/
│   └── [id]/
│       └── page.tsx    # /photo/123
└── @modal/
    └── (.)photo/       # Intercepts /photo/123 when navigating from /feed
        └── [id]/
            └── page.tsx
```

## Middleware

```typescript
// middleware.ts (project root)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth-token");

  if (!token && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
```

## Static Export Configuration

This project uses static export for deployment:

```typescript
// next.config.ts
const nextConfig = {
  output: "export",
  trailingSlash: true,
  images: {
    unoptimized: true, // Required for static export
  },
};
```

### Limitations with Static Export

- No server-side rendering (SSR)
- No API routes
- No dynamic routes at runtime (must use `generateStaticParams`)
- No Image Optimization (use `unoptimized: true`)

## Best Practices

1. **Use `'use client'` sparingly**: Keep server components by default
2. **Colocation**: Keep related components near their routes
3. **Loading states**: Always provide loading.tsx for better UX
4. **Error boundaries**: Implement error.tsx for graceful error handling
5. **Metadata**: Always set appropriate metadata for SEO
6. **Link prefetching**: Next.js automatically prefetches Link targets
7. **Route handlers**: Use for API-like endpoints (limited in static export)
