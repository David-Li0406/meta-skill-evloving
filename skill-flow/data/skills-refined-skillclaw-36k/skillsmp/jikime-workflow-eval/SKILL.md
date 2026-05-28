---
name: jikime-workflow-eval
description: Eval-Driven Development (EDD) framework - treat evals as unit tests for AI development
version: 1.0.0
tags: ["workflow", "eval", "edd", "testing", "quality", "metrics"]
triggers:
  keywords: ["eval", "pass@k", "regression eval", "capability eval", "EDD", "평가"]
  phases: ["plan", "run"]
  agents: ["manager-spec", "manager-ddd", "test-guide"]
  languages: []
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~8000
user-invocable: false
context: fork
agent: manager-ddd
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Eval-Driven Development (EDD) Skill

A comprehensive evaluation framework for AI-assisted development, treating evals as "unit tests for AI."

## Philosophy

```
Traditional TDD:    Write tests → Implement → Verify
Eval-Driven (EDD):  Define evals → Implement → Measure pass@k
```

### Why EDD?

1. **Clarity**: Define success criteria BEFORE coding
2. **Measurability**: Track reliability with pass@k metrics
3. **Confidence**: Regression evals prevent behavior degradation
4. **Iteration**: Multiple attempts are expected and measured

---

## Eval Types

### 1. Capability Evals

Test NEW functionality that doesn't exist yet:

```markdown
## CAPABILITY EVAL: user-authentication

### Task
Implement user authentication with email/password

### Success Criteria
- [ ] User can register with valid email and password
- [ ] Password is hashed using bcrypt (cost factor 12)
- [ ] Invalid email format is rejected with clear error
- [ ] Weak passwords are rejected with strength requirements
- [ ] Duplicate email registration is prevented

### Grader: code
Commands:
  - npm test -- --testPathPattern="auth"
  - grep -q "bcrypt" src/auth/password.ts

### Expected pass@k
Target: pass@3 > 90%
```

### 2. Regression Evals

Ensure EXISTING functionality still works (DDD PRESERVE phase):

```markdown
## REGRESSION EVAL: user-authentication

### Baseline
Commit: abc123def
SPEC: SPEC-042

### Tests
- [ ] Login with valid credentials → 200 OK
- [ ] Login with invalid password → 401 Unauthorized
- [ ] Session persists across requests
- [ ] Logout clears session

### Grader: code
Commands:
  - npm test -- --testPathPattern="auth.existing"

### Expected pass^k
Target: pass^3 = 100% (MANDATORY for merge)
```

### 3. Quality Evals (TRUST 5)

Verify quality principles are maintained:

```markdown
## QUALITY EVAL: user-authentication

### TRUST 5 Criteria

**Tested**
- [ ] Unit test coverage > 80%
- [ ] Integration tests exist
- [ ] Edge cases covered

**Readable**
- [ ] No functions > 50 lines
- [ ] Clear naming conventions
- [ ] Self-documenting code

**Unified**
- [ ] Consistent error handling pattern
- [ ] Follows project architecture
- [ ] Uses established abstractions

**Secured**
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] OWASP top 10 addressed

**Trackable**
- [ ] Structured logging
- [ ] Error context preserved
- [ ] Audit trail for auth events

### Grader: code + lsp
Commands:
  - npm run coverage
  - npx tsc --noEmit
  - npm run lint
```

---

## Grader Implementation

### Code Grader (Deterministic)

Execute bash commands and check exit codes:

```bash
# Grader script pattern
run_code_grader() {
  local eval_name=$1
  local command=$2

  if eval "$command" > /dev/null 2>&1; then
    echo "PASS"
    return 0
  else
    echo "FAIL"
    return 1
  fi
}

# Examples
run_code_grader "build" "npm run build"
run_code_grader "types" "npx tsc --noEmit"
run_code_grader "pattern" "grep -q 'export function' src/auth.ts"
```

### Model Grader (Claude Self-Assessment)

For open-ended evaluation:

```markdown
[MODEL GRADER PROMPT]
Evaluate the implementation against these criteria:

1. Does it solve the stated problem completely?
2. Is the code well-structured and maintainable?
3. Are edge cases handled appropriately?
4. Is error handling robust?
5. Does it follow project conventions?

Score: 1-5 (1=major issues, 5=excellent)
Issues Found: [list any problems]
Recommendation: PASS (score >= 4) / FAIL (score < 4)
```

### LSP Grader (Quality Gates)

Use LSP diagnostics for quality checks:

```typescript
// LSP grader checks
interface LSPGraderResult {
  errors: number;
  warnings: number;
  typeErrors: number;
  lintErrors: number;
  passed: boolean;
}

// Thresholds from quality.yaml
const thresholds = {
  max_errors: 0,
  max_type_errors: 0,
  max_lint_errors: 0,
  max_warnings: 10
};
```

### Human Grader (Flag for Review)

For security, UX, or subjective evaluation:

```markdown
[HUMAN REVIEW REQUIRED]
Eval: security-audit
Risk Level: HIGH
Reason: New authentication flow requires security review
Reviewer: @security-team
Checklist:
  - [ ] No SQL injection vectors
  - [ ] Session handling secure
  - [ ] Rate limiting implemented
  - [ ] Audit logging complete
```

---

## Metrics Deep Dive

### pass@k (Reliability Metric)

"Probability of at least one success in k attempts"

