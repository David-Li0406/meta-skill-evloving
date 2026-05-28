---
name: astro
description: Build content-focused websites with Astro. Use when creating .astro files, working with content collections, configuring islands architecture, or deploying to Cloudflare/DigitalOcean.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Astro Skill

Build fast, content-focused websites with Astro's islands architecture and zero-JS-by-default philosophy.

## Philosophy Alignment

Astro aligns perfectly with progressive enhancement principles:

| Principle | Astro Implementation |
|-----------|---------------------|
| HTML-first | Astro outputs static HTML by default |
| Zero JS by default | No client JavaScript unless explicitly requested |
| Progressive enhancement | Add interactivity with `client:*` directives |
| Performance | Automatic optimizations, partial hydration |

## Project Structure

```
src/
├── pages/              # File-based routing
│   ├── index.astro     # → /
│   ├── about.astro     # → /about
│   └── blog/
│       ├── index.astro # → /blog
│       └── [slug].astro # → /blog/:slug
├── components/         # Reusable components
│   ├── Header.astro
│   └── Card.astro
├── layouts/            # Page layouts
│   └── BaseLayout.astro
├── content/            # Content collections
│   └── blog/
│       └── post-1.md
└── styles/             # Global styles
    └── global.css
astro.config.mjs        # Configuration
```

## .astro File Syntax

Astro files have two parts: frontmatter (script) and template (HTML):

```astro
---
// Frontmatter: Runs at build time (server-side only)
import BaseLayout from '../layouts/BaseLayout.astro';
import Card from '../components/Card.astro';

// Props from parent component
const { title, description } = Astro.props;

// Fetch data at build time
const posts = await fetch('https://api.example.com/posts').then(r => r.json());

// Define local variables
const formattedDate = new Date().toLocaleDateString();
---

<!-- Template: Outputs as static HTML -->
<BaseLayout title={title}>
  <main>
    <h1>{title}</h1>
    <p>{description}</p>
    <time datetime={formattedDate}>{formattedDate}</time>

    <ul>
      {posts.map((post) => (
        <li>
          <Card title={post.title} href={`/blog/${post.slug}`} />
        </li>
      ))}
    </ul>
  </main>
</BaseLayout>

<style>
  /* Scoped styles - only apply to this component */
  main {
    max-width: 60ch;
    margin: 0 auto;
  }

  h1 {
    color: var(--color-primary);
  }
</style>
```

## Component Props

```astro
---
// Define prop types with JSDoc
/**
 * @typedef {Object} Props
 * @property {string} title - Card title
 * @property {string} [href] - Optional link URL
 * @property {boolean} [featured=false] - Featured styling
 */

/** @type {Props} */
const { title, href, featured = false } = Astro.props;
---

<article class:list={['card', { featured }]}>
  <h2>{title}</h2>
  {href && <a href={href}>Read more</a>}
  <slot />  <!-- Child content goes here -->
</article>
```

## Content Collections

Type-safe content management for markdown/MDX:

```javascript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    author: z.string().default('Anonymous'),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = {
  blog: blogCollection,
};
```

### Querying Content

```astro
---
import { getCollection, getEntry } from 'astro:content';

// Get all published posts
const posts = await getCollection('blog', ({ data }) => !data.draft);

// Sort by date
const sortedPosts = posts.sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);

// Get single entry
const post = await getEntry('blog', 'my-post-slug');
---
```

## Islands Architecture (Partial Hydration)

Add interactivity only where needed:

```astro
---
import StaticHeader from '../components/Header.astro';
import InteractiveSearch from '../components/Search.jsx';
import LazyCarousel from '../components/Carousel.svelte';
---

<!-- Static: No JavaScript -->
<StaticHeader />

<!-- Hydrate immediately on page load -->
<InteractiveSearch client:load />

<!-- Hydrate when browser is idle -->
<InteractiveSearch client:idle />

<!-- Hydrate when component enters viewport -->
<LazyCarousel client:visible />

<!-- Only hydrate on specific media query -->
<MobileMenu client:media="(max-width: 768px)" />

<!-- Never hydrate (render HTML only) -->
<Chart client:only="react" />
```

