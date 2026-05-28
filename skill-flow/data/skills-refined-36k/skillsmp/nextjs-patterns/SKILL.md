---
name: nextjs-patterns
description: Next.js 15 App Router patterns and best practices for React applications. Use when creating pages, components, layouts, data fetching, server actions, or routing. Triggers on Next.js, App Router, page, layout, component, server component, client component, use client.
---

# Next.js 15 Patterns

Modern Next.js 15 App Router patterns for the Vibe4Vets frontend.

## When to Use

- Creating new pages or layouts
- Building React components
- Implementing data fetching
- Setting up routing
- Working with server/client components

## Core Concepts

### Server vs Client Components

```typescript
// Server Component (default) - runs on server only
// app/resources/page.tsx
import { api } from '@/lib/api';

export default async function ResourcesPage() {
  const resources = await api.getResources();
  return <ResourceList resources={resources} />;
}

// Client Component - runs in browser
// components/SearchInput.tsx
'use client';

import { useState } from 'react';

export function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('');

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      onKeyDown={(e) => e.key === 'Enter' && onSearch(query)}
    />
  );
}
```

### When to Use 'use client'

Add `'use client'` at the top of a file when using:
- React hooks (useState, useEffect, useContext, etc.)
- Browser APIs (localStorage, window, etc.)
- Event handlers (onClick, onChange, etc.)
- Third-party client libraries

## Vibe4Vets Page Patterns

### Search Page with URL State

```typescript
// app/search/page.tsx
import { Suspense } from 'react';
import { SearchResults } from '@/components/SearchResults';
import { SearchFilters } from '@/components/SearchFilters';

interface SearchPageProps {
  searchParams: Promise<{
    q?: string;
    category?: string;
    state?: string;
  }>;
}

export default async function SearchPage({ searchParams }: SearchPageProps) {
  const params = await searchParams;

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Search Resources</h1>

      <SearchFilters
        initialQuery={params.q}
        initialCategory={params.category}
        initialState={params.state}
      />

      <Suspense fallback={<SearchSkeleton />}>
        <SearchResults
          query={params.q}
          category={params.category}
          state={params.state}
        />
      </Suspense>
    </div>
  );
}
```

### Resource Detail Page

```typescript
// app/resources/[id]/page.tsx
import { notFound } from 'next/navigation';
import { api } from '@/lib/api';
import { ResourceDetail } from '@/components/ResourceDetail';

interface ResourcePageProps {
  params: Promise<{ id: string }>;
}

export default async function ResourcePage({ params }: ResourcePageProps) {
  const { id } = await params;
  const resource = await api.getResource(id);

  if (!resource) {
    notFound();
  }

  return <ResourceDetail resource={resource} />;
}

export async function generateMetadata({ params }: ResourcePageProps) {
  const { id } = await params;
  const resource = await api.getResource(id);

  return {
    title: resource?.name ?? 'Resource Not Found',
    description: resource?.description,
  };
}
```

### Hub Page (Static)

```typescript
// app/hubs/employment/page.tsx
import { HubCard } from '@/components/HubCard';
import { employmentResources } from '@/data/hubs/employment';

export const metadata = {
  title: 'Employment Resources | Vibe4Vets',
  description: 'Job placement, career services, and vocational training for veterans',
};

export default function EmploymentHubPage() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-2">Employment Resources</h1>
      <p className="text-muted-foreground mb-8">
        Job placement, career services, and vocational training for veterans
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {employmentResources.map((resource) => (
          <HubCard key={resource.id} resource={resource} />
        ))}
      </div>
    </div>
  );
}
```

## Component Patterns

### Card Component with shadcn/ui

```typescript
// components/ResourceCard.tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { MapPin, Phone, ExternalLink } from 'lucide-react';
import Link from 'next/link';

interface ResourceCardProps {
  resource: {
    id: number;
    name: string;
    description?: string;
    category: string;
    city?: string;
    state?: string;
    phone?: string;
    website?: string;
  };
}

export function ResourceCard({ resource }: ResourceCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <CardTitle className="text-lg">
            <Link href={`/resources/${resource.id}`} className="hover:underline">
              {resource.name}
            </Link>
          </CardTitle>
          <Badge variant="secondary">{resource.category}</Badge>
        </div>
        {resource.description && (
          <CardDescription className="line-clamp-2">
            {resource.description}
          </CardDescription>
        )}
      </CardHeader>
      <CardContent>
        <div className="flex flex-col gap-2 text-sm text-muted-foreground">
          {resource.city && resource.state && (
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4" />
              <span>{resource.city}, {resource.state}</span>
            </div>
          )}
          {resource.phone && (
            <div className="flex items-center gap-2">
              <Phone className="h-4 w-4" />
              <a href={`tel:${resource.phone}`} className="hover:underline">
                {resource.phone}
              </a>
            </div>
          )}
          {resource.website && (
            <div className="flex items-center gap-2">
              <ExternalLink className="h-4 w-4" />
              <a
                href={resource.website}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:underline truncate"
              >
                {new URL(resource.website).hostname}
              </a>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
```

