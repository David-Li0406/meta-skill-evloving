---
name: cairo-component-dependencies
description: Explain component dependency patterns, trait bounds, and dependency access helpers; use when a request involves components that rely on other components in Cairo.
---

# Cairo Component Dependencies

## Overview
Explain how components depend on other components without embedding them directly.

## Quick Use
- Read `references/component-dependencies.md` before answering.
- Use trait bounds on impl blocks to require dependent components.
- Use the helper macros to access dependencies from a component state.

## Response Checklist
- Declare dependencies with trait bounds on the host contract type.
- Use `get_dep_component!` or `get_dep_component_mut!` to access the dependency.
- Ensure the host contract embeds all required components.

## Example Requests
- "How can my component call another component?"
- "Why do I need trait bounds for components?"
- "How do I access a dependency from ComponentState?"
