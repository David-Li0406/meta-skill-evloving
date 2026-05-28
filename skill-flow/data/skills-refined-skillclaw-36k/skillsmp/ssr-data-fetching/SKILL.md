---
name: ssr-data-fetching
description: Guide through proper Server-Side Rendering compatible data fetching in Nuxt 4. Use when fetching data in components or implementing data-driven UI.
---

# SSR Data Fetching Implementation Skill

Guides through proper Server-Side Rendering compatible data fetching in Nuxt 4 components.

## Purpose

USE this skill when:
- Fetching data in Vue components
- Adding API calls to pages or components
- Implementing data-driven UI
- Converting client-only fetching to SSR

## Critical Rules

⛔ **ALWAYS use useFetch() or useAsyncData()** - NEVER use raw $fetch() in components
⛔ **ALWAYS await the composable** - Required for proper SSR hydration
⛔ **ALWAYS handle loading and error states** - Provide good UX

## Why SSR Matters

**Benefits:**
- SEO: Search engines see fully rendered content
- Performance: Faster initial page load
- UX: No loading flicker on initial load
- Accessibility: Content available even if JavaScript fails

**Problem with $fetch():**
- Runs only on client (not during SSR)
- Server renders without data → empty HTML
- Client fetches and re-renders → loading flicker
- Search engines see empty page → poor SEO

## Workflow Steps

### Step 1: Identify Data Fetching Need
Determine what data needs to be fetched and choose strategy:
- Simple API call → Use `useFetch()`
- Complex async operation → Use `useAsyncData()`

### Step 2: Implement useFetch() Pattern

```vue
<script setup lang="ts">
import type { Speaker } from "~/server/database/schema"

const { data: speakers, pending, error, refresh } = 
  await useFetch<Speaker[]>("/api/speakers")
</script>

<template>
  <div v-if="pending">Loading...</div>
  <div v-else-if="error">{{ error.message }}</div>
  <div v-else-if="speakers">
    <div v-for="speaker in speakers" :key="speaker.id">
      {{ speaker.firstName }}
    </div>
  </div>
</template>
```

### Step 3: Implement useAsyncData() Pattern (If Needed)

```vue
<script setup lang="ts">
const { data, pending, error } = await useAsyncData(
  "unique-key",
  () => $fetch("/api/endpoint", {
    headers: { "X-Custom-Header": "value" }
  })
)
</script>
```

### Step 4: Verify SSR Hydration
- Check `await` keyword present
- Verify all states destructured (data, pending, error)
- Ensure template handles all states

### Step 5: Test SSR Behavior
- No loading spinner on initial page load
- Data visible in page source HTML
- No API request on initial load (check Network tab)

### Step 6: Optimize Performance
- Fetch multiple resources in parallel
- Use reactive fetching for dynamic routes: `() => \`/api/${route.params.id}\``
- Use `refresh()` to update data after mutations

## Anti-Patterns

❌ Using $fetch() directly in component
❌ Fetching in onMounted
❌ Not awaiting useFetch
❌ No error/loading handling
❌ Sequential fetching (slow)

## References
- Frontend guidelines: `app/AGENTS.md`
- Vue conventions: `.agents/vue-conventions.md`
