---
name: sdlc-plan
description: Create an implementation plan for a task
argument-hint: <workflow-id> [type] [output_dir] [explore_agents] <context>
---

# SDLC Plan

## Overview

Create a structured implementation plan for the given task. This skill analyzes the codebase, identifies relevant files and patterns, and produces a detailed plan with milestones and actionable tasks. Supports different plan types (feature, bug, chore) with type-specific guidance.

## Arguments

### Definitions

- **`<workflow-id>`** (required): The workflow identifier for output organization.
- **`[type]`** (optional): Plan type. Values: `feature`, `bug`, `chore`, `auto`. Defaults to `auto`.
- **`[output_dir]`** (optional): Directory to write plan.md file (default to `agentic/outputs/<workflow-id>`).
- **`[explore_agents]`** (optional): Number of explore agents for codebase analysis. Defaults to `0`.
- **`<context>`** (required): Task description or issue reference.

### Values

\$ARGUMENTS

## Additional Resources

Load ONE of these based on the `[type]` argument (or detected type if auto):

- For feature plans, see [references/feature.md](references/feature.md)
- For bug fix plans, see [references/bug.md](references/bug.md)
- For chore plans, see [references/chore.md](references/chore.md)

## Core Principles

### Plan Structure

- **Every plan must use Milestones and Tasks** - This applies to all plan types (feature, bug, chore). Having a single milestone is valid for smaller work items.
- Tasks should be specific enough to execute without ambiguity
- Include file paths with line numbers where changes are needed
- Consider testing requirements in each milestone
- Flag any unclear requirements or assumptions
- Plans are static documentation - never modified during implementation
- Always include a Progress section as the first `##` header with two subsections: Implementation (milestones/tasks) and Validation (verification and tests)

### Milestone Design

- Each milestone should deliver visible progress
- Milestones should be testable independently
- Order milestones by dependency (foundational work first)

### Milestone Scoping (Critical)

- **Each milestone must be scoped to a single Claude session** - If a milestone is too large for one session, split it into multiple milestones.
- **Milestones are executed in fresh sessions** - When building the plan, assume each milestone will be executed in a new session that only has access to the plan document. All necessary context must be included in the plan itself.
- **Every milestone must produce a concrete output** - Examples: generate code, update documentation, update plan, create tests. A milestone should never be purely research without output, because subsequent sessions cannot access that research.
- **Research milestones require documented outputs** - If research is needed, the milestone must output its findings (e.g., "Research X and update Milestone 2 checklist with findings"). However, this pattern is discouraged. Prefer milestones that produce direct project artifacts.
- **Ideal milestones are scoped units of work** - Each milestone should generate output in the current project that represents tangible progression toward the plan's goal.

### Milestone & Task Template

All plans must use this common structure for Progress and Milestones sections:

```markdown
## Progress

### Implementation

- [ ] Milestone 1: {{milestone_title}}
  - [ ] Task 1.1: {{task_title}}
  - [ ] Task 1.2: {{task_title}}
- [ ] Milestone 2: {{milestone_title}}
  - [ ] Task 2.1: {{task_title}}

### Validation

- [ ] {{validation_item}}

## Milestones

### Milestone {{milestone_number}}: {{milestone_title}}

{{milestone_description}}

#### Task {{milestone_number}}.{{task_number}}: {{task_title}}

{{task_description}}
```

<!--
Common placeholders (used by all plan types):
- {{milestone_number}}: Sequential number (1, 2, 3, ...)
- {{milestone_title}}: What this milestone accomplishes
- {{milestone_description}}: Brief description of the milestone
- {{task_number}}: Task number within milestone (1, 2, 3, ...)
- {{task_title}}: Clear, actionable task title
- {{task_description}}: Specific task details with acceptance criteria
- {{validation_item}}: Validation criterion or test item
-->

## Instructions

1. **Parse Arguments**
   - Extract workflow-id, type, output_dir, explore_agents, and context from arguments
   - Default type to `auto` if not specified
   - Default explore_agents to `0` if not specified

2. **Detect Plan Type** (if type=auto)
   - Analyze the context to determine type:
     - **feature**: New functionality, enhancements, additions
     - **bug**: Error fixes, unexpected behavior corrections, defects
     - **chore**: Refactoring, dependency updates, maintenance, cleanup
   - Once detected, proceed with that type

3. **Load Type-Specific Guidelines**
   Based on the detected or specified type, load the corresponding reference file:
   - `feature` -> Read [references/feature.md](references/feature.md)
   - `bug` -> Read [references/bug.md](references/bug.md)
   - `chore` -> Read [references/chore.md](references/chore.md)

4. **Analyze Codebase**
   - If `explore_agents` is 0: Perform a quick codebase exploration in the main session using Glob, Grep, and Read tools
   - If `explore_agents` is 1+: Launch that many explorer agents (Task tool with subagent_type=Explore) for in-depth parallel analysis
   - Identify files and components relevant to the task
   - Understand existing patterns and conventions
   - Map dependencies and impact areas

5. **Generate Plan**
   - Apply type-specific planning approach from the loaded reference
   - Create discrete, independent milestones
   - Include specific file paths and line numbers
   - Estimate complexity (low, medium, high)

6. **Write Output**
   - Write plan document as .md format to the output_dir.
   - Return JSON summary

## Output Guidance

Return JSON with metadata only. The full plan content is saved to the markdown file.

```json
{
  "success": true,
  "plan_type": "{{type}}",
  "summary": "{{summary}}",
  "milestone_count": "{{milestone_count}}",
  "task_count": "{{task_count}}",
  "complexity": "{{complexity}}",
  "document_path": "{{document_path}}"
}
```

<!--
Placeholders:
- {{type}}: Plan type (feature, bug, chore)
- {{summary}}: Brief one-line summary of the plan
- {{milestone_count}}: Total number of milestones
- {{task_count}}: Total number of tasks across all milestones
- {{complexity}}: Overall complexity (low, medium, high)
- {{document_path}}: Path to generated plan.md file
-->
