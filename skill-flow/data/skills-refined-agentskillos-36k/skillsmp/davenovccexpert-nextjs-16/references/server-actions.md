<overview>
Server Actions are async functions that run on the server. They're used for data mutations, form handling, and any server-side operations triggered from the client.
</overview>

<basics>
**Creating a Server Action:**

```typescript
// Option 1: In a separate file (recommended for reuse)
// lib/actions.ts
'use server'

export async function createItem(formData: FormData) {
  const title = formData.get('title') as string
  await db.items.create({ data: { title } })
}

// Option 2: Inline in Server Component
export default function Page() {
  async function handleSubmit(formData: FormData) {
    'use server'
    await db.items.create({ data: { title: formData.get('title') } })
  }

  return <form action={handleSubmit}>...</form>
}
```

**Calling from Client Component:**

```tsx
'use client'

import { createItem } from '@/lib/actions'

export function CreateForm() {
  return (
    <form action={createItem}>
      <input name="title" />
      <button type="submit">Create</button>
    </form>
  )
}
```
</basics>

<patterns>
<pattern name="with-validation">
**Validate input and return errors:**

```typescript
'use server'

import { z } from 'zod'

const CreateItemSchema = z.object({
  title: z.string().min(3, 'Title must be at least 3 characters'),
  description: z.string().optional(),
})

export async function createItem(formData: FormData) {
  const rawData = {
    title: formData.get('title'),
    description: formData.get('description'),
  }

  const validatedData = CreateItemSchema.safeParse(rawData)

  if (!validatedData.success) {
    return {
      error: validatedData.error.flatten().fieldErrors,
    }
  }

  await db.items.create({ data: validatedData.data })
  return { success: true }
}
```
</pattern>

<pattern name="with-auth">
**Always verify authentication:**

```typescript
'use server'

import { getUser } from '@/lib/dal'

export async function createItem(formData: FormData) {
  // ALWAYS verify auth first
  const user = await getUser()
  if (!user) {
    throw new Error('Unauthorized')
  }

  // Validate input
  const title = formData.get('title') as string
  if (!title || title.length < 3) {
    return { error: 'Invalid title' }
  }

  // Create with user association
  await db.items.create({
    data: {
      title,
      userId: user.id,
    }
  })

  return { success: true }
}
```
</pattern>

<pattern name="with-revalidation">
**Revalidate cache after mutation:**

```typescript
'use server'

import { revalidateTag, updateTag, revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createItem(formData: FormData) {
  const user = await getUser()
  if (!user) throw new Error('Unauthorized')

  await db.items.create({ data: { ... } })

  // Option 1: Revalidate by tag (recommended)
  updateTag('items')

  // Option 2: Revalidate by path
  revalidatePath('/items')

  // Option 3: Redirect (also revalidates)
  redirect('/items')
}
```
</pattern>

<pattern name="with-useactionstate">
**Handle pending state and errors in UI:**

```tsx
'use client'

import { useActionState } from 'react'
import { createItem } from '@/lib/actions'

type State = {
  error?: string
  success?: boolean
} | null

export function CreateForm() {
  const [state, action, pending] = useActionState<State, FormData>(
    createItem,
    null
  )

  return (
    <form action={action}>
      <input name="title" disabled={pending} />

      {state?.error && (
        <p className="text-red-500">{state.error}</p>
      )}

      <button type="submit" disabled={pending}>
        {pending ? 'Creating...' : 'Create'}
      </button>
    </form>
  )
}
```
</pattern>

<pattern name="optimistic-updates">
**Show optimistic UI while action runs:**

```tsx
'use client'

import { useOptimistic } from 'react'
import { toggleLike } from '@/lib/actions'

export function LikeButton({ postId, initialLikes, isLiked }) {
  const [optimistic, addOptimistic] = useOptimistic(
    { likes: initialLikes, isLiked },
    (state, newIsLiked: boolean) => ({
      likes: newIsLiked ? state.likes + 1 : state.likes - 1,
      isLiked: newIsLiked,
    })
  )

  async function handleClick() {
    addOptimistic(!optimistic.isLiked)
    await toggleLike(postId)
  }

  return (
    <button onClick={handleClick}>
      {optimistic.isLiked ? '❤️' : '🤍'} {optimistic.likes}
    </button>
  )
}
```
</pattern>

