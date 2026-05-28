---
name: writing-skills
description: Use this skill when creating new skills, editing existing skills, or validating skill effectiveness before deployment.
---

# Writing Skills

## Overview
This skill applies test-driven development (TDD) principles to the documentation process for skills.

## When to Use
- When the technology is not intuitively obvious to you.
- When you will reference this across different projects.
- When the pattern is broadly applicable (not project-specific).
- When others will benefit from the documentation.

**Do not use for:**
- One-off solutions.
- Well-documented standard practices elsewhere.
- Project-specific conventions (place in project-specific documentation).
- Mechanical constraints (automate with regex/validation instead).

## Core Principles
If you haven't observed the agent failing without the skill, you don't know if the skill teaches the correct behavior.

## Skill Creation Process
The entire skill creation process follows the Claim-Evidence-Refine cycle, adapted from TDD:

| TDD Concept | Skill Creation |
|-------------|----------------|
| **Test Case** | Pressure scenarios with sub-agents |
| **Production Code** | Skill documentation (SKILL.md) |
| **Test Failure (Red)** | Agent violating rules without the skill (baseline) |
| **Test Pass (Green)** | Agent complying with the skill in place |
| **Refactor** | Closing loopholes while maintaining compliance |
| **Write Tests First** | Run baseline scenarios before writing skills |
| **Watch it Fail** | Document the exact rationalizations used by the agent |
| **Minimal Code** | Write skills addressing specific violations |
| **Watch it Pass** | Validate that the agent now complies |
| **Refactor Cycle** | Identify new rationalizations → close loopholes → re-validate |

## Skill Types
### Technique
Specific step-by-step methods (e.g., condition-based waiting, root-cause tracing).

### Pattern
Ways of thinking about problems (e.g., flattening with flags, testing invariants).

### Reference
API documentation, syntax guides, tool documentation.

## Directory Structure
```
skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only when necessary
```

**Flat Namespace** - All skills are in a searchable namespace.

**Separate files for:**
1. **Heavy References** (100+ lines) - API documentation, comprehensive syntax.
2. **Reusable Tools** - Scripts, utilities, templates.

**Keep Inline:**
- Principles and concepts.
- Code patterns (< 50 lines).
- Everything else.

## SKILL.md Structure
**Frontmatter (YAML):**
- Only supports two fields: `name` and `description`.
- `name`: Use only letters, numbers, and hyphens.
- `description`: Third person, only describes when to use (not what it does).
  - Starts with "Use when..." focusing on triggering conditions.
  - Includes specific symptoms, situations, and context.
  - **Never summarize the skill's process or workflow.**
  - Keep under 500 characters if possible.

```markdown
---
name: Skill-Name-With-Hyphens
description: Use when [specific triggering conditions and symptoms].
---

# Skill Name

## Overview
What is it? Summarize core principles in 1-2 sentences.

## When to Use
- Bullet points with symptoms and use cases.
- When **not** to use.

## Core Patterns (for Techniques/Patterns)
Before/after code comparisons.

## Quick Reference
Table or bullet points for common operations.

## Implementation
Inline code for simple patterns.
Link to heavy reference or reusable tools.

## Common Mistakes
What can go wrong + fixes.

## Real-World Impact (optional)
Specific outcomes.
``` 

## Search Optimization
Future agents need to **find** your skills.

### 1. Rich Description Field
**Purpose:** Agents read the description to decide which skills to load for a given task. It should answer: "Should I read this skill now?"

**Format:** Starts with "Use when..." focusing on triggering conditions.

**Key:** Description = when to use, not what the skill does.

### 2. Keyword Coverage
Use terms agents might search for:
- Error messages.
- Symptoms: "incoherence," "logical leaps," "missing citations."
- Synonyms.
- Tools: actual commands, library names.

### 3. Descriptive Naming
**Use active voice, prioritize verbs:**
- ✅ `creating-skills` instead of `skill-creation`.
- ✅ `writing` instead of `w`.