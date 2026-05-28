---
name: performing-codebase-research
description: Use when planning or designing features and need to understand current codebase state, find existing patterns, or verify assumptions. Prevents hallucination by grounding decisions in reality.
---

# Performing Codebase Research

## Overview

Codebase research is systematic investigation to verify assumptions before acting on them. LLMs hallucinate file paths, assume patterns exist that don't, and propose changes that conflict with existing code. This skill provides a methodology for grounding design and planning decisions in what actually exists.

## When to Use

- Before designing a feature, to understand current architecture
- When a plan makes assumptions about file locations or structure
- When proposing code that should follow existing patterns
- When verifying that a design assumption holds across the codebase
- When you need to answer "where does X happen?" or "how is Y done?"

## Core Pattern

### Step 1: State the Investigation Goal

Before touching the codebase, state:
1. **The question or assumption** you're investigating
2. **Why you need to know** (context)
3. **What you expect to find** (hypothesis)

This prevents aimless exploration and creates a baseline to compare findings against.

### Step 2: Fingerprint the Project

Check fingerprint files to identify project type:

| File | Reveals |
|------|---------|
| `pyproject.toml`, `setup.py` | Python project, dependencies |
| `package.json` | Node.js project, dependencies |
| `Cargo.toml` | Rust project, dependencies |
| `go.mod` | Go project, dependencies |
| `pom.xml`, `build.gradle` | Java project, build system |

### Step 3: Map the Structure

Scan directory layout to understand architecture:

| Directory | Likely Purpose |
|-----------|----------------|
| `src/`, `lib/` | Source code |
| `api/` | API layer |
| `models/`, `entities/` | Data models |
| `services/` | Business logic |
| `storage/`, `db/` | Persistence |
| `cli/`, `cmd/` | CLI interface |
| `tests/` | Test files |

### Step 4: Find Entry Points

Locate where execution begins. Entry points clarify how pieces connect.

### Step 5: Investigate Based on Goal

**For assumption verification**:
1. State the assumption explicitly
2. Search for evidence that SUPPORTS it
3. Search for evidence that CONTRADICTS it
4. Weigh evidence and render verdict with confidence level

**For pattern search**:
1. Find one clear example
2. Search for similar patterns across codebase
3. Note variations and exceptions
4. Document the canonical pattern with `file:line` references

**For feature planning**:
1. Find where similar features live
2. Identify conventions (naming, structure, registration)
3. Document the "landing zone" with rationale

### Step 6: Synthesize Findings

Report using the output format below.

## Output Format

Findings must be both human-readable and agent-consumable.

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

### Grep for Patterns
Find all instances of something across the codebase.

### Trace from Entry Point
Follow execution flow from CLI command or API endpoint through layers.

### Compare Similar Files
Find two files doing similar things; note what's identical (the pattern) vs what differs (variation points).

### Check Test Fixtures
Find `conftest.py` or test setup files; fixtures show expected data shapes.

## Validation Checklist

Before finalizing findings:
- [ ] Investigation goal was stated before starting
- [ ] Both supporting AND contradicting evidence was sought
- [ ] All file references include paths AND line numbers
- [ ] Confidence level is explicitly stated
- [ ] Findings are actionable

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| "Explore the codebase" | Produces surveys, not answers | State a specific question or assumption |
| File paths without line numbers | Agents can't navigate to specifics | Always include `file:line` references |
| Only seeking confirming evidence | Confirmation bias; miss counter-examples | Explicitly search for contradictions |
| Yes/no verdicts | Doesn't convey certainty | Use confidence scale |
| Reading every file | Slow, context-inefficient | Pattern match from exemplars |
| Skipping fingerprint files | Miss obvious project type signals | Check `pyproject.toml`/`package.json` first |

## Anti-Rationalizations

- "I already know this codebase" — If you haven't investigated this session, you're guessing. Verify.
- "The user said X, so it must be true" — Users make mistakes. Confirm assumptions.
- "I'll just propose a location" — Proposing without verifying causes wasted work. Investigate first.
- "There's probably a pattern for this" — "Probably" isn't evidence. Find it or note its absence.

## Summary

1. **State your question before investigating.** Aimless exploration produces surveys, not answers.
2. **Seek contradicting evidence.** Confirmation bias produces false confidence.
3. **Include file:line references.** Agents and humans need precise locations.
4. **Report confidence levels.** Strongly confirmed vs. weakly confirmed changes decisions.
