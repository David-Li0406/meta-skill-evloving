---
name: debug-code
description: Debugs code issues, errors, failing tests, and broken flows using a systematic workflow. Identifies root causes, applies minimal fixes, and validates solutions. Works with errors, test failures, API issues, database problems, and integration failures. Use when debugging errors, fixing failing tests, troubleshooting API endpoints, or resolving database issues.
---

# Debug Code

Debugs code issues, errors, failing tests, and broken flows using a systematic workflow that identifies root causes, applies minimal fixes, and validates solutions.

## Project Documentation References

**Critical**: Reference Cursor rules instead of duplicating their content.

For comprehensive project documentation and compatibility requirements, see:

- **[AGENTS.md](../../../AGENTS.md)** - Central reference for all project documentation
- **[@project-overview.md](../../.agent/rules/shared/project/project-overview.md)** - Project overview and tech stack
- **[@api-development.md](../../.agent/rules/apps/control-plane/api-development.md)** - Control Plane REST API patterns
- **[@provisioning.md](../../.agent/rules/apps/control-plane/provisioning.md)** - Tenant provisioning patterns
- **[@database.md](../../.agent/rules/infrastructure/database.md)** - Neon database provisioning patterns
- **[@testing-strategy.md](../../.agent/rules/shared/testing/testing-strategy.md)** - Testing patterns and strategies
- **[@coding-standards.md](../../.agent/rules/shared/quality/coding-standards.md)** - Coding standards and guidelines

## Debugging Workflow

### Step 1: Clarify the Symptom

1. **Identify the Issue**:
   - Exact error message, stack trace, or failing test
   - Endpoint/flow affected (e.g., tenant provisioning, domain management)
   - Environment: local, dev, staging, prod
   - When it occurs: always, intermittently, specific conditions

2. **Gather Context**:
   - Recent changes that might have caused the issue
   - Related files and dependencies
   - Test output or error logs

### Step 2: Locate the Source

Trace using project patterns:

1. **Control Plane Issues**: REST routes -> Services -> Repositories -> Database
2. **Provisioning Issues**: Follow workflow in @provisioning.md
3. **Database Issues**: Neon API, Drizzle schema, migrations consistency
4. **Tenant Isolation Issues**: Verify physical database isolation as per @project-overview.md

### Step 3: Reproduce

1. **Create Reproduction**:
   - Prefer: A failing unit/integration test that reproduces the issue
   - Or: A minimal HTTP request
   - If missing: Add a targeted test as per @testing-strategy.md

2. **Isolate the Problem**:
   - Minimize the reproduction case
   - Focus on the specific failure

### Step 4: Inspect Without Destabilizing

1. **Read Code Around Failure**:
   - Understand the flow and data transformations
   - Check Control Plane patterns (from @api-development.md)
   - Verify provisioning logic (from @provisioning.md)
   - Check database operations (from @database.md)

2. **Avoid Destabilizing Changes**:
   - DO NOT add noisy or permanent console logs
   - Use structured logging via `@vendin/utils/logger` as per @coding-standards.md

### Step 5: Identify Root Cause

Check for common issues:

1. **Tenant Isolation Violations**:
   - Shared database connections
   - Missing tenant context in queries
   - Logic crossing tenant boundaries

2. **Provisioning Failures**:
   - Neon API errors
   - Cloud Run deployment issues
   - Secret Manager configuration errors
   - Rollback failures (see @provisioning.md)

3. **Database and Schema Issues**:
   - Drizzle schema mismatches
   - Missing migrations
   - Neon connection pooling issues

4. **API and Routing Issues**:
   - Incorrect REST patterns
   - Validation errors (Zod)
   - Missing TSDoc/OpenAPI registration

### Step 6: Apply Minimal Fix

1. **Implement Smallest Correct Change**:
   - Fixes the root cause (not just symptoms)
   - Aligns with all relevant rules
   - Keeps functions small and focused

2. **Follow Project Patterns**:
   - REST patterns from @api-development.md
   - Provisioning patterns from @provisioning.md
   - Database patterns from @database.md

### Step 7: Validate the Fix

1. **Run Quality Checks**:

   ```bash
   bun run lint
   bun run typecheck
   bun run test
   ```

2. **Verify**:
   - Original failing scenario is now passing
   - No regressions in related flows
   - Tenant isolation is maintained

### Step 8: Clean Up

1. **Remove Temporary Code**:
   - Remove temporary debug logs
   - Ensure no sensitive data leaked

2. **Document the Fix**:
   - Summarize the fix for Conventional Commit message

## Multi-Tenant Specific Debugging

### Tenant Isolation Check

- Verify that queries always include tenant scoping
- Check that database connection strings are never shared
- Ensure secrets are stored per tenant

### Provisioning Rollback

- If a provisioning step fails, verify that all previous resources were cleaned up as per @provisioning.md rollback logic.

## Best Practices

1. **Understand First**: Read code and understand the flow before changing
2. **Minimal Changes**: Apply smallest fix that solves the root cause
3. **Test-Driven**: Use tests to verify fixes and prevent regressions
4. **Tenant Isolation**: Always prioritize physical database isolation
