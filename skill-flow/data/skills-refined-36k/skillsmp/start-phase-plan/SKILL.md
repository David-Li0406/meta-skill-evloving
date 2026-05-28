---
name: start-phase-plan
description: Mode 1 - Strategic planning with human approval before execution
args:
  task_list_file:
    type: string
    description: Path to task list markdown file (e.g., ./planning/tasks.md)
    required: true
---

# Start-Phase: Mode 1 (Plan)

Strategic refinement of task list with human approval before execution.

## Usage

```bash
/start-phase plan /path/to/task-list.md
```

**Example:**
```bash
/start-phase plan ./job-queue/prototype-build/tasks.md
```

## Purpose

Mode 1 is the **strategic gate** before execution:
- Review task list for complexity
- Force parallelism and incremental builds
- Get human approval before proceeding
- **NO execution** - planning only

## Workflow

### Step 0: Extract Folder Locations

**CRITICAL:** Derive paths from task list location

```
Task list file: /path/to/folder/tasks.md

Derived paths:
• input_folder: /path/to/folder
• planning_folder: /path/to/folder/planning

These paths NEVER change during this phase.
```

**Store these for Mode 2:**
- input_folder = directory containing task list
- planning_folder = {input_folder}/planning

---

### Step 1: Acknowledge Mode 1

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Mode 1: Strategic Planning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task list: {task_list_file}
Input folder: {input_folder}
Planning folder: {planning_folder}

