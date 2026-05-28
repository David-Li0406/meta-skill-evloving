---
name: codebase-investigation-and-research
description: Use this skill when planning or designing features to understand the current codebase state, find existing patterns, or verify assumptions, preventing hallucination by grounding decisions in reality.
---

# Codebase Investigation and Research

## Overview

This skill provides a systematic approach to investigating a codebase to verify assumptions and understand its structure. It helps prevent incorrect assumptions about file paths, existing patterns, and code functionality, ensuring that design and planning decisions are based on actual code.

## When to Use

**Use for:**
- Verifying design assumptions before implementation (e.g., confirming the existence of specific files or functions)
- Understanding current architecture and patterns before designing a feature
- Locating features or code (e.g., "Where is user authentication implemented?")
- Investigating how specific functionalities are implemented (e.g., "How does the routing system work?")
- Confirming the existence of features or code components definitively

**Don't use for:**
- Information available in external documentation
- Questions that can be answered by reading a few specific known files
- General programming questions not specific to the codebase

## Core Investigation Workflow

1. **State the Investigation Goal**: Clearly define the question or assumption being investigated, the context, and the expected findings.
2. **Fingerprint the Project**: Identify the project type by checking key files (e.g., `package.json` for Node.js, `pyproject.toml` for Python).
3. **Map the Structure**: Understand the directory layout to identify the purpose of different folders (e.g., `src/` for source code, `tests/` for test files).
4. **Find Entry Points**: Locate where execution begins to clarify how components connect.
5. **Investigate Based on Goal**:
   - For assumption verification: Search for evidence that supports or contradicts the assumption.
   - For pattern searches: Identify clear examples and document variations.
   - For feature planning: Locate similar features and identify conventions.
6. **Synthesize Findings**: Report findings in a structured format, including evidence and confidence levels.

## Reporting Findings

### Output Format

```markdown
## Investigation: [Question/Assumption]

### Context
[Why this investigation was needed]

### Approach
[What was searched and how]

### Findings

#### Evidence For
- [Finding with file:line reference]

#### Evidence Against
- [Finding with file:line reference] (or "None found")

### Verdict

**[Confidence level]**: strongly confirmed | weakly confirmed | inconclusive | weakly contradicted | strongly contradicted

[One-paragraph explanation]

### Implications
[What this means for the work that prompted investigation]
```

## Investigation Strategies

- **Grep for Patterns**: Find all instances of a specific term or pattern across the codebase.
- **Trace from Entry Point**: Follow execution flow from the starting point through the code layers.
- **Compare Similar Files**: Identify patterns by comparing files that perform similar functions.
- **Check Test Fixtures**: Review test setup files to understand expected data shapes and structures.

## Validation Checklist

Before finalizing findings, ensure:
- The investigation goal was clearly stated.
- Both supporting and contradicting evidence were sought.
- All file references include paths and line numbers.
- Confidence levels are explicitly stated.
- Findings are actionable.

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| "Explore the codebase" | Produces surveys, not answers | State a specific question or assumption |
| File paths without line numbers | Agents can't navigate to specifics | Always include `file:line` references |
| Only seeking confirming evidence | Confirmation bias; miss counter-examples | Explicitly search for contradictions |
| Yes/no verdicts | Doesn't convey certainty | Use a confidence scale |
| Reading every file | Slow, context-inefficient | Pattern match from exemplars |
| Skipping fingerprint files | Miss obvious project type signals | Check key files first |

## Summary

1. **State your question before investigating.** Aimless exploration produces surveys, not answers.
2. **Seek contradicting evidence.** Confirmation bias produces false confidence.
3. **Include file:line references.** Agents and humans need precise locations.
4. **Report confidence levels.** Strongly confirmed vs. weakly confirmed changes decisions.