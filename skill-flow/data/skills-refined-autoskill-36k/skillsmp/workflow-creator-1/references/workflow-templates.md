# Workflow Templates

Ready-to-use workflow templates for common tasks.

## Build & Deploy

### Basic Deployment

```markdown
---
description: Deploy application to environment
---

# Deploy {Environment}

## Prerequisites

- All tests passing
- Correct branch checked out

## Steps

// turbo
1. Run tests:
   ```bash
   npm run test
   ```

// turbo
2. Build the application:
   ```bash
   npm run build
   ```

3. Deploy to {environment}:
   ```bash
   npm run deploy:{environment}
   ```

4. Verify deployment at {URL}.
```

### Release Workflow

```markdown
---
description: Create a new release version
---

# Create Release

## Steps

1. Ensure on main branch and up to date:
   ```bash
   git checkout main
   git pull origin main
   ```

2. Update version in package.json

// turbo
3. Run full test suite:
   ```bash
   npm run test:all
   ```

4. Create git tag:
   ```bash
   git tag v{VERSION}
   git push origin v{VERSION}
   ```

5. Create GitHub release with changelog.
```

---

## Testing

### Full Test Suite

```markdown
---
description: Run complete test suite with coverage
---

# Full Test Suite

// turbo-all

## Steps

1. Run unit tests:
   ```bash
   npm run test:unit
   ```

2. Run integration tests:
   ```bash
   npm run test:integration
   ```

3. Run e2e tests:
   ```bash
   npm run test:e2e
   ```

4. Generate coverage report:
   ```bash
   npm run test:coverage
   ```
```

### Quick Lint Check

```markdown
---
description: Run linting and type checking
---

# Lint Check

// turbo-all

## Steps

1. Run ESLint:
   ```bash
   npm run lint
   ```

2. Run TypeScript check:
   ```bash
   npm run typecheck
   ```

3. Run Prettier:
   ```bash
   npm run format:check
   ```
```

---

## Database

### Migration Workflow

```markdown
---
description: Run database migrations with backup
---

# Database Migration

## Prerequisites

- Database connection available
- Migration files in `migrations/`

## Steps

1. Create backup:
   ```bash
   npm run db:backup
   ```

// turbo
2. Run migrations:
   ```bash
   npm run db:migrate
   ```

3. Verify data integrity:
   ```bash
   npm run db:verify
   ```

## Rollback

If issues occur:
```bash
npm run db:rollback
```
```

### Seed Data

```markdown
---
description: Seed database with test/sample data
---

# Seed Database

## Steps

// turbo
1. Clear existing data:
   ```bash
   npm run db:reset
   ```

// turbo
2. Run seeds:
   ```bash
   npm run db:seed
   ```

3. Verify seed data loaded correctly.
```

---

## Git & Code Review

### PR Review

```markdown
---
description: Review a pull request
---

# PR Review

## Steps

1. Fetch and checkout:
   ```bash
   git fetch origin pull/{PR_NUMBER}/head:pr-{PR_NUMBER}
   git checkout pr-{PR_NUMBER}
   ```

// turbo
2. Install dependencies:
   ```bash
   npm install
   ```

// turbo
3. Run tests:
   ```bash
   npm run test
   ```

4. Review changes for:
   - [ ] Code quality
   - [ ] Security concerns
   - [ ] Test coverage
   - [ ] Documentation

5. Provide feedback or approve.
```

### Sync Fork

```markdown
---
description: Sync forked repository with upstream
---

# Sync Fork

## Steps

1. Add upstream if not exist:
   ```bash
   git remote add upstream {UPSTREAM_URL}
   ```

// turbo
2. Fetch upstream:
   ```bash
   git fetch upstream
   ```

3. Merge upstream/main:
   ```bash
   git checkout main
   git merge upstream/main
   ```

// turbo
4. Push to origin:
   ```bash
   git push origin main
   ```
```

---

## Security

### Security Audit

```markdown
---
description: Run security audit and vulnerability scan
---

# Security Audit

// turbo-all

## Steps

1. Audit npm packages:
   ```bash
   npm audit
   ```

2. Check for outdated packages:
   ```bash
   npm outdated
   ```

3. Run security scan:
   ```bash
   npm run security:scan
   ```

4. Review findings and update vulnerable packages.
```

### Secrets Check

```markdown
---
description: Scan for accidentally committed secrets
---

# Secrets Check

## Steps

// turbo
1. Scan for secrets:
   ```bash
   npx git-secrets --scan
   ```

2. Check .env files not committed:
   ```bash
   git status | grep -E "\.env"
   ```

3. Review any findings and remove secrets from history if needed.
```

---

## Maintenance

### Update Dependencies

```markdown
---
description: Update project dependencies safely
---

# Update Dependencies

## Steps

1. Check for updates:
   ```bash
   npm outdated
   ```

2. Update patch versions:
   ```bash
   npm update
   ```

// turbo
3. Run tests:
   ```bash
   npm run test
   ```

4. Review major version updates manually.

5. Commit lock file:
   ```bash
   git add package-lock.json
   git commit -m "chore: update dependencies"
   ```
```

### Cleanup Build Artifacts

```markdown
---
description: Clean build artifacts and caches
---

# Cleanup

// turbo-all

## Steps

1. Remove node_modules:
   ```bash
   rm -rf node_modules
   ```

2. Remove build folders:
   ```bash
   rm -rf dist build .next out
   ```

3. Clear caches:
   ```bash
   npm cache clean --force
   ```

4. Reinstall:
   ```bash
   npm install
   ```
```

---

## Development

### New Feature Setup

```markdown
---
description: Start a new feature branch
---

# New Feature

## Steps

1. Create feature branch:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/{FEATURE_NAME}
   ```

2. Create necessary files/folders for the feature.

3. Add basic tests.

4. Make initial commit:
   ```bash
   git add .
   git commit -m "feat: setup {FEATURE_NAME}"
   ```
```

### Dev Environment Setup

```markdown
---
description: Set up development environment from scratch
---

# Dev Setup

## Prerequisites

- Node.js installed
- Git configured

## Steps

// turbo
1. Install dependencies:
   ```bash
   npm install
   ```

2. Copy environment file:
   ```bash
   cp .env.example .env
   ```

3. Configure .env with your values.

// turbo
4. Set up database:
   ```bash
   npm run db:setup
   ```

// turbo
5. Run dev server:
   ```bash
   npm run dev
   ```
```

---

## Shopify Specific

### Sync Theme

```markdown
---
description: Sync Shopify theme from store
---

# Sync Theme

## Steps

1. Pull latest theme:
   ```bash
   shopify theme pull --store={STORE}
   ```

2. Review changes:
   ```bash
   git diff
   ```

3. Commit if needed:
   ```bash
   git add .
   git commit -m "sync: theme from {STORE}"
   ```
```

### Deploy Theme

```markdown
---
description: Deploy theme to Shopify store
---

# Deploy Theme

## Steps

// turbo
1. Run theme check:
   ```bash
   shopify theme check
   ```

2. Push to store:
   ```bash
   shopify theme push --store={STORE}
   ```

3. Preview and verify on store.
```
