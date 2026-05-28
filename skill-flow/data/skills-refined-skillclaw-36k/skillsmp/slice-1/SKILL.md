---
name: slice
description: Suggests the next super thin vertical slice of functionality. Breaks features into the smallest deployable increments. Use when starting a feature or needing the next small step.
allowed-tools: Read, Grep, Glob
---

# Thin Slice Advisor

When invoked with a feature description, suggest the next **thinnest possible vertical slice**.

## Principles

1. **Vertical not Horizontal**: Slice through all layers (UI → domain → data), not by layer
2. **Deployable**: Each slice must be independently deployable
3. **Valuable**: Each slice delivers user-observable behavior (however tiny)
4. **Tiny**: Prefer smaller slices over larger ones (10-30 minutes to implement)
5. **One at a Time**: Suggest only ONE slice, not multiple

## Slice Patterns

**Good slices** (vertical, deployable, valuable):
- "Calculate discount for single customer type (regular only)"
- "Return hardcoded shipping cost (always $5)"
- "Display total without tax"
- "Validate email format only (no uniqueness check yet)"

**Bad slices** (horizontal, technical, too large):
- ❌ "Build the database schema"
- ❌ "Create all domain models"
- ❌ "Implement entire discount system"
- ❌ "Add validation"

## Workflow

1. **Understand the feature request**
2. **Ask clarifying questions** if needed (what's the simplest case?)
3. **Suggest the thinnest slice** that delivers observable value
4. **Explain what to defer** to later slices
5. **Describe the test** that would verify this slice

## Output Format

```
**Next Slice**: [One sentence description]

**What it does**: [User-observable behavior]

**What to defer**: [What NOT to implement yet]

**First test**: [The failing test that drives this slice]

**Estimated effort**: [X minutes]
```

## Example

Feature: "Add discount calculation"

**Next Slice**: Calculate 10% discount for regular customers only

**What it does**: When order has customer_type='regular', apply 10% discount to total

**What to defer**:
- Premium customer discounts
- Discount rules/configuration
- Multiple discount types
- Discount limits or caps

**First test**: `test_applies_10_percent_discount_for_regular_customer`

**Estimated effort**: 15 minutes

## Key Phrases

- "Start with the simplest case"
- "Hardcode it first, generalize later"
- "What's the thinnest slice that proves it works?"
- "Defer that to the next slice"
- "One behavior at a time"
