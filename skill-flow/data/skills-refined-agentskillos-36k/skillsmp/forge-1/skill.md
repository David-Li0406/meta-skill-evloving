---
name: forge
description: |
  FORGE development framework for Intent-Driven Development (IDD).
  Use for: forge, FORGE, new cycle, start cycle, advance phase, next phase,
  checkpoint, validate phase, focus, orchestrate, refine, generate, evaluate,
  cycle status, complete cycle, add learning, retrospective, TDD workflow.
allowed-tools: Read, Write, Edit, Bash(uv:*), Bash(python:*), Glob, Grep
---

# FORGE Development Framework

FORGE (Focus-Orchestrate-Refine-Generate-Evaluate) is an Intent-Driven Development (IDD) methodology for AI-assisted software development.

## Interactive Workflow: Clarity Before Action

During **Focus, Orchestrate, and Refine** phases, you must gain clarity before proceeding:

1. **Assess clarity** - Are the requirements/inputs clear or vague?
2. **If vague** → Ask targeted clarifying questions (use `prompts/prd-conversation.md` as a guide)
3. **Always** → Summarize your understanding and confirm with the user before advancing

### Phase Confirmation Pattern

| Phase | Summarize & Confirm |
|-------|---------------------|
| **Focus** | "Problem: X. Users: Y. Success: Z. Boundaries: [in/out of scope]. Correct?" |
| **Orchestrate** | "Architecture: N containers/components. Dependencies: [map]. Task breakdown: [list]. Correct?" |
| **Refine** | "Acceptance criteria: [Given-When-Then]. Edge cases: [categories]. Interfaces: [specs]. Correct?" |

Only advance after user confirms. Generate and Evaluate phases may proceed without additional confirmation once Refine is validated.

## Native Tool Integration (Claude Code)

When running in Claude Code, leverage native tools for enhanced workflow:

| Phase | Native Tool | Purpose |
|-------|-------------|---------|
| **Focus** | `AskUserQuestion` | Gather requirements, clarify scope, confirm problem statement |
| **Orchestrate** | `AskUserQuestion` | Validate architecture decisions, confirm task breakdown |
| **Refine** | `AskUserQuestion` | Confirm acceptance criteria, validate edge cases |
| **Generate** | `TodoWrite` | Track implementation tasks (RED-GREEN-REFACTOR steps) |
| **Evaluate** | `AskUserQuestion` | Confirm verification results, get disposition decision |

**Adaptive behavior:**
- If `AskUserQuestion` is available, use it for structured clarification with options
- If `TodoWrite` is available, use it to track Generate phase tasks
- Fall back to conversational clarification in non-Claude-Code environments

**Example - Using AskUserQuestion in Focus:**
```
When clarifying requirements, present structured options:
- "What is your target user base?" with options like "Internal team", "External customers", "API consumers"
- This provides better UX than open-ended questions
```

**Example - Using TodoWrite in Generate:**
```
Track TDD workflow:
1. [in_progress] Write failing test for feature X
2. [pending] Implement minimal code to pass
3. [pending] Refactor while tests stay green
```

### Resolving Clarity Issues (Any Phase)

If clarity issues arise at any phase, you may:
- Ask targeted clarifying questions
- Invoke specialist agents for guidance
- Recommend returning to an earlier phase

## Tool Commands

When the user wants to work with FORGE, run the appropriate command:

| User Request | Command |
|-------------|---------|
| Initialize FORGE | `uv run .claude/skills/forge/tools/forge_init.py` |
| Start new cycle | `uv run .claude/skills/forge/tools/forge_cycle.py new "name"` |
| Check status | `uv run .claude/skills/forge/tools/forge_status.py` |
| Validate phase | `uv run .claude/skills/forge/tools/forge_status.py --validate` |
| Advance phase | `uv run .claude/skills/forge/tools/forge_phase.py advance` |
| Complete task | `uv run .claude/skills/forge/tools/forge_phase.py complete-task "desc"` |
| Add task | `uv run .claude/skills/forge/tools/forge_phase.py add-task "desc"` |
| Complete cycle | `uv run .claude/skills/forge/tools/forge_cycle.py complete <id>` |
| Add learning | `uv run .claude/skills/forge/tools/forge_learn.py add <cat> "title" "desc"` |
| Retrospective | `uv run .claude/skills/forge/tools/forge_learn.py retro` |

Learning categories: `pattern`, `anti-pattern`, `decision`, `tool`

