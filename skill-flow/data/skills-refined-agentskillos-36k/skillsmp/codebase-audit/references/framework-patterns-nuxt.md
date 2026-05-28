# Nuxt / Vue Best Practices and Anti-Patterns

Reference for: Codebase Audit

Current best practices for Nuxt and Vue projects. Focus on what actually matters for the audit.

## Version Detection

Check `package.json` for versions:
- Nuxt 3+ → Vue 3, Composition API default, Nitro server
- Nuxt 2 → Vue 2, Options API (legacy, should migrate)
- Vue 3 → Composition API available
- Vue 2 → Options API only (EOL December 31, 2023)

## Project Structure Detection

**Nuxt 3:**
- `nuxt.config.ts` (TypeScript config)
- `app.vue` (root component)
- `pages/`, `components/`, `composables/`, `server/` directories
- Auto-imports enabled by default

**Nuxt 2:**
- `nuxt.config.js` (JS config)
- `layouts/default.vue`
- Explicit imports required

## Common Anti-Patterns

### 1. Still Using Nuxt 2

**Critical:** Nuxt 2 and Vue 2 are end-of-life.

```bash
cat package.json | grep '"nuxt"' | grep -v "nuxt3\|^3\."
cat package.json | grep '"vue"' | grep '"2\.'
```

If Nuxt 2 or Vue 2, flag as **critical** - should migrate immediately.

### 2. Options API in Vue 3 Projects

**Check for:**
```bash
grep -rn "export default.*{" components/ pages/ | grep -c "data()\|methods:\|computed:"
```

Vue 3 and Nuxt 3 prefer Composition API for better TypeScript support, reusability, and performance.

**Bad (Options API):**
```vue
<script>
export default {
  data() {
    return { count: 0 }
  },
  methods: {
    increment() { this.count++ }
  }
}
</script>
```

**Good (Composition API):**
```vue
<script setup>
const count = ref(0)
const increment = () => count.value++
</script>
```

### 3. Not Using Auto-Imports

**Nuxt 3 auto-imports:** `ref`, `computed`, `useState`, `useFetch`, components, composables

**Check for unnecessary imports:**
```bash
grep -rn "import.*ref.*from 'vue'\|import.*computed.*from 'vue'" components/ pages/ composables/
```

These should be auto-imported in Nuxt 3. Explicit imports suggest not leveraging Nuxt features.

### 4. Data Fetching Anti-Patterns

**Bad:** Using `onMounted` or `created` for data fetching

```bash
grep -rn "onMounted.*fetch\|onMounted.*axios\|created.*fetch" components/ pages/
```

**Good:** Use Nuxt composables:
- `useFetch()` - Auto-refreshes on route changes
- `useAsyncData()` - Custom async operations
- `useLazyFetch()` - Client-side only fetching

### 5. Missing Server Directory Usage

**Nuxt 3 server directory:** API routes, middleware, utils

```bash
[ ! -d "server/api" ] && echo "No server/api directory"
```

If project has API needs but no `server/api/`, they might be using external API routes unnecessarily.

### 6. Not Using Composables

**Check for duplicated logic:**
```bash
grep -rn "const.*fetch\|const.*fetch\|async.*get" components/ pages/ | head -20
```

Repeated logic (auth checks, API calls, state management) should be in `composables/`.

### 7. Missing TypeScript

**Nuxt 3 has first-class TypeScript support:**

```bash
[ ! -f "tsconfig.json" ] && echo "No TypeScript config in Nuxt 3 project"
```

Not using TypeScript in Nuxt 3 is missing significant benefits.

## Performance Anti-Patterns

### 1. Not Using Lazy Loading

**Check for:**
```bash
grep -rn "import.*from.*components" pages/ layouts/
```

Heavy components should use lazy loading:

```vue
<script setup>
const HeavyComponent = defineAsyncComponent(() => import('~/components/HeavyComponent.vue'))
</script>
```

### 2. Missing Static Site Generation (SSG)

**If content is mostly static:**

```bash
cat nuxt.config.ts | grep "ssr:\|target:"
```

Should use `ssr: true` with `nitro.prerender` for SSG, or `ssr: false` only if truly SPA.

### 3. Watchers Overuse

**Check for excessive watchers:**
```bash
grep -rn "watch(" components/ composables/ | wc -l
```

Watchers are often overused. Most cases are better with `computed()`.

### 4. Not Using Virtual Scrolling for Long Lists

**Check for long lists:**
```bash
grep -rn "v-for.*items\|v-for.*list" components/ pages/ | head -20
```

Lists with 100+ items should use virtual scrolling (`vue-virtual-scroller` or similar).

## Nuxt-Specific Issues

### 1. Incorrect Use of useState

