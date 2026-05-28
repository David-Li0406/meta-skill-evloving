# Kyotee: Next.js + Tailwind Patterns

Use these patterns when building React full-stack applications with Next.js App Router and Tailwind CSS.

## Project Structure

```
app/
  layout.tsx          # Root layout
  page.tsx            # Home page
  globals.css         # Global styles + Tailwind
  (auth)/             # Route group for auth pages
    login/page.tsx
    register/page.tsx
  dashboard/
    page.tsx
    layout.tsx
  api/                # API routes
    users/route.ts
components/
  ui/                 # Reusable UI components
    button.tsx
    input.tsx
    card.tsx
  forms/              # Form components
    login-form.tsx
  layouts/            # Layout components
    header.tsx
    sidebar.tsx
lib/
  utils.ts            # Utility functions
  db.ts               # Database client
  auth.ts             # Auth utilities
types/
  index.ts            # TypeScript types
public/
  images/
tailwind.config.ts
next.config.js
package.json
```

## Naming Conventions

- **Files**: kebab-case (`user-profile.tsx`)
- **Components**: PascalCase (`UserProfile`)
- **Utilities**: camelCase (`formatDate`)
- **Types**: PascalCase (`User`, `CreateUserInput`)
- **CSS classes**: Tailwind utilities, kebab-case for custom

## Root Layout

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My App',
  description: 'Built with Next.js',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

## Page Component

```tsx
// app/page.tsx
import { Button } from '@/components/ui/button'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-8">Welcome</h1>
      <Button>Get Started</Button>
    </main>
  )
}
```

## Server Component with Data Fetching

```tsx
// app/users/page.tsx
import { getUsers } from '@/lib/db'
import { UserCard } from '@/components/user-card'

export default async function UsersPage() {
  const users = await getUsers()

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Users</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {users.map((user) => (
          <UserCard key={user.id} user={user} />
        ))}
      </div>
    </div>
  )
}
```

## Client Component

```tsx
// components/forms/login-form.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)

    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })

    if (res.ok) {
      router.push('/dashboard')
    }
    setLoading(false)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <Input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <Button type="submit" disabled={loading} className="w-full">
        {loading ? 'Loading...' : 'Sign In'}
      </Button>
    </form>
  )
}
```

## Server Action

```tsx
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { db } from '@/lib/db'

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string

  await db.user.create({
    data: { name, email },
  })

  revalidatePath('/users')
  redirect('/users')
}
```

## API Route

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/lib/db'

export async function GET() {
  const users = await db.user.findMany()
  return NextResponse.json(users)
}

export async function POST(request: NextRequest) {
  const body = await request.json()

  const user = await db.user.create({
    data: {
      name: body.name,
      email: body.email,
    },
  })

  return NextResponse.json(user, { status: 201 })
}
```

## Dynamic Route

```tsx
// app/users/[id]/page.tsx
import { notFound } from 'next/navigation'
import { getUser } from '@/lib/db'

export default async function UserPage({
  params,
}: {
  params: { id: string }
}) {
  const user = await getUser(params.id)

  if (!user) {
    notFound()
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold">{user.name}</h1>
      <p className="text-gray-600">{user.email}</p>
    </div>
  )
}
```

## UI Components

```tsx
// components/ui/button.tsx
import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline'
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          'px-4 py-2 rounded-md font-medium transition-colors',
          variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
          variant === 'secondary' && 'bg-gray-200 text-gray-900 hover:bg-gray-300',
          variant === 'outline' && 'border border-gray-300 hover:bg-gray-50',
          className
        )}
        {...props}
      />
    )
  }
)
Button.displayName = 'Button'
```

```tsx
// components/ui/input.tsx
import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn(
          'w-full px-3 py-2 border border-gray-300 rounded-md',
          'focus:outline-none focus:ring-2 focus:ring-blue-500',
          className
        )}
        {...props}
      />
    )
  }
)
Input.displayName = 'Input'
```

## Utility Functions

```tsx
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## Tailwind Config

```ts
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
      },
    },
  },
  plugins: [],
}
export default config
```

## Tips

- **Server Components by default** - Use `'use client'` only when needed
- **Server Actions** - Prefer over API routes for form submissions
- **Streaming** - Use `loading.tsx` for suspense boundaries
- **Metadata** - Export `metadata` object for SEO
- **Route groups** - Use `(folder)` for organization without URL impact
- **Parallel routes** - Use `@folder` for simultaneous rendering
