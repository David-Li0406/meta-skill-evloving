# Validation Checklist Reference

Detailed checklist for each validation type with examples and commands.

---

## Pre-Validation Setup

- [ ] Spec file path provided and file exists
- [ ] Decomposition log found in `.beads/decomposition-logs/`
- [ ] All beads from log loaded via `br show <id> --json`
- [ ] Baseline structural analysis run: `bv --robot-suggest`

---

## Check 1: Self-Containment

### Required Sections Checklist

For each bead, verify presence of:

- [ ] **Task** - Clear, actionable statement starting with a verb
  - Good: "Implement JWT authentication middleware for API routes"
  - Bad: "JWT stuff" / "Authentication"

- [ ] **Acceptance Criteria** - Specific, testable criteria
  - Good: "Endpoint returns 401 for invalid tokens; verify with `curl -H 'Authorization: Bearer invalid'`"
  - Bad: "Works correctly" / "Handles errors"

### Recommended Sections Checklist

- [ ] **Background & Reasoning** - Why this exists
  - Source: Spec introduction, project goals
  - Example: "This middleware is needed because the API will serve both internal and external clients, requiring consistent authentication..."

- [ ] **Key Files** - Files to create/modify
  - Source: Task analysis, related beads
  - Example:
    ```
    - src/middleware/auth.ts - Create new middleware
    - src/routes/index.ts - Apply middleware to routes
    - tests/auth.test.ts - Add unit tests
    ```

- [ ] **Implementation Details** - Patterns, APIs, integration
  - Source: Spec technical details, existing code patterns
  - Example:
    ```typescript
    // Follow existing middleware pattern from src/middleware/logging.ts
    export function authMiddleware(req, res, next) {
      const token = req.headers.authorization?.split(' ')[1];
      // ...
    }
    ```

- [ ] **Considerations & Edge Cases** - Gotchas, security, performance
  - Source: Spec caveats, common issues
  - Example: "Token refresh edge case: If token expires mid-request, return 401 not 403"

- [ ] **Notes for Future Self** - Helpful context
  - Source: Spec footnotes, architectural decisions
  - Example: "Chose JWT over sessions because of horizontal scaling requirements"

### Fix Commands

```bash
# View current bead
br show <id>

# Update with enhanced description
br update <id> --description="## Task
Implement JWT authentication middleware...

## Background & Reasoning
...

## Key Files
...

## Implementation Details
...

## Acceptance Criteria
- [ ] Criterion 1...

## Considerations & Edge Cases
...

## Notes for Future Self
..."
```

---

## Check 2: Spec Coverage

### Process Checklist

- [ ] Spec parsed into discrete requirements
- [ ] Each requirement searched with `bv --search`
- [ ] Coverage mapping created
- [ ] Gaps identified
- [ ] Missing beads created for gaps

### Semantic Search Commands

```bash
# Search for matching beads
bv --search "user authentication with email" --robot-search --search-limit=5

# Example output interpretation:
# - Score > 0.7: Covered
# - Score 0.4-0.7: Partially covered, review manually
# - Score < 0.4: Not covered, create bead
```

### Coverage Mapping Template

```markdown
| # | Spec Requirement | Search Query | Best Match | Score | Status |
|---|------------------|--------------|------------|-------|--------|
| 1 | "Users can log in with email and password" | "user login email password" | br-101 | 0.85 | Covered |
| 2 | "Password reset via email link" | "password reset email" | - | 0.20 | GAP |
| 3 | "Session timeout after 24 hours" | "session timeout expiration" | br-103 | 0.72 | Covered |
```

### Gap-Filling Commands

```bash
# Create new bead for uncovered requirement
br create \
  --title="Implement password reset via email" \
  --type=task \
  --priority=2 \
  --description="## Task
Implement password reset flow with email verification link.

## Background & Reasoning
Spec requirement 2.3 states users must be able to reset their password via email...

## Key Files
- src/routes/auth/reset.ts - New route handler
- src/services/email.ts - Add reset email template
- src/models/user.ts - Add resetToken field

## Implementation Details
...

## Acceptance Criteria
- [ ] POST /auth/reset-password accepts email, sends reset link
- [ ] Reset link expires after 1 hour
- [ ] Clicking link allows new password entry
- [ ] Tests pass: npm test -- --grep 'password reset'

## Considerations & Edge Cases
- Rate limit reset requests (max 3 per hour per email)
- Use secure random for reset token
..."

# Add dependencies
br dep add <new-bead-id> <email-service-bead-id>
```

---

## Check 3: Orphan Detection

### Process Checklist

- [ ] Each bead mapped to spec requirement
- [ ] Supporting beads identified (infrastructure, utilities)
- [ ] True orphans flagged
- [ ] Orphans resolved (documented or removed)

### Classification Guide

| Bead Type | Spec Mention | Classification | Action |
|-----------|--------------|----------------|--------|
| Feature bead | Direct match | Valid | None |
| Feature bead | No match | Orphan | Remove or document |
| Infrastructure | Implied by features | Supporting | Add supporting note |
| Utility | Used by multiple features | Supporting | Add supporting note |
| Infrastructure | Not implied | Orphan | Remove or document |

### Orphan Resolution

```bash
# Option 1: Document as supporting
br update <id> --description="...

## Notes for Future Self
This infrastructure bead supports spec requirements 2.1, 2.3, and 3.2 by providing
the database connection layer needed for user data persistence.
"

# Option 2: Remove true orphan
br delete <id>
```

---

## Check 4: Dependency Validity

### bv Analysis Commands

```bash
# Full suggestion scan
bv --robot-suggest

# Cycle detection
bv --robot-suggest --suggest-type=cycle

# Missing dependency suggestions
bv --robot-suggest --suggest-type=dependency

# Duplicate detection
bv --robot-suggest --suggest-type=duplicate

# Related beads (file/commit overlap)
bv --robot-related <bead-id>
```

### Issue Resolution Checklist

- [ ] **Cycles detected**: Report for manual review
- [ ] **Missing dependencies (confidence > 0.7)**: Auto-add
- [ ] **Missing dependencies (confidence < 0.7)**: Review manually
- [ ] **Reversed epic dependencies**: Fix direction
- [ ] **Duplicates**: Merge or flag

### Epic Direction Verification

```bash
# List all epics
br list --type=epic --json

# For each epic, verify children are NOT blocked by epic
# WRONG (children blocked):
#   br-100 (epic) → br-101 (child) should be a dependency
#   means br-101 depends on br-100 (WRONG!)

# CORRECT (epic blocked by children):
#   br-100 (epic) depends on br-101 (child)
#   means br-100 is blocked until br-101 is done
```

### Dependency Fix Commands

```bash
# Remove wrong dependency
br dep remove <child-id> <epic-id>

# Add correct dependency
br dep add <epic-id> <child-id>

# Add missing dependency (high confidence)
br dep add <dependent-id> <dependency-id>
```

---

## Post-Validation

### Log Update Checklist

- [ ] Update decomposition log with validation pass section
- [ ] Include timestamp
- [ ] Document all issues found
- [ ] Document all fixes applied
- [ ] Note any user clarifications gathered
- [ ] List remaining issues for manual review

### Final Verification

- [ ] All required sections present in every bead
- [ ] All spec requirements covered
- [ ] No unexplained orphan beads
- [ ] No cycles (or cycles documented for manual review)
- [ ] Epic dependencies point correct direction
- [ ] Decomposition log updated with validation results
