---
name: problem-solver
description: Intelligent problem-solving orchestrator that iteratively investigates issues, applies fixes, and verifies success criteria until resolved or exhausted.
---

# Problem Solver Orchestrator

Iterative problem-solving workflow - creates debug context, researches causes, applies fixes, verifies against success criteria, and loops until resolved.

## Execution Flow

1. **Initialize Debug Context** → Create debug spec with issue and success criteria
2. **Research Phase** → Researcher agent investigates code, finds potential causes
3. **Execute Phase** → Executor agent applies fixes, runs verification tests
4. **Verify Success** → Check if success criteria met
5. **Loop or Complete** → If not met, update context and repeat; if exhausted, report

---

## Available Agents

| Agent | Subagent Type | Description |
|-------|---------------|-------------|
| researcher | debug-researcher | Investigates codebase, identifies potential causes |
| executor | debug-executor | Applies fixes, runs tests, verifies success criteria |

---

## Workflow Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                   PROBLEM SOLVER WORKFLOW                       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────┐                                          │
│  │ User Request    │ "Fix E2E test failure in test_X.py"      │
│  └────────┬────────┘                                          │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────┐                                          │
│  │ 1. Initialize   │ Create specs/debug-XXX/context.md        │
│  │    Context      │ - Issue description                      │
│  │                 │ - Success criteria                        │
│  │                 │ - Verification command                    │
│  └────────┬────────┘                                          │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────┐                                          │
│  │ 2. Research     │ debug-researcher agent                   │
│  │                 │ - Read context.md                        │
│  │                 │ - Explore codebase                        │
│  │                 │ - Identify potential causes               │
│  │                 │ - Recommend operations                    │
│  └────────┬────────┘                                          │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────┐                                          │
│  │ 3. Execute      │ debug-executor agent                     │
│  │                 │ - Read context.md + research findings     │
│  │                 │ - Add debug logs if needed                │
│  │                 │ - Apply recommended fix                   │
│  │                 │ - Run verification command                │
│  └────────┬────────┘                                          │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────┐                                          │
│  │ 4. Verify       │ Check success criteria                   │
│  │                 │ - Tests pass?                             │
│  │                 │ - Metrics met?                            │
│  └────────┬────────┘                                          │
│           │                                                    │
│      ┌────┴────┐                                              │
│      │         │                                              │
│      ▼         ▼                                              │
│   ┌─────┐   ┌─────┐                                          │
│   │ YES │   │ NO  │                                          │
│   └──┬──┘   └──┬──┘                                          │
│      │         │                                              │
│      ▼         ▼                                              │
│  ┌───────┐  ┌──────────────────┐                             │
│  │SUCCESS│  │ Update context   │                             │
│  │REPORT │  │ - New issue found │                             │
│  └───────┘  │ - Iteration++    │                             │
│             └────────┬─────────┘                             │
│                      │                                        │
│                      ▼                                        │
│             ┌──────────────────┐                             │
│             │iteration < max?  │                             │
│             └────────┬─────────┘                             │
│                 ┌────┴────┐                                   │
│                 ▼         ▼                                   │
│              ┌─────┐   ┌─────┐                               │
│              │ YES │   │ NO  │                               │
│              └──┬──┘   └──┬──┘                               │
│                 │         │                                   │
│                 ▼         ▼                                   │
│            Loop to    ┌─────────┐                            │
│            Step 2     │EXHAUSTED│                            │
│                       │ REPORT  │                            │
│                       └─────────┘                            │
└────────────────────────────────────────────────────────────────┘
```

---

## Debug Context Spec Structure

**Location**: `specs/debug-<issue-id>/context.md`

```markdown
# Debug Context: [Issue Title]

**Debug ID**: debug-<timestamp>
**Created**: <ISO8601>
**Status**: investigating | fixing | verifying | resolved | exhausted
**Iteration**: 1 / 5

## Issue Description

[Detailed description of the problem]

## Success Criteria

How to verify the issue is resolved:

- **SC-001**: [Specific, measurable criterion]
- **SC-002**: [Another criterion if applicable]

## Verification Command

```bash
<command to verify success>
```

## Investigation History

### Iteration 1

**Timestamp**: <ISO8601>
**Research Findings**:
- [Finding 1]
- [Finding 2]

**Recommended Operations**:
1. [Operation 1]
2. [Operation 2]

**Applied Fix**:
- [Description of fix applied]
- [Files modified]

**Result**: PASS | FAIL
**New Issue** (if FAIL): [Description of new issue discovered]

---

### Iteration 2
...
```

---

## Context Passing

### WORKFLOW_CONTEXT (to researcher)

```json
{
  "workflow_id": "<uuid>",
  "debug_id": "debug-<timestamp>",
  "debug_dir": "specs/debug-<debug_id>/",
  "context_file": "specs/debug-<debug_id>/context.md",
  "iteration": 1,
  "max_iterations": 5,
  "issue_description": "<original issue>",
  "success_criteria": ["SC-001: ...", "SC-002: ..."],
  "verification_command": "<bash command>",
  "previous_results": {
    "debug-researcher": null,
    "debug-executor": null
  }
}
USER_REQUEST: <original user request>
```

### RESEARCH_CONTEXT (researcher → executor)

```json
{
  "research_from": "debug-researcher",
  "iteration": 1,
  "findings": [
    {
      "category": "ROOT_CAUSE | SYMPTOM | RELATED",
      "description": "<finding>",
      "location": "<file:line>",
      "confidence": "HIGH | MEDIUM | LOW"
    }
  ],
  "recommended_operations": [
    {
      "priority": 1,
      "operation": "ADD_LOG | MODIFY_CODE | FIX_CONFIG | UPDATE_TEST",
      "target_file": "<path>",
      "description": "<what to do>",
      "rationale": "<why this might fix it>"
    }
  ]
}
```

### FEEDBACK_CONTEXT (executor → orchestrator)

```json
{
  "feedback_from": "debug-executor",
  "iteration": 1,
  "fix_applied": {
    "operations": ["<op1>", "<op2>"],
    "files_modified": ["<file1>", "<file2>"]
  },
  "verification_result": {
    "command": "<verification command>",
    "exit_code": 0,
    "output_summary": "<key output>",
    "success_criteria_met": false
  },
  "new_issue": {
    "description": "<new issue discovered>",
    "evidence": "<error message or log>"
  }
}
```

---

## Orchestrator Protocol

### PHASE 1: INITIALIZATION

```bash
# 1. Generate debug ID
debug_id="debug-$(date +%Y%m%d%H%M%S)"
debug_dir="specs/${debug_id}"

