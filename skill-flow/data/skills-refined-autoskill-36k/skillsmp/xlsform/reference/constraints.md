# Constraints Reference

Constraints enforce validation rules. The `constraint` column contains an XPath expression that must be true for the answer to be accepted.

## Basic Syntax

The `.` refers to the current field's value.

```
| type | name | label | constraint | constraint_message |
| integer | age | Age | . >= 0 and . <= 150 | Age must be 0-150 |
```

**If user enters:** 25 → True, accepted.
**If user enters:** 200 → False, error message shown.

---

## Common Constraint Patterns

### Numeric Ranges

#### Non-negative
```
constraint: . >= 0
constraint_message: Must be a positive number
```

#### Range
```
constraint: . >= 0 and . <= 100
constraint_message: Must be between 0 and 100
```

#### Greater Than Threshold
```
constraint: . > 100
constraint_message: Must be more than 100
```

#### Less Than Maximum
```
constraint: . < 1000
constraint_message: Must be less than 1000
```

---

### Text Validation

#### Required (Not Empty)
```
constraint: . != ''
constraint_message: This field is required

(Or use required: yes column instead)
```

#### Specific Length
```
constraint: string-length(.) = 10
constraint_message: Must be exactly 10 characters
```

#### Min/Max Length
```
constraint: string-length(.) >= 5 and string-length(.) <= 50
constraint_message: Must be 5-50 characters
```

#### Phone Number Format
```
constraint: regex(., '^\+?[0-9]{10,15}$')
constraint_message: Please enter a valid phone number
```

#### Email Format
```
constraint: regex(., '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
constraint_message: Please enter a valid email address
```

#### Alphanumeric Only
```
constraint: regex(., '^[A-Za-z0-9]*$')
constraint_message: Only letters and numbers allowed
```

---

### Date Validation

#### Not in Future
```
constraint: . <= today()
constraint_message: Date cannot be in the future
```

#### Not in Past
```
constraint: . >= today()
constraint_message: Date cannot be in the past
```

#### Within Date Range
```
constraint: . >= date('2024-01-01') and . <= date('2024-12-31')
constraint_message: Must be in 2024
```

#### Minimum Age
```
constraint: today() - . >= 6570
constraint_message: Must be at least 18 years old (6570 days)
```

#### Maximum Age
```
constraint: today() - . <= 27375
constraint_message: Must be younger than 75 (27375 days)
```

---

### Selection Validation

#### At Least One Selected
```
constraint: count-selected(.) > 0
constraint_message: Please select at least one option
```

#### Exactly N Items Selected
```
constraint: count-selected(.) = 3
constraint_message: Must select exactly 3 options
```

#### Between N Items
```
constraint: count-selected(.) >= 2 and count-selected(.) <= 4
constraint_message: Select 2-4 options
```

#### Specific Choice Required
```
constraint: selected(., 'agree')
constraint_message: You must agree to proceed
```

---

### Cross-Field Validation

#### Compare With Another Field
```
| type | name | label | constraint |
| integer | min_value | Minimum |
| integer | max_value | Maximum | . >= ${min_value} |

(max_value must be >= min_value)
```

#### Price vs Quantity
```
| type | name | label | constraint |
| integer | unit_price | Unit price | . >= 0 |
| integer | quantity | Quantity | . >= 0 |
| decimal | total | Total | . = ${unit_price} * ${quantity} |

(Total must equal price * quantity)
```

#### Confirm Match
```
| type | name | label | constraint |
| text | password | Password |
| text | confirm_password | Confirm password | . = ${password} |

(Second password must match first)
```

---

## Regex (Regular Expression) Patterns

### Format

```
regex(., 'pattern')
```

The `.` is the field value. The pattern is a regex.

### Common Patterns

#### 10-Digit Phone
```
regex(., '^[0-9]{10}$')
Matches: 1234567890
Rejects: 123456789, 12345678901
```

