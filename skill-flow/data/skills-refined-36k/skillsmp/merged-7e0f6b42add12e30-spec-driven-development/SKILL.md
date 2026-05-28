---
name: spec-driven-development
description: Use this skill when you need to clarify specifications before implementing features, generating an implementation plan and task list.
---

# Spec-Driven Development

This skill clarifies specifications before feature implementation, generating an implementation plan and task list.

## ⚠️ Important: System Diagrams are Required

The generated `implementation-plan.md` must **include system diagrams (state machine diagram + data flow diagram)**. An `implementation-plan.md` without these diagrams is considered incomplete.

## Workflow Overview

```
1. User communicates their objectives
   ↓
2. Conduct interactive questioning in AskUserQuestion format
   ↓
3. Generate implementation-plan.md
   ↓
4. Review with Codex or Copilot → Correction loop (automated)
   ↓
5. Generate tasks.md
   ↓
6. Present to the user
```

## Step 1: Questioning

Upon receiving user requests, ask questions in the following categories, grouping 1-4 questions at a time.

### Required Question Categories

**Batch 1: Scope Confirmation**
- What do you want to achieve (objective)?
- Scope of impact (new / existing modification)?
- Priority and urgency?

**Batch 2: Technical Details**
- Technologies and frameworks to be used?
- Dependencies?
- Data structures and API design?

**Batch 3: Quality Requirements**
- Edge cases and error handling?
- Testing requirements?
- Performance requirements?

Refer to `references/question-patterns.md` for detailed questioning formats.

## Step 2: Generate implementation-plan.md

Based on the questioning results, generate `.specs/{feature-name}/implementation-plan.md`.

Template: `assets/templates/implementation-plan.md`

### Step 2-1: Write Each Section

- 1 feature = 1 plan (keep it small)
- Clearly specify changes at the file level
- Use `[NEW]`, `[MODIFY]`, `[DELETE]` tags
- Always include a verification plan
- **Include system diagrams** (state machine diagram + data flow diagram)

### Step 2-2: Create System Diagrams

Always create state machine and data flow diagrams to:
- Visualize all paths, branches, and edge cases
- Prevent implementation oversights
- Validate correctness at the system level

```
Example ASCII Diagram:

    Input
      │
      ▼
┌─────────────┐
│  STATE_A    │─── Condition1 ───▶ STATE_B
└─────────────┘                  │
      │                          │
   Condition2                  Condition3
      │                          │
      ▼                          ▼
┌─────────────┐           ┌─────────────┐
│  STATE_C    │           │  STATE_D    │
└─────────────┘           └─────────────┘
```

Elements to include in the diagram:
- **States**: Clearly name each state
- **Transition Conditions**: What triggers state changes
- **Branches**: Cover all conditional branches
- **Edge Cases**: Transitions during errors or timeouts
- **Loops**: If there are repetitive processes

### Step 2-3: Completion Checklist

After generating `implementation-plan.md`, confirm the following:

- [ ] Is the state machine diagram included?
- [ ] Is the data flow diagram included?
- [ ] Do the diagrams include all states, transition conditions, and edge cases?
- [ ] Are the diagrams consistent with the content of each section?

**If the checklist is not met, the generation is not considered complete.**

## Step 3: Review Loop

Review the generated `implementation-plan.md` with Codex or GitHub Copilot CLI.

### Review Execution

```bash
codex exec --full-auto "Please review the following implementation plan.

Review Criteria:
1. Are there any ambiguities or omissions in the specifications?
2. Are there any issues with feasibility?
3. Are edge cases considered?
4. Is the file structure reasonable?
5. Is there consistency with the overall architecture?

If there are no issues, please respond with 'No issues'. If there are problems, provide specific feedback and improvement suggestions."
```

### Loop Processing

1. Analyze the output from Codex or Copilot
2. If "No issues", proceed to Step 4
3. If there are issues:
   - Revise `implementation-plan.md` based on feedback
   - Re-run the review
   - Loop up to 5 times

Refer to `references/review-criteria.md` for detailed review criteria.

## Step 4: Generate tasks.md

After review completion, generate `.specs/{feature-name}/tasks.md`.

Template: `assets/templates/tasks.md`

### Task Structure

```
Task: {Objective}

□ Research & Planning
  □ Subtask 1
  □ Subtask 2

□ Implementation  
  □ Subtask 1
  □ Subtask 2

□ Verification
  □ Subtask 1
  □ Subtask 2
```

## Step 5: User Confirmation

Present the generated files to the user:

1. Summary of `implementation-plan.md`
2. List of tasks from `tasks.md`
3. "Please let us know if any corrections are needed."

If the user requests corrections, return to Step 3.

## Output Directory

```
.specs/
└── {feature-name}/
    ├── implementation-plan.md
    └── tasks.md
```

`{feature-name}` should be named in kebab-case (e.g., `user-authentication`, `block-button`).