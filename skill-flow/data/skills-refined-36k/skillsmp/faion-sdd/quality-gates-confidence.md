---
id: quality-gates-confidence
name: "Quality Gates & Confidence Checks"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Quality Gates & Confidence Checks

## Metadata

| Field | Value |
|-------|-------|
| **ID** | quality-gates-confidence |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #quality, #confidence |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-hallucination-checker-agent |

---

## Problem

Projects suffer from quality issues when:
- Bugs slip into production because testing was rushed
- AI-generated code contains hallucinations or errors
- Code review is inconsistent or skipped
- No clear criteria for "done"

**The root cause:** No systematic quality checkpoints.

---

## Framework

### What are Quality Gates?

Quality gates are checkpoints where work must meet specific criteria before proceeding. Think of them as security checkpoints at an airport - you can't board without passing.

### Quality Gate Types

| Gate | When | What's Checked |
|------|------|----------------|
| **Spec Review** | Before design starts | Requirements complete, testable |
| **Design Review** | Before implementation | Architecture sound, complete |
| **Code Review** | Before merge | Code quality, standards |
| **Test Gate** | Before deploy | All tests pass |
| **Deploy Gate** | Before production | Staging verified |

### Confidence Levels

For AI-assisted development, track confidence in outputs:

| Level | Score | Meaning | Action |
|-------|-------|---------|--------|
| **High** | 90-100% | Very confident, verified | Proceed |
| **Medium** | 70-89% | Likely correct, needs review | Review before use |
| **Low** | 50-69% | Uncertain, may have issues | Deep review required |
| **Very Low** | <50% | Probably wrong | Regenerate or manual fix |

### The Quality Gate Process

```
WORK → CHECK → GATE → PROCEED
         ↓       ↓
      ISSUES → FIX → RE-CHECK
```

1. **Work:** Complete the task
2. **Check:** Run automated checks (tests, linters)
3. **Gate:** Evaluate against criteria
4. **Proceed:** If pass, move forward
5. **Fix:** If fail, address issues
6. **Re-check:** Verify fixes, re-evaluate

---

## Templates

### Quality Gate Checklist Template

```markdown
## Quality Gate: [Gate Name]

**Phase:** [Spec/Design/Implementation/Deploy]
**Date:** YYYY-MM-DD
**Reviewer:** [Name]

### Pass Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Automated Checks

| Check | Status | Details |
|-------|--------|---------|
| Linter | PASS/FAIL | [Details] |
| Tests | PASS/FAIL | X/Y passed |
| Coverage | PASS/FAIL | X% (min Y%) |
| Build | PASS/FAIL | [Details] |

### Manual Review

| Item | Status | Notes |
|------|--------|-------|
| Code quality | OK/ISSUE | [Notes] |
| Security | OK/ISSUE | [Notes] |
| Performance | OK/ISSUE | [Notes] |
| Documentation | OK/ISSUE | [Notes] |

### Issues Found

| ID | Severity | Description | Status |
|----|----------|-------------|--------|
| 1 | High/Med/Low | [Description] | Fixed/Open |

### Decision

- [ ] **PASS** - Proceed to next phase
- [ ] **PASS WITH CONDITIONS** - Proceed after [condition]
- [ ] **FAIL** - Return to [phase] to address issues

### Signatures

- Reviewer: ________________ Date: ________
- Author: __________________ Date: ________
```

### Spec Review Gate

```markdown
## Quality Gate: Specification Review

### Pass Criteria

- [ ] Problem statement is clear and specific
- [ ] All user personas identified
- [ ] Each functional requirement has unique ID
- [ ] Each requirement is testable
- [ ] Non-functional requirements address performance, security
- [ ] Acceptance criteria use Given-When-Then format
- [ ] Out of scope is explicitly listed
- [ ] No conflicting requirements
- [ ] Dependencies documented

### Review Questions

1. Can a developer understand WHAT to build from this spec?
2. Can QA write tests from the acceptance criteria?
3. Are edge cases considered?
4. Is scope realistic for timeline?
```

### Design Review Gate

```markdown
## Quality Gate: Design Review

### Pass Criteria

- [ ] All spec requirements addressed
- [ ] Architecture decisions documented with rationale
- [ ] File structure specified (CREATE/MODIFY)
- [ ] Data models defined
- [ ] API contracts specified (if applicable)
- [ ] Dependencies listed with versions
- [ ] Security considerations documented
- [ ] Testing strategy defined
- [ ] No technology choices without justification

### Review Questions

1. Can a developer implement from this design alone?
2. Are there any obvious scalability issues?
3. Are security best practices followed?
4. Will this design handle the NFRs?
```

### Code Review Gate

