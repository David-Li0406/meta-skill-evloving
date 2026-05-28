# XPath Expressions Reference

XPath expressions are used in `relevant`, `constraint`, `calculation`, and `choice_filter` columns. This reference covers all common functions and operators.

## Basic Operators

### Arithmetic

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | Addition | `5 + 3` | 8 |
| `-` | Subtraction | `10 - 4` | 6 |
| `*` | Multiplication | `6 * 4` | 24 |
| `/` | Division | `20 / 4` | 5 |
| `mod` | Modulo (remainder) | `10 mod 3` | 1 |

### Comparison

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `=` | Equal | `5 = 5` | true |
| `!=` | Not equal | `5 != 3` | true |
| `<` | Less than | `3 < 5` | true |
| `>` | Greater than | `5 > 3` | true |
| `<=` | Less/equal | `5 <= 5` | true |
| `>=` | Greater/equal | `5 >= 3` | true |

### Logical

| Operator | Meaning | Example |
|----------|---------|---------|
| `and` | AND (both true) | `${age} > 18 and ${country} = 'USA'` |
| `or` | OR (either true) | `${gender} = 'M' or ${gender} = 'F'` |
| `not()` | NOT (negate) | `not(${hasChildren} = 'yes')` |

---

## String Functions

### concat()
Joins text strings together.

```
concat(${first_name}, ' ', ${last_name})
Result: "John Smith"

concat('Hello ', ${name})
Result: "Hello John"
```

### string-length()
Returns number of characters in text.

```
string-length(${name})
Result: 4 (for "John")

constraint: string-length(.) >= 5
(Require minimum 5 characters)
```

### substring()
Extracts part of text.

```
substring(${code}, 1, 3)
Result: First 3 characters of code

substring(${text}, 5)
Result: Text starting from position 5
```

### contains()
Checks if text contains substring.

```
contains(${country}, 'United')
Result: true if country contains "United"

relevant: contains(${description}, 'urgent')
(Show if description contains "urgent")
```

### starts-with()
Checks if text starts with substring.

```
starts-with(${code}, 'LAB')
Result: true if code starts with "LAB"
```

### translate()
Converts text (e.g., case conversion).

```
translate(${name}, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
Result: Converts to uppercase

translate(${name}, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')
Result: Converts to lowercase
```

---

## Number Functions

### round()
Rounds to nearest integer.

```
round(3.7)
Result: 4

round(3.2)
Result: 3

calculation: round(${total} * 100) / 100
Result: Round to 2 decimal places
```

### floor()
Rounds down.

```
floor(3.9)
Result: 3

calculation: floor((today() - ${dob}) / 365.25)
Result: Age in years (rounded down)
```

### ceiling()
Rounds up.

```
ceiling(3.1)
Result: 4
```

### sum()
Adds multiple values. Used mostly for display.

```
sum(${value1}, ${value2}, ${value3})
Result: Total of three values

calculation: sum(${price1}, ${price2}, ${price3})
```

### count()
Counts items in repeat group.

```
count(${household_members})
Result: Number of repeated members
```

### abs()
Absolute value (remove negative).

```
abs(-5)
Result: 5

abs(${difference})
```

---

## Selection Functions

### selected()
Checks if specific choice was selected (for select_multiple).

```
selected(${languages}, 'english')
Result: true if "english" checked

constraint: selected(${agreement}, 'accept')
(Require "accept" to be selected)
```

### count-selected()
Counts how many items selected (for select_multiple).

```
count-selected(${languages})
Result: 2 (if 2 languages selected)

constraint: count-selected(.) >= 2 and count-selected(.) <= 4
(Require 2-4 selections)
```

---

## Date/Time Functions

### today()
Returns today's date.

```
today()
Result: 2024-10-30

constraint: . <= today()
(Date cannot be future)
```

### now()
Returns current date and time.

```
now()
Result: 2024-10-30T14:30:45

calculation: now()
(Capture submission timestamp)
```

### date()
Converts text to date.

```
date('2024-12-25')
Result: Date value for Christmas 2024

constraint: . >= date('2024-01-01')
(Date must be on or after Jan 1, 2024)
```

### year()
Extracts year from date.

```
year(${birth_date})
Result: 2000

calculation: year(today())
Result: 2024
```

### month()
Extracts month from date.

```
month(${birth_date})
Result: 5 (for May)
```

### day()
Extracts day from date.

```
day(${birth_date})
Result: 15
```

### Date Arithmetic
Dates can be subtracted to get days difference.

```
today() - ${birth_date}
Result: Number of days since birth

constraint: today() - . >= 6570
Result: At least 18 years old (6570 days)

constraint: today() - . <= 27375
Result: Less than 75 years old (27375 days)
```

---

## Conditional Functions

### if()
Conditional: if condition true, return value1, else value2.

