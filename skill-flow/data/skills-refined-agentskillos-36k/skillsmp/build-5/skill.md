---
name: build
description: Build, type-check, and lint the project
allowed-tools: [Bash, Read]
---

## Purpose
Run build, type checking, and linting to ensure code quality before committing or deploying.

## Commands

### 1. Development
```bash
# Start development server
npm run dev

# Development server runs on http://localhost:3000
# Hot reload enabled
```

### 2. Type Checking
```bash
# Type check with TypeScript compiler
npx tsc --noEmit

# Shows all TypeScript errors without emitting files
```

### 3. Linting
```bash
# Check code with Biome
npm run lint

# Auto-fix issues
npm run format
```

### 4. Production Build
```bash
# Build for production
npm run build

# Build output goes to .next/ directory
# This command:
# - Compiles TypeScript
# - Optimizes React components
# - Generates static pages
# - Bundles JavaScript/CSS
```

### 5. Start Production Server
```bash
# Start production server (after build)
npm start
```

## Common Issues and Fixes

### TypeScript Errors
```bash
# Check specific file
npx tsc --noEmit src/app/page.tsx

# Common fixes:
# - Add missing types
# - Check import paths (@/ alias)
# - Verify interface implementations
```

### Build Failures
```bash
# Clean cache and rebuild
rm -rf .next node_modules/.cache
npm run build

# Check for:
# - Missing dependencies
# - Import cycles
# - Server/client component issues
```

### Linting Errors
```bash
# Show all issues
npm run lint

# Auto-fix formatting
npm run format

# Common Biome rules:
# - No unused variables
# - Consistent quotes
# - Proper spacing
```

## Pre-Commit Checklist

Run these commands before committing:

```bash
# 1. Format code
npm run format

# 2. Check linting
npm run lint

# 3. Type check
npx tsc --noEmit

# 4. Build to catch production issues
npm run build

# If all pass, you're good to commit!
```

## CI/CD Integration

For GitHub Actions or similar:
```yaml
- name: Install dependencies
  run: npm ci

- name: Lint
  run: npm run lint

- name: Type check
  run: npx tsc --noEmit

- name: Build
  run: npm run build
```

## Performance Tips

```bash
# Analyze bundle size
npm run build
# Check .next/analyze output

# Check for:
# - Large dependencies
# - Duplicate packages
# - Unnecessary imports
```

## Database Migrations Before Build

If you have pending migrations:
```bash
# Initialize schema
npm run init:schema

# Run specific migration
npm run migrate:auth

# Check database
npm run check:db
```

## Environment Variables

Required for build:
```bash
# .env.local
DATABASE_URL=data/learning-cards.db
NEXTAUTH_SECRET=your-secret-here
NEXTAUTH_URL=http://localhost:3000

# For production:
NODE_ENV=production
```

## Troubleshooting

### "Module not found" errors
```bash
# Verify paths in tsconfig.json
# Check @/ alias points to ./src/*

# Restart dev server
npm run dev
```

### "Cannot find module" in production
```bash
# Ensure all imports use correct casing
# Check that files exist in production build
```

### Out of memory during build
```bash
# Increase Node memory
NODE_OPTIONS=--max-old-space-size=4096 npm run build
```

## Best Practices
- ✅ Run type check before committing
- ✅ Fix all linting errors
- ✅ Test production build locally
- ✅ Check bundle size after changes
- ✅ Keep dependencies updated
- ⚠️ Don't commit with build errors
- ⚠️ Don't ignore TypeScript errors
- ⚠️ Don't skip linting
