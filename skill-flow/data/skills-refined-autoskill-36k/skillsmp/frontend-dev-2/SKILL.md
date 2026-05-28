---
name: frontend-dev
description: Comprehensive React, TypeScript, and Tailwind frontend development with Next.js and TanStack ecosystem (TanStack Router, TanStack Query, TanStack Start). Use when building, configuring, or developing modern web applications with these specific technologies, including project setup, routing, data fetching, component patterns, and TypeScript configurations.
---

# Frontend Development

Modern React development with TypeScript, Tailwind CSS, Next.js, and the TanStack ecosystem.

## Project Setup

### Initialize Next.js Project

```bash
npx create-next-app@latest my-app --typescript --tailwind --app --src-dir --import-alias "@/*"
cd my-app
npm install @tanstack/react-query @tanstack/react-router @tanstack/start
```

### Essential Configuration

**tsconfig.json**:

```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**tailwind.config.ts**:

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
  },
  plugins: [],
};
export default config;
```

**app/globals.css**:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #ffffff;
  --foreground: #171717;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}

body {
  color: var(--foreground);
  background: var(--background);
}
```

## TanStack Router

### File-based Routing Structure

```
src/
├── routes/
│   ├── index.tsx              # /
│   ├── about.tsx              # /about
│   ├── posts/
│   │   ├── index.tsx           # /posts
│   │   ├── [$postId].tsx       # /posts/:postId
│   │   └── new.tsx             # /posts/new
└── app/
    ├── layout.tsx
    └── page.tsx
```

### Router Configuration

**router.tsx**:

```typescript
import { createRootRoute, createRouter, Outlet } from '@tanstack/react-router'
import { NotFoundComponent } from './components/not-found'

const rootRoute = createRootRoute({
  component: () => (
    <div className="min-h-screen bg-background text-foreground">
      <header className="border-b p-4">
        <h1 className="text-2xl font-bold">My App</h1>
      </header>
      <main className="p-4">
        <Outlet />
      </main>
    </div>
  ),
  notFoundComponent: NotFoundComponent,
})

const router = createRouter({ routeTree: rootRoute })

declare module '@tanstack/react-router' {
  interface Register { router: typeof router }
}

export default router
```

**main.tsx**:

```typescript
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider } from '@tanstack/react-router'
import router from './router'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
```

### Route with Loader

```typescript
import { createFileRoute } from '@tanstack/react-router'
import { z } from 'zod'

const postSchema = z.object({
  id: z.string(),
  title: z.string(),
  content: z.string(),
  createdAt: z.string(),
})

export const Route = createFileRoute('/posts/$postId')({
  validateSearch: z.object({ filter: z.string().optional() }),
  loader: async ({ params, search }) => {
    const res = await fetch(`/api/posts/${params.postId}?filter=${search.filter}`)
    return postSchema.parse(await res.json())
  },
  component: PostComponent,
})

function PostComponent() {
  const { postId } = Route.useParams()
  const { post } = Route.useLoaderData()

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">{post.title}</h1>
      <p className="text-gray-600">{post.content}</p>
    </div>
  )
}
```

### Layout Route

```typescript
import { createFileRoute, Outlet } from '@tanstack/react-router'

export const Route = createFileRoute('/dashboard/_layout')({
  component: DashboardLayout,
})

function DashboardLayout() {
  return (
    <div className="dashboard-layout">
      <nav className="p-4 border-b">Dashboard Navigation</nav>
      <Outlet />
    </div>
  )
}
```

### Error Boundary

```typescript
export function NotFoundComponent({ error }: { error: Error }) {
  return (
    <div className="p-6 text-center">
      <h2 className="text-2xl font-bold">404</h2>
      <p className="text-gray-600">Page not found</p>
    </div>
  )
}
```

## TanStack Query

### Query Client Setup

**query-client.ts**:

```typescript
import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      retry: 1,
    },
  },
});
```

**app/layout.tsx**:

```typescript
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from '../query-client'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-background text-foreground">
        {children}
      </div>
    </QueryClientProvider>
  )
}
```

### Basic Data Fetching

```typescript
import { useQuery } from '@tanstack/react-query'

