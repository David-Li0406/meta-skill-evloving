# Example: Poorly-Written AGENTS.md

This example demonstrates common mistakes to avoid.

```markdown
# Billing

This folder has the billing stuff.

## Files

There are some components here:
- PlanCard
- SubscriptionModal
- Some other files

## How to use

Call the subscription hook:

\`\`\`typescript
usePlanSubscribe()
\`\`\`

And then it works.

## Notes

- Use Stripe
- Don't forget to render the modal
- Test cards available online
\`\`\`

## Why This Example Is Bad

❌ **Vague header** - "Billing" instead of full path, no context
❌ **No commands** - How do I test this?
❌ **Incomplete list** - "Some other files" is lazy
❌ **No hook signature** - What parameters? What does it return?
❌ **No import path** - Where is `usePlanSubscribe` from?
❌ **Unclear example** - `usePlanSubscribe()` with no context
❌ **Vague instructions** - "then it works" - how?
❌ **Weak warnings** - "Don't forget" is not CRITICAL
❌ **No specifics** - "Test cards available online" - which one?
❌ **Missing types** - No data structure documentation
❌ **No integration details** - How is Stripe configured?
❌ **No cross-references** - Related files not mentioned

## Common Mistakes Breakdown

### 1. Vague Descriptions
❌ "This folder has the billing stuff"
✅ "Stripe billing integration components for Zo Computer"

**Why:** Be specific about technology (Stripe) and purpose (billing integration).

### 2. Incomplete Information
❌ "Some other files"
✅ Complete table of all components with purposes

**Why:** Agents can't work with vague information.

### 3. Missing Signatures
❌ `usePlanSubscribe()`
✅ Complete signature with parameters, types, return values

**Why:** Agents need to know how to call the function.

### 4. No Import Paths
❌ "Call the subscription hook"
✅ `import { usePlanSubscribe } from "@/components/billing/use-plan-subscribe"`

**Why:** Agents can't import without knowing the path.

### 5. Weak Warnings
❌ "Don't forget to render the modal"
✅ **CRITICAL:** `modalUI` must be rendered or Stripe modal won't appear

**Why:** Critical issues need emphasis and explanation of consequences.

### 6. Missing Context
❌ "Test cards available online"
✅ Use Stripe test card: `4242 4242 4242 4242`

**Why:** Provide specific, actionable information.

### 7. No Type Definitions
❌ Missing
✅ Show complete `Plan` interface

**Why:** Agents need to understand data structures.

### 8. Unclear Flow
❌ "And then it works"
✅ Step-by-step flow: Click → API call → Modal opens → Success → Update

**Why:** Agents benefit from understanding the process.

### 9. No Testing Guidance
❌ Missing
✅ Specific test commands and test mode setup

**Why:** Testing is critical for code changes.

### 10. Poor Organization
❌ Random sections with no structure
✅ Logical flow: Overview → Components → Hooks → Types → Integration → Testing → Warnings

**Why:** Structure helps agents find information quickly.

## Fixing This AGENTS.md

To fix this example:

1. **Add full path** - `components/billing/ - Agent Instructions`
2. **Complete the component list** - All files with purposes
3. **Document hook fully** - Parameters, return type, usage example
4. **Show imports** - Exact import statements
5. **Add type definitions** - Show `Plan` interface
6. **Explain integration** - How Stripe is configured
7. **Add testing** - Commands and test mode setup
8. **Strengthen warnings** - Use **CRITICAL** for must-dos
9. **Provide specifics** - Exact test card number
10. **Cross-reference** - Link related files

The result should look like the `good-agents-md.md` example.
