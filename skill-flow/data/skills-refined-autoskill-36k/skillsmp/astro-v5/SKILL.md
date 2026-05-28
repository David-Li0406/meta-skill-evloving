---
name: astro-v5
description: Astro v5 features, patterns, and best practices for building static sites with dynamic islands. Use when creating pages, components, content collections, or configuring Astro.
allowed-tools: Read, Edit, Write, Bash(npm:*, astro:*)
---

# Astro v5 Features and Patterns

Domain knowledge for working with Astro v5 in this template.

## When to Use

Apply this knowledge when:
- Creating new Astro pages or components
- Working with Content Collections
- Implementing View Transitions
- Optimizing images
- Configuring static vs hybrid rendering
- Debugging Astro-specific issues

## Key Concepts

### Content Collections API

Content Collections provide type-safe content management for blog posts, documentation, etc.

**Define a Collection** (`src/content/config.ts`):

```typescript
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

**Query Collections**:

```astro
---
import { getCollection } from 'astro:content';

// Get all non-draft posts
const posts = await getCollection('blog', ({ data }) => !data.draft);

// Sort by date
const sortedPosts = posts.sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);
---
```

**Render Content**:

```astro
---
import { getEntry, render } from 'astro:content';

const post = await getEntry('blog', 'my-post');
const { Content, headings, remarkPluginFrontmatter } = await render(post);
---

<article>
  <h1>{post.data.title}</h1>
  <Content />
</article>
```

### View Transitions

Enable smooth page transitions without full reloads.

**Enable in Layout** (`src/layouts/BaseLayout.astro`):

```astro
---
import { ViewTransitions } from 'astro:transitions';
---

<html>
  <head>
    <ViewTransitions />
  </head>
  <body>
    <slot />
  </body>
</html>
```

**Named Transitions** (morph elements between pages):

```astro
<!-- Page 1: Blog listing -->
<img
  src={post.heroImage}
  transition:name={`hero-${post.slug}`}
/>

<!-- Page 2: Blog post -->
<img
  src={heroImage}
  transition:name={`hero-${slug}`}
/>
```

**Animation Directives**:

```astro
<div transition:animate="slide">Slides in</div>
<div transition:animate="fade">Fades in</div>
<div transition:animate="none">No animation</div>

<!-- Custom animation -->
<div transition:animate={{
  old: { name: 'fadeOut', duration: '0.2s' },
  new: { name: 'slideIn', duration: '0.3s' }
}}>
  Custom
</div>
```

**Persist State** (keep element state across navigations):

```astro
<video transition:persist id="media-player">
  <source src="/video.mp4" />
</video>
```

### Image Optimization

Astro v5 includes built-in image optimization.

**Basic Usage**:

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.jpg';
---

<Image
  src={heroImage}
  alt="Hero image"
  width={800}
  height={600}
  format="webp"
  quality={80}
/>
```

**Remote Images** (requires configuration):

```javascript
// astro.config.mjs
export default defineConfig({
  image: {
    domains: ['images.unsplash.com'],
    remotePatterns: [{ protocol: 'https' }],
  },
});
```

**Picture Element** (multiple formats):

```astro
---
import { Picture } from 'astro:assets';
import heroImage from '../assets/hero.jpg';
---

<Picture
  src={heroImage}
  formats={['avif', 'webp']}
  alt="Hero"
  widths={[400, 800, 1200]}
  sizes="(max-width: 800px) 100vw, 800px"
/>
```

### Static vs Hybrid Rendering

**Static (Default)** - Pre-rendered at build time:

```javascript
// astro.config.mjs
export default defineConfig({
  output: 'static', // Default
});
```

**Hybrid** - Mix of static and server-rendered:

```javascript
// astro.config.mjs
import node from '@astrojs/node';

export default defineConfig({
  output: 'hybrid',
  adapter: node({ mode: 'standalone' }),
});
```

**Server-render specific pages**:

```astro
---
// src/pages/api/data.ts
export const prerender = false; // Render on each request
---
```

**Force prerender in hybrid mode**:

```astro
---
export const prerender = true; // Always static
---
```

### Component Patterns

**Props with TypeScript**:

```astro
---
interface Props {
  title: string;
  description?: string;
  variant?: 'primary' | 'secondary';
}

const { title, description, variant = 'primary' } = Astro.props;
---

<div class={`card card--${variant}`}>
  <h2>{title}</h2>
  {description && <p>{description}</p>}
</div>
```