function PostList() {
  const { data: posts, isLoading, error } = useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const res = await fetch('/api/posts')
      return res.json()
    },
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div className="space-y-4">
      {posts.map((post: any) => (
        <div key={post.id} className="border p-4 rounded">
          {post.title}
        </div>
      ))}
    </div>
  )
}
```

### Optimistic Updates

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function PostForm() {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: async (newPost: any) => {
      const res = await fetch('/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPost),
      })
      return res.json()
    },
    onMutate: async (newPost) => {
      await queryClient.cancelQueries({ queryKey: ['posts'] })
      const previousPosts = queryClient.getQueryData(['posts'])
      queryClient.setQueryData(['posts'], (old: any[] = []) => [
        ...old,
        { ...newPost, id: Date.now().toString() },
      ])
      return { previousPosts }
    },
    onError: (err, newPost, context) => {
      if (context?.previousPosts) {
        queryClient.setQueryData(['posts'], context.previousPosts)
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] })
    },
  })

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        const formData = new FormData(e.target as HTMLFormElement)
        mutation.mutate({
          title: formData.get('title'),
          content: formData.get('content'),
        })
      }}
      className="space-y-4"
    >
      <input name="title" placeholder="Title" className="border p-2 w-full" />
      <textarea name="content" placeholder="Content" className="border p-2 w-full" />
      <button
        type="submit"
        disabled={mutation.isPending}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {mutation.isPending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  )
}
```

### Pagination

```typescript
import { useQuery } from '@tanstack/react-query'

function PaginatedPostList() {
  const [page, setPage] = useState(1)

  const { data, isLoading } = useQuery({
    queryKey: ['posts', page],
    queryFn: async () => {
      const res = await fetch(`/api/posts?page=${page}`)
      return res.json()
    },
    keepPreviousData: true,
  })

  return (
    <div>
      {isLoading && <div>Loading...</div>}
      <div className="space-y-4">
        {data?.data?.map((post: any) => (
          <div key={post.id} className="border p-4 rounded">{post.title}</div>
        ))}
      </div>
      <div className="flex justify-between mt-4">
        <button onClick={() => setPage(p => p - 1)} disabled={page === 1} className="border px-4 py-2 rounded">
          Previous
        </button>
        <span>Page {page}</span>
        <button onClick={() => setPage(p => p + 1)} disabled={!data?.hasNext} className="border px-4 py-2 rounded">
          Next
        </button>
      </div>
    </div>
  )
}
```

## TanStack Start

### Server-side Data Loading

```typescript
import { createFileRoute, json } from '@tanstack/start'

export const Route = createFileRoute('/dashboard/$userId')({
  loader: async ({ params }) => {
    const res = await fetch(`https://api.example.com/users/${params.userId}`)
    if (!res.ok) throw new Error('User not found')
    const userData = await res.json()
    return json({
      user: {
        id: userData.id,
        name: userData.name,
        email: userData.email,
      },
    })
  },
  component: DashboardPage,
})

function DashboardPage() {
  const { user } = Route.useLoaderData()
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Welcome, {user.name}!</h1>
      <p className="text-gray-600">{user.email}</p>
    </div>
  )
}
```

### Server Actions

```typescript
import { createFileRoute, ServerFunction } from '@tanstack/start'

const createPost: ServerFunction = async ({ request }) => {
  const formData = await request.formData()
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  if (!title || !content) {
    return { error: 'Title and content are required' }
  }

  const newPost = await db.post.create({ data: { title, content } })
  return { success: true, post: newPost }
}

export const Route = createFileRoute('/posts/new')({
  component: NewPostPage,
})