**Bad:** Using `ref` for shared state across components

```bash
grep -rn "const.*=.*ref\|const.*=.*reactive" composables/
```

In composables, use `useState()` for shared state, not `ref()` or `reactive()`.

**Why:** `ref()` creates new instances per component. `useState()` provides shared state.

### 2. Not Using Nuxt Modules

**Check for common needs that have Nuxt modules:**

```bash
# Check if using third-party auth without @nuxtjs/auth
grep -rn "firebase.*auth\|Auth0" . | head -5
cat package.json | grep "@nuxtjs/auth"

# Check if using axios without @nuxtjs/axios
grep -rn "import axios" . | head -5
cat package.json | grep "@nuxtjs/axios"
```

Nuxt modules provide better integration than manual setup.

### 3. Layouts Not Being Used

**Check for:**
```bash
[ ! -d "layouts" ] && echo "No layouts directory"
ls layouts/ 2>/dev/null | wc -l
```

If pages share structure but no layouts exist, there's duplication.

### 4. Missing Error Handling

**Check for error.vue:**
```bash
[ ! -f "error.vue" ] && echo "No error.vue for error handling"
```

Nuxt 3 uses `error.vue` in root for global error handling.

## State Management Issues

### 1. Using Vuex in Nuxt 3

**Critical:** Vuex is not recommended for Nuxt 3

```bash
grep -rn "vuex\|createStore" . | grep -v node_modules
```

Should use Pinia (official state management) or `useState()` composables.

### 2. Not Using Pinia When Needed

**If complex state management is needed:**

```bash
cat package.json | grep "pinia"
```

For complex apps, Pinia provides DevTools, plugins, and better TypeScript support than just `useState()`.

## Security Issues

### 1. Runtime Config Misuse

**Bad:** Using `publicRuntimeConfig` for secrets

```bash
grep -rn "publicRuntimeConfig" nuxt.config.ts
```

`publicRuntimeConfig` is exposed to the browser. Use `privateRuntimeConfig` or environment variables for secrets.

### 2. Missing CSRF Protection

**Check for forms without CSRF:**
```bash
grep -rn "<form\|@submit" pages/ components/ | head -20
```

Nuxt server routes should have CSRF protection for mutations.

### 3. SSR Data Leakage

**Check for sensitive data in SSR:**
```bash
grep -rn "ssrContext\|useRequestHeaders" server/ composables/
```

Ensure sensitive headers (cookies, auth tokens) don't leak between requests.

## Vue-Specific Anti-Patterns

### 1. Mutating Props

```bash
grep -rn "props\.\|props\[" components/ | grep "=.*props\."
```

Never mutate props directly. Emit events or use v-model.

### 2. Missing Keys in v-for

```bash
grep -rn "v-for" components/ pages/ | grep -v ":key="
```

### 3. Reactive Data Not Being Reactive

**Check for:**
```bash
grep -rn "let.*=.*ref\|var.*=.*ref" components/ composables/
```

Should use `const` with `ref()` - the `.value` is what changes, not the ref itself.

### 4. Not Using Proper Event Naming

**Check for:**
```bash
grep -rn "@click\|@input\|emit(" components/ | head -20
```

Custom events should use kebab-case: `@update-value` not `@updateValue`.

## Recommended Checks

```bash
# Check Nuxt version
cat package.json | grep '"nuxt"'

# Check for Nuxt 3 features
[ -d "composables" ] && echo "Using composables (Nuxt 3)"
[ -d "server/api" ] && echo "Using server API routes (Nuxt 3)"

# Check for TypeScript
[ -f "tsconfig.json" ] && echo "TypeScript enabled"

# Check for Pinia (state management)
cat package.json | grep "pinia"

# Check for Options API usage (should minimize in Vue 3)
grep -rn "export default.*{" components/ pages/ | grep -c "data()\|methods:"

# Check for proper Nuxt 3 data fetching
grep -rn "useFetch\|useAsyncData" pages/ components/ | wc -l
```

## When to Flag as Critical

- Using Nuxt 2 or Vue 2 (EOL)
- Exposing secrets in `publicRuntimeConfig`
- Using Vuex in Nuxt 3 (deprecated)
- SSR data leakage between requests

## When to Flag as Important

- Using Options API extensively in Vue 3
- Not using auto-imports (manual imports of Vue/Nuxt functions)
- Not using composables for shared logic
- Missing TypeScript in Nuxt 3 project
- No error.vue for error handling
- Data fetching in `onMounted` instead of `useFetch`

## When to Flag as Minor

- Not using Pinia when state management is simple
- Layouts directory missing when pages are similar
- Missing lazy loading for heavy components
- Excessive watchers (unless causing performance issues)
