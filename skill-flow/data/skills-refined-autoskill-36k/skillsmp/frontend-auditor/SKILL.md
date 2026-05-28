---
name: frontend-auditor
description: Audit frontend code for security, UX regressions, performance, and accessibility issues. Use when reviewing React, Next.js, Vue, Svelte, or any frontend code changes. Triggers on "audit frontend", "review UI", "check accessibility", "a11y audit", "frontend security", "UX review", "performance audit", "review components", "audit React".
---

# Frontend Auditor

Comprehensive auditor for frontend code focusing on security, correctness, UX regressions, performance, accessibility, and maintainability. All findings are grounded in actual code, components, routes, and state management patterns.

## When to Use

- Reviewing frontend code changes before merge
- Auditing React/Next/Vue/Svelte components
- Checking accessibility compliance
- Performance auditing UI code
- Security review of client-side code
- UX regression testing after changes

## Audit Workflow

On EVERY invocation, execute these steps in order:

### Step 1: Detect Stack & Layout

Identify the frontend technology stack:

```
- Framework: React/Next.js/Vue/Svelte/Angular/etc.
- Router: React Router/Next.js App Router/Vue Router/etc.
- State management: Redux/Zustand/Jotai/Pinia/Context/etc.
- Styling: Tailwind/CSS Modules/Styled Components/Emotion/etc.
- Build tool: Vite/Webpack/Turbopack/etc.
- API layer: fetch/axios/React Query/SWR/tRPC/etc.
```

Identify key locations:
- App entrypoints (`main.tsx`, `App.tsx`, `_app.tsx`)
- Pages/routes directory structure
- Shared components library
- API client layer and hooks

### Step 2: Scan Recent Changes

Review what has changed recently:

```bash
# Check working directory changes
git status
git diff --stat

# Review recent commits affecting frontend
git log --oneline -20 --all -- "src/" "app/" "pages/" "components/" "lib/"
```

Summarize:
- What UI/behavior changes were introduced?
- What components/routes were modified?
- What possible regressions could occur?

### Step 3: Build UI Map

Create a map of the touched areas:

| Component | Details |
|-----------|---------|
| **Routes/Screens** | Pages affected, navigation flows |
| **Components** | UI components modified |
| **Data Fetching** | API calls, queries, mutations |
| **Forms** | Form handling, validation |
| **State** | Local/global state changes |

### Step 4: Execute Audit Checklist

Audit touched components plus critical paths (auth flows, payments, user data display).

See [CHECKLIST.md](CHECKLIST.md) for the complete audit checklist covering:
- Security (XSS, token storage, secrets leakage)
- Correctness & UX (loading states, validation, edge cases)
- Performance (bundle size, re-renders, network)
- Accessibility (keyboard nav, ARIA, contrast)
- Maintainability (types, tests, component design)

## Output Format

Structure your audit report as follows:

### A) Scope Scanned
```
Framework: [detected stack]
Routes reviewed: [list routes/pages]
Components analyzed: [count]
Commits analyzed: [range]
```

### B) UI Map
```
Routes: [list affected routes]
Components: [key components modified]
Data flows: [API integrations touched]
State: [state management affected]
```

### C) Findings by Category

Use severity levels:

| Severity | Icon | Meaning |
|----------|------|---------|
| CRITICAL | :red_circle: | XSS, auth bypass, data exposure |
| HIGH | :orange_circle: | Security issue, major UX regression |
| MEDIUM | :yellow_circle: | Performance issue, a11y problem |
| LOW | :white_circle: | Minor issue, code smell |
| INFO | :blue_circle: | Observation, suggestion |

For each finding:
```
### [SEVERITY] Title

**Location:** `components/Form.tsx:45`
**Category:** Security > XSS

**Issue:** [Describe the problem]

**Evidence:**
[Code snippet]

**Risk:** [What could go wrong]

**Fix:**
[Code showing the fix]
```

### D) Summary Table

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Security | 0 | 1 | 0 | 1 |
| UX/Correctness | 0 | 0 | 2 | 1 |
| Performance | 0 | 0 | 1 | 2 |
| Accessibility | 0 | 1 | 1 | 0 |
| Maintainability | 0 | 0 | 0 | 2 |

### E) Suggested Patches

Step-by-step fixes for critical and high-severity issues:

```
1. [First fix with code]
2. [Second fix with code]
3. ...
```

## Quick Commands

```bash
# Check for vulnerable dependencies
npm audit
pnpm audit

# Find potential XSS vectors (React)
grep -rn "dangerouslySetInnerHTML\|innerHTML" --include="*.tsx" --include="*.jsx"

# Find hardcoded secrets
grep -rn "API_KEY\|SECRET\|password" --include="*.ts" --include="*.tsx"

# Check bundle size
npx vite-bundle-visualizer
npx @next/bundle-analyzer

# Lighthouse audit
npx lighthouse http://localhost:3000 --view
```

## Resources

- [CHECKLIST.md](CHECKLIST.md) - Complete audit checklist
- [PATTERNS.md](PATTERNS.md) - Framework-specific vulnerability patterns
