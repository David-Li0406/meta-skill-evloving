---
name: nextjs-development-best-practices
description: Use this skill when developing applications with Next.js, focusing on best practices for App Router, Server Components, data fetching, and performance optimization.
---

# Next.js Development Best Practices

## 📋 Overview

This skill covers best practices for developing applications using Next.js, particularly with the App Router. It includes guidance on Server Components, data fetching strategies, caching, and deployment.

## Key Principles

- Use Server Components by default; only use 'use client' when necessary.
- Perform data fetching within Server Components using async/await.
- Prioritize mutations with Server Actions.
- Optimize performance using features like Suspense, revalidatePath, and caching strategies.

## Workflow Steps

### 1. Investigation (Pre-implementation)

Before implementing changes, conduct an investigation to understand the existing code structure:

```bash
# Check existing structure
find app -name "*.tsx" | head -20

# Check usage of Client Components
grep -r "use client" app/ --include="*.tsx"

# List existing UI components
ls src/components/ui/

# Check versions in package.json
cat package.json | grep -E "next|react"
```

### 2. Implementation

- Follow existing patterns based on the investigation results.
- Reuse existing UI components where possible.
- Minimize changes to the existing codebase.

### 3. Validation (Mandatory)

After implementation, validate the changes with the following commands:

```bash
# Static analysis
npm run type-check
npm run lint

# Build confirmation
npm run build

# Development server check
npm run dev
```

### 4. Browser Verification (Using Playwright)

- Access the relevant page in the browser.
- Ensure there are no console errors.
- Verify intended display and functionality.
- Check responsiveness by switching viewports.

## Reporting Format

When reporting your implementation, use the following format:

```
## Next.js Implementation Report

### Investigation Results
- Existing Patterns: Server/Client ratio, used components
- package.json Version: next@X.X.X

### Changes Made
- File: Summary of changes

### Validation Results
- Type-check: OK/NG
- Lint: OK/NG
- Build: OK/NG
- Browser Check: OK/NG (URL, verification items)
```

## 📚 Official Documentation and Resources

- **[Next.js Documentation](https://nextjs.org/docs)** - Official documentation for Next.js.
- **[Next.js Learn](https://nextjs.org/learn)** - Interactive learning courses and step-by-step project building.
- **[Vercel Documentation](https://vercel.com/docs)** - Documentation for the deployment platform.
- **[Next.js Examples](https://github.com/vercel/next.js/tree/canary/examples)** - A collection of official examples.
- **[Awesome Next.js](https://github.com/unicodeveloper/awesome-nextjs)** - A curated list of libraries and plugins for Next.js.
- **[Next.js Conf](https://nextjs.org/conf)** - Videos from the annual conference.