# Workflow Phases - Detailed Guide

This document provides comprehensive instructions for each phase of the feature development workflow.

## Phase 1: Discovery

### Purpose
Transform vague requirements into clear, actionable decisions.

### Entry Criteria
- User has expressed a feature request
- Feature workspace initialized with `init.sh`

### Process

**Step 1: Initialize Workspace**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/init.sh {feature-name}
```

**Step 2: Understand the Request**
Ask clarifying questions:
- What problem is being solved?
- Who are the users?
- What's the expected outcome?
- What constraints exist (time, tech, compatibility)?

**Step 3: Identify Decision Points**
Use numbered questions format:
```markdown
## Q1: [Decision Point Title]

问题描述...

Options:
- A. Option one - [pros/cons]
- B. Option two - [pros/cons]

Recommendation: [Your suggestion with reasoning]
```

**Step 4: Record Decisions**
Update README.md with confirmed decisions.

**Step 5: Update Progress**
Update progress.md:
- phase: 1
- phase_name: discovery
- Add decisions to decisions array

### Exit Criteria
- All key decisions confirmed by user
- README.md updated with decisions
- progress.md updated

### GATE
**Must have user confirmation before proceeding to Phase 2**

---

## Phase 2: Codebase Exploration

### Purpose
Deeply understand existing code patterns before designing new features.

### Entry Criteria
- Phase 1 completed
- User confirmed decisions

### Process

**Step 1: Launch Exploration Agents**
Launch 2-3 `codebase-explorer` agents in parallel with different focuses:

```markdown
Agent 1: "Find features similar to {feature} and trace implementation"
Agent 2: "Map architecture and abstractions for {related area}"
Agent 3: "Analyze current implementation of {existing feature}"
```

**Step 2: Synthesize Findings**
After agents return:
- Compile list of essential files
- Read all identified files
- Note patterns and conventions

**Step 3: Present Summary**
Create findings summary:
```markdown
## Codebase Analysis: {Feature}

### Similar Features Found
- Feature A: `path/file.ts` - Pattern used
- Feature B: `path/file.ts` - Pattern used

### Architecture Patterns
- Pattern 1: Description
- Pattern 2: Description

### Key Files
1. `path/file1.ts` - Why important
2. `path/file2.ts` - Why important
```

**Step 4: Update Progress**
- phase: 2
- phase_name: exploration
- Add phase 1 to completed_phases

### Exit Criteria
- Codebase patterns documented
- Key files identified and read
- Ready to design architecture

---

## Phase 3: Documentation & Tasks

### Purpose
Create specification documents and break down implementation tasks.

### Sub-phase 3a: Documentation

**Step 1: Write contracts.md**
Define all data contracts:
- Input types and validation
- Output structures
- API endpoints
- Error responses

**Step 2: Update README.md**
Add:
- Goal and scope
- All decisions from Phase 1
- Document navigation

**GATE: User approves spec documents**

### Sub-phase 3b: Task Breakdown

**Step 1: Launch Architect Agent**
Get implementation blueprint:
```markdown
"Design architecture for {feature} considering:
- Patterns found in Phase 2
- Decisions from Phase 1
- Project conventions"
```

**Step 2: Create Task List**
Write tasks.md with atomic tasks:
```markdown
## T1: Task Name

**Goal**: One sentence
**Size**: S (30min) / M (1-2h) / L (half day)
**Files**:
- [ ] `path/to/file.ts`

**Acceptance**:
- [ ] Criterion 1
- [ ] Criterion 2

**Status**: pending
```

**Step 3: Update Progress**
- phase: 3
- phase_name: documentation

### Task Sizing Guidelines

| Size | Duration | Complexity |
|------|----------|------------|
| S | 30 min | Single file, simple change |
| M | 1-2 hours | 2-3 files, moderate logic |
| L | Half day | Multiple files, complex logic |

**GATE: User confirms task list before implementation**

---

## Phase 4: Implementation

### Purpose
Build the feature incrementally with verification.

### Entry Criteria
- Phase 3 completed
- User approved task list
- **Explicit user approval to start**

### Process

**Step 1: Create Feature Branch**
```bash
git checkout -b feat/{feature-name}
```

**Step 2: Implement Tasks**
For each task:
1. Update tasks.md status to `in_progress`
2. Read related files
3. Implement changes
4. Run verification: `bun run check`
5. Update tasks.md status to `completed`
6. Update progress.md

**Step 3: Periodic Verification**
After every 2-3 tasks:
```bash
bun run check && bun run test
```

**Step 4: Update Progress Continuously**
Keep progress.md current with:
- Current task
- Any blockers
- Context for resumption

### Exit Criteria
- All tasks completed
- All verifications pass
- Code ready for review

---

## Phase 5: Review & PR

### Purpose
Ensure quality and submit for merge.

### Process

**Step 1: Launch Review Agents**
Launch 3 `reviewer` agents with different focuses:
- Simplicity/DRY/elegance
- Bugs/functional correctness
- Project conventions/patterns

**Step 2: Present Findings**
Consolidate issues by severity:
- Critical: Must fix
- High: Should fix
- Medium: Consider fixing

**Step 3: User Decision**
Ask user:
- Fix now?
- Fix later?
- Proceed as-is?

**Step 4: Final Verification**
```bash
bun run check && bun run test && bun run build
```

**Step 5: Create PR**
```bash
git push -u origin feat/{feature-name}
gh pr create --title "feat: {Feature}" --body-file .works/spec/{feature-name}/PR.md
```

**Step 6: Complete Workflow**
Update progress.md:
- status: completed
- Add PR URL

### Exit Criteria
- PR created
- progress.md marked complete
- Ready for merge
