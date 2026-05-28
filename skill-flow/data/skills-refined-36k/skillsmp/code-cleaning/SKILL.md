---
name: code-cleaning
description: Pre-commit Clean Code refactoring (Python-focused)
---

Clean Code is a reader's gift — refactor for the next developer, not the compiler.

**Boy Scout Rule:** Leave the code cleaner than you found it. Every change is an opportunity to improve.

# Modes

| Mode | Scope | When |
|------|-------|------|
| **Staged** (default) | `git diff --cached` | Pre-commit cleanup |
| **Full-file** | Any file (no staging required) | Deeper refactoring session |

Announce mode: `"Cleaning in [mode]. Override?"`

# Pre-flight Checks

Before any transformation:

1. **Staged changes exist**
```bash
   git diff --cached --quiet && echo "Nothing staged" && exit 1
```

2. **Tests pass**
```bash
   pytest -q || exit 1
```

3. **Coverage gate** (≥70% of staged lines)
  - Run: `pytest --cov --cov-report=xml && diff-cover coverage.xml --compare-branch=HEAD`
  - `diff-cover` maps coverage to staged hunks specifically
  - **STOP if below threshold** — report uncovered lines, do not proceed

4. **Diff size guard**
  - If staged diff >500 lines: require scope reduction or switch to Full-file mode with chunking strategy
  - **STOP if >500 lines** — "Staged diff too large (N lines). Reduce scope or switch to Full-file mode?"

5. **Git stash backup**
```bash
   BACKUP=$(git stash create)
   git stash store -m "code-cleaner-backup-$(date +%s)" "$BACKUP"
```

**Pre-flight summary:**
```
Pre-flight:
  Staged files: N
  Tests: ✓ pass (X tests)
  Coverage: Y% of staged lines (threshold: ≥70%)
  Backup: stash@{0}
Proceed (P)?
```

# Analysis Phase

**Examine staged diff.** For each change, identify:

1. **Clean Code violations** (see Principle Catalog)
2. **Bugs spotted** — flag separately, do not auto-fix

**Output format:**
```
Analysis:

Violations:
  - [file:lines] [principle] — [description]
  - [file:lines] [principle] — [description]

Bugs identified (not auto-fixed):
  - [file:line] [description] — [suggested fix]

Proposed batches:
  1. [batch name] — [N transformations]
  2. [batch name] — [N transformations]

Proceed with batch 1 (P)?
```

# Transformation Loop

For each batch:

1. **Describe** transformations textually
2. **Await approval** — user confirms or skips
3. **Apply** directly to files
4. **Run tests**
  - ✓ Pass → continue to next batch
  - ✗ Fail → **STOP**, show failure, ask user:
```
     Tests failed after [batch name].
     Options: (R)evert batch | (I)nvestigate | (F)orce continue

     (I)nvestigate: Show failure output and affected code, propose hypothesis, await instruction. No autonomous fixing.
```
5. **Loop** until no violations remain

**Batch completion:**
```
Batch N applied:
  - [transformation 1]
  - [transformation 2]
  Tests: ✓ pass

Next: [batch N+1 name] — [description]
Proceed (P) / Skip (S) / Stop (X)?
```

If no batches remain, skip the "Next:" line and proceed to Convergence.

# Pre-commit Validation

After all batches complete, run pre-commit hooks on touched files:

```bash
   pre-commit run --files $(git diff --cached --name-only)
```

**Outcomes:**

| Result | Action |
|--------|--------|
| ✓ Pass | Proceed to final summary |
| ✗ Fail (formatter) | Apply formatter output, re-run tests; if tests fail, revert and report |
| ✗ Fail (linter) | Show violations, ask user — linters require judgment |
| ✗ Fail (unfixable) | After 3 attempts, show failure, ask user |

**Output:**
```
Pre-commit validation:
  Hooks: ✓ pass (N hooks)
  — or —
  Hooks: ✗ black (reformatted 2 files)
  Auto-fixes applied. Re-running tests...
```

