# Question Examples

Sample clarifying questions for plan review.

## Completeness

### Missing error handling
```
Context: Plan describes happy path but no error scenarios.

Current state: The plan shows data flowing from API to database,
but doesn't mention what happens if the database is unavailable.

Impact: Production outages could leave users with cryptic errors
or data loss.

Options:
1. Add retry with exponential backoff
2. Add circuit breaker pattern
3. Fail fast with clear error message
4. Queue writes for later retry
```

### Missing edge cases
```
Context: User input validation seems incomplete.

Current state: Plan validates email format but doesn't mention:
- Maximum length limits
- Unicode/emoji handling
- Duplicate detection

Impact: Could allow malformed data or duplicates in database.

Options:
1. Add comprehensive validation rules now
2. Rely on database constraints
3. Add basic limits, iterate later
```

## Technical Feasibility

### Performance concern
```
Context: Proposed approach may not scale.

Current state: Plan loads all records into memory for filtering.
Current dataset: 10K records. Expected growth: 1M+ records.

Impact: Memory exhaustion, slow response times at scale.

Options:
1. Use database-level filtering
2. Add pagination
3. Implement caching layer
4. Accept limitation, revisit when needed
```

### Architecture concern
```
Context: Tight coupling between components.

Current state: Component A directly imports and calls Component B's
internal functions.

Impact: Changes to B require changes to A. Testing A requires B.

Options:
1. Add interface/contract between them
2. Use dependency injection
3. Accept coupling (simple enough)
```

## Implementation Clarity

### Ambiguous requirement
```
Context: "Fast" is not defined.

Current state: Plan says "API should respond fast" without metrics.

Impact: No way to verify success. Could over-engineer or under-deliver.

Options:
1. p95 < 100ms
2. p95 < 500ms
3. p95 < 2s
4. "Faster than current" (measure first)
```

### Missing decision
```
Context: Multiple valid implementation approaches.

Current state: Plan needs to store user sessions but doesn't specify where.

Impact: Wrong choice could require rewrite later.

Options:
1. Database (simple, persistent)
2. Redis (fast, requires infrastructure)
3. JWT (stateless, larger tokens)
4. In-memory (development only)
```

## Dependencies

### External dependency risk
```
Context: Plan relies on third-party service.

Current state: Plan uses ExternalAPI for geocoding with no fallback.

Impact: ExternalAPI downtime = our downtime.

Options:
1. Add fallback to alternative provider
2. Cache results aggressively
3. Accept risk (non-critical feature)
4. Build in-house solution
```

## Asking Good Questions

1. **State context first** - What aspect, why it matters
2. **Show current state** - What plan says (or doesn't)
3. **Explain impact** - Why this decision matters
4. **Provide options** - Make it easy to decide
5. **One at a time** - Don't overwhelm
