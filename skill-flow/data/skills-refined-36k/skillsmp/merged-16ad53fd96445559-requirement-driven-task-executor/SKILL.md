---
name: requirement-driven-task-executor
description: Use this skill when you need to automate the execution of tasks based on user-defined requirements, including analysis, planning, execution, verification, and reporting.
---

# Requirement-Driven Task Executor Skill

This skill implements a complete workflow for executing tasks driven by user requirements, covering analysis, planning, execution, verification, summarization, and archiving.

## Core Workflow

The skill follows a six-stage process:

```
Requirement Analysis → Task Planning → Task Execution → Verification → Final Report → Archiving
```

### Stage 1: Requirement Analysis

**Goal**: Read and understand all requirement files.

**Steps**:

1. Check if the `workspace/requirement/` directory exists.
   - If not, create the directory and prompt the user to place requirement files.

2. Read all requirement files:
   ```bash
   find workspace/requirement/ -type f \( -name "*.md" -o -name "*.txt" -o -name "*.doc*" \)
   ```

3. Analyze each requirement file:
   - Extract core requirements.
   - Identify dependencies.
   - Assess complexity.
   - Determine priority.

4. Create a requirement summary document:
   ```bash
   # Create in workspace/plan/
   workspace/plan/00_requirement_summary.md
   ```

**Output Format**:
```markdown
# Requirement Overview

## Requirement Sources
- requirement/req1.md
- requirement/req2.txt

## Requirement List
### REQ-001: [Requirement Name]
- **Source**: requirement/req1.md
- **Priority**: High/Medium/Low
- **Complexity**: Complex/Medium/Simple
- **Dependencies**: REQ-002
- **Description**: [Detailed description]
```

### Stage 2: Task Planning

**Goal**: Break down requirements into executable task lists.

**Steps**:

