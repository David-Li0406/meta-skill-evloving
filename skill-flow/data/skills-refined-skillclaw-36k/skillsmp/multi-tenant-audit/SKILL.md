---
name: multi-tenant-audit
description: Automated auditing for multi-tenant data isolation and security in OutreachGlobal/Nextier platform
---

# Multi-Tenant Isolation Audit Instructions

## Purpose
This skill helps ensure that different companies (tenants) using the OutreachGlobal platform cannot access each other's data. Based on critical audit findings, this is essential for GDPR/CCPA compliance and preventing data breaches.

## When to Use This Skill
- Reviewing new code changes that touch database queries
- Before deploying updates to production
- During security audits
- When investigating data access issues

## Key Audit Areas

### 1. Database Query Checks
**Always verify:**
- Every SELECT, UPDATE, DELETE query includes `teamId` filter
- JOIN operations maintain tenant isolation
- Subqueries respect tenant boundaries
- No queries use `globalThis` or in-memory storage

**Red flags to catch:**
```typescript
// ❌ BAD - No teamId filter
const leads = await db.select().from(leadsTable);

// ✅ GOOD - Proper tenant filtering
const leads = await db.select().from(leadsTable).where(eq(leadsTable.teamId, teamId));
```

### 2. API Route Validation
**Check every API endpoint:**
- `apiAuth()` returns valid `teamId` (not undefined)
- Frontend routes pass `teamId` to backend
- JWT tokens include `teamId` claim
- No routes bypass tenant filtering

### 3. File Storage Security
**Verify:**
- DigitalOcean Spaces objects are prefixed with `teamId/`
- No shared files across tenants
- Proper access controls on uploaded content

### 4. Queue Job Isolation
**Ensure:**
- Background jobs include `teamId` context
- BullMQ jobs don't process cross-tenant data
- Redis keys are namespaced by tenant

## Common Issues to Flag

1. **Missing teamId in WHERE clauses** - Most common violation
2. **apiAuth() returning undefined teamId** - Critical authentication bug
3. **Shared database tables without RLS** - Row-Level Security gaps
4. **In-memory storage (globalThis)** - Data lost on restart, no isolation
5. **Unbounded queries** - Performance issues affecting all tenants

## Audit Checklist

- [ ] All database schemas have `teamId` columns
- [ ] Foreign keys maintain referential integrity across tenants
- [ ] API routes validate teamId before processing
- [ ] File uploads are tenant-isolated
- [ ] Background jobs respect tenant boundaries
- [ ] No cross-tenant data leaks in logs or errors

## Response Format
When auditing, provide:
1. **Severity level** (Critical/High/Medium/Low)
2. **Specific code locations** with line numbers
3. **Clear fix recommendations** with code examples
4. **Testing steps** to verify the fix

## Related Skills
- Use with `security-scan` for vulnerability assessment
- Combine with `schema-audit` for database structure validation
- Reference `cost-guardian` for resource isolation