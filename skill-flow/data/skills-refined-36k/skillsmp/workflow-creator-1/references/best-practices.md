# Workflow Best Practices

Guidelines for writing effective, maintainable workflows.

## Writing Clear Steps

### Use Imperative Verbs

Start each step with an action verb:

| ✅ Good | ❌ Avoid |
|---------|----------|
| Run tests | You should run tests |
| Create backup | Creating a backup |
| Check status | The status needs to be checked |

### Be Specific

Include exact commands, paths, and expected outcomes:

```markdown
# ✅ Good
1. Run unit tests:
   ```bash
   npm run test:unit -- --coverage
   ```

# ❌ Avoid
1. Run the tests
```

### One Action Per Step

Keep steps atomic for clarity:

```markdown
# ✅ Good
1. Install dependencies:
   ```bash
   npm install
   ```

2. Run migrations:
   ```bash
   npm run db:migrate
   ```

# ❌ Avoid
1. Install dependencies and run migrations
```

## Turbo Annotations

### When to Use `// turbo`

Use on **safe, non-destructive** commands:
- `npm install`
- `npm run test`
- `npm run build`
- `npm run lint`
- Read-only git commands (`git status`, `git log`)

### When NOT to Use `// turbo`

Never auto-run:
- Commands that delete data (`rm`, `DROP TABLE`)
- Deployment commands to production
- Commands requiring user input
- Commands with side effects (emails, payments)
- Commands modifying git history

### `// turbo` vs `// turbo-all`

```markdown
# Use // turbo for selective automation
1. Review configuration (manual)

// turbo
2. Run tests (safe to auto-run)

3. Deploy (manual - production impact)

---

# Use // turbo-all when ALL steps are safe
// turbo-all

## Steps
1. Run lint
2. Run tests
3. Generate report
```

## Handling Variables

### User-Provided Values

Use `{PLACEHOLDER}` syntax for user input:

```markdown
1. Create feature branch:
   ```bash
   git checkout -b feature/{FEATURE_NAME}
   ```
```

### Environment-Specific Values

Document which values need configuration:

```markdown
## Configuration

Before running, set these values:
- `{ENVIRONMENT}`: staging or production
- `{STORE_URL}`: Your Shopify store URL
```

## Error Handling

### Include Rollback Steps

```markdown
## Rollback

If deployment fails:
```bash
git revert HEAD
npm run deploy
```
```

### Document Prerequisites

```markdown
## Prerequisites

- [ ] All tests passing locally
- [ ] On correct branch (`main` for prod)
- [ ] Environment variables configured
- [ ] Required secrets available
```

### Add Verification Steps

```markdown
4. Verify deployment:
   - Check {URL} loads correctly
   - Verify key features work
   - Monitor error logs for 5 minutes
```

## Organization Tips

### Group Related Workflows

```
.agent/workflows/
├── deploy-staging.md
├── deploy-production.md
├── db-migrate.md
├── db-rollback.md
└── db-backup.md
```

### Use Consistent Naming

| Pattern | Examples |
|---------|----------|
| `{action}` | `deploy.md`, `test.md`, `build.md` |
| `{action}-{target}` | `deploy-staging.md`, `test-e2e.md` |
| `{resource}-{action}` | `db-migrate.md`, `theme-sync.md` |

### Cross-Reference Workflows

```markdown
## See Also

- `/db-backup` - Create backup before migrations
- `/db-rollback` - Revert if issues occur
```

## Common Pitfalls

### ❌ Too Vague

```markdown
1. Set up the environment
2. Run the tests
3. Deploy
```

### ✅ Better

```markdown
1. Copy environment file:
   ```bash
   cp .env.example .env
   ```

2. Configure these variables in `.env`:
   - `DATABASE_URL`
   - `API_KEY`

3. Run test suite:
   ```bash
   npm run test -- --coverage
   ```

4. Deploy to staging:
   ```bash
   npm run deploy:staging
   ```
```

### ❌ Too Long

Workflows over 12K characters should be split:

```markdown
# Instead of one mega-workflow

# Create separate workflows:
/setup-dev        # Initial setup
/test             # Run tests
/deploy           # Deploy application
```

### ❌ Missing Context

```markdown
1. Run the migration script
```

### ✅ Better

```markdown
1. Run the migration script:
   ```bash
   npm run db:migrate
   ```
   
   This will apply all pending migrations from `migrations/`.
   Expected output: "X migrations applied successfully"
```

## Documentation Patterns

### Short Description (frontmatter)

Keep under 80 characters:

```yaml
---
description: Deploy application to production with zero downtime
---
```

### Step Comments

Add context when needed:

```markdown
// This step may take 5-10 minutes
3. Build production bundle:
   ```bash
   npm run build
   ```
```

### Notes Section

Add tips and warnings:

```markdown
## Notes

> ⚠️ **Warning**: This will restart the server, causing brief downtime.

> 💡 **Tip**: Run during low-traffic hours for best results.
```
