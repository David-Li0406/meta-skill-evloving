# Form UX Patterns

## Core Principles

Every form field costs conversions. HubSpot saw 42% lift from reducing 15 fields to 5.

## Layout

| Pattern | Implementation |
|---------|---------------|
| **Single column** | Vertical flow, one field per row (except City/State/Zip) |
| **Labels above** | Never use placeholder-as-label (accessibility issue) |
| **Logical grouping** | Related fields together with clear sections |
| **Progress bar** | Multi-step forms need navigation + ability to go back |

## Validation

| Pattern | Implementation |
|---------|---------------|
| **Inline validation** | Validate on blur, not on submit (22% success rate increase) |
| **Green checkmarks** | Positive feedback for valid input |
| **Error placement** | Below field, red highlight, explain how to fix |
| **Positive framing** | "Enter valid email" not "Invalid email" |

## Input Optimization

| Pattern | Implementation |
|---------|---------------|
| **HTML5 input types** | `email`, `tel`, `number` for correct mobile keyboards |
| **Auto-format** | Space credit card numbers, format phone numbers |
| **Smart defaults** | Pre-fill country, date format when possible |
| **Autofill support** | Use correct `autocomplete` attributes |
| **Auto-detect** | City/state from postal code (28% of mobile sites don't) |

## Field Marking

- Mark **optional** fields, not just required
- 32% of users miss required fields when only optional is marked

## Multi-Step Forms

```
Step 1: Essential info (email, name)
Step 2: Details (preferences, customization)
Step 3: Payment/confirmation

Always show:
- Progress indicator ("Step 2 of 3")
- Back navigation
- Summary before final submit
```

## Mobile Form Considerations

- Large touch targets for inputs (44px+ height)
- Adequate spacing between fields
- Sticky submit button at bottom
- Minimize typing: dropdowns, toggles, date pickers
- Show/hide password toggle

## Error Message Examples

**Bad:**
- "Invalid input"
- "Error"
- "Field required"

**Good:**
- "Please enter a valid email (e.g., name@example.com)"
- "Password needs at least 8 characters"
- "We'll use this to send your receipt"

## Baymard Institute Key Findings

- 62% of sites fail to make guest checkout prominent
- 18% abandon due to checkout complexity
- Top frustrations: too many fields, unclear errors, slow validation
