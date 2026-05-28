---
name: progress-tracker
description: Identify next development task from project schedule and validate claimed progress against actual codebase state. Serves as GPS for development - tells you where you are and where to go next. Stage 2 of dev-workflow pipeline. Use when user says "检查进度", "status", "下一个任务", "what's next", "定位任务".
metadata:
  category: progress-tracking
  triggers: "status, what's next, find task, 检查进度, 下一个任务, 定位任务"
allowed-tools: Read Bash(python:*)
---

#  Progress Tracker & Task Discovery

This skill identifies the **next development task** from the project schedule and **validates** that claimed progress matches actual code state. It serves as the "GPS" for development - telling you where you are and where to go next.

> **Single Responsibility**: Locate → Validate → Confirm

---

## When to Use This Skill

- When you need to **find the next task** to work on
- When you want to **check current project progress**
- When you suspect **progress tracking is out of sync** with actual code
- As **Stage 2** of the `dev-workflow` pipeline
- After a break to **resume development** from the correct point

---

## Workflow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Step 1              Step 2                Step 3              Step 4        │
│  ────────            ────────              ────────            ────────      │
│  Data Collection  →  Progress Validation → Task Identification → Confirm    │
│  (Data Prep)         (Validation)          (Task Confirm)       (User OK)    │
│                          │                                                   │
│                          ▼                                                   │
│                     ️ Mismatch? → Escalate to User → Fix DEV_SPEC          │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Data Collection

**Goal**: Gather information about claimed progress and actual code state.

### 1.1 Read Schedule from Spec

1. Read `.github/skills/spec-sync/specs/06-schedule.md` (Project Schedule)
2. Parse the task table to identify:
   - All tasks and their status markers
   - Current phase (A, B, C, D, E, F)
   - Tasks marked as completed vs in-progress vs not-started

### 1.2 Status Marker Recognition

| Marker | Meaning | Status |
|--------|---------|--------|
| `[ ]` | Not started | `NOT_STARTED` |
| `` | Not started | `NOT_STARTED` |
| `[~]` | In progress | `IN_PROGRESS` |
| `` | In progress | `IN_PROGRESS` |
| `[x]` | Completed | `COMPLETED` |
| `` | Completed | `COMPLETED` |
| `(进行中)` | In progress | `IN_PROGRESS` |
| `(已完成)` | Completed | `COMPLETED` |

### 1.3 Build Task List

**Output Structure**:
```
Phase A: 基础架构搭建
  [x] A1: 项目骨架初始化
  [x] A2: 日志系统搭建
  [~] A3: 配置加载与校验  ← CURRENT (in progress)
  [ ] A4: MCP Server 框架
  
Phase B: 核心模块开发
  [ ] B1: LLM 抽象接口与工厂
  [ ] B2: Embedding 服务封装
  ...
```

---

## Step 2: Progress Validation

**Goal**: Verify that claimed progress matches actual codebase state.

### 2.1 Identify Verification Targets

For each task marked as `COMPLETED` or `IN_PROGRESS`, identify expected artifacts:

| Task | Expected Artifacts |
|------|-------------------|
| A1: 项目骨架 | `pyproject.toml`, `src/`, `tests/` directories |
| A2: 日志系统 | `src/core/logging.py`, logging configuration |
| A3: 配置加载 | `src/core/settings.py`, `settings.yaml` |
| B1: LLM工厂 | `src/llm/base.py`, `src/llm/factory.py` |

### 2.2 Verify Artifacts Exist

For each expected artifact:
1. Check if file/directory exists
2. For code files, verify basic structure (imports work, classes defined)
3. Check if related tests exist and pass basic import

**Verification Commands**:
```bash
# Check file exists
test -f src/core/settings.py && echo "EXISTS" || echo "MISSING"

# Check module imports
python -c "from src.core.settings import Settings" 2>&1
```

### 2.3 Detect and Handle Mismatches

**Mismatch Types**:

| Type | Description | Severity |
|------|-------------|----------|
| `MISSING_FILE` | Task marked complete but file doesn't exist | High |
| `IMPORT_ERROR` | File exists but has import/syntax errors | High |
| `MISSING_TESTS` | Implementation exists but no tests | Medium |
| `STALE_PROGRESS` | Task marked "in progress" for multiple sessions | Medium |

**If any mismatch detected**, escalate to user:

```
────────────────────────────────────────────────────
️ PROGRESS INCONSISTENCY DETECTED
────────────────────────────────────────────────────

Schedule Claims: Phase B1 - LLM Factory (in progress)
Actual State: Phase A3 - Config Loading (incomplete)

Missing Items:
   src/core/settings.py - NOT FOUND
   tests/unit/test_config_loading.py - NOT FOUND
   A2 logging tests not verified

────────────────────────────────────────────────────
OPTIONS:
────────────────────────────────────────────────────

1. Fix progress tracking in DEV_SPEC.md
    → Update markers to reflect actual state
    → Re-run spec-sync
    → Restart task discovery
    
2. Confirm previous tasks as completed
    → Code may be in different location/branch
    → Provide explanation and proceed
    
3. Continue from actual progress
    → Skip incomplete tasks
    → Start from where code actually is

Please choose an option (1/2/3):
────────────────────────────────────────────────────
```

