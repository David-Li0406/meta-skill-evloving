---
name: aico-frontend-design
description: Use this skill when you need to transform a PRD or story into complete page or component designs, including ASCII layouts, component specifications, interaction flows, and frontend implementation prompts.
---

# Design

## ⚠️ CRITICAL RULES - READ FIRST

1. **CHECK EXISTING DESIGNS**: Always check `docs/reference/frontend/designs/` first.
2. **READ DESIGN SYSTEM**: Must read `docs/reference/frontend/design-system.md` before designing.
3. **READ CONSTRAINTS**: Must read `docs/reference/frontend/constraints.md` for tech stack.
4. **SAVE TO CORRECT PATH**: `docs/reference/frontend/designs/{name}.md`.

## Language Configuration

Before generating any content, check `aico.json` in project root for the `language` field to determine the output language. If not set, default to English.

## Process

1. **Read design system**: Load `docs/reference/frontend/design-system.md`.
2. **Read constraints**: Load `docs/reference/frontend/constraints.md`.
3. **Read PRD/story**: Load the source document from `docs/reference/pm/`.
4. **For each page/feature**:
   - Define user flow (entry → actions → outcome).
   - Create ASCII layout.
   - List all components with variants and props.
   - Write content/copy.
   - Document all interactions.
   - Generate frontend prompt.
5. **Save output**: ALWAYS write to `docs/reference/frontend/designs/{name}.md`.

## Design File Template

```markdown
# [Name] Design Spec

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD

## User Flow

1. User enters from [entry point].
2. User sees [initial state].
3. User can [actions].
4. Success: [outcome].

## Layout (ASCII)

┌─────────────────────────────────────┐
│ Header │
├─────────────────────────────────────┤
│ Content │
└─────────────────────────────────────┘

## Sections

### 1. [Section Name]

- **Purpose**: What this section achieves.
- **Components**: List of UI components used.
- **Content**: Actual text/copy.
- **Design notes**: Specific styling details.

## Component List

| Component | Variants           | Props          | Notes        |
| --------- | ------------------ | -------------- | ------------ |
| Button    | primary, secondary | size, disabled | Use for CTAs |

## Responsive

- **Desktop**: [layout notes].
- **Tablet**: [layout notes].
- **Mobile**: [layout notes].

## Interactions

| Trigger   | Action      | Feedback         |
|-----------|-------------|------------------|
| [Trigger] | [Action]    | [Feedback]       |
```