```
pass@1 = (successful_first_attempts) / (total_evals)
pass@3 = (evals_with_at_least_one_success_in_3_tries) / (total_evals)

Example:
  Eval 1: PASS (1st try)     → pass@1=1, pass@3=1
  Eval 2: FAIL, PASS (2nd)   → pass@1=0, pass@3=1
  Eval 3: FAIL, FAIL, PASS   → pass@1=0, pass@3=1
  Eval 4: FAIL, FAIL, FAIL   → pass@1=0, pass@3=0

  Overall:
    pass@1 = 1/4 = 25%
    pass@3 = 3/4 = 75%
```

### pass^k (Consistency Metric)

"All k consecutive attempts must succeed"

```
pass^3 = (evals_with_3_consecutive_successes) / (total_evals)

Use for:
  - Regression evals (MUST be 100%)
  - Critical path validation
  - Production readiness

Example:
  Eval 1: PASS, PASS, PASS → pass^3=1
  Eval 2: PASS, FAIL, PASS → pass^3=0 (not consecutive)
```

### Trend Analysis

Track metrics over time for improvement visibility:

```json
{
  "eval": "auth-system",
  "trend": [
    {"iteration": 1, "pass@3": 0.33, "pass^3": 0.00},
    {"iteration": 2, "pass@3": 0.67, "pass^3": 0.33},
    {"iteration": 3, "pass@3": 1.00, "pass^3": 0.67},
    {"iteration": 4, "pass@3": 1.00, "pass^3": 1.00}
  ],
  "ready_at_iteration": 4
}
```

---

## Integration with JikiME Workflows

### SPEC Integration

```
SPEC-042: User Authentication
    ↓
/jikime:eval define user-auth --auto-suggest
    ↓
Evals extracted from SPEC requirements:
  - Capability: Login, Register, Logout
  - Regression: Existing session handling
  - Quality: TRUST 5 compliance
```

### DDD Integration

```
ANALYZE phase:
  → Load regression evals from existing behavior
  → Baseline captured in .jikime/evals/baselines/

PRESERVE phase:
  → Run regression evals (pass^3 = 100% REQUIRED)
  → Any regression → STOP and fix

IMPROVE phase:
  → Run capability evals
  → Iterate until pass@3 > 90%
```

### Orchestrator Integration

**J.A.R.V.I.S.** (Development):
```
Eval check integrated into iteration cycle:
  - Phase 1: Implement
  - Phase 2: /jikime:eval check → metrics reported
  - Phase 3: If pass@3 < 90%, iterate
  - Phase 4: When pass@3 >= 90%, proceed
```

**F.R.I.D.A.Y.** (Migration):
```
Module-by-module eval tracking:
  - Each module has behavior preservation evals
  - pass^3 = 100% required before next module
  - Migration complete when all modules pass
```

---

## Eval Definition Template

```markdown
# EVAL: {{eval-name}}

Created: {{date}}
SPEC: {{spec-id or N/A}}
Status: DRAFT | ACTIVE | ARCHIVED

## Capability Evals

### 1. {{capability-name}}
**Task**: {{description}}
**Criteria**:
- [ ] {{criterion-1}}
- [ ] {{criterion-2}}
**Grader**: code | model | human
**Commands**: {{if code grader}}

### 2. {{capability-name-2}}
...

## Regression Evals

### 1. {{regression-name}}
**Baseline**: {{commit or spec}}
**Tests**:
- [ ] {{existing-behavior-1}}
- [ ] {{existing-behavior-2}}
**Grader**: code
**Commands**: {{test commands}}

## Quality Evals

### TRUST 5 Compliance
- [ ] Tested: {{criteria}}
- [ ] Readable: {{criteria}}
- [ ] Unified: {{criteria}}
- [ ] Secured: {{criteria}}
- [ ] Trackable: {{criteria}}

## Success Metrics

| Eval Type | Target |
|-----------|--------|
| Capability | pass@3 > 90% |
| Regression | pass^3 = 100% |
| Quality | All checks pass |

## Notes

{{any additional context}}
```

---

## Best Practices

### DO

1. **Define evals BEFORE implementation** - Forces clear thinking
2. **Use code graders when possible** - Deterministic > probabilistic
3. **Track pass@k over time** - Visibility into reliability
4. **Run evals frequently** - Catch regressions early
5. **Version evals with code** - Evals are first-class artifacts
6. **Keep evals fast** - Slow evals don't get run

### DON'T

1. **Skip regression evals** - They catch breaking changes
2. **Use only model graders** - Too non-deterministic
3. **Define vague criteria** - Must be measurable
4. **Ignore failing evals** - Fix or update criteria
5. **Over-engineer evals** - Keep them simple and focused

---

## Storage Structure

```
.jikime/
├── evals/
│   ├── auth-system.md          # Eval definition
│   ├── auth-system.log         # Run history
│   ├── auth-system.json        # Metrics tracking
│   ├── payment-flow.md
│   ├── payment-flow.log
│   ├── payment-flow.json
│   └── baselines/
│       ├── auth-system.json    # Regression baseline
│       └── payment-flow.json
```

---

## Works Well With

- `jikime-workflow-ddd`: DDD methodology (ANALYZE-PRESERVE-IMPROVE)
- `jikime-workflow-testing`: Test execution and coverage
- `jikime-foundation-core`: SPEC system and workflows
- `jikime-workflow-verify`: Comprehensive verification
- `jikime-workflow-spec`: SPEC document creation

---

Last Updated: 2026-01-25
Version: 1.0.0
Methodology: Eval-Driven Development (EDD)
Integration: DDD, SPEC, TRUST 5, J.A.R.V.I.S./F.R.I.D.A.Y.
