---
title: Use formAction for Progressive Enhancement
impact: HIGH
impactDescription: Forms work without JavaScript and have better accessibility
tags: server-actions, forms, progressive-enhancement, accessibility
---

## Use formAction for Progressive Enhancement

Server Actions with formAction work even when JavaScript is disabled or fails to load. This improves reliability and accessibility.

**Incorrect (JavaScript-only form):**

```typescript
'use client'

export function ContactForm() {
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    // ❌ Form broken if JS fails
    // ❌ Must manage loading state manually
    await fetch('/api/contact', {
      method: 'POST',
      body: new FormData(e.target)
    })
    setLoading(false)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <button disabled={loading}>Submit</button>
    </form>
  )
}
```

**Correct (Server Action with formAction):**

```typescript
// app/contact/actions.ts
'use server'

import { redirect } from 'next/navigation'

export async function submitContact(formData: FormData) {
  const email = formData.get('email')

  await db.contacts.create({ data: { email } })

  redirect('/contact/success')
}

// app/contact/page.tsx
import { submitContact } from './actions'

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <input name="email" type="email" required />
      <button type="submit">Submit</button>
      {/* ✓ Works without JS */}
      {/* ✓ Native form validation */}
      {/* ✓ Browser handles loading state */}
    </form>
  )
}
```

**Enhanced with useFormStatus:**

```typescript
'use client'
import { useFormStatus } from 'react-dom'

function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  )
}

// In page (Server Component)
import { submitContact } from './actions'

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <input name="email" type="email" required />
      <SubmitButton />
    </form>
  )
}
```

**Multiple actions in one form:**

```typescript
<form>
  <input name="item" />
  <button formAction={addItem}>Add</button>
  <button formAction={clearAll}>Clear All</button>
</form>
```

Reference: [Server Actions and Forms](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