### Filter Component with URL State

```typescript
// components/SearchFilters.tsx
'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { useCallback } from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Input } from '@/components/ui/input';

const CATEGORIES = ['employment', 'training', 'housing', 'legal'];
const STATES = ['TX', 'CA', 'FL', 'VA', 'DC', 'MD'];

interface SearchFiltersProps {
  initialQuery?: string;
  initialCategory?: string;
  initialState?: string;
}

export function SearchFilters({
  initialQuery,
  initialCategory,
  initialState,
}: SearchFiltersProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const updateParams = useCallback(
    (key: string, value: string | null) => {
      const params = new URLSearchParams(searchParams.toString());
      if (value) {
        params.set(key, value);
      } else {
        params.delete(key);
      }
      router.push(`/search?${params.toString()}`);
    },
    [router, searchParams]
  );

  return (
    <div className="flex flex-wrap gap-4 mb-6">
      <Input
        placeholder="Search resources..."
        defaultValue={initialQuery}
        className="w-full md:w-64"
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            updateParams('q', e.currentTarget.value);
          }
        }}
      />

      <Select
        defaultValue={initialCategory}
        onValueChange={(value) => updateParams('category', value)}
      >
        <SelectTrigger className="w-40">
          <SelectValue placeholder="Category" />
        </SelectTrigger>
        <SelectContent>
          {CATEGORIES.map((cat) => (
            <SelectItem key={cat} value={cat}>
              {cat.charAt(0).toUpperCase() + cat.slice(1)}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Select
        defaultValue={initialState}
        onValueChange={(value) => updateParams('state', value)}
      >
        <SelectTrigger className="w-32">
          <SelectValue placeholder="State" />
        </SelectTrigger>
        <SelectContent>
          {STATES.map((state) => (
            <SelectItem key={state} value={state}>
              {state}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
```

## Data Fetching Patterns

### API Client

```typescript
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Resource {
  id: number;
  name: string;
  description?: string;
  category: string;
  state?: string;
  city?: string;
  phone?: string;
  website?: string;
  trust_score: number;
}

export const api = {
  async getResources(params?: {
    category?: string;
    state?: string;
    limit?: number;
    offset?: number;
  }): Promise<Resource[]> {
    const searchParams = new URLSearchParams();
    if (params?.category) searchParams.set('category', params.category);
    if (params?.state) searchParams.set('state', params.state);
    if (params?.limit) searchParams.set('limit', String(params.limit));
    if (params?.offset) searchParams.set('offset', String(params.offset));

    const response = await fetch(
      `${API_URL}/api/v1/resources?${searchParams}`,
      { next: { revalidate: 300 } } // Cache for 5 minutes
    );

    if (!response.ok) throw new Error('Failed to fetch resources');
    return response.json();
  },

  async getResource(id: string): Promise<Resource | null> {
    const response = await fetch(`${API_URL}/api/v1/resources/${id}`, {
      next: { revalidate: 60 },
    });

    if (response.status === 404) return null;
    if (!response.ok) throw new Error('Failed to fetch resource');
    return response.json();
  },

  async search(query: string): Promise<Resource[]> {
    const response = await fetch(
      `${API_URL}/api/v1/search?q=${encodeURIComponent(query)}`,
      { next: { revalidate: 60 } }
    );

    if (!response.ok) throw new Error('Search failed');
    return response.json();
  },
};
```

## Layout Patterns

### Root Layout

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google';
import { Providers } from '@/components/providers';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Vibe4Vets - Veteran Resource Directory',
  description: 'AI-powered veteran resource database for employment, training, housing, and legal resources',
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
          <div className="flex min-h-screen flex-col">
            <Header />
            <main className="flex-1">{children}</main>
            <Footer />
          </div>
        </Providers>
      </body>
    </html>
  );
}
```

## Best Practices

### DO
- Use Server Components by default
- Add `'use client'` only when needed
- Colocate components with pages when page-specific
- Use URL state for filters/search
- Implement proper loading states with Suspense
- Use `next/image` for optimized images
- Use `next/link` for client-side navigation

### DON'T
- Add `'use client'` unnecessarily
- Fetch data in client components when server works
- Use `useEffect` for data fetching (use TanStack Query or server)
- Skip loading/error states
- Hardcode API URLs (use env vars)
- Forget to handle 404 cases
