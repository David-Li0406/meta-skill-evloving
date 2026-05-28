# Next.js + Effect-TS Integration

A pattern for integrating **Effect-TS** with **Next.js App Router** pages and server actions, solving the redirect problem and providing type-safe error handling.

## Libraries

| Package  | Purpose                           |
| -------- | --------------------------------- |
| `effect` | Functional programming primitives |
| `next`   | Next.js App Router                |

## The Problem

Next.js's `redirect()` function works by throwing a special error. When called inside an Effect pipeline, Effect catches this error internally, preventing the redirect from propagating to Next.js.

```typescript
// This DOES NOT work
Effect.gen(function* () {
  redirect('/login') // Effect catches this, redirect never happens
})
```

## The Solution: NextEffect

A thin wrapper that:

1. Provides `NextEffect.redirect()` - creates a redirect intent as a tagged error
2. Provides `NextEffect.runPromise()` - catches redirect intents and calls Next.js `redirect()` outside the Effect context

## File Structure

```
lib/next-effect/
└── index.ts          # NextEffect utility (redirect + runPromise)

lib/layers.ts         # Layer composition for dependency injection
```

## Scaffolding from Scratch

### 1. Create NextEffect Utility (`lib/next-effect/index.ts`)

```typescript
import { Data, Effect, Either } from 'effect'
import { redirect } from 'next/navigation'

// Tagged error for redirect intents
class RedirectError extends Data.TaggedError('RedirectError')<{
  path: string
}> {}

/**
 * Create a redirect effect. Use this instead of Next.js redirect() inside Effect pipelines.
 */
const redirectEffect = (path: string) => Effect.fail(new RedirectError({ path }))

/**
 * Custom Effect.runPromise that handles Next.js redirects outside the Effect context.
 */
const runPromise = async <A, E>(effect: Effect.Effect<A, E>): Promise<A> => {
  const result = await Effect.runPromise(
    Effect.catchAll(Effect.map(effect, Either.right), e =>
      e instanceof RedirectError ? Effect.succeed(Either.left(e)) : Effect.fail(e)
    )
  )
  if (Either.isLeft(result)) {
    return redirect(result.left.path)
  }
  return result.right
}

export const NextEffect = {
  redirect: redirectEffect,
  runPromise
}
```

### 2. Create Layer Composition (`lib/layers.ts`)

```typescript
import { Layer } from 'effect'
import { DbLive } from './services/db/live-layer'
import { AuthLayer } from './services/auth'
import { TelemetryLayer } from './services/telemetry/live-layer'

// Combined layer with core services
export const AppLayer = Layer.mergeAll(AuthLayer, DbLayer, TelemetryLayer)

// Additional service layers (compose as needed)
export const S3Layer = S3.defaultLayer
export const ShopifyAdminLayer = ShopifyAdminLive
export const CurrencyLayer = CurrencyServiceLayerLive
```

## Page Patterns

### Standard Page Structure

Every page follows this pattern:

```typescript
// app/(dashboard)/posts/page.tsx
import { Effect, Match } from 'effect'
import { Suspense } from 'react'
import { cookies } from 'next/headers'
import { NextEffect } from '@/lib/next-effect'
import { AppLayer } from '@/lib/layers'
import { getSessionEffect } from '@/lib/services/auth/get-session-effect'
import { getUserPosts } from '@/lib/core/post/data/get-user-posts'

// Inner async component does the real work
async function Content() {
  await cookies() // Mark route as dynamic

  return await NextEffect.runPromise(
    Effect.gen(function* () {
      const session = yield* getSessionEffect()
      const posts = yield* getUserPosts(session.user.id)
      return { posts, session }
    }).pipe(
      Effect.provide(AppLayer),
      Effect.scoped,
      Effect.matchEffect({
        onFailure: error =>
          Match.value(error._tag).pipe(
            Match.when('UnauthenticatedError', () => NextEffect.redirect('/login')),
            Match.when('UnauthorizedError', () => NextEffect.redirect('/')),
            Match.orElse(() =>
              Effect.succeed(
                <main className="p-4">
                  <p className="text-red-500">Error: {error.message}</p>
                </main>
              )
            )
          ),
        onSuccess: ({ posts, session }) =>
          Effect.succeed(<PostList posts={posts} userId={session.user.id} />)
      })
    )
  )
}

// Page component wraps Content in Suspense
export default function Page() {
  return (
    <Suspense fallback={null}>
      <Content />
    </Suspense>
  )
}
```

