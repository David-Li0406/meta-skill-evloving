---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation. Auto-invokes planning-pipeline after design. Includes agent mapping for intelligent subagent orchestration during execution."
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue, then automatically transition to implementation planning with **intelligent subagent orchestration**.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

**Key features:**
- Auto-invokes planning-pipeline after design completion
- Defines task-to-agent mappings for smart execution
- Subagent-driven-development uses mappings to dispatch appropriate specialists

## The Process

**Understanding the idea:**
- Check out the current project state first (files, docs, recent commits)
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**
- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design (Automatic Pipeline)

**Step 1: Documentation with Agent Mapping**

Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`.

**CRITICAL: Include Agent Mapping Section** at the end of the design:

```markdown
## Agent Mapping for Execution

When using subagent-driven-development, dispatch these specialized agents:

| Task Pattern | Subagent Type | Model | Notes |
|--------------|---------------|-------|-------|
| Database/migration tasks | backend-architect | sonnet | Schema, RLS, triggers |
| API endpoint tasks | backend-architect | sonnet | Routes, validation, auth |
| React component tasks | frontend-developer | sonnet | Components, hooks, state |
| TypeScript type tasks | typescript-pro | haiku | Types, interfaces, schemas |
| Test writing tasks | general-purpose | sonnet | Unit, integration tests |
| Performance tasks | performance-engineer | sonnet | Profiling, optimization |
| UI/UX design tasks | ui-ux-designer | sonnet | Design system, accessibility |
| Code review tasks | superpowers:code-reviewer | sonnet | Quality gates |

### Task-Specific Agents for This Feature

[List specific task → agent mappings based on the design]

Example:
- Task 1 (Create qc_rules table) → backend-architect
- Task 2 (Add QC API endpoints) → backend-architect  
- Task 3 (Build QCRulesTable component) → frontend-developer
- Task 4 (Add Zod schemas) → typescript-pro
- Task 5 (Write integration tests) → general-purpose
```

Use elements-of-style:writing-clearly-and-concisely skill if available.
Commit the design document to git.

**Step 2: Auto-invoke Planning Pipeline**

Once the design document is committed, **automatically invoke planning-pipeline**:

```
Skill tool -> skill: planning-pipeline
```

Announce: "Design complete. Now invoking planning-pipeline to create the implementation plan."

The planning-pipeline will:
1. Assess scope (OpenSpec vs Quick-plan path)
2. Create plan artifacts (using writing-plans if Quick-plan path)
3. **Preserve agent mappings from design in the plan**
4. Get user approval
5. Ingest tasks into Beads with dependencies
6. Offer execution method choice

**Do NOT ask "Ready to set up for implementation?" - proceed automatically.**

## Subagent Orchestration During Execution

When planning-pipeline hands off to **subagent-driven-development**, the execution follows this enhanced flow:

```
For each task in plan:
  1. Read task description
  2. Match task to agent type (from agent mapping table)
  3. Dispatch appropriate specialist subagent:
     
     Task tool -> subagent_type: [matched-agent-type], model: [sonnet|haiku]
     Prompt: "[task description with full context]"
  
  4. Two-stage review:
     - Spec compliance review (superpowers:code-reviewer)
     - Code quality review (superpowers:code-reviewer)
  
  5. Mark task complete, move to next
```

### Agent Selection Logic

```
Pattern Matching (in priority order):

1. Exact match in task-specific mapping table
   → Use specified agent

2. Pattern match on task keywords:
   - "database", "table", "migration", "RLS" → backend-architect
   - "API", "endpoint", "route", "server action" → backend-architect
   - "component", "React", "UI", "hook" → frontend-developer
   - "type", "interface", "schema", "Zod" → typescript-pro
   - "test", "spec", "e2e" → general-purpose
   - "performance", "optimize", "cache" → performance-engineer
   - "design", "UX", "accessibility" → ui-ux-designer

3. Default fallback
   → general-purpose (sonnet)
```

### Model Selection

```
Task Complexity → Model:

- Simple tasks (types, small fixes) → haiku (fast, cheap)
- Standard tasks (components, endpoints) → sonnet (quality)
- Complex tasks (architecture, security) → sonnet (thoroughness)
- Review tasks → sonnet (always)
```

### Parallel Execution

When tasks are independent (no dependency chain):

```
Dispatch multiple subagents in single message:

Task tool (parallel) → [
  { subagent_type: frontend-developer, task: "Build ComponentA" },
  { subagent_type: frontend-developer, task: "Build ComponentB" },
  { subagent_type: typescript-pro, task: "Add types for ComponentA" }
]
```

**Rules for parallelization:**
- No shared file modifications
- No dependency between tasks
- Same or compatible domains
- Max 3 parallel subagents (context management)

## Workflow Diagram

```
Complete Flow with Agent Orchestration:

  Understand Idea
       |
       v
  Explore Approaches (2-3 options)
       |
       v
  Present Design (sections)
       |
       v
  Write design.md with Agent Mapping Table
       |
       v
  git commit
       |
       v
  [AUTO] Invoke planning-pipeline
       |
       v
  Create plan.md (preserves agent mappings)
       |
       v
  User approves plan
       |
       v
  Beads ingestion (tasks with agent hints)
       |
       v
  User selects execution method
       |
       v
  [If Subagent-Driven]
       |
       v
  For each task:
    ┌─────────────────────────────────────┐
    │ 1. Match task → agent type          │
    │ 2. Dispatch specialist subagent     │
    │ 3. Subagent implements + tests      │
    │ 4. Spec compliance review           │
    │ 5. Code quality review              │
    │ 6. Mark complete, next task         │
    └─────────────────────────────────────┘
       |
       v
  All tasks complete
       |
       v
  Final review + finish branch
```

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
- **Seamless handoff** - Auto-invoke pipeline without asking
- **Smart agent selection** - Match tasks to specialist subagents
- **Parallel when safe** - Run independent tasks concurrently
- **Two-stage review** - Spec compliance + code quality gates

## Skip Planning Option

If user explicitly says they only want the design (not implementation), skip the auto-invoke:
- "Just the design, no implementation plan"
- "Design only"
- "Skip planning"

In these cases, end after committing the design document.

## Example: Agent Mapping in Practice

```markdown
## Agent Mapping for Execution

| Task | Agent Type | Model | Rationale |
|------|------------|-------|-----------|
| Create qc_rules table | backend-architect | sonnet | DB schema + RLS |
| Create qc_results table | backend-architect | sonnet | DB schema + RLS |
| Add QC validation RPC | backend-architect | sonnet | Complex SQL logic |
| Build QCRulesForm | frontend-developer | sonnet | React + form handling |
| Build QCResultsChart | frontend-developer | sonnet | React + Recharts |
| Add QC Zod schemas | typescript-pro | haiku | Type definitions |
| Write QC unit tests | general-purpose | sonnet | Test coverage |
| Write QC e2e tests | general-purpose | sonnet | Integration testing |

### Parallelization Groups

- Group 1 (parallel): qc_rules table, qc_results table
- Group 2 (sequential, depends on Group 1): QC validation RPC
- Group 3 (parallel): QCRulesForm, QCResultsChart, QC Zod schemas
- Group 4 (sequential, depends on all): Unit tests, e2e tests
```

## Integration Points

| Skill | Relationship |
|-------|--------------|
| **planning-pipeline** | Receives design with agent mappings |
| **writing-plans** | Creates tasks with agent hints |
| **subagent-driven-development** | Uses mappings to dispatch specialists |
| **superpowers:code-reviewer** | Two-stage review after each task |
| **superpowers:finishing-a-development-branch** | Final integration |