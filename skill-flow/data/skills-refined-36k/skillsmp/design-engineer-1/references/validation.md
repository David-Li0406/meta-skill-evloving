# Memory Management & Validation

## When to Document Patterns

Add patterns to `.design-engineer/system.md` when:

- Component used 2+ times
- Pattern is reusable across the project
- Has specific measurements worth remembering

**Don't document:**
- One-off components
- Temporary experiments
- Variations better handled by props

## Pattern Documentation Format

```markdown
## Button Primary
- Height: 36px
- Padding: 12px 16px
- Radius: 6px
- Font: 14px, 500 weight

## Card Default
- Border: 1px solid rgba(255, 255, 255, 0.06)
- Padding: 16px
- Radius: 8px
```

## System.md Structure

```markdown
# Design System

## Direction
[Design personality chosen]

## Foundation
[Color temperature and base]

## Tokens

### Spacing
Base: 4px
Scale: 4, 8, 12, 16, 24, 32

### Colors
[Defined palette]

### Typography
[Font choices and scale]

## Depth Strategy
[Borders-only / Subtle shadows / Layered]

## Patterns
[Component specifications]
```

## Validation Framework

Before finalizing designs, validate:

### Spacing Check
- All values align with defined base unit
- No arbitrary pixel values
- Consistent use of scale

### Depth Check
- Strategy is consistent throughout
- Borders-only means NO shadows
- No mixing strategies accidentally

### Color Check
- Only palette colors used
- No arbitrary hex codes
- Semantic colors for status only

### Pattern Check
- Reuse documented patterns
- No duplicate component definitions
- New patterns documented

## Audit Workflow

When running `/design-engineer:audit`:

1. Parse `.design-engineer/system.md`
2. Scan target files for violations
3. Report:
   - Spacing violations (values not on grid)
   - Depth violations (wrong strategy)
   - Color violations (not in palette)
   - Pattern drift (doesn't match docs)

## The Core Principle

**Memory compounds:** Each pattern saved makes future work faster and more consistent.

- First session: Establish and document
- Later sessions: Apply and extend
- Always: Validate before shipping
