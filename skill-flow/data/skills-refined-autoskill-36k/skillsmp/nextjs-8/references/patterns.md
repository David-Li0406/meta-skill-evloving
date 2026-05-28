# Next.js Patterns Reference

## Contents
- Server vs Client Components
- API Route Patterns
- Dynamic Routes
- Form Handling
- Configuration
- Anti-Patterns

## Server vs Client Components

### Server Component (Default)

Use for: layouts, metadata, static content, data fetching.

```tsx
// app/layout.tsx - NO 'use client' directive
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'XOP.ai - AI Solutions Designed by MSPs, For MSPs',
  description: '28 years of MSP experience + cutting-edge Rezolve.ai technology',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID && (
          <GoogleAnalytics measurementId={process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID} />
        )}
        {children}
      </body>
    </html>
  )
}
```

### Client Component (Interactive)

Use for: forms, dropdowns, modals, any useState/useEffect.

```tsx
// app/contact/page.tsx
'use client'

import { useState } from 'react'
import Navigation from '@/app/components/Navigation'

export default function ContactPage() {
  const [formData, setFormData] = useState({ firstName: '', email: '' })
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    // ... submit logic
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <Navigation />
      <form onSubmit={handleSubmit}>...</form>
    </div>
  )
}
```

## API Route Patterns

### POST Handler with Validation

```typescript
// app/api/contact/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { firstName, lastName, email, message } = body

    // Validate required fields
    if (!firstName || !email || !message) {
      return NextResponse.json({ error: 'All fields are required' }, { status: 400 })
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      return NextResponse.json({ error: 'Invalid email format' }, { status: 400 })
    }

    // Process (e.g., send email via Resend)
    const { error } = await resend.emails.send({
      from: 'noreply@xop.ai',
      to: ['matt@xop.ai'],
      subject: `Contact from ${firstName}`,
      html: `<p>${message}</p>`
    })

    if (error) {
      return NextResponse.json({ error: 'Failed to send' }, { status: 500 })
    }

    return NextResponse.json({ success: true }, { status: 200 })
  } catch (error) {
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
```

### Dynamic Route API Handler

```typescript
// app/api/pdf/[slug]/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params  // Note: params is a Promise in Next.js 15

  const validSlugs = ['engineer-app-v4', 'teams-chatbot']
  if (!validSlugs.includes(slug)) {
    return NextResponse.json({ error: 'Invalid slug' }, { status: 404 })
  }

  return NextResponse.json({ data: slug })
}
```

## Dynamic Routes

### Client-Side Dynamic Page

```tsx
// app/solutions/[slug]/page.tsx
'use client'

import { useParams } from 'next/navigation'

const solutionData: Record<string, { title: string; description: string }> = {
  'engineer-efficiency': {
    title: 'Engineer Efficiency',
    description: 'Free up engineers to solve complex problems'
  }
}

export default function SolutionPage() {
  const params = useParams()
  const slug = params.slug as string
  const solution = solutionData[slug]

  if (!solution) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <h1>Solution Not Found</h1>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <h1>{solution.title}</h1>
      <p>{solution.description}</p>
    </div>
  )
}
```

## Form Handling

### Complete Form Pattern

```tsx
const [formData, setFormData] = useState({
  firstName: '',
  email: '',
  message: ''
})
const [isSubmitting, setIsSubmitting] = useState(false)
const [isSubmitted, setIsSubmitted] = useState(false)
const [error, setError] = useState('')

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  setIsSubmitting(true)
  setError('')

  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    })

    const data = await response.json()
    if (!response.ok) throw new Error(data.error || 'Something went wrong')

    setIsSubmitted(true)
    setFormData({ firstName: '', email: '', message: '' })
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Something went wrong')
  } finally {
    setIsSubmitting(false)
  }
}

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setFormData({ ...formData, [e.target.name]: e.target.value })
}
```

## Configuration

### next.config.ts Pattern

```typescript
import type { NextConfig } from "next"

const nextConfig: NextConfig = {
  images: {
    unoptimized: true,  // Simpler static hosting
    remotePatterns: [{ protocol: 'https', hostname: '**' }],
  },

  async redirects() {
    return [
      { source: '/compare', destination: '/resources/compare', permanent: true },
    ]
  },

  async headers() {
    return [{
      source: '/:path*',
      headers: [
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
      ],
    }]
  },
}

export default nextConfig
```

## Anti-Patterns

### WARNING: Using `'use client'` in Layout

**The Problem:**

```tsx
// BAD - Makes entire subtree client-rendered
'use client'

export default function RootLayout({ children }) {
  return <html><body>{children}</body></html>
}
```

**Why This Breaks:**
1. Loses server-side metadata generation
2. Increases JavaScript bundle size
3. Slower initial page load

**The Fix:**

```tsx
// GOOD - Layout stays server component
import type { Metadata } from 'next'

export const metadata: Metadata = { title: 'My Site' }

export default function RootLayout({ children }) {
  return <html><body>{children}</body></html>
}
```

### WARNING: Missing Error Handling in API Routes

**The Problem:**

```typescript
// BAD - Unhandled errors crash the route
export async function POST(request: NextRequest) {
  const body = await request.json()
  await sendEmail(body.email)
  return NextResponse.json({ success: true })
}
```

**The Fix:**

```typescript
// GOOD - Try/catch with proper error responses
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    await sendEmail(body.email)
    return NextResponse.json({ success: true }, { status: 200 })
  } catch (error) {
    console.error('API error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}