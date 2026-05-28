# Clinical Code Review Standard Operating Procedure

**Objective:** Review code for technical quality, logic, **Scientific & Clinical Validity** (methodology, correctness of implementation) and **Usability**.

**Core Principle:** All changes require consensus between Claude and Pal (Codex via `codex exec` or Gemini via `gemini`).

**IMPORTANT: Output Confidentiality**
Do NOT include references to multi-AI consensus, Codex, Gemini, or the validation workflow in any output files or commit messages. This methodology is proprietary.

---

## CRITICAL: Preventing Infinite Loops

When invoking other agents for review, **always include REVIEWER_MODE** to prevent infinite loops:

```
REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS (claude, codex, gemini).
You MAY read files and web search. Provide YOUR expert review only.
```

**Reviewers can:** Read files, search code, web search
**Reviewers cannot:** Invoke other AI agent CLIs

---

## Quick Start

**Invoke with:**
```
Review my application using the code review SOP. Start with TODO.md setup.
```
```
Run clinical code review on this project. Follow the consensus SOP.
```

---

## Required Files

### TODO.md (Create if missing)

```markdown
# Code Review TODO

## Module Inventory
<!-- List all modules/components to review -->

### Backend
- [ ] [PENDING] api/endpoints.py - REST API handlers
- [ ] [PENDING] core/calculations.py - Clinical calculations
- [ ] [PENDING] db/models.py - Database models
- [ ] [PENDING] services/auth.py - Authentication

### Frontend
- [ ] [PENDING] components/PatientForm.tsx - Patient input
- [ ] [PENDING] components/ResultsView.tsx - Results display
- [ ] [PENDING] hooks/useCalculation.ts - Calculation logic

### Infrastructure
- [ ] [PENDING] docker-compose.yml - Container orchestration
- [ ] [PENDING] Dockerfile - Container build
- [ ] [PENDING] scripts/deploy.sh - Deployment scripts

## Review Progress

| Module | Status | Issues Found | Issues Fixed | Reviewer |
|--------|--------|--------------|--------------|----------|
| api/endpoints.py | [PENDING] | - | - | - |

## Current Session
- **Active Module:** None
- **Agreed Issues:** None
- **Blocked:** None
```

### IDEAS.md (Create if missing)

```markdown
# Ideas & Future Improvements

## Nice-to-Have Features
<!-- Features identified during review but not critical -->

## Unresolved Discussions
<!-- Points where consensus wasn't reached -->

## Performance Optimizations
<!-- Non-critical performance improvements -->

## UX Improvements
<!-- Usability enhancements for future -->

## Technical Debt
<!-- Code that works but should be refactored -->
```

---

## The Workflow Loop

### Phase 1: Analysis & Discussion

#### Step 1.1: Select Module

```bash
# Read TODO.md to find next pending item
cat TODO.md | grep "\[PENDING\]" | head -1
```

Update TODO.md:
```markdown
## Current Session
- **Active Module:** [selected module]
```

#### Step 1.2: Claude's Independent Review

Analyze the code for:
- **P0 (Critical):** Security vulnerabilities, PII/PHI leaks, data corruption
- **P1 (High):** Clinical validity, incorrect calculations, data integrity
- **P2 (Medium):** Usability issues, error handling, performance
- **P3 (Low):** Code style, documentation, minor optimizations

Document findings:
```markdown
### Claude's Review: [module]

#### P0 Critical
- None / [issue description]

#### P1 High
- None / [issue description]

#### P2 Medium
- None / [issue description]

#### P3 Low
- None / [issue description]
```

#### Step 1.3: Pal's Independent Review (Codex)

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --cd "$(pwd)" \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Independent code review. Clinical context.

REVIEW FOR:
- P0: Security, PII/PHI leaks, data corruption
- P1: Clinical validity, incorrect calculations, data integrity
- P2: Usability, error handling, performance
- P3: Code style, documentation

OUTPUT FORMAT:
P0: [list or 'None']
P1: [list or 'None']
P2: [list or 'None']
P3: [list or 'None']

Code:
$(cat [MODULE_PATH])"
```

#### Step 1.4: Consensus Building

Compare findings. For disagreements:

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.

BE CONCISE. I found [ISSUE]. You didn't flag it.

Is this a valid issue? Why/why not?

Context: [PASTE_CODE_SNIPPET]

Output: VALID_ISSUE: Y/N | REASON: [one line]"
```

Iterate until agreement. Document:

```markdown
### Agreed Issues: [module]

| # | Priority | Issue | Agreed By |
|---|----------|-------|-----------|
| 1 | P1 | [description] | Claude ✓ Pal ✓ |
| 2 | P2 | [description] | Claude ✓ Pal ✓ |
```

---

### Phase 2: Implementation Strategy

#### Step 2.1: Propose Fix Plan

For each agreed issue, propose a fix:

```markdown
### Fix Plan: [module]

| # | Issue | Proposed Fix |
|---|-------|--------------|
| 1 | [issue] | [fix approach] |
| 2 | [issue] | [fix approach] |
```

#### Step 2.2: Validate Plan with Pal

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Validate fix plan.

ISSUES:
1. [issue1]
2. [issue2]

PROPOSED FIXES:
1. [fix1]
2. [fix2]

