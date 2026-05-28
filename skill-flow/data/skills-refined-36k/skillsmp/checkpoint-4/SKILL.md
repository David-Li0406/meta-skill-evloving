---
name: checkpoint
description: Summarize completed work, update progress tracking in DEV_SPEC.md, and prepare for next iteration. Final stage of dev-workflow pipeline. Use when task implementation and testing is completed, or when user says "完成检查点", "checkpoint", "保存进度", "save progress", "任务完成".
metadata:
  category: progress-tracking
  triggers: "checkpoint, save progress, 完成检查点, 保存进度, 任务完成"
allowed-tools: Bash(python:*) Bash(git:*) Read Write
---

# Checkpoint & Progress Persistence

This skill handles **task completion summarization** and **progress tracking synchronization**. It ensures that completed work is properly documented and the project schedule in `DEV_SPEC.md` stays up-to-date.

> **Single Responsibility**: Summarize → Persist → Prepare Next

---

## When to Use This Skill

- When a task implementation and testing is **completed**
- When you need to **manually update progress** in DEV_SPEC.md
- When you want to **generate a commit message** for completed work
- As the **final stage** of the `dev-workflow` pipeline

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 1           Step 1.5                 Step 2              Step 3      │
│  ────────         ────────                 ────────            ────────     │
│  Summarize   →   User Confirm (WHAT)  →   Persist Progress →  Commit Prep │
│  (Summarize)      (Verify work done)       (Update DEV_SPEC)   (WHETHER)   │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │   Tests Passed   │
                    └────────┬─────────┘
                             ▼
                  ┌──────────────────────┐
                  │  Step 1: Summarize   │
                  │  Generate summary    │
                  └────────┬─────────────┘
                           ▼
                  ┌──────────────────────┐
                  │ Step 1.5: User       │
                  │ Confirmation         │
                  │ Wait for user OK     │
                  └────────┬─────────────┘
                           │
                     User OK? ──No──→ Revise summary → Back to Step1
                           │
                       Yes ▼
                  ┌──────────────────────┐
                  │ Step 2: Persist      │
                  │ Progress             │
                  │ Update DEV_SPEC.md   │
                  └────────┬─────────────┘
                           ▼
                  ┌──────────────────────┐
                  │ Step 3: Commit Prep  │
                  │ Generate commit msg  │
                  │ Wait for user OK     │
                  └────────┬─────────────┘
                           │
                     User OK? ──No──→ Skip commit → Flow end
                           │
                       Yes ▼
                  ┌──────────────────────┐
                  │  Execute git commit  │
                  └────────┬─────────────┘
                           ▼
                  ┌──────────────────────┐
                  │   Checkpoint Done  │
                  └──────────────────────┘
```

---

## Step 1: Work Summary

**Goal**: Generate a clear, structured summary of completed work.

### 1.1 Collect Information

Gather the following from the current session:
- **Task ID**: e.g., `A3`, `B1`, `C5`
- **Task Name**: e.g., "配置加载与校验"
- **Files Created/Modified**: List all file changes
- **Test Results**: Pass/fail status and coverage (if available)
- **Implementation Iterations**: How many test-fix cycles occurred

### 1.2 Generate Summary Report

**Output Format**:
```
────────────────────────────────────────────────────
 TASK COMPLETED: [Task ID] [Task Name]
────────────────────────────────────────────────────

 Files Changed:
  Created:
    - src/xxx/yyy.py
    - tests/unit/test_yyy.py
  Modified:
    - src/xxx/zzz.py

 Test Results:
    - tests/unit/test_yyy.py: 5/5 passed 
    - tests/unit/test_zzz.py: 3/3 passed 
    - Coverage: 85% (if available)

 Iterations: [N] (1 = first try success)

 Spec Reference: DEV_SPEC.md Section [X.Y]
────────────────────────────────────────────────────
```

---

## Step 1.5: User Confirmation (Verify WHAT Was Done)

**Goal**: Present summary to user for verification before persisting progress.

**This confirms WHAT work was completed** - validating the summary accuracy, not whether to save it.

### 1.5.1 Confirmation Prompt

**Output Format**:
```
════════════════════════════════════════════════════
 Please Verify Completion Summary / 请验证工作总结
════════════════════════════════════════════════════

 Task: [Task ID] [Task Name]
 Spec Reference: DEV_SPEC.md Section [X.Y]

 Files Changed:
  Created:
    - src/xxx/yyy.py
    - tests/unit/test_yyy.py
  Modified:
    - src/xxx/zzz.py

 Test Results:
    - tests/unit/test_yyy.py: 5/5 passed 
    - tests/unit/test_zzz.py: 3/3 passed 

 Iterations: [N]

════════════════════════════════════════════════════
 Is this summary accurate?
 以上总结是否准确？

   Please reply: "confirm" / "确认" to save progress to DEV_SPEC.md
                "revise" / "修改" to regenerate summary
                
 Note: This only verifies the summary. DEV_SPEC.md will be updated
 after confirmation. Git commit decision comes later.
════════════════════════════════════════════════════
```

### 1.5.2 Handle User Response

| User Response | Action |
|---------------|--------|
| "confirm" / "yes" / "确认" / "是" | Proceed to Step 2 |
| "revise" / "no" / "修改" / "否" | Ask user what needs to be corrected, then regenerate summary |

**Important**: Do NOT proceed to Step 2 until user explicitly confirms.

---

## Step 2: Persist Progress

**Goal**: Update `DEV_SPEC.md` to mark the task as completed.

> **Auto-Execute**: This step runs automatically after Step 1.5 user confirmation. No additional user input required.

### 2.1 Locate Task in DEV_SPEC.md

1. Read `DEV_SPEC.md` (the **GLOBAL** file, NOT chapter files)
2. Find the task by its identifier pattern:
   - Look for `### [Task ID]：[Task Name]` (e.g., `### A3：配置加载与校验`)
   - Or look for checkbox pattern: `- [ ] [Task ID] [Task Name]`

