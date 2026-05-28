---
name: shadcn-ui
description: Build public-facing React pages with ShadCN UI components, Inertia.js, and the Algoma Jobs theme. Use for landing pages, auth pages (login, register, password reset), and all non-admin user interfaces.
allowed-tools: Bash,Read,Write,Edit,Glob,Grep
---

# ShadCN UI - Public Application Frontend

Build professional, accessible React interfaces using ShadCN UI components with the Algoma Jobs design system.

## Scope

This skill covers the **public-facing application**:
- Landing pages
- Authentication pages (login, register, password reset, email verification, 2FA)
- Job seeker interfaces
- Employer interfaces
- Any non-Filament user-facing pages

**NOT for Filament admin panel** - that uses its own theme system.

## Pre-Flight Checklist

1. **Check existing components** in `resources/js/components/ui/`
2. **Review page patterns** in `resources/js/pages/`
3. **Verify theme colors** are applied in `resources/css/app.css`
4. **Use TodoWrite** for multi-page implementations

## Theme System

### CRITICAL: Always Use Theme Variables

**NEVER use hardcoded colors.** Always use CSS variables or Tailwind semantic classes:

```tsx
// ✅ CORRECT - Use semantic classes
<Button className="bg-primary text-primary-foreground" />
<div className="bg-background text-foreground" />
<Card className="bg-card border-border" />

// ❌ WRONG - Hardcoded colors
<Button className="bg-orange-500 text-white" />
<div className="bg-white text-gray-900" />
```

### Color Palette Reference

| Variable | Light Mode | Dark Mode | Usage |
|----------|------------|-----------|-------|
| `primary` | Copper orange | Lighter copper | CTAs, links, focus rings |
| `secondary` | Teal | Teal | Secondary actions |
| `muted` | Light gray | Dark gray | Subtle backgrounds |
| `accent` | Near white | Dark gray | Hover states |
| `destructive` | Red | Teal | Errors, delete actions |
| `background` | White | Dark purple-gray | Page background |
| `foreground` | Dark blue-gray | Light gray | Primary text |

### CSS Variables (resources/css/app.css)

```css
:root {
  --background: oklch(1.0000 0 0);
  --foreground: oklch(0.2101 0.0318 264.6645);
  --card: oklch(1.0000 0 0);
  --card-foreground: oklch(0.2101 0.0318 264.6645);
  --popover: oklch(1.0000 0 0);
  --popover-foreground: oklch(0.2101 0.0318 264.6645);
  --primary: oklch(0.6716 0.1368 48.5130);
  --primary-foreground: oklch(1.0000 0 0);
  --secondary: oklch(0.5360 0.0398 196.0280);
  --secondary-foreground: oklch(1.0000 0 0);
  --muted: oklch(0.9670 0.0029 264.5419);
  --muted-foreground: oklch(0.5510 0.0234 264.3637);
  --accent: oklch(0.9491 0 0);
  --accent-foreground: oklch(0.2101 0.0318 264.6645);
  --destructive: oklch(0.6368 0.2078 25.3313);
  --border: oklch(0.9276 0.0058 264.5313);
  --input: oklch(0.9276 0.0058 264.5313);
  --ring: oklch(0.6716 0.1368 48.5130);
  --radius: 0.625rem;
}

.dark {
  --background: oklch(0.1797 0.0043 308.1928);
  --foreground: oklch(0.8109 0 0);
  --card: oklch(0.1822 0 0);
  --card-foreground: oklch(0.8109 0 0);
  --popover: oklch(0.1797 0.0043 308.1928);
  --popover-foreground: oklch(0.8109 0 0);
  --primary: oklch(0.7214 0.1337 49.9802);
  --primary-foreground: oklch(0.1797 0.0043 308.1928);
  --secondary: oklch(0.5940 0.0443 196.0233);
  --secondary-foreground: oklch(0.1797 0.0043 308.1928);
  --muted: oklch(0.2520 0 0);
  --muted-foreground: oklch(0.6268 0 0);
  --accent: oklch(0.3211 0 0);
  --accent-foreground: oklch(0.8109 0 0);
  --destructive: oklch(0.5940 0.0443 196.0233);
  --border: oklch(0.2520 0 0);
  --input: oklch(0.2520 0 0);
  --ring: oklch(0.7214 0.1337 49.9802);
}
```

## Component Usage

### Available Components

Check `resources/js/components/ui/` for installed components:

```bash
ls resources/js/components/ui/
```

Common components: `button`, `card`, `input`, `label`, `dialog`, `dropdown-menu`, `select`, `checkbox`, `badge`, `alert`, `separator`, `skeleton`, `tooltip`

### Installing New Components

```bash
npx shadcn@latest add [component-name]
```

### Button Variants

```tsx
import { Button } from '@/components/ui/button';

// Primary action (copper orange)
<Button>Submit</Button>

// Secondary action
<Button variant="secondary">Cancel</Button>

// Outline
<Button variant="outline">Learn More</Button>

// Ghost (for nav items)
<Button variant="ghost">Menu Item</Button>

// Destructive
<Button variant="destructive">Delete</Button>

// With icon
<Button>
  <ArrowRight className="mr-2 h-4 w-4" />
  Continue
</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
```

