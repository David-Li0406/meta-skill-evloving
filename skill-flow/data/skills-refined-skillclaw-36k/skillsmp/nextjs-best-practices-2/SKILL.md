---
name: nextjs-best-practices
description: Next.js App Router development standards. Triggers when working with Next.js applications, Server Components, Server Actions, or App Router patterns.
trigger_patterns:
  - next.js
  - nextjs
  - app router
  - server component
  - use server
  - use client
  - app/
  - next/image
  - next/font
auto_load_with:
  - react-best-practices
  - javascript-best-practices
---

# Next.js Best Practices

Comprehensive coding standards for Next.js App Router applications, optimized for AI agents and LLMs.

## Overview

This skill provides 24 rules organized across 8 performance categories:

1. **App Router (app-)** - Server Components, layouts, loading states [CRITICAL]
2. **Data Fetching (fetch-)** - Caching, revalidation, streaming [CRITICAL]
3. **Server Actions (actions-)** - Form handling, mutations, optimistic updates [HIGH]
4. **Rendering (render-)** - SSR vs SSG vs ISR, dynamic vs static [HIGH]
5. **Middleware (middleware-)** - Edge functions, redirects, rewrites [MEDIUM-HIGH]
6. **Asset Optimization (assets-)** - next/image, next/font, placeholders [MEDIUM]
7. **Route Handlers (routes-)** - API endpoints, streaming responses [MEDIUM]
8. **Deployment (deploy-)** - Vercel config, edge runtime, static export [LOW-MEDIUM]

## Usage

Reference this skill when:
- Building new Next.js applications
- Migrating from Pages Router to App Router
- Optimizing Next.js performance
- Implementing Server Components or Server Actions
- Configuring caching and revalidation strategies

## Build

```bash
pnpm build    # Compile rules to AGENTS.md
pnpm validate # Validate rule files
```
