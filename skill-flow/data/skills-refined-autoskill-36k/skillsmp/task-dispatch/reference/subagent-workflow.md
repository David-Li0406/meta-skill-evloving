# Subagent Workflow Details

## Task Batching

Before dispatching, analyze `dependencies.yaml` for execution batches:

1. Parse task dependency graph
2. Identify `[P]` markers (parallelizable within same phase)
3. Group consecutive `[P]` tasks that modify different files
4. Non-`[P]` tasks form single-task batches
5. Phase boundaries force batch breaks

## Three-Phase Pipeline

**Each batch executes three mandatory phases:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase A: TESTERS                                               │
│  ├── Writes failing tests (RED)                                 │
│  └── Reports test paths + failure output                        │
│                          ↓                                      │
│  Phase B: IMPLEMENTERS                                          │
│  ├── Receives tester's report                                   │
│  ├── Makes tests pass (GREEN)                                   │
│  └── Reports impl files + pass output                           │
│                          ↓                                      │
│  Phase C: REVIEWERS                                             │
│  ├── Reviews ALL changes from batch                             │
│  ├── Checks against spec requirements                           │
│  └── Reports issues by severity                                 │
└─────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** All three phases are mandatory. A batch is not complete until reviewers finish.

---

## Tester Dispatch Template

```yaml
Task:
  subagent_type: task-tester
  model: opus
  description: "Write tests for Task N: [task name]"
  prompt: |
    You are writing failing tests for Task N from [spec-file].

    **First:** Invoke the `code-test` skill for TDD methodology.
    **Second:** Invoke the `code-implement` skill for language-specific test patterns.

    **Task requirements:**
    [paste task from tasks.yaml including test_hints]

    **Your job:**
    1. Read the task requirements and test_hints
    2. Write tests that cover all specified behaviors
    3. Tests must FAIL (features not implemented yet)
    4. Run tests to verify RED state

    **Work from:** [directory]

    **Report in YAML format:**
    ```yaml
    tester_report:
      status: success  # or "gap" if cannot write tests
      test_files:
        - path: [test file path]
          tests: [list of test names]
      failure_output: |
        [actual test failure output]
      gap_reason: null  # or explanation if status=gap
    ```
```

**For parallel batch (N tasks):**
Dispatch ALL testers in a SINGLE message:

```yaml
# Single message with multiple Task tool calls
Task (task-tester, opus): "Write tests for Task N1" ...
Task (task-tester, opus): "Write tests for Task N2" ...
Task (task-tester, opus): "Write tests for Task N3" ...
```

Wait for ALL testers to complete before dispatching implementers.

---

## Implementer Dispatch Template

