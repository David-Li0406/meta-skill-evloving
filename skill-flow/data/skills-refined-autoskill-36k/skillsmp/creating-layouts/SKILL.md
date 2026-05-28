---
name: creating-layouts
description: Create React layout components for Inertia.js pages with TypeScript and AppHead. Use when creating layouts, wrapping pages, implementing navigation, or when user mentions layouts, authenticated layout, guest layout, or page wrappers.
---

# Create React Layouts

Create layout components that wrap Inertia.js pages with shared navigation and structure. Layouts provide consistent headers, sidebars, and footers across pages, assigned via the `layout` property on page components.

## File Structure

Layouts are organized in a flat structure:

```
resources/js/layouts/{name}-layout.tsx
```

**Examples:**

- `resources/js/layouts/authenticated-layout.tsx`
- `resources/js/layouts/guest-layout.tsx`
- `resources/js/layouts/admin-layout.tsx`

## Core Conventions

### 1. Layout Structure

Layouts wrap page content and include `AppHead`:

```tsx
import { AppHead } from '@/components/app-head'
import { AppFooter } from '@/components/app-footer'
import { Navigation } from '@/components/navigation'
import type { PropsWithChildren } from 'react'

interface LayoutProps {
  title?: string
}

export function MainLayout({
  title,
  children,
}: PropsWithChildren<LayoutProps>) {
  return (
    <>
      <AppHead title={title} />

      <div className="flex min-h-screen flex-col">
        <Navigation />

        <main className="flex-1 px-4 py-6 lg:px-8">{children}</main>

        <AppFooter />
      </div>
    </>
  )
}
```

**Key Requirements:**

- Use function declarations for layouts (NOT arrow functions assigned to const)
- Always use `PropsWithChildren<Props>`
- Include `<AppHead title={title} />` for page metadata
- Accept optional `title` prop
- Render `{children}` where page content should appear
- Use semantic HTML (`<main>`, `<header>`, `<footer>`)
- **Use `useTranslation()` for all user-facing text**

### 2. AppHead Component

Use `AppHead` for document head management:

```tsx
import { AppHead } from '@/components/app-head'

export function GuestLayout({
  title,
  children,
}: PropsWithChildren<{ title?: string }>) {
  return (
    <>
      <AppHead title={title} />
      <div className="min-h-screen bg-gray-50">{children}</div>
    </>
  )
}
```

The `AppHead` component handles:

- Page title
- Meta tags
- Open Graph tags
- Favicon

### 3. Layouts with Inertia Shared Data

Access shared Inertia props when needed:

```tsx
import { AppHead } from '@/components/app-head'
import { UserMenu } from '@/components/user-menu'
import { usePage } from '@inertiajs/react'
import type { PropsWithChildren } from 'react'

export function AuthenticatedLayout({
  title,
  children,
}: PropsWithChildren<{ title?: string }>) {
  const { user } = usePage().props

  return (
    <>
      <AppHead title={title} />

      <div className="min-h-screen">
        <header className="border-b bg-white px-4 py-3">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-semibold">App Name</h1>
            {user && <UserMenu user={user} />}
          </div>
        </header>

        <main className="p-6">{children}</main>
      </div>
    </>
  )
}
```

### 4. Complex Layouts with Sidebars

Use shadcn/ui Sidebar components:

```tsx
import { AppFooter } from '@/components/app-footer'
import { AppHead } from '@/components/app-head'
import { AppSidebar } from '@/components/app-sidebar'
import { MobileHeader } from '@/components/mobile-header'
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar'
import type { PropsWithChildren } from 'react'
import { useCookie } from 'react-use'

export function AuthenticatedLayout({
  title,
  children,
}: PropsWithChildren<{ title?: string }>) {
  const [value] = useCookie('sidebar_state')
  const defaultOpen = value === null || value === 'true'

  return (
    <>
      <AppHead title={title} />

      <SidebarProvider defaultOpen={defaultOpen}>
        <div className="flex h-full w-full flex-col lg:flex-row">
          <MobileHeader />

          <AppSidebar />

          <SidebarInset className="flex flex-col justify-between">
            <main className="px-4 py-6 lg:p-10">{children}</main>
            <AppFooter />
          </SidebarInset>
        </div>
      </SidebarProvider>
    </>
  )
}
```

## Examples

### Example 1: Simple Guest Layout

```tsx
import { AppHead } from '@/components/app-head'
import type { PropsWithChildren } from 'react'

export function GuestLayout({
  title,
  children,
}: PropsWithChildren<{ title?: string }>) {
  return (
    <>
      <AppHead title={title} />

      <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
        <div className="w-full max-w-md">{children}</div>
      </div>
    </>
  )
}
```

Usage in page:

```tsx
import { GuestLayout } from '@/layouts/guest-layout'

export default function Login() {
  return (
    <GuestLayout title="Log In">
      <LoginForm />
    </GuestLayout>
  )
}
```

### Example 2: Dashboard Layout with Navigation

