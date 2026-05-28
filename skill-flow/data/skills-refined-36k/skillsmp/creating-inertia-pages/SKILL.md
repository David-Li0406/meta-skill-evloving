---
name: creating-inertia-pages
description: Create Inertia.js page components with TypeScript, forms, and navigation. Use when creating pages, implementing routes, handling forms, or when user mentions pages, Inertia pages, router, or page navigation.
---

# Create Inertia.js Pages

Create Inertia.js page components with TypeScript, forms, and navigation. Pages receive props from Laravel controllers, handle form submissions via the `useForm` hook, and navigate using the Inertia router without full page reloads.

## File Structure

Pages are organized by feature or domain:

```
resources/js/pages/{feature}/{name}.tsx
```

**Examples:**

- `resources/js/pages/auth/login.tsx`
- `resources/js/pages/auth/register.tsx`
- `resources/js/pages/dashboard.tsx`
- `resources/js/pages/profile/edit.tsx`

## Core Conventions

### 1. Page Component Structure

Pages must use **default exports** (unlike other components):

```tsx
import { AuthenticatedLayout } from '@/layouts/authenticated-layout'
import { useTranslation } from 'react-i18next'

export default function Dashboard() {
  const { t } = useTranslation()

  return (
    <AuthenticatedLayout title={t('dashboard')}>
      <h1 className="text-2xl font-bold">{t('welcome')}</h1>
      <DashboardContent />
    </AuthenticatedLayout>
  )
}
```

**Key Requirements:**

- Use function declarations for pages (NOT arrow functions assigned to const)
- Use **default export** for page components (exception to named export rule)
- Wrap content in a Layout component
- Use `useTranslation()` for i18n
- Type props with `PageProps` from Inertia

### 2. Accessing Inertia Props

Use `usePage()` to access props passed from Laravel:

```tsx
import type { PageProps } from '@/types'
import { usePage } from '@inertiajs/react'

interface DashboardProps extends PageProps {
  stats: {
    users: number
    posts: number
  }
}

export default function Dashboard() {
  const { stats } = usePage<DashboardProps>().props

  return (
    <div>
      <p>Users: {stats.users}</p>
      <p>Posts: {stats.posts}</p>
    </div>
  )
}
```

**Shared props** (available on all pages):

```tsx
export default function Header() {
  const { user, supportedLocales } = usePage().props

  return <header>{user && <span>Welcome, {user.name}</span>}</header>
}
```

### 3. Form Handling with Inertia

Use `router` for form submissions:

```tsx
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useFormValidation } from '@/hooks/use-form-validation'
import { zodResolver } from '@hookform/resolvers/zod'
import { router } from '@inertiajs/react'
import { useForm } from 'react-hook-form'
import { useTranslation } from 'react-i18next'
import { z } from 'zod'

const formSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export default function Login() {
  const { t } = useTranslation()
  const { setFormServerErrors } = useFormValidation()

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    await new Promise<void>((resolve) =>
      router.post(route('login'), values, {
        onError: (errors) => {
          setFormServerErrors(form, errors)
        },
        onFinish: () => resolve(),
      })
    )
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <Input {...form.register('email')} />
      <Input {...form.register('password')} type="password" />
      <Button type="submit" loading={form.formState.isSubmitting}>
        {t('logIn')}
      </Button>
    </form>
  )
}
```

### 4. Navigation with Inertia Router

**Using `router.get()`:**

```tsx
import { router } from '@inertiajs/react'

export function NavigationButton() {
  const navigate = () => {
    router.get(route('dashboard'))
  }

  return <Button onClick={navigate}>Go to Dashboard</Button>
}
```

**Using `Link` component:**

```tsx
import { Link } from '@inertiajs/react'

export function Navigation() {
  return (
    <nav>
      <Link href={route('dashboard')}>Dashboard</Link>
      <Link href={route('profile.edit')}>Profile</Link>
    </nav>
  )
}
```

## Examples

### Example 1: Simple Page

```tsx
import { GuestLayout } from '@/layouts/guest-layout'
import { useTranslation } from 'react-i18next'

export default function Welcome() {
  const { t } = useTranslation()

  return (
    <GuestLayout title={t('welcome')}>
      <h1 className="text-4xl font-bold">{t('welcome')}</h1>
      <p className="mt-4 text-lg">{t('welcomeDescription')}</p>
    </GuestLayout>
  )
}
```

### Example 2: Page with Props

```tsx
import { AuthenticatedLayout } from '@/layouts/authenticated-layout'
import type { User } from '@/types/models'
import type { PageProps, PaginatedData } from '@/types'
import { usePage } from '@inertiajs/react'

interface UsersIndexProps extends PageProps {
  users: PaginatedData<User>
}

export default function UsersIndex() {
  const { users } = usePage<UsersIndexProps>().props

  return (
    <AuthenticatedLayout title="Users">
      <h1 className="text-2xl font-bold">Users</h1>

      <div className="mt-6 space-y-4">
        {users.data.map((user) => (
          <UserCard key={user.id} user={user} />
        ))}
      </div>

      <Pagination meta={users.meta} />
    </AuthenticatedLayout>
  )
}
```

