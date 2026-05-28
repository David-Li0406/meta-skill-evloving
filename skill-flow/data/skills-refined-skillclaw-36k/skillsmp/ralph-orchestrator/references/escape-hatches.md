# Escape Hatches for Ralph Loops

Recovery patterns when Claude gets stuck during Ralph loops.

## Why Escape Hatches Matter

Without escape hatches, Claude can:
- Spin forever on an impossible problem
- Burn through iterations without progress
- Output false completion promises to escape
- Lose all context trying the same failed approach

Escape hatches provide structured recovery paths that maintain loop integrity.

## The 3-Attempt Rule

The fundamental escape hatch pattern.

### How It Works

```
attempt_count = 0

for each iteration:
    if working on same issue as last iteration:
        attempt_count += 1
    else:
        attempt_count = 1

    if attempt_count > 3:
        trigger_escape_hatch()
```

### Implementation in Progress.md

Track attempts in the Current State section:

```markdown
## Current State

**Working on**: Fix database connection timeout
**Attempts on current issue**: 3  <-- Increment each iteration on same issue
**Last attempt result**: Connection still timing out after increasing timeout to 30s
```

When attempts > 3:

```markdown
## Current State

**Working on**: [ESCAPE HATCH TRIGGERED] Database connection timeout
**Attempts on current issue**: 4
**Escape hatch action**: Marking as BLOCKED, moving to next story
```

## Escape Hatch Patterns

### Pattern 1: Document and Move On

When stuck on a non-critical story.

**Trigger**: 3+ attempts, story is not blocking others

**Actions**:
1. Document thoroughly in progress.md
2. Mark story as BLOCKED in prd.json
3. Move to next non-blocked story
4. Continue loop with remaining stories

**Progress.md Entry**:
```markdown
## Blocked Stories

### US-003: Integrate with payment API
**Blocked after**: 4 attempts
**Issue**: API returns 403 despite valid credentials
**Attempted**:
  - Verified API key is correct
  - Tried both test and production endpoints
  - Contacted support (no response yet)
**Hypothesis**: IP whitelist issue on their end
**Action taken**: Moved to US-004, will return if resolved
```

**prd.json Update**:
```json
{
  "id": "US-003",
  "title": "Integrate with payment API",
  "passes": false,
  "blocked": true,
  "blocked_reason": "API returning 403, likely IP whitelist issue"
}
```

### Pattern 2: Try Alternative Approach

When the approach might be wrong, not the goal.

**Trigger**: 3+ attempts with same approach

**Actions**:
1. Document what didn't work
2. Identify alternative approach
3. Reset attempt counter
4. Try alternative
5. If alternative also fails after 3 attempts, use Pattern 1

**Progress.md Entry**:
```markdown
## Learnings (append-only)

[Iteration 5] Original approach: Using ORM for complex query - keeps timing out
[Iteration 5] Switching to raw SQL approach as alternative
[Iteration 6] Raw SQL approach working - ORM was generating inefficient joins
```

### Pattern 3: Simplify Requirements

When the requirement might be too complex.

**Trigger**: 3+ attempts, complexity seems to be the issue

**Actions**:
1. Identify minimal viable version
2. Document what's being deferred
3. Implement simplified version
4. Mark story as PARTIAL
5. Create follow-up story for full implementation

**Progress.md Entry**:
```markdown
## Learnings (append-only)

[Iteration 7] Full sorting with all 12 fields too complex in single iteration
[Iteration 7] Simplifying to sort by created_at only, deferring multi-field sort
[Iteration 8] Basic sorting working, created US-010 for advanced sorting
```

**prd.json Update**:
```json
{
  "id": "US-005",
  "title": "Add sorting to list endpoint",
  "passes": true,
  "notes": "PARTIAL: Implements created_at sort only. See US-010 for multi-field."
}
```

### Pattern 4: Skip and Return

When blocked by external dependency.

**Trigger**: Blocked waiting for something external (API, human, deployment)

