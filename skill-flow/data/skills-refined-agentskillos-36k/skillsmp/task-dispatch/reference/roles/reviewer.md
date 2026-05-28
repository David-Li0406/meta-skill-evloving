# Reviewer Role

Multi-agent review of batch implementations. Multiple reviewers run in parallel for diverse perspectives.

## Reviewers

**Reviewers dispatch in parallel (SINGLE message):**

| Reviewer | Tool | Model | Required |
|----------|------|-------|----------|
| Native Claude | Task (task-reviewer) | from validation.yaml (opus) | Yes |
| OpenCode (0-N) | Bash (opencode) | from validation.yaml | No |

**Common OpenCode models:**
- `openai/gpt-5.2-codex` - Code-specialized, fresh perspective
- `google/gemini-3-pro-preview` - Different reasoning, catches edge cases
- `openai/gpt-5.2-pro` - Extended capabilities

**CRITICAL:** Dispatch all configured reviewers in the same message for true parallelism.

## Purpose

Reviewers check the **diff of changes** from a batch, ensuring quality and spec compliance before proceeding to the next batch.

**This is Phase C of the Three-Phase Pipeline.** It is mandatory - no batch completes without review.

**Key:** Reviewers work with the git diff, not full file contents. This keeps reviews focused and efficient.

## Skills to Invoke

**First action:** Invoke `code-review` skill for review methodology.
**Second action:** Invoke `code-implement` skill for language-specific patterns.

## Input

Each reviewer receives:

**1. Batch diff (primary input):**
```diff
# git diff <last_batch_commit>..HEAD
diff --git a/src/feature_a.py b/src/feature_a.py
new file mode 100644
...
```

**2. Implementer reports (context):**
```yaml
# Task N1
implementer_report:
  status: success
  implementation_files: [src/feature_a.py]
  test_output: "3 passed"

# Task N2
implementer_report:
  status: success
  implementation_files: [src/feature_b.py]
  test_output: "2 passed"
```

**3. Task specs from tasks.yaml (requirements)**

## Responsibilities

1. Review all changes from the batch together
2. Evaluate against five gates (Correctness, Style, Performance, Security, Architecture)
3. Check each task against its spec requirements
4. Verify tests cover the implementation
5. Identify issues by severity
6. Report with actionable feedback

## Dispatch Configuration

**CRITICAL:** Dispatch ALL reviewers in a SINGLE message for true parallelism.

```
# Single message with multiple tool calls:

# 1. Native Claude reviewer (Task tool) [required]
Task(
  subagent_type="task-reviewer",
  model={claude_model},  # from review_config (opus)
  prompt=review_prompt
)

# 2. OpenCode reviewers (Bash tool, background) [from validation.yaml]
Bash(run_in_background=true):
  timeout 1200 opencode run --model "openai/gpt-5.2-codex" --variant {reasoning_effort}-medium "{review_prompt}"

Bash(run_in_background=true):
  timeout 1200 opencode run --model "google/gemini-3-pro-preview" --variant {reasoning_effort}-medium "{review_prompt}"
```

All models and reasoning effort are configured in `validation.yaml` under `review_config`.

## When Reviewers Run

**After ALL implementers in a batch complete** - as Phase C of the pipeline.

```
Batch N:
├── Phase A: Testers (parallel)
├── Phase B: Implementers (parallel)
└── Phase C: Reviewers (1+N in parallel) ← this role
    ├── Claude opus [required]
    └── OpenCode reviewers (0-N from validation.yaml)
```

## Report Format

Each reviewer produces a YAML report with gates:

```yaml
reviewer_report:
  reviewer: claude-opus  # or opencode-codex, opencode-gemini-3-pro
  gates:
    correctness:
      status: pass | fail
      issues: ["Logic error in X"]
    style:
      status: pass | fail
      issues: []
    performance:
      status: pass | fail
      issues: []
    security:
      status: pass | fail
      issues: ["SQL injection risk"]
    architecture:
      status: pass | fail
      issues: []
  issues:
    - task: N1
      severity: critical | high | medium
      gate: security
      location: "src/db/query.py:45"
      description: "SQL injection via unsanitized input"
      suggestion: "Use parameterized queries"
  strengths:
    - "Good test coverage for edge cases"
    - "Clean separation of concerns"
```