Beginning strategic review...
```

---

### Step 2: Read Context

**A. Read Task List**

```bash
Read {task_list_file}
```

Extract:
- Phase name (if present in file)
- List of tasks
- Task descriptions
- Dependencies (if specified)

**B. Read Documentation Hub (if exists)**

```bash
Read {input_folder}/docs/*.md
```

Or check for Memory Bank:
```bash
Read memory-bank/systemPatterns.md
Read memory-bank/activeContext.md
```

Get context about:
- Current system architecture
- Existing patterns
- Technologies in use
- Constraints

**C. Display Current Task List**

```
📋 Current Task List

Total tasks: 8

1. Setup authentication API
2. Create user database schema
3. Build login UI
4. Implement JWT tokens
5. Add password hashing
6. Create auth middleware
7. Write integration tests
8. Deploy to staging

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Beginning strategic analysis...
```

---

### Step 3: Strategic Analysis

**Question Complexity:**

Analyze if scope is too large for one phase:

```
⚠️ Complexity Analysis

This task list aims for production-ready auth in one phase.

Concerns:
• Task 8 "Deploy to staging" suggests production scope
• 8 tasks is manageable BUT mixing prototype + production
• No clear MVP vs polish separation

Recommendation: Focus on working prototype first
• Phase 1: Basic auth (login/logout) - MVP
• Phase 2: Production hardening (security, deploy)
```

---

**Identify Parallelism:**

Find tasks that can run independently:

```
🔀 Parallelism Opportunities

Independent tasks (can run in parallel):
• Task 1: Setup auth API (backend)
• Task 3: Build login UI (frontend)
• Task 7: Write tests (QA)

Dependencies:
• Task 4 depends on Task 1 (JWT needs API)
• Task 6 depends on Task 1 (middleware needs API)
• Task 7 depends on Tasks 1, 3, 4 (integration tests)

Proposed waves:
Wave 1 (parallel): Tasks 1, 3
Wave 2 (parallel): Tasks 2, 4, 5
Wave 3 (sequential): Task 6
Wave 4 (sequential): Task 7
```

---

**Identify Sub-Agent Delegation Opportunities:**

Analyze if feature requires specialized agents:

```
🤖 Sub-Agent Delegation Analysis

Feature characteristics:
• Total files impacted: 6 (3 new, 3 modified)
• Skill sets required: Backend API, Frontend UI, Testing
• Components: API endpoint, UI form, database schema, tests

Sub-agent opportunity assessment:
✅ RECOMMEND sub-agent delegation

Rationale:
• Multiple specializations: Backend (API + DB) + Frontend (UI) + QA (tests)
• Parallel execution benefit: ~30-40% time savings
• Agent expertise: Each agent has specialized knowledge base
• Progress tracking: Granular task updates per agent

Proposed delegation:
• nextjs-backend-developer: Tasks 1, 2, 4, 5, 6 (API, DB, JWT, middleware)
• ui-developer: Task 3 (Login form UI)
• qa-engineer: Task 7 (Integration tests)

Parallel waves with agents:
Wave 1 (parallel):
  • Task 1: Setup auth API (nextjs-backend-developer)
  • Task 3: Build login UI (ui-developer)

Wave 2 (parallel):
  • Tasks 2, 4, 5: DB + JWT + hashing (nextjs-backend-developer)

Wave 3 (sequential):
  • Task 6: Middleware (nextjs-backend-developer)
  • Task 7: Tests (qa-engineer)

Expected time savings: ~2h sequential → ~1.5h parallel (25% faster)
```

**When NOT to use sub-agents:**
```
❌ Skip sub-agent delegation if:

• Single file change (documentation update, config tweak)
• <3 tasks total
• Single skill set (only backend OR only frontend, not both)
• Bug fix or hotfix (speed over tracking)
• Proof of concept / throwaway code

Use manual execution or lightweight mode instead.
```

---

**Force Incremental Builds:**

Reorder for early integration:

```
🔨 Incremental Build Strategy

Current order: Setup → Build → Test → Deploy
Problem: No integration until Task 7

Proposed order:
1. Minimal API endpoint (1h) ✅ Working code
2. Minimal UI form (1h) ✅ Integration point
3. Connect UI → API (30m) ✅ End-to-end working
4. Add JWT (1h) ✅ Still working
5. Add DB schema (1h) ✅ Still working
6. Add password hashing (30m) ✅ Still working
7. Add middleware (45m) ✅ Still working
8. Integration tests (1h) ✅ Final verification

Result: Working code after EVERY task, not just at end
```

---

### Step 4: Propose Refined Plan

Present revised task list:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Proposed Refined Plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes made:
✅ Reduced scope to MVP (removed "Deploy to staging")
✅ Reorganized for early integration
✅ Identified 2 parallel waves
✅ Ensured working code after each task

Revised Task List:

Wave 1 (Parallel - Run simultaneously):
1. Create minimal auth API endpoint (POST /login)
   Agent: nextjs-backend-developer
   Duration: ~1h
   Output: Working API endpoint

2. Create minimal login UI form
   Agent: ui-developer
   Duration: ~1h
   Output: Working form component

Wave 2 (Integration):
3. Connect UI to API (end-to-end test)
   Agent: nextjs-backend-developer
   Duration: ~30m
   Output: Login flow works end-to-end

Wave 3 (Parallel - Add features):
4. Add JWT token generation
   Agent: nextjs-backend-developer
   Duration: ~1h
   Depends on: Task 1

5. Create user database schema
   Agent: nextjs-backend-developer
   Duration: ~1h
   Depends on: Task 1

6. Add password hashing (bcrypt)
   Agent: nextjs-backend-developer
   Duration: ~30m
   Depends on: Task 5

Wave 4 (Sequential - Finalize):
7. Add auth middleware (protected routes)
   Agent: nextjs-backend-developer
   Duration: ~45m
   Depends on: Task 4

8. Write integration tests
   Agent: qa-engineer
   Duration: ~1h
   Depends on: All previous tasks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
• Total tasks: 8 (same count, better organized)
• Parallel waves: 2 (Wave 1: 2 tasks, Wave 3: 3 tasks)
• Working code after: Task 3 (end-to-end MVP)
• Estimated time: ~6-7h (vs 8h sequential)
• Time saved: ~1-2h through parallelism

Deferred to Phase 2:
• Deploy to staging
• Production security hardening
• Rate limiting
• Session management
```

---

### Step 5: Highlight Key Changes

```
🔑 Key Improvements

1. Scope Reduction ✅
   - Removed: Deploy to staging
   - Focus: Working prototype only
   - Reason: One phase, one clear goal

2. Early Integration ✅
   - Before: Integration at Task 7
   - After: Integration at Task 3
   - Benefit: Catch issues early, not late

3. Parallelism ✅
   - Wave 1: Backend + Frontend simultaneously
   - Wave 3: JWT + DB + Hashing simultaneously
   - Benefit: 1-2h time savings

4. Clear Dependencies ✅
   - Every task lists dependencies
   - Waves prevent conflicts
   - Integration points explicit

5. Incremental Value ✅
   - Task 3: MVP works end-to-end
   - Every task after: Still works
   - Never broken for long periods
```

---

### Step 6: Await Human Approval

**Present options:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✋ Human Approval Required
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This refined plan is ready for your review.

Options:
1. ✅ Approve - Proceed to Mode 2 (Execute)
2. 🔄 Revise - Suggest changes to the plan
3. ❌ Reject - Start over with different approach
4. 💬 Question - Ask about specific tasks/decisions

Which option? (1/2/3/4)
```

---

**Handle user response:**

#### Option 1: Approve ✅

```
✅ Plan Approved!

Refined task list is ready for execution.

Next step:
/start-phase execute {task_list_file}

This will:
• Finalize the approved plan (write to task list file)
• Create planning directory structure
• Generate detailed planning documents
• Begin execution with quality gates

Ready to proceed? (y/n)
```

If user says yes:
```
Great! Please run:

/start-phase execute {task_list_file}

[Mode 1 complete]
```

---

#### Option 2: Revise 🔄

```
🔄 Plan Revision

What would you like to change?

Common revisions:
• Adjust task order
• Change parallel grouping
• Add/remove tasks
• Modify task descriptions
• Adjust scope (more/less ambitious)

Please describe your requested changes:
```

**After user provides changes:**
- Update the refined plan
- Re-present revised plan
- Ask for approval again

---

#### Option 3: Reject ❌

```
❌ Plan Rejected

Would you like to:
1. Start over with different objectives
2. Use original task list as-is (not recommended)
3. Cancel phase planning

Which option? (1/2/3)
```

---

#### Option 4: Question 💬

```
💬 Questions Welcome

Ask about:
• Why tasks are ordered this way
• How parallelism works
• Why certain tasks are deferred
• Dependency reasoning
• Time estimates
• Agent assignments

Your question:
```

**After answering:**
Return to approval options.

---

### Step 7: Save Context for Mode 2

**If approved, store:**

```
Planning context saved:
• task_list_file: {path}
• input_folder: {derived from task list}
• planning_folder: {input_folder}/planning
• phase_name: {extracted or inferred}
• approved_plan: {refined task list}

Ready for Mode 2 execution.
```

---

## Important Rules

### Mode 1 Constraints

**NEVER do these in Mode 1:**
- ❌ Create directories
- ❌ Write files (except notes for user)
- ❌ Make git commits
- ❌ Execute tasks
- ❌ Run quality checks

**ONLY do these in Mode 1:**
- ✅ Read files (task list, docs, memory bank)
- ✅ Analyze and strategize
- ✅ Propose changes
- ✅ Get human approval

### Path Management

**CRITICAL - Never lose folder locations:**

```
Input folder = directory containing task list file
Planning folder = {input_folder}/planning

Example:
Task list: ./job-queue/prototype/tasks.md
→ input_folder: ./job-queue/prototype
→ planning_folder: ./job-queue/prototype/planning

All Mode 2 artifacts go in planning_folder!
```

**Always pass to Mode 2:**
- Full path to task_list_file
- Derived input_folder
- Derived planning_folder

---

## Example Session

```bash
# User starts Mode 1
/start-phase plan ./job-queue/auth-prototype/tasks.md

# System extracts paths
Input folder: ./job-queue/auth-prototype
Planning folder: ./job-queue/auth-prototype/planning

# System reads task list
[Reads 8 tasks from file]

# System analyzes
⚠️ Complexity too high for one phase
🔀 Found parallelism opportunities
🔨 Reorganized for incremental builds

# System proposes refined plan
[Shows revised 8 tasks with waves]

# System asks for approval
Options: Approve / Revise / Reject / Question

# User approves
User: 1

# System confirms
✅ Plan approved!
Next: /start-phase execute ./job-queue/auth-prototype/tasks.md

# [Mode 1 complete]
```

---

## Success Criteria

Mode 1 succeeds when:
- ✅ Task list analyzed strategically
- ✅ Parallelism opportunities identified
- ✅ Incremental build order proposed
- ✅ Complexity questioned if too high
- ✅ Human approval obtained
- ✅ Planning paths preserved
- ✅ Ready for Mode 2

---

## Notes

- **Mode 1 is fast:** 5-15 minutes of analysis
- **Human-in-loop is mandatory:** No execution without approval
- **Paths are sacred:** Never lose input_folder or planning_folder
- **Iteration is fine:** Revise plan as many times as needed
- **No work done yet:** Mode 1 is purely strategic

---

**Estimated time:** 5-15 minutes (analysis + discussion)
**Token usage:** ~2,500 tokens (comprehensive planning)
