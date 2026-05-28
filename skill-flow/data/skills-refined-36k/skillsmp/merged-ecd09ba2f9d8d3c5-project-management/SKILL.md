---
name: project-management
description: Use this skill for managing projects efficiently, especially when dealing with large tasks, development support, and guideline loading.
---

# Project Management Workflow

This skill encompasses various workflows for managing projects, including loading guidelines, handling large tasks, and providing development support.

## Loading Guidelines

Automatically load guidelines based on the detected technology stack of the project, applying only the necessary guidelines to the session to save tokens.

## Large Task Workflow

Efficiently implement large tasks by splitting them into multiple sessions.

### Conditions for Automatic Use

This skill is automatically triggered under the following conditions:
1. Anticipation of changes to five or more files.
2. Inclusion of multiple independent feature implementations.
3. Research expected to take over 30 minutes.
4. User mentions keywords like "large-scale," "multi-day," or "incremental."

### Directory Structure

```
${MEMORY_DIR}/
├── memory/YYMMDD_<task>/    # Standard memory directory (existing Phase 0-5)
└── tasks/YYMMDD_<task_name>/       # Dedicated for large tasks (this skill)
    ├── 00_plan.md           # Overall plan
    ├── 01_<subtask>.md      # Individual task 1
    ├── 02_<subtask>.md      # Individual task 2
    └── ...
```

- `MEMORY_DIR`: Defined in PJ CLAUDE.md (default: `.local/`)
- `task_name`: A short name to identify the task (e.g., `data-site`, `auth-refactor`)

### Subcommands

#### /large-task plan

**Execute in Session 1**: Comprehensive investigation → Create overall plan + individual task files.

1. Clarify requirements (confirm with AskUserQuestion).
2. Conduct comprehensive investigation:
   - Review existing codebase.
   - Reference external information via context7/WebSearch.
3. Create directory `${MEMORY_DIR}/tasks/YYMMDD_<task_name>/`.
4. Create `00_plan.md` (overall plan).
5. Create `01_xxx.md`, `02_xxx.md...` (individual tasks).
6. Validate the plan with agent review (request user execution).

#### /large-task implement <task_num>

**Execute in Sessions 2 and beyond**: Implement the specified task.

1. Identify task files (do not guess):
   - Use `Glob("${tasks_dir}/*.md")` to list files.
   - Identify files starting with `<task_num>_`.
2. Read `00_plan.md` and the identified task file.
3. Apply Phase 0-5 for implementation.

### File Formats

#### 00_plan.md (Overall Plan)

```markdown
# <Task Name> Implementation Plan

## Overview
[1-2 sentences explaining the overall picture]

## Background and Purpose
[Why this implementation is necessary]

## Task List

| # | Task | Dependency | Status |
|---|------|------------|--------|
| 01 | <Task Name> | - | pending |
| 02 | <Task Name> | 01 | pending |
| ... | ... | ... | ... |

Status: pending / in_progress / completed

## Overall Architecture
[Diagram or explanation]

## Risks and Concerns
| Risk | Impact | Mitigation |
|------|--------|------------|

## Agent Review Results
[Feedback and responses from the agent during the planning phase]
```

#### Individual Task Files (01_xxx.md, etc.)

Template: [references/task-template.md](references/task-template.md)

```markdown
# Task XX: <Task Name>

## Purpose
[What this task aims to achieve]

## Prerequisites
- [ ] Dependent tasks (if any)
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

### Commit
- `feat: ...`

## Verification Steps
```bash
# Verification command
bun run typecheck
bun run test
```

## Notes
- [Pitfall 1]
- [Pitfall 2]
```

### Integration with Phase 0-5

When implementing each task, apply the standard Phase 0-5 workflow.

1. **Phase 0**: Create `memory/YYMMDD_<task>/`, initialize `05_log.md`.
2. **Phase 1**: Conduct detailed investigation based on the task file's "Work Details."
3. **Phase 2**: Create detailed plans if necessary.
4. **Phase 3**: Implementation (4 steps: investigation → planning → execution → review).
5. **Phase 4**: Quality assurance + agent review (request user execution).
6. **Phase 5**: Completion report, update status in `00_plan.md`.

### Development Support

This skill is optimized for short, interruptible development sessions. It aids in feature design, documentation creation (requirements, architecture, test plans, roadmaps), context management during interruptions, and resuming work. It supports any technology stack and helps maintain productivity even in fragmented work sessions.

## References

- Workflow details: @context/workflow-rules.md
- Memory file formats: @context/memory-file-formats.md
- Task tool utilization: @context/task-tool-guide.md
- Agent CLI: @context/agent-cli-guide.md
- Project-specific settings: PJ CLAUDE.md