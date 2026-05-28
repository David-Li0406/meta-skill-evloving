---
name: setup-react-grab
description: Automatically detects React framework (Next.js, Vite, CRA, Remix) and injects react-grab for element selection. Use when setting up react-grab, adding react-grab to a project, or when user mentions react-grab installation or configuration.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Setup React Grab

Automatically inject react-grab into any React codebase with framework-aware configuration.

## Overview

This skill:
1. Detects the React framework (Next.js App Router, Pages Router, Vite, CRA, Remix)
2. Finds the correct entry file to inject react-grab
3. Adds the react-grab script with proper development-only guards
4. Installs the npm package if needed
5. Provides clear next steps for the user

## Step-by-Step Instructions

### Step 1: Detect Project Type

Read `package.json` to identify the framework:
- Look for dependencies: `next`, `vite`, `react-scripts`, `@remix-run/react`
- Check for framework config files: `next.config.js`, `vite.config.js`

### Step 2: Find Entry Files Based on Framework

#### Next.js App Router
- Target: `app/layout.tsx` or `app/layout.jsx`
- Injection point: Inside `<head>` tag
- Code:

```tsx
import Script from 'next/script';

{process.env.NODE_ENV === 'development' && (
  <Script
    src="//unpkg.com/react-grab/dist/index.global.js"
    crossOrigin="anonymous"
    strategy="beforeInteractive"
  />
)}
```

#### Next.js Pages Router
- Target: `pages/_document.tsx` or `pages/_document.jsx`
- Injection point: Inside `<Head>` component
- Code:

```tsx
import { Html, Head, Main, NextScript } from 'next/document';

{process.env.NODE_ENV === 'development' && (
  <script
    src="//unpkg.com/react-grab/dist/index.global.js"
    crossOrigin="anonymous"
  />
)}
```

#### Vite
- Target: `index.html`
- Injection point: Inside `<head>` tag
- Code:

```html
<script type="module">
  if (import.meta.env.DEV) {
    import('react-grab');
  }
</script>
```

Also install:
```bash
npm install react-grab --save-dev
```

#### Create React App / Webpack
- Target: `public/index.html` or `src/index.tsx`
- Injection point: Inside `<head>` tag
- Code:

```html
<script>
  if (process.env.NODE_ENV === 'development') {
    const script = document.createElement('script');
    script.src = '//unpkg.com/react-grab/dist/index.global.js';
    script.crossOrigin = 'anonymous';
    document.head.appendChild(script);
  }
</script>
```

#### Remix
- Target: `app/root.tsx`
- Injection point: Inside `<head>` tag
- Code:

```tsx
{process.env.NODE_ENV === 'development' && (
  <script
    src="//unpkg.com/react-grab/dist/index.global.js"
    crossOrigin="anonymous"
  />
)}
```

### Step 3: Implementation Guidelines

1. ALWAYS read the target file first before making changes
2. Check if react-grab already exists to avoid duplicates
3. Preserve existing code - only add react-grab
4. Maintain proper indentation matching file style
5. Use appropriate syntax (JSX for tsx/jsx, HTML for html)

### Step 4: Package Installation

For CDN-based installations (Next.js, Remix, CRA), package installation is optional.

For Vite or local installation:
```bash
npm install react-grab --save-dev
```

### Step 5: Provide Summary

After setup, report:
- Framework detected
- File modified with line number
- Next steps: restart dev server
- Usage: hover over element, press Cmd+C (Mac) or Ctrl+C (Windows)

Example output:
```
Setup Complete

Detected: Next.js 14 with App Router
Modified: app/layout.tsx (line 12)

Next steps:
1. Restart dev server (npm run dev)
2. Open app in browser
3. Hover over element, press Cmd+C or Ctrl+C
4. Component context copied to clipboard

Example output:
<button class="login-btn">Login</button>
in LoginButton
src/components/auth.tsx:42:6
```

## Error Handling

1. Cannot detect framework: Ask user which framework they use
2. Cannot find entry file: Use Glob to search, list options for user
3. React-grab exists: Inform user, skip installation
4. Multiple entry files: List options, ask user to choose

## Important Notes

- Development only: Always wrap in environment checks
- Non-blocking: Use CDN or async loading
- Security: Use `crossOrigin="anonymous"` for CDN scripts
- No production: Never inject in production builds

## Verification Checklist

- Correct framework detected
- Right file modified
- Development-only guard present
- Syntax correct for file type
- No duplicate code
- User received clear instructions
