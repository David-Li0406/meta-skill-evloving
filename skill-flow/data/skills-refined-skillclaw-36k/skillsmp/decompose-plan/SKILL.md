---
name: decompose-plan
description: Decomposes a plan file into beads with epics, dependencies, and self-documenting context. Use when you have a comprehensive feature specification or implementation plan that needs to be broken into actionable, trackable tasks for multi-agent execution.
---

# Decompose Plan Skill

Transform implementation plans into structured, self-contained beads with proper epic groupings and dependencies.

## Your Role

**You are the decision-maker** for:
1. **Granularity** - How many beads? How big/small?
2. **Decomposition** - What work goes in each bead?
3. **Dependencies** - Which beads block which?
4. **Context Distribution** - What information each bead needs to be self-contained
5. **Epic Structure** - How to group related beads under epics

You are NOT just running `br create` commands—you're applying judgment to create a coherent, actionable task structure.

## Input Handling

**Expected input:** A file path to a plan document (e.g., `/path/to/plan.md`)

1. Validate the file exists using the Read tool
2. Parse the entire plan content
3. If file doesn't exist, report error and stop

## Analysis Phase

Before creating any beads, thoroughly analyze the plan:

### 1. Understand Business Context
- What problem does this solve?
- What are the project's overarching goals?
- Why does this matter?

### 2. Identify Natural Boundaries
Look for seams in the work:

| Boundary Type | Example |
|---------------|---------|
| Different files/modules | API routes vs middleware vs models |
| Different concerns | Auth logic vs token handling vs rate limiting |
| Sequential dependencies | Must have X before Y |
| Parallelizable work | Can do X and Y simultaneously |
| Phases/milestones | Phase 1: Setup, Phase 2: Core features |

### 3. Map Structure
- Identify phases → these become **epics**
- Identify tasks within phases → these become **beads**
- Note dependencies between tasks

## Decomposition Rules

### Granularity Guidelines

| Plan Complexity | Typical Beads | Epic Structure |
|-----------------|---------------|----------------|
| Tiny (1 file change) | 1 bead | No epic needed |
| Small (2-3 related files) | 2-3 beads | Maybe 1 epic |
| Medium (feature) | 4-8 beads | 1-2 epics |
| Large (system) | 8+ beads | Multiple epics, possibly nested |

### Signs a Bead is Too Big
- Touches 5+ unrelated files
- Has 10+ acceptance criteria
- Mixes multiple concerns (auth AND email AND database)
- Would take a full day+ to implement

### Signs a Bead is Too Small
- Single line change
- No meaningful acceptance criteria
- Could easily be combined with related work

## Self-Contained Bead Principle (CRITICAL)

**Every bead must be completely self-documenting.** A developer should be able to implement it without reading the original plan or other beads.

### Required in Every Bead Description

Use the template from `references/bead-template.md`:

1. **Task**: Clear, actionable statement
2. **Background & Reasoning**: Why this exists, how it serves project goals
3. **Key Files**: Every file to create/modify with purpose
4. **Implementation Details**: Patterns, snippets, APIs, integration points
5. **Acceptance Criteria**: Specific, testable, with verification commands
6. **Considerations & Edge Cases**: Gotchas, security, performance
7. **Notes for Future Self**: Anything else helpful

### Anti-Patterns to AVOID
- "See the main plan for details" → Include the details
- "Similar to task X" → Repeat the relevant information
- Assuming shared context → Each bead is standalone
- Vague criteria like "works correctly" → Specific testable criteria

### The "Future Self" Test
Ask: "Would someone reading ONLY this bead understand what to do, why to do it, and how to verify it's done?"

## Epic Creation

Phases and logical feature groupings become epics.

### Epic Dependency Direction (CRITICAL)

```bash
# CORRECT: Epic depends on children (children are READY to work)
br dep add <epic-id> <child-id>

# Result:
# - child: READY (no blockers)
# - epic: BLOCKED (waiting for children)
```

```bash
# WRONG: This blocks children forever!
br dep add <child-id> <epic-id>  # DO NOT DO THIS
```

### Creating Epics

```bash
# Create the epic first
br create --title="Phase 1: Authentication System" --type=epic --priority=1

# Create child beads
br create --title="Setup JWT middleware" --type=task --priority=1 --description="..."

# Link epic to children (epic depends on children)
br dep add <epic-id> <child-1-id>
br dep add <epic-id> <child-2-id>
```

## Existing Bead Detection (Autonomous)

