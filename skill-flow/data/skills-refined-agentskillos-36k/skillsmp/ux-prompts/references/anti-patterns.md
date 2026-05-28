# Prompt Anti-Patterns

Common mistakes that reduce prompt effectiveness, with fixes.

## Anti-Pattern 1: The Mega-Prompt

### Problem
Entire UX spec crammed into one prompt.

```markdown
❌ BAD: Build the entire e-commerce app with product listing,
cart, checkout, user auth, order history, admin dashboard...
[3000+ words]
```

### Why It Fails
- Overwhelms AI context window
- No clear stopping point
- Interdependencies hidden
- Can't verify incrementally
- One failure breaks everything

### Fix
Break into atomic features:
```markdown
✓ GOOD: Prompt 1 - Design tokens
✓ GOOD: Prompt 2 - Product card component
✓ GOOD: Prompt 3 - Product list with cards
✓ GOOD: Prompt 4 - Cart drawer
...
```

### Rule
If prompt exceeds 500 words, consider splitting.

---

## Anti-Pattern 2: The Reference Trap

### Problem
Prompts reference other prompts instead of being self-contained.

```markdown
❌ BAD: Style the button as described in Prompt 3.
❌ BAD: Use the same spacing as the card component.
❌ BAD: See earlier prompt for color values.
```

### Why It Fails
- AI tools don't share context between prompts
- Readers must hunt for referenced info
- Changes in referenced prompt break dependent prompts
- Can't run prompts in parallel

### Fix
Re-state all needed context inline:
```markdown
✓ GOOD: Style the button with:
- Background: var(--color-primary, #2563EB)
- Padding: 12px 24px
- Border-radius: 8px
- Font: 14px, weight 500
```

### Rule
Each prompt must be executable with zero context from other prompts.

---

## Anti-Pattern 3: Vague Specifications

### Problem
Using subjective or relative terms without concrete values.

```markdown
❌ BAD: "Use appropriate spacing"
❌ BAD: "Make it look professional"
❌ BAD: "Add a nice hover effect"
❌ BAD: "Use brand colors"
```

### Why It Fails
- AI interprets vague terms inconsistently
- Different runs produce different results
- No way to verify correctness
- Designer intent lost in translation

### Fix
Use exact specifications:
```markdown
✓ GOOD: Padding: 16px horizontal, 12px vertical
✓ GOOD: Background: #F8FAFC, border: 1px solid #E2E8F0
✓ GOOD: Hover: darken background 5%, add shadow 0 2px 8px rgba(0,0,0,0.1)
✓ GOOD: Primary color: #2563EB, secondary: #64748B
```

### Rule
Every visual property needs a concrete value.

---

## Anti-Pattern 4: Missing States

### Problem
Only describing the "happy path" default state.

```markdown
❌ BAD: "Create a product card showing name and price"
[No mention of: loading, error, empty, hover, disabled...]
```

### Why It Fails
- Real apps have many states
- Users experience edge cases
- Implementation must guess at other states
- Results in incomplete components

### Fix
Enumerate all states:
```markdown
✓ GOOD:
### States
- Default: Name, price, image displayed
- Loading: Skeleton with pulse animation
- Error: Error icon + "Failed to load" text
- Hover: Lift 4px + shadow
- Out of stock: Grayed overlay + "Sold Out" badge
- Selected: Blue border, checkmark
```

### Rule
List at least 5 states for interactive components.

---

## Anti-Pattern 5: Wrong Build Order

### Problem
Building advanced features before their dependencies.

```markdown
❌ BAD:
Prompt 1: Build checkout flow
Prompt 2: Build cart
Prompt 3: Build product card
[Checkout needs cart, cart needs products]
```

### Why It Fails
- Can't test components in isolation
- Must mock dependencies
- Rework when dependencies change
- Integration nightmare

### Fix
Sequence by dependency graph:
```markdown
✓ GOOD:
Prompt 1: Design tokens (colors, spacing)
Prompt 2: Product card component
Prompt 3: Cart item component
Prompt 4: Cart drawer (uses cart items)
Prompt 5: Checkout flow (uses cart)
```

### Rule
If A requires B, build B first.

---

## Anti-Pattern 6: Implicit Boundaries

### Problem
Not stating what the prompt excludes.

```markdown
❌ BAD: "Build the login form"
[Does this include password reset? OAuth? Remember me?
 Email verification? Rate limiting?]
```

