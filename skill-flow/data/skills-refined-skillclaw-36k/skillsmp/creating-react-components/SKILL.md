---
name: creating-react-components
description: Create reusable React components with TypeScript, Tailwind CSS, and shadcn/ui. Use when creating components, building UI elements, implementing reusable widgets, or when user mentions components, UI, buttons, cards, forms, or reusable elements.
---

# Create React Components

Create reusable React components with TypeScript, Tailwind CSS, and shadcn/ui patterns. Components are function-based with typed props interfaces, following composition patterns for flexibility and the project's naming conventions.

## File Structure

Components are organized in a flat structure:

```
resources/js/components/{name}.tsx
```

**Examples:**

- `resources/js/components/auth-form.tsx`
- `resources/js/components/user-avatar.tsx`
- `resources/js/components/app-footer.tsx`

**shadcn/ui components:**

```
resources/js/components/ui/{name}.tsx
```

Generated via `npx shadcn@latest add {component-name}`.

## Core Conventions

### 1. Component Structure

Components must follow React 19 patterns:

```tsx
import type { PropsWithChildren } from 'react'

interface CardProps {
  title: string
  description?: string
  variant?: 'default' | 'outlined'
}

export function Card({
  title,
  description,
  variant = 'default',
  children,
}: PropsWithChildren<CardProps>) {
  return (
    <div className="rounded-lg border p-6">
      <h3 className="text-lg font-semibold">{title}</h3>
      {description && (
        <p className="text-muted-foreground mt-2 text-sm">{description}</p>
      )}
      <div className="mt-4">{children}</div>
    </div>
  )
}
```

**Key Requirements:**

- Use function components (NOT `React.FC` or `FunctionComponent`)
- Use function declarations for components (NOT arrow functions assigned to const)
- Use `PropsWithChildren<T>` for components accepting children
- Export components with named exports (NOT default exports)
- TypeScript props interface above the component
- Use optional chaining and optional props with defaults

### 2. Function Declaration Style

**Always use function declarations for components:**

```tsx
// ✅ Correct: Function declaration
export function Button({ label }: ButtonProps) {
  return <button>{label}</button>
}
```

**Use function declarations for helper functions within components:**

```tsx
export function ProductCard({ product }: ProductCardProps) {
  // ✅ Function declaration for helpers
  function calculateDiscount(price: number, discount: number): number {
    return price * (1 - discount)
  }

  const finalPrice = calculateDiscount(product.price, product.discount)

  return <div>{finalPrice}</div>
}
```

This pattern makes it clear what is a function versus a variable, improving code readability and maintainability.

### 3. Props Interface Patterns

**Simple props:**

```tsx
interface ButtonProps {
  label: string
  onClick: () => void
  disabled?: boolean
}

export function Button({ label, onClick, disabled = false }: ButtonProps) {
  // ...
}
```

**Props with children:**

```tsx
interface CardProps {
  title: string
}

export function Card({ title, children }: PropsWithChildren<CardProps>) {
  // ...
}
```

**Props extending HTML attributes:**

```tsx
import type { HTMLAttributes } from 'react'

interface ContainerProps extends HTMLAttributes<HTMLDivElement> {
  maxWidth?: 'sm' | 'md' | 'lg'
}

export function Container({
  maxWidth = 'lg',
  className,
  ...props
}: ContainerProps) {
  return <div className={cn('container', className)} {...props} />
}
```

### 4. Styling with Tailwind

Use Tailwind CSS v4 utility classes:

```tsx
export function Alert({ children }: PropsWithChildren) {
  return (
    <div className="rounded-md border border-yellow-200 bg-yellow-50 p-4">
      <div className="flex items-start gap-3">
        <AlertCircle className="size-5 text-yellow-600" />
        <div className="text-sm text-yellow-800">{children}</div>
      </div>
    </div>
  )
}
```

Use the `cn()` utility from shadcn/ui for conditional classes:

```tsx
import { cn } from '@/lib/utils'

interface BadgeProps {
  variant?: 'default' | 'success' | 'error'
}

export function Badge({
  variant = 'default',
  children,
}: PropsWithChildren<BadgeProps>) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
        {
          'bg-gray-100 text-gray-800': variant === 'default',
          'bg-green-100 text-green-800': variant === 'success',
          'bg-red-100 text-red-800': variant === 'error',
        }
      )}
    >
      {children}
    </span>
  )
}
```

### 5. Using shadcn/ui Components

Import and compose shadcn/ui components:

```tsx
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { useTranslation } from 'react-i18next'

interface StatsCardProps {
  title: string
  value: string
  description: string
  onViewDetails: () => void
}

export function StatsCard({
  title,
  value,
  description,
  onViewDetails,
}: StatsCardProps) {
  const { t } = useTranslation()

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold">{value}</div>
        <Button onClick={onViewDetails} variant="outline" className="mt-4">
          {t('viewDetails')}
        </Button>
      </CardContent>
    </Card>
  )
}
```

### 6. Localization

**All user-facing text must use `useTranslation()` for i18n:**

