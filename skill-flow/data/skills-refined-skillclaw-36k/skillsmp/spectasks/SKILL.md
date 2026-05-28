---
name: spec:tasks
description: Create Tasks Document - generates an implementation plan with tracked tasks based on requirements and design documents
---

# Create Tasks Document

Creates a tasks document based on the requirements and design documents. This command reads both documents and generates an implementation plan with tracked tasks.

## When to use

Use this skill when the user needs to:
- Create an implementation plan from existing requirements and design
- Generate a task breakdown for development work
- Plan the order of implementation with dependencies

## Instructions

### Step 1: Locate Documents

1. If `<args>` contains a spec name, look for:
   - Requirements at `.specs/<spec-name>/requirements.md`
   - Design at `.specs/<spec-name>/design.md`
2. If no spec name provided, list available specs in `.specs/` and ask user to choose
3. Read and analyze both documents

### Step 2: Analyze the Design

Before creating tasks:
1. Review the architecture and components from the design
2. Identify dependencies between components
3. Determine the optimal order of implementation
4. Note checkpoints for verification

### Step 3: Create the Tasks Document

Create the document at `.specs/<spec-name>/tasks.md` with this structure:

```markdown
# Implementation Plan: [Feature Name]

## Overview

[Brief description of the implementation and goals]

## Tasks

- [ ] 1. [Major Task Name]
  - [ ] 1.1 [Subtask Name]
    - [Detailed description of what to do]
    - [File to create/modify: `path/to/file.ts`]
    - [Key implementation points]
    - _Requirements: X.X, X.X_

  - [ ] 1.2 [Subtask Name]
    - [Details]
    - _Requirements: X.X_

- [ ] 2. Checkpoint - [Verification point]
  - [What to verify]
  - [How to verify]

- [ ] 3. [Next Major Task]
  - [ ] 3.1 [Subtask]
    - [Details]
    - _Requirements: X.X_

[Continue with all tasks]

- [ ] N. Final checkpoint - Complete verification
  - Ensure all tests pass
  - Verify all requirements are met

## Notes

- [Important notes about the implementation]
- [Dependencies or constraints]
- [Any special considerations]
```

### Task Structure Guidelines

1. **Group related tasks** - Major tasks contain related subtasks
2. **Include file paths** - Specify which files to create/modify
3. **Reference requirements** - Link each task to requirements with `_Requirements: X.X_`
4. **Add checkpoints** - Include verification points after major milestones
5. **Order by dependencies** - Tasks that depend on others come later
6. **Be specific** - Each subtask should be actionable and clear

### Task Types

1. **Implementation tasks** - Create or modify code
2. **Configuration tasks** - Update configs, dependencies
3. **Testing tasks** - Write unit/integration tests
4. **Cleanup tasks** - Remove old code, update references
5. **Checkpoint tasks** - Verify implementation milestones

### Checkbox States

- `[ ]` - Pending (not started)
- `[-]` - Pending tasks
- `[x]` - Completed

### Step 4: Confirm with User

After creating the document, show the user:
1. The location of the created file
2. A summary of the task breakdown
3. Total number of tasks and estimated checkpoints
4. Ask if they want to make any changes

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