OUTPUT: For each fix: CORRECT/INCORRECT | [concern if incorrect]"
```

#### Step 2.3: Refine if Needed

If Pal raises concerns, discuss and adjust:

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.

BE CONCISE. You flagged concern with [FIX].

Alternative approach: [NEW_APPROACH]

OUTPUT: APPROVED/REJECTED | [reason]"
```

---

### Phase 3: Execution & Verification

#### Step 3.1: Apply Fixes

Implement the agreed fixes in code.

#### Step 3.2: Verify Fixes with Pal

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --cd "$(pwd)" \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Verify fixes applied correctly.

ORIGINAL ISSUES:
1. [issue1]
2. [issue2]

EXPECTED FIXES:
1. [fix1]
2. [fix2]

OUTPUT FORMAT:
| # | Issue | Fixed | Regression |
|---|-------|-------|------------|
| 1 | [issue] | Y/N | Y/N |

VERDICT: ALL_FIXED / ISSUES_REMAIN

Modified code:
$(cat [MODULE_PATH])"
```

#### Step 3.3: Iterate if Rejected

If issues remain:
1. Discuss the failure with Pal
2. Adjust the code
3. Re-verify (repeat Step 3.2)

---

### Phase 4: Completion

#### Step 4.1: Update TODO.md

```markdown
- [x] [DONE] api/endpoints.py - REST API handlers ✓
```

Update progress table:
```markdown
| api/endpoints.py | [DONE] | 3 | 3 | Claude+Pal |
```

#### Step 4.2: Log Ideas

Add any nice-to-have features or unresolved points to IDEAS.md:

```markdown
## Nice-to-Have Features
- [module]: Could add caching for performance (P3, not critical)

## Unresolved Discussions
- [module]: Disagreed on whether X is a security issue (Claude: Yes, Pal: No)
```

#### Step 4.3: Next Module

**CRITICAL:** Read this SOP again and pick the next `[PENDING]` module.

```
DO NOT STOP UNTIL ALL MODULES ARE [DONE]
```

---

## Priority Level Definitions

| Level | Name | Description | Examples |
|-------|------|-------------|----------|
| **P0** | Critical | Must fix immediately. Security/safety risk. | SQL injection, PII exposure, auth bypass, data corruption |
| **P1** | High | Clinical validity at risk. Fix before release. | Wrong dose calculation, incorrect unit conversion, invalid statistical test |
| **P2** | Medium | Affects usability/reliability. Fix soon. | Missing error handling, confusing UI, slow performance, edge case crashes |
| **P3** | Low | Quality improvements. Fix when convenient. | Code style, missing comments, minor refactoring, documentation gaps |

---

## Consensus Commands (Concise Format)

> **Note:** All commands include `REVIEWER_MODE` to prevent infinite loops.

### Initial Review Request
```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Review for P0-P3 issues. Clinical context.

Output: P0: [list] | P1: [list] | P2: [list] | P3: [list]

Code: [PASTE_CODE]"
```

### Disagreement Resolution
```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.

BE CONCISE. Is [ISSUE] valid? Output: Y/N | REASON"
```

### Fix Validation
```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.

BE CONCISE. Is fix for [ISSUE] correct? Output: Y/N | CONCERN"
```

### Fix Verification
```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Verify: [ISSUES] fixed in [CODE]? Output: FIXED/NOT_FIXED per issue"
```

---

## Full Module Review Checklist

For each module, complete:

- [ ] **1.1** Select module from TODO.md
- [ ] **1.2** Claude independent review (P0-P3)
- [ ] **1.3** Pal independent review (P0-P3)
- [ ] **1.4** Consensus on issues reached
- [ ] **2.1** Fix plan proposed
- [ ] **2.2** Fix plan validated by Pal
- [ ] **3.1** Fixes implemented
- [ ] **3.2** Fixes verified by Pal
- [ ] **3.3** All issues resolved (iterate if not)
- [ ] **4.1** Module marked [DONE] in TODO.md
- [ ] **4.2** Ideas logged to IDEAS.md
- [ ] **4.3** Next module selected

---

## Review Scope

### What to Review

**Backend:**
- API endpoints (security, validation, error handling)
- Business logic (correctness, edge cases)
- Database operations (integrity, injection risks)
- Authentication/authorization (access control)
- Clinical calculations (accuracy, units, ranges)

**Frontend:**
- Components (state management, rendering)
- Forms (validation, sanitization)
- Data display (accuracy, formatting)
- User interactions (error states, feedback)

**Infrastructure:**
- Docker configurations (security, efficiency)
- Deployment scripts (idempotency, rollback)
- Environment handling (secrets, configs)
- Dependencies (vulnerabilities, versions)

### Review Depth by Priority

| Priority | Review Depth |
|----------|--------------|
| P0 | Line-by-line analysis, threat modeling |
| P1 | Logic flow analysis, calculation verification |
| P2 | Functional testing, UX evaluation |
| P3 | Style check, documentation review |

---

## Integration with Scientific Analysis

If reviewing scientific/clinical analysis code:

1. **Statistical Methods:** Verify correct implementation of tests
2. **Data Processing:** Check for data leakage, proper validation
3. **Visualization:** Ensure figures are accurate representations
4. **Reproducibility:** Verify random seeds, versioning

Cross-reference with `analysis/plan.md` if conducting analysis review.
