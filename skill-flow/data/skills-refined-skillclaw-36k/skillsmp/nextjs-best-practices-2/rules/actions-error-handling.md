---
title: Return Error States from Server Actions
impact: HIGH
impactDescription: Provides actionable feedback without crashing the app
tags: errors, server-actions, validation, ux
---

## Return Error States from Server Actions

Don't throw errors in Server Actions - return error states that the client can display. Throwing errors makes it hard to show contextual feedback.

**Incorrect (throwing errors):**

```typescript
'use server'

export async function createUser(formData: FormData) {
  const email = formData.get('email') as string

  if (!email.includes('@')) {
    throw new Error('Invalid email') // ❌ Caught by error boundary
  }

  const exists = await db.users.findUnique({ where: { email } })
  if (exists) {
    throw new Error('User already exists') // ❌ No field-level feedback
  }

  await db.users.create({ data: { email } })
}
```

**Correct (returning error states):**

```typescript
'use server'

import { z } from 'zod'

const schema = z.object({
  email: z.string().email('Please enter a valid email'),
  name: z.string().min(2, 'Name must be at least 2 characters')
})

type ActionState = {
  success: boolean
  errors?: {
    email?: string[]
    name?: string[]
    _form?: string[]
  }
}

export async function createUser(
  prevState: ActionState,
  formData: FormData
): Promise<ActionState> {
  // Validate
  const result = schema.safeParse({
    email: formData.get('email'),
    name: formData.get('name')
  })

  if (!result.success) {
    return {
      success: false,
      errors: result.error.flatten().fieldErrors
    }
  }

  // Check uniqueness
  const exists = await db.users.findUnique({
    where: { email: result.data.email }
  })

  if (exists) {
    return {
      success: false,
      errors: { email: ['This email is already registered'] }
    }
  }

  // Create user
  try {
    await db.users.create({ data: result.data })
    return { success: true }
  } catch (e) {
    return {
      success: false,
      errors: { _form: ['Failed to create account. Please try again.'] }
    }
  }
}
```

**Client component with useFormState:**

```typescript
'use client'
import { useFormState } from 'react-dom'
import { createUser } from './actions'

export function SignupForm() {
  const [state, action] = useFormState(createUser, { success: false })

  return (
    <form action={action}>
      <div>
        <input name="email" type="email" />
        {state.errors?.email && (
          <p className="text-red-500">{state.errors.email[0]}</p>
        )}
      </div>

      <div>
        <input name="name" />
        {state.errors?.name && (
          <p className="text-red-500">{state.errors.name[0]}</p>
        )}
      </div>

      {state.errors?._form && (
        <p className="text-red-500">{state.errors._form[0]}</p>
      )}

      <SubmitButton />
    </form>
  )
}
```

Reference: [Server Actions Error Handling](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations#error-handling)
