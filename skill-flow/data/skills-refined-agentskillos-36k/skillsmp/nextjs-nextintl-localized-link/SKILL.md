---
name: nextjs-nextintl-localized-link
description: |
  Fix broken locale routing in Next.js apps using next-intl. Use when: (1) Links
  navigate without locale prefix (e.g., /dashboard instead of /en/dashboard), (2)
  Language preference lost on navigation, (3) 404 errors due to missing locale in URL,
  (4) Setting up new Next.js project with next-intl. Solves import of Link component
  from wrong module - must use @/i18n/routing instead of next/link.
author: Claude Code
version: 1.0.0
date: 2026-01-22
---

# Next.js next-intl Localized Link Component

## Problem

When using next-intl for internationalization in Next.js, importing `Link` from
`next/link` breaks locale routing. Links will navigate without the locale prefix,
causing 404 errors or loss of language preference.

**Example issue**:
- Expected URL: `/en/admin/instructors/123`
- Actual URL: `/admin/instructors/123` (missing locale prefix → 404)

## Context / Trigger Conditions

Use the localized Link when:

1. **next-intl is configured** with `localePrefix: "always"` or `"as-needed"`
2. **Navigation breaks locale routing**: Links work but URL loses locale prefix
3. **404 errors** on navigation despite routes existing
4. **Language preference resets** when clicking internal links
5. **Setting up new components** in a next-intl project

## Solution

### Step 1: Import from Localized Routing Module

**❌ WRONG** (standard Next.js Link):
```typescript
import Link from "next/link";
```

**✅ CORRECT** (localized Link):
```typescript
import { Link } from "@/i18n/routing";
```

### Step 2: Use the Localized Link in Components

The API is identical to Next.js Link, but it automatically includes locale:

```typescript
import { Link } from "@/i18n/routing";

export function MyComponent() {
  return (
    <Link href="/admin/instructors">
      View Instructors
    </Link>
  );
}
```

**What happens**:
- In English locale: Renders `/en/admin/instructors`
- In Urdu locale: Renders `/ur/admin/instructors`
- Locale is automatically prepended based on current user's language

### Step 3: Configure Routing Module (First-Time Setup)

If `@/i18n/routing` doesn't exist, create it:

**File**: `src/i18n/routing.ts`

```typescript
import { createNavigation } from 'next-intl/navigation';

// Define your routing configuration
export const routing = {
  locales: ['en', 'ur', 'ar', 'so'],  // Your supported locales
  defaultLocale: 'en',
  localePrefix: 'always' as const  // Always include locale prefix
};

// Create navigation utilities
export const { Link, redirect, usePathname, useRouter } =
  createNavigation(routing);
```

### Step 4: Update All Components

Search and replace across your codebase:

```bash
# Find components using wrong import
grep -r "import Link from \"next/link\"" apps/web/components/

# Update each file to use localized Link
```

## Verification

After using the localized Link:
- ✅ URLs include locale prefix (e.g., `/en/dashboard`)
- ✅ Language preference preserved on navigation
- ✅ No 404 errors on internal links
- ✅ Locale switching works correctly

## Example: Real-World Fix

**Before** (broken locale routing):
```typescript
import Link from "next/link";  // ❌ Wrong import

export function InstructorReviewCard({ instructor }: Props) {
  return (
    <Link href={`/admin/instructors/${instructor.id}`}>
      View Details
    </Link>
  );
}
```

**Issue**: Link navigates to `/admin/instructors/123` without locale prefix → 404

**After** (correct locale routing):
```typescript
import { Link } from "@/i18n/routing";  // ✅ Correct import

export function InstructorReviewCard({ instructor }: Props) {
  return (
    <Link href={`/admin/instructors/${instructor.id}`}>
      View Details
    </Link>
  );
}
```

**Result**: Link navigates to `/en/admin/instructors/123` (or `/ur/...` based on locale)

## Other Localized Navigation APIs

The `createNavigation` function provides more than just `Link`:

```typescript
import { Link, redirect, usePathname, useRouter } from "@/i18n/routing";

// Localized Link component
<Link href="/dashboard">Dashboard</Link>

// Localized redirect (in Server Components)
redirect('/login');  // Automatically includes locale

// Localized pathname (in Client Components)
const pathname = usePathname();  // Returns path without locale prefix

// Localized router (in Client Components)
const router = useRouter();
router.push('/settings');  // Automatically includes locale
```

## Common Pitfalls

### 1. Mixing Imports
```typescript
// ❌ BAD: Mixing standard and localized imports
import Link from "next/link";
import { useRouter } from "@/i18n/routing";
```

**Fix**: Use all navigation APIs from `@/i18n/routing`

### 2. External Links
```typescript
// For external links, standard Link or <a> is fine
<a href="https://example.com">External Link</a>
```

Localized Link is only needed for **internal navigation**.

### 3. API Routes
```typescript
// API routes don't need localized navigation
fetch('/api/data')  // ✅ Correct
```

## Configuration Options

### localePrefix Strategies

```typescript
// Always include locale prefix (recommended for consistency)
localePrefix: 'always'
// URLs: /en/dashboard, /ur/dashboard

// Omit prefix for default locale
localePrefix: 'as-needed'
// URLs: /dashboard (en), /ur/dashboard (ur)
```

### Pathname Localization (Advanced)

```typescript
export const routing = {
  locales: ['en', 'de'],
  defaultLocale: 'en',
  pathnames: {
    '/': '/',
    '/about': {
      en: '/about',
      de: '/uber-uns'  // Localized pathname
    }
  }
};
```

With pathname localization:
- English: `<Link href="/about">` → `/en/about`
- German: `<Link href="/about">` → `/de/uber-uns`

## Notes

- **Type Safety**: Localized Link is fully typed with TypeScript
- **Performance**: No runtime overhead - just wraps Next.js Link with locale logic
- **Server Components**: Works in both Server and Client Components
- **Backward Compatible**: Same API as Next.js Link (href, prefetch, etc.)
- **Automatic Locale Detection**: Uses locale from URL, cookies, or headers

## References

- [next-intl Routing Documentation](https://next-intl.dev/docs/routing)
- [next-intl Navigation APIs](https://next-intl.dev/docs/routing/navigation)
- [next-intl Routing Configuration](https://next-intl.dev/docs/routing/configuration)
- [Next.js App Router Localization with next-intl Tutorial](https://phrase.com/blog/posts/next-js-app-router-localization-next-intl/)
- [next-intl Setup Guide](https://next-intl.dev/docs/routing/setup)
