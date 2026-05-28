# Next.js / React Best Practices and Anti-Patterns

Reference for: Codebase Audit

Current best practices for Next.js and React projects. Focus on what actually matters for the audit.

## Version Detection

Check `package.json` for versions:
- Next.js 13+ → App Router may be available
- Next.js 14+ → App Router is default, Server Components
- React 18+ → Concurrent features, Server Components

## Routing Pattern Detection

**Pages Router (Next.js <13 or legacy):**
- Routes in `pages/` directory
- `getServerSideProps`, `getStaticProps`, `getInitialProps`

**App Router (Next.js 13+):**
- Routes in `app/` directory
- Server Components by default
- `async` components with direct data fetching
- `loading.tsx`, `error.tsx` files

## Common Anti-Patterns

### 1. Mixing Router Paradigms

**Bad:** Using both `pages/` and `app/` without migration plan
```bash
grep -r "getServerSideProps\|getStaticProps" app/
```

If found in `app/` directory, that's wrong - App Router doesn't use these.

### 2. Client Components Overuse

**Bad:** Making everything `'use client'` unnecessarily

```bash
grep -r "'use client'" app/ | wc -l
```

If most files have `'use client'`, Server Components benefits are lost.

**Check for:**
- Client components that don't use interactivity (onClick, useState, etc.)
- Entire pages marked client when only small parts need it

### 3. Data Fetching Anti-Patterns

**Bad patterns to look for:**

```bash
# useEffect for data fetching in Server Components
grep -rn "useEffect.*fetch\|useEffect.*axios" app/

# API routes just proxying to external APIs
grep -rn "fetch.*process.env" app/api/
```

**Better:** Fetch directly in Server Components

### 4. Metadata Not Using generateMetadata

**Bad:** Static metadata in layout/page files for Next.js 14+

```bash
# Check if using old Head component
grep -rn "next/head" app/
```

Should use `export const metadata` or `generateMetadata()` in App Router.

### 5. Images Without next/image

**Bad:** Using `<img>` instead of `<Image>`

```bash
grep -rn "<img" app/ pages/ components/ | grep -v "next/image\|Image from"
```

`next/image` provides automatic optimization, lazy loading, responsive images.

### 6. Missing Loading States

**Check for:**
```bash
ls -R app/ | grep -c "loading.tsx\|loading.js"
```

App Router benefits from `loading.tsx` files for instant loading states.

### 7. Missing Error Boundaries

**Check for:**
```bash
ls -R app/ | grep -c "error.tsx\|error.js"
```

Should have error boundaries at route segments.

## Performance Anti-Patterns

### 1. Not Using Dynamic Imports

**Check for large client components:**
```bash
grep -rn "'use client'" app/ components/ | head -20
```

Look for heavy components (charts, editors) that should use `next/dynamic`:

```typescript
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false
})
```

### 2. Blocking Scripts

**Check for:**
```bash
grep -rn "<script" app/ pages/ | grep -v "next/script"
```

Should use `next/script` with `strategy` prop for third-party scripts.

### 3. Font Loading Issues

**Check for:**
```bash
grep -rn "@font-face\|font-family" styles/ app/
```

Should use `next/font` for automatic font optimization.

## State Management Issues

### 1. Prop Drilling

**Check for deep component trees passing same props:**
```bash
# Look for components with excessive props
grep -rn "props\.\|{.*,.*,.*,.*,.*,.*,.*}" components/ | head -20
```

Consider Context API or state management library.

### 2. Unnecessary Client State

**Check if data that could be URL params is in state:**
```bash
grep -rn "useState.*filter\|useState.*search\|useState.*page" components/
```

Filters, search terms, pagination should often be URL params for shareability.

## Security Issues

### 1. Exposing Env Variables

**Bad:** Using `NEXT_PUBLIC_` for secrets

```bash
grep -rn "NEXT_PUBLIC_" .env* | grep -i "secret\|key\|password\|token"
```

`NEXT_PUBLIC_` variables are exposed to the browser. Secrets should never use this prefix.

### 2. API Routes Without Auth

**Check API routes for auth middleware:**
```bash
grep -rn "export.*GET\|export.*POST" app/api/ pages/api/ | head -20
```

Each API route should validate auth unless explicitly public.

### 3. Unvalidated Form Inputs

**Check for direct form handling without validation:**
```bash
grep -rn "formData.get\|request.json()" app/api/ pages/api/
```

Should validate with zod, yup, or similar before processing.

## React-Specific Anti-Patterns

### 1. Missing Keys in Lists

```bash
grep -rn "\.map(" components/ app/ | grep -v "key=" | head -20
```

### 2. Inline Function Definitions

**Check for functions defined in render:**
```bash
grep -rn "onClick={() =>" components/ app/ | head -20
```

Creates new function on every render. Use `useCallback` or define outside component.

### 3. Mutating State

```bash
grep -rn "state\.\|setState.*\[" components/ app/ | head -20
```

Never mutate state directly: `state.push()`, `state.items[0] = x`

### 4. Missing Dependencies in useEffect

Look for `// eslint-disable-next-line react-hooks/exhaustive-deps`

These are often hiding bugs. Verify they're necessary.

## Recommended Checks

```bash
# Check for Pages Router in Next 14+ (should migrate)
[ -d "pages" ] && echo "Still using Pages Router"

# Check for deprecated getInitialProps
grep -rn "getInitialProps" pages/ app/

# Check for missing TypeScript
[ ! -f "tsconfig.json" ] && echo "No TypeScript config"

# Check for App Router usage
[ -d "app" ] && echo "Using App Router"

# Verify proper Image usage
grep -rn "next/image" app/ pages/ components/ | wc -l
```

## When to Flag as Critical

- API routes exposing secrets
- No auth on sensitive API routes
- Using `dangerouslySetInnerHTML` with user input
- Exposing secrets via `NEXT_PUBLIC_` variables

## When to Flag as Important

- Not using `next/image` for images
- Not using Server Components when possible
- Missing error boundaries
- Missing loading states
- Blocking scripts not using `next/script`
- Heavy client components not code-split

## When to Flag as Minor

- Inline function definitions (unless causing perf issues)
- Missing keys in lists (if not causing issues)
- Prop drilling (unless excessive)
