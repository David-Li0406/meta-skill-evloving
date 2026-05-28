---
name: create-page
description: Create a new tutorial/content page on agentconfig.org with proper file structure, routing, and registry entry. Use when adding a new top-level page like /skills, /agents, or /mcp.
---

# Create Page

Create a new content page on agentconfig.org following project conventions.

## Overview

This skill creates all the necessary files for a new page:
1. HTML entry point (`site/{slug}/index.html`)
2. Page renderer (`site/src/pages/{slug}.tsx`)
3. Page component (`site/src/components/{Name}Page/`)
4. Data file (`site/src/data/{slug}Tutorial.ts`)
5. Vite config entry
6. Navigation link
7. **Page registry entry** for llms generation

## When to Use

Use this skill when:
- Creating a new tutorial or content page
- Adding a major new section to the site
- The page needs to be included in llms.txt generation

## Step-by-Step Process

### Step 1: Create HTML Entry Point

Create `site/{slug}/index.html`:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{Page Title} - agentconfig.org</title>
    <meta name="description" content="{One-line description}" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/pages/{slug}.tsx"></script>
  </body>
</html>
```

### Step 2: Create Page Renderer

Create `site/src/pages/{slug}.tsx`:

```tsx
import { render } from 'preact'
import { {Name}Page } from '@/components/{Name}Page'
import '@/index.css'

const rootElement = document.getElementById('root')
if (!rootElement) {
  throw new Error('Root element not found')
}

render(<{Name}Page />, rootElement)
```

### Step 3: Create Page Component

Create `site/src/components/{Name}Page/index.ts`:

```typescript
export { {Name}Page } from './{Name}Page'
```

Create `site/src/components/{Name}Page/{Name}Page.tsx`:

```tsx
import type { VNode } from 'preact'
import { PageLayout } from '@/layouts'
import { TableOfContents } from '@/components/TableOfContents'
import { tocItems } from '@/data/{slug}Tutorial'

export function {Name}Page(): VNode {
  return (
    <PageLayout>
      {/* Hero Section */}
      <header className="border-b border-border bg-muted/30">
        <div className="container mx-auto px-4 py-12 md:py-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            {Page Title}
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl">
            {Description}
          </p>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Add page content here */}
      </div>
    </PageLayout>
  )
}
```

### Step 4: Create Data File

Create `site/src/data/{slug}Tutorial.ts`:

```typescript
import type { TocItem } from '@/components/TableOfContents'

export const tocItems: readonly TocItem[] = [
  { id: 'section-1', label: '1. First Section', level: 'beginner' },
  // Add more sections
] as const

export const codeSamples: Record<string, string> = {
  // Add code samples
}

export const furtherReadingLinks: readonly FurtherReadingLink[] = [
  // Add further reading links
] as const
```

### Step 5: Add to Vite Config

Update `site/vite.config.ts` build inputs:

```typescript
build: {
  rollupOptions: {
    input: {
      main: resolve(__dirname, 'index.html'),
      skills: resolve(__dirname, 'skills/index.html'),
      agents: resolve(__dirname, 'agents/index.html'),
      {slug}: resolve(__dirname, '{slug}/index.html'),  // Add this
    },
  },
},
```

### Step 6: Add Navigation Link

Update `site/src/components/Navigation/Navigation.tsx`:

```typescript
const navLinks = [
  { href: '/', label: 'Home' },
  { href: '/skills/', label: 'Skills' },
  { href: '/agents/', label: 'Agents' },
  { href: '/{slug}/', label: '{Label}' },  // Add this
]
```

### Step 7: Add to Page Registry (IMPORTANT!)

Update `site/src/data/pages.ts` to include the new page:

```typescript
export const pages: readonly PageMeta[] = [
  // ... existing pages
  {
    slug: '{slug}',
    title: '{Page Title}',
    description: '{One-line description for llms.txt}',
    features: '{What the md file contains}',
    dataFile: '{slug}Tutorial.ts',
    mdFile: '{slug}.md',
    partNumber: {next number},  // Increment from last page
  },
]
```

### Step 8: Update generate-llms Script

If the page has unique data structure, update `.claude/skills/generate-llms/scripts/generate-llms-full.ts`:

1. Import the new data file in `loadData()`
2. Add a `generate{Name}Md()` function
3. Call it in the `main()` function

### Step 9: Regenerate LLMs Files

After creating the page, regenerate the llms files:

```
Use the generate-llms skill to regenerate all llms files
```

## Checklist

Before considering the page complete:

- [ ] HTML entry point created in `site/{slug}/index.html`
- [ ] Page renderer created in `site/src/pages/{slug}.tsx`
- [ ] Page component created in `site/src/components/{Name}Page/`
- [ ] Data file created in `site/src/data/{slug}Tutorial.ts`
- [ ] Vite config updated with build input
- [ ] Navigation link added
- [ ] **Page registry entry added to `site/src/data/pages.ts`**
- [ ] generate-llms script updated (if needed)
- [ ] LLMs files regenerated

## Example Prompts

### Create a new page
```
Create a new page at /security for security best practices documentation
```

### Add page to registry only
```
Add the /mcp page to the page registry so it's included in llms generation
```