**Actions**:
1. Document the external dependency
2. Skip to next independent story
3. After other stories, check if dependency resolved
4. If resolved, return to blocked story
5. If still blocked at end, leave as BLOCKED

**Progress.md Entry**:
```markdown
## Current State

**Skipped stories**:
- US-007: Waiting for staging API credentials (requested from DevOps)

**Working on**: US-008 (independent of US-007)

---

[Later in loop]

## Learnings (append-only)

[Iteration 15] Checked back on US-007 - credentials now available in .env
[Iteration 15] Resuming US-007
```

### Pattern 5: Graceful Degradation

When full solution isn't possible, implement partial solution.

**Trigger**: Cannot achieve full acceptance criteria but can achieve subset

**Actions**:
1. Identify which criteria CAN be met
2. Implement partial solution
3. Document limitations
4. Mark as PARTIAL with notes
5. Create follow-up stories for remaining criteria

**Example**:
```
Original:
US-003: Add comprehensive input validation
- Email format validation
- Password strength (8+ chars, mixed case, numbers, symbols)
- Username uniqueness check
- Rate limiting

After escape hatch:
US-003: PARTIAL - Email validation and basic password check implemented
US-011: Add password strength requirements
US-012: Add username uniqueness check
US-013: Add rate limiting
```

## When All Stories Are Blocked

The nuclear escape hatch - when nothing can progress.

**Trigger**: Every non-completed story is BLOCKED

**Actions**:
1. DO NOT output false completion promise
2. Create comprehensive summary in progress.md
3. List all blockers with details
4. Suggest next steps for human
5. Let loop continue until max iterations (human can cancel)

**Progress.md Entry**:
```markdown
## LOOP BLOCKED - Human Intervention Needed

All remaining stories are blocked. Summary:

### US-003: Payment Integration
- Blocked by: API credentials not working
- Needed: Contact payment provider or check IP whitelist

### US-007: Email Service
- Blocked by: SMTP server rejecting connections
- Needed: Verify SMTP credentials and server configuration

### Suggestions for Human
1. Check with DevOps about API credentials
2. Verify SMTP configuration in staging environment
3. Consider using mock services for development

Loop will continue until max iterations or /cancel-ralph.
Do NOT output completion promise until blockers resolved.
```

## Escape Hatch Decision Tree

```
Is issue blocking other stories?
├── Yes → Can it be worked around temporarily?
│   ├── Yes → Document workaround, continue, create follow-up story
│   └── No → Mark as BLOCKED, attempt next non-dependent story
└── No → Is there an alternative approach?
    ├── Yes → Document original approach, try alternative (reset attempts)
    └── No → Can requirements be simplified?
        ├── Yes → Implement simplified version, mark PARTIAL
        └── No → Mark as BLOCKED, move to next story
```

## Anti-Patterns

### Never Do These

1. **False Completion Promise**
   - NEVER output completion promise just to escape the loop
   - This defeats the entire purpose of Ralph

2. **Silent Failure**
   - NEVER skip a story without documenting why
   - Future iterations need to know what happened

3. **Endless Retry**
   - NEVER try the same approach more than 3 times
   - Definition of insanity: same action, expecting different result

4. **Blame Without Evidence**
   - NEVER mark as blocked without documenting what was tried
   - "It just doesn't work" is not acceptable documentation

5. **Premature Escalation**
   - NEVER mark as blocked after only 1 attempt
   - Give genuine effort before triggering escape hatch

## Recovery After Escape

When returning to a blocked story later:

1. Read the documented issue carefully
2. Check if external factors have changed
3. Try the alternative approaches suggested
4. If resolved, update status and continue
5. If still blocked, add new learnings to documentation

**Progress.md Pattern**:
```markdown
## Learnings (append-only)

[Iteration 20] Returning to US-007 (was blocked on API credentials)
[Iteration 20] Credentials now working after DevOps updated IP whitelist
[Iteration 21] US-007 implemented successfully
```
