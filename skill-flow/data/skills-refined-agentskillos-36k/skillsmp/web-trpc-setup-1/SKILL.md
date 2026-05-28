---
name: web-trpc-setup
description: Sets up tRPC queries and mutations in web components
---

# Web tRPC Setup Skill

## When to Use
- Adding data fetching to a web page
- Setting up mutations for forms
- Implementing optimistic updates
- Converting components to use tRPC

## What This Skill Does
1. Analyzes data requirements
2. Determines query vs mutation
3. Generates proper tRPC hooks usage:
   - `useQuery` for reads
   - `useMutation` for writes
   - Proper options (staleTime, enabled, etc.)
4. Adds loading and error states
5. Sets up cache invalidation

## Query Pattern

### Basic Query
```typescript
'use client';

import { trpc } from '@/lib/trpc';

export function ActivitiesList() {
  const { data, isLoading, error, refetch } = trpc.activities.list.useQuery(
    { limit: 20, offset: 0 },
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    }
  );

  if (isLoading) return <ActivityListSkeleton />;
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
'use client';

import { trpc } from '@/lib/trpc';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';

export function CreateActivityForm() {
  const router = useRouter();
  const utils = trpc.useUtils();

  const mutation = trpc.activities.create.useMutation({
    onSuccess: () => {
      utils.activities.list.invalidate();
      toast.success('Activity created successfully');
      router.push('/activities');
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });

  const handleSubmit = async (data: ActivityInput) => {
    await mutation.mutateAsync(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Creating...' : 'Create Activity'}
      </button>
    </form>
  );
}
```

### Mutation with Form Validation
```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { activitySchema } from '@repo/core/schemas';

export function ActivityForm() {
  const form = useForm({
    resolver: zodResolver(activitySchema),
    defaultValues: {
      name: '',
      type: 'run',
    },
  });

  const utils = trpc.useUtils();

  const mutation = trpc.activities.create.useMutation({
    onSuccess: () => {
      utils.activities.list.invalidate();
      toast.success('Activity created');
    },
    onError: (error) => {
      // Map Zod validation errors to form fields
      if (error.data?.zodError) {
        const fieldErrors = error.data.zodError.fieldErrors;
        Object.entries(fieldErrors).forEach(([field, messages]) => {
          form.setError(field as any, { message: messages?.[0] });
        });
      } else {
        toast.error(error.message);
      }
    },
  });

  const onSubmit = form.handleSubmit((data) => {
    mutation.mutate(data);
  });

  return (
    <Form {...form}>
      <form onSubmit={onSubmit}>
        {/* Form fields */}
      </form>
    </Form>
  );
}
```

## Optimistic Updates

### Optimistic Update Pattern
```typescript
export function ActivityActions({ activity }: { activity: Activity }) {
  const utils = trpc.useUtils();

  const updateMutation = trpc.activities.update.useMutation({
    onMutate: async (updatedActivity) => {
      // Cancel outgoing refetches
      await utils.activities.list.cancel();

      // Snapshot current value
      const previousActivities = utils.activities.list.getData();

      // Optimistically update to new value
      utils.activities.list.setData(undefined, (old) =>
        old?.map((act) =>
          act.id === updatedActivity.id ? { ...act, ...updatedActivity.data } : act
        )
      );

      // Return context with snapshot
      return { previousActivities };
    },
    onError: (err, updatedActivity, context) => {
      // Rollback on error
      utils.activities.list.setData(undefined, context?.previousActivities);
      toast.error(err.message);
    },
    onSettled: () => {
      // Refetch after error or success
      utils.activities.list.invalidate();
    },
  });

  return (
    <button onClick={() => updateMutation.mutate({ id: activity.id, data: { name: 'Updated' } })}>
      Update
    </button>
  );
}
```

## Cache Management

### Manual Cache Invalidation
```typescript
const utils = trpc.useUtils();

// Invalidate specific query
utils.activities.list.invalidate();

// Invalidate all activities queries
utils.activities.invalidate();

// Invalidate all queries
utils.invalidate();
```

### Manual Cache Updates
```typescript
// Get current data
const currentData = utils.activities.list.getData();

// Set new data
utils.activities.list.setData({ limit: 20 }, (old) => {
  return [...(old ?? []), newActivity];
});
```

## Common Options

### Query Options
```typescript
trpc.activities.list.useQuery(input, {
  // Caching
  staleTime: 5 * 60 * 1000,      // 5 minutes
  cacheTime: 10 * 60 * 1000,     // 10 minutes

  // Refetching
  refetchOnMount: false,          // Don't refetch on mount
  refetchOnWindowFocus: false,    // Don't refetch on focus
  refetchInterval: 30 * 1000,     // Refetch every 30s

  // Conditional execution
  enabled: !!someCondition,       // Only run if condition true

  // Callbacks
  onSuccess: (data) => { },
  onError: (error) => { },
});
```

### Mutation Options
```typescript
trpc.activities.create.useMutation({
  // Callbacks
  onSuccess: (data) => {
    utils.activities.list.invalidate();
    toast.success('Created');
  },
  onError: (error) => {
    toast.error(error.message);
  },
  onMutate: (variables) => {
    // Optimistic updates
  },
  onSettled: () => {
    // Always runs after success/error
  },
});
```

## Loading States

### Query Loading
```typescript
const { data, isLoading, isError, error } = trpc.activities.list.useQuery();

if (isLoading) return <Skeleton />;
if (isError) return <ErrorAlert message={error.message} />;

return <ActivityList activities={data} />;
```

### Mutation Loading
```typescript
const mutation = trpc.activities.create.useMutation();

<button disabled={mutation.isPending}>
  {mutation.isPending ? 'Creating...' : 'Create'}
</button>
```

## Error Handling

### Display Errors
```typescript
import { toast } from 'sonner';

const mutation = trpc.activities.create.useMutation({
  onError: (error) => {
    // Display user-friendly error
    toast.error(error.message);

    // Or handle specific error codes
    if (error.data?.code === 'UNAUTHORIZED') {
      router.push('/login');
    }
  },
});
```

### Retry Logic
```typescript
trpc.activities.list.useQuery(input, {
  retry: 3,                    // Retry 3 times
  retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
});
```

## Example Use Cases

### 1. List Page with Search
```typescript
const [search, setSearch] = useState('');
const [page, setPage] = useState(0);

const { data, isLoading } = trpc.activities.list.useQuery({
  search,
  limit: 20,
  offset: page * 20,
});
```

### 2. Form Submission
```typescript
const mutation = trpc.activities.create.useMutation({
  onSuccess: () => {
    utils.activities.list.invalidate();
    toast.success('Created');
    router.push('/activities');
  },
});

const handleSubmit = (data) => {
  mutation.mutate(data);
};
```

### 3. Delete with Confirmation
```typescript
const deleteMutation = trpc.activities.delete.useMutation({
  onSuccess: () => {
    utils.activities.list.invalidate();
    toast.success('Deleted');
  },
});

const handleDelete = () => {
  if (confirm('Are you sure?')) {
    deleteMutation.mutate({ id: activity.id });
  }
};
```

## Critical Patterns

- ✅ Always invalidate cache after mutations
- ✅ Use `enabled` for dependent queries
- ✅ Set appropriate `staleTime` for caching
- ✅ Handle loading and error states
- ✅ Show user feedback (toast notifications)
- ✅ Use `isPending` for loading states (not `isLoading`)
- ✅ Type inputs and outputs properly
