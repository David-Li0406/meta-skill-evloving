# Next.js 16 & React 19 API Integration

Modern data fetching and mutation patterns for the 2026 web ecosystem.

## 1. Data Fetching in Server Components

Fetch data directly in your components to minimize client-side bundles and hide API keys.

```tsx
// src/components/UserDashboard.tsx
import { cache } from 'react';

// Memoize the fetch if used in multiple components
const getUser = cache(async (id: string) => {
  const res = await fetch(`https://api.example.com/users/${id}`, {
    headers: { Authorization: `Bearer ${process.env.API_SECRET}` },
    next: { revalidate: 3600 } // Cache for 1 hour
  });
  return res.json();
});

export default async function UserDashboard({ userId }: { userId: string }) {
  const user = await getUser(userId);
  
  return (
    <div>
      <h1>Welcome, {user.name}</h1>
    </div>
  );
}
```

## 2. Server Actions for Mutations

Server Actions provide a secure way to handle form submissions and data updates.

```tsx
// src/app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2)
});

export async function updateUser(prevState: any, formData: FormData) {
  const validated = schema.safeParse({
    email: formData.get('email'),
    name: formData.get('name'),
  });

  if (!validated.success) {
    return { errors: validated.error.flatten().fieldErrors };
  }

  const res = await fetch('https://api.example.com/user', {
    method: 'PATCH',
    body: JSON.stringify(validated.data),
    headers: { 'Content-Type': 'application/json' }
  });

  if (!res.ok) return { message: "Update failed" };

  revalidatePath('/dashboard');
  return { message: "User updated successfully!" };
}
```

## 3. Optimistic Updates with `useOptimistic`

Improve UX by reflecting changes immediately while the Server Action processes.

```tsx
'use client';

import { useOptimistic } from 'react';
import { updateUserAction } from './actions';

export function ProfileForm({ user }) {
  const [optimisticUser, addOptimisticUser] = useOptimistic(
    user,
    (state, newUser: any) => ({ ...state, ...newUser })
  );

  async function action(formData: FormData) {
    const name = formData.get('name') as string;
    addOptimisticUser({ name }); // UI updates immediately
    await updateUserAction(formData);
  }

  return (
    <form action={action}>
      <input name="name" defaultValue={optimisticUser.name} />
      <button type="submit">Update</button>
    </form>
  );
}
```

## 4. Typed API Clients with Zod/Valibot

Always validate API responses at runtime to ensure your TS types match reality.

```typescript
import { z } from 'zod';

const APIUserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  roles: z.array(z.enum(['admin', 'user']))
});

export type APIUser = z.infer<typeof APIUserSchema>;

async function fetchUser(id: string): Promise<APIUser> {
  const res = await fetch(`/api/users/${id}`);
  const data = await res.json();
  
  // Safe parsing ensures no runtime errors downstream
  return APIUserSchema.parse(data);
}
```

## Best Practices
- **Never expose `SECRET_KEYS`**: Prefix only client-safe variables with `NEXT_PUBLIC_`.
- **Use `fetch` over Axios**: Next.js 16 extends the native `fetch` with advanced caching and revalidation logic.
- **Streaming UI**: Use `Suspense` around data-heavy components to enable partial page loading.

*Updated: January 22, 2026 - 15:18
