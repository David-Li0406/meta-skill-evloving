---
name: url-state-management
description: Use this skill to sync React state to URL query parameters for shareable filters, search queries, and deep-linkable dialogs.
---

# URL State Management

Sync React state to URL query parameters for shareable filters, search queries, and deep-linkable dialogs. This setup preserves UI state on browser back/forward navigation.

## Prerequisites

Complete these recipes first (in order):

### Next.js on Vercel

Create a Next.js app running on Bun, configure the development environment, and deploy to Vercel with automatic deployments on push.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/nextjs-on-vercel
```

## Cookbook - Complete These Recipes in Order

### URL State with nuqs

To set up URL State with nuqs, refer to the fullstackrecipes MCP server resource:

**Resource URI:** `recipe://fullstackrecipes.com/nuqs-setup`

If the MCP server is not configured, fetch the recipe directly:

```bash
curl -H "Accept: text/plain" https://fullstackrecipes.com/api/recipes/nuqs-setup
```

### Working with nuqs

Manage React state in URL query parameters with nuqs. Covers Suspense boundaries, parsers, clearing state, and deep-linkable dialogs.

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/using-nuqs
```