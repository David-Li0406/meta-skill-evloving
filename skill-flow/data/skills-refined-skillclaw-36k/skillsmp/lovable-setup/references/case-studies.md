# Real Case Studies

Actual debugging sessions with symptoms, diagnosis, and fixes. Use these to recognize similar patterns.

---

## Case Study 1: 504 Gateway Timeout on Dependency

**Commit**: `0fd62f7` - "Add framer-motion to optimizeDeps for Lovable preview"

### Symptoms
- White screen in Lovable preview
- User checked browser console (F12 → Network tab)
- Found: `GET .../node_modules/.vite/deps/framer-motion.js 504 (Gateway Timeout)`

### Diagnosis
Lovable's server timed out while pre-bundling the `framer-motion` library. Large dependencies can exceed Lovable's default timeout during Vite's dependency optimization step.

### Fix
Added the dependency to `optimizeDeps.include` in `vite.config.ts`:

```typescript
optimizeDeps: {
  include: [
    "react",
    "react-dom",
    "react/jsx-runtime",
    "framer-motion",  // Added to fix 504 timeout
  ],
},
```

### How User Helped
User opened browser DevTools (F12), went to Network tab, and spotted the 504 status code. This immediately pointed to a dependency pre-bundling timeout.

---

## Case Study 2: Dynamic Import Failure - AppEntry.tsx

**Commit**: `4d92d9d` - "Fix AppEntry.tsx export for Lovable compatibility"

### Symptoms
- White screen in Lovable preview
- Browser console showed: `Failed to fetch dynamically imported module: .../AppEntry.tsx`
- Build worked locally, TypeScript check passed

### Diagnosis
Lovable uses dynamic ESM imports for `AppEntry.tsx`. The re-export syntax `export { default } from "./App"` doesn't work correctly with Lovable's dynamic import mechanism.

### Fix
Changed `AppEntry.tsx` from re-export to explicit import/export:

```tsx
// Before (broken)
export { default } from "./App";

// After (working)
import App from "./App";
export default App;
```

### How User Helped
User provided the exact error message from browser console, including the full URL. This confirmed the issue was specifically with AppEntry.tsx loading, not a general build issue.

---

## Case Study 3: Schema Query Error

**Commit**: `e5ede94` - "Fix cinema preferences schema query"

### Symptoms
- App loaded but feature didn't work
- Browser console showed: `Error loading cinema preferences: {code: 'PGRST205', message: "Could not find the table 'public.cinema_preferences' in the schema cache"}`

### Diagnosis
The `cinema_preferences` table exists in `bible_schema`, not `public`. Supabase queries default to `public` schema unless explicitly specified.

### Fix
Added `.schema("bible_schema")` to the Supabase query:

```typescript
// Before (wrong - queries public schema)
const { data } = await supabase
  .from("cinema_preferences")
  .select("*");

// After (correct - queries bible_schema)
const { data } = await (supabase as any)
  .schema("bible_schema")
  .from("cinema_preferences")
  .select("*");
```

### How User Helped
User knew which schema the table was in ("cinema.preferences is in the bible_schema") and provided the exact error code and message.

---

## Case Study 4: Package Lock Out of Sync

**Context**: CI pipeline failure after dependency changes

### Symptoms
- GitHub Actions CI failed
- Error: `npm ci can only install packages when package.json and package-lock.json are in sync`

### Diagnosis
Changes were made to `package.json` (adding framer-motion to root deps) but the lock file wasn't regenerated.

### Fix
```bash
rm package-lock.json
npm install
git add package-lock.json
git commit -m "Refresh package-lock.json"
git push
```

### How User Helped
User ran CI doctor skill which fetched the GitHub Actions logs and identified the exact error.

---

## Case Study 5: Vite Root Misconfigured for Monorepo

**Commit**: `a31c7b2` - "Fix Vite root for Lovable editor runtime"

### Symptoms
- White screen in Lovable `/projects/...` view
- `id-preview--*.lovable.app` worked fine
- Browser console showed: `Failed to load module script: Expected a JavaScript module script but the server responded with a MIME type of "text/html"`

### Diagnosis
In a monorepo, `vite.config.ts` had `root` pointing to `apps/raamattu-nyt`, but Lovable's editor runtime expects source modules to be resolvable from project root. Dynamic imports were rewritten to paths that returned HTML fallback instead of JS.

### Fix
Removed custom root and relied on default project root resolution:

```typescript
// Before (problematic in Lovable)
export default defineConfig({
  root: "apps/raamattu-nyt",
});

// After (Lovable-compatible)
export default defineConfig({
  // no custom root
});
```

### How User Helped
User noticed that the failing network request returned HTML instead of JS and shared the exact console error.

---

## Case Study 6: Security Headers Blocking Dynamic Imports

**Commit**: `9b41a6e` - "Remove restrictive COOP/CORP headers in preview"

### Symptoms
- White screen in Lovable preview
- No visible React error
- Browser console warning: `Blocked by Cross-Origin-Opener-Policy`

