---
name: pr-comment
description: PR review comment workflow - understand the concern before fixing
user_invocable: true
---

# PR Comment Workflow

Understanding-first workflow for addressing PR review comments.

## Initialize (REQUIRED FIRST STEP)

```bash
python3 ~/.claude/plugins/agent-swarm/lib/pr_comment_workflow.py start "<comment>" <pr_number>
```

This creates the workflow state and sets you to the UNDERSTAND phase.

## Flow

```
UNDERSTAND → [adversary] → FIX → [adversary] → VERIFY → PUSH → CHECK_REVIEWS → DONE
     ↑                             ↑                              |
     └──────── new comments ───────┴──── tests fail ──────────────┘
```

## Phases

| Phase | Purpose | Allowed Tools | Blocked | Required Outputs |
|-------|---------|---------------|---------|------------------|
| **UNDERSTAND** | Grasp reviewer's concern | Read, Glob, Grep | Edit, Write, Bash | articulation, current_code_problem |
| **FIX** | Implement changes | Read, Glob, Grep, Edit, Write, Bash | - | - |
| **VERIFY** | Run tests/lint | Read, Glob, Grep, Bash | Edit, Write | tests_pass, lint_pass |
| **PUSH** | Push changes | Bash | - | - |
| **CHECK_REVIEWS** | Check for new comments | Read, Bash | Edit, Write | no new_comments |
| **DONE** | Complete | - | - | - |

## Adversary Gates

Two phases have adversary gates:

1. **UNDERSTAND** - Adversary validates your understanding
   - "Can you articulate the reviewer's concern in your own words?"
   - "What specific problem does the current code have?"
   - "Why is the reviewer's suggestion better than what exists?"

2. **FIX** - Adversary checks fix matches understanding
   - "Does this change address the articulated concern?"
   - "Did you change anything beyond what the reviewer asked?"

## Required Outputs

Before leaving UNDERSTAND phase, you must provide:

- **articulation** - Restate the reviewer's concern in your own words
- **current_code_problem** - What specific problem exists in the current code

This prevents "just do what they said" without understanding why.

## Kickback Logic

| From | To | Trigger |
|------|-----|---------|
| VERIFY | FIX | Tests or lint fail |
| CHECK_REVIEWS | UNDERSTAND | New review comments appear |

If new comments appear after your push, you go back to UNDERSTAND - not FIX. This ensures you don't just keep tweaking without understanding.

## CLI Commands

```bash
# Start workflow
python3 lib/pr_comment_workflow.py start "reviewer comment" 123

# Check status
python3 lib/pr_comment_workflow.py status

# Get current phase
python3 lib/pr_comment_workflow.py phase

# Record understanding
python3 lib/pr_comment_workflow.py understand "<articulation>" "<problem>"

# Record verification
python3 lib/pr_comment_workflow.py verify <tests_pass> <lint_pass>

# Advance to next phase
python3 lib/pr_comment_workflow.py advance

# Stop workflow
python3 lib/pr_comment_workflow.py stop
```

## Example Session

```bash
# 1. Start with the review comment
python3 lib/pr_comment_workflow.py start \
  "This function is doing too much. Consider extracting the validation logic." \
  42

# 2. UNDERSTAND - Read the code, understand the concern
# Record your understanding:
python3 lib/pr_comment_workflow.py understand \
  "Reviewer wants separation of concerns - validation mixed with business logic makes testing harder" \
  "validate_and_process() has 3 responsibilities: input validation, transformation, and persistence"

# 3. FIX - Extract validation
python3 lib/pr_comment_workflow.py advance
# Make the changes...

# 4. VERIFY
pytest && ruff check .
python3 lib/pr_comment_workflow.py verify 1 1
python3 lib/pr_comment_workflow.py advance

# 5. PUSH
git add -A && git commit -m "refactor: extract validation from validate_and_process"
git push
python3 lib/pr_comment_workflow.py advance

# 6. CHECK_REVIEWS - Wait, check for new comments
python3 lib/pr_comment_workflow.py advance

# 7. DONE (or kickback to UNDERSTAND if new comments)
```

## DO NOT

- Start editing before articulating the concern
- Skip the understanding phase because "it's obvious"
- Make changes beyond what the reviewer asked
- Ignore kickbacks - new comments mean you missed something

## Why This Matters

Common anti-patterns this prevents:

1. **Cargo cult fixes** - "Reviewer said X, so I'll do X" without understanding why
2. **Scope creep** - Making extra changes "while I'm here"
3. **Iteration churn** - Pushing fixes that don't address the actual concern

This workflow ensures you **understand before acting** and **stay focused on the specific feedback**.

## Permission Awareness

At task start, check workflow state for active permissions:

1. **Check active workflow**: `get_active_workflow_id()` returns current workflow
2. **Get permissions**: `get_permissions(workflow_id)` returns PermissionStore
3. **Verify tool access**: `is_tool_allowed(tool_name, **context)` before operations

**Self-enforcement**: The phase table above shows allowed/blocked tools per phase. Do not attempt blocked operations - they exist to enforce the "understand before fixing" discipline.

**Programmatic check** (lib/permission_query.py):
```python
from permission_query import get_permissions, is_tool_allowed

# Check if Edit is allowed in current phase
allowed, reason = is_tool_allowed("Edit", file_path="src/auth.py")
if not allowed:
    print(f"Blocked: {reason}")  # e.g., "Edit blocked in UNDERSTAND phase"
```

**UNDERSTAND phase**: Edit/Write/Bash are blocked to force articulation of the reviewer's concern before making changes.
