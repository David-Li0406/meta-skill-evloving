---
id: wireframing
name: "Wireframing"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Wireframing

## Metadata
- **Category:** UX / Design Methods
- **Difficulty:** Beginner
- **Tags:** #methodology #ux #design #wireframes #prototyping
- **Agent:** faion-usability-agent

---

## Problem

Design jumps straight to high-fidelity visuals. Layout and functionality are debated alongside colors and fonts. Changes are expensive because designs are "finished." Stakeholders get distracted by aesthetics instead of usability. Structure problems are discovered late.

Without wireframing:
- Premature focus on aesthetics
- Expensive design changes
- Unclear information hierarchy
- Stakeholder misalignment

---

## Framework

### What are Wireframes?

Wireframes are low-fidelity representations of a user interface that focus on structure, layout, and functionality without visual design details.

### Fidelity Levels

| Level | Detail | Purpose | When to Use |
|-------|--------|---------|-------------|
| **Low** | Boxes and lines | Explore concepts | Early ideation |
| **Medium** | Basic content | Test structure | Design iteration |
| **High** | Detailed layout | Finalize design | Pre-visual design |

### What Wireframes Show

| Include | Exclude |
|---------|---------|
| Layout structure | Colors |
| Content hierarchy | Typography styles |
| Navigation | Images |
| Functionality | Branding |
| Interaction patterns | Final copy |

---

## Process

### Step 1: Understand Requirements

Before wireframing:
- User needs (from research)
- Business requirements
- Technical constraints
- Content inventory

### Step 2: Sketch Ideas

Start with pencil and paper:
- Quick exploration
- Multiple concepts
- No commitment
- Cheap to discard

### Step 3: Create Wireframes

**Key elements:**
- Header and navigation
- Content areas
- Calls to action
- Form elements
- Footer

### Step 4: Review and Iterate

Share for feedback:
- Does it meet requirements?
- Is the hierarchy clear?
- Can users accomplish goals?
- What is confusing?

### Step 5: Document Annotations

Add notes explaining:
- Behavior and interactions
- Conditional states
- Content notes
- Technical requirements

---

## Templates

### Wireframe Documentation Template

```markdown
# Wireframe: [Page/Screen Name]

**Version:** [X.X]
**Date:** [Date]
**Designer:** [Name]
**Status:** [Draft/Review/Approved]

## Purpose
[What this page/screen is for]

## User Goal
[What user wants to accomplish here]

## Layout

[Wireframe image]

## Annotations

| # | Element | Description | Notes |
|---|---------|-------------|-------|
| 1 | [Element name] | [What it is] | [Behavior/requirements] |
| 2 | [Element name] | [What it is] | [Behavior/requirements] |

## States

### Default State
[Description or wireframe]

### Empty State
[Description or wireframe]

### Error State
[Description or wireframe]

### Loading State
[Description or wireframe]

## Interactions

| Element | Trigger | Action | Result |
|---------|---------|--------|--------|
| [Element] | [Click/Hover] | [What happens] | [Outcome] |

## Responsive Considerations
- **Desktop:** [Notes]
- **Tablet:** [Notes]
- **Mobile:** [Notes]

## Open Questions
- [Question 1]
- [Question 2]
```

### Component Wireframe Template

```markdown
# Component: [Name]

## Purpose
[What this component does]

## Variants

### Variant 1: [Name]
[Wireframe]
- When to use: [Context]

### Variant 2: [Name]
[Wireframe]
- When to use: [Context]

## States
- Default: [Description]
- Hover: [Description]
- Active: [Description]
- Disabled: [Description]

## Content Guidelines
- [Content rule 1]
- [Content rule 2]

## Usage Notes
- [When to use]
- [When not to use]
```

---

## Examples

### Low-Fidelity Wireframe

```
+----------------------------------+
|  Logo        [Nav] [Nav] [Nav]  |
+----------------------------------+
|                                  |
|  [     Hero Headline      ]     |
|  [     Subtext            ]     |
|       [  CTA Button  ]          |
|                                  |
+----------------------------------+
|  [Card]    [Card]    [Card]     |
+----------------------------------+
|  Footer links | Social | Legal  |
+----------------------------------+
```

### Medium-Fidelity Wireframe

```
+------------------------------------------+
|  [Logo]     Home | Products | About | CTA|
+------------------------------------------+
|                                          |
|  Welcome to Our Platform                 |
|  Helping you achieve your goals          |
|                                          |
|         [ Get Started Free ]             |
|                                          |
+------------------------------------------+
|  +-----------+  +-----------+  +-------+ |
|  | Feature 1 |  | Feature 2 |  | Feat 3| |
|  |           |  |           |  |       | |
|  | [Image]   |  | [Image]   |  | [Img] | |
|  |           |  |           |  |       | |
|  | Text here |  | Text here |  | Text  | |
|  +-----------+  +-----------+  +-------+ |
+------------------------------------------+
```

---

## Best Practices

### Do

- Start with user goals
- Explore multiple layouts
- Get feedback early
- Annotate behavior
- Consider all states
- Design for mobile too

### Don't

- Use colors (except gray)
- Add final images
- Write perfect copy
- Skip to high-fidelity
- Wireframe alone (collaborate)
- Forget error/empty states

---

## Common Elements

### Navigation
```
[Logo] [Link] [Link] [Link] [CTA]
```

### Hero Section
```
[     Headline        ]
[     Subtext         ]
[  Primary CTA  ]
```

### Card
```
+-----------------+
| [Image]         |
| Title           |
| Description     |
| [Action]        |
+-----------------+
```

### Form
```
Label
[Input field          ]

Label
[Input field          ]

[Submit Button]
```

### Footer
```
[Links] [Links] [Links] [Social]
[Copyright and legal]
```

---

## Common Mistakes

1. **Too pretty too soon** - Add visual design later
2. **Missing states** - Only default view
3. **No annotations** - Behavior unclear
4. **Skipping sketches** - Jump to tool
5. **One layout only** - No exploration

---

## Tools

| Tool | Best For | Notes |
|------|----------|-------|
| **Pen and paper** | Early exploration | Fastest |
| **Figma** | Collaborative | Popular choice |
| **Sketch** | Mac users | Design focused |
| **Balsamiq** | Quick mockups | Deliberately lo-fi |
| **Whimsical** | Fast wireframes | Simple and clean |
| **Miro** | Workshop collaboration | Whiteboard style |

---

## Wireframe Critique Checklist

- [ ] Does it meet user goals?
- [ ] Is hierarchy clear?
- [ ] Is navigation intuitive?
- [ ] Are CTAs prominent?
- [ ] Are all states shown?
- [ ] Is it responsive-ready?
- [ ] Are annotations complete?
- [ ] Does it follow conventions?

---

## Transitioning to High-Fidelity

**When wireframes are done:**
1. Requirements validated
2. Stakeholders aligned
3. Layout approved
4. Interactions documented

**Next steps:**
1. Apply visual design
2. Add real content
3. Create interactive prototype
4. Conduct usability testing

---

## References

- Don't Make Me Think by Steve Krug
- About Face by Alan Cooper
- Wireframing Best Practices