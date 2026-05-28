# Prompt Quality Amplifiers

Techniques to maximize prompt effectiveness for UI generation tools.

## Context Density Test

Each prompt should be understandable by someone who:
- Has never seen this project
- Has 30 seconds to read
- Will implement immediately

### Density Checklist

| Element | Present? | Quality Check |
|---------|----------|---------------|
| What it is | ✓/✗ | One sentence, no jargon |
| Where it fits | ✓/✗ | Parent context named |
| All dimensions | ✓/✗ | Specific values, not "appropriate" |
| All states | ✓/✗ | Exhaustive list |
| All interactions | ✓/✗ | User actions covered |
| What's excluded | ✓/✗ | Boundaries explicit |

## Specificity Ladder

Progress from vague to excellent:

| Level | Example | Problem |
|-------|---------|---------|
| Vague | "Make it look good" | No direction |
| Better | "Use consistent spacing" | Still unclear |
| Good | "8px padding, 16px gap" | Missing context |
| Excellent | "8px padding (var(--space-2)), 16px gap (var(--space-4)), matching card pattern from design system" | ✓ Complete |

### Specificity Rules

**Dimensions:**
- ❌ "Appropriate padding"
- ✓ "16px padding on all sides"

**Colors:**
- ❌ "Blue button"
- ✓ "Primary action button using --color-primary (#2563EB)"

**States:**
- ❌ "With loading state"
- ✓ "Loading: spinner replaces button text, button disabled, opacity 0.7"

**Interactions:**
- ❌ "Clickable"
- ✓ "On click: opens modal, on hover: background darkens 5%, on focus: 2px ring"

## Completeness Checklist

Every prompt must include:

### Required Elements
- [ ] **Context** - What this is, where it fits
- [ ] **All dimensions** - Width, height, padding, margins
- [ ] **All possible states** - Default, hover, active, disabled, loading, error
- [ ] **All interactions** - Click, hover, focus, keyboard, touch
- [ ] **What NOT to include** - Explicit boundaries

### Conditional Elements (include when applicable)
- [ ] **Animations** - Duration, easing, triggers
- [ ] **Responsive behavior** - Breakpoint changes
- [ ] **Accessibility** - ARIA labels, keyboard nav
- [ ] **Dark mode** - Color variations
- [ ] **Empty states** - When no data
- [ ] **Error states** - Invalid, failed

## Extraction Patterns

### From UX Spec State Table

**Spec:**
```markdown
| State | User Sees | User Understands | User Can Do |
|-------|-----------|------------------|-------------|
| Empty | Illustration + "No items" | Nothing here | Add item |
| Loading | Skeleton cards | Loading | Wait |
```

**Prompt extraction:**
```markdown
### States
- Empty: Show illustration (48x48px icon) centered, "No items yet" text below (14px, gray-500), "Add Item" button below (primary style)
- Loading: Show 3 skeleton cards, pulse animation, maintain list structure
```

### From Affordance Table

**Spec:**
```markdown
| Element | Action | Visual Signal | Touch Target |
|---------|--------|---------------|--------------|
| Card | Open detail | Hover lift, pointer | Full card |
```

**Prompt extraction:**
```markdown
### Interactions
- Hover: Card lifts with subtle shadow (0 4px 12px rgba(0,0,0,0.1)), cursor: pointer
- Click (entire card): Opens detail view/modal
- Touch target: Full card area, minimum 44x44px
```

### From Flow Risk Table

**Spec:**
```markdown
| Risk | Location | Mitigation |
|------|----------|------------|
| Data loss | Form | Auto-save on blur |
```

**Prompt extraction:**
```markdown
### Constraints
- Must auto-save form data on field blur
- Must preserve draft state on accidental navigation
- Include unsaved changes indicator
```

## Dependency Notation

### Explicit Dependencies

```markdown
### Dependencies
- **Requires:** Design tokens (prompt 1), Button component (prompt 3)
- **Required by:** Checkout flow (prompt 15)
```

### Import Hints

```markdown
### Integration
Import from:
- `@/components/ui/button` - Primary button
- `@/lib/tokens` - Spacing, colors
- `@/hooks/useForm` - Form state management
```

## Boundary Setting

### Explicit Inclusions

```markdown
### This Prompt Includes
- Card visual structure
- All interactive states
- Responsive variants
- Accessibility attributes
```

### Explicit Exclusions

```markdown
### This Prompt Does NOT Include
- Data fetching logic
- API integration
- Parent layout
- Navigation between cards
- Persistent state management
```

### Handoff Notes

```markdown
### Handoff
- Component should accept: { data, onClick, variant }
- Returns: Single DOM element for easy list rendering
- For integration: See prompt 8 (List Container)
```

## Context Templates

### Component Context

```markdown
### Context
A [component type] used in [parent context]. Users interact with this to [primary action]. Part of the [feature name] flow.

**Visual reference:** [If available, describe or link]
**Related components:** [Names of sibling components]
```

### Page Context

```markdown
### Context
The [page name] page where users [primary purpose]. Accessed from [entry points]. Main flow: [1-2 sentence journey].

**User state when arriving:** [What they know/have]
**Exit points:** [Where they can go from here]
```

### Feature Context

```markdown
### Context
The [feature name] feature enabling users to [capability]. Triggered by [user action]. Impacts [affected areas].

**Feature flag:** [If applicable]
**Rollout:** [Full/gradual]
```

## Value Extraction

### From PRD Section 5 (Functional Decisions)

**PRD:**
```markdown
| ID | Function | Notes |
|----|----------|-------|
| F1 | Add item to cart | Max 99 per item |
```

**Prompt:**
```markdown
### Requirements
- Add to cart button increments quantity
- Maximum quantity: 99 per item
- Show quantity badge when > 0
- Disable "+" button at max
```

### From PRD Section 6 (UX Decisions)

**PRD:**
```markdown
#### 6.4 Feedback & States
- Loading: Spinner
- Success: Checkmark
```

**Prompt:**
```markdown
### States
- Loading: Button shows spinner (16px, centered), text hidden, button disabled
- Success: Checkmark icon replaces spinner, hold 400ms, then revert to default
```

## Quality Scoring

Rate each prompt 1-5 on these dimensions:

| Dimension | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|-----------|----------|--------------|---------------|
| Context | Missing | Partial | Complete + relations |
| Specificity | Vague | Some values | All values explicit |
| States | Missing | Common only | Exhaustive |
| Interactions | Missing | Click only | Full interaction model |
| Boundaries | Implicit | Partial | Explicit include/exclude |

**Target:** Average 4+ across all dimensions.