```markdown
## Quality Gate: Code Review

### Automated Checks

- [ ] Linter passes (ESLint/Pylint/etc.)
- [ ] Formatter applied (Prettier/Black/etc.)
- [ ] Type checks pass (TypeScript/mypy)
- [ ] Unit tests pass
- [ ] Coverage meets minimum (>80%)
- [ ] No security vulnerabilities (Snyk/Dependabot)

### Manual Review

- [ ] Code follows project conventions
- [ ] Functions are small (<50 lines)
- [ ] No code duplication
- [ ] Error handling is complete
- [ ] Edge cases covered
- [ ] Comments explain WHY, not WHAT
- [ ] No hardcoded secrets
- [ ] Performance acceptable

### Security Checklist

- [ ] Input validation present
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Authentication/authorization correct
- [ ] Sensitive data encrypted
- [ ] Logging doesn't include secrets
```

### Confidence Check Template

```markdown
## Confidence Check: [Task/Output]

**Date:** YYYY-MM-DD
**Author/Source:** [Human/AI Agent]

### Confidence Assessment

| Aspect | Confidence | Notes |
|--------|------------|-------|
| Correctness | High/Med/Low | [Notes] |
| Completeness | High/Med/Low | [Notes] |
| Best Practices | High/Med/Low | [Notes] |
| Security | High/Med/Low | [Notes] |
| Performance | High/Med/Low | [Notes] |

### Overall Confidence: [X]%

### Evidence

- [x] Tested manually
- [x] Unit tests pass
- [ ] Reviewed by human
- [ ] Compared to reference implementation
- [ ] Verified against documentation

### Verification Steps Taken

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Areas of Uncertainty

- [Area 1]: [Why uncertain]
- [Area 2]: [Why uncertain]

### Recommendation

- [ ] Use as-is (high confidence)
- [ ] Use after review (medium confidence)
- [ ] Regenerate/rework (low confidence)
```

---

## Examples

### Example: AI Code Confidence Check

**Scenario:** AI agent generated authentication middleware.

```markdown
## Confidence Check: Auth Middleware

**Source:** faion-code-agent
**Task:** TASK-010 - Implement auth middleware

### Confidence Assessment

| Aspect | Confidence | Notes |
|--------|------------|-------|
| Correctness | Medium (75%) | Logic looks right, needs testing |
| Completeness | High (90%) | All requirements covered |
| Best Practices | Medium (70%) | JWT handling standard |
| Security | Medium (65%) | Need to verify token validation |
| Performance | High (85%) | Simple middleware, no concerns |

### Overall Confidence: 77%

### Evidence

- [x] Code compiles without errors
- [x] Unit tests written and pass
- [ ] Reviewed by human ← NEEDED
- [x] Compared to Express middleware patterns
- [x] Verified JWT library usage

### Areas of Uncertainty

1. **Token expiration handling:** Not sure if edge cases covered
2. **Error messages:** May leak information
3. **Rate limiting:** Not implemented, spec was unclear

### Verification Steps Needed

1. Human review of security aspects
2. Test with expired tokens
3. Test with malformed tokens
4. Confirm rate limiting requirements

### Recommendation

- [ ] Use as-is
- [x] Use after review - human should verify security
- [ ] Regenerate/rework
```

### Example: Quality Gate Failure

```markdown
## Quality Gate: Code Review - FAILED

**PR:** #123 - Add user registration
**Date:** 2026-01-17

### Automated Checks

| Check | Status | Details |
|-------|--------|---------|
| Linter | PASS | No issues |
| Tests | FAIL | 2/15 failed |
| Coverage | PASS | 85% |
| Build | PASS | Successful |

### Issues Found

| ID | Severity | Description | Status |
|----|----------|-------------|--------|
| 1 | High | Password validation test fails | Open |
| 2 | High | Email duplicate check test fails | Open |
| 3 | Medium | Missing error handling for DB timeout | Open |

### Decision

- [ ] PASS
- [ ] PASS WITH CONDITIONS
- [x] FAIL - Fix failing tests before re-review

### Action Items

1. Fix password validation (min 8 chars not enforced)
2. Fix email duplicate detection (case sensitivity)
3. Add try-catch for database operations
4. Re-run all tests
5. Request re-review
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping gates under time pressure | Gates exist for a reason - bugs cost more later |
| Vague pass criteria | Make every criterion specific and testable |
| No automated checks | Automate everything that can be automated |
| 100% confidence claims | Even experts have uncertainty - be honest |
| Ignoring low-confidence areas | Address them before production |

---

## Related Methodologies

- **task-creation-parallelization:** Task Creation & Parallelization
- **reflexion-learning:** Reflexion & Learning
- **code-review:** Code Review Best Practices
- **testing-strategies:** Testing Strategies

---

## Agent

**faion-hallucination-checker-agent** verifies AI outputs. Invoke with:
- "Check confidence of this code"
- "Review for hallucinations"
- "Run quality gate for [phase]"

---

*Methodology | SDD Foundation | Version 1.0*