Note: If pre-commit not installed, skip with warning.

# Convergence

Loop terminates when:
- No more violations detected in staged scope
- User stops manually
- **Max 5 batches reached** — if violations remain, report and stop

**Idempotence:** Re-running code-cleaning on already-clean staged code must produce no changes. If it doesn't, something is wrong (oscillating renames, extract/inline loops, style churn).

**Final summary:**
```
Cleaning complete:

Batches applied: N
Transformations: M total
  - [principle]: X instances
  - [principle]: Y instances

Bugs flagged (not fixed): K
  - [file:line] [description]

Backup: stash@{0} (restore with `git stash pop`, drop with `git stash drop` when satisfied)

Suggested commit message:
---
refactor: [summary]

- [key transformation 1]
- [key transformation 2]
---
```

# Principle Catalog (Uncle Bob)

Equal priority — apply contextually.

| Principle | Signal | Transformation |
|-----------|--------|----------------|
| **Meaningful names** | Abbreviations, single letters, generic names (`data`, `info`, `temp`) | Rename to express intent |
| **Small functions** | >20 lines, multiple indent levels | Extract function |
| **Single Responsibility** | Function does X and Y | Split into focused units |
| **DRY** | Repeated logic (not coincidental similarity) | Extract common abstraction |
| **Early return** | Nested conditionals, arrow code | Guard clauses at top |
| **No "what" comments** | Comment restates code | Delete or improve naming |
| **Explain "why" only** | Magic values, non-obvious decisions | Add rationale comment |
| **Immutability preferred** | Mutable state where avoidable | Use immutable structures |
| **One level of abstraction** | Function mixes high/low level | Extract or inline to normalize |
| **Command-Query Separation** | Function both mutates and returns | Split into command + query |
| **Minimal arguments** | >3 parameters | Introduce parameter object |
| **No flag arguments** | Boolean changes behavior | Split into two functions |
| **Error handling isolation** | Try/except mixed with logic | Separate error handling |
| **KISS** | Complex solution where simple one works | Simplify: fewer branches, less indirection, obvious over clever |
| **No nested ternaries** | Chained `? :` operators | Use if/else chain or switch statement |
| **Clarity over brevity** | Dense one-liners, clever compaction | Prefer explicit form; longer can be cleaner |
| **Dead code removal** | Unused imports, functions, variables, unreachable branches | Delete (use `vulture` for detection; false positives common — require explicit approval per item, do not batch delete) |

# Scope Discipline

**Staged mode (default):**
- Transform ONLY code in `git diff --cached`
- Impact MAY propagate (renames, signature changes affect callers)
- Propagation to unstaged files requires explicit approval before applying batch
- **Rename threshold:** If rename affects >10 files, show full propagation scope and require explicit confirmation before proceeding

**Full-file mode:**
- Transform entire files that have a staged change
- Same propagation rules

# Anti-patterns

**FORBIDDEN:**
- Refactoring without test coverage
- Mixing bug fixes with refactoring (flag bugs separately)
- Touching unstaged files (unless refactoring side effect with explicit user approval)
- Continuing after test failure without user approval
- Premature abstraction (don't extract for one use)
- Renaming for personal preference (rename for clarity only)
- Modifying tests as part of refactoring (invoke Testing skill instead)
- Formatting-only changes (delegate to pre-commit hooks; only touch formatting in lines already being refactored)
- Changing public APIs (function signatures, class interfaces) without explicit approval
- Over-compaction (optimizing for line count at expense of readability)
- Premature flattening (inlining abstractions that exist for clarity, even if used once)

# Integration

**Position in workflow:**
```
code → stage → **clean** → review → commit
```

Runs BEFORE code review. Reviewer sees clean code, not raw changes.

**Relation to other skills:**
- Testing skill: invoke if coverage insufficient
- Code Review: complementary — cleaner handles style/structure, review handles correctness/architecture
