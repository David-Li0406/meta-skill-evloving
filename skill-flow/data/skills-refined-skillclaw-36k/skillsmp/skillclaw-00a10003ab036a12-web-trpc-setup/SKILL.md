---
name: web-trpc-setup
description: Use this skill when you need to set up tRPC queries and mutations in web components, ensuring proper typing, React Query integration, and error handling.
---

# Skill body

## When to Use
- Adding data fetching to a web page
- Creating new tRPC queries or mutations
- Setting up React Query with tRPC
- Implementing optimistic updates and form submissions

## What This Skill Does
1. Analyzes data requirements to determine if a query or mutation is needed.
2. Generates proper tRPC hooks usage:
   - `useQuery` for fetching data
   - `useMutation` for submitting data
   - Configures options like `staleTime` and `enabled`.
3. Handles loading, error, and success states.
4. Sets up cache invalidation for mutations.

## Query Pattern

### Basic Query
```typescript
"use client";

import { trpc } from "@/lib/trpc";

export function ActivitiesList() {
  const { data, isLoading, error, refetch } = trpc.activities.list.useQuery(
    { limit: 20, offset: 0 },
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    }
  );

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorAlert message={error.message} onRetry={refetch} />;

  return (
    <div className="grid gap-4">
      {data?.map((activity) => (
        <ActivityCard key={activity.id} activity={activity} />
      ))}
    </div>
  );
}
```

### Query with Parameters
```typescript
export function ActivityDetail({ id }: { id: string }) {
  const { data: activity, isLoading, error } = trpc.activities.getById.useQuery(
    { id },
    {
      enabled: !!id, // Only run when id exists
      staleTime: 1 * 60 * 1000, // 1 minute
    }
  );

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorAlert message={error.message} />;
  if (!activity) return <NotFound />;

  return <ActivityDetailView activity={activity} />;
}
```

### Dependent Queries
```typescript
// Query B depends on Query A
export function UserActivities() {
  const { data: profile } = trpc.profiles.getCurrent.useQuery();

  const { data: activities, isLoading } = trpc.activities.list.useQuery(
    { userId: profile?.id! },
    {
      enabled: !!profile?.id, // Only run when profile loaded
    }
  );

  if (isLoading) return <Skeleton />;

  return <ActivityList activities={activities} />;
}
```

## Mutation Pattern

### Basic Mutation
```typescript
"use client";

import { trpc } from "@/lib/trpc";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

export function CreateActivityForm() {
  const router = useRouter();
  const utils = trpc.useUtils();

  const mutation = trpc.activities.create.useMutation({
    onSuccess: () => {
      utils.activities.list.invalidate();
      toast.success("Activity created");
      router.push("/activities");
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });

  // Form submission logic goes here
}
```

## Error Handling
```typescript
if (isLoading) return <Skeleton />;
if (error) return <ErrorAlert message={error.message} onRetry={refetch} />;
```

## Loading States
```typescript
import { Skeleton } from '@/components/ui/skeleton';

function ActivityList() {
  const { data, isLoading } = trpc.activities.list.useQuery();

  if (isLoading) {
    return (
      <View className="p-4">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-24 mb-4" />
        ))}
      </View>
    );
  }

  return <ActivityListView activities={data} />;
}
```

## Cache Invalidation
```typescript
// Invalidate after mutation
utils.activities.list.invalidate();

// Invalidate specific item
utils.activities.getById.invalidate({ id });
```