# 2. Create debug directory
mkdir -p "${debug_dir}"

# 3. Create context.md from user request
# Extract: issue description, success criteria, verification command
# Write to: ${debug_dir}/context.md
```

### PHASE 2: RESEARCH LOOP

```bash
# For each iteration:
iteration=1
max_iterations=5

while [ $iteration -le $max_iterations ]; do
  # 2a. Invoke researcher agent
  Task(subagent_type="debug-researcher", prompt="""
  WORKFLOW_CONTEXT:
  {
    "debug_id": "${debug_id}",
    "context_file": "${debug_dir}/context.md",
    "iteration": ${iteration}
  }
  """)

  # 2b. Parse research findings
  # 2c. Update context.md with findings

  # 2d. Invoke executor agent
  Task(subagent_type="debug-executor", prompt="""
  WORKFLOW_CONTEXT:
  {
    "debug_id": "${debug_id}",
    "context_file": "${debug_dir}/context.md",
    "iteration": ${iteration}
  }
  RESEARCH_CONTEXT:
  ${researcher_output}
  """)

  # 2e. Check verification result
  if executor_result.success_criteria_met; then
    status="resolved"
    break
  fi

  # 2f. Update context with new issue
  # 2g. Increment iteration
  iteration=$((iteration + 1))
done
```

### PHASE 3: REPORT

**Success Report**:
```
## Problem Solved

**Debug ID**: debug-XXXXXX
**Iterations Used**: 2 / 5
**Total Time**: 15 minutes

### Issue
[Original issue description]

### Solution
[Description of fix that worked]

### Files Modified
- path/to/file1.py
- path/to/file2.py

### Verification
```bash
<verification command>
```
Output: PASS
```

**Exhausted Report**:
```
## Unable to Resolve

**Debug ID**: debug-XXXXXX
**Iterations Used**: 5 / 5

### Issue
[Original issue description]

### Investigation Summary
1. Iteration 1: Tried X, discovered Y
2. Iteration 2: Tried A, discovered B
...

### Remaining Issue
[Current state of the problem]

### Recommendations
- Manual investigation of [area]
- Consider [alternative approach]

### Debug Artifacts
- Context: specs/debug-XXXXXX/context.md
- Logs: [any debug logs added]
```

---

## Agent Response Contract

### Researcher Response

```json
{
  "agent": "debug-researcher",
  "status": "success | error",
  "timestamp": "<ISO8601>",
  "execution_time_ms": <number>,
  "result": {
    "debug_id": "<debug_id>",
    "iteration": 1,
    "findings": [...],
    "recommended_operations": [...],
    "confidence_level": "HIGH | MEDIUM | LOW",
    "files_analyzed": ["<file1>", "<file2>"]
  }
}
```

### Executor Response

```json
{
  "agent": "debug-executor",
  "status": "success | error",
  "timestamp": "<ISO8601>",
  "execution_time_ms": <number>,
  "result": {
    "debug_id": "<debug_id>",
    "iteration": 1,
    "fix_applied": {
      "operations": [...],
      "files_modified": [...]
    },
    "verification_result": {
      "command": "<cmd>",
      "success_criteria_met": true | false,
      "output_summary": "<summary>"
    },
    "new_issue": null | { "description": "...", "evidence": "..." },
    "debug_logs_added": ["<file1:line>", "<file2:line>"],
    "debug_logs_removed": ["<file1:line>"]
  }
}
```

---

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| max_iterations | 5 | Maximum research-execute cycles |
| verification_timeout | 300000 | Timeout for verification command (ms) |
| auto_cleanup_logs | true | Remove debug logs after success |

---

## Usage Examples

```bash
# Basic usage - fix a failing test
problem-solver: Fix test_full_pipeline failing with timeout error

# With explicit success criteria
problem-solver: Fix audio sync drift, success when A/V offset < 100ms

# With specific verification command
problem-solver: Fix memory leak in segment_buffer, verify with: make e2e-test -k memory

# For specific test file
fix: tests/e2e/test_full_pipeline.py - RTMP output has no audio

# Quick debug session
debug: Why is STS receiving empty fragments?
```

---

## Triggers

| Trigger | Action |
|---------|--------|
| `problem-solver:` | Full problem-solving workflow |
| `fix:` | Alias for problem-solver |
| `debug:` | Alias for problem-solver |
| `investigate:` | Research-only mode (no execution) |

---

## Constraints

**MUST**:
- Create debug context spec before any research
- Verify success criteria after each fix attempt
- Document all iterations in context.md
- Clean up debug logs after successful resolution
- Stop at max_iterations and report

**MUST NOT**:
- Skip verification step
- Apply fixes without documenting
- Leave debug logs in code after success
- Continue beyond max_iterations without reporting

---

*Problem Solver Orchestrator - Iterative debugging with context persistence and verification loops*
