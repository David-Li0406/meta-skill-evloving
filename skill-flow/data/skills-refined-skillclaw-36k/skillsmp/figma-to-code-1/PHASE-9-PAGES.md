# Phase 9: Page Assembly with Global Content

**CRITICAL:** Pages fetch global content and pass to layout components.
All components must pass the correct `entry` prop for inline editing.

> **IMPORTANT:** The examples show PATTERNS.
> Create pages using YOUR components based on YOUR Figma.

## Root Layout Pattern

```typescript
// src/app/layout.tsx
import { getSiteSettings, getNavigation, getFooterContent } from '@/lib/content';
import { Navigation, Footer } from '@/components/layout';

export const dynamic = 'force-dynamic';

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  // Fetch global content
  const siteSettings = await getSiteSettings();
  const navigation = await getNavigation();
  const footer = await getFooterContent();

  return (
    <html lang="en">
      <body>
        <Navigation
          menuLinks={navigation.menuLinks}
          logoUrl={siteSettings.logoUrl}
          logoAlt={siteSettings.logoAlt}
          // Pass props based on YOUR navigation
        />

        <main>{children}</main>

        <Footer
          footerLinks={footer.footerLinks}
          copyrightText={footer.copyrightText}
          // Pass props based on YOUR footer
        />
      </body>
    </html>
  );
}
```

## Page Component Pattern

```typescript
// src/app/page.tsx (or src/app/[slug]/page.tsx)
import { getPageContent } from '@/lib/content';

export const dynamic = 'force-dynamic';

export default async function Page() {
  // Use YOUR page slug
  const pageContent = await getPageContent('[your-page-slug]');
  const { data } = pageContent;

  return (
    <>
      {/* Render YOUR sections with data attributes */}
      <section>
        <h1
          data-cms-entry="[your-page-slug]"
          data-cms-field="hero.title"
        >
          {data.hero.title}
        </h1>
      </section>

      {/* Add sections based on YOUR Figma */}
    </>
  );
}
```

## 404 Page (If in Figma)

```typescript
// src/app/not-found.tsx
// Create ONLY if 404 exists in Figma

import { getPageContent } from '@/lib/content';

export const dynamic = 'force-dynamic';

export default async function NotFound() {
  const content = await getPageContent('404');

  return (
    <div>
      <h1 data-cms-entry="404" data-cms-field="title">
        {content.title}
      </h1>
      <p data-cms-entry="404" data-cms-field="message">
        {content.message}
      </p>
    </div>
  );
}
```

## Build Pages Sequentially

For each page:
1. Create page file in `/src/app/`
2. Import necessary components
3. Fetch content from CMS
4. Render with data attributes
5. Test locally before proceeding

**Get human approval at each page before moving on.**

## Git Commit

```bash
git commit -m "feat: all pages assembled with CMS content"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 9: Pages assembled" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-10-AUDIT.md](PHASE-10-AUDIT.md)
