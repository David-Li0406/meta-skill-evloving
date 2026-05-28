# next-intl Setup Guide

Step-by-step installation and configuration of next-intl for Next.js 15 App Router.

## Installation

```bash
npm install next-intl
```

## File Structure

```
project-root/
├── i18n.ts                    # i18n configuration
├── middleware.ts              # Locale routing middleware
├── messages/                  # Translation files
│   ├── en.json
│   ├── es.json
│   ├── fr.json
│   └── de.json
└── app/
    └── [locale]/              # Locale-aware routes
        ├── layout.tsx         # Root layout with provider
        ├── page.tsx           # Landing page
        ├── (auth)/
        └── (dashboard)/
```

## Step 1: Create i18n Configuration

**File**: `i18n.ts` (project root)

```typescript
import { getRequestConfig } from 'next-intl/server';

export default getRequestConfig(async ({ locale }) => ({
  messages: (await import(`./messages/${locale}.json`)).default
}));
```

## Step 2: Configure Middleware

**File**: `middleware.ts` (update existing)

```typescript
import createMiddleware from 'next-intl/middleware';
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient, type CookieOptions } from '@supabase/ssr';

// Create i18n middleware
const intlMiddleware = createMiddleware({
  locales: ['en', 'es', 'fr', 'de'],
  defaultLocale: 'en',
  localePrefix: 'always' // Always show locale in URL
});

export async function middleware(request: NextRequest) {
  // Run i18n middleware
  let response = intlMiddleware(request);

  // Merge with Supabase auth middleware
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value;
        },
        set(name: string, value: string, options: CookieOptions) {
          response.cookies.set({ name, value, ...options });
        },
        remove(name: string, options: CookieOptions) {
          response.cookies.delete({ name, ...options });
        },
      },
    }
  );

  await supabase.auth.getUser();

  return response;
}

export const config = {
  matcher: ['/((?!api|_next|_vercel|.*\\..*).*)']
};
```

## Step 3: Update Root Layout

**File**: `app/[locale]/layout.tsx`

```typescript
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { notFound } from 'next/navigation';

const locales = ['en', 'es', 'fr', 'de'];

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  // Validate locale
  if (!locales.includes(locale)) {
    notFound();
  }

  // Load messages
  const messages = await getMessages();

  return (
    <html lang={locale}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

## Step 4: Create Translation Files

**File**: `messages/en.json`

```json
{
  "common": {
    "appName": "Lucid",
    "actions": {
      "save": "Save",
      "cancel": "Cancel"
    }
  }
}
```

**File**: `messages/es.json`

```json
{
  "common": {
    "appName": "Lucid",
    "actions": {
      "save": "Guardar",
      "cancel": "Cancelar"
    }
  }
}
```

## Step 5: Use in Components

**Server Component**:

```tsx
import { useTranslations } from 'next-intl';

export default function HomePage() {
  const t = useTranslations('common');

  return (
    <div>
      <h1>{t('appName')}</h1>
      <button>{t('actions.save')}</button>
    </div>
  );
}
```

**Client Component**:

```tsx
'use client';

import { useTranslations } from 'next-intl';

export function Dialog() {
  const t = useTranslations('common');

  return <button>{t('actions.cancel')}</button>;
}
```

## Step 6: Add Locale Switcher

```tsx
'use client';

import { useRouter, usePathname } from 'next/navigation';
import { useLocale } from 'next-intl';

export function LocaleSwitcher() {
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();

  const switchLocale = (newLocale: string) => {
    // Replace current locale in pathname
    const newPath = pathname.replace(`/${locale}`, `/${newLocale}`);
    router.push(newPath);
  };

  return (
    <select value={locale} onChange={(e) => switchLocale(e.target.value)}>
      <option value="en">English</option>
      <option value="es">Español</option>
      <option value="fr">Français</option>
      <option value="de">Deutsch</option>
    </select>
  );
}
```

## Step 7: Update Links

```tsx
import { Link } from 'next-intl';

// Automatically includes locale prefix
<Link href="/dashboard">Dashboard</Link>
// Renders: /en/dashboard (or /es/dashboard, etc.)
```

## Step 8: Update Navigation

```tsx
import { useRouter } from 'next/navigation';
import { useLocale } from 'next-intl';

function Component() {
  const router = useRouter();
  const locale = useLocale();

  const navigateToVault = () => {
    router.push(`/${locale}/dashboard/vault`);
  };
}
```

## Testing Setup

```bash
# Test English
curl http://localhost:3000/en

# Test Spanish
curl http://localhost:3000/es

# Default redirects to English
curl http://localhost:3000
# Redirects to /en
```

## TypeScript Support

```typescript
// Type-safe translations
import { useTranslations } from 'next-intl';

// Infer types from en.json
type Messages = typeof import('../messages/en.json');

declare global {
  interface IntlMessages extends Messages {}
}
```

## Production Build

```bash
# Generate static params for all locales
npm run build

# Verifies:
# - All translation files exist
# - No missing keys
# - Static generation works
```

---

**For more information:**
- [Locale Structure](locale-structure.md)
- [next-intl Documentation](https://next-intl-docs.vercel.app/)
