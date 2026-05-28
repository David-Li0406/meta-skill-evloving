---
name: npm-package-manager
description: Manage npm packages in the LucidData Next.js project. Use when adding, removing, or updating package dependencies, checking for outdated packages, auditing for vulnerabilities, or resolving dependency conflicts. Follows LucidData conventions for dependency management and version pinning strategies.
license: MIT
compatibility: Designed for Claude Code and GitHub Copilot. Requires Node.js 18+ and npm 9+ installed. Works with package.json and package-lock.json in project root.
metadata:
  author: LucidData Team
  version: "1.0"
  package_manager: npm
  node_version: "18+"
allowed-tools: Bash(npm:*) Bash(npx:*) Read Write Edit
---

# npm Package Manager

Comprehensive dependency management skill for the LucidData Next.js application using npm as the package manager.

## Overview

This skill provides workflows for managing Node.js packages in the LucidData project, following best practices for version pinning, security auditing, and Prisma-specific operations. It ensures consistent dependency management across development and production environments.

## When to Use This Skill

Activate this skill when you need to:

- **Install packages**: Add new dependencies or dev dependencies
- **Remove packages**: Uninstall packages and clean up dependencies
- **Update packages**: Update specific packages or check for outdated versions
- **Security audit**: Check for vulnerabilities and apply security fixes
- **Prisma operations**: Run Prisma commands with environment configuration
- **Troubleshoot**: Resolve dependency conflicts, lockfile issues, or installation errors
- **Verify packages**: Check if a package exists on npm registry before installing

## Core Rules

⚠️ **CRITICAL: Always follow these rules when managing packages**

1. **Never manually edit dependencies in package.json** - Always use `npm install` or `npm uninstall` commands
2. **Always commit package-lock.json** - The lockfile ensures consistent installations across environments
3. **Run `npm audit` after installing new packages** - Check for security vulnerabilities
4. **Verify package exists on npm registry** - Use the verify-package script or check npmjs.com before installing
5. **Use exact versions for security-critical packages** - Crypto, auth, and database packages should use exact versions (`1.2.3` not `^1.2.3`)

## LucidData Version Pinning Strategy

### Exact Versions (no caret `^`)

Use exact versions for packages where stability and security are critical:

```json
{
  "dependencies": {
    "@prisma/client": "6.19.1",
    "prisma": "6.19.1",
    "@supabase/supabase-js": "2.70.5",
    "@supabase/ssr": "0.5.2"
  }
}
```

**When to use exact versions:**
- Database clients (@prisma/client, prisma)
- Authentication libraries (@supabase/supabase-js, @supabase/ssr)
- Security-critical packages (future: encryption, auth tokens)

### Caret Versions (with `^`)

Use caret versions for packages where minor/patch updates are safe:

```json
{
  "dependencies": {
    "next": "^15.1.3",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@radix-ui/react-dialog": "^1.1.4",
    "tailwindcss": "^3.4.1",
    "lucide-react": "^0.562.0"
  },
  "devDependencies": {
    "@playwright/test": "^1.57.0",
    "vitest": "^3.2.4",
    "prettier": "^3.7.4",
    "eslint": "^9"
  }
}
```

**When to use caret versions:**
- UI component libraries (Radix UI, shadcn/ui)
- Development tools (ESLint, Prettier, TypeScript)
- Testing frameworks (Playwright, Vitest)
- Build tools (PostCSS, Autoprefixer)

### Avoid

- **Tilde (`~`) ranges**: Less predictable than caret
- **Wildcard (`*`) or `latest`**: Breaks builds when breaking changes are released
- **Version ranges (`1.0.0 - 2.0.0`)**: Too permissive

## Common Workflows

### Installing a New Package

```bash
# Production dependency
npm install <package-name>

# Development dependency
npm install --save-dev <package-name>

# Specific version
npm install <package-name>@<version>

# Exact version (recommended for security packages)
npm install --save-exact <package-name>@<version>
```

**Example:**
```bash
# Install date-fns for date formatting
npm install date-fns

# Install as exact version
npm install --save-exact @supabase/supabase-js@2.70.5

# Install dev dependency
npm install --save-dev @types/node
```

**After installation:**
1. Verify package.json and package-lock.json were updated
2. Run `npm audit` to check for vulnerabilities
3. Test the application (`npm run dev`)
4. Commit both package.json and package-lock.json

### Removing a Package

```bash
# Uninstall package
npm uninstall <package-name>

# Uninstall dev dependency
npm uninstall --save-dev <package-name>
```

**Example:**
```bash
# Remove unused package
npm uninstall lodash

# Remove dev dependency
npm uninstall --save-dev unused-tool
```

