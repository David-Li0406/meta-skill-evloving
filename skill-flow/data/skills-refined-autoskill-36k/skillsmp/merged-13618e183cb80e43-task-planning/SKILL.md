---
name: task-planning
description: Use this skill when you want to break down a PRD into implementable tasks.
---

# Task Planning Skill

This skill is activated when the user wants to break down a PRD into implementable tasks.

## When to Use

- After the PRD is ready
- To plan a sprint
- To estimate effort
- To define the order of implementation

## Template

Use the template in `templates/task-template.md` as a base.

## Process

1. **Analyze PRD**
   - Identify all functional requirements
   - Map dependencies between requirements
   - Identify technical components

2. **Decompose into Tasks**
   - A task = an atomic deliverable
   - Each task must be testable
   - Each task must have clear criteria

3. **Order Tasks**
   - Technical dependencies first
   - Setup before implementation
   - Testing alongside implementation (TDD)

4. **Document**
   - Files to create/modify
   - Acceptance criteria
   - Necessary tests

## Principles

- **Atomicity**: A task does one thing only
- **Testability**: Can validate that it is ready
- **Independence**: Can be done in one session
- **Clarity**: No ambiguity in what to do

## Outputs

- `.claude/plans/features/<name>/tasks.md`