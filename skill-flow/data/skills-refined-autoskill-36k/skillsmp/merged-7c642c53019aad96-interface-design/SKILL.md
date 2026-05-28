---
name: interface-design
description: Use this skill for designing interfaces such as dashboards, admin panels, apps, tools, and interactive products, ensuring a systematic and consistent approach.
---

# Interface Design

Build interface designs with craft, consistency, and systematic precision.

## Scope

**Use for:** Dashboards, admin panels, SaaS apps, tools, settings pages, data interfaces.

**Not for:** Landing pages, marketing sites, campaigns. Redirect those to `/design-suite:launchpad`.

## Design Principles

### Spacing
Use a consistent base unit for spacing. Stick to multiples to maintain a cohesive design.

### Padding
Keep padding symmetrical. If one side is 16px, others should match unless there's a clear reason.

### Depth
Choose ONE approach and commit:
- **Borders-only** — Clean, technical. For dense tools.
- **Subtle shadows** — Soft lift. For approachable products.
- **Layered shadows** — Premium, dimensional. For cards that need presence.

### Border Radius
Select a scale for border radius that reflects the product's tone:
- Sharper feels technical; rounder feels friendly.

### Typography
Establish a hierarchy with appropriate weights and styles for headlines, body text, and data.

### Color
Use color to communicate meaning and structure. Avoid decorative colors that do not serve a purpose.

### Animation
Implement fast micro-interactions with smooth easing. Avoid bouncy effects.

### Controls
Utilize native components where possible, but build custom components for enhanced styling.

## Workflow

### Before Writing Code
State your design choices to clarify intent:
```
Direction: [what this should feel like]
Depth: [borders / subtle shadows / layered]
Spacing: [base unit]
```

### Communication
Be invisible in your process. Avoid announcing modes or narrating your actions. Instead, jump into work and provide suggestions with reasoning.

### Suggest + Ask
Lead with your exploration and recommendation, then confirm with the user:
```
"Domain: [5+ concepts from the product's world]
Color world: [5+ colors that exist in this domain]
Signature: [one element unique to this product]
Rejecting: [default 1] → [alternative], [default 2] → [alternative], [default 3] → [alternative]

Direction: [approach that connects to the above]"

[AskUserQuestion: "Does that direction feel right?"]
```

### If Project Has system.md
Read the existing system file and apply the established decisions.

### If No system.md
1. Explore the domain — Produce required outputs.
2. Propose a direction referencing all outputs.
3. Confirm with the user.
4. Build using established principles.
5. Evaluate your work against the mandate checks before presenting.
6. Offer to save your patterns for future sessions.

## Avoid

- Harsh borders and dramatic surface jumps.
- Inconsistent spacing and mixed depth strategies.
- Missing interaction states for components.
- Decorative gradients and multiple accent colors.

## After Completing a Task
When you finish building something, **always offer to save**:
```
"Want me to save these patterns for future sessions?"
```
If yes, document the design choices and configurations for future reference.

## Templates
Starting points for common interface types:
- `templates/saas-dashboard.md` — SaaS analytics dashboards, admin panels.

Templates are scaffolds, not solutions. Adapt to your product's specific needs.

## Commands
- `/design-suite:workbench-init` — Initialize design system for a project.
- `/design-suite:workbench-status` — Current system state.
- `/design-suite:workbench-audit` — Check code against system.
- `/design-suite:workbench-extract` — Extract patterns from code.