**After uninstalling:**
1. Verify package.json and package-lock.json were updated
2. Remove any imports/references to the package in code
3. Test the application
4. Commit both files

### Updating Packages

**Update specific package:**
```bash
npm update <package-name>
```

**Update all packages (use with caution):**
```bash
npm update
```

**Update to specific version:**
```bash
# Edit package.json to desired version, then:
npm install
```

**Example - Updating Prisma:**
```bash
# Check current versions
npm list @prisma/client prisma

# Update both packages to same version (CRITICAL: keep synchronized)
npm install @prisma/client@6.20.0 prisma@6.20.0

# Generate Prisma client after update
npx prisma generate
```

**After updating:**
1. Review CHANGELOG for breaking changes
2. Run tests (`npm run test:run`)
3. Test E2E flows (`npm run test:e2e`)
4. Commit package.json and package-lock.json

### Checking for Outdated Packages

```bash
# List outdated packages
npm outdated

# Output shows:
# Package         Current  Wanted  Latest  Location
# next            15.1.3   15.1.4  15.1.4  node_modules/next
# @prisma/client  6.19.1   6.19.1  6.20.0  node_modules/@prisma/client
```

**Interpreting output:**
- **Current**: Version currently installed
- **Wanted**: Maximum version that satisfies semver in package.json
- **Latest**: Latest version available on npm

**Decision matrix:**
- Patch updates (6.19.1 → 6.19.2): Usually safe, update when convenient
- Minor updates (6.19.1 → 6.20.0): Review changelog, test thoroughly
- Major updates (6.x.x → 7.0.0): Review breaking changes, plan migration

### Security Auditing

```bash
# Check for vulnerabilities
npm audit

# Show detailed report
npm audit --json

# Auto-fix vulnerabilities (updates package-lock.json)
npm audit fix

# Fix including breaking changes (use with caution)
npm audit fix --force
```

**Example output:**
```
found 3 vulnerabilities (1 moderate, 2 high)
  run `npm audit fix` to fix 2 of them.
  1 vulnerability requires manual review.
```

**Handling vulnerabilities:**
1. Review the audit report
2. Check if vulnerable package is direct or transitive dependency
3. If direct: Update to patched version
4. If transitive: Update parent package or wait for upstream fix
5. If no fix available: Assess risk and consider alternatives

**After audit fix:**
1. Test application thoroughly
2. Commit package-lock.json (and package.json if versions changed)

### Prisma-Specific Commands

LucidData uses Prisma with environment-specific configuration. Always use `npx dotenv` to load the correct `.env` file:

```bash
# Generate Prisma client
npx dotenv -e .env.local -- npx prisma generate

# Create migration
npx dotenv -e .env.local -- npx prisma migrate dev --name migration_name

# Deploy migrations
npx dotenv -e .env.local -- npx prisma migrate deploy

# Open Prisma Studio
npx dotenv -e .env.local -- npx prisma studio

# Reset database (CAUTION: deletes all data)
npx dotenv -e .env.local -- npx prisma migrate reset

# Seed database
npx dotenv -e .env.local -- npx prisma db seed
```

**Why use `npx dotenv`?**
Prisma needs database connection string from `.env.local`, but doesn't load it by default. The `dotenv-cli` package loads environment variables before running Prisma commands.

### Verifying Package Exists

Before installing a package, verify it exists on npm registry:

**Method 1: Use verify-package script**
```bash
node .claude/skills/npm-package-manager/scripts/verify-package.js <package-name> [version]
```

**Method 2: Manual check**
```bash
npm view <package-name>
npm view <package-name> versions
npm view <package-name>@<version>
```

**Example:**
```bash
# Check if package exists
npm view date-fns

# Check specific version
npm view date-fns@3.0.0

# List all versions
npm view date-fns versions
```

## LucidData-Specific Package Categories

### Core Framework (conservative updates)

```json
{
  "next": "^15.1.3",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "typescript": "^5"
}
```

**Update strategy**: Wait 1-2 weeks after major releases, review Next.js upgrade guide

### Database & ORM (synchronized exact versions)

```json
{
  "@prisma/client": "6.19.1",
  "prisma": "6.19.1"
}
```

**Update strategy**: Keep @prisma/client and prisma versions identical, run `npx prisma generate` after update

### Authentication (exact versions for stability)

```json
{
  "@supabase/supabase-js": "2.70.5",
  "@supabase/ssr": "0.5.2"
}
```

**Update strategy**: Test auth flows thoroughly after updates (signup, login, logout, protected routes)

### UI Components (frequent updates OK)

