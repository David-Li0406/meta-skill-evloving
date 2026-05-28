---
name: agentic-jumpstart-dependency-management
description: Dependency management best practices for npm projects with 40+ dependencies. Use when adding packages, updating dependencies, resolving conflicts, or when the user mentions npm, packages, dependencies, versions, or updates.
---

# Dependency Management

## Package Installation

### Adding Dependencies

```bash
# Production dependency
npm install package-name

# Development dependency
npm install -D package-name

# Specific version
npm install package-name@1.2.3

# Latest version
npm install package-name@latest
```

### When to Use devDependencies

```json
{
  "dependencies": {
    // Runtime code - ships to production
    "react": "^19.1.0",
    "drizzle-orm": "^0.44.3",
    "stripe": "^18.3.0"
  },
  "devDependencies": {
    // Build/test tools - not in production bundle
    "@playwright/test": "^1.54.2",
    "typescript": "^5.8.3",
    "vitest": "^3.2.4",
    "@types/react": "^19.1.8"
  }
}
```

## Version Ranges

### Semver Notation

```json
{
  "dependencies": {
    // Exact version - use sparingly
    "critical-lib": "1.2.3",

    // Patch updates only (1.2.x)
    "stable-lib": "~1.2.3",

    // Minor updates (1.x.x) - recommended for most
    "flexible-lib": "^1.2.3",

    // Any version - avoid in production
    "any-lib": "*"
  }
}
```

### Recommended Approach

Use `^` (caret) for most dependencies to get bug fixes and minor improvements:

```json
{
  "react": "^19.1.0",       // Will update to 19.x.x
  "typescript": "^5.8.3"    // Will update to 5.x.x
}
```

## Updating Dependencies

### Check for Updates

```bash
# Check outdated packages
npm outdated

# Interactive update tool
npx npm-check-updates -i
```

### Safe Update Process

1. **Review changelogs** for breaking changes
2. **Update in stages** - don't update everything at once
3. **Run tests** after each update
4. **Commit separately** for easy rollback

```bash
# Update single package
npm update package-name

# Update all (respecting semver ranges)
npm update

# Update to latest (may include breaking changes)
npm install package-name@latest
```

## Lock File Management

### package-lock.json

- **Always commit** the lock file
- **Don't manually edit** - let npm manage it
- **Use `npm ci`** in CI/CD for reproducible builds

```bash
# Clean install from lock file (CI/CD)
npm ci

# Install and update lock file (development)
npm install
```

## Security Updates

### Audit Dependencies

```bash
# Check for vulnerabilities
npm audit

# Fix automatically where possible
npm audit fix

# Force fix (may include breaking changes)
npm audit fix --force
```

### Regular Maintenance

- Run `npm audit` weekly
- Update security patches immediately
- Review and update major versions monthly

## Common Dependencies in This Project

### Core Framework

```json
{
  "@tanstack/react-start": "^1.143.3",
  "@tanstack/react-router": "^1.143.3",
  "@tanstack/react-query": "^5.83.0",
  "react": "^19.1.0",
  "react-dom": "^19.1.0"
}
```

### Database

```json
{
  "drizzle-orm": "^0.44.3",
  "pg": "^8.16.3",
  "drizzle-kit": "^0.31.4"  // devDependency
}
```

### UI Components

```json
{
  "@radix-ui/react-dialog": "^1.1.14",
  "@radix-ui/react-dropdown-menu": "^2.1.15",
  "tailwindcss": "^4.1.11",
  "lucide-react": "^0.528.0",
  "class-variance-authority": "^0.7.1"
}
```

### Forms & Validation

```json
{
  "react-hook-form": "^7.62.0",
  "@hookform/resolvers": "^5.2.1",
  "zod": "^4.0.10"
}
```

### Payments & Auth

```json
{
  "stripe": "^18.3.0",
  "@stripe/stripe-js": "^7.6.1",
  "arctic": "^3.7.0"
}
```

### Testing

```json
{
  "@playwright/test": "^1.54.2",
  "vitest": "^3.2.4",
  "@vitest/coverage-v8": "^3.2.4"
}
```

## Peer Dependencies

Some packages require specific peer dependencies:

```bash
# Check peer dependency warnings
npm install

# Install missing peer dependencies
npm install react@19 react-dom@19
```

### Radix UI Peer Dependencies

Radix components require React as a peer:

```json
{
  "peerDependencies": {
    "react": "^16.8 || ^17 || ^18 || ^19",
    "react-dom": "^16.8 || ^17 || ^18 || ^19"
  }
}
```

## Troubleshooting

### Dependency Conflicts

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Force resolution
npm install --force

# Check why a package is installed
npm explain package-name
```

### Version Mismatches

```bash
# List all installed versions
npm ls package-name

# Deduplicate
npm dedupe
```

## Import Optimization

### Tree-Shaking Friendly Imports

```typescript
// GOOD: Import specific items (tree-shakeable)
import { Button } from "~/components/ui/button";
import { eq, and } from "drizzle-orm";

// AVOID: Barrel imports of large libraries
// import * as RadixUI from "@radix-ui/react-primitives";
```

### Dynamic Imports for Large Libraries

```typescript
// Lazy load heavy dependencies
const marked = await import("marked");
const { OpenAI } = await import("openai");
```

## Dependency Checklist

- [ ] Lock file is committed to git
- [ ] `npm audit` shows no high/critical vulnerabilities
- [ ] DevDependencies are correctly categorized
- [ ] No `*` version ranges in production
- [ ] Peer dependencies are satisfied
- [ ] Tree-shaking friendly imports used
- [ ] Large libraries lazy-loaded where possible
- [ ] Regular updates scheduled (monthly)
- [ ] Breaking changes reviewed before major updates
- [ ] CI uses `npm ci` for reproducible builds