### When to Use Each Directive

| Directive | Use Case |
|-----------|----------|
| (none) | Static content, no interactivity needed |
| `client:load` | Critical interactive elements (nav, search) |
| `client:idle` | Non-critical interactive elements |
| `client:visible` | Below-the-fold content (carousels, comments) |
| `client:media` | Device-specific interactivity |

## Layouts

```astro
---
// src/layouts/BaseLayout.astro
const { title, description } = Astro.props;
---

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="description" content={description}/>
  <title>{title}</title>
  <link rel="stylesheet" href="/styles/global.css"/>
</head>
<body>
  <slot />
</body>
</html>
```

## Configuration

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';

// Adapters for deployment
import cloudflare from '@astrojs/cloudflare';
import node from '@astrojs/node';

export default defineConfig({
  // Site URL for canonical links
  site: 'https://example.com',

  // Output mode
  output: 'static', // or 'server' for SSR, 'hybrid' for mixed

  // Adapter for deployment target
  adapter: cloudflare(), // or node({ mode: 'standalone' })

  // Integrations
  integrations: [],

  // Vite configuration
  vite: {
    css: {
      devSourcemap: true,
    },
  },
});
```

## Image Optimization

Astro has built-in image optimization:

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.jpg';
---

<!-- Optimized image with automatic format conversion -->
<Image
  src={heroImage}
  alt="Hero image description"
  width={800}
  height={600}
/>

<!-- Remote images (must specify dimensions) -->
<Image
  src="https://example.com/image.jpg"
  alt="Remote image"
  width={400}
  height={300}
/>

<!-- Picture element for art direction -->
<picture>
  <source
    srcset={heroImage.src}
    media="(min-width: 768px)"
  />
  <Image src={heroImage} alt="Responsive hero" />
</picture>
```

## Deployment

### Cloudflare Pages

```javascript
// astro.config.mjs
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'server', // or 'hybrid'
  adapter: cloudflare(),
});
```

```bash
# Deploy
npx wrangler pages deploy dist
```

### DigitalOcean (Node.js)

```javascript
// astro.config.mjs
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',
  adapter: node({ mode: 'standalone' }),
});
```

```dockerfile
# Dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY dist ./dist
EXPOSE 3000
CMD ["node", "dist/server/entry.mjs"]
```

## View Transitions

Enable smooth page transitions:

```astro
---
// In layout
import { ViewTransitions } from 'astro:transitions';
---

<head>
  <ViewTransitions />
</head>

<!-- Persist elements across navigations -->
<header transition:persist>
  ...
</header>

<!-- Custom transition animation -->
<main transition:animate="slide">
  <slot />
</main>
```

## Using Web Components

Integrate your custom elements:

```astro
---
// Import the custom element definition
import '../components/icon-wc.js';
---

<!-- Use custom element (no hydration needed) -->
<icon-wc name="menu" size="24"></icon-wc>

<!-- Custom element with slots -->
<theme-selector>
  <button slot="trigger">Toggle Theme</button>
</theme-selector>
```

## Checklist

Before deploying:

- [ ] Content collections have schemas defined
- [ ] Images use `astro:assets` for optimization
- [ ] Interactive components use appropriate `client:*` directive
- [ ] Static content has no client directives
- [ ] Layouts include proper meta tags
- [ ] Adapter matches deployment target
- [ ] Build succeeds: `npm run build`
- [ ] Preview works: `npm run preview`

## Related Skills

- **xhtml-author** - HTML patterns used in Astro templates
- **css-author** - CSS patterns for scoped and global styles
- **javascript-author** - JavaScript patterns for interactive islands
- **deployment** - Cloudflare and DigitalOcean deployment
- **env-config** - Environment variables in Astro
- **performance** - Core Web Vitals optimization
