# Common Pitfalls & Solutions for Astro Development

This guide covers the most common mistakes developers encounter when working with Astro, along with practical solutions and prevention strategies.

## Table of Contents

1. [Islands Architecture Pitfalls](#islands-architecture-pitfalls)
2. [Client Directive Mistakes](#client-directive-mistakes)
3. [SSR vs Static Rendering Confusion](#ssr-vs-static-rendering-confusion)
4. [State Management Issues](#state-management-issues)
5. [Performance Pitfalls](#performance-pitfalls)
6. [Build & Deployment Issues](#build--deployment-issues)
7. [TypeScript & Type Safety](#typescript--type-safety)
8. [Styling & Tailwind CSS](#styling--tailwind-css)

## Islands Architecture Pitfalls

### Problem 1: Components Not Interactive

**Symptom**: React/Vue/Svelte components render but don't respond to user interaction.

**Cause**: Missing `client:*` directive. By default, Astro strips all client-side JavaScript.

**Solution**:

```astro
---
import ReactCounter from '@/components/ReactCounter.jsx';
---

<!-- ❌ Wrong: No client directive -->
<ReactCounter />

<!-- ✅ Correct: Add client directive -->
<ReactCounter client:load />

<!-- ✅ Correct: For below-fold content -->
<ReactCounter client:visible />

<!-- ✅ Correct: For non-critical features -->
<ReactCounter client:idle />
```

**Prevention**: Always add a `client:*` directive to interactive components.

### Problem 2: Context API Doesn't Work Across Islands

**Symptom**: React Context providers don't share state between different components.

**Cause**: Each Astro island hydrates in isolation. Context won't bridge between islands.

**Solution**:

```javascript
// ❌ Wrong: Context won't work across islands
// Parent.astro
<ContextProvider>
  <ChildIsland1 client:load />
  <ChildIsland2 client:load />
</ContextProvider>

// ✅ Correct: Use external state management
// store.ts (Zustand example)
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));

// ChildIsland1.jsx
import useStore from './store';

function ChildIsland1() {
  const { count, increment } = useStore();
  return <button onClick={increment}>{count}</button>;
}

// ChildIsland2.jsx
import useStore from './store';

function ChildIsland2() {
  const { count } = useStore();
  return <div>Count: {count}</div>;
}
```

**External Solutions**: Use Zustand, Redux, or MobX for cross-island state sharing.

### Problem 3: Hydration Mismatches

**Symptom**: Error about content differing between server and client render.

**Cause**: Server-rendered content doesn't match client-side initial render.

**Solution**:

```astro
---
// ❌ Wrong: Dynamic content on server
const date = new Date();
---

<!-- ❌ Wrong: Time will differ -->
<div>Current time: {date.toLocaleTimeString()}</div>

<!-- ✅ Correct: Render on client only -->
<div>Current time: <span id="time"></span></div>

<script>
  document.getElementById('time').textContent =
    new Date().toLocaleTimeString();
</script>

<!-- ✅ Correct: Use ClientOnly component -->
---
import { ClientOnly } from '@/components/ClientOnly.astro';
import TimeDisplay from '@/components/TimeDisplay.jsx';
---

<ClientOnly fallback={<div>Loading...</div>}>
  <TimeDisplay client:load />
</ClientOnly>
```

## Client Directive Mistakes

### Problem 1: Overusing `client:load`

**Symptom**: Slow page load, large JavaScript bundles.

**Cause**: Loading all interactive components immediately, even when not needed.

**Solution**:

```astro
---
import Header from '@/components/Header.jsx';
import NewsletterForm from '@/components/NewsletterForm.jsx';
import ImageCarousel from '@/components/ImageCarousel.jsx';
import CommentsSection from '@/components/CommentsSection.jsx';
---

<!-- ✅ Above-fold, critical - load immediately -->
<Header client:load />

<!-- ✅ Below-fold - load when visible -->
<ImageCarousel client:visible />

<!-- ✅ Secondary feature - load when idle -->
<NewsletterForm client:idle />

<!-- ✅ Mobile-only - load conditionally -->
<MobileMenu client:load media="(max-width: 768px)" />

<!-- ❌ Wrong: Everything with client:load -->
<Header client:load />
<ImageCarousel client:load />
<NewsletterForm client:load />
<CommentsSection client:load />
```

**Best Practice**: Use the least aggressive client directive that works.

### Problem 2: Incorrect Media Query Syntax

**Symptom**: Components load on wrong devices or not at all.

**Cause**: Invalid media query syntax.

**Solution**:

```astro
<!-- ❌ Wrong: Missing quotes or invalid syntax -->
<Component client:load media=max-width: 768px />
<Component client:load media="(max-width 768px)" />

<!-- ✅ Correct: Valid CSS media query -->
<Component client:load media="(max-width: 768px)" />
<Component client:load media="(min-width: 1024px)" />
<Component client:load media="(prefers-reduced-motion: reduce)" />
```

## SSR vs Static Rendering Confusion

### Problem 1: Using `document` or `window` on Server

**Symptom**: Build error or runtime error: `document is not defined`.

**Cause**: Accessing browser-only APIs in server-side code.

**Solution**:

```astro
---
// ❌ Wrong: Browser API in component frontmatter
const width = window.innerWidth;
const element = document.getElementById('app');
---

<!-- ✅ Correct: Move to script tag -->
<div id="app"></div>

<script>
  // This runs in the browser
  const width = window.innerWidth;
  const element = document.getElementById('app');
</script>

<!-- ✅ Correct: For framework components, use lifecycle methods -->
---
import ReactComponent from '@/components/ReactComponent.jsx';
---

<ReactComponent client:load />
```

```jsx
// ReactComponent.jsx
import { useEffect, useState } from 'react';

export default function ReactComponent() {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    // This only runs on the client
    setWidth(window.innerWidth);
  }, []);

  return <div>Width: {width}px</div>;
}
```

### Problem 2: Forgetting `export const prerender` for SSR Pages

**Symptom**: Page not rendering dynamically in SSR mode.

**Cause**: Not opting individual pages into SSR when using `output: 'server'` or `'hybrid'`.

**Solution**:

```astro
---
// For static pages (default)
// Nothing needed - pages are static by default in hybrid mode
---

---

// For SSR pages in hybrid mode
export const prerender = false;

// Now this page will render on each request
const data = await fetch('https://api.example.com/data').then(r => r.json());
---

---

// astro.config.mjs
export default defineConfig({
  output: 'hybrid', // or 'server'
});
```

## State Management Issues

### Problem 1: State Lost During Navigation

**Symptom**: Form data or user state resets when navigating between pages.

**Cause**: View transitions replace the entire page, resetting component state.

**Solution**:

```astro
---
// Use View Transitions API to preserve state
import { ViewTransitions } from 'astro:transitions';
---

<html>
  <head>
    <ViewTransitions />
  </head>
  <body>
    <!-- State in islands with transition:persist will be preserved -->
    <div transition:persist="sidebar">
      <Sidebar client:load />
    </div>
  </body>
</html>
```

### Problem 2: Server State Not Refreshing

**Symptom**: Stale data displayed after updates.

**Cause**: Static pages not revalidating server-side data.

**Solution**:

```astro
---
// ❌ Wrong: Static data never refreshes
const posts = await getCollection('blog');
---

// ✅ Correct: Use hybrid rendering for dynamic data
export const prerender = false;

// Revalidate every 60 seconds
export async function GET({ params }) {
  const posts = await getCollection('blog');

  return Response.json(posts, {
    headers: {
      'Cache-Control': 'public, max-age=60, s-maxage=60',
    },
  });
}
```

## Performance Pitfalls

### Problem 1: Large Client-Side Bundles

**Symptom**: Slow page load, large JavaScript files.

**Cause**: Too many components with `client:load` or heavy dependencies.

**Solution**:

```astro
---
// ✅ Use code splitting
const HeavyComponent = lazy(() => import('./HeavyComponent.jsx'));
---

// ✅ Use client:visible for below-fold content
<HeavyComponent client:visible />

// ✅ Use client:idle for non-critical features
<Analytics client:idle />

// ✅ Analyze bundle size
// npm run build -- --analyze
```

### Problem 2: Unoptimized Images

**Symptom**: Slow image loading, layout shifts.

**Cause**: Not using Astro's built-in Image optimization.

**Solution**:

```astro
---
// ❌ Wrong: Using raw img tags
import heroImage from '@/images/hero.jpg';
---
<img src={heroImage.src} alt="Hero" />

<!-- ✅ Correct: Use Image component -->
---
import { Image } from 'astro:assets';
import heroImage from '@/images/hero.jpg';
---

<Image
  src={heroImage}
  alt="Hero section"
  widths={[400, 800, 1200]}
  formats={['avif', 'webp', 'jpg']}
  loading="lazy"
  decoding="async"
/>
```

### Problem 3: CSS Not Purged

**Symptom**: Large CSS files with unused styles.

**Cause**: Tailwind not properly configured or scanning wrong files.

**Solution**:

```javascript
// tailwind.config.js
export default {
  // ✅ Ensure all file types are scanned
  content: [
    "./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}",
  ],

  // ✅ Enable CSS purging in production
  // (automatic in Tailwind v3+)
}
```

## Build & Deployment Issues

### Problem 1: Build Fails with Module Not Found

**Symptom**: Error about missing modules during build.

**Cause**: Monorepo setup or incorrect path resolution.

**Solution**:

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import path from 'node:path';

export default defineConfig({
  vite: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '@/components': path.resolve(__dirname, './src/components'),
        '@/layouts': path.resolve(__dirname, './src/layouts'),
      },
    },
    // ✅ For monorepos
    ssr: {
      noExternal: [
        '@astrojs/vue',
        'astro-component-lib',
      ],
    },
  },
});
```

### Problem 2: Environment Variables Not Working

**Symptom**: `import.meta.env` variables undefined.

**Cause**: Not prefixing with `PUBLIC_` for client-side access.

**Solution**:

```bash
# .env
# ✅ Public - available on client
PUBLIC_API_URL=https://api.example.com
PUBLIC_SITE_URL=https://mysite.com

# ❌ Private - server-only
SECRET_KEY=abc123
DATABASE_URL=postgresql://...
```

```astro
---
// ✅ Public variables work everywhere
const apiUrl = import.meta.env.PUBLIC_API_URL;

// ❌ Private variables only on server
const secret = import.meta.env.SECRET_KEY;
---
```

## TypeScript & Type Safety

### Problem 1: `any` Types in Props

**Symptom**: Loss of type safety, potential runtime errors.

**Cause**: Not defining proper TypeScript interfaces.

**Solution**:

```astro
---
// ❌ Wrong: Using any
export interface Props {
  data: any;
}

// ✅ Correct: Define specific types
export interface Props {
  title: string;
  count: number;
  isActive: boolean;
  tags: string[];
  metadata?: {
    created: Date;
    updated?: Date;
  };
}

const { title, count, isActive, tags, metadata } = Astro.props;
---
```

### Problem 2: Not Using Strict Mode

**Symptom**: Type errors slipping through, lower code quality.

**Cause**: Using relaxed TypeScript configuration.

**Solution**:

```json
// tsconfig.json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    // ✅ Enable strict mode
    "strict": true,

    // ✅ Enable additional checks
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,

    // ✅ Path aliases
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## Styling & Tailwind CSS

### Problem 1: Tailwind v4 Class Name Changes

**Symptom**: Linter warnings or classes not applying.

**Cause**: Using deprecated Tailwind v3 class names.

**Solution**:

```astro
<!-- ❌ Wrong: Tailwind v3 syntax -->
<div class="bg-gradient-to-r flex-shrink-0 aspect-[3/2] grayscale-[30%]">

<!-- ✅ Correct: Tailwind v4 canonical names -->
<div class="bg-linear-to-r shrink-0 aspect-3/2 grayscale-30">
```

**Common v4 Changes**:
- `bg-gradient-to-*` → `bg-linear-to-*`
- `flex-shrink-0` → `shrink-0`
- `aspect-[3/2]` → `aspect-3/2`
- `grayscale-[30%]` → `grayscale-30`

### Problem 2: Styles Not Applying in Production

**Symptom**: Styles work in dev but not in production build.

**Cause**: CSS not imported or Tailwind not processing files.

**Solution**:

```astro
---
// ✅ Import global styles in layout
import '../styles/global.css';
---

<html>
  <head>
    <!-- Global CSS imported -->
  </head>
</html>
```

```css
/* src/styles/global.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
@layer components {
  .btn-primary {
    @apply bg-blue-500 text-white px-4 py-2 rounded;
  }
}
```

## Quick Reference: Common Gotchas

| Problem | Quick Fix |
|---------|-----------|
| Component not interactive | Add `client:load` or other client directive |
| `document is not defined` | Move code to `<script>` tag or use `useEffect` in React |
| Context not working across islands | Use Zustand, Redux, or MobX instead |
| Large bundle size | Use `client:visible` or `client:idle` where possible |
| Images slow to load | Use `<Image />` from `astro:assets` |
| Build fails in monorepo | Add packages to `vite.ssr.noExternal` |
| Env vars undefined | Prefix with `PUBLIC_` for client-side access |
| Types not strict enough | Use `"strict": true` in tsconfig.json |
| Tailwind classes not working | Check for v4 syntax changes |

## Sources

- [Astro Troubleshooting Guide](https://docs.astro.build/en/guides/troubleshooting/)
- [Astro Islands Architecture](https://docs.astro.build/en/concepts/islands/)
- [React Recap with Astro](https://dev.to/ingosteinke/react-recap-years-later-thanks-to-astro-2b4a)