### Example 3: Form Page

```tsx
import { AuthForm, AuthFormFooter } from '@/components/auth-form'
import { Text } from '@/components/text'
import { TextLink } from '@/components/text-link'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { useFormValidation } from '@/hooks/use-form-validation'
import { GuestLayout } from '@/layouts/guest-layout'
import { zodResolver } from '@hookform/resolvers/zod'
import { router } from '@inertiajs/react'
import { useForm } from 'react-hook-form'
import { useTranslation } from 'react-i18next'
import { z } from 'zod'

const formSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  password: z.string().min(8),
  password_confirmation: z.string().min(8),
})

export default function Register() {
  const { t } = useTranslation()
  const { setFormServerErrors, passwordConfirmationMessage } =
    useFormValidation()

  formSchema.refine(
    (data) => data.password === data.password_confirmation,
    passwordConfirmationMessage
  )

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
      password: '',
      password_confirmation: '',
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    await new Promise<void>((resolve) =>
      router.post(
        route('register'),
        {
          ...values,
          language: navigator.language,
        },
        {
          onError: (errors) => {
            setFormServerErrors(form, errors)
          },
          onFinish: () => resolve(),
        }
      )
    )
  }

  return (
    <GuestLayout title={t('registerNewAccount')}>
      <AuthForm
        description={t('registerNewAccountDescription')}
        title={t('registerNewAccount')}
      >
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>{t('name')}</FormLabel>
                  <FormControl>
                    <Input autoComplete="name" required {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>{t('email')}</FormLabel>
                  <FormControl>
                    <Input
                      autoComplete="username"
                      inputMode="email"
                      required
                      type="email"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              loading={form.formState.isSubmitting}
              className="w-full"
              type="submit"
            >
              {t('register')}
            </Button>
          </form>
        </Form>

        <AuthFormFooter>
          <Text size="sm" variant="muted">
            {t('alreadyHaveAccount') + ' '}
            <TextLink href={route('login')}>{t('logIn')}</TextLink>
          </Text>
        </AuthFormFooter>
      </AuthForm>
    </GuestLayout>
  )
}
```

## Anti-Patterns

### ❌ Don't Do This

```tsx
// Don't use arrow functions assigned to const for pages
const Dashboard = () => {
  // ❌ Use function declaration
  return <div>Content</div>
}
export default Dashboard

// Don't use named exports for pages
export function Dashboard() {} // ❌ Must use default export

// Don't forget to wrap in layout
export default function Dashboard() {
  return <div>Content</div> // ❌ Missing layout
}

// Don't use untyped props
export default function Users() {
  const { users } = usePage().props // ❌ Missing type
}

// Don't navigate with window.location
export function Button() {
  const navigate = () => {
    window.location.href = '/dashboard' // ❌ Use router.get()
  }
}

// Don't forget error handling
async function onSubmit(values) {
  router.post(route('login'), values) // ❌ Missing onError
}
```

### ✅ Do This Instead

```tsx
// Use default exports
export default function Dashboard() {}

// Always wrap in layout
export default function Dashboard() {
  return (
    <AuthenticatedLayout title="Dashboard">
      <div>Content</div>
    </AuthenticatedLayout>
  )
}

// Type props with PageProps
interface UsersProps extends PageProps {
  users: User[]
}

export default function Users() {
  const { users } = usePage<UsersProps>().props
}

// Use Inertia router
export function Button() {
  const navigate = () => {
    router.get(route('dashboard'))
  }
}

// Handle errors
async function onSubmit(values: FormValues) {
  await new Promise<void>((resolve) =>
    router.post(route('login'), values, {
      onError: (errors) => {
        setFormServerErrors(form, errors)
      },
      onFinish: () => resolve(),
    })
  )
}
```

## Router Methods

**Navigation:**

```tsx
router.get(route('dashboard'))
router.visit(route('profile.edit'))
```

**Form submissions:**

```tsx
router.post(route('login'), data, { onError, onFinish })
router.put(route('profile.update'), data)
router.patch(route('user.update', userId), data)
router.delete(route('user.destroy', userId))
```

**Reload current page:**

```tsx
router.reload()
router.reload({ only: ['users'] }) // Only reload 'users' prop
```

## Quality Standards

- All pages must use **default exports**
- Wrap all pages in layout components
- Type page props with `PageProps<T>`
- Use `router` for navigation and form submissions
- Handle form errors with `onError` callback
- Use `route()` helper for all URLs
- Test pages with Pest browser tests
- Ensure responsive design and accessibility