```tsx
import { AppHead } from '@/components/app-head'
import { DashboardNav } from '@/components/dashboard-nav'
import { UserMenu } from '@/components/user-menu'
import { usePage } from '@inertiajs/react'
import type { PropsWithChildren } from 'react'
import { useTranslation } from 'react-i18next'

interface DashboardLayoutProps {
  title?: string
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
}

export function DashboardLayout({
  title,
  maxWidth = 'xl',
  children,
}: PropsWithChildren<DashboardLayoutProps>) {
  const { user } = usePage().props
  const { t } = useTranslation()

  const maxWidthClasses = {
    sm: 'max-w-screen-sm',
    md: 'max-w-screen-md',
    lg: 'max-w-screen-lg',
    xl: 'max-w-screen-xl',
    full: 'max-w-full',
  }

  return (
    <>
      <AppHead title={title} />

      <div className="min-h-screen bg-gray-100">
        <header className="border-b bg-white shadow-sm">
          <div className="mx-auto max-w-screen-xl px-4 py-4">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold">{t('dashboard')}</h1>
              <UserMenu user={user} />
            </div>
          </div>
        </header>

        <div className="py-6">
          <div className={cn('mx-auto px-4', maxWidthClasses[maxWidth])}>
            <DashboardNav />

            <main className="mt-6">{children}</main>
          </div>
        </div>
      </div>
    </>
  )
}
```

### Example 3: Admin Layout with Breadcrumbs

```tsx
import { AppHead } from '@/components/app-head'
import { AdminSidebar } from '@/components/admin-sidebar'
import { Breadcrumbs } from '@/components/breadcrumbs'
import type { PropsWithChildren } from 'react'

interface AdminLayoutProps {
  title?: string
  breadcrumbs?: Array<{ label: string; href?: string }>
}

export function AdminLayout({
  title,
  breadcrumbs,
  children,
}: PropsWithChildren<AdminLayoutProps>) {
  return (
    <>
      <AppHead title={title} />

      <div className="flex min-h-screen">
        <AdminSidebar />

        <div className="flex-1">
          <header className="border-b bg-white px-6 py-4">
            {breadcrumbs && <Breadcrumbs items={breadcrumbs} />}
            {title && <h1 className="mt-2 text-2xl font-bold">{title}</h1>}
          </header>

          <main className="p-6">{children}</main>
        </div>
      </div>
    </>
  )
}
```

## Anti-Patterns

### ❌ Don't Do This

```tsx
// Don't use arrow functions assigned to const
export const MainLayout = ({ children }: PropsWithChildren) => {
  // ❌ Use function declaration
  return <div>{children}</div>
}

// Don't forget AppHead
export function Layout({ children }: PropsWithChildren) {
  return <div>{children}</div> // ❌ Missing AppHead
}

// Don't skip PropsWithChildren
export function Layout({ title, children }: { title: string }) {
  // ❌ Should use PropsWithChildren<{ title: string }>
}

// Don't hardcode page-specific content
export function Layout({ children }: PropsWithChildren) {
  return (
    <div>
      <h1>Dashboard</h1> {/* ❌ Too specific */}
      {children}
    </div>
  )
}

// Don't hardcode user-facing text
export function Layout({ children }: PropsWithChildren) {
  return (
    <div>
      <h1>Welcome</h1> {/* ❌ Use t('welcome') */}
      {children}
    </div>
  )
}

// Don't use default exports for layouts
export default function AuthenticatedLayout() {} // ❌ Use named export

// Don't render layouts inside pages
export default function Dashboard() {
  return (
    <AuthenticatedLayout>
      {' '}
      {/* ❌ Should wrap in layout */}
      <Content />
    </AuthenticatedLayout>
  )
}
```

### ✅ Do This Instead

```tsx
// Always include AppHead
export function Layout({
  title,
  children,
}: PropsWithChildren<{ title?: string }>) {
  return (
    <>
      <AppHead title={title} />
      <div>{children}</div>
    </>
  )
}

// Use PropsWithChildren
export function Layout({
  title,
  children,
}: PropsWithChildren<{ title: string }>) {}

// Keep layouts generic
export function Layout({
  title,
  children,
}: PropsWithChildren<{ title?: string }>) {
  return (
    <div>
      {title && <h1>{title}</h1>}
      {children}
    </div>
  )
}

// Use translations for user-facing text
export function Layout({ children }: PropsWithChildren) {
  const { t } = useTranslation()
  return (
    <div>
      <h1>{t('welcome')}</h1>
      {children}
    </div>
  )
}

// Use named exports
export function AuthenticatedLayout() {}

// Wrap pages in layouts at the page level
export default function Dashboard() {
  return (
    <AuthenticatedLayout title="Dashboard">
      <Content />
    </AuthenticatedLayout>
  )
}
```

## Using Layouts in Pages

Import and wrap page content:

```tsx
import { AuthenticatedLayout } from '@/layouts/authenticated-layout'

export default function Dashboard() {
  return (
    <AuthenticatedLayout title="Dashboard">
      <h2>Welcome to your dashboard</h2>
      <DashboardContent />
    </AuthenticatedLayout>
  )
}
```

## Quality Standards

- All layouts must include `AppHead`
- Use `PropsWithChildren<Props>` for TypeScript
- Accept optional `title` prop
- **Use `useTranslation()` for all user-facing text in layouts**
- Use semantic HTML elements
- Keep layouts focused and reusable
- Don't include page-specific logic in layouts
- Ensure responsive design (mobile-first)
- Test layouts with Pest browser tests
