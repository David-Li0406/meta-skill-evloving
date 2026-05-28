---
name: design-and-implementation-plan-reviewer
description: Use this skill when reviewing design documents and implementation plans to ensure clarity and prevent integration failures before execution.
---

# Skill body

## Purpose
This skill is designed to help you thoroughly review design documents and implementation plans, ensuring that all specifications are clear and that there are no gaps that could lead to integration failures.

## When to Use
- When reviewing design documents, technical specifications, or architecture docs before implementation planning.
- When reviewing implementation plans derived from design documents before execution.

## Critical Instructions
1. **Compare Plans**: Always compare the implementation plan to the parent design document (if available) to ensure alignment.
2. **Verify Interfaces**: Check that every interface between parallel work streams is explicitly specified to avoid assumptions.
3. **Identify Gaps**: Look for points where executing agents would have to guess or invent details that are not specified.
4. **Cite Sources**: Ensure that any references to existing code behaviors cite the source directly, rather than inferring from method names.

## Invariant Principles
1. **Specification Sufficiency**: Ensure that all designs and plans are sufficiently detailed to prevent implementers from having to guess.
2. **Explicit Contracts**: Every handoff point between work streams must specify exact data shapes, protocols, and error formats.
3. **Comprehensive Documentation**: Document completeness means every item is either specified or explicitly marked as N/A with justification.

## Review Process
### Phase 1: Context and Inventory
- Assess whether a parent design document exists.
- Identify parallel vs. sequential work items.
- Determine what setup or skeleton work must be completed first.
- Map out existing interfaces between parallel tracks.

### Phase 2: Completeness Checklist
Mark each category as **SPECIFIED**, **VAGUE**, **MISSING**, or **N/A** (with justification):
- **Architecture**: System diagrams, component boundaries, data flow, etc.
- **Data**: Models with field specifications, schema, validation rules, etc.
- **API/Protocol**: Method, path, request/response schema, error codes, etc.

### Outputs
- **Findings Report**: An inline report scoring each section with SPECIFIED/VAGUE/MISSING verdicts.
- **Remediation Plan**: A prioritized list of fixes with acceptance criteria.
- **Factcheck Escalations**: Claims requiring verification before implementation.

## Reflection
After reviewing, ask yourself:
- Could I code against this RIGHT NOW?
- What would I have to invent or guess?
- Verdict: SPECIFIED | VAGUE | MISSING