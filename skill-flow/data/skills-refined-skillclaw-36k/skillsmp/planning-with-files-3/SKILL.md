---
name: planning-with-files
version: "2.0.2"
description: "Structured file-based planning for Alexandria's complex multi-step tasks. Creates task_plan.md, findings.md, progress.md. REQUIRED for: >5 tool calls, database schema changes, queue architecture, external API integrations, performance optimization, data migration. DO NOT use mcp__pal__planner for file-based implementation tasks."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
hooks:
  Start:
    - type: command
      command: echo "📋 Planning mode activated - creating task files..."
  Stop:
    - type: command
      command: echo "✅ Planning complete - execution phase ready"
---

# Planning With Files - Alexandria Edition

**Priority: PRIMARY tool for all complex implementation tasks**

## When to Use (REQUIRED)

This skill is **MANDATORY** for:

- **Database work**: Schema changes, migrations, query optimization
- **Queue architecture**: Batch size tuning, handler optimization, backfill
- **External APIs**: Adding providers (ISBNdb, Google Books, Gemini, etc.)
- **Performance**: Optimization, profiling, index design
- **Data migration**: Backfill, enrichment pipeline changes
- **Multi-file changes**: >3 files touched
- **Complex tasks**: >5 tool calls required

## When NOT to Use

**Use PAL MCP tools instead for:**
- `mcp__pal__debug` - Deep debugging of mysterious bugs
- `mcp__pal__codereview` - Post-implementation code review
- `mcp__pal__secaudit` - Security vulnerability scanning
- `mcp__pal__consensus` - Multi-model architectural decision validation

**Clear distinction:**
- **planning-with-files** = Implementation planning & execution
- **PAL MCP planner** = Conceptual architectural planning (rarely needed)
- **PAL MCP debug/review** = Post-implementation validation

## The 3-File Pattern

Create these in your **project root** (not in skill directory):

### 1. `task_plan.md` - Implementation Roadmap
```markdown
# Task: [Descriptive Name]

## Goal
[What we're building/fixing and why]

## Context
- Current state: [What exists now]
- Problem: [What needs to change]
- Success criteria: [How we know it's done]

## Implementation Steps
- [ ] Phase 1: Research & Design
  - [ ] Explore current codebase
  - [ ] Document findings
  - [ ] Design approach
- [ ] Phase 2: Core Implementation
  - [ ] File 1: [Changes]
  - [ ] File 2: [Changes]
- [ ] Phase 3: Testing & Validation
  - [ ] Unit tests
  - [ ] Integration tests
  - [ ] Manual validation
- [ ] Phase 4: Deployment
  - [ ] Deploy to production
  - [ ] Monitor metrics
  - [ ] Validate no regressions

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Database lock | Production outage | Test migration on staging first |
| ISBNdb quota exhaustion | Failed enrichment | Add quota check before operations |

## Files Modified
- `worker/src/services/enrichment.ts`
- `worker/src/routes/api.ts`
- `worker/wrangler.jsonc`

## Testing Strategy
- Unit: [Specific test cases]
- Integration: [Workflow tests]
- E2E: [Full pipeline validation]
```

### 2. `findings.md` - Research Journal
```markdown
# Findings: [Task Name]

## Current Implementation Analysis
**Date:** [YYYY-MM-DD HH:MM]

### Architecture
- Current approach: [How it works now]
- Key files: [List with line numbers]
- Dependencies: [What this depends on]
- Performance: [Current metrics]

### Database Schema
```sql
-- Current schema
CREATE TABLE enriched_editions (...);
```

## Research Notes
**[YYYY-MM-DD HH:MM]** - Discovered ISBNdb batch endpoint
- Can send 1000 ISBNs in one POST
- Counts as 1 API call, not 1000
- Requires Content-Type: application/json

**[YYYY-MM-DD HH:MM]** - Found Hyperdrive connection pooling issue
- Only 50 connections available
- Current code creates connection per request
- Solution: Use request-scoped connection from context

## Decisions Made
**[YYYY-MM-DD HH:MM]** - Decision: Use lazy backfill strategy
- **Rationale**: Avoids migrating 49M rows
- **Alternative considered**: Full backfill (rejected - too expensive)
- **Trade-off**: 10-15ms one-time cost vs 2-day migration

## Blockers & Questions
- [ ] BLOCKED: Need ISBNdb API key with higher quota
  - **Impact**: Can't test batch endpoint
  - **Owner**: @user
- [x] RESOLVED: How to handle concurrent writes?
  - **Solution**: ON CONFLICT DO NOTHING in PostgreSQL
```