```yaml
Task:
  subagent_type: task-implementer
  model: opus
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N from [spec-file].

    **First:** Invoke the `code-implement` skill for language guidelines.

    **Tests written by tester:**
    ```yaml
    [paste tester_report YAML]
    ```

    **Your job:**
    1. Run the tests to see current failures
    2. Write minimal code to make tests pass (GREEN)
    3. If requirements are ambiguous, use AskUserQuestion
    4. Refactor while keeping tests green

    **Work from:** [directory]

    **Report in YAML format:**
    ```yaml
    implementer_report:
      status: success  # or "blocked" if cannot proceed
      implementation_files:
        - path: [impl file path]
      test_output: |
        [test pass output]
      clarifications:
        - question: [if used AskUserQuestion]
          answer: [user's response]
      blocked_reason: null  # or explanation if status=blocked
    ```
```

**For parallel batch (N tasks):**
Dispatch ALL implementers in a SINGLE message, each with its corresponding tester report:

```yaml
# Single message with multiple Task tool calls
Task (task-implementer, opus): "Implement Task N1" + tester_1_report
Task (task-implementer, opus): "Implement Task N2" + tester_2_report
Task (task-implementer, opus): "Implement Task N3" + tester_3_report
```

Wait for ALL implementers to complete before dispatching reviewers.

---

## Reviewer Dispatch Template

**CRITICAL:** Reviewers are mandatory. Every batch gets reviewed.

**Step 1: Get batch diff**
```bash
# Get diff of changes made in this batch
git diff <last_batch_commit>..HEAD > /tmp/batch_diff.txt
```

**Step 2: Dispatch ALL reviewers in a SINGLE message:**

```yaml
# Single message with multiple tool calls for true parallelism

# Native Claude reviewer (Task tool) [REQUIRED]
Task:
  subagent_type: task-reviewer
  model: {claude_model}  # from review_config (opus)
  description: "Review batch: Tasks N1, N2, N3"
  prompt: |
    Review the batch diff for Tasks N1, N2, N3.

    **First:** Invoke the `code-review --diff` skill for review methodology.

    **Batch Diff:**
    ```diff
    [paste git diff of batch changes - NOT full files]
    ```

    **What was implemented:**
    [paste all implementer_report YAMLs]

    **Spec requirements:**
    [paste relevant tasks from tasks.yaml]

    **Review against these gates:**
    1. Correctness - Logic errors, edge cases, error handling
    2. Style - Naming, formatting, idioms
    3. Performance - Efficiency, data structures
    4. Security - Input validation, secrets, injection risks
    5. Architecture - Design patterns, coupling

    **Report in YAML format:**
    ```yaml
    reviewer_report:
      reviewer: claude-opus
      batch: N
      diff_reviewed: true
      gates:
        correctness: { status: pass | fail, issues: [] }
        style: { status: pass | fail, issues: [] }
        performance: { status: pass | fail, issues: [] }
        security: { status: pass | fail, issues: [] }
        architecture: { status: pass | fail, issues: [] }
      issues:
        - task: N1
          severity: critical | high | medium
          gate: correctness
          location: "file:line"
          description: "Clear description"
          suggestion: "How to fix"
      strengths:
        - "Positive observation"
    ```

# OpenCode reviewers (0-N from validation.yaml, Bash tool, background)
# Include one Bash call per model configured in validation.yaml review_config.reviewers
# Use reasoning_effort from review_config to build variant: {reasoning_effort}-medium

Bash:
  command: timeout 1200 opencode run --model "openai/gpt-5.2-codex" --variant {reasoning_effort}-medium "[review_prompt_with_diff]"
  run_in_background: true

Bash:
  command: timeout 1200 opencode run --model "google/gemini-3-pro-preview" --variant {reasoning_effort}-medium "[review_prompt_with_diff]"
  run_in_background: true
```

Wait for ALL reviewers (Claude + OpenCode) to complete before synthesizing.

**validation.yaml configuration:**
```yaml
review_config:
  reasoning_effort: high  # low | medium | high | xhigh (user-selected, xhigh GPT-5.2 only)
  reviewers:
    - openai/gpt-5.2-codex
    - google/gemini-3-pro-preview
  # Empty list = Claude-only review
  # Variant = {reasoning_effort}-medium
```

---

## Review Synthesis

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
## Critical (found by 2+ reviewers)
- [C1] SQL injection in user input at src/db/query.py:45
  Found by: claude-opus, gemini-3-pro
  Suggestion: Use parameterized queries

## High
- [H1] Missing null check at src/api/handler.ts:112
  Found by: claude-opus
  Suggestion: Add guard clause
```

---

## Fix Subagent Template

When review finds Critical/High issues:

```yaml
Task:
  subagent_type: task-implementer
  model: opus
  description: "Fix issues from batch review"
  prompt: |
    Fix these issues from code review:

    **Issues to fix:**
    ```yaml
    [paste relevant issues from synthesized review]
    ```

    Make targeted fixes only. Don't refactor beyond what's needed.
    Run tests to verify fixes don't break anything.

    **Report in YAML format:**
    ```yaml
    fix_report:
      status: success
      fixes_applied:
        - issue: [description]
          fix: [what you did]
      test_output: |
        [test output after fixes]
    ```
```

After fixes, dispatch targeted review (can be single Claude reviewer for speed).

---

## Workflow Diagram (Three-Phase Pipeline)

```
Load Spec + dependencies.yaml
    |
    v
Build Execution Batches
    |
    v
[For each batch]
    |
    +--> Single task?
    |         |
    |    YES: Phase A: Dispatch 1 tester (opus)
    |         Phase B: Dispatch 1 implementer (opus)
    |         Phase C: Dispatch 1+N reviewers (parallel)
    |         |
    |    NO (parallel [P] tasks):
    |         Phase A: Dispatch N testers (single message)
    |         Phase B: Dispatch N implementers (single message)
    |         Phase C: Dispatch 1+N reviewers (single message)
    |         |
    |         v
    +--> Synthesize Reviews
    |         |
    |         v
    |    Critical/High Issues? --YES--> Dispatch Fix Subagent(s)
    |         |                              |
    |         NO                             v
    |         |                        Targeted Review
    |         v                              |
    |    Commit Batch <----------------------+
    |         |
    v         v
[Next Batch]
    |
    v
Final Review (1+N reviewers in parallel)
    |
    v
Done

(1+N = 1 Claude [required] + N OpenCode [from validation.yaml])
```

---

## Handling Tester Gaps

If tester reports `status: gap`:

1. Read `gap_reason` from tester's report
2. Consult spec (tasks.yaml, spec.md) for clarification
3. If still unclear, use AskUserQuestion to clarify with user
4. Re-dispatch tester with additional context:

```yaml
Task:
  subagent_type: task-tester
  model: opus
  description: "Write tests for Task N (clarified)"
  prompt: |
    Previous attempt reported gap: [gap_reason]

    **Clarification received:**
    [additional context or user's answer]

    Now write tests with this clarified understanding.
    [rest of tester template]
```

---

## Handling Reviewer Timeouts

If OpenCode reviewer times out (> 5 minutes):

1. Continue with completed reviews (minimum 1 required)
2. Add warning to output:
   ```
   Note: [Reviewer] timed out after 5 minutes.
   Results are from available reviewers only.
   ```
3. Proceed with synthesis using available data
4. Consider re-running batch if only 1 reviewer completed

---

## Best Practices

1. **Always opus** - Never use sonnet for task subagents
2. **Tester first** - Implementer must receive failing tests
3. **Reviewers mandatory** - Every batch gets at least Claude reviewer (+ configured OpenCode)
4. **YAML reports** - Structured handoff between phases
5. **Single message dispatch** - All parallel subagents in one message
6. **Fresh context** - Each subagent starts clean
7. **Track progress** - Update TodoWrite after each phase
8. **Configure reviewers** - Set OpenCode models in validation.yaml (0-N)