### Dynamic Route Parameters

```typescript
// app/(dashboard)/post/[id]/page.tsx
type Props = {
  params: Promise<{ id: string }>
}

async function Content({ params }: Props) {
  await cookies()
  const { id } = await params // Await params in Next.js 15+

  return await NextEffect.runPromise(
    Effect.gen(function* () {
      const session = yield* getSessionEffect()
      const post = yield* getPostById(id)

      // Check ownership
      if (post.userId !== session.user.id && session.user.role !== 'ADMIN') {
        return yield* Effect.fail(new UnauthorizedError({ message: 'Not your post' }))
      }

      return { post, isOwner: post.userId === session.user.id }
    }).pipe(
      Effect.provide(AppLayer),
      Effect.scoped,
      Effect.matchEffect({
        onFailure: error =>
          Match.value(error._tag).pipe(
            Match.when('UnauthenticatedError', () => NextEffect.redirect('/login')),
            Match.when('UnauthorizedError', () => NextEffect.redirect('/')),
            Match.when('PostNotFoundError', () => NextEffect.redirect('/posts')),
            Match.orElse(() => Effect.succeed(<ErrorMessage error={error} />))
          ),
        onSuccess: ({ post, isOwner }) =>
          Effect.succeed(<PostDetail post={post} canEdit={isOwner} />)
      })
    )
  )
}

export default function Page(props: Props) {
  return (
    <Suspense fallback={null}>
      <Content params={props.params} />
    </Suspense>
  )
}
```

### Admin-Only Page

```typescript
// app/(dashboard)/(admin)/users/page.tsx
async function Content() {
  await cookies()

  return await NextEffect.runPromise(
    Effect.gen(function* () {
      yield* getAdminSession() // Fails if not admin
      const users = yield* getAllUsers()
      return { users }
    }).pipe(
      Effect.provide(AppLayer),
      Effect.scoped,
      Effect.matchEffect({
        onFailure: error =>
          Match.value(error._tag).pipe(
            Match.when('UnauthenticatedError', () => NextEffect.redirect('/login')),
            Match.when('UnauthorizedError', () => NextEffect.redirect('/')),
            Match.orElse(() => Effect.succeed(<ErrorMessage error={error} />))
          ),
        onSuccess: ({ users }) => Effect.succeed(<UserTable users={users} />)
      })
    )
  )
}
```

### Alternative Pattern: catchTags

For simpler pages, use `catchTags` instead of `matchEffect`:

```typescript
// app/(auth)/login/page.tsx
async function Content() {
  await cookies()

  const result = await Effect.runPromise(
    Effect.gen(function* () {
      yield* getSessionEffect()
      return { _tag: 'Authenticated' as const }
    }).pipe(
      Effect.provide(AuthLayer),
      Effect.scoped,
      Effect.catchTags({
        UnauthenticatedError: () => Effect.succeed({ _tag: 'Unauthenticated' as const })
      }),
      Effect.catchAll(error => Effect.succeed({ _tag: 'UnknownError' as const, error }))
    )
  )

  // Handle outside Effect with Match
  return Match.value(result).pipe(
    Match.tag('Authenticated', () => redirect('/')),
    Match.tag('UnknownError', ({ error }) => { throw error }),
    Match.tag('Unauthenticated', () => <LoginForm />),
    Match.exhaustive
  )
}
```

## Server Action Patterns

### Standard Action Structure

```typescript
// app/(dashboard)/post/new/create-post-action.ts
'use server'

import { Effect, Layer, Match, Schema } from 'effect'
import { revalidatePath } from 'next/cache'
import { NextEffect } from '@/lib/next-effect'
import { AppLayer } from '@/lib/layers'
import { getSessionEffect } from '@/lib/services/auth/get-session-effect'
import { createPost } from '@/lib/core/post/data/create-post'
import { createId } from '@paralleldrive/cuid2'

// Input validation schema
const InputSchema = Schema.Struct({
  title: Schema.compose(Schema.Trim, Schema.NonEmptyString),
  content: Schema.String
})

export const createPostAction = async (input: { title: string; content: string }) => {
  return await NextEffect.runPromise(
    Effect.gen(function* () {
      const postId = createId()

      // 1. Annotate span with input context
      yield* Effect.annotateCurrentSpan({
        operation: 'post.create',
        'post.id': postId
      })

      // 2. Auth check
      const { user } = yield* getSessionEffect()
      yield* Effect.annotateCurrentSpan({ 'user.id': user.id })

      // 3. Validate input
      const validated = yield* Schema.decodeUnknown(InputSchema)(input)

      // 4. Create post
      yield* createPost({
        id: postId,
        userId: user.id,
        title: validated.title,
        content: validated.content
      })

      return { id: postId }
    }).pipe(
      Effect.withSpan('action.post.create'),
      Effect.provide(AppLayer),
      Effect.scoped,
      Effect.matchEffect({
        onFailure: error =>
          Match.value(error._tag).pipe(
            Match.when('UnauthenticatedError', () => NextEffect.redirect('/login')),
            Match.when('ParseError', () =>
              Effect.succeed({
                _tag: 'Error' as const,
                message: 'Invalid input',
                fieldErrors: { title: 'Title is required' }
              })
            ),
            Match.orElse(() =>
              Effect.succeed({
                _tag: 'Error' as const,
                message: 'Something went wrong'
              })
            )
          ),
        onSuccess: ({ id }) => NextEffect.redirect(`/post/${id}`)
      })
    )
  )
}
```