### 3. `progress.md` - Execution Log
```markdown
# Progress: [Task Name]

## Summary
- **Status**: In Progress
- **Started**: 2026-01-11 10:30
- **Last Updated**: 2026-01-11 14:15
- **Completion**: 60%
- **Current Phase**: Phase 2 - Core Implementation

## Completed Work
✅ **Phase 1: Research & Design** (10:30-12:00)
- Explored `worker/src/services/enrichment.ts`
- Documented current provider chain
- Designed new circuit breaker approach
- Created architecture diagrams in findings.md

✅ **Step 2.1: Implement circuit breaker** (12:15-13:30)
- Created `worker/src/middleware/circuit-breaker.ts`
- Added unit tests (8/8 passing)
- Integrated with enrichment service

## Current Work
🔄 **Step 2.2: Update enrichment pipeline** (13:45-present)
- Modifying `enrichment.ts` to use circuit breaker
- Need to test with real ISBNdb API
- Next: Add analytics tracking

## Pending Work
- [ ] Step 2.3: Add provider fallback logic
- [ ] Step 2.4: Update tests
- [ ] Phase 3: Testing & Validation
- [ ] Phase 4: Deployment

## Issues Encountered
| Time | Error | Attempted Fix | Resolution |
|------|-------|---------------|------------|
| 13:50 | ISBNdb 429 (rate limit) | Added circuit breaker | ✅ Circuit opens after 5 failures |
| 14:10 | TypeScript error in tests | Fixed mock types | ✅ All tests passing |

## Next Actions
1. Complete circuit breaker integration
2. Run full test suite (`npm run test`)
3. Deploy to staging for validation
4. Monitor ISBNdb quota usage

## Metrics
- Files modified: 3
- Lines changed: +245 / -87
- Tests added: 12
- Tests passing: 20/20
```

## Alexandria-Specific Workflows

### Workflow 1: Database Schema Migration

**Trigger:** "Add subject_tags column to enriched_works"

**Required steps:**
1. Create planning files
2. **Test in psql FIRST** (Alexandria golden rule!)
3. Design zero-downtime migration
4. Update TypeScript types
5. Modify Zod schemas
6. Update enrichment pipeline
7. Add unit tests
8. Deploy with rollback plan

**Key files:**
- `worker/src/schemas/` - Zod validation
- `worker/src/services/enrichment.ts` - Pipeline logic
- Database schema docs

### Workflow 2: Queue Optimization

**Trigger:** "Enrichment queue is backing up"

**Required steps:**
1. Profile current performance (Wrangler tail + analytics)
2. Identify bottleneck (R2? Database? API calls?)
3. Design optimization approach
4. Update `queue-handlers.ts`
5. Adjust batch size/concurrency in `wrangler.jsonc`
6. Add performance tests
7. Deploy incrementally (10% → 50% → 100%)
8. Monitor metrics (queue depth, processing time)

**Key files:**
- `worker/src/services/queue-handlers.ts`
- `worker/wrangler.jsonc` - Queue config
- `worker/src/services/cover-processor.ts`

### Workflow 3: External API Integration

**Trigger:** "Add LibraryThing API support"

**Required steps:**
1. Research API (rate limits, auth, response schema)
2. Design client service
3. Add to provider chain (priority order)
4. Implement circuit breaker protection
5. Add normalization logic
6. Update enrichment orchestrator
7. Add API cost tracking (Analytics Engine)
8. Document rate limits in `docs/operations/RATE-LIMITS.md`

