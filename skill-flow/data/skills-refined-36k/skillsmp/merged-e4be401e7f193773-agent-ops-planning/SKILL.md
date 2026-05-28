---
name: agent-ops-planning
description: "Use this skill to produce a thorough plan before implementation, clarifying unknowns, creating plan iterations based on confidence level, validating each, and finalizing the plan."
---

# Planning workflow

**Works with or without `aoc` CLI installed.** Issue tracking can be done via direct file editing.

## Issue Tracking (File-Based — Default)

| Operation | How to Do It |
|-----------|--------------|
| Create planning issue | Append to `.agent/issues/medium.md` with type `PLAN` |
| Update status | Edit `status:` field directly in priority file |
| Add log entry | Append to issue's `### Log` section |
| Show issue | Search for issue ID in priority files |

### Build Commands (from constitution)

```bash
# Read actual commands from .agent/constitution.md to understand project structure
build: uv run python -m build
test: uv run pytest
```

### Reference Documents

Implementation details are stored as markdown:
```
.agent/issues/references/{ISSUE-ID}-impl-plan.md
```

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Operation | Command |
|-----------|---------|
| Create planning issue | `aoc issues create --type PLAN --title "..."` |
| Update status | `aoc issues update <ID> --status in-progress` |
| Add log entry | `aoc issues update <ID> --log "Plan iteration 2 complete"` |
| Show issue | `aoc issues show <ID>` |

## Preconditions
- Work should be tracked as an issue before planning begins.
- Constitution exists and is baseline-ready (or stop and run constitution workflow).
- Baseline exists if any code change is expected (or stop and run baseline workflow first).

## Issue-First Principle

Before starting detailed planning:

1. **Check for existing issue**: Is there already an issue for this work?
   - Yes → proceed with planning, reference the issue ID.
   - No → suggest creating one first.

2. **Create issue if needed**:
   ```
   This work isn't tracked yet. Create an issue first?
   
   Suggested: FEAT-{next}@{hash} — "{title from request}"
   Priority: {inferred priority}
   
   [Y]es, create and continue / [N]o, plan without issue
   ```

3. **Reference issue throughout**:
   - Plan title: "Plan for {ISSUE-ID}: {title}"
   - Update issue status to `in_progress` when planning starts.
   - Link plan to issue in notes section.

## Iterations based on confidence

| Confidence | Minimum iterations | Validation depth | Implementation Details Level |
|------------|-------------------|------------------|------------------------------|
| low        | 3+                | exhaustive — question everything | **extensive** — full code snippets, edge cases, test scenarios |
| normal     | 2                 | standard — validate key assumptions | **normal** — pseudo-code, signatures, data flow |
| high       | 1 (or skip)       | quick — trust established patterns | **low** — bullet points, files, approach |

Read confidence from:
1. Task's `confidence` field (if set).
2. Otherwise, constitution's default confidence.

## Low Confidence Mandatory Interview (invoke `agent-ops-interview`)

**When confidence is LOW, an interview is MANDATORY before planning begins.**

This ensures assumptions are surfaced and clarified with the human before any design work.

### Interview Trigger

```
🎯 LOW CONFIDENCE DETECTED — Mandatory Interview Required

Before planning {ISSUE-ID}, I need to clarify key aspects with you.
This is required for low confidence work to reduce implementation risk.

Starting structured interview (one question at a time)...
```

### Interview Questions Template

Ask these questions ONE AT A TIME, waiting for response before proceeding:

1. **Scope Boundaries**
   ```
   Q1: What is explicitly OUT OF SCOPE for this issue?
   (List anything I should NOT touch or change)
   ```

2. **Expected Behavior**
   ```
   Q2: Can you describe the expected behavior in specific terms?
   (What should happen when X? What output for input Y?)
   ```

3. **Edge Cases**
   ```
   Q3: What edge cases should I consider?
   (Empty inputs, errors, concurrent access, etc.)
   ```

4. **Testing Expectations**
   ```
   Q4: What testing approach do you expect?
   (Unit tests? Integration? Manual verification? Specific scenarios?)
   ```

5. **Success Criteria**
   ```
   Q5: How will you know this is done correctly?
   (What will you check during code review?)
   ```

6. **Known Constraints**
   ```
   Q6: Are there any constraints I should know about?
   (Performance requirements, compatibility, dependencies, etc.)
   ```

### Interview Notes Capture

After interview completes:

1. Summarize answers in issue notes section.
2. Create `.agent/issues/references/{ISSUE-ID}-interview.md` if answers are extensive.
3. Link interview notes from issue's `spec_file` or `notes` field.

```markdown
### Interview Summary (YYYY-MM-DD)
- **Out of scope**: {answer}
- **Expected behavior**: {answer}
- **Edge cases**: {answer}
- **Testing**: {answer}
- **Success criteria**: {answer}
- **Constraints**: {answer}
```

### Interview Bypass (NOT RECOMMENDED)

User may skip interview, but must acknowledge the risk:

```
⚠️ Skipping interview for low confidence issue is NOT recommended.
This increases risk of incorrect implementation.

Skip anyway? [Y]es, I accept the risk / [N]o, let's do the interview
```