### Handling Each Option

**Option 1: Fix DEV_SPEC.md**
1. User provides corrected progress state
2. Update `DEV_SPEC.md` directly (the GLOBAL file)
3. Run `python .github/skills/spec-sync/sync_spec.py`
4. **Restart from Step 1** of this skill

**Option 2: Confirm Complete**
1. User explains where the code is
2. Document the explanation in session
3. Proceed to Step 3 with user's confirmation

**Option 3: Continue from Actual**
1. Identify the actual current task based on code state
2. Override the schedule's claimed position
3. Proceed to Step 3 with the corrected task

---

## Step 3: Task Identification

**Goal**: Clearly identify the single next task to work on.

### 3.1 Determine Next Task

**Priority Logic**:
1. If any task is `IN_PROGRESS` → That is the current task
2. Otherwise, find the first `NOT_STARTED` task → That is the next task
3. If all tasks complete → Report "All tasks complete"

### 3.2 Gather Task Context

For the identified task, collect:
- **Task ID**: e.g., `A3`, `B1`
- **Task Name**: e.g., "配置加载与校验"
- **Phase**: e.g., "Phase A: 基础架构搭建"
- **Spec Section**: Which chapter file contains implementation details
- **Dependencies**: Previous tasks that should be complete

### 3.3 Output Task Information

```
────────────────────────────────────────────────────
 CURRENT TASK IDENTIFIED
────────────────────────────────────────────────────

Phase:    A - 基础架构搭建
Task ID:  A3
Name:     配置加载与校验
Status:   IN_PROGRESS ()

Spec Reference:
  Schedule: specs/06-schedule.md (line XX)
  Details:  specs/03-tech-stack.md Section 3.2

Dependencies:
   A1: 项目骨架初始化
   A2: 日志系统搭建

Verification: Progress validated 
────────────────────────────────────────────────────
```

---

## Step 4: User Confirmation

**Goal**: Get explicit user confirmation before proceeding.

### 4.1 Request Confirmation

```
────────────────────────────────────────────────────
 CONFIRM TASK
────────────────────────────────────────────────────

Ready to work on:
  [A3] 配置加载与校验

Options:
   Confirm / 确认 - Proceed with this task
   Override / 指定其他 - Specify a different task
   Cancel / 取消 - Stop and review

Your choice:
────────────────────────────────────────────────────
```

### 4.2 Handle User Response

| Response | Action |
|----------|--------|
| Confirm / 确认 / Yes | Return task info to caller (dev-workflow Stage 3) |
| Override / 指定其他 | Ask for task ID, validate it exists, return that task |
| Cancel / 取消 | Stop the workflow, return to idle state |

---

## Quick Commands

| User Says | Behavior |
|-----------|----------|
| "status" / "检查进度" | Steps 1-3 (report current state, no confirmation needed) |
| "what's next" / "下一个任务" | Steps 1-3 (identify next task) |
| "find task" / "定位任务" | Full workflow (Steps 1-4) |
| "validate" / "验证进度" | Steps 1-2 only (validation report) |
| "fix progress" / "修正进度" | Step 2.4 workflow (mismatch handling) |

---

## Output Contract

When called by `dev-workflow`, this skill returns:

**Status Types**: `OK` | `MISMATCH` | `ALL_COMPLETE` | `CANCELLED`

**If status == OK**:

| Field | Example Value |
|-------|---------------|
| Task ID | `A3` |
| Task Name | `配置加载与校验` |
| Phase | `A - 基础架构搭建` |
| Spec Schedule Reference | `specs/06-schedule.md` line 142 |
| Spec Detail File | `specs/03-tech-stack.md` Section 3.2 |
| Dependencies Met | Yes/No |

**If status == MISMATCH**:
- Claimed Task vs Actual Task
- List of missing items
- User choice needed: Fix DEV_SPEC / Confirm / Continue from actual

---

## Important Rules

1. **Always Validate Before Proceeding**: Never assume the schedule is accurate. Always check actual code state.

2. **User Confirmation Required**: Don't auto-proceed to implementation. Wait for explicit user confirmation.

3. **Single Task Focus**: Identify ONE task at a time. Don't batch-identify multiple tasks.

4. **Dependency Awareness**: Warn if previous tasks appear incomplete, but let user decide how to proceed.

5. **Non-Destructive**: This skill only READS and REPORTS. It doesn't modify code or spec files (except when user explicitly chooses Option 1 in mismatch handling).

6. **Graceful Degradation**: If spec files are missing, fall back to reading `DEV_SPEC.md` directly.

---
