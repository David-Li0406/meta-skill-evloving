---
name: plan
description: This skill should be used when the user requests help building a complex multi-phase project plan, resuming an existing plan from CURRENT_PLAN.md, or executing projects that require research, planning, building, validation, and cleanup phases. Use when users say "create a plan", "help me plan", show a CURRENT_PLAN.md file, or need structured project execution with memory optimization between phases.
---

# Plan Skill

**If you are a Plan subagent**: Invoke this skill immediately using the Skill tool.

## Quick Reference

**Use for**: Multi-phase projects with research/planning/building/validation phases
**Don't use for**: Single-step tasks, quick fixes, minor changes

### Core Commands

```bash
# Initialize
python3 <skill_path>/scripts/orchestrator.py --dir . init "PROJECT_GOAL" [--phases research planning building]

# Status check
python3 <skill_path>/scripts/orchestrator.py --dir . status

# Update phase
python3 <skill_path>/scripts/orchestrator.py --dir . update <phase> completed --outputs "file1.md" "file2.md"

# Generate phase template
python3 <skill_path>/scripts/phase_templates.py <phase_name> .plans/<phase_name>/plan.md

# Cleanup
python3 <skill_path>/scripts/orchestrator.py --dir . cleanup
```

## Workflow

### Starting New Plan

1. **Clarify goal** - Ask questions if unclear
2. **Initialize** - Run `init` command with project goal
3. **Generate templates** - Create phase plan templates as needed
4. **Execute phases** - Follow phase template → create outputs → update status
5. **Iterate** - Repeat until all phases complete

### Resuming Existing Plan

1. **Check status** - Run `status` command
2. **Load minimal context**:
   - Read `CURRENT_PLAN.md`
   - Read `.plans/<current_phase>/plan.md`
   - Read previous phase's `phase_summary.md` ONLY
   - Load knowledge base files on-demand
3. **Continue execution** - Pick up where previous instance stopped

## Memory Management Rules

**CRITICAL - Always follow these rules to prevent high CPU usage:**

### Context Loading Protocol
- ✅ DO: Load previous phase's `phase_summary.md` (<500 words)
- ✅ DO: Load knowledge base files only when specifically needed
- ✅ DO: Use `.plans/knowledge-base/` for cross-phase references
- ❌ DON'T: Load full previous phase context
- ❌ DON'T: Read all phase directories
- ❌ DON'T: Load outputs from non-adjacent phases

### Phase Output Requirements
Every phase MUST create:
1. Phase-specific outputs (findings, plans, logs, etc.)
2. `phase_summary.md` - Concise summary under 500 words
3. Knowledge base files for cross-phase references (if needed)

### Summary Cascade Pattern
```
Research → phase_summary.md → Planning → phase_summary.md → Building → ...
```
Each phase sees only the previous summary, not full context.

## Phase Quick Reference

| Phase | Purpose | Key Inputs | Key Outputs |
|-------|---------|------------|-------------|
| **research** | Gather information | User requirements | `research_findings.md`, KB files, `phase_summary.md` |
| **planning** | Design solution | Research summary | `plan.md`, `architecture.md`, `phase_summary.md` |
| **revision** | Review & refine | Planning outputs | `review_notes.md`, `phase_summary.md` |
| **building** | Implement | Plan summary | Code, `implementation_log.md`, `phase_summary.md` |
| **validation** | Verify implementation | Building summary | `validation_results.md`, `phase_summary.md` |
| **cleanup** | Finalize | All summaries | `final_summary.md` |

## Iteration Pattern

If phase reveals issues:
1. Document reason in `phase_summary.md`
2. Update `CURRENT_PLAN.md` with iteration note
3. Return to appropriate phase
4. Create `iteration_01_plan.md`
5. Resume forward progress

**Limit**: Max 2-3 iterations per phase

## Best Practices

**DO:**
- Create concise summaries (<500 words)
- Store shared references in `knowledge-base/`
- Load summaries first, details only if needed
- Update `CURRENT_PLAN.md` after each phase

**DON'T:**
- Load full previous phase context
- Skip `phase_summary.md` creation
- Mix phase concerns
- Read unnecessary files

## Structure Created

```
.
├── CURRENT_PLAN.md           # Central progress tracking
└── .plans/
    ├── knowledge-base/       # Cross-phase references
    ├── research/
    │   ├── plan.md
    │   ├── research_findings.md
    │   └── phase_summary.md
    ├── planning/
    │   ├── plan.md
    │   └── phase_summary.md
    └── [other phases...]
```

## Detailed Documentation

For comprehensive phase workflows, see `references/phase_workflows.md`.
Load this file ONLY when you need detailed guidance for a specific phase.
