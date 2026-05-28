# Performing Code Reviews: Working Notes for Skill Discovery

Working notes from discovery sessions reviewing:
- `/Users/cyarie/Code/goals/trackman/trackman/storage` module
- `/Users/cyarie/Code/goals/trackman/trackman/cli` module

---

## Skill Development Notes

### Insight 1: Verification Tools Are Table Stakes

Verification commands must run and pass. If tools aren't installed or configured, **the review fails** — not because the code is bad, but because the project lacks the infrastructure for maintainable code.

- Tests: Must exist and pass
- Linter (ruff or equivalent): Must be configured and pass
- Type checker (mypy): Must be configured and pass

Missing any of these is itself a Critical issue.

**Skill implication**: Verification tool availability is a quality gate. Missing tools = automatic fail with "configure tooling" as the required fix.

### Insight 2: Skills Provide Review Lenses

Each loaded skill becomes a "lens" through which to view the code:
- `designing-software` → Is this well-architected? Clean separation?
- `defensive-coding` → Are boundaries validated? Error handling adequate?
- `writing-useful-tests` → Tests testing real behavior? Coverage gaps?
- `howto-code-in-python` → Google Python style followed?

Without explicit skill loading, entire categories of issues are missed.

**Skill implication**: The skill should enumerate which lenses to apply and what questions each lens asks.

### Insight 3: Issue Categorization Requires Explicit Criteria

I naturally sorted issues into Critical/Important/Minor, but needed criteria. The reference model provides:
- **Critical**: Failing tests, security issues, type violations, missing error handling, **missing tooling infrastructure**
- **Important**: Code organization, incomplete documentation, performance
- **Minor**: Naming improvements, style preferences, refactoring opportunities

**Skill implication**: The skill must define explicit categorization criteria so reviewers are consistent.

### Insight 4: Tests Need Their Own Review Pass

Looking at tests separately from code revealed gaps:
- No `exists()` returning False test
- No `get_by_club()` test
- No invalid format error test

This is a distinct review activity from reviewing implementation.

**Skill implication**: The skill should have a separate "test coverage review" step that compares public methods against existing tests.

### Insight 5: Defensive Coding Requires Specific Questions

Without the "defensive coding" lens, I might not have noticed:
- Missing key validation in `repository.py`
- Missing encoding in `import_service.py`
- No try/except around JSON parsing

Each skill provides specific things to look for.

**Skill implication**: When loading a skill, extract its "review questions" and apply them systematically.

### Insight 6: Output Template Forces Completeness

Having a required output template means you can't skip sections. The template itself is a checklist.

**Skill implication**: The skill must provide the exact output template, not just guidelines.

### Insight 7: Verification Evidence Section Builds Trust

Stating what verification was run (and its results) lets the reader know this wasn't a superficial review.

**Skill implication**: Always include verification evidence. Failed or missing tools are Critical issues.

### Insight 8: "Skills Applied" Section Shows Rigor

Listing which skills were applied demonstrates the review was systematic, not ad-hoc.

**Skill implication**: Require listing which skills were loaded and applied.

### Insight 9: Python-Specific Patterns Emerge

Several issues were Python-specific:
- `encoding="utf-8"` on file opens
- Sentinel pattern typing (`object` vs `Literal`)
- Raw index access vs named columns

**Skill implication**: Language-specific skills should be loaded based on file types being reviewed.

### Insight 10: Duplication Patterns Reveal Extraction Opportunities

The repeated database session pattern (init → connect → try → finally close) appeared in 4 CLI commands. This wasn't visible until reviewing multiple files together.

**Skill implication**: Review should explicitly look for cross-file patterns, not just within-file issues.

### Insight 11: Test Coverage Comparison Requires File-to-Test Mapping

I noticed `import_cmd.py` and `query_cmd.py` had no tests only because I checked which test files existed. This should be a systematic step.

**Skill implication**: Add explicit step: "For each source file, verify corresponding test file exists."

### Insight 12: Consistency Across Similar Commands

The `Optional` vs `str | None` inconsistency and the required vs optional argument patterns were visible because I reviewed related files together.

**Skill implication**: When reviewing a module, compare similar components for consistency.

---

## Questions and Resolutions

### Question: What happens if verification tools aren't available?

**Options considered**: Skip verification / Report failure / Block review

**Resolution**: **Block review.** Missing linter, type checker, or tests is a Critical infrastructure issue. Code review cannot proceed until tooling is in place. These tools are table stakes for maintainable code.

**Skill implication**: Missing verification tools = automatic Critical issue. Review is blocked until fixed.

### Question: Which skills to load and in what order?

**Options considered**: Load all / Load based on file type / Load based on review focus

**Resolution**: Load a core set always (`designing-software`, `defensive-coding`, `writing-useful-tests`) plus language-specific skills based on file types being reviewed.

**Skill implication**: Skill should specify the loading order and logic for language detection.

### Question: How strict on output template?

**Options considered**: Exact template / Flexible structure / Just guidelines

**Resolution**: Exact template enforces completeness. Flexibility leads to omissions.

**Skill implication**: Provide exact template; require all sections even if "None found."

---

## Cross-Skill Notes

- **`howto-code-in-python`**: Should mention `encoding="utf-8"` explicitly in file I/O section
- **`writing-useful-tests`**: Could add "coverage gap analysis" guidance — comparing public methods to test coverage
- **`defensive-coding`**: Add explicit guidance on JSON/dict key validation