### Action with Revalidation (No Redirect)

```typescript
// app/(dashboard)/post/[id]/update-post-action.ts
'use server'

export const updatePostAction = async (postId: string, input: { title: string }) => {
  return await NextEffect.runPromise(
    Effect.gen(function* () {
      yield* Effect.annotateCurrentSpan({ 'post.id': postId, operation: 'post.update' })

      const { user } = yield* getSessionEffect()
      const { post } = yield* verifyPostAccess(postId) // Checks ownership
      const validated = yield* Schema.decodeUnknown(InputSchema)(input)

      yield* updatePost(postId, validated)

      return { id: postId }
    }).pipe(
      Effect.withSpan('action.post.update'),
      Effect.provide(AppLayer),
      Effect.scoped,
      Effect.matchEffect({
        onFailure: error =>
          Match.value(error._tag).pipe(
            Match.when('UnauthenticatedError', () => NextEffect.redirect('/login')),
            Match.when('UnauthorizedError', () => NextEffect.redirect('/')),
            Match.when('PostNotFoundError', () =>
              Effect.succeed({ _tag: 'Error' as const, message: 'Post not found' })
            ),
            Match.when('ParseError', () =>
              Effect.succeed({
                _tag: 'Error' as const,
                message: 'Invalid input',
                fieldErrors: { title: 'Title is required' }
              })
            ),
            Match.orElse(() =>
              Effect.succeed({ _tag: 'Error' as const, message: 'Something went wrong' })
            )
          ),
        onSuccess: result =>
          Effect.sync(() => {
            revalidatePath(`/post/${postId}`)
            return { _tag: 'Success' as const, data: result }
          })
      })
    )
  )
}
```

### Delete Action

```typescript
// app/(dashboard)/post/[id]/delete-post-action.ts
'use server'

export const deletePostAction = async (postId: string) => {
  return await NextEffect.runPromise(
    Effect.gen(function* () {
      yield* Effect.annotateCurrentSpan({ 'post.id': postId, operation: 'post.delete' })

      const { post, session } = yield* verifyPostAccess(postId)
      yield* Effect.annotateCurrentSpan({ 'user.id': session.user.id })

      yield* deletePost(postId)

      return { deleted: true }
    }).pipe(
      Effect.withSpan('action.post.delete'),
      Effect.provide(Layer.mergeAll(AppLayer, S3Layer)), // Add S3 for file cleanup
      Effect.scoped,
      Effect.matchEffect({
        onFailure: error =>
          Match.value(error._tag).pipe(
            Match.when('UnauthenticatedError', () => NextEffect.redirect('/login')),
            Match.when('UnauthorizedError', () => NextEffect.redirect('/')),
            Match.when('PostNotFoundError', () =>
              Effect.succeed({ _tag: 'Error' as const, message: 'Post not found' })
            ),
            Match.orElse(() =>
              Effect.succeed({ _tag: 'Error' as const, message: 'Something went wrong' })
            )
          ),
        onSuccess: () => Effect.sync(() => revalidatePath('/posts'))
      })
    )
  )
}
```

### Action with Multiple Service Layers

