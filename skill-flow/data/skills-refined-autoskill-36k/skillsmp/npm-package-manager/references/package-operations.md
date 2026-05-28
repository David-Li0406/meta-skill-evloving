# Package Operations - Detailed Guide

Comprehensive reference for npm package management operations in LucidData.

## Installation Operations

### Basic Installation

```bash
# Install production dependency
npm install <package-name>

# Install and save exact version
npm install --save-exact <package-name>

# Install specific version
npm install <package-name>@1.2.3

# Install latest version (use with caution)
npm install <package-name>@latest

# Install from GitHub
npm install user/repo

# Install from local directory
npm install ../local-package
```

### Development Dependencies

```bash
# Install dev dependency
npm install --save-dev <package-name>

# Install multiple dev dependencies
npm install --save-dev prettier eslint @types/node

# Install global package (avoid when possible)
npm install -g <package-name>
```

### Example: Adding UI Component Library

```bash
# Install Radix UI dialog component
npm install @radix-ui/react-dialog

# Verify installation
npm list @radix-ui/react-dialog

# Expected output in package.json:
# "@radix-ui/react-dialog": "^1.1.4"
```

### Example: Adding Type Definitions

```bash
# Install type definitions for Node.js
npm install --save-dev @types/node

# Install type definitions for React
npm install --save-dev @types/react @types/react-dom
```

## Uninstallation Operations

### Removing Packages

```bash
# Uninstall production dependency
npm uninstall <package-name>

# Uninstall dev dependency
npm uninstall --save-dev <package-name>

# Uninstall global package
npm uninstall -g <package-name>

# Uninstall multiple packages
npm uninstall package1 package2 package3
```

### Cleanup After Uninstall

```bash
# Remove package
npm uninstall unused-package

# Remove unused dependencies (prune)
npm prune

# Clean npm cache
npm cache clean --force
```

### Example: Removing Unused Package

```bash
# Uninstall lodash
npm uninstall lodash

# Verify removal
npm list lodash
# Should show: npm ERR! (package not found)

# Check package.json and package-lock.json were updated
git diff package.json package-lock.json
```

## Update Operations

### Updating Specific Packages

```bash
# Update to latest version within semver range
npm update <package-name>

# Update to specific version
npm install <package-name>@<version>

# Update all packages (caution: may break things)
npm update

# Update global package
npm update -g <package-name>
```

### Checking for Updates

```bash
# List outdated packages
npm outdated

# Check specific package
npm outdated <package-name>

# Show detailed information
npm outdated --long

# Output as JSON
npm outdated --json
```

### Example: Updating Next.js

```bash
# Check current version
npm list next

# Check available updates
npm outdated next

# Update to latest minor/patch version
npm update next

# Or update to specific version
npm install next@15.1.4

# Test the application
npm run dev
npm run build
npm run test:run

# If successful, commit changes
git add package.json package-lock.json
git commit -m "chore: update Next.js to 15.1.4"
```

### Example: Synchronized Prisma Update

```bash
# CRITICAL: Update both @prisma/client and prisma together
npm install @prisma/client@6.20.0 prisma@6.20.0

# Verify both are same version
npm list @prisma/client prisma

# Generate Prisma client
npx dotenv -e .env.local -- npx prisma generate

# Test database connection
npm run dev
# Navigate to app and verify data loads correctly

# Commit changes
git add package.json package-lock.json prisma/migrations/
git commit -m "chore: update Prisma to 6.20.0"
```

## Security Operations

### Auditing for Vulnerabilities

```bash
# Run security audit
npm audit

# Show audit as JSON
npm audit --json

# Audit production dependencies only
npm audit --production

# Audit only high/critical vulnerabilities
npm audit --audit-level=high
```

### Fixing Vulnerabilities

```bash
# Automatically fix vulnerabilities
npm audit fix

# Fix including semver-major changes (caution)
npm audit fix --force

# Dry run (show what would be fixed)
npm audit fix --dry-run

# Force install after manual package.json edits
npm install
```

### Example: Handling Security Alert

**Scenario:** npm audit shows high vulnerability in `axios@0.21.1`

```bash
# Run audit
npm audit

# Output:
# High: Server-Side Request Forgery in axios
# Package: axios
# Patched in: >=0.21.2
# Dependency of: some-package
# Path: some-package > axios

# Check if direct or transitive dependency
npm list axios

# If direct dependency, update:
npm install axios@latest

# If transitive, update parent package:
npm update some-package

# Verify fix
npm audit

# Commit fix
git add package.json package-lock.json
git commit -m "security: update axios to fix SSRF vulnerability"
```

## Information Commands

### Package Information

```bash
# View package information
npm view <package-name>

# View specific field
npm view <package-name> version
npm view <package-name> description
npm view <package-name> dependencies

# View all versions
npm view <package-name> versions

# View latest version
npm view <package-name> dist-tags.latest

# View package on npm website
npm home <package-name>

# View package repository
npm repo <package-name>

# View package bugs/issues
npm bugs <package-name>
```

### Installed Packages

```bash
# List installed packages
npm list

# List top-level packages only
npm list --depth=0

# List specific package
npm list <package-name>

# List global packages
npm list -g --depth=0

# List with package.json info
npm list --json

# Find duplicate packages
npm dedupe
```

### Example: Investigating Package

