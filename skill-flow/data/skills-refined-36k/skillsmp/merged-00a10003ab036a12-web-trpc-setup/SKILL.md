---
name: web-trpc-setup
description: Use this skill to set up tRPC queries and mutations in web components, including data fetching, error handling, and cache management.
---

# Web tRPC Setup Skill

## When to Use
- Adding data fetching to a web page or component
- Creating new tRPC queries or mutations
- Setting up form submissions with tRPC
- Implementing optimistic updates and cache management

## What This Skill Does
1. Analyzes data requirements and determines if a query or mutation is needed.
2. Generates proper tRPC hooks usage:
   - `useQuery` for data fetching
   - `useMutation` for data writing
   - Configures options like `staleTime`, `enabled`, etc.
3. Handles loading, error, and success states.
4. Implements cache invalidation for mutations and updates.
5. Provides TypeScript typing for procedures.

## Query Patterns

### Basic Query
```typescript
"use client";

import { trpc } from "@/lib/trpc";

export function ActivitiesList() {
  const { data, isLoading, error, refetch } = trpc.activities.list.useQuery(
    { limit: 20, offset: 0 },
    {
      staleTime: 5 * 60 * 1000,
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
      enabled: !!id,
      staleTime: 1 * 60 * 1000,
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
export function UserActivities() {
  const { data: profile } = trpc.profiles.getCurrent.useQuery();

  const { data: activities, isLoading } = trpc.activities.list.useQuery(
    { userId: profile?.id! },
    {
      enabled: !!profile?.id,
    }
  );

  if (isLoading) return <Skeleton />;

  return <ActivityList activities={activities} />;
}
```

## Mutation Patterns

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
      toast.success("Activity created successfully");
      router.push("/activities");
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
        {mutation.isPending ? "Creating..." : "Create Activity"}
      </button>
    </form>
  );
}
```

### Mutation with Form Validation
```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { activitySchema } from "@repo/core/schemas";

export function ActivityForm() {
  const form = useForm({
    resolver: zodResolver(activitySchema),
    defaultValues: {
      name: "",
      type: "run",
    },
  });

  const utils = trpc.useUtils();

  const mutation = trpc.activities.create.useMutation({
    onSuccess: () => {
      utils.activities.list.invalidate();
      toast.success("Activity created");
    },
    onError: (error) => {
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
```typescript
export function ActivityActions({ activity }: { activity: Activity }) {
  const utils = trpc.useUtils();

  const updateMutation = trpc.activities.update.useMutation({
    onMutate: async (updatedActivity) => {
      await utils.activities.list.cancel();
      const previousActivities = utils.activities.list.getData();
      utils.activities.list.setData(undefined, (old) =>
        old?.map((act) =>
          act.id === updatedActivity.id ? { ...act, ...updatedActivity.data } : act
        )
      );
      return { previousActivities };
    },
    onError: (err, updatedActivity, context) => {
      utils.activities.list.setData(undefined, context?.previousActivities);
      toast.error(err.message);
    },
    onSettled: () => {
      utils.activities.list.invalidate();
    },
  });

  return (
    <button onClick={() => updateMutation.mutate({ id: activity.id, data: { name: "Updated" } })}>
      Update
    </button>
  );
}
```

## Cache Management
### Manual Cache Invalidation
```typescript
const utils = trpc.useUtils();
utils.activities.list.invalidate();
utils.activities.invalidate();
utils.invalidate();
```

### Manual Cache Updates
```typescript
const currentData = utils.activities.list.getData();
utils.activities.list.setData({ limit: 20 }, (old) => {
  return [...(old ?? []), newActivity];
});
```

## Common Options

### Query Options
```typescript
trpc.activities.list.useQuery(input, {
  staleTime: 5 * 60 * 1000,
  cacheTime: 10 * 60 * 1000,
  refetchOnMount: false,
  refetchOnWindowFocus: false,
  refetchInterval: 30 * 1000,
  enabled: !!someCondition,
  onSuccess: (data) => {},
  onError: (error) => {},
});
```

### Mutation Options
```typescript
trpc.activities.create.useMutation({
  onSuccess: (data) => {
    utils.activities.list.invalidate();
    toast.success("Created");
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
  {mutation.isPending ? "Creating..." : "Create"}
</button>
```

## Error Handling

### Display Errors
```typescript
import { toast } from "sonner";

const mutation = trpc.activities.create.useMutation({
  onError: (error) => {
    toast.error(error.message);
    if (error.data?.code === "UNAUTHORIZED") {
      router.push("/login");
    }
  },
});
```

### Retry Logic
```typescript
trpc.activities.list.useQuery(input, {
  retry: 3,
  retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
});
```

## Example Use Cases

### 1. List Page with Search
```typescript
const [search, setSearch] = useState("");
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
    toast.success("Created");
    router.push("/activities");
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
    toast.success("Deleted");
  },
});

const handleDelete = () => {
  if (confirm("Are you sure?")) {
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