```tsx
import { useTranslation } from 'react-i18next'

interface WelcomeMessageProps {
  userName: string
}

export function WelcomeMessage({ userName }: WelcomeMessageProps) {
  const { t } = useTranslation()

  return (
    <div>
      <h1>{t('welcome')}</h1>
      <p>{t('greeting', { name: userName })}</p>
    </div>
  )
}
```

**When to use translations:**

- Button labels, link text, headings
- Error messages, success messages, notifications
- Form labels, placeholders, helper text
- Any text visible to users

**When NOT to use translations:**

- Developer-only content (console logs, error boundaries)
- Data passed as props (already translated)
- Technical identifiers (IDs, keys, enums)

## Examples

### Example 1: Simple Component

```tsx
import type { User } from '@/types/models'

interface UserAvatarProps {
  user: User
  size?: 'sm' | 'md' | 'lg'
}

export function UserAvatar({ user, size = 'md' }: UserAvatarProps) {
  const sizeClasses = {
    sm: 'size-8 text-xs',
    md: 'size-10 text-sm',
    lg: 'size-12 text-base',
  }

  return (
    <div
      className={cn(
        'bg-primary text-primary-foreground flex items-center justify-center rounded-full',
        sizeClasses[size]
      )}
    >
      {user.avatar_url ? (
        <img
          src={user.avatar_url}
          alt={user.name}
          className="size-full rounded-full object-cover"
        />
      ) : (
        <span>{user.name.charAt(0).toUpperCase()}</span>
      )}
    </div>
  )
}
```

### Example 2: Component with Multiple Sub-components

```tsx
import { Heading } from '@/components/heading'
import { Text } from '@/components/text'
import type { PropsWithChildren } from 'react'

export function AuthFormFooter({ children }: PropsWithChildren) {
  return <div className="mt-6">{children}</div>
}

interface AuthFormProps {
  title: string
  description: string
}

export function AuthForm({
  title,
  description,
  children,
}: PropsWithChildren<AuthFormProps>) {
  return (
    <div className="w-full space-y-10 sm:max-w-sm">
      <div className="space-y-2">
        <Heading>{title}</Heading>
        <Text size="sm" variant="muted">
          {description}
        </Text>
      </div>

      {children}
    </div>
  )
}
```

## Anti-Patterns

### ❌ Don't Do This

```tsx
// Don't use React.FC
export const Button: React.FC<ButtonProps> = ({ children }) => {
  return <button>{children}</button>
}

// Don't use arrow functions assigned to const
export const Card = ({ children }: PropsWithChildren) => {
  return <div>{children}</div>
}

// Don't use default exports (except for pages)
export default function Card() {}

// Don't inline large components
export function Dashboard() {
  return (
    <div>
      <div className="...">
        <h1>...</h1>
        {/* 200 lines of JSX */}
      </div>
    </div>
  )
}

// Don't skip TypeScript types
export function Button({ label, onClick }) {
  // ❌ No type annotations
}

// Don't use inline styles
export function Card() {
  return <div style={{ padding: '16px' }}>...</div>
}

// Don't hardcode user-facing text
export function SubmitButton() {
  return <button>Submit</button> // ❌ Use t('submit')
}

// Don't forget to import useTranslation
export function WelcomeMessage() {
  return <h1>Welcome</h1> // ❌ Use t('welcome')
}
```

### ✅ Do This Instead

```tsx
// Use function components
export function Button({ children }: PropsWithChildren) {
  return <button>{children}</button>
}

// Use named exports
export function Card() {}

// Extract components
export function Dashboard() {
  return (
    <div>
      <DashboardHeader />
      <DashboardContent />
      <DashboardFooter />
    </div>
  )
}

// Always type props
interface ButtonProps {
  label: string
  onClick: () => void
}

export function Button({ label, onClick }: ButtonProps) {}

// Use Tailwind classes
export function Card({ children }: PropsWithChildren) {
  return <div className="rounded-lg p-4">{children}</div>
}

// Use translations for user-facing text
export function SubmitButton() {
  const { t } = useTranslation()
  return <button>{t('submit')}</button>
}

// Always import useTranslation for text
export function WelcomeMessage() {
  const { t } = useTranslation()
  return <h1>{t('welcome')}</h1>
}
```

## Importing Components

Use path aliases:

```tsx
// Components
import { Button } from '@/components/ui/button'
import { UserAvatar } from '@/components/user-avatar'

// Types
import type { User } from '@/types/models'

// Hooks
import { useTranslation } from 'react-i18next'
import { useUser } from '@/contexts/user-context'

// Utils
import { cn } from '@/lib/utils'
```

## Quality Standards

- All components must be fully typed (no `any`)
- **All user-facing text must use `useTranslation()` for i18n**
- Use ESLint and Prettier for formatting
- Prefer composition over prop drilling
- Keep components focused and single-purpose
- Use semantic HTML elements
- Ensure accessibility (ARIA labels, keyboard navigation)
- Test components with Pest browser tests (see `writing-browser-tests` skill)