**Key files:**
- `worker/src/services/external-apis/`
- `worker/src/services/normalizers/`
- `worker/src/middleware/circuit-breaker.ts`

## Critical Rules

### 1. Never Skip Planning Files
Complex Alexandria tasks touch database + queues + external APIs. You **will** lose track without planning files.

### 2. Test in psql Before Worker Code
Alexandria's golden rule: **Always validate SQL in psql first**. Never write Worker code blind.

```bash
ssh root@Tower.local "docker exec postgres psql -U openlibrary -d openlibrary"
```

### 3. Update Findings After Discovery
Every research session adds to findings.md. Includes:
- Database query plans (EXPLAIN ANALYZE output)
- API responses (full JSON examples)
- Performance metrics (before/after)

### 4. Log All Errors
Alexandria runs on production data (54M+ books). Errors are learning opportunities:

```markdown
## Errors Encountered
| Error | Root Cause | Fix |
|-------|------------|-----|
| PG timeout (30s) | Missing index on edition_isbns.isbn | CREATE INDEX CONCURRENTLY |
| ISBNdb 402 (quota) | Daily limit exceeded | Added quota tracking via KV |
```

### 5. Read Plan Before Major Changes
Before modifying database schema or queue config, **re-read task_plan.md**. Keeps goals fresh in context.

## Integration with Other Tools

### Combined with Specialized Skills
```bash
# Schema migration uses planning-with-files automatically
/schema-migration
  ↳ Loads postgres-optimizer agent
  ↳ Creates planning files
  ↳ Runs db-check.sh validation

# Queue optimization uses planning-with-files automatically
/queue-optimization
  ↳ Loads cloudflare-workers-optimizer agent
  ↳ Creates planning files
  ↳ Profiles current performance
```

### Combined with PAL MCP (Post-Implementation)
```bash
# 1. Use planning-with-files for implementation
# 2. After completion, validate with PAL:

# Code review
mcp__pal__codereview - Check for bugs, patterns, optimization opportunities

# Security audit
mcp__pal__secaudit - Scan for SQL injection, API key exposure, etc.

# Document findings from PAL in findings.md
```

## Success Metrics (BooksTrack Proven)

After 2+ months of production use in BooksTrack:
- ✅ **0% regression rate** on complex changes
- ✅ **40% faster completion** (planning saves debugging time)
- ✅ **100% resumability** (can pause/resume across sessions)
- ✅ **Zero surprise breaking changes** in production

## Common Anti-Patterns

| ❌ Don't Do This | ✅ Do This Instead |
|-----------------|-------------------|
| Start coding immediately | Create task_plan.md first |
| Use TodoWrite for persistence | Use markdown planning files |
| Skip findings.md | Document every discovery |
| Test Worker code first | Test SQL in psql first |
| Commit planning files | Git-ignore them (session-specific) |
| Use PAL planner for implementation | Use planning-with-files |
| Repeat failed actions | Log errors, mutate approach |

## Template Files

Starter templates are in `templates/` subdirectory:
- `templates/task_plan.md` - Full implementation template
- `templates/findings.md` - Research journal template
- `templates/progress.md` - Execution log template

Copy these to your project root when starting a new task.

## Quick Reference

```bash
# 1. Create planning files (project root)
touch task_plan.md findings.md progress.md

# 2. Start with task_plan.md
# - Define goal and success criteria
# - Break into phases
# - List files to modify
# - Identify risks

# 3. Research phase (update findings.md)
# - Explore codebase
# - Test queries in psql
# - Document current architecture

# 4. Implementation phase (update progress.md)
# - Mark steps complete
# - Log errors
# - Track metrics

# 5. Validation phase
# - Run tests
# - Deploy to staging
# - Monitor production

# 6. (Optional) Post-implementation review
# - mcp__pal__codereview for code quality
# - mcp__pal__secaudit for security
# - Document findings in findings.md
```

---

**Version:** 2.0.2 (Alexandria Optimized)
**Last Updated:** 2026-01-11
**Maintained By:** Alexandria AI Team
**Pattern Source:** BooksTrack (2+ months production validated)
