---
name: speckit2beads
description: Convert Spec Kit task list markdown files to bd (Beads) issues with proper hierarchy
---

# Spec Kit to Beads Converter

This skill converts Spec Kit-generated task list markdown files into bd (Beads) issue hierarchies.

## Conversion Rules

1. **Document → Epic**: The entire tasks document becomes a single bd epic (from the `# Tasks:` title)
2. **Phase headers** (pattern: `## Phase N: Title`) → bd features
   - Each phase becomes a feature under the epic
   - Phase "Purpose" text → feature description
   - Phase "Checkpoint" text → feature acceptance_criteria
3. **Task items** (pattern: `- [ ] T\d{3}`) → bd tasks under their phase's feature
   - Task ID (e.g., T001) preserved in title or description
   - `[P]` marker indicates parallel capability (add to design notes)
   - `[US#]` marker indicates user story association (add label or description)
4. **Contract references** → Added to feature acceptance_criteria
5. **Dependencies section** → Used to set up bd blocking dependencies between features

## Field Distribution Logic

Bullet points should be intelligently distributed based on their content:

- **Description**: General explanatory content, "what" statements, background information
- **Design**: Technical implementation details, architecture notes, file locations, technical "how" statements
- **Acceptance Criteria**: Testing requirements, validation rules, property tests, requirements references

## Workflow

When invoked with a path to a spec-kit tasks.md file:

1. **Parse** the tasks markdown file
2. **Extract** the epic title from `# Tasks: <Title>` heading
3. **Identify phases** by scanning for `## Phase N:` headers
4. **For each phase**:
   - Extract phase title and number
   - Extract "Purpose" text for description
   - Extract "Checkpoint" text for acceptance_criteria
   - Extract "Contract" reference if present
   - Collect all `- [ ] T###` task items
5. **Parse task markers**:
   - `[P]` → parallel capability
   - `[US#]` → user story association
   - File paths in description → design field
6. **Extract dependencies** from "Dependencies" section if present
7. **Generate JSONL** preview showing all issues to be created
8. **Display** the JSONL to the user for review
9. **Wait** for user approval
10. **Create** issues using bd create commands if approved

## Issue Structure

### Epic (from document)
- `title`: From `# Tasks: <Title>` heading
- `description`: From document header content (Input, Prerequisites, etc.)
- `issue_type`: epic
- `priority`: 1

### Feature (from phase)
- `title`: Phase title (e.g., "Setup (Shared Infrastructure)")
- `description`: Phase "Purpose" text
- `design`: Path conventions, implementation notes
- `acceptance_criteria`: Phase "Checkpoint" text + Contract reference
- `issue_type`: feature
- `priority`: Derived from user story priority (P1=1, P2=2, P3=3) or default 2

### Task (from task item)
- `title`: Task description (e.g., "Create plugin directory structure per plan.md")
- `description`: Full task text including file paths
- `design`: File paths extracted from task (e.g., "plugins/bkff-git/")
- `issue_type`: task
- `priority`: Inherit from parent feature
- `labels`: `[P]` → "parallel", `[US#]` → "user-story-#"

## Example JSONL Output

### Epic (from document title)

Input:
```markdown
# Tasks: Git Lifecycle Plugin

**Input**: Design documents from `/specs/001-git-lifecycle-plugin/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
```

Output:
```jsonl
{"type":"epic","title":"Git Lifecycle Plugin","description":"Input: Design documents from /specs/001-git-lifecycle-plugin/. Prerequisites: plan.md, spec.md, research.md, data-model.md, contracts/"}
```

### Feature (from phase header)

Input:
```markdown
## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Plugin initialization and directory structure

- [ ] T001 Create plugin directory structure per plan.md at plugins/bkff-git/
- [ ] T002 [P] Create plugin.json with metadata in plugins/bkff-git/.claude-plugin/plugin.json
```

Output:
```jsonl
{"type":"feature","title":"Phase 1: Setup (Shared Infrastructure)","description":"Plugin initialization and directory structure","parent":"epic-id"}
```

### Feature with checkpoint and contract (User Story phase)

Input:
```markdown
## Phase 3: User Story 1 - Check Development Status (Priority: P1) 🎯 MVP

**Goal**: Developer can check current worktree status including uncommitted changes, last commit, beads tasks, and PR status

**Independent Test**: Run `/bkff:git-st` in a git worktree and verify output shows correct status information

**Contract**: specs/001-git-lifecycle-plugin/contracts/git-st.md

- [ ] T017 [US1] Create skill.md documentation for git-st command
...

