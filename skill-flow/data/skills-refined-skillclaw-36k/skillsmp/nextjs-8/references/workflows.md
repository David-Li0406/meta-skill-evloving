# Next.js Workflows Reference

## Contents
- Creating New Pages
- Adding API Routes
- Form-to-Email Flow
- Adding Dynamic Routes
- Deployment Checklist

## Creating New Pages

### New Static Page

1. Create directory: `app/[page-name]/page.tsx`
2. Add client directive if interactive
3. Import shared components

```tsx
// app/about/page.tsx
'use client'

import Navigation from '@/app/components/Navigation'
import Footer from '@/app/components/Footer'

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-black text-white">
      <Navigation />
      <section className="px-6 py-16">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl font-bold">About Us</h1>
        </div>
      </section>
      <Footer />
    </div>
  )
}
```

Copy this checklist and track progress:
- [ ] Create `app/[page-name]/page.tsx`
- [ ] Add `'use client'` if using hooks/events
- [ ] Import `Navigation` and `Footer`
- [ ] Add to navigation links in `Navigation.tsx`
- [ ] Test mobile and desktop views

## Adding API Routes

### New POST Endpoint

1. Create `app/api/[endpoint]/route.ts`
2. Export async function for HTTP method
3. Add validation and error handling

```typescript
// app/api/webinar/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

export async function POST(request: NextRequest) {
  try {
    const { name, email, webinarId } = await request.json()

    if (!name || !email || !webinarId) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 })
    }

    await resend.emails.send({
      from: 'noreply@xop.ai',
      to: [email],
      subject: 'Webinar Registration Confirmed',
      html: `<p>Hi ${name}, you're registered for webinar ${webinarId}!</p>`
    })

    return NextResponse.json({ success: true }, { status: 200 })
  } catch (error) {
    console.error('Webinar API error:', error)
    return NextResponse.json({ error: 'Registration failed' }, { status: 500 })
  }
}
```

Copy this checklist and track progress:
- [ ] Create `app/api/[name]/route.ts`
- [ ] Import `NextRequest`, `NextResponse`
- [ ] Add input validation
- [ ] Wrap in try/catch
- [ ] Log errors with context
- [ ] Return appropriate status codes

## Form-to-Email Flow

### Complete Implementation

**Step 1: Create form state**

```tsx
const [formData, setFormData] = useState({
  firstName: '',
  lastName: '',
  email: '',
  message: ''
})
const [isSubmitting, setIsSubmitting] = useState(false)
const [isSubmitted, setIsSubmitted] = useState(false)
const [error, setError] = useState('')
```

**Step 2: Create submit handler**

```tsx
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

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.error || 'Submission failed')
    }

    setIsSubmitted(true)
    setFormData({ firstName: '', lastName: '', email: '', message: '' })
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Something went wrong')
  } finally {
    setIsSubmitting(false)
  }
}
```

**Step 3: Create API route with Resend**

See the **resend** skill for email template patterns.

```typescript
// app/api/contact/route.ts
const { error } = await resend.emails.send({
  from: 'xop.ai <noreply@xop.ai>',
  to: ['matt@xop.ai'],
  subject: `Contact from ${firstName} ${lastName}`,
  html: `<div>...</div>`
})
```

**Step 4: Add form UI with states**

```tsx
<form onSubmit={handleSubmit}>
  <input name="firstName" value={formData.firstName} onChange={handleChange} />
  {error && <div className="text-red-400">{error}</div>}
  {isSubmitted && <div className="text-green-400">Submitted!</div>}
  <button disabled={isSubmitting}>
    {isSubmitting ? 'Sending...' : 'Send'}
  </button>
</form>
```

## Adding Dynamic Routes

### Content-Based Dynamic Route

1. Create `app/[section]/[slug]/page.tsx`
2. Use `useParams()` to get slug
3. Map slug to content data

```tsx
// app/solutions/[slug]/page.tsx
'use client'

import { useParams } from 'next/navigation'

const solutions: Record<string, { title: string; icon: string }> = {
  'engineer-efficiency': { title: 'Engineer Efficiency', icon: '⚡' },
  'service-desk-management': { title: 'Service Desk Management', icon: '📊' },
}

export default function SolutionPage() {
  const { slug } = useParams() as { slug: string }
  const solution = solutions[slug]

  if (!solution) {
    return <NotFoundComponent />
  }

  return (
    <div>
      <span>{solution.icon}</span>
      <h1>{solution.title}</h1>
    </div>
  )
}
```

Copy this checklist and track progress:
- [ ] Create `app/[section]/[slug]/page.tsx`
- [ ] Define content map with all valid slugs
- [ ] Handle invalid slugs with fallback UI
- [ ] Add links from parent pages
- [ ] Test all valid slug paths

## Deployment Checklist

### Pre-Deploy Validation

1. Build locally
2. Check for TypeScript errors
3. Verify environment variables

```bash
# Build and check for errors
npm run build

# Check TypeScript
npx tsc --noEmit

# Lint
npm run lint
```

Copy this checklist and track progress:
- [ ] Run `npm run build` - no errors
- [ ] Run `npm run lint` - no warnings
- [ ] Verify all environment variables documented
- [ ] Test forms submit to correct endpoints
- [ ] Check mobile responsiveness
- [ ] Verify all links work

### Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `RESEND_API_KEY` | Yes | Email delivery |
| `NEXT_PUBLIC_GA_MEASUREMENT_ID` | No | Google Analytics |

### Vercel Configuration

Deployment is automatic on push to main. Configuration in `next.config.ts`:

```typescript
// Redirects
async redirects() {
  return [
    { source: '/compare', destination: '/resources/compare', permanent: true },
  ]
}

// Security headers
async headers() {
  return [{
    source: '/:path*',
    headers: [
      { key: 'X-Frame-Options', value: 'DENY' },
    ],
  }]
}
```

See the **vercel** skill for deployment-specific configuration.