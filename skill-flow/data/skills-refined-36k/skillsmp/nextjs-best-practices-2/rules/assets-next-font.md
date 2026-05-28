---
title: Use next/font for Zero Layout Shift
impact: MEDIUM
impactDescription: Eliminates font loading flash (FOUT) and improves CLS
tags: fonts, optimization, cls, performance
---

## Use next/font for Zero Layout Shift

next/font automatically self-hosts fonts and eliminates layout shift. External font loading causes visible text flashing.

**Incorrect (external fonts):**

```typescript
// app/layout.tsx
// ❌ External CSS - causes layout shift
<link
  href="https://fonts.googleapis.com/css2?family=Inter"
  rel="stylesheet"
/>

// ❌ Multiple network requests
// ❌ Flash of unstyled text (FOUT)
// ❌ Privacy concerns (Google tracking)
```

**Correct (next/font):**

```typescript
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}
```

**With Tailwind CSS:**

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
      },
    },
  },
}

// Usage in components
<p className="font-sans">Uses Inter font</p>
```

**Local fonts:**

```typescript
import localFont from 'next/font/local'

const customFont = localFont({
  src: [
    {
      path: './fonts/CustomFont-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: './fonts/CustomFont-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  variable: '--font-custom',
})
```

**Preload critical fonts:**

```typescript
// Subset for faster loading
const inter = Inter({
  subsets: ['latin'],
  // Only include characters you need
  display: 'swap',
  preload: true, // Default true for subsets
})
```

Reference: [next/font](https://nextjs.org/docs/app/api-reference/components/font)
