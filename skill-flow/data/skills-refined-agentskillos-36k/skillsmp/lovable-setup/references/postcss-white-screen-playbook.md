# White Screen Playbook: "Cannot find package 'postcss'"

Use when Lovable preview shows white screen with console error:
`[plugin:vite:css] [postcss] Cannot find package 'postcss'`

## What This Error Means

This is **NOT a CSS bug** - it's a build toolchain dependency resolution failure:
1. Vite's CSS pipeline tries to load PostCSS
2. Lovable preview environment doesn't have `postcss` installed
3. Vite never finishes bundling → app never mounts → white screen

## Confirm You're Looking at the Right Problem

**In Lovable:**
- Active Edit can be misleading - verify via latest commit → "See Preview" (full build)

**In console:**
- If you see `[plugin:vite:css] [postcss] Cannot find package 'postcss'`
- You're in **dependency/install territory**, not UI rendering territory

## Root Causes (90% of cases)

### A) Dependencies in devDependencies Only

Lovable preview installs only production deps.

**Fix:** Move/duplicate to `dependencies` in **root** package.json:
- `postcss`
- `autoprefixer`
- `tailwindcss`
- `tailwindcss-animate` (if used)

### B) Tailwind v4 Plugin Split

Tailwind v4 requires separate PostCSS plugin:
- Install `@tailwindcss/postcss`
- Update `postcss.config.*` to reference it correctly

### C) Multiple PostCSS Configs

Having both root and app-level configs causes non-determinism.

**Fix:** Keep only ONE `postcss.config.*` at root level (where Vite runs).

## Fast Triage Checklist

### Step 1: Verify Dependency Placement

```bash
# Check root package.json has these in dependencies (not just devDependencies)
grep -E "postcss|tailwindcss|autoprefixer" package.json
```

Expected: All three visible in root package.json dependencies.

### Step 2: Verify Lockfile Consistency

```bash
# If package.json changed, lockfile must be updated
npm install
git diff package-lock.json
```

If lockfile changed, commit it.

### Step 3: Verify PostCSS Config is Unambiguous

```bash
# Find all postcss configs
find . -name "postcss.config.*" -not -path "./node_modules/*"
```

Keep only root config, remove app-level duplicates.

### Step 4: Confirm No Tailwind CDN

```bash
# Search for CDN usage
grep -r "cdn.tailwindcss.com" . --include="*.html" --include="*.tsx"
```

If found, remove it.

### Step 5: Confirm Which Vite Entry Runs

In monorepos, check:
- Which `vite.config.ts` runs in Lovable preview?
- PostCSS config must be where that Vite instance resolves it

## Verification

When fixed, you should see ALL of:
1. Lovable preview loads without overlay
2. CSS is applied (Tailwind utilities render)
3. Static assets behave normally
4. i18n `public/locales/*` changes show in commit preview

## Prevention Guardrails

### A) CI Check

Add CI job that:
1. Installs with production-only semantics
2. Runs `vite build`

Catches: missing postcss, Tailwind upgrade issues, lockfile drift.

### B) Single Config Rule

- Only one `postcss.config.*` in project root
- App-level config only if app has separate Vite entry

### C) Tailwind Upgrade Checklist

When Tailwind major version changes:
1. Verify PostCSS plugin expectations
2. Verify config syntax
3. Verify dependencies exist in Lovable preview environment

## Quick Fix Commands

```bash
# 1. Add postcss to root dependencies
npm install --save postcss autoprefixer tailwindcss

# 2. Regenerate lockfile
rm package-lock.json && npm install

# 3. Remove duplicate configs
rm apps/*/postcss.config.* 2>/dev/null || true

# 4. Commit and push
git add package.json package-lock.json
git commit -m "fix: Move PostCSS deps to root for Lovable"
git push
```

## AI Agent Prompt

Copy/paste when white screen happens:

> Investigate Lovable white screen. Prioritize build-chain errors over UI bugs. If console shows `[plugin:vite:css] [postcss] Cannot find package 'postcss'`, treat as dependency/install issue. Verify root package.json has postcss, tailwindcss, autoprefixer (and for Tailwind v4 also @tailwindcss/postcss) available to the preview environment (often requires placing them in dependencies, not only devDependencies). Ensure lockfile updated. Ensure only one PostCSS config is used by the Vite entry actually running in Lovable (remove duplicates under apps/* if root Vite runs). Confirm no Tailwind CDN script exists. Validate fix by opening latest commit "See Preview" and confirming overlay is gone and Tailwind styles apply.
