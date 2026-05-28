# Documentation Site Generation Instructions

Detailed instructions for generating Level 3 documentation site content.

## Implementation Steps

### Step 1: Determine Framework

Based on `--framework` parameter or config:

- `rspress` - RSPress 2.x (default for this project)
- `docusaurus` - Docusaurus 2.x
- `vitepress` - VitePress

Load framework-specific template and features.

### Step 2: Create Landing Page

**File:** `index.mdx` or `index.md`

**RSPress example:**

```mdx
---
pageType: home
hero:
  name: {Module Name}
  text: {One-line description}
  tagline: {Tagline from design docs}
  actions:
    - theme: brand
      text: Get Started
      link: /guides/getting-started
    - theme: alt
      text: View on GitHub
      link: {GitHub URL}
features:
  - title: {Feature 1}
    details: {Description}
  - title: {Feature 2}
    details: {Description}
  - title: {Feature 3}
    details: {Description}
---
```

**Content extraction:**

- Hero name from package name
- Tagline from design doc overview
- Features from design doc capabilities
- Actions to getting started and GitHub

### Step 3: Generate Getting Started

**File:** `guides/getting-started.mdx`

**Structure:**

1. **Installation** - Detailed installation steps
2. **Your First Example** - Step-by-step first use
3. **Understanding the Basics** - Key concepts
4. **Common Patterns** - Typical usage
5. **Next Steps** - Links to guides

**Use framework features:**

````mdx
:::tip
Quick tip for new users
:::

:::tabs
== npm
```bash
npm install package-name
```

== pnpm

```bash
pnpm add package-name
```

:::

````

### Step 4: Generate Concept Documentation

Transform architecture design docs:

**From design doc section:**

> ## Architecture
>
> The system uses Effect-TS layers for dependency injection...

**To concept doc (`concepts/architecture.mdx`):**

```mdx
---
title: Architecture Overview
description: Understand how the package is organized
---

# Architecture Overview

The package is organized into three main components that work
together seamlessly.

## Components

### Package Fetcher

Downloads type definitions from npm.

### Cache Manager

Stores definitions for fast repeated access.

### Type Registry

Coordinates fetching and caching automatically.

:::note
You don't need to configure these components individually - they
work together automatically when you use the registry.
:::
```

### Step 5: Generate How-To Guides

Create task-oriented guides:

**Example: `guides/caching.mdx`**

````mdx
---
title: How to Use Caching
description: Configure and use the caching system
---

# How to Use Caching

Learn how to configure caching for your use case.

## Configure Cache Location

```typescript
const registry = createRegistry({
  cacheDir: '~/.my-app/cache'
});
```

## Set Cache Duration

```typescript
const registry = createRegistry({
  cacheTTL: 3600 // 1 hour
});
```

:::warning
Setting TTL too low will cause frequent re-fetching.
Setting it too high may result in stale types.
:::

## Clear Cache

```typescript
await registry.clearCache();
```

## Next Steps

- [Performance Optimization](./performance)
- [Configuration Reference](./configuration)

````

### Step 6: Create Navigation

**RSPress `_meta.json`:**

```json
[
  {
    "text": "Guide",
    "items": [
      {
        "text": "Getting Started",
        "link": "/guides/getting-started"
      },
      {
        "text": "Caching",
        "link": "/guides/caching"
      }
    ]
  },
  {
    "text": "Concepts",
    "items": [
      {
        "text": "Architecture",
        "link": "/concepts/architecture"
      }
    ]
  }
]
```

### Step 7: Integrate API Documentation

If `--api-docs` provided:

Add API reference section to navigation:

```json
{
  "text": "API Reference",
  "link": "/api/README"
}
```

Link from guides to relevant API methods:

```mdx
See the [`createRegistry` API reference](/api/functions/createRegistry)
for all options.
```

## Framework-Specific Features

### RSPress Features

**Tabs:**

````mdx
:::tabs
== TypeScript

```typescript
const x = 1;
```

== JavaScript

```javascript
const x = 1;
```

:::

````

**Callouts:**

```mdx
:::tip
Helpful tip
:::

:::warning
Warning message
:::

:::danger
Danger message
:::

:::note
Note message
:::
```

**Code Groups:**

````mdx
:::code-group

```typescript [index.ts]
export const foo = 'bar';
```

```json [package.json]
{
  "name": "my-package"
}
```

:::

````

### Docusaurus Features

**Admonitions:**

```mdx
:::note
Note content
:::

:::tip
Tip content
:::

:::info
Info content
:::

:::caution
Caution content
:::

:::danger
Danger content
:::
```

**Tabs:**

```mdx
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="npm" label="npm">
    npm install package
  </TabItem>
  <TabItem value="pnpm" label="pnpm">
    pnpm add package
  </TabItem>
</Tabs>
```

## Content Transformation

### Design Doc Architecture → User Concept

**Design doc:**

> Uses Effect-TS Layer system with three layers: HTTP, Cache,
> Registry. Layers are composed via Layer.provide() for
> dependency injection.

**User concept:**

```mdx
# Architecture

The package has three main parts:

1. **HTTP Layer** - Fetches packages from npm
2. **Cache Layer** - Stores downloaded types
3. **Registry Layer** - Coordinates everything

These layers work together automatically - you don't need to
configure them separately.

:::tip Why This Matters
This architecture means the package is easy to test and extend.
Each layer can be swapped out independently.
:::
```

### Design Doc Pattern → User Guide

**Design doc:**

> VFS generation: pipe(packages, Effect.flatMap(fetchTypes),
> Effect.map(generateVFS))

**User guide:**

````mdx
# Generate Virtual File System

Create a VFS for TypeScript tooling:

```typescript
const vfs = await registry.generateVFS(['zod@3.22.0']);
```

The VFS includes all type definitions and can be used with
TypeScript's language service or Twoslash.

:::tabs
== Single Package

```typescript
const vfs = await registry.generateVFS(['zod@3.22.0']);
```

== Multiple Packages

```typescript
const vfs = await registry.generateVFS([
  'zod@3.22.0',
  'ts-pattern@5.0.0'
]);
```

:::

````

## Quality Standards

Level 3 site docs must meet:

- **Engaging:** Landing page hooks users
- **Progressive:** Getting started builds gradually
- **Interactive:** Uses tabs, callouts, code blocks
- **Visual:** Diagrams and examples
- **Mobile:** Works on mobile devices
- **SEO:** Proper metadata and descriptions
- **Accessibility:** Proper heading structure