function NewPostPage() {
  const navigate = useNavigate()

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const formData = new FormData(e.target as HTMLFormElement)
    const result = await createPost({ request: new Request('', { method: 'POST', body: formData }) })
    if (!result.error) {
      navigate({ to: `/posts/${result.post.id}` })
    }
  }

  return <form onSubmit={onSubmit}>{/* form fields */}</form>
}
```

## Component Patterns

### Utility Functions

```typescript
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'
import React, { forwardRef } from 'react'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

const Slot = forwardRef<any, React.HTMLAttributes<HTMLElement>>(
  ({ children, ...props }, ref) => {
    const child = React.Children.only(children) as React.ReactElement
    return React.cloneElement(child, {
      ...props,
      ...child.props,
      ref,
    })
  }
)
Slot.displayName = 'Slot'
```

### Button Component

```typescript
import { cva, type VariantProps } from 'class-variance-authority'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  asChild?: boolean
}

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-blue-600 text-white hover:bg-blue-700',
        destructive: 'bg-red-600 text-white hover:bg-red-700',
        outline: 'border border-gray-300 bg-white hover:bg-gray-100 text-gray-800',
        secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
        ghost: 'hover:bg-gray-100',
        link: 'text-blue-600 underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  }
)

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'default', asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button'
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = 'Button'
```

### Input Component

```typescript
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          'flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white',
          'placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500',
          'disabled:cursor-not-allowed disabled:opacity-50',
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = 'Input'
```

### Card Compound Component

```typescript
const Card = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('rounded-lg border bg-white shadow-sm', className)} {...props} />
  )
)
Card.displayName = 'Card'

const CardHeader = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('flex flex-col space-y-1.5 p-6', className)} {...props} />
  )
)
CardHeader.displayName = 'CardHeader'

const CardTitle = forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn('text-2xl font-semibold leading-none tracking-tight', className)} {...props} />
  )
)
CardTitle.displayName = 'CardTitle'

const CardDescription = forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn('text-sm text-gray-600', className)} {...props} />
  )
)
CardDescription.displayName = 'CardDescription'

const CardContent = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
  )
)
CardContent.displayName = 'CardContent'

const CardFooter = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('flex items-center p-6 pt-0', className)} {...props} />
  )
)
CardFooter.displayName = 'CardFooter'
```

### Dialog Compound Component

```typescript
type DialogContextValue = {
  open: boolean
  onOpenChange: (open: boolean) => void
}

const DialogContext = React.createContext<DialogContextValue | undefined>(undefined)

function useDialog() {
  const context = React.useContext(DialogContext)
  if (!context) throw new Error('Dialog components must be used within a Dialog')
  return context
}

interface DialogProps {
  open?: boolean
  onOpenChange?: (open: boolean) => void
  children: React.ReactNode
}

function Dialog({ open = false, onOpenChange, children }: DialogProps) {
  return (
    <DialogContext.Provider value={{ open, onOpenChange: onOpenChange ?? (() => {}) }}>
      {children}
    </DialogContext.Provider>
  )
}
Dialog.displayName = 'Dialog'

const DialogTrigger = forwardRef<HTMLButtonElement, React.ButtonHTMLAttributes<HTMLButtonElement>>(
  ({ asChild = false, ...props }, ref) => {
    const { onOpenChange } = useDialog()
    const Comp = asChild ? Slot : 'button'
    return <Comp ref={ref} onClick={() => onOpenChange(true)} {...props} />
  }
)
DialogTrigger.displayName = 'DialogTrigger'

const DialogContent = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => {
    const { open, onOpenChange } = useDialog()

    if (!open) return null

    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center">
        <div className="fixed inset-0 bg-black/50" onClick={() => onOpenChange(false)} />
        <div
          ref={ref}
          className={cn(
            'relative z-50 w-full max-w-md rounded-lg bg-white p-6 shadow-lg animate-in fade-in-0 zoom-in-95 duration-200',
            className
          )}
          {...props}
        >
          {children}
        </div>
      </div>
    )
  }
)
DialogContent.displayName = 'DialogContent'