<pattern name="file-upload">
**Handle file uploads:**

```typescript
'use server'

export async function uploadFile(formData: FormData) {
  const user = await getUser()
  if (!user) throw new Error('Unauthorized')

  const file = formData.get('file') as File

  if (!file || file.size === 0) {
    return { error: 'No file provided' }
  }

  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    return { error: 'Invalid file type' }
  }

  // Validate file size (e.g., 5MB)
  if (file.size > 5 * 1024 * 1024) {
    return { error: 'File too large' }
  }

  // Upload to storage
  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)
  const url = await uploadToStorage(buffer, file.name)

  return { url }
}
```
</pattern>

<pattern name="non-form-invocation">
**Call from event handlers:**

```tsx
'use client'

import { deleteItem } from '@/lib/actions'

export function DeleteButton({ itemId }: { itemId: string }) {
  async function handleDelete() {
    if (!confirm('Are you sure?')) return

    await deleteItem(itemId)
  }

  return (
    <button onClick={handleDelete}>
      Delete
    </button>
  )
}
```
</pattern>
</patterns>

<security>
**Security requirements for Server Actions:**

1. **Always authenticate:**
```typescript
'use server'
export async function sensitiveAction() {
  const user = await getUser()
  if (!user) throw new Error('Unauthorized')
  // ...
}
```

2. **Always validate input:**
```typescript
'use server'
export async function updateEmail(formData: FormData) {
  const email = formData.get('email')
  if (typeof email !== 'string' || !isValidEmail(email)) {
    return { error: 'Invalid email' }
  }
  // ...
}
```

3. **Authorize the action:**
```typescript
'use server'
export async function deletePost(postId: string) {
  const user = await getUser()
  if (!user) throw new Error('Unauthorized')

  const post = await db.posts.findUnique({ where: { id: postId } })

  // Check ownership
  if (post.userId !== user.id && user.role !== 'admin') {
    throw new Error('Forbidden')
  }

  await db.posts.delete({ where: { id: postId } })
}
```

4. **Rate limit sensitive actions:**
```typescript
'use server'
import { rateLimit } from '@/lib/rate-limit'

export async function login(formData: FormData) {
  const ip = headers().get('x-forwarded-for')

  const { success } = await rateLimit.limit(ip)
  if (!success) {
    return { error: 'Too many attempts' }
  }

  // ... login logic
}
```
</security>

<error_handling>
**Proper error handling:**

```typescript
'use server'

export async function createItem(formData: FormData) {
  try {
    const user = await getUser()
    if (!user) {
      return { error: 'Please log in to continue' }
    }

    const result = await db.items.create({ data: { ... } })
    updateTag('items')

    return { success: true, id: result.id }

  } catch (error) {
    console.error('Failed to create item:', error)

    // Don't expose internal errors to client
    return { error: 'Failed to create item. Please try again.' }
  }
}
```

**In Client Component:**

```tsx
'use client'

export function CreateForm() {
  const [state, action, pending] = useActionState(createItem, null)

  return (
    <form action={action}>
      {state?.error && (
        <div className="bg-red-100 p-4 rounded">
          {state.error}
        </div>
      )}

      {state?.success && (
        <div className="bg-green-100 p-4 rounded">
          Item created successfully!
        </div>
      )}

      {/* form fields */}
    </form>
  )
}
```
</error_handling>

<anti_patterns>
<anti_pattern name="no-auth-check">
**Problem:** Missing authentication

```typescript
'use server'
export async function deleteAccount(userId: string) {
  // BAD - anyone can delete any account!
  await db.users.delete({ where: { id: userId } })
}
```

**Fix:** Always verify the caller

```typescript
'use server'
export async function deleteAccount() {
  const user = await getUser()
  if (!user) throw new Error('Unauthorized')

  // Only delete own account
  await db.users.delete({ where: { id: user.id } })
}
```
</anti_pattern>

<anti_pattern name="trusting-client-input">
**Problem:** Using client input without validation

```typescript
'use server'
export async function updateUser(formData: FormData) {
  const role = formData.get('role')  // BAD - user could set role='admin'
  await db.users.update({ data: { role } })
}
```

**Fix:** Validate and sanitize all input, ignore unauthorized fields
</anti_pattern>
</anti_patterns>
