# Nextjs App Router - Sharp Edges

## Nextjs Async Client Component

### **Id**
nextjs-async-client-component
### **Summary**
Client Components cannot be async
### **Severity**
critical
### **Situation**
You add async to a component that has 'use client' directive
### **Why**
  Client Components run in the browser. While top-level await exists,
  React components need to return JSX synchronously. The async keyword
  on a component means it returns a Promise, not JSX.
  
### **Solution**
  Move data fetching to:
  1. A Server Component parent that passes data as props
  2. useEffect with useState for client-side fetching
  3. A data fetching library like SWR or React Query
  
### **Symptoms**
  - Cannot use keyword 'await' outside an async function
  - Component returns Promise instead of JSX
  - Hydration mismatch errors
### **Detection Pattern**
["']use client["'][\\s\\S]*?async\\s+function
### **Version Range**
>=13.0.0

## Nextjs Server Import In Client

### **Id**
nextjs-server-import-in-client
### **Summary**
Server-only imports in Client Components fail
### **Severity**
critical
### **Situation**
You import fs, path, database clients, or 'server-only' in a 'use client' file
### **Why**
  Client Components are bundled for the browser. Node.js modules and
  server-only packages don't exist in the browser environment.
  
### **Solution**
  1. Move the import to a Server Component
  2. Create a Server Action for the server-side logic
  3. Create an API route if you need an endpoint
  
### **Symptoms**
  - Module not found: Can't resolve 'fs'
  - Module not found: Can't resolve 'server-only'
  - Build fails with "can't be imported from a Client Component"
### **Detection Pattern**
["']use client["'][\\s\\S]*?import.*from\\s*["'](?:fs|path|crypto|server-only|next/headers)
### **Version Range**
>=13.0.0

## Nextjs Hydration Mismatch

### **Id**
nextjs-hydration-mismatch
### **Summary**
Hydration errors from browser-only APIs
### **Severity**
high
### **Situation**
Using window, document, localStorage, or Date during initial render
### **Why**
  Server Components render on the server where browser APIs don't exist.
  If the server renders different content than the client, React throws
  a hydration mismatch error.
  
### **Solution**
  1. Use useEffect for browser-only code (runs only on client)
  2. Use dynamic import with { ssr: false }
  3. Check typeof window !== 'undefined' before accessing
  4. Use the 'use client' directive and useEffect
  
### **Symptoms**
  - Text content did not match
  - Hydration failed because the initial UI does not match
  - There was an error while hydrating
### **Detection Pattern**
(?<!typeof\\s)(?:window\\.|document\\.|localStorage)
### **Version Range**
>=13.0.0

## Nextjs Missing Use Server

### **Id**
nextjs-missing-use-server
### **Summary**
Server Action without 'use server' directive
### **Severity**
high
### **Situation**
Creating a function meant to run on the server but forgetting the directive
### **Why**
  Without 'use server', the function is just a regular function. If called
  from a Client Component, it will try to run in the browser, failing or
  exposing server logic.
  
### **Solution**
  Add 'use server' either:
  1. At the top of a file containing only server actions
  2. At the top of the individual function body
  
### **Symptoms**
  - Function runs on client instead of server
  - Database operations fail in browser
  - Secrets exposed to client
### **Detection Pattern**
export\\s+async\\s+function\\s+\\w+Action
### **Version Range**
>=14.0.0

## Nextjs Cookies In Client

### **Id**
nextjs-cookies-in-client
### **Summary**
Using cookies() in Client Components
### **Severity**
critical
### **Situation**
Calling cookies() from next/headers in a Client Component
### **Why**
  cookies() is a server-only function that reads request headers.
  It doesn't exist in the browser context.
  
### **Solution**
  1. Read cookies in a Server Component and pass values as props
  2. Use document.cookie for client-side cookie access
  3. Use a Server Action to get cookie values
  
### **Symptoms**
  - cookies is not a function
  - headers is not a function
  - Build error about server-only imports
### **Detection Pattern**
["']use client["'][\\s\\S]*?cookies\\(\\)
### **Version Range**
>=13.0.0

## Nextjs Use Client Boundary

### **Id**
nextjs-use-client-boundary
### **Summary**
Forgetting that 'use client' creates a boundary
### **Severity**
medium
### **Situation**
  Expecting child components of a Client Component to be Server Components
  
### **Why**
  When you mark a component with 'use client', all its children are also
  Client Components by default (unless passed as children props).
  
### **Solution**
  To use Server Components inside Client Components:
  1. Pass them as children props
  2. Pass them as any prop (composition pattern)
  
  // This works:
  <ClientComponent>
    <ServerComponent /> {/* Still a Server Component */}
  </ClientComponent>
  
### **Symptoms**
  - Server-only imports failing in child components
  - Larger bundle than expected
  - Database queries in components that should be server
### **Detection Pattern**

### **Version Range**
>=13.0.0

## Nextjs Revalidate Confusion

### **Id**
nextjs-revalidate-confusion
### **Summary**
Not understanding revalidatePath vs revalidateTag
### **Severity**
medium
### **Situation**
Cache not invalidating after mutations
### **Why**
  revalidatePath invalidates a specific URL path's cache.
  revalidateTag invalidates all fetches tagged with that tag.
  Using the wrong one means stale data.
  
### **Solution**
  Use revalidatePath when:
  - You know the exact page that needs refreshing
  - Single page affected by the mutation
  
  Use revalidateTag when:
  - Multiple pages show the same data
  - You want granular cache control
  - Data is fetched with fetch() and tagged
  
### **Symptoms**
  - Data not updating after Server Action
  - Need to hard refresh to see changes
  - Some pages update, others don't
### **Detection Pattern**
revalidate(?:Path|Tag)\\(
### **Version Range**
>=13.0.0

## Nextjs Middleware Cold Start

### **Id**
nextjs-middleware-cold-start
### **Summary**
Middleware redirects flash on cold start
### **Severity**
medium
### **Situation**
Users see a flash of the wrong page before redirect kicks in
### **Why**
  Next.js middleware runs at the edge. On cold starts, there can be a
  delay before the middleware executes, causing the original page to
  briefly render.
  
### **Solution**
  1. Use loading.tsx to show a loading state
  2. Check auth state in the page component as backup
  3. Use cookies for instant auth checks
  4. Consider using layout-level auth checks
  
### **Symptoms**
  - Brief flash of protected content
  - Redirect happens after page starts rendering
  - Inconsistent behavior between hot and cold loads
### **Detection Pattern**
middleware\\.ts
### **Version Range**
>=13.0.0

## Nextjs Dynamic Metadata Streaming

### **Id**
nextjs-dynamic-metadata-streaming
### **Summary**
Dynamic metadata blocks streaming
### **Severity**
low
### **Situation**
Using generateMetadata with slow data fetches
### **Why**
  generateMetadata must complete before the page starts streaming.
  If it does slow database queries, the entire page is delayed.
  
### **Solution**
  1. Cache metadata queries aggressively
  2. Keep metadata fetches fast and simple
  3. Consider static metadata for pages that don't need dynamic titles
  
### **Symptoms**
  - Slow Time to First Byte (TTFB)
  - Page takes long to start showing content
  - Streaming benefits lost
### **Detection Pattern**
generateMetadata
### **Version Range**
>=13.0.0