Before creating beads, check for existing related work:

```bash
br list --status=open --json
br list --status=in_progress --json
```

**Automatically determine** (do NOT ask user):

| Situation | Action |
|-----------|--------|
| **Clear dependency**: Existing bead is prerequisite | Add as dependency with `br dep add` |
| **True duplicate**: Existing covers identical scope | Skip creation, include in dependency flow |
| **Related but distinct**: Similar topic, different scope | Create new bead, may share dependencies |

Document all decisions in the decomposition log.

## Priority Assignment

Assign priorities based on the **nature of the work**, not keywords:

| Priority | Task Type | Examples |
|----------|-----------|----------|
| P0 | **Foundation** | Setup, infrastructure, core abstractions, dependencies that block everything |
| P1 | **Core Features** | Primary functionality, main user-facing features, critical path work |
| P2 | **Core Features** | Secondary features, supporting functionality, important but not critical |
| P3 | **Polish** | Error handling improvements, UX refinements, documentation |
| P4 | **Polish** | Nice-to-haves, optimizations, stretch goals, future enhancements |

**Assignment logic:**
1. Tasks with no dependents AND many dependencies → likely P0 foundation
2. Tasks on the critical path to MVP → P1-P2 core features
3. Tasks that enhance but don't enable functionality → P3-P4 polish
4. When in doubt, default to P2

## Bead Creation Process

For each identified task:

### 1. Craft the Description
Use the self-contained template. Include ALL context needed.

### 2. Determine Type
- `task` - Standard implementation work
- `bug` - Fixing something broken
- `epic` - Parent grouping for related tasks

### 3. Set Priority
Based on task type: P0=foundation, P1-P2=core features, P3-P4=polish. Default to P2 if unclear.

### 4. Create the Bead
```bash
br create \
  --title="<concise title>" \
  --type=<task|bug|epic> \
  --priority=<0-4> \
  --description="<full self-contained description>"
```

### 5. Establish Dependencies
```bash
# Task B requires Task A
br dep add <task-B-id> <task-A-id>

# Epic depends on all its children
br dep add <epic-id> <child-id>
```

## Summary Output

After creating all beads, write a decomposition log to:
`.beads/decomposition-logs/<timestamp>-<plan-name>.md`

### Log Format

```markdown
# Decomposition: <plan-name>

**Source:** /path/to/original/plan.md
**Created:** 2026-01-19T12:34:56Z
**Total beads created:** 8
**Epics:** 2
**Tasks:** 6

## Decisions Made

### Duplicates/Dependencies Found
- Found existing `br-45: Setup database` - added as dependency to br-101
- Skipped "Add user model" - duplicate of existing br-50

### Priority Assignments
- br-101: P0 (foundation) - core setup that blocks other work
- br-102: P1 (core feature) - primary user-facing functionality
- br-106: P3 (polish) - pagination is enhancement, not critical path

## Epics Created

### br-100: Phase 1 - Authentication
Depends on: br-101, br-102, br-103
Status: BLOCKED (waiting for children)

### br-104: Phase 2 - API Endpoints
Depends on: br-105, br-106
Status: BLOCKED (waiting for children)

## All Beads

| ID | Title | Type | Priority | Blocked By | Status |
|----|-------|------|----------|------------|--------|
| br-101 | Setup JWT middleware | task | 1 | - | READY |
| br-102 | Add login endpoint | task | 2 | br-101 | blocked |
| br-103 | Add logout endpoint | task | 2 | br-101 | blocked |
| br-105 | Create user CRUD | task | 2 | br-100 | blocked |
| br-106 | Add pagination | task | 3 | br-105 | blocked |

## Dependency Graph

br-100 (epic: Phase 1 - Auth)
├── br-101 Setup JWT middleware (READY)
├── br-102 Add login endpoint → br-101
└── br-103 Add logout endpoint → br-101

br-104 (epic: Phase 2 - API)
├── br-105 Create user CRUD → br-100
└── br-106 Add pagination → br-105
```

## Guidelines

### DO
- Read and understand the ENTIRE plan before creating beads
- Make each bead completely self-contained
- Include specific, testable acceptance criteria
- Use correct epic dependency direction
- Check for existing related beads
- Document your decisions in the log
- Create the decomposition log file

### DON'T
- Create beads without full context
- Use vague acceptance criteria
- Block children on epics (reverse the dependency)
- Skip duplicate checking
- Forget to establish dependencies
- Leave out the "why" - always include reasoning