```
if(${age} >= 18, 'adult', 'minor')
Result: "adult" if age >= 18, else "minor"

calculation: if(${quantity} > 100, ${price} * 0.9, ${price})
Result: 10% discount if qty > 100, else regular price
```

### Nested if()
Multiple conditions.

```
if(${income} > 5000, 'high', if(${income} > 2000, 'medium', 'low'))
Result: Three-tier classification

if(${age} < 18, 'child', if(${age} < 65, 'adult', 'senior'))
Result: Age brackets
```

### true() / false()
Boolean constants.

```
if(${condition}, 'yes', false())
Result: "yes" or false

relevant: if(${type} = 'other', true(), false())
Result: Show if type equals "other"
```

---

## Regular Expression Functions

### regex()
Validates text against pattern.

```
regex(., '^[0-9]{10}$')
Result: true if field is exactly 10 digits

constraint: regex(., '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
(Email validation)
```

### Regex Patterns

| Pattern | Matches | Rejects |
|---------|---------|---------|
| `^[0-9]{10}$` | 1234567890 | 123456789, abc123 |
| `^\+?[0-9]{10,}$` | +1234567890 or 1234567890 | abc123 |
| `^[A-Z]{2}$` | US, KE, UG | USA, us |
| `^[a-z0-9_]*$` | username, user_123 | User-Name |
| `^[0-9]+\.[0-9]{2}$` | 10.50, 9.99 | 10.5, 10.505 |

---

## Field Reference

### Current Field
```
.
(In constraint/calculation - refers to field itself)

constraint: . >= 0
(Current field must be >= 0)
```

### Other Fields
```
${field_name}
(Reference another question's value)

relevant: ${has_children} = 'yes'
(Reference the has_children question)
```

---

## Practical Examples

### Age Validation
```
constraint: . >= 0 and . <= 150
constraint: today() - ${birth_date} >= 6570
(At least 18 years old)
```

### Email Validation
```
constraint: regex(., '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
```

### Phone Validation
```
constraint: regex(., '^\+?[1-9]\d{1,14}$')
(International phone format)
```

### Inventory Management
```
calculation: concat(${item_name}, ' (', ${quantity}, ' units)')
Result: "Apples (50 units)"
```

### Budget Status
```
calculation: if(${income} - ${expenses} > 0, 'surplus', 'deficit')
Result: "surplus" or "deficit"
```

### Discount Calculation
```
calculation: if(${quantity} > 100, ${price} * 0.9, ${price})
Result: 10% discount for 100+
```

### Age Grouping
```
calculation: if(${age} < 5, 'toddler', if(${age} < 13, 'child', if(${age} < 18, 'teen', 'adult')))
Result: Age category
```

### Text Manipulation
```
calculation: concat(translate(${last_name}, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), ', ', ${first_name})
Result: "SMITH, John"
```

### Confirm Match
```
constraint: . = ${password}
constraint_message: Passwords do not match
(For password confirmation field)
```

### Date Range
```
constraint: . >= date('2024-01-01') and . <= date('2024-12-31')
constraint_message: Must be in 2024
```

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `${field name}` (space) | Parse error | Use underscore: `${field_name}` |
| Missing quotes on text | Syntax error | Use quotes: `'text'` |
| `sum(${a} + ${b})` | Wrong result | Use: `${a} + ${b}` (not sum) |
| `contains(text)` without field | Error | Use: `contains(${field}, 'text')` |
| Division by zero | Error | Use: `if(${count} > 0, ${sum}/${count}, 0)` |
| Typo in function | Unknown function | Check spelling: `today()`, `sum()` |
| Circular reference | Error | Don't reference field from own calculation |
| Case mismatch | Logic fails | Be exact: `'yes'` not `'Yes'` |

---

## Performance Tips

- Simple expressions fast: `${age} > 18`
- Complex nested conditions: slower but acceptable for most forms
- Very long regex patterns: slightly slower
- Avoid circular references: X depends on Y, Y depends on X
- Test on actual device before deployment

---

## Testing Expressions

**Example Test Cases:**
```
Expression: ${age} >= 18
Test 1: age = 18, Result: true ✓
Test 2: age = 17, Result: false ✓
Test 3: age = 65, Result: true ✓

Expression: string-length(${password}) >= 8
Test 1: password = "Pass123", Result: false ✓
Test 2: password = "Password123", Result: true ✓

Expression: regex(., '^\d{10}$')
Test 1: Input = "1234567890", Result: true ✓
Test 2: Input = "12345", Result: false ✓
Test 3: Input = "abc1234567", Result: false ✓
```

---

## See Also

- [skip-logic.md](skip-logic.md) - Using expressions in `relevant`
- [calculations.md](calculations.md) - Using expressions in `calculation`
- [constraints.md](constraints.md) - Using expressions in `constraint`
- [cascading-selects.md](cascading-selects.md) - Using expressions in `choice_filter`
