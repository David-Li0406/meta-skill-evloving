---
name: tui-design-inspector
description: Professional TUI/terminal UI design inspection skill. Use this skill when the user asks to review, inspect, critique, or analyze the visual design and UX of a terminal-based application. Triggers on requests like "review my TUI", "inspect the terminal UI", "design feedback for my CLI", or "UX review". Analyzes both screenshots and source code to provide comprehensive design feedback.
---

# TUI Design Inspector

This skill enables professional-grade design inspection for terminal user interfaces (TUI). It combines visual analysis of screenshots with source code review to provide comprehensive UX feedback.

## When to Use

- User requests design review of a terminal application
- User asks for UX feedback on a CLI or TUI
- User wants to improve the visual design of their terminal app
- User shares screenshots of their terminal application for critique

## Inspection Workflow

### Phase 1: Gather Context

1. **Capture the current state**
   - Request or locate screenshots of the TUI in different states
   - Identify the UI framework being used (Bubble Tea, tview, termbox, etc.)
   - Read the main view/rendering source files

2. **Understand the application**
   - Identify the application's purpose and target users
   - Map out the different screens/states/modes
   - Document the navigation flow between states

### Phase 2: Analyze UX Patterns

Evaluate the following areas using the principles in `references/tui_design_principles.md`:

#### 2.1 Information Architecture
- Is content organized logically?
- Are related items grouped together?
- Is the hierarchy of information clear?
- Can users find what they need quickly?

#### 2.2 Navigation & Flow
- Are navigation patterns consistent across screens?
- Is the current location/state always clear?
- Can users easily move between sections?
- Are there dead-ends or confusing loops?

#### 2.3 Keyboard Interaction
- Are shortcuts intuitive and memorable?
- Do shortcuts follow common conventions (vim, emacs, standard)?
- Is there consistency in key bindings across modes?
- Are destructive actions protected (confirmation required)?

#### 2.4 Feedback & Affordances
- Do actions provide immediate visual feedback?
- Are loading/processing states indicated?
- Are errors clearly communicated?
- Is success feedback appropriate (not over/under stated)?

#### 2.5 Visual Hierarchy
- Is the most important information prominent?
- Are visual weights balanced across the layout?
- Do colors guide attention appropriately?
- Is there sufficient contrast for readability?

#### 2.6 Layout & Spacing
- Is whitespace used effectively?
- Are elements aligned consistently?
- Is the layout responsive to terminal size?
- Are panels/sections clearly delineated?

#### 2.7 Help & Discoverability
- Are available actions visible or discoverable?
- Is there contextual help available?
- Are keyboard shortcuts documented in the UI?
- Can new users orient themselves quickly?

### Phase 3: Generate Report Document

**IMPORTANT**: After completing the analysis, MUST generate a formal document using one of these methods:

1. **Preferred: Use `docx` skill** to create a professional Word document
   ```
   Invoke the docx skill to create a TUI inspection report document
   ```

2. **Alternative: Create Markdown file** in the project's `docs/` directory
   ```
   Write report to: docs/tui-inspection-report-YYYY-MM-DD.md
   ```

The document MUST include:
- Application name and inspection date
- Executive summary (2-3 sentences)
- Detailed findings for all 7 UX pattern areas
- Prioritized recommendations
- Overall UX score

### Phase 4: Deliver Feedback

After generating the document, provide a summary to the user. Structure the summary using this format:

```markdown
## TUI Design Inspection Report

### Overview
[Brief summary of the application and inspection scope]

### Strengths
[What the design does well - be specific]

### Areas for Improvement

#### Critical Issues
[Problems that significantly impact usability]

#### Recommendations
[Suggestions for enhancement, prioritized by impact]

### UX Pattern Analysis
[Detailed findings for each area inspected]

### Summary
[Key takeaways and next steps]

### Generated Document
[Path to the generated report document]
```

## Feedback Guidelines

When providing feedback:

1. **Be specific** - Reference exact screens, elements, or interactions
2. **Explain the "why"** - Connect issues to UX principles
3. **Prioritize** - Distinguish critical issues from nice-to-haves
4. **Be constructive** - Frame feedback as opportunities, not failures
5. **Consider context** - Account for terminal limitations and target users

## Common TUI Anti-patterns to Watch For

| Anti-pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Modal overload | Too many nested modals confuse users | Use inline editing or slide panels |
| Hidden shortcuts | Users can't discover functionality | Show hints in help bar or status line |
| Inconsistent focus | Unclear which element is active | Strong visual indicator for focus |
| Wall of text | Information overload | Progressive disclosure, collapsible sections |
| No escape hatch | Users feel trapped in modes | Always allow Esc to go back/cancel |
| Silent failures | Actions fail with no feedback | Clear error messages with recovery hints |
| Overcrowded UI | Too much on one screen | Prioritize, use tabs or views |
| Poor contrast | Hard to read in various terminals | Test with light/dark themes |

## Terminal-Specific Considerations

- **256-color vs true color** - Design should degrade gracefully
- **Terminal size** - Test at minimum viable dimensions (80x24)
- **Font variations** - Avoid relying on specific Unicode characters
- **Copy/paste** - Ensure text can be selected when needed
- **Accessibility** - Consider screen reader compatibility

## Resources

### references/
Contains detailed TUI design principles and evaluation criteria:
- `tui_design_principles.md` - Comprehensive guide to terminal UI design patterns, color theory, and UX best practices
