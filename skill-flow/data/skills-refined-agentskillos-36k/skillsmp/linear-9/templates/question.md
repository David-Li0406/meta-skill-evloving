# Question Issue Template

Use this template for decisions or discussions that need resolution.

## Template

```markdown
**Title:** [Question] {Topic}
**Labels:** question
**Priority:** Medium

## Question
{What needs to be decided}

## Context (Auto-gathered)
**Relevant code:**
- `{path/to/file.ts}` - {why relevant}

**Current implementation:**
{What exists now}

## Options
1. **Option A**: {description}
   - Pro: {benefit}
   - Con: {drawback}

2. **Option B**: {description}
   - Pro: {benefit}
   - Con: {drawback}

## Decision
{Leave blank - to be filled after discussion}

## Follow-up Issues
{Issues to create after decision is made}
```

## Example

**User says:** "Should we use Redis or Memcached for session storage?"

**Created issue:**
```markdown
**Title:** [Question] Session storage - Redis vs Memcached
**Labels:** question
**Priority:** Medium

## Question
Which caching solution should we use for session storage?

## Context (Auto-gathered)
**Relevant code:**
- `src/auth/session.ts` - Current in-memory session storage
- `src/config/database.ts` - Existing Redis connection for queues

**Current implementation:**
Sessions stored in-memory, lost on restart.

## Options
1. **Redis**
   - Pro: Already used for job queues, supports persistence
   - Con: Slightly more memory overhead

2. **Memcached**
   - Pro: Simpler, faster for pure caching
   - Con: No persistence, would need new infrastructure

## Decision
{To be decided}

## Follow-up Issues
- Implement chosen solution
- Add session expiry configuration
- Update deployment docs
```
