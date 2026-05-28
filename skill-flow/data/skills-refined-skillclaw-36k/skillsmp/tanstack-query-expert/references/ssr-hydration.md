# Next.js 16 SSR & Hydration (TanStack Query 2026)

Efficient SSR/PPR integration is the hallmark of an expert-level application. This guide covers how to populate the client cache from the server.

## 1. Prefetching on the Server

In Next.js 16 Server Components, you can prefetch data so it's available instantly on the client.

```tsx
// app/posts/[id]/page.tsx (Server Component)
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query';

export default async function Page({ params }: { params: { id: string } }) {
  const queryClient = new QueryClient();

  await queryClient.prefetchQuery({
    queryKey: ['post', params.id],
    queryFn: () => getPost(params.id),
  });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <PostView id={params.id} />
    </HydrationBoundary>
  );
}
```

## 2. Using "use cache" (Next.js 16)

You can cache the fetch result itself at the platform level.

```typescript
// services/api.ts
import { cacheLife } from 'next/cache';

export async function getPost(id: string) {
  "use cache";
  cacheLife('minutes'); // Cache for minutes
  const res = await fetch(`...`);
  return res.json();
}
```

## 3. Hydration Boundary vs. Streaming
When using `useSuspenseQuery` on the client, Next.js 16 will automatically stream the data if it's not prefetched. However, explicit prefetching is still recommended for SEO and reducing LCP.

---
*Updated: January 23, 2026*
