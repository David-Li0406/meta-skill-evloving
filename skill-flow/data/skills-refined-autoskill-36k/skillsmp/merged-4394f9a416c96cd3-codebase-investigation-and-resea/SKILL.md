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
- Finding existing patterns to follow in new code (e.g., how errors are handled)
- Locating features or code (e.g., where user authentication is implemented)
- Understanding component architecture (e.g., how routing works)
- Confirming the existence of features definitively (e.g., does feature X exist?)
- Preventing hallucination about file paths and structure

**Don't use for:**
- Information available in external documentation (use internet research)
- Questions answered by reading 1-2 specific known files (use Read directly)
- General programming questions not specific to this codebase

## Core Investigation Workflow

1. **State the Investigation Goal**
   - Clearly define the question or assumption being investigated.
   - Explain the context and what is expected to be found.

2. **Fingerprint the Project**
   - Identify project type by checking key files (e.g., `package.json` for Node.js, `pyproject.toml` for Python).

3. **Map the Structure**
   - Scan the directory layout to understand the architecture (e.g., `src/` for source code, `tests/` for test files).

4. **Find Entry Points**
   - Locate where execution begins to clarify how components connect.

5. **Investigate Based on Goal**
   - For assumption verification, search for supporting and contradicting evidence.
   - For pattern searches, find examples and document canonical patterns.
   - For feature planning, identify conventions and document the rationale.

6. **Synthesize Findings**
   - Report findings in a structured format, including evidence and confidence levels.

## Output Format

Findings should be both human-readable and agent-consumable:

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

- **Grep for Patterns**: Find all instances of something across the codebase.
- **Trace from Entry Point**: Follow execution flow from CLI command or API endpoint.
- **Compare Similar Files**: Identify patterns and variations by comparing similar files.
- **Check Test Fixtures**: Review test setup files for expected data shapes.

## Validation Checklist

Before finalizing findings:
- [ ] Investigation goal was stated before starting.
- [ ] Both supporting and contradicting evidence was sought.
- [ ] All file references include paths and line numbers.
- [ ] Confidence level is explicitly stated.
- [ ] Findings are actionable.

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| "Explore the codebase" | Produces surveys, not answers | State a specific question or assumption |
| File paths without line numbers | Agents can't navigate to specifics | Always include `file:line` references |
| Only seeking confirming evidence | Confirmation bias; miss counter-examples | Explicitly search for contradictions |
| Yes/no verdicts | Doesn't convey certainty | Use confidence scale |
| Reading every file | Slow, context-inefficient | Pattern match from exemplars |
| Skipping fingerprint files | Miss obvious project type signals | Check key files first |

## Summary

1. **State your question before investigating.** Aimless exploration produces surveys, not answers.
2. **Seek contradicting evidence.** Confirmation bias produces false confidence.
3. **Include file:line references.** Agents and humans need precise locations.
4. **Report confidence levels.** Strongly confirmed vs. weakly confirmed changes decisions.