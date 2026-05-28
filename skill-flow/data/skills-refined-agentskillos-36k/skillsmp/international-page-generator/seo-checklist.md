# SEO Checklist for International Pages

## Required Metadata (Every Page)

### 1. Title Tag

```
Online Biology Tutoring for {Country} Students | Cerebrum Academy
```

- Max 60 characters
- Include country name
- Brand at end

### 2. Meta Description

```
Expert biology tutoring for {Exam1}, {Exam2}, {Exam3}. Small group from {Symbol}{Price}/hr.
Online classes in your timezone. Book a free demo class today!
```

- Max 160 characters
- Include pricing
- Include CTA

### 3. Canonical URL

```html
<link rel="canonical" href="https://cerebrumacademy.com/international/{code}/" />
```

- Trailing slash
- HTTPS
- No query params

## Hreflang Implementation

### Layout.tsx Hreflang Tags

```tsx
// src/app/international/layout.tsx

import { Metadata } from 'next'

export const metadata: Metadata = {
  // ... other metadata
}

export default function InternationalLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <head>
        {/* Hreflang tags for all countries */}
        <link
          rel="alternate"
          hreflang="en-US"
          href="https://cerebrumacademy.com/international/us/"
        />
        <link
          rel="alternate"
          hreflang="en-GB"
          href="https://cerebrumacademy.com/international/uk/"
        />
        <link
          rel="alternate"
          hreflang="en-CA"
          href="https://cerebrumacademy.com/international/ca/"
        />
        <link
          rel="alternate"
          hreflang="en-AU"
          href="https://cerebrumacademy.com/international/au/"
        />
        <link
          rel="alternate"
          hreflang="en-SG"
          href="https://cerebrumacademy.com/international/sg/"
        />
        <link
          rel="alternate"
          hreflang="en-AE"
          href="https://cerebrumacademy.com/international/ae/"
        />
        <link
          rel="alternate"
          hreflang="en-IE"
          href="https://cerebrumacademy.com/international/ie/"
        />
        <link
          rel="alternate"
          hreflang="en-HK"
          href="https://cerebrumacademy.com/international/hk/"
        />
        <link
          rel="alternate"
          hreflang="en-NZ"
          href="https://cerebrumacademy.com/international/nz/"
        />
        <link
          rel="alternate"
          hreflang="en-ZA"
          href="https://cerebrumacademy.com/international/za/"
        />
        <link
          rel="alternate"
          hreflang="x-default"
          href="https://cerebrumacademy.com/international/"
        />
      </head>
      {children}
    </>
  )
}
```

## Structured Data (JSON-LD)

### EducationalOrganization Schema

```tsx
// Add to each country page

const structuredData = {
  '@context': 'https://schema.org',
  '@type': 'EducationalOrganization',
  name: 'Cerebrum Biology Academy',
  description: `Expert biology tutoring for ${country.name} students`,
  url: `https://cerebrumacademy.com/international/${country.code}/`,
  logo: 'https://cerebrumacademy.com/logo.png',
  areaServed: {
    '@type': 'Country',
    name: country.name,
  },
  availableLanguage: 'English',
  hasOfferCatalog: {
    '@type': 'OfferCatalog',
    name: 'Biology Tutoring Services',
    itemListElement: [
      {
        '@type': 'Offer',
        name: 'Small Group Tutoring',
        price: country.pricing.smallGroup,
        priceCurrency: country.currency.code,
      },
      {
        '@type': 'Offer',
        name: 'One-on-One Tutoring',
        price: country.pricing.oneOnOneMin,
        priceCurrency: country.currency.code,
      },
    ],
  },
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: '4.9',
    reviewCount: '500',
  },
}
```

### Course Schema (Per Course Page)

```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "AP Biology Tutoring",
  "description": "Comprehensive AP Biology preparation with expert tutors",
  "provider": {
    "@type": "EducationalOrganization",
    "name": "Cerebrum Biology Academy"
  },
  "hasCourseInstance": {
    "@type": "CourseInstance",
    "courseMode": "online",
    "courseSchedule": {
      "@type": "Schedule",
      "repeatFrequency": "P1W"
    }
  }
}
```

## Open Graph Tags

```tsx
openGraph: {
  title: `Biology Tutoring for ${country.name} Students`,
  description: `Expert ${country.examSystems[0]} tutoring. From ${country.currency.symbol}${country.pricing.smallGroup}/hr.`,
  url: `https://cerebrumacademy.com/international/${country.code}/`,
  siteName: 'Cerebrum Biology Academy',
  locale: country.hreflang.replace('-', '_'), // e.g., 'en_US'
  type: 'website',
  images: [
    {
      url: `https://cerebrumacademy.com/og/international-${country.code}.jpg`,
      width: 1200,
      height: 630,
      alt: `Biology tutoring for ${country.name} students`,
    },
  ],
}
```

## Twitter Card Tags

```tsx
twitter: {
  card: 'summary_large_image',
  title: `Biology Tutoring for ${country.name} Students`,
  description: `Expert tutoring for ${country.examSystems.slice(0,2).join(' & ')}`,
  images: [`https://cerebrumacademy.com/og/international-${country.code}.jpg`],
}
```

## Keywords Strategy

### Primary Keywords (Per Country)

| Country | Primary Keywords                                                                       |
| ------- | -------------------------------------------------------------------------------------- |
| US      | "AP Biology tutor online", "MCAT biology prep", "biology tutor USA"                    |
| UK      | "GCSE Biology tutor", "A-Level Biology tutoring", "biology tutor UK"                   |
| CA      | "biology tutor Canada", "MCAT prep Canada", "online biology tutoring Canada"           |
| AU      | "HSC Biology tutor", "VCE Biology tutoring", "biology tutor Australia"                 |
| SG      | "biology tutor Singapore", "O-Level Biology tutoring", "A-Level Biology Singapore"     |
| AE      | "biology tutor Dubai", "IGCSE Biology UAE", "IB Biology tutor Dubai"                   |
| IE      | "Leaving Cert Biology tutor", "biology grinds Ireland", "online biology tutor Ireland" |
| HK      | "HKDSE Biology tutor", "biology tutor Hong Kong", "A-Level Biology HK"                 |
| NZ      | "NCEA Biology tutor", "biology tutor New Zealand", "online biology tutoring NZ"        |
| ZA      | "NSC Biology tutor", "IEB Biology tutoring", "biology tutor South Africa"              |

## XML Sitemap Entry

```xml
<url>
  <loc>https://cerebrumacademy.com/international/us/</loc>
  <lastmod>2025-01-06</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>
```

## Robots.txt

```
User-agent: *
Allow: /international/

Sitemap: https://cerebrumacademy.com/sitemap-international.xml
```

## Page Speed Checklist

- [ ] Images optimized (WebP, lazy loading)
- [ ] CSS above-fold inlined
- [ ] JS deferred/async
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] TTFB < 600ms

## Content Uniqueness

Each page must have 60%+ unique content:

- [ ] Country-specific headline
- [ ] Country-specific exam systems
- [ ] Local currency pricing
- [ ] Timezone mention
- [ ] Country-specific testimonials (or regional)
- [ ] Country-specific FAQ
- [ ] Local trust signals