## Synthesizing Multiple Reviews

After all reviewers complete:

1. **Parse reports** - Extract YAML from all reviewer outputs
2. **Merge issues:**
   - Deduplicate by location + description similarity
   - Combine issues flagged by multiple reviewers (higher confidence)
   - Note which reviewer(s) found each issue
3. **Aggregate gates:**
   - Gate fails if ANY reviewer fails it
   - Record which reviewer(s) failed each gate
4. **Aggregate severity:**
   - Issue severity is the HIGHEST across all reviewers
   - Critical by any reviewer = Critical overall
5. **Present unified feedback:**
   - Gate summary table
   - Issues grouped by severity
   - Show which reviewers found each issue

**Gate Summary Table:**

```
| Gate         | Claude | Codex  | Gemini |
|--------------|--------|--------|--------|
| Correctness  | pass   | fail   | pass   |
| Style        | pass   | pass   | pass   |
| Performance  | pass   | pass   | pass   |
| Security     | fail   | pass   | fail   |
| Architecture | pass   | pass   | pass   |
```

**Issues by Severity:**

```
## Critical (found by 2+ reviewers - high confidence)
- [C1] SQL injection at src/db/query.py:45
  Found by: claude-opus, opencode-gemini-3-pro
  Suggestion: Use parameterized queries

## High
- [H1] Missing null check at src/api/handler.ts:112
  Found by: opencode-codex
  Suggestion: Add guard clause
```

## Issue Severity

| Severity | Definition | Action |
|----------|------------|--------|
| Critical | Bugs, security issues, data corruption | Fix immediately before next batch |
| High | Significant issues, missing coverage | Fix before next batch |
| Medium | Style, naming, small improvements | Note for later, proceed |

## Handling Timeouts

If OpenCode reviewer times out (> 5 minutes):

1. Continue with completed reviews (minimum 1 Claude required)
2. Note: "[Reviewer] timed out, partial results"
3. Proceed with available data
4. Consider re-running if critical issues suspected

## Quality Criteria

Review is good when it:
- Evaluates all five gates
- Covers all tasks in the batch
- Provides actionable feedback (not vague)
- Prioritizes issues by severity
- Acknowledges strengths
- Includes file/line references

## Example

**Batch:** Tasks T002, T003, T004 (parallel)

**Dispatch (single message):**
```
Task(task-reviewer, {claude_model}): "Review batch T002-T004" ...
Bash(background): opencode run --model "openai/gpt-5.2-codex" --variant {reasoning_effort}-medium ...
Bash(background): opencode run --model "google/gemini-3-pro-preview" --variant {reasoning_effort}-medium ...
```

**Individual Outputs:**

Claude Opus:
```yaml
reviewer_report:
  reviewer: claude-opus
  gates:
    correctness: { status: fail, issues: ["Missing null check"] }
    style: { status: pass, issues: [] }
    performance: { status: pass, issues: [] }
    security: { status: fail, issues: ["SQL injection"] }
    architecture: { status: pass, issues: [] }
  issues:
    - task: T002
      severity: critical
      gate: security
      location: "src/db/query.py:45"
      description: "SQL injection via unsanitized input"
      suggestion: "Use parameterized queries"
```

OpenCode Gemini:
```yaml
reviewer_report:
  reviewer: opencode-gemini-3-pro
  gates:
    correctness: { status: pass, issues: [] }
    style: { status: pass, issues: [] }
    performance: { status: pass, issues: [] }
    security: { status: fail, issues: ["Unsanitized query parameter"] }
    architecture: { status: pass, issues: [] }
  issues:
    - task: T002
      severity: critical
      gate: security
      location: "src/db/query.py:45"
      description: "Query parameter not sanitized"
      suggestion: "Add input validation"
```

**Synthesized:**
```
## Gate Summary
| Gate         | Claude | Codex  | Gemini |
|--------------|--------|--------|--------|
| Correctness  | fail   | pass   | pass   |
| Security     | fail   | pass   | fail   |
| (others)     | pass   | pass   | pass   |

## Critical (2 reviewers agree)
- [C1] SQL injection at src/db/query.py:45
  Found by: claude-opus, opencode-gemini-3-pro
  Fix: Use parameterized queries + input validation

Action: Dispatch fix subagent before proceeding
```