const DialogHeader = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('flex flex-col space-y-1.5 text-center sm:text-left', className)} {...props} />
  )
)
DialogHeader.displayName = 'DialogHeader'

const DialogTitle = forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h2 ref={ref} className={cn('text-lg font-semibold leading-none tracking-tight', className)} {...props} />
  )
)
DialogTitle.displayName = 'DialogTitle'

const DialogDescription = forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn('text-sm text-gray-600', className)} {...props} />
  )
)
DialogDescription.displayName = 'DialogDescription'

const DialogFooter = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2', className)} {...props} />
  )
)
DialogFooter.displayName = 'DialogFooter'

const DialogClose = forwardRef<HTMLButtonElement, React.ButtonHTMLAttributes<HTMLButtonElement>>(
  ({ className, ...props }, ref) => {
    const { onOpenChange } = useDialog()
    return (
      <button ref={ref} className={cn('rounded-sm opacity-70 hover:opacity-100', className)} onClick={() => onOpenChange(false)} {...props} />
    )
  }
)
DialogClose.displayName = 'DialogClose'
```

### Usage Examples

```typescript
import { useState } from 'react'

// Button usage
<Button variant="default">Click me</Button>
<Button variant="destructive" size="sm">Delete</Button>
<Button variant="outline">Cancel</Button>
<Button variant="ghost">Ghost</Button>
<Button asChild>
  <a href="/login">Login with Link</a>
</Button>

// Input usage
<Input type="email" placeholder="Email" />
<Input type="password" placeholder="Password" />

// Card usage
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description goes here</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Card content goes here</p>
  </CardContent>
  <CardFooter className="flex justify-between">
    <Button variant="outline">Cancel</Button>
    <Button>Save</Button>
  </CardFooter>
</Card>