## Core Concepts

### Intent-Driven Development Triad

- **Intent** - Why the work exists; the problem being solved
- **Outcomes** - Observable, defensible changes in reality
- **Accountability** - Single owner responsible for consequences

### The Five Phases

| Phase | Purpose | Key Question |
|-------|---------|--------------|
| **FOCUS** | Clarity | What are you actually building? |
| **ORCHESTRATE** | Planning | How do you break this into pieces? |
| **REFINE** | Precision | What specifically does "done" look like? |
| **GENERATE** | Creation | AI writes code following TDD |
| **EVALUATE** | Verification | Does output match intent? |

## Phase Details

### 1. FOCUS - Clarity

**Required Outputs**:
- Problem statement and target users defined
- Testable success criteria (not vague aspirations)
- System Context diagram (C4 Level 1)
- Clear boundaries on what you WON'T build

### 2. ORCHESTRATE - Planning

**Required Outputs**:
- Container architecture (C4 Level 2)
- Component architecture (C4 Level 3)
- Dependency map
- Tasks sized for single AI sessions

### 3. REFINE - Precision

**CRITICAL**: No code in this phase - specifications only.

**Required Outputs**:
- Acceptance criteria in Given-When-Then format
- Interface specifications (inputs, outputs, errors)
- Edge cases by category (empty/null, boundary, invalid, timing, failure, concurrent)
- Constraints vs criteria documented

### 4. GENERATE - Creation

**Process**: RED → GREEN → REFACTOR
1. Write failing test first
2. Minimal code to pass
3. Improve while tests stay green

**Rules**:
- One task per session
- Tests BEFORE implementation
- 80% minimum coverage

### 5. EVALUATE - Verification

**Process**:
- Line-by-line check against acceptance criteria
- Test edge cases (specified AND discovered)
- Security review
- Integration testing

**Dispositions**: Accept | Accept with issues | Revise | Reject

## Document Creation

During each phase, create and maintain documents in `docs/`. Documents are organized per cycle/feature:

```
docs/
├── prd/
│   └── <cycle-name>.md         # Focus: Problem statement, users, success criteria, scope
├── tasks/
│   └── <cycle-name>.md         # Orchestrate: Session-sized task breakdown
└── <cycle-name>/
    ├── system-context.md       # Focus: C4 Level 1 - system boundaries
    ├── containers.md           # Orchestrate: C4 Level 2 - deployable units
    ├── components.md           # Orchestrate: C4 Level 3 - internal structure
    ├── acceptance-criteria.md  # Refine: Given-When-Then scenarios
    ├── interfaces.md           # Refine: inputs, outputs, error contracts
    └── edge-cases.md           # Refine: categorized edge cases
```

**Phase → Document mapping:**
| Phase | Create/Update |
|-------|---------------|
| Focus | `prd/<cycle>.md`, `<cycle>/system-context.md` |
| Orchestrate | `tasks/<cycle>.md`, `<cycle>/containers.md`, `<cycle>/components.md` |
| Refine | `<cycle>/acceptance-criteria.md`, `<cycle>/interfaces.md`, `<cycle>/edge-cases.md` |

Create documents as you complete phase work. These are the source of truth for Generate and Evaluate phases.

## State Management

All cycle state lives in `.forge/`:
```
.forge/
├── config.yaml
├── context.md
├── learnings.md
└── cycles/
    ├── active/
    └── completed/
```

## Phase Blocking

- Cannot write code during Focus, Orchestrate, or Refine
- Cannot advance without completing mandatory items
- Evaluation may send you back to earlier phases

### Hook-Based Enforcement (Claude Code)

For automated phase constraint enforcement, configure hooks in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "command": [".claude/hooks/forge-phase-guard.sh"]
      }
    ]
  }
}
```

The hook script:
- Reads current phase from `.forge/cycles/active/`
- **Allows** all writes to `docs/` (specs, PRDs, architecture docs)
- **Blocks** code writes during Focus, Orchestrate, Refine phases
- **Allows** code writes during Generate and Evaluate phases

Install the hook:
```bash
mkdir -p .claude/hooks
cp path/to/forge-skill/.claude/hooks/forge-phase-guard.sh .claude/hooks/
chmod +x .claude/hooks/forge-phase-guard.sh
```

## Key Principle

**Clarity before code** - Time in Focus, Orchestrate, and Refine prevents waste in Generate and Evaluate.
