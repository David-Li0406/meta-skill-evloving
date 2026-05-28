---
name: writing-skills
description: Use this skill when you need to apply Test-Driven Development principles to create and document reusable skills for AI agents.
---

# Writing Skills

## Overview

**Writing skills is Test-Driven Development (TDD) applied to process documentation.** This approach ensures that skills are thoroughly tested and refined before deployment.

**Skills are stored in `.gemini/skills/` (project-local) or `~/.gemini/skills/` (user-global).** You edit skills directly in the project's codebase.

You write test cases (pressure scenarios with subagents), observe them fail (baseline behavior), create the skill (documentation), verify tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't observe an agent fail without the skill, you can't be sure the skill teaches the right concept.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools that help future Agent instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides  
**Skills are NOT:** Narratives about how you solved a problem once

## When to Create a Skill

**Create when:**

- A technique wasn't intuitively obvious to you.
- You would reference this again across projects.
- A pattern applies broadly (not project-specific).
- Others would benefit.

**Don't create for:**

- One-off solutions.
- Standard practices well-documented elsewhere.
- Project-specific conventions (put in `GEMINI.md`).

## When to Use This Skill

**Situations:**

- When you discover a technique, pattern, or tool worth documenting for reuse.
- When editing existing skills.
- When asked to modify skill documentation.
- When you've written a skill and need to verify it works before deploying.

## TDD Mapping for Skills

| TDD Concept             | Skill Creation                                   |
| ----------------------- | ------------------------------------------------ |
| **Test case**           | Pressure scenario with subagent                  |
| **Production code**     | Skill document (SKILL.md)                        |
| **Test fails (RED)**    | Agent violates rule without skill (baseline)     |
| **Test passes (GREEN)** | Agent complies with skill present                |
| **Refactor**            | Close loopholes while maintaining compliance     |

The entire skill creation process follows the RED-GREEN-REFACTOR cycle.

## Skill Types

### Technique

Concrete method with steps to follow (e.g., condition-based waiting, root-cause tracing).

### Pattern

Way of thinking about problems (e.g., flatten-with-flags, test invariants).

### Reference

API docs, syntax guides, tool documentation.

## Directory Structure

**All skills are stored in `.gemini/skills/`:**

```
.gemini/skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed
```

**Flat namespace** - all skills in one searchable location.

## SKILL.md Structure

```markdown
---
name: Human-Readable Name
description: One-line summary of what this does (ASO-critical)
version: 1.0.0
---

# Skill Name

## Overview

What is this? Core principle in 1-2 sentences.

## When to Use

Bullet list with SYMPTOMS and use cases.  
When NOT to use.

## Core Pattern (for techniques/patterns)

Before/after code comparison.

## Quick Reference

Table or bullets for scanning common operations.

## Implementation

Inline code for simple patterns.  
Link to file for heavy reference or reusable tools.

## Common Mistakes

What goes wrong + fixes.

## Real-World Impact (optional)

Concrete results.
```

## Agent Search Optimization (ASO)

**Critical for discovery:** Future Agents need to FIND your skill.

### 1. Rich Description

Include SYMPTOMS and key keywords in the `description` field, as this is the primary discovery mechanism.

### 2. Keyword Coverage

Use words an Agent would search for, including error messages, symptoms, synonyms, and tools.

### 3. Descriptive Naming

**Use active voice, verb-first:**  
- ✅ `creating-skills` not `skill-creation`.

### 4. Token Efficiency

**Problem:** Skills are loaded into the Agent's context. Every token counts.

**Target word counts:**  
- Getting-started workflows: <150 words each.  
- Other skills: <500 words (be concise).

### 5. Content Repetition

Mention key concepts in the description, overview, and section headers to increase searchability.

### 6. Cross-Referencing Other Skills

Use path format relative to the skills root.

## Flowchart Usage

Use flowcharts ONLY for non-obvious decision points or process loops.

## Code Examples

**One excellent example beats many mediocre ones.** Ensure examples are complete, runnable, and well-commented.

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills.

## Testing All Skill Types

### Discipline-Enforcing Skills

**Test with:** Pressure scenarios (time + sunk cost + exhaustion).

### Technique Skills

**Test with:** Application scenarios.

### Pattern Skills

**Test with:** Recognition scenarios.

### Reference Skills

**Test with:** Retrieval scenarios.

## Common Rationalizations for Skipping Testing

| Excuse                     | Reality                                        |
| -------------------------- | ---------------------------------------------- |
| "Skill is obviously clear" | Clear to you ≠ clear to other agents. Test it. |
| "Testing is overkill"      | Untested skills have issues. Always.           |
| "I'm confident it's good"  | Overconfidence guarantees issues. Test anyway. |

## Bulletproofing Skills Against Rationalization

### Close Every Loophole Explicitly

Forbid specific workarounds.

### Build Rationalization Table

Capture excuses from baseline testing and provide counters.

### Create Red Flags List

```markdown
## Red Flags - STOP and Start Over

- Code before test
- "I already manually tested it"
- "It's about spirit not ritual"
```

## RED-GREEN-REFACTOR for Skills

### RED: Write Failing Test (Baseline)

Run scenario with subagent WITHOUT the skill. Document baseline behavior and rationalizations verbatim.

### GREEN: Write Minimal Skill

Write skill addressing those specific failures. Verify Agent now complies.

### REFACTOR: Close Loopholes

Add explicit counters for any new rationalizations found during testing.

## STOP: Before Moving to Next Skill

**After writing ANY skill, you MUST STOP and complete the verification process.**

## Skill Creation Checklist

- [ ] Create pressure scenarios
- [ ] Run scenarios WITHOUT skill - document baseline behavior
- [ ] Name describes what you DO
- [ ] Frontmatter with rich description
- [ ] Address baseline failures
- [ ] One excellent example
- [ ] Run scenarios WITH skill - verify compliance
- [ ] Identify NEW rationalizations and add explicit counters
- [ ] Re-test until bulletproof

## Discovery Workflow

1. **Encounter problem** ("tests are flaky").
2. **Automatic Discovery** (Agent scans `.gemini/skills/` descriptions).
3. **Finds SKILL.md** (rich description matches).
4. **Scans overview** (is this relevant?).
5. **Reads patterns** (quick reference table).

## The Bottom Line

**Creating skills IS TDD for process documentation.**  
Same Iron Law: No skill without failing test first.  
Same cycle: RED (baseline) → GREEN (write skill) → REFACTOR (close loopholes).  
Same benefits: Better quality, fewer surprises, bulletproof results.