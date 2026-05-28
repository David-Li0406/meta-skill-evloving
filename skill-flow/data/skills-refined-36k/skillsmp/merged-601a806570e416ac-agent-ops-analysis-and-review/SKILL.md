---
name: agent-ops-analysis-and-review
description: Use this skill for comprehensive analysis and review of codebases, including linting, improvement discovery, and code reviews.
---

# Comprehensive Code Analysis and Review

This skill encompasses the validation, improvement discovery, and thorough review of codebases, focusing on enhancing quality, maintainability, and alignment with project goals.

## Instruction File Linter

### Purpose
Validate AgentOps markdown-based instruction files for formatting, structure, and consistency.

### Supported File Types
| Type     | Pattern         | Location                     |
|----------|-----------------|------------------------------|
| Skill    | `SKILL.md`      | `.github/skills/*/`         |
| Prompt   | `*.prompt.md`   | `.github/prompts/`          |
| Agent    | `AGENTS.md`     | Project root or subdirs     |
| Instructions | `copilot-instructions.md` | `.github/` |

### Trigger
```bash
/lint-instructions [path]/lint-skills/lint-prompts
```

### Validation Rules
#### Critical Errors (must fix)
- **ERR001**: No code fence wrapper
- **ERR002**: Valid YAML frontmatter
- **ERR003**: Required frontmatter fields
- **ERR004**: File encoding

#### Warnings (should fix)
- **WARN001**: Excessive blank lines
- **WARN002**: Trailing whitespace
- **WARN003**: Heading hierarchy
- **WARN004**: Inconsistent list markers
- **WARN005**: Missing newline at EOF
- **WARN006**: Table alignment

### Auto-Fix Support
```bash
/lint-instructions --fix [path]
```

## Improvement Discovery

### Core Objective
Analyze the current state of the codebase and propose specific enhancements that:
- Align with the project’s stated purpose
- Improve correctness, maintainability, or delivery confidence
- Reduce risk, ambiguity, or future cost

### Mandatory Analysis Axes
1. **Project Goal Alignment**: Assess alignment with project goals.
2. **Delivery State Assessment**: Evaluate completeness and fragility.
3. **Risk & Fragility Hotspots**: Identify areas likely to break.
4. **Maintainability & Change Cost**: Assess ease of modification.
5. **Baseline Consistency**: Identify regressions or gaps.
6. **Synergy, Composability & Sequencing**: Evaluate how improvements can work together.

### Enhancement Proposal Rules
Propose enhancements that:
- Close a verified delivery gap
- Reduce a documented risk
- Improve confidence via evidence
- Simplify without loss of behavior

### Output Format
```markdown
# Project Enhancement Analysis

## Project Understanding
Concise summary of the project’s current goals and state.

## Key Findings
Concrete observations tied to specific areas of the codebase.

## Risks & Gaps
Verified risks, missing pieces, or fragile areas.

## Proposed Enhancements
Each enhancement must include:
- Description
- Affected area(s)
- Problem it solves
- Why it matters now
- Expected outcome
- Priority: critical | high | medium | low

## Explicit Non-Recommendations
Improvements intentionally *not* suggested, with reasoning.

## Suggested Next Steps
A short, ordered list of what should be done next.
```

## Comprehensive Code Review

### Role
You are a **Senior Code Review Expert** tasked with producing critical, thorough, constructive, and evidence-based reviews.

### Operating Modes
```yaml
output_mode: report | issues | both
default: report
issue_prefix: CR  # Code Review
```

### Mandatory Review Axes
1. **Problem Fit & Requirement Fidelity**
2. **Abstractions & Over-Engineering**
3. **Conceptual Integrity**
4. **Cognitive Load & Local Reasoning**
5. **Changeability & Refactor Cost**
6. **Data Flow & State Management**
7. **Error Handling & Failure Semantics**
8. **Naming & Semantic Precision**
9. **Deletion Test**
10. **Test Strategy**
11. **Observability & Debuggability**
12. **Proportionality & Context Awareness**

### Output Requirements
When `output_mode: report`
```markdown
# Critical Code Review Report

## Scope
(files / diff / repo reviewed)

## Summary
High-level risks and themes (no solutions here).

## Findings
Grouped by review axis.
Each finding includes:
- Location (file:line)
- Severity
- Short rationale

## Recommendations
Concrete actions, grouped by priority.

## Non-Issues / Trade-offs
Intentional decisions worth keeping.

## Appendix
Notes, edge cases, reviewer assumptions.
```

### End Condition
The review should leave the codebase:
- Easier to understand
- Easier to change
- Cheaper to maintain
- No more complex than necessary

**Guiding constraint:**
> If complexity cannot clearly justify its existence today, it is a liability.