**Checkpoint**: User Story 1 complete - `/bkff:git-st` should be fully functional and testable independently
```

Output:
```jsonl
{"type":"feature","title":"User Story 1 - Check Development Status","description":"Developer can check current worktree status including uncommitted changes, last commit, beads tasks, and PR status","acceptance_criteria":"Checkpoint: /bkff:git-st should be fully functional and testable independently. Contract: specs/001-git-lifecycle-plugin/contracts/git-st.md","priority":1,"parent":"epic-id"}
```

### Task (from task item)

Input:
```markdown
- [ ] T017 [US1] Create skill.md documentation for git-st command in plugins/bkff-git/skills/git-st/skill.md
```

Output:
```jsonl
{"type":"task","title":"T017: Create skill.md documentation for git-st command","design":"plugins/bkff-git/skills/git-st/skill.md","labels":["user-story-1"],"parent":"feature-us1-id"}
```

### Parallel task

Input:
```markdown
- [ ] T002 [P] Create plugin.json with metadata in plugins/bkff-git/.claude-plugin/plugin.json
```

Output:
```jsonl
{"type":"task","title":"T002: Create plugin.json with metadata","design":"plugins/bkff-git/.claude-plugin/plugin.json","labels":["parallel"],"parent":"feature-phase1-id"}
```

## Usage

```
/speckit2beads path/to/tasks.md
```

Or simply invoke the skill and provide the path when prompted.

Example with the Git Lifecycle Plugin spec:
```
/speckit2beads specs/001-git-lifecycle-plugin/tasks.md
```

## Implementation Notes

- Use the Read tool to load the tasks.md file
- Parse markdown systematically (line by line)
- Use regex patterns to identify elements:
  - **Document title**: `^# Tasks:\s*(.+)$` (captures epic title)
  - **Phase header**: `^## Phase (\d+):\s*(.+)$` (captures phase number and title)
  - **Task item**: `^- \[ \] (T\d{3})\s*(.+)$` (captures task ID and description)
  - **Parallel marker**: `\[P\]` in task description
  - **User story marker**: `\[US(\d+)\]` in task description (captures story number)
  - **Purpose text**: `^\*\*Purpose\*\*:\s*(.+)$`
  - **Goal text**: `^\*\*Goal\*\*:\s*(.+)$`
  - **Checkpoint text**: `^\*\*Checkpoint\*\*:\s*(.+)$`
  - **Contract reference**: `^\*\*Contract\*\*:\s*(.+)$`
  - **File path**: `\b(plugins/[^\s]+|specs/[^\s]+)` in task description
- **Phase parsing logic**:
  - When a `## Phase N:` header is found, start a new feature
  - Collect all `- [ ] T###` items until the next `## Phase` or `---` separator
  - Extract Purpose/Goal for description, Checkpoint for acceptance_criteria
- **Priority mapping**:
  - `(Priority: P1)` → priority 1
  - `(Priority: P2)` → priority 2
  - `(Priority: P3)` → priority 3
  - No priority marker → default 2
- Generate unique IDs using bd's prefix pattern
- Present JSONL for review before creating issues
- Use bd create commands with proper escaping for special characters

## Creating Issues and Dependencies

### Step 1: Create all issues first

Create issues in any order:
1. Create epic
2. Create all features
3. Create all tasks

Capture the issue IDs from the output for use in step 2.

### Step 2: Add blocking dependencies

**Use `blocks` type** to enforce completion order:

```bash
bd dep add <blocked-issue> <blocker-issue>
```

**Rule**: The thing that must complete FIRST blocks the thing that depends on it.

**For hierarchies:**
- Tasks block Features (tasks must close before feature can close)
- Features block Epic (features must close before epic can close)

**Examples:**
```bash
# Tasks block their feature
bd dep add bkfflz-feature bkfflz-task1    # task1 blocks feature
bd dep add bkfflz-feature bkfflz-task2    # task2 blocks feature

# Features block their epic
bd dep add bkfflz-epic bkfflz-feature1    # feature1 blocks epic
bd dep add bkfflz-epic bkfflz-feature2    # feature2 blocks epic

# Batch multiple dependencies
bd dep add bkfflz-feature bkfflz-task1 && \
bd dep add bkfflz-feature bkfflz-task2 && \
bd dep add bkfflz-feature bkfflz-task3
```

**Verification:**
```bash
bd show <issue-id>    # See what blocks this issue
bd blocked            # List all blocked issues
bd ready              # Show only unblocked work
```

**Result**: Epic cannot close until all features close, features cannot close until all tasks close.

### Step 3: Add cross-phase dependencies

Parse the "Dependencies & Execution Order" section to set up phase-level blocking:

```bash
# Example from tasks.md: Foundational (Phase 2) blocks all User Story phases (3-7)
bd dep add bkfflz-phase3 bkfflz-phase2    # Phase 2 blocks Phase 3
bd dep add bkfflz-phase4 bkfflz-phase2    # Phase 2 blocks Phase 4
bd dep add bkfflz-phase5 bkfflz-phase2    # Phase 2 blocks Phase 5
...

# Polish phase (8) depends on all user story phases
bd dep add bkfflz-phase8 bkfflz-phase3
bd dep add bkfflz-phase8 bkfflz-phase4
...
```

**Optional - Add parent-child for structure:**
If you want hierarchical metadata (doesn't enforce closure order):
```bash
bd dep add bkfflz-task bkfflz-feature --type parent-child
bd dep add bkfflz-feature bkfflz-epic --type parent-child
```
