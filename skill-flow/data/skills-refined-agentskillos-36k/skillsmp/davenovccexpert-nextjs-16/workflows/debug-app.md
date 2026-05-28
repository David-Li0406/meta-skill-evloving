<workflow name="debug-app">
<title>Debug Next.js 16 App</title>

<required_reading>
**Read these reference files NOW:**
1. references/devtools-mcp.md
2. references/server-client-components.md
3. references/cache-components.md
</required_reading>

<process>

<step name="1-identify-error-type">
<title>Identify Error Type</title>

**Build Errors:** Occur during `npm run build`
- TypeScript errors
- Import errors
- Configuration issues

**Runtime Errors:** Occur during `npm run dev` or in production
- Hydration mismatches
- Server/Client boundary issues
- API errors

**Console Errors:** Appear in browser dev tools
- React warnings
- Network failures
- Unhandled promise rejections
</step>

<step name="2-use-devtools-mcp">
<title>Use Next.js DevTools MCP</title>

Next.js 16+ has MCP enabled by default at http://localhost:3000/_next/mcp

**Get all errors:**
```
Use the get_errors MCP tool to retrieve build, runtime, and type errors
```

**Get logs:**
```
Use the get_logs MCP tool to see console output and server logs
```

**Get routes:**
```
Use the get_routes MCP tool to map out application structure
```

**Get Server Action by ID:**
```
Use the get_server_action_by_id MCP tool when debugging Server Action issues
```
</step>

<step name="3-fix-hydration-mismatches">
<title>Fix Hydration Mismatches</title>

**Symptoms:**
- "Hydration failed" error
- Content flicker on page load
- Different content on server vs client

**Common Causes & Fixes:**

**Cause 1: Using browser APIs in Server Component**
```tsx
// BAD - window is undefined on server
function Component() {
  const width = window.innerWidth
  return <div>{width}</div>
}

// GOOD - mark as client component
'use client'
function Component() {
  const [width, setWidth] = useState(0)
  useEffect(() => {
    setWidth(window.innerWidth)
  }, [])
  return <div>{width}</div>
}
```

**Cause 2: Date/time differences**
```tsx
// BAD - different on server vs client
function Component() {
  return <div>{new Date().toLocaleString()}</div>
}

// GOOD - use suppressHydrationWarning or client component
function Component() {
  return <div suppressHydrationWarning>{new Date().toLocaleString()}</div>
}
```

**Cause 3: Non-serializable props**
```tsx
// BAD - passing function from server to client
<ClientComponent onClick={() => {}} />

// GOOD - pass Server Action instead
<ClientComponent action={serverAction} />
```
</step>

<step name="4-fix-server-client-boundary-issues">
<title>Fix Server/Client Boundary Issues</title>

**Error: "Cannot read properties of undefined"**

Check if you're using hooks in Server Component:
```tsx
// BAD - hooks in Server Component
export default function Page() {
  const [state, setState] = useState() // Error!
}

// GOOD - use client directive
'use client'
export default function Page() {
  const [state, setState] = useState()
}
```

**Error: "Unsupported Server Component type"**

Check if passing non-serializable data:
```tsx
// BAD - functions aren't serializable
export default function Page() {
  return <Client fn={() => console.log('hi')} />
}

// GOOD - use Server Actions
export default function Page() {
  async function action() {
    'use server'
    console.log('hi')
  }
  return <Client action={action} />
}
```
</step>

<step name="5-fix-caching-issues">
<title>Fix Caching Issues</title>

**Data not updating after mutation:**

1. Check if using `revalidateTag` or `updateTag`:
```tsx
'use server'
import { revalidateTag, updateTag } from 'next/cache'

export async function updateItem(id: string) {
  await db.items.update(id, { ... })

  // Use updateTag for immediate refresh
  updateTag('items')

  // Or revalidateTag for eventual consistency
  revalidateTag('items')
}
```

2. Verify the component has matching `cacheTag`:
```tsx
async function ItemList() {
  'use cache'
  cacheTag('items')  // Must match revalidateTag call

  const items = await db.items.findMany()
  return <ul>{...}</ul>
}
```

**Cache not working at all:**

Check `next.config.ts`:
```typescript
const nextConfig = {
  cacheComponents: true,  // Must be enabled!
}
```
</step>

<step name="6-fix-proxy-issues">
<title>Fix Proxy Issues (formerly Middleware)</title>

**Error: "proxy.ts not running"**

1. Check file location - must be at project root or in `src/`:
```
src/proxy.ts  OR  proxy.ts (root level)
```

2. Check export name:
```typescript
// BAD - old middleware name
export function middleware(request) { }

// GOOD - new proxy name
export function proxy(request) { }
```

3. Check runtime - proxy only runs on Node.js:
```typescript
// This is NOT supported in proxy.ts
export const runtime = 'edge'  // Remove this!
```
</step>

<step name="7-verify-fix">
<title>Verify Fix</title>

```bash
# Clear cache
rm -rf .next

# Rebuild
npm run build

# Run dev server
npm run dev

# Check for errors
npx tsc --noEmit
```

Use browser dev tools:
- Check Console for errors
- Check Network tab for failed requests
- Check React DevTools for component tree
</step>

</process>

<common_errors>
<error name="MODULE_NOT_FOUND">
**Cause:** Missing dependency or incorrect import path
**Fix:** Check import path, install missing packages
</error>

<error name="NEXT_NOT_FOUND">
**Cause:** 404 error for a route
**Fix:** Check file exists in app/ directory, check dynamic route params
</error>

<error name="DYNAMIC_SERVER_USAGE">
**Cause:** Using dynamic functions without proper handling
**Fix:** Add Suspense boundary or use `loading.tsx`
</error>

<error name="INVALID_SERVER_ACTION">
**Cause:** Server Action not properly marked
**Fix:** Add `'use server'` at top of function or file
</error>
</common_errors>

<success_criteria>
Debugging is complete when:
- [ ] Error no longer appears in console
- [ ] Build completes without errors
- [ ] TypeScript passes (`npx tsc --noEmit`)
- [ ] No hydration warnings in browser
- [ ] Feature works as expected
</success_criteria>

</workflow>
