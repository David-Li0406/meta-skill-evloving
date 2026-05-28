---
name: i18n-best-practices
description: Guide for internationalization with next-intl. Use when adding links, translations, or localized URLs. Always use Link from @i18n/routing.
---

# Internationalization (i18n) Best Practices Skill

## Purpose

Enforce correct i18n patterns using `next-intl` to prevent broken navigation and SEO issues.

## ⚠️ CRITICAL: Always Use Link from @i18n/routing

**For ALL internal navigation, use `Link` from `@i18n/routing`, NOT `next/link`.**

ESLint will warn on `next/link` imports in components.

### Why This Matters

Using `next/link` directly loses the locale prefix on navigation:

- User on `/es/barcelona` clicks link
- With `next/link`: Goes to `/barcelona` (loses Spanish locale)
- With `@i18n/routing Link`: Goes to `/es/barcelona` (correct)

### Correct Pattern

```tsx
// ✅ CORRECT - Always use this
import { Link } from "@i18n/routing";

export function MyComponent() {
  return <Link href="/barcelona">Barcelona</Link>;
}
```

### Wrong Pattern

```tsx
// ❌ WRONG - Loses locale on navigation
import Link from "next/link";

export function MyComponent() {
  return <Link href="/barcelona">Barcelona</Link>;
}
```

### Exceptions (Rare)

- Primitives with manual locale handling
- External-only links (use `<a>` tag)

## Project i18n Setup

| Aspect          | Configuration                            |
| --------------- | ---------------------------------------- |
| Library         | `next-intl` ^4.6.1                       |
| Locales         | `ca` (default), `es`, `en`               |
| Prefix Strategy | `as-needed` (no prefix for default `ca`) |
| Routing Config  | `i18n/routing.ts`                        |
| Messages        | `messages/{locale}.json`                 |

## Navigation Exports from @i18n/routing

```typescript
import {
  Link, // Use for all internal links
  redirect, // Server-side redirects
  usePathname, // Get current path (client)
  useRouter, // Programmatic navigation (client)
  getPathname, // Build localized paths
} from "@i18n/routing";
```

## Server vs Client Components

### Server Components

```typescript
import { getTranslations, getLocale } from "next-intl/server";

export default async function ServerComponent() {
  const locale = await getLocale();
  const t = await getTranslations("common");

  return <h1>{t("title")}</h1>;
}
```

### Client Components

```typescript
"use client";
import { useTranslations, useLocale } from "next-intl";

export function ClientComponent() {
  const locale = useLocale();
  const t = useTranslations("common");

  return <button>{t("submit")}</button>;
}
```

## JSON-LD URLs Must Be Localized

For structured data (JSON-LD), always use `toLocalizedUrl`:

```typescript
import { toLocalizedUrl } from "@utils/i18n-seo";

// ✅ CORRECT
const url = toLocalizedUrl("/barcelona/avui", locale);
// Returns: "https://example.com/es/barcelona/avui" for Spanish

// ❌ WRONG - Missing locale prefix
const url = `https://example.com/barcelona/avui`;
```

## Breadcrumbs in JSON-LD

Use the tested helper function:

```typescript
import { generateBreadcrumbList } from "@components/partials/seo-meta";

// ✅ CORRECT - Handles locale automatically
const breadcrumbs = generateBreadcrumbList(items, locale);
```

## Adding New Translations

1. Add keys to all locale files in `messages/`:

   - `messages/ca.json`
   - `messages/es.json`
   - `messages/en.json`

2. Prefer reusing existing keys before adding new ones

3. Use namespaced keys:

   ```json
   {
     "common": {
       "submit": "Enviar",
       "cancel": "Cancel·lar"
     },
     "events": {
       "title": "Esdeveniments"
     }
   }
   ```

## Adding a New Locale

1. Update `types/i18n.ts`:

   ```typescript
   export type Locale = "ca" | "es" | "en" | "fr"; // Add new locale
   ```

2. Create `messages/fr.json` with all translations

3. Update `i18n/routing.ts`:

   ```typescript
   export const routing = defineRouting({
     locales: ["ca", "es", "en", "fr"],
     defaultLocale: "ca",
   });
   ```

4. Update loader map in `i18n/request.ts`

## Checklist Before i18n Changes

- [ ] Using `Link` from `@i18n/routing`? (not `next/link`)
- [ ] JSON-LD URLs using `toLocalizedUrl()`?
- [ ] Breadcrumbs using `generateBreadcrumbList()`?
- [ ] New strings added to ALL locale files?
- [ ] Server component using `getTranslations`?
- [ ] Client component using `useTranslations`?

## Files to Reference

- [i18n/routing.ts](i18n/routing.ts) - Routing configuration and exports
- [i18n/request.ts](i18n/request.ts) - Message loading
- [utils/i18n-seo.ts](utils/i18n-seo.ts) - SEO helpers like `toLocalizedUrl`
- [types/i18n.ts](types/i18n.ts) - Locale type definitions
- [messages/\*.json](messages/) - Translation files
