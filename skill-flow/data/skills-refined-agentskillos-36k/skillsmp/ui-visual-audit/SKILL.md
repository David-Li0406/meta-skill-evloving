---
name: ui-visual-audit
description: Advanced UI verification using Antigravity Manager's Vision MCP.
---

# UI Visual Audit Skill

This skill empowers the agent to verify UI implementation against design specs using visual feedback from the Antigravity Manager's built-in Vision MCP.

## Protocol

1. **Capture**: Use the `Vision MCP` to take a screenshot of the current UI (or a specific component).
2. **Analyze**: Compare the screenshot against:
   - Design tokens (colors, spacing, typography).
   - Component state (hover, active, focus).
   - Accessibility requirements (contrast, target sizes).
3. **Report**: Identify discrepancies and provide actionable fix implementation details.

## Patterns

- **Theme Check**: `Does the UI follow the Sleek Mid-Century / Bauhaus theme rules?`
- **Color Audit**: `Verify that the #FFB800 accent color is used consistently across buttons.`
- **UX Layout**: `Check the Bento grid alignment on mobile vs desktop screenshots.`

## Tooling Integration

- **Vision MCP**: For screenshots and visual understanding.
- **Frontend Design Skill**: For cross-referencing theme principles.
- **Arize Phoenix**: For logging visual audit traces.
