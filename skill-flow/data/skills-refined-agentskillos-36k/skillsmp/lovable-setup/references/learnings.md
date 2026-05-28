# Lovable Setup Learnings

Patterns discovered from debugging Lovable preview issues.

## Monorepo Configuration

### New Shared Package Requires 3 Path Alias Updates

**Pattern:** Adding new shared package to monorepo used by apps

**Symptom:**
- Lovable preview white screen
- Build error: "Failed to resolve import @shared-X"
- 404 for main entry file

**Wrong:** ❌
```typescript
// Only added to root vite.config.ts - build fails!
// Root vite.config.ts
alias: {
  "@shared-errors": path.resolve(__dirname, "./packages/shared-errors/src"),
}
```

**Right:** ✅
```typescript
// 1. Root vite.config.ts (for monorepo launcher)
export default defineConfig({
  resolve: {
    alias: {
      "@shared-errors": path.resolve(__dirname, "./packages/shared-errors/src"),
    },
  },
});

// 2. apps/[app-name]/vite.config.ts (for app build)
export default defineConfig({
  resolve: {
    alias: {
      "@shared-errors": path.resolve(__dirname, "../../packages/shared-errors/src"),
    },
  },
});

// 3. tsconfig.app.json (for TypeScript)
{
  "compilerOptions": {
    "paths": {
      "@shared-errors/*": ["./packages/shared-errors/src/*"]
    }
  }
}
```

**Why:**
- **Root vite.config.ts:** Used by monorepo launcher (`src/App.tsx`) that dynamically loads apps
- **App vite.config.ts:** Used when building the specific app (apps run their own vite build)
- **tsconfig.app.json:** Used by TypeScript compiler for type checking and IDE support

Missing any one causes build failures or Lovable white screen.

**Diagnostic Steps:**
1. Check build locally: `npm run build`
2. If "Failed to resolve import @shared-X" → Check all 3 locations
3. Verify paths match: root uses `./packages/`, app uses `../../packages/`

**Real Example:** Added `@shared-errors` package, forgot to add alias to app vite.config.ts. Lovable showed white screen because app build couldn't resolve imports.

---

## Module Resolution

### Vite Aliases vs TypeScript Paths

**Pattern:** Aliases work in dev but fail in build

**Why:**
- Vite uses `resolve.alias` for runtime module resolution
- TypeScript uses `compilerOptions.paths` for type checking
- Both must match for builds to work

**Checklist When Adding Package:**
- [ ] Added to root vite.config.ts `resolve.alias`
- [ ] Added to app vite.config.ts `resolve.alias`
- [ ] Added to tsconfig.app.json `compilerOptions.paths`
- [ ] Paths use correct relative depth (`./` vs `../../`)
- [ ] Build succeeds locally: `npm run build`

---

*Update this file when discovering Lovable-specific patterns.*
