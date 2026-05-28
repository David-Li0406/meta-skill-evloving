---
name: code-review
description: Code review methodology. Use when reviewing code locally or preparing for a PR review.
---

# Code Review Skill

Multi-perspective code review using parallel subagent dispatch for comprehensive analysis.

> **Reference:** See [reference/roles/](reference/roles/) for reviewer personas, [reference/report.md](reference/report.md) for YAML schemas, [reference/playbook.md](reference/playbook.md) for edge case handling.

---

## When to Use

- Reviewing code changes locally before commit
- Preparing review feedback for a PR
- Final review of a spec implementation
- Analyzing code quality across multiple dimensions

---

## Command

```
/code.review [target]
/code.review --spec <name>
/code.review --rev <ref>
/code.review --path <path>
/code.review --diff
```

**Target types (auto-detected by default):**
- **Spec name** → Final review of spec implementation
- **Git rev** → Review changes in commit(s)
- **Git range** → Review changes between refs
- **Path** → Review file or directory
- **No argument** → Review staged/unstaged changes

**Disambiguation flags (optional):**
- `--spec` → Force spec mode (e.g., spec named "main")
- `--rev` → Force git rev mode (e.g., path named "HEAD")
- `--path` → Force path mode (e.g., directory named "v1.0")
- `--diff` → Force diff mode (staged/unstaged changes)

---

## Workflow

### Step 1: Detect Input Type

**If flag provided, use it directly:**

```
--spec auth-system  → Spec mode (no detection)
--rev main          → Git rev mode (no detection)
--path ./main       → Path mode (no detection)
```

**Otherwise, auto-detect:**

```
Input                    | Detection                           | Mode
-------------------------|-------------------------------------|-------------
auth-system              | ./specs/active/auth-system/ exists  | Spec (final)
HEAD~3                   | Valid git rev                       | Git rev
main..feature            | Valid git range                     | Git range
abc123f                  | Valid commit SHA                    | Git rev
src/auth/                | Path exists                         | Path
(no argument)            | -                                   | Diff
```

**Auto-detection priority:**

1. **Check for spec:** `test -d ./specs/active/{arg}/`
   - If exists → **Spec mode** (final review)
2. **Check for git rev:** `git rev-parse --verify {arg} 2>/dev/null`
   - If valid → **Git rev mode**
3. **Check for git range:** contains `..` and valid refs
   - If valid → **Git range mode**
4. **Check for path:** `test -e {arg}`
   - If exists → **Path mode**
5. **No argument:**
   - Check `git diff --cached` → staged changes
   - Check `git diff` → unstaged changes
   - If neither → ask user

**Ambiguity examples:**
```bash
# "main" could be spec, branch, or directory
/code.review main           # Auto-detect (spec first, then git, then path)
/code.review --spec main    # Force: spec named "main"
/code.review --rev main     # Force: git branch "main"
/code.review --path main    # Force: directory named "main"
```

### Step 2: Load Review Context

**Spec mode:**
```
Read (in parallel):
  ./specs/active/<spec>/spec.md        # Requirements
  ./specs/active/<spec>/tasks.yaml     # Task definitions
  ./specs/active/<spec>/review.yaml    # Batch review history
  ./specs/active/<spec>/validation.yaml # Review config + reviewers
```

**Git rev/range mode:**
```bash
git show <rev>              # Single commit
git diff <range>            # Range (e.g., main..feature)
git log --oneline <range>   # Commit messages for context
```

**Path mode:**
```bash
# Read file(s) at path
# If directory, find changed files or all files
```

**Diff mode:**
```bash
git diff --cached           # Staged changes (preferred)
git diff                    # Unstaged changes (fallback)
```

### Step 3: Select Reviewers

**Spec mode:** Use reviewers from `validation.yaml` (no prompt):

```yaml
review_config:
  reviewers:
    - type: claude
      model: opus
    - type: opencode
      model: openai/gpt-5.2-codex
```

**Other modes:** Use **AskUserQuestion**:

**Question 1:** Select reviewers:
```
Header: Reviewers
Question: Which reviewers should analyze this code?
multiSelect: true
Options:
- claude-opus: Claude Opus - native subagent, context-aware, codebase access
- claude-sonnet: Claude Sonnet - faster native review
- openai-gpt5.2-codex: OpenAI GPT-5.2 Codex - code-specialized (Recommended)
- openai-gpt5.2-pro: OpenAI GPT-5.2 Pro - extended capabilities
- gemini-3-pro: Google Gemini 3 Pro - advanced reasoning
```

**Default selection:** claude-opus, openai-gpt5.2-codex

**Question 2:** Select reasoning effort (if OpenCode reviewers selected):
```
Header: Reasoning
Question: What reasoning effort level for OpenCode reviewers?
multiSelect: false
Options:
- low: Quick responses, minimal deliberation
- medium: Balanced reasoning (Recommended)
- high: Deep analysis, thorough deliberation
- xhigh: Maximum reasoning (GPT-5.2 only)
```

**Default:** medium