```json
{
  "@radix-ui/react-dialog": "^1.1.4",
  "@radix-ui/react-label": "^2.1.2",
  "tailwindcss": "^3.4.1",
  "lucide-react": "^0.562.0"
}
```

**Update strategy**: Update regularly for bug fixes and new features, test UI components

### Testing (minor updates OK)

```json
{
  "vitest": "^3.2.4",
  "@playwright/test": "^1.57.0",
  "@testing-library/react": "^16.3.1"
}
```

**Update strategy**: Update when new features are needed, ensure tests still pass after update

### Build Tools (cautious updates)

```json
{
  "eslint": "^9",
  "prettier": "^3.7.4",
  "postcss": "^8",
  "autoprefixer": "^10.4.20"
}
```

**Update strategy**: Update for security patches, be cautious with ESLint major versions (config changes)

## Troubleshooting

### Issue: `npm install` fails with dependency conflict

**Error:**
```
npm ERR! ERESOLVE unable to resolve dependency tree
npm ERR! Found: react@19.0.0
npm ERR! Could not resolve dependency: peer react@"^18.0.0" required by some-package
```

**Solution:**
1. Check if package supports React 19
2. If yes, wait for package update or use `--legacy-peer-deps` flag
3. If no, find alternative package

```bash
npm install --legacy-peer-deps
```

See [Troubleshooting Reference](references/troubleshooting.md) for more solutions.

### Issue: package-lock.json conflicts in git

**Solution:**
```bash
# Accept incoming changes
git checkout --theirs package-lock.json
npm install

# Or regenerate lockfile
rm package-lock.json
npm install
```

### Issue: `npm audit` shows high vulnerability in transitive dependency

**Solution:**
1. Check if parent package has update that fixes it
2. If not, check if vulnerability affects LucidData's usage
3. Consider using `npm audit fix --force` or wait for upstream fix
4. Document decision in issue if accepting risk

## Best Practices

1. **One package at a time**: Install/update one package at a time for easier troubleshooting
2. **Test after changes**: Run `npm run dev` and verify app works after package changes
3. **Read changelogs**: Review CHANGELOG.md or release notes before updating
4. **Commit atomically**: Commit package.json and package-lock.json together
5. **Use npm scripts**: Prefer npm scripts in package.json over global commands
6. **Clean installs**: Periodically delete node_modules and reinstall for consistency
7. **Check bundle size**: Use `npm run build` to check if new packages bloat bundle

## npm Scripts in LucidData

Available scripts in package.json:

```bash
# Development
npm run dev                 # Start Next.js dev server
npm run build              # Build for production
npm run start              # Start production server

# Testing
npm run test               # Run Vitest in watch mode
npm run test:run           # Run Vitest once
npm run test:coverage      # Generate coverage report
npm run test:e2e           # Run Playwright E2E tests
npm run test:all           # Run all tests

# Code Quality
npm run lint               # Run ESLint
npm run format             # Run Prettier

# Database
npm run db:generate        # Generate Prisma client
npm run db:migrate         # Run migrations
npm run db:studio          # Open Prisma Studio
npm run db:seed            # Seed database
```

## References

For more detailed information, see:

- [Package Operations](references/package-operations.md) - Detailed command examples and workflows
- [Troubleshooting](references/troubleshooting.md) - Common errors and solutions

## Verify Package Script

For convenience, use the [verify-package.js](scripts/verify-package.js) script to check if a package exists before installing:

```bash
node .claude/skills/npm-package-manager/scripts/verify-package.js date-fns
node .claude/skills/npm-package-manager/scripts/verify-package.js @prisma/client 6.20.0
```

## Quick Reference

| Task | Command | Notes |
|------|---------|-------|
| Install package | `npm install <package>` | Adds to dependencies |
| Install dev dependency | `npm install --save-dev <package>` | Adds to devDependencies |
| Install exact version | `npm install --save-exact <package>@<version>` | No caret in package.json |
| Uninstall package | `npm uninstall <package>` | Removes from package.json |
| Update package | `npm update <package>` | Updates within semver range |
| Check outdated | `npm outdated` | Lists packages with updates |
| Security audit | `npm audit` | Check vulnerabilities |
| Auto-fix vulnerabilities | `npm audit fix` | Updates package-lock.json |
| Verify package exists | `npm view <package>` | Check npm registry |
| List installed versions | `npm list <package>` | Show dependency tree |
| Clean install | `rm -rf node_modules package-lock.json && npm install` | Fresh installation |

---

**Version**: 1.0
**Last Updated**: 2026-01-13
**Maintained by**: LucidData Team