---

## Process Summary: Performing Code Reviews

### Purpose

Systematic code review that:
- Enforces verification tooling as table stakes
- Loads relevant skills as review lenses
- Categorizes issues consistently
- Produces structured, actionable output

### Inputs Required

Before starting, you need:
- **Code to review** (file paths or module)
- **Context** (is this new feature? bug fix? refactor?)
- **Any plan or requirements** to compare against

### Step-by-Step Process

#### Step 1: Load Skills

Load skills in this order:
1. `designing-software` — architecture lens
2. `defensive-coding` — boundary validation lens
3. `writing-useful-tests` — test quality lens
4. Language-specific skill(s) based on file types (e.g., `howto-code-in-python`)
5. `technical-writing` — for clear review output

#### Step 2: Run Verification Commands

Run and document:
- **Test suite** (`pytest`, `npm test`, etc.) — REQUIRED
- **Linter** (`ruff`, `eslint`, etc.) — REQUIRED
- **Type checker** (`mypy`, `tsc`, etc.) — REQUIRED
- Build (if applicable)

**If any required tool is missing or not configured:**
- Stop the review
- Report a Critical issue: "Missing [tool] configuration"
- Block until tooling is configured

This is non-negotiable. Type checking and linting are table stakes for maintainable code.

#### Step 3: Review Implementation

Apply each loaded skill as a lens:

**From `designing-software`**:
- Is architecture appropriate for the problem?
- Are concerns properly separated?
- Are abstractions at the right level?

**From `defensive-coding`**:
- Are inputs validated at boundaries?
- Is error handling appropriate?
- Are resources properly managed?

**From language skill**:
- Does code follow style conventions?
- Are idioms used correctly?
- Are there language-specific gotchas?

#### Step 4: Review Tests

Separately review test coverage:
- List all public methods/functions
- Check each has corresponding test(s)
- Verify tests test real behavior (not mocks)
- Check error paths and edge cases

#### Step 5: Categorize Issues

Classify each finding:

| Category | Criteria |
|----------|----------|
| **Critical** | Failing tests, security issues, data corruption risk, missing error handling, **missing verification tooling** |
| **Important** | Code organization, performance concerns, missing tests, documentation gaps |
| **Minor** | Style preferences, naming suggestions, refactoring opportunities |

#### Step 6: Produce Structured Output

Use the exact template (see Output Format below).

### Output Format

```markdown
# Code Review: [Component/Feature Name]

## Status
**[APPROVED / BLOCKED - CHANGES REQUIRED]**

## Issue Summary
**Critical: [count] | Important: [count] | Minor: [count]**

## Verification Evidence
- Tests: [command] → [results]
- Linter: [command] → [results] (REQUIRED - if missing, Critical issue)
- Type checker: [command] → [results] (REQUIRED - if missing, Critical issue)

## Skills Applied
- [skill name]: [what it was used to check]

## Critical Issues (count: N)
[For each:]
### N. [Issue title]
**Location**: `file:line` or "Project configuration"
**Issue**: [What's wrong]
**Impact**: [Why it matters]
**Fix**: [How to resolve]

## Important Issues (count: N)
[Same format]

## Minor Issues (count: N)
[Same format]

## Decision
**[APPROVED / BLOCKED - CHANGES REQUIRED]**

[If blocked]: Fix Critical issues before merge. Any Critical issue = blocked.
[If approved]: All quality gates met.
```

### Validation Checks

Before finalizing:
- [ ] All verification tools present and passing (Critical if not)
- [ ] All loaded skills applied as review lenses
- [ ] Test coverage gaps identified
- [ ] Every issue has Location, Issue, Impact, Fix
- [ ] Issues correctly categorized
- [ ] Decision matches issue severity (any Critical = blocked)

---

## Example Review (from this session)

The `/Users/cyarie/Code/goals/trackman/trackman/storage` module review would be:

**Status**: BLOCKED - CHANGES REQUIRED

**Critical Issues** (2):
1. Missing mypy configuration — type checking is table stakes
2. Uninformative error on malformed wrapped JSON (`import_service.py:53`)

**Important Issues** (5):
1. No FK constraint on strokes
2. Code duplication in repository
3. Inefficient batch insert
4. File opened without encoding
5. Test coverage gaps

The review is blocked primarily because type checking isn't configured. Even if the code issues were fixed, the tooling must be in place first.

---

## Example Review 2: CLI Module

The `/Users/cyarie/Code/goals/trackman/trackman/cli` module review:

**Status**: BLOCKED - CHANGES REQUIRED

**Critical Issues** (2):
1. Missing mypy configuration
2. Ruff not working (environment issue)

**Important Issues** (6):
1. Massive code duplication across command handlers (database session pattern repeated 4x)
2. File opened without encoding (`import_cmd.py:75`)
3. Using deprecated `Optional` instead of `| None` (`fetch.py`)
4. No tests for `import_cmd.py` or `query_cmd.py`
5. Generic exception handling hides root cause
6. Inconsistent Option/Argument patterns

**Minor Issues** (3):
1. Empty callback function in `main.py`
2. Stub commands should indicate WIP more clearly
3. Emoji usage may not render in all terminals

This review revealed cross-file patterns (duplication) and file-to-test mapping gaps that weren't visible in the storage module review.

---

## Next Steps

- [ ] Create SKILL.md from these working notes
- [ ] Create `code-reviewer` agent that loads this skill
- [ ] Pressure test with different codebase types
