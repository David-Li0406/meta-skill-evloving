# Forms & Testing

## Table of Contents

1. [Form Rules](#form-rules)
2. [Testing Rules](#testing-rules)

---

## Form Rules

Use **React Hook Form** with **Zod** for validation.

### Principles

- All validation lives in Zod schemas
- Presenters contain no async logic
- Never duplicate schema validation in UI attributes
- Form-level errors must be visible and actionable

### Feature Form Structure

```
features/<feature>/
├─ forms/
│  ├─ <schema>.ts           # Zod schema
│  └─ use-<form>-form.ts    # Form hook
├─ components/
│  └─ <Form>.tsx            # Form component
```

### Example Schema

```tsx
// forms/create-order.schema.ts
import { z } from 'zod'
import { isAddress } from 'ethers'

export const createOrderSchema = z.object({
  amount: z.string().min(1, 'Amount is required'),
  recipient: z.string().refine(isAddress, 'Invalid address'),
})

export type CreateOrderInput = z.infer<typeof createOrderSchema>
```

### Example Form Hook

```tsx
// forms/use-create-order-form.ts
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { createOrderSchema, CreateOrderInput } from './create-order.schema'

export function useCreateOrderForm() {
  return useForm<CreateOrderInput>({
    resolver: zodResolver(createOrderSchema),
    defaultValues: {
      amount: '',
      recipient: '',
    },
  })
}
```

---

## Testing Rules

**Stack**: Vitest + React Testing Library + MSW

### Test Behavior, Not Internals

- **Presenters**: test UI output based on props
- **Containers**: test async states via mock responses
- **Forms**: test via input + submit + visible error

### Do NOT Test

- Tailwind classes
- Internal helpers
- Third-party logic (Radix, RHF, Query internals)

> **Interaction Testing in Storybook:** In addition to Vitest, you can write and run interaction tests directly in the browser with Storybook's `play` function. This is an excellent way to verify complex user flows. See the [Advanced Storybook Guide](advanced-storybook.md) for examples.

### Example Presenter Test

```tsx
import { render, screen } from '@testing-library/react'
import { RevenueCardView } from './RevenueCardView'

describe('RevenueCardView', () => {
  it('shows loading state', () => {
    render(<RevenueCardView state="loading" />)
    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('shows error with message', () => {
    render(<RevenueCardView state="error" message="Failed to load" />)
    expect(screen.getByText('Failed to load')).toBeInTheDocument()
  })

  it('shows empty state with message', () => {
    render(<RevenueCardView state="empty" message="No data yet" />)
    expect(screen.getByText('No data yet')).toBeInTheDocument()
  })

  it('renders value in ready state', () => {
    render(<RevenueCardView state="ready" value={1000} previousValue={900} />)
    expect(screen.getByText('$1,000')).toBeInTheDocument()
  })
})
```

### Example Form Test

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { CreateOrderForm } from './CreateOrderForm'

describe('CreateOrderForm', () => {
  it('shows validation error for invalid address', async () => {
    render(<CreateOrderForm onSubmit={vi.fn()} />)

    await userEvent.type(screen.getByLabelText('Recipient'), 'invalid')
    await userEvent.click(screen.getByRole('button', { name: 'Submit' }))

    expect(screen.getByText('Invalid address')).toBeInTheDocument()
  })
})
```
