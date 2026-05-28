---
name: learner
description: Use this skill when you want to extract a learned skill from a conversation that involves solving complex problems or debugging specific issues.
---

# Skill body

## The Insight

Reusable skills are not code snippets to copy-paste, but **principles and decision-making heuristics** that teach how to think about a class of problems.

**The difference:**
- BAD (mimicking): "When you see ConnectionResetError, add this try/except block."
- GOOD (reusable skill): "In async network code, any I/O operation can fail independently due to client/server lifecycle mismatches. The principle: wrap each I/O operation separately, because failure between operations is the common case, not the exception."

A good skill changes how you approach problems, not just what code it produces.

## Why This Matters

Before extracting a skill, ask yourself:
- "Could someone Google this in 5 minutes?" → If yes, STOP. Don't extract.
- "Is this specific to THIS codebase?" → If no, STOP. Don't extract.
- "Did this take real debugging effort to discover?" → If no, STOP. Don't extract.

If a potential skill fails any of these questions, it's not worth saving.

## Recognition Pattern

Use `/oh-my-claudecode:learner` ONLY after:
- Solving a tricky bug that required deep investigation.
- Discovering a non-obvious workaround specific to this codebase.
- Finding a hidden gotcha that wastes time when forgotten.
- Uncovering undocumented behavior that affects this project.

## The Approach

### Extraction Process

**Step 1: Gather Required Information**

- **Problem Statement**: The SPECIFIC error, symptom, or confusion that occurred.
  - Include actual error messages, file paths, line numbers.
  - Example: "TypeError in src/hooks/session.ts:45 when sessionId is undefined after restart."

- **Solution**: The EXACT fix, not general advice.
  - Include code snippets, file paths, configuration changes.
  - Example: "Add null check before accessing session.user, regenerate session on 401."

- **Triggers**: Keywords that would appear when hitting this problem again.
  - Use error message fragments, file names, symptom descriptions.
  - Example: ["sessionId undefined", "session.ts TypeError", "401 session"].

- **Scope**: Almost always Project-level unless it's a truly universal insight.

**Step 2: Quality Validation**

The system REJECTS skills that are:
- Too generic (no file paths, line numbers, or specific error messages).
- Easily Googleable (standard patterns, library usage).
- Vague solutions (no code snippets or precise instructions).
- Poor triggers (generic terms).