### Why It Fails
- Scope creeps unknowingly
- Implementer makes assumptions
- Results don't match expectations
- Review cycles increase

### Fix
Explicit include/exclude:
```markdown
✓ GOOD:
### This prompt includes:
- Email and password fields
- Submit button
- Basic validation messages
- "Forgot password" link (navigation only)

### This prompt does NOT include:
- OAuth/social login
- Remember me checkbox
- Password reset flow
- Account creation
- Rate limiting logic
```

### Rule
Explicitly state 3+ exclusions for every prompt.

---

## Anti-Pattern 7: Duplicate Definitions

### Problem
Defining the same component multiple times across prompts.

```markdown
❌ BAD:
Prompt 5: "Create a Button component with..."
Prompt 8: "Build a primary button with rounded corners..."
Prompt 12: "Add a submit button styled as..."
```

### Why It Fails
- Inconsistent implementations
- Maintenance nightmare
- No single source of truth
- Wasted effort

### Fix
Define once, reference by name:
```markdown
✓ GOOD:
Prompt 3: "Create Button component with variants (primary, secondary, ghost)"

Prompt 8: "Use the Button component (from Prompt 3) with variant='primary'"

Prompt 12: "Use Button component, type='submit', variant='primary'"
```

### Rule
Each component defined exactly once.

---

## Anti-Pattern 8: Missing Interactions

### Problem
Describing appearance but not behavior.

```markdown
❌ BAD: "Card should be 200x150px with product image and title"
[What happens on click? Hover? Touch? Keyboard?]
```

### Why It Fails
- Appearance without behavior is incomplete
- Implementer guesses at interactions
- Accessibility often missed
- Inconsistent user experience

### Fix
Document all interactions:
```markdown
✓ GOOD:
### Interactions
- Hover: Card lifts 4px, cursor becomes pointer
- Click: Navigates to /product/[id]
- Keyboard: Tab focusable, Enter/Space to activate
- Touch: 48px touch target minimum
- Long press (mobile): Shows quick-add menu
```

### Rule
Every interactive element needs click, hover, and keyboard behavior.

---

## Anti-Pattern 9: Responsive Afterthought

### Problem
Designing only for one viewport size.

```markdown
❌ BAD: "Create a 3-column product grid"
[What about mobile? Tablet?]
```

### Why It Fails
- Mobile often majority of traffic
- Retrofit is harder than design upfront
- Broken layouts on untested viewports
- Inconsistent spacing between breakpoints

### Fix
Specify all breakpoints:
```markdown
✓ GOOD:
### Layout
- Mobile (<640px): Single column, full width
- Tablet (640-1024px): 2-column grid, 16px gap
- Desktop (>1024px): 3-column grid, 24px gap

### Responsive Details
- Images: aspect-ratio 4:3, object-fit cover
- Card padding: 12px mobile, 16px desktop
- Touch targets: 44px minimum on mobile
```

### Rule
Every layout prompt specifies at least 3 breakpoints.

---

## Anti-Pattern 10: No Verification Criteria

### Problem
No way to know if implementation is correct.

```markdown
❌ BAD: "Build the header component"
[How do we know it's done? How do we test it?]
```

### Why It Fails
- "Done" is subjective
- QA has no acceptance criteria
- Bugs slip through
- Unclear when to stop iterating

### Fix
Include verification checklist:
```markdown
✓ GOOD:
### Verification
- [ ] Logo displays and links to home
- [ ] Navigation items all clickable
- [ ] Active state shows on current page
- [ ] Mobile menu opens/closes
- [ ] Sticky behavior works on scroll
- [ ] Dark mode colors correct
```

### Rule
Every prompt ends with specific, testable verification criteria.

---

## Quick Reference: Anti-Pattern Detection

| If You See... | Suspect... | Fix By... |
|---------------|------------|-----------|
| 500+ word prompt | Mega-prompt | Split into atomic units |
| "See prompt X" | Reference trap | Inline the context |
| "Appropriate", "nice" | Vague specs | Add concrete values |
| Only default state | Missing states | List 5+ states |
| Features before deps | Wrong order | Dependency graph |
| No exclusions | Implicit boundaries | Add NOT include section |
| Same thing twice | Duplicates | Define once, reference |
| No hover/click | Missing interactions | Full interaction model |
| One viewport | Responsive afterthought | 3+ breakpoints |
| No checklist | No verification | Add testable criteria |
