# Bundle Analysis

## Running Bundle Analysis

```bash
# Standard analysis command
npm run analyze

# This opens a visual treemap of your bundle
```

## Reading the Analysis

### Chunk Types

| Chunk | Contains | Optimize By |
|-------|----------|-------------|
| `main` | Core framework | Upgrade Next.js |
| `pages/*` | Page-specific code | Code splitting |
| `node_modules/*` | Dependencies | Tree shaking, alternatives |
| `commons` | Shared between pages | Dynamic imports |

### Size Benchmarks

```
Good:
├── First Load JS: 87KB
├── main chunk: 45KB
└── page chunk: 12KB

Needs Work:
├── First Load JS: 250KB  ← Too large
├── main chunk: 120KB     ← Heavy dependencies
└── page chunk: 80KB      ← Too much page-specific code
```

## Optimization Strategies

### 1. Dynamic Imports

```typescript
// Before: Everything loaded upfront
import { Chart, DataTable, ExportButton } from "./components";

// After: Load on demand
import dynamic from "next/dynamic";

const Chart = dynamic(() => import("./Chart"), {
  loading: () => <ChartSkeleton />,
  ssr: false  // Skip SSR for client-only components
});

const DataTable = dynamic(() => import("./DataTable"));

// Conditional loading
const ExportButton = dynamic(
  () => import("./ExportButton"),
  { ssr: false }
);
```

### 2. Tree Shaking

```typescript
// ❌ Bad: Imports entire library
import _ from "lodash";
const result = _.debounce(fn, 300);

// ✅ Good: Tree-shakeable import
import debounce from "lodash/debounce";
const result = debounce(fn, 300);

// ✅ Better: Use lodash-es
import { debounce } from "lodash-es";

// ✅ Best: Native alternative
const debounce = (fn: Function, ms: number) => {
  let timeout: NodeJS.Timeout;
  return (...args: unknown[]) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), ms);
  };
};
```

### 3. Replace Heavy Dependencies

| Heavy Library | Size | Lighter Alternative | Size |
|---------------|------|---------------------|------|
| moment | 67KB | date-fns | 13KB |
| lodash | 71KB | lodash-es (tree-shakeable) | ~5KB used |
| axios | 13KB | fetch (native) | 0KB |
| uuid | 8KB | crypto.randomUUID() | 0KB |
| classnames | 1KB | clsx | 0.5KB |

### 4. Analyze Duplicates

```bash
# Check for duplicate packages
npm ls <package-name>

# Dedupe dependencies
npm dedupe
```

Common duplicates:
- Multiple React versions
- Multiple Tailwind versions
- Polyfills included twice

### 5. Externalize Large Libraries

```typescript
// next.config.ts
export default {
  experimental: {
    optimizePackageImports: [
      "@szum-tech/design-system",
      "lucide-react",
      "date-fns"
    ]
  }
};
```

## Code Splitting Patterns

### Route-Based (Automatic)

Next.js App Router automatically splits by route:
```
app/
├── page.tsx      → / (chunk)
├── about/
│   └── page.tsx  → /about (chunk)
└── dashboard/
    └── page.tsx  → /dashboard (chunk)
```

### Component-Based

```typescript
// Split heavy features
const AdminPanel = dynamic(() => import("./AdminPanel"), {
  loading: () => <AdminSkeleton />
});

// Only load for admins
{isAdmin && <AdminPanel />}
```

### Library-Based

```typescript
// Split heavy chart library
const ChartComponent = dynamic(
  () => import("recharts").then(mod => mod.LineChart),
  { ssr: false }
);
```

## Monitoring Bundle Size

### Build Output

```bash
npm run build

# Check output
Route (app)                    Size     First Load JS
┌ ○ /                         5.2 kB        89.1 kB
├ ○ /about                    1.8 kB        85.7 kB
├ ● /dashboard               12.4 kB        96.3 kB  ← Watch this
└ ○ /settings                 3.1 kB        87.0 kB

First Load JS shared by all:  83.9 kB
```

### Size Limits

```json
// package.json
{
  "size-limit": [
    {
      "path": ".next/static/chunks/*.js",
      "limit": "100 KB"
    }
  ]
}
```

## Common Bundle Issues

### Issue: Large First Load

```
First Load JS: 250KB ← Too large
```

**Diagnose:**
1. Run `npm run analyze`
2. Find largest chunks
3. Check for heavy dependencies

**Fix:**
- Dynamic import large components
- Replace heavy libraries
- Enable `optimizePackageImports`

### Issue: Duplicate Dependencies

**Diagnose:**
```bash
npm ls react
# Shows multiple versions
```

**Fix:**
```json
// package.json - force single version
{
  "overrides": {
    "react": "19.0.0"
  }
}
```

### Issue: Unshaken Code

**Diagnose:**
- Dead code visible in bundle analyzer

**Fix:**
```typescript
// Use named exports
export { Button } from "./Button";

// Not default exports for tree shaking
export default Button;  // Harder to tree shake
```
