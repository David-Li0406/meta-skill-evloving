---
name: coding-style
description: Guidelines for writing clean, professional code. Use when writing or modifying code, creating commits, or generating code comments. Ensures code is written for team consumption without conversation artifacts.
---

# Coding Style Guidelines

## Context-Free Communication

Never reference our conversation in code, commits, or comments. Avoid phrases like:
- "Option A/B"
- "as discussed"
- "per your request"
- "as mentioned earlier"

Write for developers who will read the code without access to this chat.

## Comments

Avoid tutorial-style or learning-oriented comments such as:
- `// someFunctionName is no longer needed here`
- `// We removed this because...`
- Explanatory comments directed at the developer making the change

Only add comments that explain non-obvious "why" decisions that future maintainers need to understand.

## Write for the Team

Commits, comments, and code will be read by other developers. Explain the "why" in a way that stands alone. The code and its history should be self-documenting without requiring conversation context.

## Newspaper Article Code Organization

Structure code with important elements at the top, details below—like a newspaper article where the headline comes first.

**Ordering principles:**
1. Public members before private members
2. Public functions before private functions
3. High-level logic before implementation details
4. When extracting a helper function from a larger function, place the helper **after** the original function

This allows readers to understand the public API and main flow before diving into implementation details.
