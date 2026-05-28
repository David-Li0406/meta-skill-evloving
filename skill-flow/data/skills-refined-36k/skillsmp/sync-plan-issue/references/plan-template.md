# Plan Summary Template

Based on Linear Method + Shape Up best practices.

## Structure

```markdown
## Plan Summary

### Problem
{1-2 sentences: what's broken, missing, or needed. Why does this matter?}

### Appetite
{Scope constraint: "Small batch (1-2 days)" or "Full cycle (1-2 weeks)" or custom}

### Solution
{2-4 sentences: high-level approach. Key technical decisions.}

### Scope
| Path | Change |
|------|--------|
| `src/path/file.ts` | {brief description} |
| `src/other/` | {brief description} |

### Tasks
- [ ] {verb} {object}
- [ ] {verb} {object}
- [ ] {verb} {object}

### Rabbit Holes
{Known risks, complexity, or things that could derail the work. Skip if none.}

### No-Gos
{Explicitly out of scope. What we're NOT doing. Skip if obvious.}

---
*Synced: {YYYY-MM-DD}*
```

## Section Guidelines

### Problem
Start here. Without a problem, you can't judge if the solution is good.

- State what's broken, painful, or missing
- One specific story/scenario is better than abstract description
- Anyone should understand why this matters

**Good**: "Users get duplicate notifications when rapidly toggling settings. Support tickets spiking."
**Bad**: "Add deduplication middleware"

### Appetite
From Shape Up: how much time/effort is this worth? Constrains the solution.

- Small batch: 1-2 days
- Medium: 3-5 days
- Full cycle: 1-2 weeks
- If longer, consider splitting

**Good**: "Small batch - 2 days max. If it takes longer, we're overengineering."
**Bad**: (omitting this entirely)

### Solution
High-level approach only. Not implementation details.

- Key technical decisions
- Why this approach vs alternatives (if non-obvious)
- 2-4 sentences max

**Good**: "Add request deduplication at API gateway using Redis. Same user+action within 5s window gets deduplicated. Notification service unchanged."
**Bad**: "First we'll add a Redis client using ioredis, then create a DeduplicationMiddleware class that implements the Express middleware interface..."

### Scope
Table format for scannability. Path + one-line change.

**Good**:
| Path | Change |
|------|--------|
| `src/middleware/dedup.ts` | new deduplication middleware |
| `src/config/redis.ts` | Redis connection config |
| `tests/integration/` | dedup behavior tests |

**Bad**:
- Update the middleware folder with new stuff
- Some Redis configuration
- Tests

### Tasks
From Linear: plain language, imperative, concrete deliverables.

- Start with verb
- Specific enough to verify completion
- 5-10 tasks typical
- Order matters (dependencies implicit)

**Good**:
- [ ] Add ioredis dependency
- [ ] Create Redis connection module
- [ ] Implement dedup middleware
- [ ] Wire to notification routes
- [ ] Write integration tests

**Bad**:
- [ ] Do the Redis stuff
- [ ] Make it work
- [ ] Tests and documentation

### Rabbit Holes
From Shape Up: things that could derail the work. Call them out.

- Technical risks
- Scope creep temptations
- Dependencies on external factors

**Good**: "Tempting to add configurable TTL per endpoint - don't. Single 5s window is enough. Config adds complexity."
**Bad**: (omitting known risks)

### No-Gos
From Shape Up: explicitly out of scope. Prevents scope creep.

- Features intentionally excluded
- Edge cases we're not handling
- Future work deferred

**Good**: "Not handling: batch notification dedup, webhook dedup, admin override. Those are separate features."
**Bad**: (leaving scope ambiguous)

## Updating Existing Issues

When issue already has content:

1. **Has `## Plan Summary`**: Replace entire section (from header to closing `---`)
2. **No plan section**: Append after existing content with `---` separator
3. **Preserve**: Labels, assignees, milestone, original issue description

Regex to find existing plan:
```
## Plan Summary.*?---\n\*Synced:.*?\*
```

## Complete Example

```markdown
## Plan Summary

### Problem
Users receiving duplicate push notifications when rapidly toggling settings. 12 support tickets this week. Happens because concurrent API requests each trigger notification.

### Appetite
Small batch - 2 days. Simple middleware, no architectural changes.

### Solution
Add request deduplication at API gateway using Redis. Requests with same user+action within 5s window are deduplicated. Notification service stays unchanged.

### Scope
| Path | Change |
|------|--------|
| `src/middleware/dedup.ts` | new deduplication middleware |
| `src/config/redis.ts` | Redis connection config |
| `src/routes/notifications.ts` | wire middleware |
| `tests/integration/dedup.test.ts` | dedup behavior tests |
| `docker-compose.yml` | local Redis for dev |

### Tasks
- [ ] Add ioredis dependency
- [ ] Create Redis connection module
- [ ] Implement DeduplicationMiddleware
- [ ] Add middleware to notification routes
- [ ] Write integration tests
- [ ] Update docker-compose for local Redis

### Rabbit Holes
- Tempting to make TTL configurable per endpoint - don't. Single 5s window covers all cases.
- Don't add metrics/logging in v1. Get it working first.

### No-Gos
- Batch notification dedup (different problem)
- Webhook dedup (needs separate design)
- Admin bypass (no current need)

---
*Synced: 2026-01-23*
```
