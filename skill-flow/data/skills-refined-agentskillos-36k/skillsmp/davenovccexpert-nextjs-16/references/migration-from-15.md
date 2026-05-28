<overview>
Complete guide for migrating from Next.js 15 to Next.js 16.
</overview>

<breaking_changes>
**Major breaking changes:**

| Change | Impact | Migration |
|--------|--------|-----------|
| `middleware.ts` → `proxy.ts` | File and export renamed | Run codemod |
| Caching is explicit | No default caching | Add `use cache` where needed |
| PPR config changed | `experimental.ppr` removed | Use `cacheComponents` |
| Edge runtime in proxy | Not supported | Remove `runtime: 'edge'` |
| Auth in middleware | Not secure | Move to DAL |
</breaking_changes>

<upgrade_steps>
**Step 1: Backup**
```bash
git checkout -b backup-before-v16
git push origin backup-before-v16
git checkout main
git checkout -b upgrade-to-v16
```

**Step 2: Upgrade dependencies**
```bash
npx @next/codemod@canary upgrade latest
```

Or manually:
```bash
npm install next@latest react@latest react-dom@latest
npm install -D @types/react@latest @types/react-dom@latest
```

**Step 3: Run codemods**
```bash
# Rename middleware to proxy
npx @next/codemod@latest rename-middleware-to-proxy .
```

**Step 4: Update next.config.ts**

Before:
```typescript
const nextConfig = {
  experimental: {
    ppr: true,
    reactCompiler: true,
  },
}
```

After:
```typescript
const nextConfig = {
  cacheComponents: true,
  reactCompiler: true,
}
```

**Step 5: Update proxy.ts**

Remove Edge runtime:
```typescript
// REMOVE this line
export const runtime = 'edge'
```

Rename export:
```typescript
// Before
export function middleware(request) { }

// After
export function proxy(request) { }
```

**Step 6: Move auth to DAL**

Before (in middleware):
```typescript
export function middleware(request) {
  const token = request.cookies.get('token')
  const user = await verifyJWT(token)  // DON'T DO THIS
  if (!user) return NextResponse.redirect('/login')
}
```

After (in DAL):
```typescript
// lib/dal.ts
export async function getUser() {
  const cookieStore = await cookies()
  const token = cookieStore.get('token')
  if (!token) return null
  return await verifyJWT(token.value)
}

export async function requireAuth() {
  const user = await getUser()
  if (!user) redirect('/login')
  return user
}
```

Use in pages/actions:
```typescript
export default async function DashboardPage() {
  const user = await requireAuth()
  return <Dashboard user={user} />
}
```

**Step 7: Update caching**

Before (implicit caching):
```typescript
async function getData() {
  // Cached by default in v15
  const res = await fetch(url)
  return res.json()
}
```

After (explicit caching):
```typescript
async function getData() {
  'use cache'
  cacheLife('hours')
  cacheTag('data')

  const res = await fetch(url)
  return res.json()
}
```

**Step 8: Update revalidation**

Before:
```typescript
revalidateTag('data')
```

After (choose based on need):
```typescript
// Immediate refresh
updateTag('data')

// Background revalidation
revalidateTag('data')
```

**Step 9: Test**
```bash
rm -rf .next
npm run build
npm run dev
npm test
```

**Step 10: Deploy**
```bash
git add .
git commit -m "Upgrade to Next.js 16"
git push origin upgrade-to-v16
# Create PR and merge
```
</upgrade_steps>

<codemod_reference>
**Available codemods:**

| Codemod | Purpose |
|---------|---------|
| `rename-middleware-to-proxy` | Rename file and export |
| `upgrade-next-config` | Update config options |

Run all:
```bash
npx @next/codemod@latest upgrade latest
```
</codemod_reference>

<common_issues>
<issue name="middleware-not-running">
**Symptom:** Proxy not executing

**Cause:** File not renamed or export not renamed

**Fix:**
```bash
# Check file exists
ls src/proxy.ts || ls proxy.ts

# Check export name
grep "export function proxy" src/proxy.ts
```
</issue>

<issue name="cache-not-working">
**Symptom:** Data always fresh, no caching

**Cause:** `cacheComponents` not enabled or `use cache` not added

**Fix:**
1. Check next.config.ts has `cacheComponents: true`
2. Add `'use cache'` to functions/components
</issue>

<issue name="auth-bypass">
**Symptom:** Protected routes accessible without auth

**Cause:** Auth only in proxy, not in DAL

**Fix:** Move auth checks to Data Access Layer
</issue>

<issue name="type-errors">
**Symptom:** TypeScript errors after upgrade

**Fix:**
```bash
npm install -D @types/react@latest @types/react-dom@latest
npx tsc --noEmit
```
</issue>

<issue name="hydration-errors">
**Symptom:** Hydration mismatch after upgrade

**Cause:** Server/Client component boundary issues

**Fix:**
- Check for browser APIs in Server Components
- Add `'use client'` where needed
- Use `suppressHydrationWarning` for dynamic content
</issue>
</common_issues>

<feature_comparison>
| Feature | Next.js 15 | Next.js 16 |
|---------|------------|------------|
| Bundler | Webpack (Turbo opt-in) | Turbopack (default) |
| Caching | Implicit | Explicit (`use cache`) |
| Middleware | `middleware.ts` | `proxy.ts` |
| PPR | `experimental.ppr` | `cacheComponents` |
| React Compiler | `experimental.reactCompiler` | `reactCompiler` |
| Auth location | Middleware (insecure) | DAL (recommended) |
| MCP DevTools | Not available | Built-in |
</feature_comparison>

<rollback>
**If upgrade fails:**

```bash
# Revert to backup
git checkout backup-before-v16

# Or revert specific commit
git revert HEAD

# Or downgrade dependencies
npm install next@15 react@18 react-dom@18
```
</rollback>

<checklist>
**Migration checklist:**

- [ ] Created backup branch
- [ ] Upgraded dependencies
- [ ] Ran codemods
- [ ] Updated next.config.ts
- [ ] Renamed middleware.ts to proxy.ts
- [ ] Updated proxy export name
- [ ] Removed Edge runtime from proxy
- [ ] Moved auth to DAL
- [ ] Added `use cache` where needed
- [ ] Updated revalidation calls
- [ ] Fixed TypeScript errors
- [ ] Build passes
- [ ] Tests pass
- [ ] Manual testing complete
- [ ] Deployed to staging
- [ ] Deployed to production
</checklist>
