# Phase 14: Deployment

**Skip if Deployment Platform = None in config**

## For Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel --prod
```

3. Set environment variables in Vercel dashboard:
   - `NEXT_PUBLIC_CMS_GRAPHQL_URL`
   - `CMS_ORGANIZATION_ID`
   - `CDN_BUCKET_URL`

## For AWS Amplify

1. Create Amplify app in AWS Console

2. Connect to repository

3. Configure build settings:
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

4. Set environment variables in Amplify Console

## For Netlify

1. Install Netlify CLI:
```bash
npm i -g netlify-cli
```

2. Deploy:
```bash
netlify deploy --prod
```

3. Set environment variables in Netlify dashboard

## Inline Editor Script

Add the inline editor script to `src/app/layout.tsx` before the closing `</body>` tag:

Use the `InlineEditorLoader` component to conditionally load the editor when `?edit=true` is in the URL:

```tsx
// src/components/InlineEditorLoader.tsx
'use client';

import { useEffect } from 'react';
import { useSearchParams } from 'next/navigation';

interface InlineEditorLoaderProps {
  orgSlug: string;
  apiBase?: string;
  adminBase?: string;
}

export function InlineEditorLoader({
  orgSlug,
  apiBase = 'https://backend-production-162b.up.railway.app',
  adminBase = 'https://sphereos.vercel.app',
}: InlineEditorLoaderProps) {
  const searchParams = useSearchParams();
  const isEditMode = searchParams.get('edit') === 'true';

  useEffect(() => {
    if (!isEditMode) return;
    if (document.querySelector('script[data-cms-editor]')) return;

    const script = document.createElement('script');
    script.src = `${apiBase}/inline-editor.js`;
    script.dataset.cmsOrg = orgSlug;
    script.dataset.cmsApi = apiBase;
    if (adminBase) script.dataset.cmsAdmin = adminBase;
    script.dataset.cmsEditor = 'true';
    script.defer = true;
    document.head.appendChild(script);
  }, [isEditMode, orgSlug, apiBase, adminBase]);

  return null;
}
```

Then in `layout.tsx`:
```tsx
import { Suspense } from 'react';
import { InlineEditorLoader } from '@/components/InlineEditorLoader';

// In the body:
<Suspense fallback={null}>
  <InlineEditorLoader orgSlug="your-org-slug" />
</Suspense>
```

This enables inline editing for authenticated CMS users when they visit with `?edit=true`.

## Post-Deployment

### Lighthouse Audit

```bash
npx lighthouse https://your-deployed-url.com --output html --output-path ./lighthouse-report.html
```

Targets:
- Performance: > 90
- Accessibility: > 90
- Best Practices: > 90
- SEO: > 90

### Verify Production

- [ ] All pages load correctly
- [ ] CMS content displays
- [ ] Images load from CDN
- [ ] No console errors

## Git Commit

```bash
git commit -m "feat: deployed to [Platform]"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 14: Deployment complete!" with title "Claude Code" sound name "Ping"'
```

---

## BUILD COMPLETE

The website is now:
- ✓ Built from Figma designs
- ✓ All content from CMS
- ✓ Zero hardcoded strings
- ✓ Inline editor ready
- ✓ Production deployed
