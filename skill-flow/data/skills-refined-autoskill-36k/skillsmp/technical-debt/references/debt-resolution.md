# Debt Resolution Strategies

Approaches for systematically reducing technical debt.

## Resolution Approaches

### 1. Boy Scout Rule

*"Leave the code better than you found it."*

**How it works:**
- Make small improvements during regular work
- Fix one small thing in each PR
- No dedicated debt time needed

**Best for:**
- P3 items
- Small, isolated improvements
- Code you're already touching

**Example:**
```python
# Original task: Add logging to process_order

# Also fix while there:
def process_order(order):
    # Renamed unclear variable (debt item)
    customer = order.user  # was: u
    logger.info(f"Processing order for {customer.email}")
```

### 2. Dedicated Debt Sprint

Reserve a full sprint for debt reduction.

**When to use:**
- Accumulated critical debt
- Before major feature work
- After major milestone

**Structure:**
```
Sprint: Technical Debt Reduction

Goals:
- Resolve all P0 items
- Reduce P1 items by 50%
- Update dependencies

Day 1-2: P0 items (critical)
Day 3-5: P1 items (high priority)
Day 6-8: P2 items (if time permits)
Day 9-10: Testing and verification
```

### 3. 20% Time Allocation

Dedicate 20% of each sprint to debt.

**Implementation:**
```
Sprint Capacity: 10 story points
- Features: 8 points (80%)
- Debt: 2 points (20%)
```

**Best for:**
- Ongoing maintenance
- Preventing debt accumulation
- Team skill building

### 4. Refactoring Friday

Weekly dedicated time for improvements.

**Schedule:**
```
Friday afternoon (2-4 hours):
- Pick 1-2 P2/P3 items
- Pair programming encouraged
- Must include tests
- PR before end of day
```

### 5. Opportunistic Resolution

Fix debt when it directly blocks work.

**Trigger:** "I need to fix X before I can do Y"

**Process:**
1. Scope the fix precisely
2. Time-box the effort
3. Create separate PR if significant
4. Update debt tracking

## Resolution Workflow

### Step 1: Select Debt Item

```markdown
## Selection Criteria

1. Check P0 items first (always do immediately)
2. Consider what's blocking current work
3. Look for quick wins (high impact, low effort)
4. Consider team expertise
```

### Step 2: Analyze Scope

Before starting, understand full scope:

```markdown
## Scope Analysis: DEBT-001

### Questions
- [ ] How many files affected?
- [ ] What tests need updating?
- [ ] Any dependencies on this code?
- [ ] Risk of breaking changes?

### Findings
- 5 files need changes
- 12 tests reference this code
- 2 other services call this
- Medium risk - need careful testing
```

### Step 3: Create Plan

```markdown
## Resolution Plan: DEBT-001

### Approach
Extract duplicate validation to shared module

### Steps
1. Create ValidationService class
2. Add comprehensive tests
3. Update OrdersController
4. Update UsersController
5. Update remaining controllers
6. Remove old validation methods
7. Update documentation

### Estimated Time
4-6 hours

### Rollback Plan
Revert PR if issues found
```

### Step 4: Implement

```markdown
## Implementation Notes

### Branch
`debt/DEBT-001-extract-validation`

### Commits
- Create ValidationService with tests
- Migrate OrdersController
- Migrate UsersController
- Migrate remaining controllers
- Clean up old code

### PR Checklist
- [ ] All tests pass
- [ ] No regression in functionality
- [ ] Documentation updated
- [ ] Debt item linked in PR
```

### Step 5: Verify Resolution

```markdown
## Verification: DEBT-001

### Test Results
- All 47 tests passing
- New tests: 12 added
- Coverage: 95% for new code

### Manual Verification
- [ ] Order creation works
- [ ] User registration works
- [ ] Error messages display correctly

### Performance Check
- No performance regression
- Slight improvement due to code reuse
```

### Step 6: Close Debt Item

```yaml
---
id: DEBT-001
status: resolved
resolved: 2024-01-20
pr: https://github.com/org/repo/pull/123
resolution_notes: |
  Extracted validation to ValidationService.
  All controllers now use shared validation.
  Added 12 new tests for edge cases.
---
```

## Handling Large Debt

### Breaking Down Large Items

Transform a large debt item into smaller, manageable pieces:

```markdown
## Original: DEBT-010
Monolith needs to be split into services
Effort: 5 (months)

## Broken Down:
- DEBT-010a: Extract user service (effort: 3)
- DEBT-010b: Extract payment service (effort: 3)
- DEBT-010c: Extract notification service (effort: 2)
- DEBT-010d: Update API gateway (effort: 2)
- DEBT-010e: Migrate data (effort: 3)
```

### Strangler Fig Pattern

Gradually replace old code:

```markdown
## Phase 1: New Service
- Build new UserService alongside old code
- Route 10% of traffic to new service

## Phase 2: Migration
- Increase traffic to 50%, then 100%
- Monitor for issues

## Phase 3: Cleanup
- Remove old code
- Archive migration code
```

## Measuring Progress

### Debt Metrics Dashboard

```markdown
## Debt Metrics - January 2024

### Overview
| Metric | Value | Trend |
|--------|-------|-------|
| Total Items | 15 | ↓ -3 |
| Open | 10 | ↓ -2 |
| P0/P1 | 5 | ↓ -1 |

### Resolution Rate
- Items resolved: 5
- Avg resolution time: 3.5 days
- Velocity: 1.25 items/week

### Categories
| Category | Count | Change |
|----------|-------|--------|
| Code | 6 | -2 |
| Test | 4 | -1 |
| Architecture | 3 | 0 |
| Docs | 2 | 0 |
```

### Tracking Debt Ratio

```
Debt Ratio = Debt Story Points / Total Story Points

Target: < 20%

Current Sprint:
- Feature points: 40
- Debt points: 8
- Ratio: 16.7% ✓
```

## Anti-Patterns to Avoid

### 1. Debt Bankruptcy
*Declaring all debt "won't fix"*

**Problem:** Ignores legitimate issues
**Solution:** Review each item, close only with good reason

### 2. Perfectionism Paralysis
*Trying to fix everything at once*

**Problem:** Never ships, overwhelming
**Solution:** Incremental improvement, prioritize

### 3. Hidden Debt
*Not tracking debt formally*

**Problem:** Forgotten, accumulates interest
**Solution:** Make debt visible, track consistently

### 4. Debt Whack-a-Mole
*Fixing symptoms not causes*

**Problem:** Same debt reappears
**Solution:** Find and fix root causes

### 5. Gold Plating
*Over-engineering the fix*

**Problem:** Simple debt becomes big project
**Solution:** Minimum viable fix, iterate if needed

## Team Practices

### Debt Review Meeting

**Weekly, 30 minutes:**
1. Review new debt items (5 min)
2. Status update on in-progress (10 min)
3. Celebrate resolutions (5 min)
4. Plan next week's debt work (10 min)

### Debt Retrospective

**Monthly:**
- What debt caused the most pain?
- What patterns are we seeing?
- How can we prevent this type of debt?
- Should we adjust our process?

### Knowledge Sharing

**After resolving significant debt:**
- Document what was learned
- Share patterns to avoid
- Update team guidelines
