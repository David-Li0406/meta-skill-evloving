---
name: typescript-performance
description: Debug and fix slow TypeScript type checking. Use when tsc or IDE is slow, type checking takes too long, or need to analyze TS compiler performance. Covers diagnostics, tracing, analysis tools, and common fixes.
---

# TypeScript Performance Debugging

## Diagnostic Commands

### Quick Assessment
```bash
# Basic metrics - run multiple times (caching affects results)
tsc --noEmit --extendedDiagnostics

# Key metrics to watch:
# - Check time: Should be <10s for medium projects
# - Instantiations: >1M is a red flag
# - Types: Correlates with complexity
# - Memory used: Watch for >1GB
```

### Generate Trace (Primary Tool)
```bash
# Generate trace files for deep analysis
tsc --noEmit --generateTrace ./trace-output

# For memory issues, increase heap
node --max-old-space-size=8192 ./node_modules/.bin/tsc --noEmit --generateTrace ./trace-output
```

Outputs `trace.json` and `types.json` in the output directory.

## Trace Analysis

### Using @typescript/analyze-trace (Recommended)
```bash
npm install --save-dev @typescript/analyze-trace
npx analyze-trace ./trace-output
```

Output shows hot spots with file locations, line numbers, and time spent. Look for:
- Check file times >1s
- checkExpression operations
- Compare types operations
- Deferred node checks

Options:
- `--skipMillis=50` - lower threshold to see more results
- `--forceMillis=1000` - only show items >1s

### Simplify Types File
```bash
npx simplify-trace-types ./trace-output/types.json output.txt
npx print-trace-types ./trace-output/types.json <type-id>
```

### Visual Analysis
Load `trace.json` into:
- **Perfetto** (https://ui.perfetto.dev) - modern, handles large files
- **chrome://tracing** - built into Chrome
- **Speedscope** (https://speedscope.app) - better UX

Focus on the "Check" phase in the flame graph - typically 90%+ of total time.

## Common Performance Killers

### 1. Complex Generic Types
Conditional types, mapped types, and deep recursion cause exponential checking:
```typescript
// BAD: Deeply nested conditional
type DeepPartial<T> = T extends object 
  ? { [P in keyof T]?: DeepPartial<T[P]> } 
  : T;

// BETTER: Limit recursion depth or use simpler patterns
```

### 2. Large Union Types
Union intersection is quadratic:
```typescript
// BAD: 100+ member unions
type AllEvents = Event1 | Event2 | ... | Event100;

// BETTER: Use base type + discriminator
interface BaseEvent { type: string }
```

### 3. Excessive Type Inference
```typescript
// BAD: Complex inferred return types
export const createStore = () => {
  // 50 lines of complex logic
};

// BETTER: Explicit return type annotation
export const createStore = (): Store => { ... };
```

### 4. Duplicate Package Versions
`analyze-trace` warns about this. Different versions = different type identities = no caching. Fix with:
- npm/pnpm `overrides` 
- yarn `resolutions`
- Dedupe: `npm dedupe` / `pnpm dedupe`

### 5. Including Too Many Files
```json
// Check what's included
tsc --listFiles
```

## tsconfig.json Optimizations

### Quick Wins
```json
{
  "compilerOptions": {
    "skipLibCheck": true,        // Skip .d.ts checking
    "incremental": true,         // Cache between builds
    "tsBuildInfoFile": ".tsbuildinfo"
  }
}
```

### For Large Projects
```json
{
  "compilerOptions": {
    "composite": true,           // Required for project refs
    "declaration": true,
    "declarationMap": true,
    "isolatedModules": true      // For bundlers (Babel/esbuild)
  }
}
```

### Exclude Unnecessary Files
```json
{
  "include": ["src/**/*"],
  "exclude": [
    "node_modules",
    "**/*.test.ts",
    "**/*.spec.ts",
    "dist",
    "coverage"
  ]
}
```

### Limit @types
```json
{
  "compilerOptions": {
    "types": ["node", "jest"],  // Only include what's needed
    "typeRoots": ["./node_modules/@types"]
  }
}
```

## Project References (Monorepos)

Split large codebase into smaller compilable units:

```json
// Root tsconfig.json
{
  "files": [],
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/ui" }
  ]
}

// packages/core/tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

Build with: `tsc --build` or `tsc -b`

## IDE/Editor Performance

### VS Code TSServer Logs
1. Open Settings, search "typescript trace"
2. Set `typescript.tsserver.trace` to "verbose"
3. Open Output panel → TypeScript

### Disable Plugins
Test without TS-related extensions to isolate issues.

## Workflow

1. **Baseline**: `tsc --noEmit --extendedDiagnostics` (run 3x, average)
2. **Trace**: `tsc --noEmit --generateTrace ./trace`
3. **Analyze**: `npx analyze-trace ./trace`
4. **Investigate**: Focus on top hot spots, check specific files/lines
5. **Fix**: Apply targeted changes
6. **Verify**: Re-run diagnostics, compare metrics

## Red Flags in Diagnostics

| Metric | Warning | Critical |
|--------|---------|----------|
| Check time | >15s | >60s |
| Instantiations | >1M | >5M |
| Types | >500K | >1M |
| Memory | >1GB | >4GB |

## Quick Fixes Checklist

- [ ] `skipLibCheck: true`
- [ ] `incremental: true`
- [ ] Exclude test files from main tsconfig
- [ ] Add explicit return type annotations to exported functions
- [ ] Deduplicate node_modules packages
- [ ] Split into project references if >500 files
- [ ] Check for circular dependencies
- [ ] Limit union type sizes (<50 members)
- [ ] Avoid deeply nested conditional types
