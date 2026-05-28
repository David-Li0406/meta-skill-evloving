---
name: release-checklist
description: Pre-deployment verification checklist covering build health, migrations, feature flags, rollback readiness, and environment parity. Use before deploying to production, after major features, or when preparing releases.
---

# Release Checklist

Comprehensive pre-deployment verification to ensure safe, successful releases.

## Pre-Release Verification

### 1. Build Health
- [ ] `npm run build` completes without errors
- [ ] `npm run type-check` passes (TypeScript strict mode)
- [ ] `npm run lint` passes with no errors
- [ ] No console warnings in build output
- [ ] Bundle size within acceptable limits

### 2. Database Migrations (per CLAUDE.md workflow)
- [ ] All migrations generated with `npm run db:generate -- --name <change>`
- [ ] Migration SQL reviewed in `drizzle/migrations/`
- [ ] Migrations applied to staging: `npm run db:migrate`
- [ ] No destructive migrations without data backup plan
- [ ] Rollback migration prepared if needed
- [ ] Schema changes backward compatible (or coordinated deploy)

### 3. Environment Configuration
- [ ] All required env vars documented in `.env.example`
- [ ] No hardcoded secrets in codebase
- [ ] Environment parity: dev/staging/prod configs aligned
- [ ] New env vars added to Vercel project settings
- [ ] Supabase project settings updated if needed

### 4. Feature Flags (per AGENTS.md)
- [ ] New features behind flags if risky
- [ ] Flag defaults appropriate for production
- [ ] Gradual rollout plan defined
- [ ] Kill switch ready for new features

### 5. API Compatibility
- [ ] Breaking API changes versioned under `/api/v{n}`
- [ ] Deprecated endpoints still functional
- [ ] Response contracts unchanged or backward compatible
- [ ] Webhook integrations tested (leads-intake, etc.)

### 6. Authentication & Authorization
- [ ] New routes protected with `requireUser()` or `requireRole()`
- [ ] Permission checks via `ensureClientAccess()` verified
- [ ] No new privilege escalation paths
- [ ] Session handling unchanged or tested

### 7. Data Integrity
- [ ] Soft delete patterns maintained
- [ ] No orphaned records from new relationships
- [ ] Activity logging added for new mutations
- [ ] Existing data compatible with schema changes

### 8. Performance Verification
- [ ] No N+1 queries introduced
- [ ] Large lists virtualized (TanStack Virtual)
- [ ] Images optimized via Supabase transforms
- [ ] Caching headers on new API routes

### 9. Observability (per AGENTS.md)
- [ ] Structured logging for new server actions
- [ ] Sentry error boundaries on new routes
- [ ] PostHog events for new user actions
- [ ] No sensitive data in logs

### 10. Rollback Readiness
- [ ] Previous deployment tagged/noted
- [ ] Database rollback plan if migrations fail
- [ ] Feature flags can disable new functionality
- [ ] Vercel instant rollback available

## Deployment Process

### Staging Verification
1. Deploy to Vercel preview
2. Run smoke tests on preview URL
3. Verify new features work as expected
4. Check for console errors
5. Test with both ADMIN and CLIENT roles

### Production Deployment
1. Merge to main branch
2. Monitor Vercel deployment
3. Verify production URL
4. Check Sentry for new errors
5. Monitor PostHog for anomalies

### Post-Deployment
- [ ] Smoke test critical paths
- [ ] Verify database migrations applied
- [ ] Check external integrations (email, webhooks)
- [ ] Monitor error rates for 30 minutes
- [ ] Communicate release to stakeholders

## Output Format

```markdown
# Release Checklist: [Feature/Version]

## Summary
- Release date: YYYY-MM-DD
- Key changes: [list]
- Risk level: LOW|MEDIUM|HIGH

## Verification Status
[Checklist with pass/fail status]

## Rollback Plan
[Steps to revert if issues found]

## Stakeholder Communication
[Who to notify, what to communicate]
```

## Actions

1. Run all build/lint/type-check commands
2. Review pending migrations
3. Check environment variable changes
4. Verify feature flag configurations
5. Document rollback procedure

## Post-Release

- Monitor error rates in Sentry
- Watch PostHog for user behavior changes
- Keep rollback option ready for 24 hours
- Update changelog per AGENTS.md guidelines
