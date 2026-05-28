# Guardrail: Plan Completeness Check

## When to Run

Run this check **before issuing any sprint/project plan**.

## Required Sections

A plan is INCOMPLETE without ALL of these:

### 1. Sprint/Project Metadata
- [ ] Name/identifier
- [ ] Goal statement
- [ ] Date/timeline

### 2. Scope Definition
- [ ] In-scope items with rationale
- [ ] Out-of-scope / deferred items
- [ ] Non-goals (if applicable)

### 3. Backlog
- [ ] Prioritized list with IDs
- [ ] Rationale for prioritization
- [ ] Dependencies identified
- [ ] Conflicts identified

### 4. Phase Plan
- [ ] Clear phase boundaries
- [ ] Parallel vs sequential tasks
- [ ] Integration checkpoints per phase
- [ ] CI gates per phase

### 5. Merge Plan
- [ ] Branch strategy
- [ ] Feature branch naming
- [ ] Integration branches (if needed)
- [ ] Explicit merge order

### 6. Dependency Graph
- [ ] Mermaid visualization (human-readable)
- [ ] YAML edges (machine-readable)
- [ ] All dependencies explicit
- [ ] Conflicts addressed

### 7. Task Files
- [ ] One per backlog item
- [ ] All sections complete
- [ ] Testing expectations included

### 8. Testing & Quality Plan
- [ ] Unit test requirements
- [ ] Coverage expectations
- [ ] Integration test requirements
- [ ] CI gates
- [ ] Regression protection (if applicable)

### 9. Risk Register
- [ ] Identified risks
- [ ] Likelihood/impact assessment
- [ ] Mitigations

### 10. Decision Log
- [ ] Template in place
- [ ] Initial decisions documented

## Failure Handling

If any section is missing:

1. **DO NOT** issue the plan
2. **COMPLETE** the missing sections
3. **RE-RUN** this check

## Quick Validation

```
Plan: <name>

Required sections:
- [ ] Metadata
- [ ] Scope
- [ ] Backlog
- [ ] Phase plan
- [ ] Merge plan
- [ ] Dependency graph
- [ ] Task files
- [ ] Testing plan
- [ ] Risk register
- [ ] Decision log

Status: COMPLETE / INCOMPLETE
Missing: <list>
```
