---
name: prp-workflow
description: Use this skill when implementing features systematically with a comprehensive Product Requirements Prompt (PRP) that includes context, implementation blueprints, and validation gates for one-pass success.
---

# PRP (Product Requirement Prompt) Workflow

## Overview

The PRP workflow is designed for systematic feature implementation, providing a structured approach to generate, clarify, and execute PRPs. A PRP is a PRD engineered for AI, including complete context, implementation blueprints, and validation gates.

## Workflow Phases

1. **Generation**: Create a comprehensive PRP from a feature request.
2. **Clarification**: Resolve ambiguities in the PRP before execution.
3. **Execution**: Implement the feature using the validated PRP.

---

## Mode 1: PRP Generation

### Process

1. **Launch 2 parallel agents** for research:
   - **Agent #1 - Codebase Research**: Identify similar features and conventions in the codebase.
   - **Agent #2 - External Research**: Gather documentation, implementation examples, and best practices.

2. **Read key files** identified by agents to build understanding.

3. **Clarify with user** if needed.

4. **Generate PRP** using a predefined template.

5. **Save** the PRP to `plans/{XXX}-{feature-name}.md`.

6. **Report** confidence score and ask whether to clarify or execute.

---

## Mode 2: PRP Clarification

### Process

1. **Locate PRP**: Ask the user or search for existing PRPs.

2. **Launch an agent** to analyze the PRP for ambiguities against a coverage taxonomy.

3. **Present clarification questions** to the user.

4. **Integrate answers** into the PRP, updating relevant sections.

5. **Report** coverage summary and recommend the next step.

### Early Exit
- If no critical gaps are found, proceed to execution.
- If the PRP is missing, generate it first.

---

## Mode 3: PRP Execution

### Process

1. **Load PRP**: Read the entire document and note success criteria.

2. **Launch an agent** to execute the implementation:
   - Create a task list from the PRP.
   - Work through tasks one at a time, following PRP patterns.
   - Run validation commands after each major step.
   - Fix failures immediately.

3. **Handle blockers**: Resolve any issues that arise during execution.

4. **Report** completion summary.

### Validation Philosophy

If validation fails:
1. Read the error carefully.
2. Understand the root cause.
3. Fix the underlying issue and re-run validation.

---

## PRP Structure

### PRD Structure (for large features)

```markdown
# {Feature Name}

## Problem Statement
{Who has what problem, cost of not solving}

## Evidence
{Proof the problem exists}

## Proposed Solution
{What we're building and why}

## Key Hypothesis
We believe {capability} will {solve problem} for {users}.
We'll know we're right when {measurable outcome}.

## Implementation Phases
| # | Phase | Description | Status | Parallel | Depends |
|---|-------|-------------|--------|----------|---------|
| 1 | ... | ... | pending | - | - |
```

### Plan Structure (for implementation)

```markdown
# Feature: {Name}

## Summary
{What we're building}

## User Story
As a {user}, I want to {action}, so that {benefit}

## Patterns to Mirror
{Actual code snippets from codebase with file:line}

## Files to Change
| File | Action | Justification |
|------|--------|---------------|
| ... | CREATE/UPDATE | ... |

## Step-by-Step Tasks
### Task 1: {Description}
- ACTION: {what to do}
- MIRROR: {file:line to copy}
- VALIDATE: {command to run}

## Validation Commands
{Executable commands for each level}

## Acceptance Criteria
{Checkboxes for completion}
```

---

## Best Practices

### DO
- Start with codebase exploration before planning.
- Include actual code snippets, not generic examples.
- Define validation commands for every task.
- Mark out-of-scope items explicitly.
- Update PRD status after each phase.

### DON'T
- Create plans without understanding existing patterns.
- Skip validation steps.
- Ignore the structured format.
- Hardcode values that should be config.

---

## Quick Reference

### File Locations
- PRPs: `plans/{XXX}-{feature-name}.md`
- Template: [references/prp-template.md](references/prp-template.md)
- Taxonomy: [references/clarification-taxonomy.md](references/clarification-taxonomy.md)

### Agent Summary
| Phase | Agents | Model |
|-------|--------|-------|
| Generation | 2 parallel (codebase + external research) | Opus |
| Clarification | 1 (coverage analysis) | Opus |
| Execution | 1 (implementation) | Opus |

### Key Constraints
- Clarification: max 5 questions, 4 per AskUserQuestion batch.
- Execution: one task in progress at a time.
- Validate after each major step.

### Anti-Patterns
- Skipping research to save time.
- Implementing without reading the full PRP.
- Ignoring validation failures.
- Creating new patterns instead of following existing ones.

---

## Success Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| First-Pass Success | > 80% | Plans implemented without replanning. |
| Validation Pass Rate | > 95% | Implementations passing all checks. |
| Context Completeness | 100% | All patterns documented with file:line. |
| Test Coverage | > 80% | New code covered by tests. |