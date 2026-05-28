---
id: error-prevention
name: "Error Prevention"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Error Prevention

## Metadata
- **Category:** UX / Usability Heuristic #5
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #heuristics #nielsen-norman #errors
- **Agent:** faion-usability-agent

---

## Problem

Users make mistakes that could have been prevented. They enter invalid data that the system accepts and then fails later. They accidentally trigger destructive actions. They miss required fields because nothing indicated they were required. Recovery is expensive; prevention is better.

Without error prevention:
- Wasted user effort
- Data quality issues
- Frustrated users
- Increased support costs

---

## The Heuristic

**Usability Heuristic #5:** Even better than good error messages is a careful design which prevents a problem from occurring in the first place. Either eliminate error-prone conditions or check for them and present users with a confirmation option before they commit to the action.

---

## Framework

### Error Types

| Type | Description | Prevention Strategy |
|------|-------------|---------------------|
| **Slips** | Right intention, wrong action | Constrain options, confirm |
| **Mistakes** | Wrong intention | Clear information, guidance |

### Prevention Strategies

1. **Constraints** - Limit what can be entered/selected
2. **Suggestions** - Guide toward correct input
3. **Defaults** - Provide smart starting values
4. **Confirmation** - Verify before destructive actions
5. **Validation** - Check input in real-time
6. **Affordances** - Make correct actions obvious

---

## Implementation Patterns

### Constraints

**Date input:**
```
Bad: Text field where user types date
Good: Date picker that only allows valid dates
```

**Quantity limits:**
```
Bad: Accept any number
Good: Min 1, max 99, +/- buttons
```

**Selection instead of input:**
```
Bad: "Enter country name"
Good: Dropdown of countries
```

### Smart Defaults

**Location:**
```
Detect user location, pre-fill country
```

**Dates:**
```
Today's date for current events
Next business day for shipping
```

**Forms:**
```
Remember previous selections
Suggest based on profile
```

### Inline Validation

**Real-time feedback:**
```
Email field:
✓ Format is valid
✗ Invalid format (show as user types)

Password field:
Requirements shown and checked as user types:
✓ 8+ characters
✗ One uppercase letter
✗ One number
```

### Confirmation Dialogs

**When to use:**
- Irreversible actions (permanent delete)
- Significant consequences (cancel subscription)
- Uncommon but impactful (bulk operations)

**When NOT to use:**
- Routine actions (saving a file)
- Easily reversible actions (moving to trash)
- Frequent operations (logging out)

**Good confirmation:**
```
Delete 47 items permanently?

This action cannot be undone. All selected files
will be permanently removed.

[Cancel] [Delete 47 Items]
```

### Format Guidance

**Phone numbers:**
```
Field shows format: (XXX) XXX-XXXX
Auto-formats as user types
Accepts various input formats
```

**Credit cards:**
```
Auto-detect card type
Show card type icon
Format with spaces
```

---

## Templates

### Error Prevention Audit

```markdown
# Error Prevention Audit: [Feature]

**Date:** [Date]
**Reviewer:** [Name]

## Form Fields Analysis

| Field | Input Type | Constraints | Validation | Default | Notes |
|-------|------------|-------------|------------|---------|-------|
| [Field] | [Type] | [Constraints] | [Timing] | [Default] | [Notes] |

## Destructive Actions

| Action | Confirmation? | Undo Available? | Risk Level | Recommendation |
|--------|---------------|-----------------|------------|----------------|
| [Action] | Y/N | Y/N | H/M/L | [Recommendation] |

## Common Error Points

| Error | Frequency | Root Cause | Prevention |
|-------|-----------|------------|------------|
| [Error] | [Count] | [Why] | [How to prevent] |

## Recommendations Priority

1. [High priority prevention]
2. [Medium priority prevention]
3. [Low priority prevention]
```

---

## Examples

### Good Examples

**Gmail compose:**
- "Did you mean to attach a file?" (detects "attached" without attachment)
- Warns about empty subject line
- Undo send option

**Google Forms:**
- Required fields clearly marked
- Validation before submission
- Field types constrain input

**Amazon checkout:**
- Address validation/suggestions
- Payment validation before order
- Clear shipping timeline

### Bad Examples

**No validation until submit:**
```
User fills long form
Clicks submit
All errors shown at once at top
User must find each error
```

**Accepting invalid data:**
```
User enters invalid email
System accepts it
Email confirmation fails later
User never knew email was wrong
```

---

## Prevention Techniques by Field Type

### Text Fields
- Character limits with counter
- Format hints and masks
- Auto-complete suggestions
- Real-time validation

### Numeric Fields
- Numeric keyboard on mobile
- Min/max constraints
- Increment buttons
- Format guidance (currency, etc.)

### Date Fields
- Date picker (not text input)
- Disable invalid dates
- Clear format display
- Relative dates (Today, Tomorrow)

### Selection Fields
- Default selection when appropriate
- Clear labels and descriptions
- Logical ordering
- Search for long lists

---

## Common Mistakes

1. **Validation only on submit** - User wastes time
2. **Too many confirmations** - Users dismiss without reading
3. **No constraints** - Accepting any input
4. **Unclear requirements** - User guesses what is needed
5. **Vague defaults** - Placeholders that confuse

---

## Measuring Effectiveness

| Metric | How to Measure |
|--------|----------------|
| Form abandonment | % users who start but do not finish |
| Validation errors | Errors caught before submission |
| Submission errors | Errors on form submit |
| Support tickets | "How do I..." questions |
| Task completion time | Faster = better prevention |

---

## Checklist

- [ ] Required fields clearly marked
- [ ] Input constraints (type, length, format) applied
- [ ] Real-time validation for important fields
- [ ] Smart defaults where appropriate
- [ ] Format guidance visible
- [ ] Confirmation for destructive actions
- [ ] Auto-formatting for structured data
- [ ] Suggestions and auto-complete where helpful

---

## References

- UX research community: 10 Usability Heuristics
- Forms that Work by Caroline Jarrett
- Defensive Design for the Web