#### International Phone
```
regex(., '^\+?[1-9]\d{1,14}$')
Matches: +12125551234, 2125551234
```

#### Email
```
regex(., '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
Matches: user@example.com
Rejects: user@.com, @example.com
```

#### URL
```
regex(., '^https?://.+\..+$')
Matches: http://example.com, https://example.com
```

#### Username (Alphanumeric, underscore)
```
regex(., '^[a-zA-Z0-9_]{3,20}$')
Matches: john_doe, user123
Rejects: ab (too short), user-name (hyphen)
```

#### 3-Letter Country Code
```
regex(., '^[A-Z]{3}$')
Matches: USA, KEN, FRA
Rejects: US, USAA
```

#### Numeric Only
```
regex(., '^[0-9]*$')
Matches: 12345
Rejects: 123a45
```

#### Decimal (2 places)
```
regex(., '^[0-9]+\.[0-9]{2}$')
Matches: 10.50, 9.99
Rejects: 10.5, 10.505
```

---

## Advanced Patterns

### Conditional Constraints

```
constraint: if(${type} = 'other', string-length(.) > 5, true())
constraint_message: When type is "other", specify details (min 5 chars)

(Constraint only active if type = 'other')
```

### Department-Specific Validation

```
constraint: if(${department} = 'engineering', . >= 50, true())
constraint_message: Engineers must have at least 50 salary units
```

### Age-Based Validation

```
constraint: if(${age} < 18, . <= 100, true())
constraint_message: Minors can earn max 100
```

---

## Best Practices

### Always Include constraint_message
✓ Good user experience
✓ Users understand why input rejected
✓ Reduces support questions

```
constraint: . >= 0 and . <= 100
constraint_message: Please enter a number between 0 and 100
```

### Validation vs Skip Logic

| Use Case | Use... |
|----------|--------|
| Hide question based on answer | `relevant` (skip logic) |
| Validate answer format | `constraint` |
| Make field mandatory | `required` |
| Require if condition met | `required: ${condition}` |

### Keep Messages Clear

✓ Good:
```
constraint_message: Date must be in format YYYY-MM-DD
constraint_message: Price must be between $0 and $10,000
constraint_message: Phone must be 10 digits
```

✗ Poor:
```
constraint_message: Invalid input
constraint_message: Constraint failed
constraint_message: Error in field
```

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Missing `constraint_message` | Generic error | Always include message |
| `.` not in constraint | Wrong syntax | Use `.` for current field |
| Quotes wrong in regex | Parse error | Use single quotes: `regex(., '^...$')` |
| Too strict constraint | Users frustrated | Test practical values |
| Circular validation | Impossible to satisfy | Don't validate against its own calc |
| Wrong operator | Logic fails | Verify: `=`, `!=`, `>`, `<`, `>=`, `<=` |

---

## Testing Constraints

**Before Deployment:**
1. Test valid values pass
2. Test invalid values rejected
3. Test edge cases (0, negative, very large)
4. Test empty/null values
5. Verify message displays correctly
6. Test on actual mobile device

**Example Test Cases:**
```
Constraint: . >= 0 and . <= 100
constraint_message: Enter 0-100

Test: 50
Expected: Pass
Actual: ✓ Pass

Test: 101
Expected: Fail, show message
Actual: ✓ Fails, message shows

Test: -1
Expected: Fail, show message
Actual: ✓ Fails, message shows

Test: (empty)
Expected: Pass (not required)
Actual: ✓ Pass
```

---

## Performance Notes

- Constraints evaluated when user moves to next question
- Simple constraints fast (`.` > 10)
- Complex regex slightly slower
- Very long constraints (1000+ chars) rare and slow
- Test on actual devices for performance

---

## See Also

- [xpath-expressions.md](xpath-expressions.md) - Complete function reference
- [skip-logic.md](skip-logic.md) - Using `relevant` for conditional display
- [calculations.md](calculations.md) - Using formulas