### Diagnosis
Custom security headers (COOP, CORP, Cross-Origin-Embedder-Policy) were injected via Vite dev server config. Lovable's preview environment loads modules from multiple origins, which broke dynamic imports.

### Fix
Disabled strict headers in preview/dev mode:

```typescript
// vite.config.ts
server: {
  headers: process.env.NODE_ENV === "production"
    ? {
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Embedder-Policy": "require-corp",
      }
    : {},
},
```

### How User Helped
User suspected headers because preview worked locally but failed only in Lovable, and shared the security config.

---

## Case Study 7: Missing React Error Boundary - Silent White Screen

**Commit**: `c72f4aa` - "Add global error boundary to prevent blank screen"

### Symptoms
- White screen in Lovable preview
- No visible errors in UI
- Console showed an uncaught exception during render

### Diagnosis
A runtime error occurred during React render, but no error boundary was present. Lovable preview does not always surface React render errors visually - app fails silently.

### Fix
Added a global error boundary:

```tsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong.</div>;
    }
    return this.props.children;
  }
}

// usage
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

### How User Helped
User copied the full console stack trace, revealing a render-time exception.

---

## Case Study 8: Dependency Installed Only in Workspace, Not Root

**Commit**: `f18d0e4` - "Move dependency to root package.json for Lovable"

### Symptoms
- White screen in Lovable preview
- Console error: `Failed to resolve module 'dayjs'`
- Local dev worked

### Diagnosis
Dependency was installed only in `apps/raamattu-nyt/package.json`. Lovable's dependency resolution expects shared deps in root `package.json`.

### Fix
Moved dependency to root:

```json
// root package.json
"dependencies": {
  "dayjs": "^1.11.10"
}
```

Reinstalled and rebuilt.

### How User Helped
User compared workspace vs root dependencies and noticed mismatch.

---

## Case Study 9: Incorrect Base Path for Assets

**Commit**: `61c92de` - "Remove custom base path for Lovable preview"

### Symptoms
- White screen
- Network tab showed: `GET /assets/index-xxxx.js 404`

### Diagnosis
`base` was set in `vite.config.ts` for production deployment (`/raamattu/`). Lovable preview serves app at root, causing asset URLs to break.

### Fix
Conditional base config:

```typescript
export default defineConfig(({ mode }) => ({
  base: mode === "production" ? "/raamattu/" : "/",
}));
```

### How User Helped
User noticed JS bundle 404s in Network tab.

---

## Case Study 10: Service Worker Caching Old Entry Chunk

**Commit**: `aa903ef` - "Disable service worker in Lovable preview"

### Symptoms
- White screen after recent changes
- Hard refresh didn't help
- Preview worked in incognito

### Diagnosis
A previously registered service worker served an outdated JS bundle incompatible with current code.

### Fix
Disabled SW in preview/dev:

```typescript
if (import.meta.env.DEV) {
  navigator.serviceWorker?.getRegistrations()
    .then(rs => rs.forEach(r => r.unregister()));
}
```

### How User Helped
User tested incognito mode and reported difference.

---

## User Debugging Guide

**What you can do to help diagnose Lovable issues:**

### 1. Check Browser Console
1. Open browser DevTools: `F12` (Windows/Linux) or `Cmd+Option+I` (Mac)
2. Go to **Console** tab for JavaScript errors
3. Go to **Network** tab for loading issues

### 2. Look for Non-200 HTTP Responses
In the Network tab, look for requests with status codes other than 200:

| Status | Meaning | Common Cause |
|--------|---------|--------------|
| **404** | Not Found | Missing file, wrong import path |
| **500** | Server Error | Build/compile error |
| **504** | Gateway Timeout | Dependency pre-bundling timeout |

### 3. Copy the Exact Error Message
When reporting issues, include:
- The full error message (not just the first line)
- The file path or URL mentioned in the error
- The HTTP status code if it's a network error

### 4. Note What Works vs What Doesn't
- Does local `npm run dev` work?
- Does local `npm run build` work?
- Does TypeScript check pass (`npm run typecheck`)?

### 5. Check Recent Changes
What changed since it last worked?
- New dependencies added?
- Files renamed or moved?
- Database schema changes?

### 6. Try Lovable's Rebuild Button
Sometimes Lovable's cache needs clearing. Use the "Rebuild" button in Lovable UI before diving into debugging.

---

## Quick Diagnostic Commands

Run these locally to narrow down the issue:

```bash
# 1. TypeScript check
npm run typecheck --workspace=apps/raamattu-nyt

# 2. Build check
npm run build --workspace=apps/raamattu-nyt

# 3. Lock file sync check
npm ci --dry-run

# 4. Missing dependencies
npm ls 2>&1 | grep -E "missing|extraneous"
```

If all pass locally but Lovable fails, the issue is likely:
- Export/import pattern incompatibility
- Dependency needs adding to `optimizeDeps.include`
- Dependency needs adding to root `package.json`
