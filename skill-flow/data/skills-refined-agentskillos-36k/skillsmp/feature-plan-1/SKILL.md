---
name: feature-plan
description: Document a feature plan. Use when user explicitly asks to create, document, or log a feature plan.
allowed-tools: Write, Read, Glob, Task
---

# Feature Plan Skill

Create feature documentation in `DevPlans/Features/` to capture discussed features for future implementation.

**Important**: Only create a feature plan when the user explicitly requests it.

## Investigation First

**Before writing the feature plan**, launch an Explore subagent using the Task tool to investigate the codebase thoroughly:

```
Task tool with subagent_type: "Explore"
model: "opus"
prompt: "Investigate the codebase to understand how to implement [feature description]. Find:
- Existing systems this feature would integrate with
- Similar patterns or features already implemented
- Data structures and classes that would be involved
- Entry points where the feature would hook in
- Any existing TODOs or comments related to this feature area
- Architectural patterns used in similar areas"
```

Use the investigation results to fill in the Design, Key Components, and Integration Points sections with concrete findings from the codebase rather than generic suggestions.

## File Naming

`{STATUS}-{FeatureName}.md`

| Status | Meaning |
|--------|---------|
| PLANNED | Feature documented, not yet started |
| IN_PROGRESS | Currently being implemented |
| DONE | Feature has been implemented |
| CANCELLED | Won't implement |

New features should always start with `PLANNED-`.

## Required Sections

```markdown
# Feature: {Title}

## Summary
Brief description of what this feature does and why it's needed.

## Goals
- What this feature should accomplish
- User-facing benefits
- Technical benefits

## Design

### Overview
High-level description of the approach.

### Key Components
- List main classes/systems involved
- New files to create
- Existing files to modify

### Data Structures
Describe any new structs, classes, or data formats needed.

### Behavior
How the feature works step-by-step.

## Integration Points
- How this connects to existing systems
- Dependencies on other features
- Systems that will depend on this

## Open Questions
- Unresolved design decisions
- Areas needing further discussion

## Priority
Low / Medium / High

## Related Files
- `path/to/related/file.cs`
```

## Example

For a belt conveyor feature:
- File: `DevPlans/Features/PLANNED-BeltSystem.md`
- Title: `# Feature: Belt Conveyor System`
- Include diagrams or ASCII art if helpful

## Status Changes

When implementation status changes, rename the file:
- `PLANNED-MyFeature.md` → `IN_PROGRESS-MyFeature.md`
- `IN_PROGRESS-MyFeature.md` → `DONE-MyFeature.md`
- `PLANNED-MyFeature.md` → `CANCELLED-MyFeature.md`