```typescript
// app/(dashboard)/order/create-order-action.ts
'use server'

export const createOrderAction = async (input: OrderInput) => {
  return await NextEffect.runPromise(
    Effect.gen(function* () {
      const { user } = yield* getSessionEffect()

      // Uses multiple services
      const priceEur = yield* convertToEur(input.price, input.currency)
      const { stripePaymentId } = yield* createStripePayment({ ... })
      const order = yield* createOrder({ ... })
      yield* sendOrderConfirmation(user.email, order)

      return { orderId: order.id }
    }).pipe(
      Effect.withSpan('action.order.create'),
      Effect.provide(Layer.mergeAll(
        AppLayer,
        StripeLayer,
        CurrencyLayer,
        EmailLayer
      )),
      Effect.scoped,
      Effect.matchEffect({ ... })
    )
  )
}
```

## Client Form Patterns

### Standard Form with useTransition

```typescript
// app/(dashboard)/post/new/post-form.tsx
'use client'

import { useTransition, useState, FormEvent } from 'react'
import { toast } from 'sonner'
import { createPostAction } from './create-post-action'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { LoaderCircleIcon } from 'lucide-react'

export function PostForm() {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({})
  const [isProcessing, startTransition] = useTransition()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setFieldErrors({})

    startTransition(async () => {
      const result = await createPostAction({ title, content })

      // Action may redirect on success, so result may not exist
      if (result?._tag === 'Error') {
        if (result.fieldErrors) {
          setFieldErrors(result.fieldErrors)
          return
        }
        toast.error(result.message)
      }
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Input
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="Post title"
          className={fieldErrors.title ? 'border-destructive' : ''}
        />
        {fieldErrors.title && (
          <p className="text-sm text-destructive mt-1">{fieldErrors.title}</p>
        )}
      </div>

      <textarea
        value={content}
        onChange={e => setContent(e.target.value)}
        placeholder="Write your post..."
        className="w-full min-h-32 p-2 border rounded"
      />

      <Button type="submit" disabled={isProcessing}>
        {isProcessing && <LoaderCircleIcon className="size-4 animate-spin mr-2" />}
        Create Post
      </Button>
    </form>
  )
}
```

### Inline Edit Pattern

```typescript
// app/(dashboard)/post/[id]/post-title.tsx
'use client'

import { useTransition, useState, FormEvent } from 'react'
import { toast } from 'sonner'
import { updatePostAction } from './update-post-action'
import { PencilIcon, CheckIcon, XIcon } from 'lucide-react'

type Props = {
  postId: string
  title: string
}

export function PostTitle({ postId, title: initialTitle }: Props) {
  const [isEditing, setIsEditing] = useState(false)
  const [title, setTitle] = useState(initialTitle)
  const [error, setError] = useState<string>()
  const [isProcessing, startTransition] = useTransition()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    const trimmedTitle = title.trim()

    if (!trimmedTitle) {
      setError('Title cannot be empty')
      return
    }

    if (trimmedTitle === initialTitle) {
      setIsEditing(false)
      return
    }

    startTransition(async () => {
      const result = await updatePostAction(postId, { title: trimmedTitle })

      if (result?._tag === 'Error') {
        if (result.fieldErrors?.title) {
          setError(result.fieldErrors.title)
          return
        }
        toast.error(result.message)
        return
      }

      setIsEditing(false)
      toast.success('Title updated')
    })
  }

  const handleCancel = () => {
    setTitle(initialTitle)
    setError(undefined)
    setIsEditing(false)
  }

  if (!isEditing) {
    return (
      <div className="group flex items-center gap-2">
        <h1 className="text-2xl font-bold">{title}</h1>
        <button
          onClick={() => setIsEditing(true)}
          className="opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <PencilIcon className="size-4" />
        </button>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2">
      <input
        value={title}
        onChange={e => { setTitle(e.target.value); setError(undefined) }}
        className={`text-2xl font-bold border-b ${error ? 'border-destructive' : 'border-primary'}`}
        autoFocus
      />
      <button type="submit" disabled={isProcessing}>
        <CheckIcon className="size-4" />
      </button>
      <button type="button" onClick={handleCancel}>
        <XIcon className="size-4" />
      </button>
      {error && <span className="text-sm text-destructive">{error}</span>}
    </form>
  )
}
```

### Dialog Form Pattern

```typescript
// app/(dashboard)/(admin)/users/create-user-dialog.tsx
'use client'

import { useTransition, useState, FormEvent } from 'react'
import { toast } from 'sonner'
import { createUserAction } from './create-user-action'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export function CreateUserDialog() {
  const [open, setOpen] = useState(false)
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [isProcessing, startTransition] = useTransition()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()

    startTransition(async () => {
      const result = await createUserAction({ name, email })

      if (result?._tag === 'Error') {
        toast.error(result.message)
        return
      }

      // Success
      setOpen(false)
      setName('')
      setEmail('')
      toast.success('User created')
    })
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Create User</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create User</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="Name"
          />
          <Input
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="Email"
            type="email"
          />
          <Button type="submit" disabled={isProcessing}>
            {isProcessing ? 'Creating...' : 'Create'}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}
```

