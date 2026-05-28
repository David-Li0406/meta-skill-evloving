---
name: web-uiux-design
description: "Comprehensive UI/UX design principles for web applications based on Sociomedia Human Interface Guidelines (SHIG). Use when Claude needs to design or review web application interfaces, evaluate UI/UX decisions and patterns, create user-friendly forms and navigation, build accessible and consistent interfaces, apply object-oriented UI design principles, or optimize user workflows and reduce cognitive load."
---

# Web UI/UX Design Principles

A comprehensive guide for designing effective web application interfaces, derived from Sociomedia's Human Interface Guidelines (SHIG). Apply these principles when creating, reviewing, or improving UI/UX designs.

## Quick Reference Categories

Select the appropriate reference based on task:

- **Model & Conceptual Design**: See [references/model-principles.md](references/model-principles.md) - Mental models, object-oriented UI, user empowerment
- **Interaction Design**: See [references/interaction-principles.md](references/interaction-principles.md) - Direct manipulation, feedback, controls, forms
- **Presentation & Layout**: See [references/presentation-principles.md](references/presentation-principles.md) - Visual design, navigation, accessibility

## Core Design Philosophy

### 1. Simplicity First
Reduce elements to essentials. Every feature must justify its existence.

### 2. User Empowerment
Users control the system, not vice versa. Enable self-paced, modeless workflows.

### 3. Object-Oriented UI (OOUI)
Extract domain objects from requirements. Let users manipulate objects directly (Noun → Verb pattern).

### 4. Consistency & Learnability
Apply uniform rules for colors, shapes, positions, behaviors. Same property = same expression.

### 5. Fail-Safe Over Fool-Proof
Prioritize reversible actions and undo capability over excessive confirmations.

## Essential Principles Checklist

When designing/reviewing UI, verify:

**Structure**
- [ ] Navigation items are nouns, not verbs
- [ ] Object-action order (select target first, then action)
- [ ] Consistent visual hierarchy and grouping (Gestalt principles)
- [ ] Clear escape routes back to home/start

**Interaction**
- [ ] Feedback within 0.1 seconds
- [ ] Transitions for state changes (0.1-0.5s)
- [ ] Modeless design where possible
- [ ] Direct manipulation feel

**Forms & Input**
- [ ] Smart defaults (safe, common, neutral)
- [ ] Constraint controls (dropdowns, pickers) for limited options
- [ ] Suggestions/autocomplete for text input
- [ ] Flexible format acceptance (system normalizes input)
- [ ] Prerequisites shown upfront

**Controls**
- [ ] Radio buttons for single selection (requires default)
- [ ] Checkboxes for independent on/off toggles
- [ ] Action buttons with specific verbs ("Save", "Delete")
- [ ] Touch targets ≥7mm

**Accessibility**
- [ ] Works without color dependency
- [ ] Supports text scaling
- [ ] Screen reader compatible
- [ ] No time-limited interactions

## Key Laws & Concepts

| Law | Application |
|-----|-------------|
| Fitts's Law | Larger + closer = easier to click. Size buttons appropriately. |
| Hick's Law | More choices = longer decision time. Limit visible options. |
| Conservation of Complexity | Complexity cannot be destroyed, only moved. Push complexity to system side. |
| Task Coherence | Users repeat recent actions. Remember and prioritize recent behaviors. |
| Pareto (80/20) | 80% use 20% of features. Optimize for major tasks. |

## Anti-Patterns to Avoid

- Modal dialogs for routine confirmations
- "OK/Cancel" instead of specific action verbs
- Confirmation dialogs for reversible actions
- System-centric terminology
- Requiring user to remember information across screens
- Changing menu item positions dynamically
- Game-like elements in non-game applications
- Customization as a solution for bad defaults
- Negative phrasing in checkbox labels

## Design Decision Framework

```
Is this action reversible?
├── Yes → Execute silently, show result in UI
└── No → Is data loss involved?
    ├── No → Execute with inline feedback
    └── Yes → Confirm with specific verb button
```

```
How many options to present?
├── 0-2 → Radio buttons or segmented control
├── 3-7 → Dropdown or radio group
├── 8+ → Searchable list or autocomplete
└── Unlimited → Text input with suggestions
```

## Implementation Notes

- Test interfaces in grayscale to verify non-color-dependent design
- Follow platform conventions for button order (OK/Cancel positioning)
- Expand hotspots beyond visible button boundaries
- Preserve user-placed spatial arrangements
- Use bidirectional transitions (expand ↔ collapse must animate both ways)