**Model mapping to commands:**
- `claude-opus` → Task tool with `model: "opus"`
- `openai-gpt5.2-codex` → `opencode run --model "openai/gpt-5.2-codex" --variant {reasoning}-medium`
- `openai-gpt5.2-pro` → `opencode run --model "openai/gpt-5.2-pro" --variant {reasoning}-medium`
- `gemini-3-pro` → `opencode run --model "google/gemini-3-pro-preview" --variant {reasoning}-medium`

### Step 4: Dispatch Reviewers in Parallel

**CRITICAL:** Dispatch all reviewers in the same message for true parallelism.

**Dispatch by Type:**

**Claude reviewers (Task tool):**
```python
Task(
  subagent_type="general-purpose",
  model="opus",  # or "sonnet"
  prompt=review_prompt
)
```

**OpenCode reviewers (Bash tool, background):**
```bash
timeout 1200 opencode run --model "{MODEL_PATH}" --variant {reasoning}-medium "{review_prompt}"
```

**Examples (with high reasoning):**
- `opencode run --model "openai/gpt-5.2-codex" --variant high-medium "{prompt}"`
- `opencode run --model "openai/gpt-5.2-pro" --variant high-medium "{prompt}"`
- `opencode run --model "google/gemini-3-pro-preview" --variant high-medium "{prompt}"`

**Review Prompt (standard):**

```
You are reviewing code for quality, correctness, and maintainability.

## Code to Review
[Include diff or file contents]

## Context
[Git commit message, PR description, or spec requirements]

## Review Focus
Evaluate against these gates:

1. **Correctness** - Logic errors, edge cases, error handling, type safety
2. **Style** - Naming, formatting, idioms, readability
3. **Performance** - Efficiency, data structures, unnecessary work
4. **Security** - Input validation, secrets, injection risks
5. **Architecture** - Design patterns, coupling, separation of concerns

## Output Format
[Standard reviewer_report YAML - see reference/report.md]
```

**Review Prompt (spec mode - final review):**

```
You are performing a FINAL REVIEW of a complete spec implementation.

## Spec Requirements
[Include spec.md content]

## Tasks Implemented
[Include tasks.yaml]

## Batch Review History
[Summarize from review.yaml]

## Deferred Issues
[List medium-severity issues from batch reviews]

## Review Focus
1. **Spec Compliance** - All requirements met? Acceptance criteria satisfied?
2. **Gates** - Correctness, Style, Performance, Security, Architecture
3. **Deferred Issues** - Address or document remaining issues
4. **Integration** - Components work together? No regressions?
5. **Test Coverage** - All behaviors tested?

## Output Format
[Final review YAML - see reference/report.md]
```

### Step 5: Synthesize Reviews

After all reviewers complete:

1. **Parse reports** - Extract YAML from all outputs
2. **Merge issues:**
   - Deduplicate by location + description similarity
   - Combine issues flagged by multiple reviewers (higher confidence)
   - Note which reviewer(s) found each issue
3. **Aggregate gates:**
   - Gate fails if ANY reviewer fails it
   - Record which reviewer(s) failed each gate
4. **Prioritize by severity:**
   - Critical → High → Medium
   - Within severity, group by gate

### Step 6: Write Review Output

**Spec mode** → `./specs/active/<spec>/review.yaml`:

```yaml
final_review:
  status: completed
  timestamp: <ISO_TIMESTAMP>
  reviewers: [...]
  gates: { correctness: pass, style: pass, ... }
  spec_compliance:
    all_tasks_complete: true
    acceptance_criteria_met: true
    edge_cases_handled: true
  issues: [...]
  strengths: [...]
  recommendation: ready_to_merge | changes_requested

readiness:
  all_batches_reviewed: true
  critical_issues_resolved: true
  high_issues_resolved: true
  final_review_passed: true
  tests_passing: true
```

**Other modes** → `~/.claude/reviews/<generated-name>.md` (ephemeral):

```bash
# Generate review name based on input type
mkdir -p ~/.claude/reviews

# Git rev:    review-abc123f-2026-01-22T14-30.md
# Git range:  review-main..feature-2026-01-22T14-30.md
# Path:       review-src-auth-2026-01-22T14-30.md
# Diff:       review-staged-2026-01-22T14-30.md
```

**Ephemeral review format (Markdown):**

```markdown
# Code Review: <target>

**Date:** 2026-01-22T14:30:00Z
**Reviewers:** claude-opus, opencode-codex
**Target:** HEAD~3 | main..feature | src/auth/ | staged changes

## Gate Summary

| Gate         | Status | Claude | Codex  |
|--------------|--------|--------|--------|
| Correctness  | PASS   | pass   | pass   |
| Style        | PASS   | pass   | pass   |
| Performance  | PASS   | pass   | pass   |
| Security     | FAIL   | fail   | pass   |
| Architecture | PASS   | pass   | pass   |

## Issues

### Critical
- **[C1]** SQL injection in user input (Security)
  - Location: src/db/query.py:45
  - Found by: claude-opus
  - Suggestion: Use parameterized queries

### High
...

### Medium
...

## Strengths
- Clean separation of concerns
- Good error messages

## Recommendation
Address critical issues before proceeding
```