### Form Inputs

```tsx
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input
    id="email"
    type="email"
    placeholder="you@example.com"
    value={data.email}
    onChange={(e) => setData('email', e.target.value)}
  />
  {errors.email && (
    <p className="text-sm text-destructive">{errors.email}</p>
  )}
</div>
```

### Cards

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description text</CardDescription>
  </CardHeader>
  <CardContent>
    {/* Content */}
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

## Page Structure

### Standard Page Template

```tsx
import { Head, Link } from '@inertiajs/react';
import { Button } from '@/components/ui/button';

export default function PageName() {
  return (
    <>
      <Head title="Page Title">
        <meta name="description" content="Page description for SEO" />
      </Head>

      <div className="min-h-screen bg-background">
        {/* Navigation */}
        <header className="border-b border-border">
          <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
            {/* Nav content */}
          </nav>
        </header>

        {/* Main content */}
        <main className="mx-auto max-w-7xl px-6 py-12">
          <h1 className="text-3xl font-bold text-foreground">Page Title</h1>
          {/* Content */}
        </main>

        {/* Footer */}
        <footer className="border-t border-border px-6 py-12">
          {/* Footer content */}
        </footer>
      </div>
    </>
  );
}
```

### Auth Page Template

```tsx
import { Head, Link, useForm } from '@inertiajs/react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export default function Login() {
  const { data, setData, post, processing, errors } = useForm({
    email: '',
    password: '',
  });

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    post(route('login'));
  };

  return (
    <>
      <Head title="Sign In" />

      <div className="flex min-h-screen items-center justify-center bg-background px-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Sign In</CardTitle>
            <CardDescription>Enter your credentials to continue</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={submit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={data.email}
                  onChange={(e) => setData('email', e.target.value)}
                  required
                />
                {errors.email && (
                  <p className="text-sm text-destructive">{errors.email}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  value={data.password}
                  onChange={(e) => setData('password', e.target.value)}
                  required
                />
                {errors.password && (
                  <p className="text-sm text-destructive">{errors.password}</p>
                )}
              </div>

              <Button type="submit" className="w-full" disabled={processing}>
                {processing ? 'Signing in...' : 'Sign In'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </>
  );
}
```

## Inertia.js Patterns

### Forms with useForm

```tsx
import { useForm } from '@inertiajs/react';

const { data, setData, post, processing, errors, reset } = useForm({
  name: '',
  email: '',
});

const submit = (e: React.FormEvent) => {
  e.preventDefault();
  post(route('users.store'), {
    onSuccess: () => reset(),
  });
};
```

### Links with Inertia

```tsx
import { Link } from '@inertiajs/react';

// Basic link
<Link href="/dashboard">Dashboard</Link>

// With Button component
<Button asChild>
  <Link href="/register">Get Started</Link>
</Button>

// Using route helpers
import { login, register, dashboard } from '@/routes';

<Link href={login()}>Sign In</Link>
<Link href={register()}>Register</Link>
```

### Shared Data

```tsx
import { usePage } from '@inertiajs/react';
import { type SharedData } from '@/types';

const { auth } = usePage<SharedData>().props;

{auth.user ? (
  <span>Welcome, {auth.user.name}</span>
) : (
  <Link href={login()}>Sign In</Link>
)}
```

## Dark Mode Support

The application supports both light and dark themes. Use semantic color classes that automatically adapt:

```tsx
// ✅ These adapt automatically
<div className="bg-background text-foreground" />
<div className="bg-card text-card-foreground" />
<div className="bg-muted text-muted-foreground" />
<div className="border-border" />

// For conditional dark mode styles (rarely needed)
<div className="bg-white dark:bg-gray-900" />
```

## Landing Page (Dark Theme)

The landing page uses a separate dark theme defined in `resources/css/landing.css`. For landing page work:

1. Use the `.landing-page` wrapper class
2. Reference `landing.css` for custom styles
3. See `resources/js/pages/welcome.tsx` for patterns

## Icons

Use Lucide React icons (already installed):

```tsx
import { ArrowRight, Check, X, Menu, User } from 'lucide-react';

<ArrowRight className="h-4 w-4" />
<Check className="h-5 w-5 text-primary" />
```

## Accessibility Requirements

- All form inputs must have associated `<Label>` elements
- Use `aria-label` for icon-only buttons
- Ensure sufficient color contrast (theme colors are pre-validated)
- Support keyboard navigation
- Include focus states (handled by ShadCN defaults)

## Important Reminders

- **ALWAYS** use semantic color classes (`bg-primary`, `text-foreground`, etc.)
- **ALWAYS** check existing components before installing new ones
- **NEVER** hardcode colors - use CSS variables
- **NEVER** modify ShadCN component internals - extend via className
- **ENSURE** all pages have proper `<Head>` with title and meta description
- **TEST** both light and dark modes when applicable
- **USE** Inertia's `useForm` for all form submissions

## Reference Files

- Theme: `resources/css/app.css`
- Landing styles: `resources/css/landing.css`
- Components: `resources/js/components/ui/`
- Pages: `resources/js/pages/`
- Types: `resources/js/types/index.d.ts`
