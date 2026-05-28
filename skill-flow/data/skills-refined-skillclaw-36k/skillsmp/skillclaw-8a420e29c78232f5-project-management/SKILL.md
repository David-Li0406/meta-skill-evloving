---
name: project-management
description: Use this skill when managing projects that require efficient task division, context management, and guideline application across multiple sessions.
---

# Skill body

## Overview

This skill helps in managing projects by dividing large tasks into manageable sessions, applying relevant guidelines, and maintaining context across interruptions.

## Workflow

### 1. Load Guidelines

Automatically load relevant guidelines based on the project's technology stack to optimize token usage.

### 2. Large Task Management

#### When to Use

Use this workflow when:
- Anticipating changes in five or more files.
- Implementing multiple independent features.
- Expecting research to take over 30 minutes.
- The user mentions keywords like "large," "multiple days," or "incremental."

#### Directory Structure

```
${MEMORY_DIR}/
├── memory/YYMMDD_<task>/    # Standard memory directory
└── tasks/YYMMDD_<task_name>/       # Dedicated directory for large tasks
    ├── 00_plan.md           # Overall plan
    ├── 01_<subtask>.md      # Subtask 1
    ├── 02_<subtask>.md      # Subtask 2
    └── ...
```

### 3. Session Management

#### Starting a New Session

1. Check the latest progress files:
   ```bash
   ls .agents/progress/*.md | sort -r | head -3
   ```
2. Read the latest progress file to understand previous work.
3. Identify any unfinished tasks or handover items.

### 4. Task Implementation

#### Plan Command

**Execute in Session 1**: Create an overall plan and individual task files.

1. Clarify requirements.
2. Conduct a comprehensive investigation of the existing codebase.
3. Create the task directory.
4. Generate `00_plan.md` and individual task files.
5. Validate the plan with an agent review.

#### Implement Command

**Execute in Session 2 and beyond**: Implement the specified task.

1. Identify task files without guessing.
2. Read the overall plan and the specific task file.
3. Apply the standard workflow phases (0-5) for implementation.

### 5. Progress Files

Refer to past session progress files to maintain context and continuity in work.

#### Accessing Progress Files

- Locate files in `.agents/progress/*.md`.
- Use commands to check the latest progress or search for specific keywords.

## File Formats

### 00_plan.md (Overall Plan)

```markdown
# <Task Name> Implementation Plan

## Overview
[Brief description of the overall task]

## Background and Purpose
[Why this implementation is necessary]

## Task List

| # | Task | Dependency | Status |
|---|------|------------|--------|
| 01 | <Task Name> | - | pending |
| 02 | <Task Name> | 01 | pending |
| ... | ... | ... | ... |

## Overall Architecture
[Diagrams or descriptions]

## Risks and Concerns
| Risk | Impact | Mitigation |
|------|--------|------------|

## Agent Review Results
[Feedback and responses from the agent]
```

### Individual Task File (01_xxx.md)

```markdown
# Task XX: <Task Name>

## Purpose
[What this task aims to achieve]

## Prerequisites
- [ ] Dependency tasks (if any)
- [ ] Required environment/settings

## Completion Criteria
- [ ] Verifiable condition 1
- [ ] Verifiable condition 2

## Work Details
### Files to Change
- path/to/file1.ts
- path/to/file2.ts

### Detailed Steps
1. [Step 1]
2. [Step 2]
3. ...

### Commit Message
- `feat: ...`

## Verification Steps
```bash
# Verification commands
bun run typecheck
bun run test
```

## Notes
- [Potential issues]
- [Additional considerations]
```