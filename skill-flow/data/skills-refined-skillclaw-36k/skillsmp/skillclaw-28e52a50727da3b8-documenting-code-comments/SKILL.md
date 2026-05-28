---
name: documenting-code-comments
description: Use this skill when auditing, cleaning up, or improving inline code documentation to ensure clarity and maintainability.
---

# Code Comment Guidelines

## Core Philosophy

**The best comment is the one you didn't need to write.**

Self-documenting code reduces maintenance burden and prevents comment drift. Clear naming and structure can significantly reduce onboarding time.

### Writing Style Guidelines

**Tone:** Be direct, practical, and clear. Write in a natural and relaxed tone, avoiding corporate buzzwords and overly formal language.

**Avoid**:

- Corporate buzzwords and marketing speak
- AI-sounding language or excessive enthusiasm
- Overly formal or boring documentation style
- Dramatic hyperbole about revolutionary solutions
- Em dashes (—)
- Emojis
- Sycophancy

### Hierarchy of Documentation

1. **Make code self-documenting** (naming, structure, types)
2. **Use type systems** to document contracts
3. **Add comments only for WHY**, never for WHAT

## Refactoring: Preserve Existing Comments

This skill's guidance applies to writing new code. When refactoring existing code, preserve comments as they represent institutional knowledge.

### Never Remove

- Comments explaining WHY something exists
- Comments warning about gotchas or edge cases
- Comments referencing external context (tickets, specs, RFCs)
- Comments documenting non-obvious business logic

### Update When Necessary

- If refactoring changes behavior the comment describes, update the comment.
- If refactoring makes a workaround obsolete, update or remove it.
- Add to existing comments if refactoring introduces new context.

### Only Remove When

- The comment is demonstrably incorrect (doesn't match code behavior).
- The comment documents code you're deleting entirely.
- The refactoring eliminates the "why" (e.g., removing a workaround makes its explanation obsolete).