**Slots**:

```astro
---
// Card.astro
---
<div class="card">
  <header>
    <slot name="header" />
  </header>
  <main>
    <slot /> <!-- Default slot -->
  </main>
  <footer>
    <slot name="footer">
      <p>Default footer</p>
    </slot>
  </footer>
</div>
```

**Usage**:

```astro
<Card>
  <h2 slot="header">Title</h2>
  <p>Main content</p>
  <!-- footer uses default -->
</Card>
```

### Data Fetching

**Build-time Fetching**:

```astro
---
// Runs at build time only (static output)
const response = await fetch('https://api.example.com/data');
const data = await response.json();
---

<ul>
  {data.items.map(item => <li>{item.name}</li>)}
</ul>
```

**With Error Handling**:

```astro
---
let data;
let error;

try {
  const res = await fetch('https://api.example.com/data');
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  data = await res.json();
} catch (e) {
  error = e.message;
}
---

{error ? (
  <p class="error">Failed to load: {error}</p>
) : (
  <ul>
    {data.items.map(item => <li>{item.name}</li>)}
  </ul>
)}
```

## Project-Specific Patterns

### YAML-Driven Configuration

This template uses YAML for all configuration:

```astro
---
import { loadSiteConfig } from '@utils/config';
const config = await loadSiteConfig();
---

<head>
  <title>{config.site.title}</title>
  <meta name="description" content={config.site.description} />
</head>
```

### DynamicContent Integration

Use with HTMX for serverless content:

```astro
---
import DynamicContent from '@components/DynamicContent.astro';
import { loadSiteConfig } from '@utils/config';

const config = await loadSiteConfig();
const commentsEnabled = config.features?.comments ?? false;
---

{commentsEnabled && (
  <DynamicContent
    endpoint={config.services.remark42.endpoint}
    trigger="revealed"
  />
)}
```

## Common Mistakes

### 1. Importing Client-Side Only Libraries at Top Level

```astro
---
// WRONG: Runs at build time, will fail
import Chart from 'chart.js';
---

<!-- CORRECT: Use client directive -->
<script>
  import Chart from 'chart.js';
  // Initialize chart
</script>
```

### 2. Forgetting Async in Content Collection Queries

```astro
---
// WRONG: Missing await
const posts = getCollection('blog');

// CORRECT
const posts = await getCollection('blog');
---
```

### 3. Using Client State in Astro Components

```astro
---
// WRONG: Astro components don't have client state
let count = 0;
function increment() { count++; } // Won't work
---

<!-- CORRECT: Use a framework component with client directive -->
<Counter client:load />

<!-- OR use vanilla JS -->
<button id="counter">0</button>
<script>
  const btn = document.getElementById('counter');
  let count = 0;
  btn.addEventListener('click', () => {
    count++;
    btn.textContent = count;
  });
</script>
```

### 4. Hardcoding Values Instead of Using Config

```astro
---
// WRONG: Hardcoded
const siteName = "My Site";

// CORRECT: Use YAML config
import { loadSiteConfig } from '@utils/config';
const config = await loadSiteConfig();
const siteName = config.site.title;
---
```

### 5. Not Handling View Transition Events

```javascript
// Listen for navigation events
document.addEventListener('astro:page-load', () => {
  // Re-initialize scripts after navigation
  initializeWidgets();
});

document.addEventListener('astro:after-swap', () => {
  // Runs after DOM swap, before page-load
  // Good for scroll position, focus management
});
```

### 6. Image Optimization in Wrong Directory

```
src/
  assets/       # Optimized at build time
    hero.jpg
  pages/
public/
  images/       # NOT optimized, served as-is
    logo.png
```

## Debugging Tips

### Check Build Output

```bash
npm run build
# Look at dist/ to see generated files
```

### Enable Verbose Logging

```bash
DEBUG=astro:* npm run dev
```

### Inspect Content Collection Types

```bash
# After running dev/build, check generated types
cat .astro/types.d.ts
```

### View Transitions Not Working

1. Ensure `<ViewTransitions />` is in `<head>`
2. Check browser supports View Transitions API
3. Verify same `transition:name` on both pages
4. Check for JavaScript errors blocking transitions

## Related

- Config: `astro.config.mjs`
- Content: `src/content/config.ts`
- Layouts: `src/layouts/BaseLayout.astro`
- Astro Docs: https://docs.astro.build