Reviews are stored ephemerally like Claude's internal plans - useful for reference but not committed to the repo.

### Step 7: Present Review

**Gate Summary Table:**

```
| Gate         | Status | Claude | Codex  |
|--------------|--------|--------|--------|
| Correctness  | PASS   | pass   | pass   |
| Style        | PASS   | pass   | pass   |
| Performance  | PASS   | pass   | pass   |
| Security     | FAIL   | fail   | pass   |
| Architecture | PASS   | pass   | pass   |
```

**Issues by Severity:**

```
## Critical (must fix)
- [C1] SQL injection in user input (Security) at src/db/query.py:45
  Found by: claude-opus
  Suggestion: Use parameterized queries

## High (should fix)
...

## Medium (consider)
...
```

**Spec mode additional output:**

```
### Spec Compliance
- All tasks complete: ✓
- Acceptance criteria met: ✓
- Edge cases handled: ✓

### Deferred Issues
- Resolved: 3
- Remaining: 0
```

### Step 8: Recommend Action

**All gates pass:**
```
Review complete. All gates passed.
Recommendation: Ready to commit/merge
```

**Issues found:**
```
Review complete. 1 gate failed.
Critical: 1, High: 0, Medium: 2
Recommendation: Address critical issues before proceeding
```

**Spec mode (all pass):**
```
Final review complete: auth-system
Recommendation: Ready to merge ✓
Next: Create PR with /pr.create or merge directly
```

---

## Gates

| Gate | What It Checks |
|------|----------------|
| **Correctness** | Logic errors, edge cases, error handling, type safety |
| **Style** | Naming conventions, formatting, readability, idioms |
| **Performance** | Efficiency, data structures, unnecessary computation |
| **Security** | Input validation, secrets exposure, injection risks |
| **Architecture** | Design patterns, coupling, separation of concerns |

---

## Issue Areas

| Area | Covers |
|------|--------|
| `logic` | Control flow, algorithms, conditionals |
| `error_handling` | Exceptions, error states, recovery |
| `type_safety` | Type correctness, nullability |
| `naming` | Variable, function, class names |
| `formatting` | Code layout, indentation, spacing |
| `efficiency` | Time/space complexity, caching |
| `validation` | Input checking, sanitization |
| `secrets` | Credentials, keys, tokens |
| `coupling` | Dependencies, interfaces |
| `testing` | Test coverage, testability |

---

## Examples

```bash
# Auto-detected (most common)
/code.review auth-system      # Spec → final review
/code.review HEAD~3           # Git rev → last 3 commits
/code.review main..feature    # Git range → branch diff
/code.review abc123f          # Git rev → specific commit
/code.review src/auth/        # Path → directory
/code.review                  # Diff → staged/unstaged

# Disambiguation flags (when names collide)
/code.review --spec main      # Spec named "main" (not git branch)
/code.review --rev main       # Git branch "main" (not spec/path)
/code.review --path HEAD      # Directory named "HEAD" (not git ref)
/code.review --rev v1.0       # Git tag "v1.0" (not path)
/code.review --diff           # Staged/unstaged changes explicitly
```

---

## Review Storage

| Mode | Location | Persistence |
|------|----------|-------------|
| Spec | `./specs/active/<spec>/review.yaml` | Committed with spec |
| Other | `~/.claude/reviews/<name>.md` | Ephemeral (like plans) |

**Naming convention for ephemeral reviews:**
- `review-<sha>-<timestamp>.md` - Git rev
- `review-<from>..<to>-<timestamp>.md` - Git range
- `review-<path-slug>-<timestamp>.md` - Path
- `review-staged-<timestamp>.md` - Staged changes

---

## Edge Cases

**Spec not found:**
- List available specs in `./specs/active/`
- Suggest closest match if typo likely

**Git rev invalid:**
- Report error, suggest valid refs
- List recent commits for reference

**OpenCode timeout (> 20 minutes):**
- Continue with completed reviews
- Note: "[Reviewer] timed out, partial results"

**No code to review:**
- List recent changed files
- Ask user to specify target

---

## Integration

**Command:** `/code.review [target]`

**Related skills:**
- `code-implement` - Language-specific patterns to check against
- `pr-review` - GitHub PR workflow (uses this for methodology)
- `code-debug` - Root cause analysis when issues found
- `task-dispatch` - Batch reviews during implementation (Phase C)

---

## Reference

- [reference/roles/claude-reviewer.md](reference/roles/claude-reviewer.md) - Claude reviewer persona
- [reference/roles/opencode-reviewer.md](reference/roles/opencode-reviewer.md) - OpenCode reviewer persona
- [reference/report.md](reference/report.md) - YAML report schemas
- [reference/playbook.md](reference/playbook.md) - Edge case handling
- [reference/checklist.md](reference/checklist.md) - Review checklist
