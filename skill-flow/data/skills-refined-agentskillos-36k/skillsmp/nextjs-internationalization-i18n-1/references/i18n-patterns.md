# Next.js Internationalization Patterns

## App Router i18n Setup

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import Negotiator from 'negotiator';
import { match } from '@formatjs/intl-localematcher';

const locales = ['en', 'vi', 'ja'];
const defaultLocale = 'en';

function getLocale(request: NextRequest): string {
  const headers = { 'accept-language': request.headers.get('accept-language') || '' };
  const languages = new Negotiator({ headers }).languages();
  return match(languages, locales, defaultLocale);
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check if locale is in pathname
  const pathnameHasLocale = locales.some(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  );

  if (pathnameHasLocale) return;

  // Redirect to locale path
  const locale = getLocale(request);
  request.nextUrl.pathname = `/${locale}${pathname}`;
  return NextResponse.redirect(request.nextUrl);
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

## Directory Structure

```
app/
├── [locale]/
│   ├── layout.tsx
│   ├── page.tsx
│   └── about/
│       └── page.tsx
└── dictionaries/
    ├── en.json
    ├── vi.json
    └── ja.json
```

## Dictionary Loading

```typescript
// dictionaries.ts
const dictionaries = {
  en: () => import('./dictionaries/en.json').then((m) => m.default),
  vi: () => import('./dictionaries/vi.json').then((m) => m.default),
  ja: () => import('./dictionaries/ja.json').then((m) => m.default),
};

export const getDictionary = async (locale: string) => {
  return dictionaries[locale]?.() ?? dictionaries.en();
};

// app/[locale]/page.tsx
export default async function Page({ params: { locale } }) {
  const dict = await getDictionary(locale);

  return (
    <main>
      <h1>{dict.home.title}</h1>
      <p>{dict.home.description}</p>
    </main>
  );
}
```

## Dictionary File

```json
// dictionaries/en.json
{
  "home": {
    "title": "Welcome",
    "description": "This is the home page"
  },
  "nav": {
    "about": "About",
    "contact": "Contact"
  },
  "common": {
    "loading": "Loading...",
    "error": "Something went wrong"
  }
}
```

## Layout with Locale

```typescript
// app/[locale]/layout.tsx
import { getDictionary } from '../dictionaries';

export async function generateStaticParams() {
  return [{ locale: 'en' }, { locale: 'vi' }, { locale: 'ja' }];
}

export default async function LocaleLayout({
  children,
  params: { locale },
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  const dict = await getDictionary(locale);

  return (
    <html lang={locale} dir={locale === 'ar' ? 'rtl' : 'ltr'}>
      <body>
        <nav>
          <a href={`/${locale}`}>{dict.nav.home}</a>
          <a href={`/${locale}/about`}>{dict.nav.about}</a>
          <LocaleSwitcher locale={locale} />
        </nav>
        {children}
      </body>
    </html>
  );
}
```

## Locale Switcher

```typescript
'use client';

import { usePathname, useRouter } from 'next/navigation';

export function LocaleSwitcher({ locale }: { locale: string }) {
  const pathname = usePathname();
  const router = useRouter();

  const switchLocale = (newLocale: string) => {
    const newPath = pathname.replace(`/${locale}`, `/${newLocale}`);
    router.push(newPath);
  };

  return (
    <select value={locale} onChange={(e) => switchLocale(e.target.value)}>
      <option value="en">English</option>
      <option value="vi">Tiếng Việt</option>
      <option value="ja">日本語</option>
    </select>
  );
}
```

## next-intl Integration

```typescript
// For more advanced i18n, use next-intl
import { useTranslations } from 'next-intl';

export default function HomePage() {
  const t = useTranslations('home');

  return (
    <div>
      <h1>{t('title')}</h1>
      <p>{t('greeting', { name: 'World' })}</p>
      <p>{t('items', { count: 5 })}</p>
    </div>
  );
}
```