// Dialog usage
function MyDialog() {
  const [open, setOpen] = useState(false)

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Open Dialog</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Are you sure?</DialogTitle>
          <DialogDescription>This action cannot be undone. This will permanently delete your account.</DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <p>Some dialog content here</p>
        </div>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Cancel</Button>
          </DialogClose>
          <Button variant="destructive">Delete Account</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

### Composition Patterns

```typescript
// 1. forwardRef pattern - for ref forwarding
export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        ref={ref}
        className={cn('flex h-10 w-full rounded-md border bg-white px-3 py-2', className)}
        {...props}
      />
    )
  }
)

// 2. asChild pattern - polymorphic components
function Button({ asChild = false, children, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : 'button'
  return <Comp {...props}>{children}</Comp>
}

// Usage: Button wraps Link
<Button asChild>
  <Link href="/dashboard">Dashboard</Link>
</Button>

// 3. Context pattern - for compound components
const TabsContext = React.createContext<{ value: string } | undefined>(undefined)

function Tabs({ value, children }: { value: string; children: React.ReactNode }) {
  return <TabsContext.Provider value={{ value }}>{children}</TabsContext.Provider>
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div className="flex border-b">{children}</div>
}

function Tab({ value, children }: { value: string; children: React.ReactNode }) {
  const context = React.useContext(TabsContext)
  const isActive = context?.value === value
  return (
    <button className={cn('px-4 py-2', isActive && 'border-b-2 border-blue-600')}>
      {children}
    </button>
  )
}

// Usage: compound components
<Tabs value="tab1">
  <TabList>
    <Tab value="tab1">Tab 1</Tab>
    <Tab value="tab2">Tab 2</Tab>
  </TabList>
</Tabs>

// 4. cva pattern - for variant management
import { cva, type VariantProps } from 'class-variance-authority'

const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-blue-600 text-white',
        secondary: 'border-transparent bg-gray-200 text-gray-800',
        destructive: 'border-transparent bg-red-600 text-white',
        outline: 'text-gray-800 border-gray-300',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

interface BadgeProps extends VariantProps<typeof badgeVariants> {}

function Badge({ variant, className, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}

// Usage
<Badge variant="secondary">Badge</Badge>
<Badge variant="destructive">Error</Badge>
```

### Data Fetching Component

```typescript
import { useQuery } from '@tanstack/react-query'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const res = await fetch(`/api/posts/${params.postId}`)
    return res.json()
  },
  component: PostComponent,
})

function PostComponent() {
  const { postId } = Route.useParams()
  const { data: post, isLoading, error } = useQuery({
    queryKey: ['post', postId],
    queryFn: async () => {
      const res = await fetch(`/api/posts/${postId}`)
      return res.json()
    },
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">{post.title}</h1>
      <p className="text-gray-600">{post.content}</p>
    </div>
  )
}
```

### Form Component

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
})

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  })

  const onSubmit = (data: any) => {
    // Handle form submission
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Email</label>
        <input {...register('email')} className="w-full px-3 py-2 border rounded" />
        {errors.email && <p className="text-red-500 text-sm">{errors.email.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Password</label>
        <input {...register('password')} type="password" className="w-full px-3 py-2 border rounded" />
        {errors.password && <p className="text-red-500 text-sm">{errors.password.message}</p>}
      </div>

      <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
        Login
      </button>
    </form>
  )
}
```

## TypeScript Utility Types

```typescript
// Common types
type ApiResponse<T> = { data: T; message?: string; error?: string }
type Status = 'loading' | 'success' | 'error'

// Type guards
function isUser(data: unknown): data is User {
  return typeof data === 'object' && data !== null && 'id' in data && 'name' in data
}

// Generic components
interface GenericListProps<T> {
  items: T[]
  renderItem: (item: T, index: number) => React.ReactNode
  className?: string
}

function GenericList<T>({ items, renderItem, className }: GenericListProps<T>) {
  return <div className={className}>{items.map((item, i) => renderItem(item, i))}</div>
}

// Query types
type PostQuery = { id: string; title: string; content: string; createdAt: string }

// Event types
type FormEvent = React.FormEvent<HTMLFormElement>
type ChangeEvent = React.ChangeEvent<HTMLInputElement>
```

## Tailwind Utility Classes

```typescript
// Common component classes
const buttonStyles = {
  primary: "bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded",
  secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300 px-4 py-2 rounded",
  destructive: "bg-red-600 text-white hover:bg-red-700 px-4 py-2 rounded",
  outline: "border border-gray-300 px-4 py-2 rounded hover:bg-gray-50",
  ghost: "px-4 py-2 rounded hover:bg-gray-100",
};

const inputStyles = {
  base: "w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500",
  error: "border-red-500 focus:ring-red-500",
};

const cardStyles = {
  base: "border rounded-lg p-6 shadow-sm",
  hover: "hover:shadow-md transition-shadow",
};
```

## Common Workflows

### Protected Routes

```typescript
export const Route = createFileRoute("/dashboard/_protected")({
  beforeLoad: ({ location }) => {
    if (!isAuthenticated()) {
      throw redirect({ to: "/login", search: { redirect: location.pathname } });
    }
  },
  component: DashboardPage,
});

function isAuthenticated(): boolean {
  return !!localStorage.getItem("auth-token");
}
```

### API Error Handling

```typescript
try {
  const res = await fetch("/api/data");
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.message || "Request failed");
  }
  return res.json();
} catch (error) {
  console.error("API Error:", error);
  throw error;
}
```

### Loading States

```typescript
function DataComponent() {
  const { data, isLoading, isFetching } = useQuery({ queryKey: ['data'], queryFn: fetchData })

  if (isLoading) return <div className="animate-pulse">Loading...</div>
  if (isFetching) <div>Updating...</div>

  return <div>{data}</div>
}
```
