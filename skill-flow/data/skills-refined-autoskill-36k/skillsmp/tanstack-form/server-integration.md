# Server Integration Reference

## Key Imports

```tsx
// TanStack Form
import { useForm, useStore } from '@tanstack/react-form';
import { createFormHook, createFormHookContexts } from '@tanstack/react-form';

// React Aria Components
import { TextField, Button, Select } from '@oakoss/ui';
```

## Form Submission with Server Function

```tsx
import { createServerFn } from '@tanstack/react-start';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { db } from '@oakoss/database';
import { auth } from '@oakoss/auth/server';

// Server function with validation
const createPost = createServerFn({ method: 'POST' })
  .inputValidator(
    z.object({
      title: z.string().min(1).max(200),
      body: z.string().min(10),
      tags: z.array(z.string()).optional(),
    }),
  )
  .handler(async ({ data, request }) => {
    // Auth check
    const session = await auth.api.getSession({ headers: request.headers });
    if (!session) {
      return { error: 'Unauthorized', code: 'AUTH_REQUIRED' };
    }

    // Create post
    const [post] = await db
      .insert(posts)
      .values({
        ...data,
        authorId: session.user.id,
      })
      .returning();

    return { success: true, data: post };
  });

// Form component
function CreatePostForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (values: typeof schema._output) => createPost({ data: values }),
    onSuccess: (result) => {
      if (result.success) {
        queryClient.invalidateQueries({ queryKey: ['posts'] });
        toast.success('Post created');
        form.reset();
      }
    },
    onError: () => {
      toast.error('Something went wrong');
    },
  });

  const form = useForm({
    defaultValues: { title: '', body: '', tags: [] },
    validators: { onSubmit: schema },
    onSubmit: async ({ value }) => {
      const result = await mutation.mutateAsync(value);
      if (result.error) {
        // Handle server-side error
        form.setErrorMap({ onServer: result.error });
      }
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        form.handleSubmit();
      }}
    >
      {/* Form fields */}
      <form.Subscribe selector={(s) => s.errorMap.onServer}>
        {(error) =>
          error && (
            <div role="alert" className="text-destructive">
              {error}
            </div>
          )
        }
      </form.Subscribe>
      <Button type="submit" isDisabled={mutation.isPending}>
        {mutation.isPending ? 'Creating...' : 'Create Post'}
      </Button>
    </form>
  );
}
```

## Optimistic Updates with Form

```tsx
const mutation = useMutation({
  mutationFn: updateProfile,
  onMutate: async (newProfile) => {
    await queryClient.cancelQueries({ queryKey: ['profile'] });
    const previousProfile = queryClient.getQueryData(['profile']);

    // Optimistically update
    queryClient.setQueryData(['profile'], (old) => ({ ...old, ...newProfile }));

    return { previousProfile };
  },
  onError: (err, variables, context) => {
    // Rollback on error
    if (context?.previousProfile) {
      queryClient.setQueryData(['profile'], context.previousProfile);
    }
    toast.error('Failed to update profile');
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['profile'] });
  },
});
```

## Server-Side Validation Errors

```tsx
// Server function returns field-specific errors
const updateUser = createServerFn({ method: 'POST' })
  .inputValidator(schema)
  .handler(async ({ data }) => {
    // Check username availability
    const existing = await db.query.users.findFirst({
      where: eq(users.username, data.username),
    });

    if (existing) {
      return {
        error: 'Validation failed',
        code: 'VALIDATION_ERROR',
        fieldErrors: { username: 'Username already taken' },
      };
    }

    // Update user
    return { success: true };
  });

// Form handling
const form = useForm({
  onSubmit: async ({ value }) => {
    const result = await mutation.mutateAsync(value);

    if (result.fieldErrors) {
      // Set field-specific errors
      for (const [field, error] of Object.entries(result.fieldErrors)) {
        form.setFieldMeta(field, (prev) => ({
          ...prev,
          errors: [...prev.errors, error],
        }));
      }
    }
  },
});
```

## SSR Forms

### Form with Prefetched Data

```tsx
// Route loader prefetches data
export const Route = createFileRoute('/profile/edit')({
  loader: async ({ context }) => {
    await context.queryClient.ensureQueryData(profileOptions());
  },
  component: EditProfilePage,
});

function EditProfilePage() {
  // Data is already in cache
  const { data: profile } = useSuspenseQuery(profileOptions());

  const form = useForm({
    defaultValues: {
      name: profile.name,
      email: profile.email,
      bio: profile.bio ?? '',
    },
    validators: { onSubmit: profileSchema },
    onSubmit: async ({ value }) => {
      await updateProfile({ data: value });
    },
  });

  return <ProfileForm form={form} />;
}
```

### Preventing Hydration Mismatch

```tsx
// For forms with dynamic defaults (current date, user data, etc.)
function DateForm() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const form = useForm({
    defaultValues: {
      // Use static default for SSR, update on mount
      date: mounted ? new Date().toISOString().split('T')[0] : '',
    },
  });

  // Don't render form until mounted to avoid hydration mismatch
  if (!mounted) {
    return <FormSkeleton />;
  }

  return <form>{/* ... */}</form>;
}
```
