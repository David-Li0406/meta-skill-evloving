<workflow name="migrate-from-15">
<title>Migrate from Next.js 15 to 16</title>

<required_reading>
**Read these reference files NOW:**
1. references/migration-from-15.md
2. references/proxy.md
3. references/cache-components.md
</required_reading>

<process>

<step name="1-backup-and-prepare">
<title>Backup and Prepare</title>

```bash
# Create a backup branch
git checkout -b backup-before-nextjs-16
git push origin backup-before-nextjs-16

# Return to main branch
git checkout main

# Create migration branch
git checkout -b migrate-to-nextjs-16
```
</step>

<step name="2-upgrade-dependencies">
<title>Upgrade Dependencies</title>

**Use the automated upgrade CLI:**
```bash
npx @next/codemod@canary upgrade latest
```

This will:
- Update `next` to latest version
- Update `react` and `react-dom` to compatible versions
- Update TypeScript types

**Or upgrade manually:**
```bash
npm install next@latest react@latest react-dom@latest
npm install -D @types/react@latest @types/react-dom@latest
```
</step>

<step name="3-run-codemods">
<title>Run Codemods</title>

**Rename middleware to proxy:**
```bash
npx @next/codemod@latest rename-middleware-to-proxy .
```

This renames:
- `middleware.ts` → `proxy.ts`
- Export `middleware` → `proxy`

**If codemod fails, do manually:**
```bash
# Rename file
mv src/middleware.ts src/proxy.ts  # or mv middleware.ts proxy.ts

# Edit the file
# Change: export function middleware(...)
# To: export function proxy(...)
```
</step>

<step name="4-update-next-config">
<title>Update next.config</title>

**Before (Next.js 15):**
```typescript
const nextConfig = {
  experimental: {
    ppr: true,
    reactCompiler: true,
  },
}
```

**After (Next.js 16):**
```typescript
const nextConfig = {
  cacheComponents: true,  // Replaces experimental.ppr
  reactCompiler: true,    // Now stable, not experimental
}
```

**Remove deprecated options:**
- `experimental.ppr` → Use `cacheComponents`
- `experimental.dynamicIO` → Part of `cacheComponents`
- `experimental.useCache` → Part of `cacheComponents`
</step>

<step name="5-migrate-middleware-to-proxy">
<title>Migrate Middleware to Proxy</title>

**Key differences:**
1. Proxy runs on Node.js runtime (NOT Edge)
2. Proxy is for routing only (NOT auth)
3. Export name changed from `middleware` to `proxy`

**Before (Next.js 15 middleware.ts):**
```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export const runtime = 'edge'  // Remove this!

export function middleware(request: NextRequest) {
  // DON'T do auth here anymore
  const token = request.cookies.get('token')
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  return NextResponse.next()
}
```

**After (Next.js 16 proxy.ts):**
```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// No runtime export - always Node.js

export function proxy(request: NextRequest) {
  // Only do routing logic
  // Check for session cookie existence (NOT validation)
  const hasSession = request.cookies.has('session')
  if (!hasSession) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  return NextResponse.next()
}
```

**Move auth logic to Data Access Layer:**
```typescript
// lib/dal.ts
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export async function getUser() {
  const cookieStore = await cookies()
  const session = cookieStore.get('session')

  if (!session) {
    redirect('/login')
  }

  // Actually validate the session
  const user = await verifySession(session.value)
  if (!user) {
    redirect('/login')
  }

  return user
}
```
</step>

<step name="6-update-caching-patterns">
<title>Update Caching Patterns</title>

**Before (Next.js 15 - implicit caching):**
```typescript
// Data was cached by default
async function getData() {
  const res = await fetch('https://api.example.com/data')
  return res.json()
}
```

**After (Next.js 16 - explicit caching):**
```typescript
// Data is NOT cached by default
async function getData() {
  'use cache'
  cacheLife('hours')
  cacheTag('data')

  const res = await fetch('https://api.example.com/data')
  return res.json()
}
```

**Update revalidation calls:**
```typescript
// Before
import { revalidatePath, revalidateTag } from 'next/cache'

// After - also consider updateTag for immediate updates
import { revalidatePath, revalidateTag, updateTag } from 'next/cache'

// Use updateTag when you need immediate refresh
updateTag('data')

// Use revalidateTag for eventual consistency
revalidateTag('data')
```
</step>

<step name="7-remove-edge-runtime">
<title>Remove Edge Runtime Usage</title>

**Proxy doesn't support Edge:**
```typescript
// REMOVE from proxy.ts
export const runtime = 'edge'  // DELETE THIS
```

**If you need Edge for routes:**
```typescript
// app/api/fast/route.ts
export const runtime = 'edge'  // OK for API routes
```
</step>

<step name="8-update-security-patterns">
<title>Update Security Patterns</title>

**Add auth to Server Actions:**
```typescript
'use server'

import { getUser } from '@/lib/dal'

export async function updateProfile(formData: FormData) {
  // ALWAYS verify auth in Server Actions
  const user = await getUser()

  // ALWAYS validate input
  const name = formData.get('name')
  if (typeof name !== 'string' || name.length < 2) {
    return { error: 'Invalid name' }
  }

  await db.users.update({
    where: { id: user.id },
    data: { name },
  })

  return { success: true }
}
```

**Apply security patches:**
Check for CVE-2025-55182 and CVE-2025-66478 fixes:
```bash
npm audit
npm audit fix
```
</step>

<step name="9-test-migration">
<title>Test Migration</title>

```bash
# Clear cache
rm -rf .next

# Check types
npx tsc --noEmit

# Run dev server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

**Manual testing checklist:**
- [ ] All pages load without errors
- [ ] Authentication works correctly
- [ ] Forms submit and data updates
- [ ] No hydration errors in console
- [ ] Navigation works (client and server)
- [ ] API routes respond correctly
</step>

<step name="10-deploy-and-monitor">
<title>Deploy and Monitor</title>

```bash
# Commit changes
git add .
git commit -m "Migrate to Next.js 16"

# Deploy to staging first
vercel --env preview

# Test staging thoroughly

# Deploy to production
git push origin migrate-to-nextjs-16
# Create PR and merge
```

**Monitor for issues:**
- Check error tracking (Sentry, etc.)
- Monitor Core Web Vitals
- Watch for auth-related errors
- Check cache behavior
</step>

</process>

<breaking_changes>
**Next.js 16 Breaking Changes:**

1. **middleware.ts → proxy.ts**
   - File renamed
   - Export renamed from `middleware` to `proxy`
   - Runs on Node.js only (no Edge)

2. **Caching is explicit**
   - No default caching
   - Must use `'use cache'` directive
   - `experimental.ppr` removed → use `cacheComponents`

3. **React Compiler stable**
   - `experimental.reactCompiler` → `reactCompiler`

4. **Security hardening**
   - Middleware/proxy not for auth
   - Use Data Access Layer pattern
   - Server Actions must verify auth
</breaking_changes>

<success_criteria>
Migration is complete when:
- [ ] All codemods applied successfully
- [ ] middleware.ts renamed to proxy.ts
- [ ] Auth logic moved to Data Access Layer
- [ ] Caching updated to explicit model
- [ ] next.config.ts updated for v16
- [ ] Build passes without errors
- [ ] Types pass
- [ ] All tests pass
- [ ] Manual testing passes
- [ ] Deployed to production successfully
</success_criteria>

</workflow>