```bash
# View package info
npm view date-fns

# Output shows:
# date-fns@3.6.0 | MIT | deps: none | versions: 300
# Modern JavaScript date utility library

# Check available versions
npm view date-fns versions

# Check latest version
npm view date-fns dist-tags.latest

# View on npm website
npm home date-fns
```

## Cache Operations

### Managing npm Cache

```bash
# Verify cache integrity
npm cache verify

# Clean cache (use when troubleshooting)
npm cache clean --force

# View cache location
npm config get cache

# View cache contents
npm cache ls
```

### When to Clean Cache

- Installation errors that persist
- Corrupted downloads
- Switching npm versions
- Freeing disk space

**Note:** npm automatically manages cache; manual cleaning rarely needed.

## Lock File Operations

### Working with package-lock.json

```bash
# Generate lockfile
npm install

# Update lockfile without installing
npm install --package-lock-only

# Install from lockfile (CI/production)
npm ci

# Force regenerate lockfile
rm package-lock.json
npm install
```

### Resolving Lock File Conflicts

**Scenario:** Git merge conflict in package-lock.json

```bash
# Option 1: Accept one version and regenerate
git checkout --ours package-lock.json   # or --theirs
npm install

# Option 2: Delete and regenerate
rm package-lock.json
npm install

# Option 3: Use npm merge tool (npm 8.5+)
npm install --lockfile-version=2
```

## Configuration

### Viewing npm Configuration

```bash
# View all config
npm config list

# View specific config
npm config get registry
npm config get prefix

# View global config location
npm config get globalconfig

# View user config location
npm config get userconfig
```

### Common Configurations

```bash
# Set registry (use default)
npm config set registry https://registry.npmjs.org/

# Set init defaults
npm config set init.author.name "Your Name"
npm config set init.author.email "you@example.com"
npm config set init.license "MIT"

# Save exact versions by default
npm config set save-exact true

# Disable package-lock.json (not recommended)
npm config set package-lock false
```

## CI/Production Best Practices

### Clean Installation (CI)

```bash
# Install from lockfile (exact versions)
npm ci

# Benefits:
# - Faster than npm install
# - Requires package-lock.json
# - Removes node_modules before install
# - Fails if package.json and lockfile are out of sync
```

### Production Installation

```bash
# Install only production dependencies
npm install --production

# Or set NODE_ENV
NODE_ENV=production npm install

# Skip dev dependencies
npm install --omit=dev
```

## LucidData-Specific Workflows

### Adding shadcn/ui Component

```bash
# Use shadcn CLI (recommended)
npx shadcn@latest add button

# Or manually install Radix UI primitive
npm install @radix-ui/react-primitive-name

# Example: Add Tooltip component
npx shadcn@latest add tooltip

# Verify component added to components/ui/
ls components/ui/tooltip.tsx
```

### Updating TanStack Query

```bash
# Check current version
npm list @tanstack/react-query

# Update to latest v5.x
npm update @tanstack/react-query

# Update devtools too (keep versions aligned)
npm update @tanstack/react-query-devtools

# Verify versions match
npm list @tanstack/react-query @tanstack/react-query-devtools

# Test queries and mutations
npm run test:run
```

### Adding Testing Library

```bash
# Install React Testing Library
npm install --save-dev @testing-library/react

# Install user-event for interactions
npm install --save-dev @testing-library/user-event

# Install jest-dom for matchers
npm install --save-dev @testing-library/jest-dom

# Verify in test setup (test/setup.ts)
# import '@testing-library/jest-dom/vitest'
```

## Performance Tips

### Faster Installations

```bash
# Use npm ci in CI/CD (faster, stricter)
npm ci

# Use --prefer-offline to use cache
npm install --prefer-offline

# Use --no-audit to skip security audit (not recommended)
npm install --no-audit

# Use --no-fund to skip funding messages
npm install --no-fund
```

### Reducing Install Time

1. Keep dependencies minimal (remove unused packages)
2. Use npm ci in CI/CD instead of npm install
3. Cache node_modules in CI/CD pipeline
4. Use npm v7+ for better performance
5. Consider using pnpm or yarn if team agrees (requires migration)

## Comparing Package Managers

| Feature | npm | pnpm | yarn |
|---------|-----|------|------|
| Speed | Moderate | Fast | Fast |
| Disk usage | High | Low (hard links) | Moderate |
| Monorepo support | Workspaces | Workspaces | Workspaces |
| Lock file | package-lock.json | pnpm-lock.yaml | yarn.lock |
| LucidData status | **Current** | Not used | Not used |

**Note:** LucidData uses npm. Changing package managers requires team consensus and migration plan.

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Installation fails | `rm -rf node_modules package-lock.json && npm install` |
| Peer dependency warning | Add `--legacy-peer-deps` flag |
| Lock file conflict | Delete lockfile, run `npm install` |
| Corrupted cache | `npm cache clean --force` |
| Global package not found | Check `npm config get prefix` and add to PATH |
| Permission errors (Linux/Mac) | Use nvm to install Node.js (avoid sudo) |
| Slow installation | Use `npm ci` or `--prefer-offline` |
| Wrong Node version | Use nvm: `nvm use 18` |

---

**For more information:**
- [npm Documentation](https://docs.npmjs.com/)
- [Troubleshooting Reference](troubleshooting.md)
- [Main Skill Documentation](../SKILL.md)