1. Create the `workspace/task/` directory (if it doesn't exist).

2. For each requirement, create task breakdowns:
   - Identify implementation steps.
   - Determine task order.
   - Define acceptance criteria.
   - Estimate execution time.

3. Generate numbered task files:
   ```
   task/01_task_[short_description].md
   task/02_task_[short_description].md
   ```

**Task File Template**:
```markdown
# Task-[Number]: [Task Title]

## Corresponding Requirement
- REQ-001: [Requirement Name]

## Task Goal
[Clearly describe what this task aims to achieve]

## Execution Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Expected Output
- File: [Path]
- Result: [Description]

## Dependency Tasks
- Task-[Number]: [Reason]

## Status
- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Revision

## Execution Log
[Fill in during execution]
```

4. Generate a master task list:
   ```
   workspace/task/00_task_manifest.md
   ```

**Task List Format**:
```markdown
# Task Execution List

## Task Overview
- Total Tasks: X
- Estimated Total Time: Y hours

## Execution Order
1. Task-01: [Title] - Corresponding REQ-001
2. Task-02: [Title] - Corresponding REQ-002
3. Task-03: [Title] - Corresponding REQ-001, REQ-003

## Dependency Graph
Task-01
  └─> Task-03
Task-02
  └─> Task-03
```

### Stage 3: Task Execution

**Goal**: Execute all planned tasks in order.

**Execution Principles**:

1. **Sequential Execution**: Execute tasks in order of their numbering.
2. **Dependency Check**: Confirm that dependent tasks are completed before execution.
3. **Status Update**: Update the status after completing each task.
4. **Error Handling**: Record errors and decide whether to continue.

**Execution Process**:
```python
for task_file in sorted(task_files):
    1. Read the task file.
    2. Check the status of dependency tasks.
    3. Update status to "In Progress".
    4. Execute task steps.
    5. Record execution results.
    6. Update status to "Completed" or "Needs Revision".
    7. Continue to the next task.
```

**Execution Log Format**:
Add to the execution log section of each task file:
```markdown
## Execution Log

### Execution Time
- Start: YYYY-MM-DD HH:MM:SS
- End: YYYY-MM-DD HH:MM:SS
- Duration: X minutes

### Execution Result
- Status: Success/Failure/Partially Completed
- Output Files: [Path List]
- Issues Encountered: [Description]
- Solutions: [Description]

### Acceptance Criteria Check
- [x] Criterion 1 - Passed
- [x] Criterion 2 - Passed
- [ ] Criterion 3 - Not Passed, Reason: [Explanation]
```

### Stage 4: Verification

**Goal**: Review all tasks to ensure they meet requirements.

**Verification Process**:

1. **Re-read all task files**:
   - Check each task/*.md in order.

2. **Verification Items**:
   - Task status should be "Completed".
   - All acceptance criteria should be met.
   - Expected outputs should exist.
   - Output content should meet requirements.

3. **Cross-Verification**:
   - Trace back to requirement files to ensure each requirement has a corresponding completed task.
   - Check consistency between tasks.
   - Verify that dependencies are correctly handled.

4. **Generate Verification Report**:
   ```
   workspace/task/99_verification_report.md
   ```

**Verification Report Format**:
```markdown
# Task Verification Report

## Verification Time
YYYY-MM-DD HH:MM:SS

## Task Completion Statistics
- Total Tasks: X
- Completed: Y
- Partially Completed: Z
- Failed: W
- Completion Rate: XX%

## Requirement Coverage Check
### REQ-001: [Requirement Name]
- Corresponding Tasks: Task-01, Task-03
- Completion Status: ✓ Completed
- Verification Result: Passed

### REQ-002: [Requirement Name]
...
```

### Stage 5: Final Report

**Goal**: Produce a comprehensive execution summary and results report.

**Report Content**:

1. Create final report files:
   ```
   workspace/report/final_report.md
   workspace/report/execution_summary.md
   ```

2. Organize all output files into `workspace/report/`.

**Final Report Format**:
```markdown
# Final Execution Report

## Execution Overview

### Project Information
- Execution Time: YYYY-MM-DD HH:MM:SS ~ YYYY-MM-DD HH:MM:SS
- Total Execution Duration: X hours Y minutes
- Number of Requirements Processed: X
- Number of Tasks Generated: Y

### Requirement Completion Status

#### Completed Requirements (X/Y)
- ✓ REQ-001: [Requirement Name]
- ✓ REQ-002: [Requirement Name]

#### Incomplete Requirements (X/Y)
- ✗ REQ-003: [Requirement Name] - Reason: [Explanation]

### Task Execution Statistics
- Successfully Completed: X
- Partially Completed: Y
- Failed: Z
- Skipped: W

## Requirement Achievement Confirmation

### REQ-001: [Requirement Name]
- **Status**: ✓ Achieved
- **Implementation Method**: 
  - Task-01: [Description]
  - Task-03: [Description]
- **Verification Result**: All acceptance criteria passed
- **Output**:
  - [File List]

### REQ-002: [Requirement Name]
...
```

### Stage 6: Archiving

**Goal**: Move the executed requirement files and related execution records to the historical records area.

**Execution Steps**:

1. Create the `workspace/history/YYYYMMDD/hhmm` directory (if it doesn't exist), where YYYYMMDD is today's date and hhmm is the current time.
2. Move files from `workspace/requirement`, `workspace/plan`, `workspace/task`, `workspace/report`, etc., into the newly created history directory, and confirm the removal of moved files.

## Task Execution Directory Structure

The standard directory structure during task execution:

```
project/workspace/
├── requirement/          # Original requirement files (provided by user)
│   ├── req1.md
│   ├── req2.txt
│   └── ...
├── plan/                 # Task planning
│   ├── 00_requirement_summary.md
├── task/                 # Execution records
│   ├── 00_task_manifest.md
│   ├── 01_task_xxx.md
│   ├── 02_task_xxx.md
│   ├── ...
│   └── 99_verification_report.md
└── report/              # Final output
    ├── final_report.md
    ├── execution_summary.md
    └── [Other output files]
```

## Execution Command Examples

You can trigger this skill with commands like:
```
"Please execute all requirements in the requirement directory."
"Analyze and execute the tasks in the requirement files."
"Read the requirements, generate a task list, and execute."
```

## Key Principles

1. **Traceability**: Each task can be traced back to its requirement, and each requirement can find its corresponding implementation tasks.
2. **Verifiability**: Clear acceptance criteria and objective verification methods.
3. **Transparency**: Detailed execution logs and complete status updates.
4. **Completeness**: Ensure all requirements are addressed, and the final report covers all aspects.

## Error Handling

### Common Error Scenarios

1. **Requirement File Not Found**:
   - Create the requirement/ directory.
   - Prompt the user to place requirement files.

2. **Task Execution Failure**:
   - Log error details.
   - Mark task status.
   - Assess whether it affects subsequent tasks.
   - Note in the final report.

3. **Dependency Task Not Completed**:
   - Check dependency status.
   - Wait or skip.
   - Record the reason for skipping.

4. **Verification Fails**:
   - Log details of failed items.
   - Provide improvement suggestions.
   - Annotate in the final report.

## Best Practices for Using This Skill

1. **Prepare Requirement Files**:
   - Use a clear structure.
   - Include explicit acceptance criteria.
   - Annotate priorities and dependencies.

2. **Monitor Execution**:
   - Regularly check task statuses.
   - Address errors promptly.
   - Maintain complete records.

3. **Rigorous Verification**:
   - Do not skip verification steps.
   - Cross-verify requirements and tasks.
   - Ensure quality standards are met.

4. **Document Maintenance**:
   - Keep document structures clear.
   - Update statuses promptly.
   - Record important decisions.

## Advanced Features

### Parallel Task Support

For tasks without dependencies, identify and mark them for parallel execution:
```markdown
## Parallel Executable Task Groups
- Group 1: Task-02, Task-04, Task-05
- Group 2: Task-07, Task-08
```

### Milestone Tracking

Set milestones in the task list:
```markdown
## Milestones
- Milestone 1: Basic Functionality Completed (Task-01 ~ Task-05)
- Milestone 2: Core Functionality Completed (Task-06 ~ Task-10)
- Milestone 3: All Functionality Completed (Task-11 ~ Task-15)
```

### Risk Management

Identify risks during the task planning stage:
```markdown
## Risk List
- Risk-01: [Description] - Affects Task-XX - Mitigation Measures: [Description]
```

## Reference Documents

For detailed implementation examples and templates, refer to:
- `references/task-template.md` - Detailed task file template.
- `references/report-examples.md` - Examples of various reports.

---

This skill ensures a systematic, traceable, and verifiable requirement-driven development process, ultimately producing a comprehensive execution report.