If skipped, log in issue: "Interview skipped by user — higher risk accepted".

## Procedure
1) Intake:
   - Restate the goal (1–3 lines).
   - List unknowns as explicit questions.
   - Stop and ask until clarified; no guessing.

2) Plan iteration 1:
   - Steps.
   - Files expected to change.
   - Files that must not change.
   - Test strategy.
   - Risks/unknowns.
   - Why it is minimal change.

3) Validate iteration 1:
   - Check every requirement.
   - Check constitution constraints.
   - Check baseline constraints.
   - Identify assumptions; convert assumptions into questions.

4) Plan iteration 2+ (if confidence requires):
   - Revise based on validation.
   - Tighten diffs and test plan.

5) **Generate Implementation Details** (invoke `agent-ops-impl-details`):
   - Determine detail level from confidence (see table above).
   - Generate detailed implementation specification.
   - Save to `.agent/issues/references/{ISSUE-ID}-impl-plan.md`.
   - Link from issue's `spec_file` field.

6) Final implementation plan:
   - Numbered steps.
   - Acceptance criteria mapping.
   - Test plan mapping.
   - **Reference to implementation details file**.

7) Approval gate (based on confidence):
   - low: HARD gate — wait for explicit approval, plan for single issue only.
   - normal: SOFT gate — ask "Ready to implement?", continue if no objection.
   - high: MINIMAL — proceed unless user objects.

   **LOW confidence additional requirements:**
   - Plan must cover exactly 1 issue (no batching).
   - Reference document in `.agent/issues/references/` is MANDATORY.
   - Implementation will have HARD STOP after completion for human review.
   - Test coverage threshold: ≥90% line, ≥85% branch on changed code.

8) Update `.agent/focus.md` and issue status via `agent-ops-state`.

## Implementation Details Integration

**MANDATORY: After plan iterations are complete, you MUST generate implementation details.**

This is not optional. Every plan must have an implementation details file.

### Low Confidence → Extensive Details

For risky, complex, or uncertain changes:

```
Invoking agent-ops-impl-details with level: extensive

Output MUST include:
- ACTUAL EXECUTABLE CODE for each change (not pseudo-code).
- Complete function implementations with types.
- Edge case handling with specific code.
- Error scenarios with specific exception handling.
- Full test cases with assertions.
- Import statements.
- Docstrings.
```

**Example extensive output:**
```python
# File: src/services/user.py
# Change: Add process_user function

from datetime import datetime
from typing import Optional
from .models import User, UserResult
from .exceptions import NotFoundError

def process_user(user_id: str, db: Database) -> UserResult:
    """Process user with validation.
    
    Args:
        user_id: The user's unique identifier.
        db: Database connection.
        
    Returns:
        UserResult with processed user data.
        
    Raises:
        ValueError: If user_id is invalid.
        NotFoundError: If user doesn't exist.
    """
    if not user_id:
        raise ValueError("user_id is required")
    
    user = db.get_user(user_id)
    if user is None:
        raise NotFoundError(f"User {user_id} not found")
    
    return UserResult(
        id=user.id,
        name=user.name,
        processed_at=datetime.utcnow(),
    )
```

### Normal Confidence → Normal Details

For standard features and typical changes:

```
Invoking agent-ops-impl-details with level: normal

Output includes:
- Function signatures with parameter types.
- Pseudo-code for logic flow.
- Data structure definitions.
- API contracts (request/response).
- Key test scenarios (not full code).
```

### High Confidence → Low Details

For simple, well-understood changes:

```
Invoking agent-ops-impl-details with level: low

Output includes:
- Files to change with brief description.
- High-level approach (1-2 sentences per file).
- Dependencies and risks.
- Basic test coverage outline.
```

### Detail Level Override

User can override the default level:

```
Plan with extensive details regardless of confidence? [y/n]
```

Or specify in the planning request: "Plan with extensive implementation details".

## Issue Discovery During Planning

**During planning, invoke `agent-ops-tasks` discovery procedure for:**

1) **Sub-tasks discovered**:
   - Large feature breaks into multiple issues.
   - Prerequisites that need addressing first.
   - "Before we can do X, we need to Y".

2) **Risks identified**:
   - Technical risks → `CHORE` or `TEST` issues.
   - Security concerns → `SEC` issues.
   - Performance concerns → `PERF` issues.

3) **Dependencies found**:
   - External blockers → blocked issues.
   - Missing APIs/features → `FEAT` issues.

**Present after plan iteration:**
```
📋 Planning revealed {N} additional work items:

- [FEAT] API endpoint for user preferences (prerequisite).
- [TEST] Integration tests needed for payment flow.
- [DOCS] Update API documentation for new fields.

Create issues for these? [A]ll / [S]elect / [N]one

These will be linked as dependencies/related to {ORIGINAL-ISSUE-ID}.
```

**After creating sub-issues:**
```
Created {N} related issues. What's next?

1. Continue planning {ORIGINAL-ISSUE-ID} (with dependencies noted).
2. Plan the prerequisite first ({NEW-ISSUE-ID}).
3. Review all related issues.
```