### 2.2 Update Progress Marker

**Supported Marker Styles**:

| Before | After | Style |
|--------|-------|-------|
| `[ ]` | `[x]` | Checkbox |
| `` | `` | Emoji |
| `### A3：任务名` | `### A3：任务名 ` | Title suffix |
| `(进行中)` | `(已完成)` | Chinese status |
| `(In Progress)` | `(Completed)` | English status |

**Update Logic**:
```python
# Pseudo-code for update logic
if task_line contains "[ ]":
    replace "[ ]" with "[x]"
elif task_line contains "":
    replace "" with ""
elif task_line contains "(进行中)" or "(In Progress)":
    replace with "(已完成)" or "(Completed)"
else:
    append " " to task title
```

### 2.3 Step 2 Output Format

**Output after updating DEV_SPEC.md**:
```
────────────────────────────────────
DEV_SPEC.md Progress Updated
────────────────────────────────────
Task: [Task ID] [Task Name]
Status: [ ] -> [x]
────────────────────────────────────
```

---

## Step 3: Commit Preparation

**Goal**: Generate structured commit message and ask user whether to commit.

### 3.1 Commit Message Template

**Subject Format**:
```
<type>(<scope>): [Phase X.Y] <brief description>
```

**Template Definition**:
| Field | Description | Example |
|-------|-------------|---------|
| `<type>` | Commit type (see table below) | `feat`, `fix`, `test` |
| `<scope>` | Module/component name | `config`, `retriever`, `pipeline` |
| `[Phase X.Y]` | DEV_SPEC phase number | `[Phase 2.3]`, `[Phase A3]` |
| `<brief description>` | What was done (< 50 chars) | `implement config loader` |

**Commit Type Guidelines**:
| Change Type | Commit Prefix |
|-------------|---------------|
| New feature | `feat:` |
| Bug fix | `fix:` |
| Refactoring | `refactor:` |
| Tests only | `test:` |
| Documentation | `docs:` |
| Configuration | `chore:` |

### 3.2 Generate Commit Message

**Output Format**:
```
════════════════════════════════════════════════════
 COMMIT MESSAGE / 提交信息
════════════════════════════════════════════════════

【Subject】
feat(<module>): [Phase X.Y] implement <feature name>

【Description】
Completed DEV_SPEC.md Phase X.Y: <Task Name>

Changes:
- Added <component 1> implementation
- Added <component 2> implementation
- Added unit tests test_xxx.py

Testing:
- Command: pytest tests/unit/test_xxx.py -v
- Results: X/X passed 
- Coverage: XX% (if available)

Refs: DEV_SPEC.md Section X.Y
Task: [Task ID] <Task Name>

════════════════════════════════════════════════════
```

### 3.3 User Commit Confirmation (Decide WHETHER to Commit)

**This confirms WHETHER to commit** - deciding if changes should be committed to git now or manually later.

**Prompt User**:
```
────────────────────────────────────
 Do you want me to commit these changes?
 是否需要帮您执行 git commit？
────────────────────────────────────

Please reply / 请回复:
  "yes" / "commit" / "是" → Execute git add + git commit
  "no" / "skip" / "否"   → End flow, you can commit manually later
────────────────────────────────────
```

### 3.4 Execute Commit (If Confirmed)

**If user confirms**:
```bash
# Stage all changed files
git add <list of changed files>

# Commit with generated message
git commit -m "<subject>" -m "<description>"
```

**Success Output**:
```
────────────────────────────────────
 COMMIT SUCCESSFUL
────────────────────────────────────
Commit: <short hash>
Branch: <current branch>

Progress saved, task [Task ID] completed!
进度已保存，任务 [Task ID] 已完成！
────────────────────────────────────
```

### 3.5 Skip Commit (If Declined)

**If user declines**:
```
────────────────────────────────────
 WORKFLOW COMPLETED (No Commit)
────────────────────────────────────
 DEV_SPEC.md updated
 Git commit skipped

You can manually commit later with:
  git add .
  git commit -m "<subject>" -m "<description>"

Task [Task ID] checkpoint completed!
任务 [Task ID] 检查点完成！
────────────────────────────────────
```

---

## Quick Commands

| User Says | Behavior |
|-----------|---------|
| "checkpoint" / "完成检查点" | Full workflow (Step 1-3) with confirmations |
| "save progress" / "保存进度" | Step 1.5-2 only (confirm + persist) |
| "commit message" / "生成提交信息" | Step 3 only (generate commit message) |
| "commit for me" / "帮我提交" | Step 3 + execute git commit |

---

## Important Rules

1. **Always Update GLOBAL DEV_SPEC.md**: This is the single source of truth for progress tracking.

2. **Preserve Existing Format**: Match the marker style already used in the document (checkbox vs emoji vs text).

3. **Atomic Updates**: Update ONE task at a time. Don't batch-update multiple tasks.

4. **Two User Confirmations Required**: 
   - Step 1.5: User must confirm work summary before persisting
   - Step 3.3: User must confirm before git commit
   - **NEVER skip these confirmations!**

5. **Traceability**: Every checkpoint must reference the specific spec section that defined the task.

---