## Directory Structure

Co-locate actions with their consuming components:

```
app/
├── (auth)/
│   └── login/
│       ├── page.tsx              # Page with session check
│       └── login-form.tsx        # Client form
│
├── (dashboard)/
│   ├── posts/
│   │   ├── page.tsx              # List page
│   │   └── post-list.tsx         # List component
│   │
│   └── post/
│       ├── new/
│       │   ├── page.tsx          # Create page
│       │   ├── post-form.tsx     # Form component
│       │   └── create-post-action.ts  # Co-located action
│       │
│       └── [id]/
│           ├── page.tsx          # Detail page
│           ├── post-title.tsx    # Inline edit component
│           ├── update-post-action.ts  # Co-located action
│           └── delete-post-action.ts  # Co-located action
│
└── (admin)/
    └── users/
        ├── page.tsx
        ├── user-table.tsx
        ├── create-user-dialog.tsx
        └── create-user-action.ts
```

## Best Practices

### 1. Always Mark Routes as Dynamic

Access cookies before any auth check:

```typescript
async function Content() {
  await cookies() // Required for Next.js dynamic rendering
  // ...
}
```

### 2. Use Suspense with Null Fallback

Keep pages simple - no loading.tsx or error.tsx needed:

```typescript
export default function Page() {
  return (
    <Suspense fallback={null}>
      <Content />
    </Suspense>
  )
}
```

### 3. Handle All Error Types Explicitly

Use Match for type-safe error handling:

```typescript
Match.value(error._tag).pipe(
  Match.when('UnauthenticatedError', () => NextEffect.redirect('/login')),
  Match.when('UnauthorizedError', () => NextEffect.redirect('/')),
  Match.when('NotFoundError', () => NextEffect.redirect('/posts')),
  Match.when('ParseError', () => Effect.succeed({ _tag: 'Error', fieldErrors: {...} })),
  Match.orElse(() => Effect.succeed({ _tag: 'Error', message: 'Something went wrong' }))
)
```

### 4. Return Discriminated Unions from Actions

Enable type-safe error handling in clients:

```typescript
// Success types
{ _tag: 'Success', data: result }
{ _tag: 'Success' } // For void operations

// Error types
{ _tag: 'Error', message: string }
{ _tag: 'Error', message: string, fieldErrors: Record<string, string> }
```

### 5. Co-locate Actions with Components

Keep actions close to their consumers:

```
post/[id]/
├── post-title.tsx
├── update-title-action.ts  # Used by post-title.tsx
├── post-status.tsx
└── update-status-action.ts  # Used by post-status.tsx
```

### 6. Use Effect.scoped for Resource Management

Always include `Effect.scoped` in the pipe:

```typescript
Effect.gen(function* () { ... }).pipe(
  Effect.withSpan('action.entity.operation'),
  Effect.provide(AppLayer),
  Effect.scoped,  // Ensures resources are properly cleaned up
  Effect.matchEffect({ ... })
)
```

### 7. Annotate Spans for Observability

Add context at the start of operations:

```typescript
Effect.gen(function* () {
  yield* Effect.annotateCurrentSpan({
    operation: 'post.create',
    'post.id': postId,
    'user.id': user.id
  })
  // ...
})
```

### 8. Compose Layers Based on Needs

Only include the layers you need:

```typescript
// Simple CRUD - just AppLayer
Effect.provide(AppLayer)

// With external services
Effect.provide(Layer.mergeAll(AppLayer, StripeLayer, EmailLayer))
```

## Environment Variables

| Variable | Required | Description                                           |
| -------- | -------- | ----------------------------------------------------- |
| (none)   | -        | NextEffect has no config - it uses Effect and Next.js |

## Anti-Patterns to Avoid

1. **Never call `redirect()` directly inside Effect** - use `NextEffect.redirect()`
2. **Never use `Effect.runPromise` for actions** - use `NextEffect.runPromise`
3. **Never forget `await cookies()`** in page Content functions
4. **Never forget `Effect.scoped`** in the pipe chain
5. **Never report auth errors to Sentry** - they're expected business cases
