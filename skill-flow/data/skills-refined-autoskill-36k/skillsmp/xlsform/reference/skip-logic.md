# Skip Logic Reference

Skip logic (also called "relevance" or "conditional logic") controls which questions appear based on previous answers. Use the `relevant` column in survey sheet.

## Basic Concept

The `relevant` column contains an XPath expression. If expression is true, question shows. If false, question is hidden.

```
| type | name | label | relevant |
| select_one yes_no | has_children | Do you have children? | |
| integer | num_children | How many children? | ${has_children} = 'yes' |
```

**If User Selects "yes":** Next question appears.
**If User Selects "no":** Next question hidden.

---

## Expression Syntax

### Reference Other Questions
Use `${question_name}` to reference another question's answer.

```
${age}              (the value of the age question)
${country}          (the selected country)
${num_children}     (the entered number)
```

### Comparison Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| = | Equal | `${age} = 18` |
| != | Not equal | `${gender} != 'male'` |
| > | Greater than | `${age} > 18` |
| >= | Greater than or equal | `${income} >= 5000` |
| < | Less than | `${age} < 65` |
| <= | Less than or equal | `${income} <= 10000` |

---

## Common Patterns

### Show if Specific Answer
```
relevant: ${has_children} = 'yes'

(Show only if user answered 'yes' to has_children)
```

### Show if Number Meets Condition
```
relevant: ${age} >= 18

(Show only if age is 18 or older)
```

### Show if Multiple Conditions Met
```
relevant: ${age} >= 18 and ${country} = 'USA'

(Show only if age >= 18 AND country = USA)
```

### Show if Either Condition Met
```
relevant: ${income_source} = 'salary' or ${income_source} = 'business'

(Show if either salary OR business income)
```

### Show if NOT Something
```
relevant: ${country} != 'USA'

(Show if country is not USA)
```

---

## Advanced Patterns

### Using Functions

#### selected()
Check if specific choice was selected.

```
relevant: selected(${languages}, 'english')

(Show if 'english' was checked in select_multiple)
```

#### count-selected()
Count how many items selected.

```
relevant: count-selected(${languages}) >= 2

(Show if 2+ languages selected)
```

#### string functions
```
relevant: string-length(${name}) > 0

(Show if name entered)
```

#### date functions
```
relevant: today() - ${dob} >= 6570

(Show if person at least 18 years old, ~6570 days)
```

---

## Complex Examples

### Nested Conditional Logic

```
| type | name | label | relevant |
| select_one yes_no | has_income | Do you have income? | |
| select_one income_type | income_type | Type of income? | ${has_income} = 'yes' |
| decimal | salary | Monthly salary | ${has_income} = 'yes' and ${income_type} = 'salary' |
| decimal | commission | Monthly commission | ${has_income} = 'yes' and ${income_type} = 'commission' |
| text | income_source | Other source | ${has_income} = 'yes' and ${income_type} = 'other' |
```

**Logic:**
1. Ask if has income
2. If yes, ask income type
3. If salary, ask salary amount
4. If commission, ask commission amount
5. If other, ask to specify

### Multi-Level Cascading

```
| type | name | label | relevant |
| select_one country | country | Country | |
| select_one region | region | Region | ${country} != '' |
| select_one district | district | District | ${region} != '' |
| select_one ward | ward | Ward | ${district} != '' |
```

**Logic:**
- Show region only if country selected
- Show district only if region selected
- Show ward only if district selected

### Hide Based on Calculation

```
| type | name | label | relevant |
| integer | price | Unit price | |
| integer | quantity | Quantity | |
| integer | total | Total | ${price} * ${quantity} > 0 |
```

(Show total only if both price and quantity entered)

---

## When Questions Are Hidden

If `relevant` is false:

| Behavior | Detail |
|----------|--------|
| **Not shown** | Question not displayed in form |
| **Not answered** | User can't input data |
| **No data stored** | No value recorded (empty) |
| **Not required** | Constraint/required column ignored |
| **Still referenceable** | Can still be used in other formulas |

**Note:** Questions hidden by `relevant` don't store data, even if they had previous values.

---

## Writing Good Relevant Expressions

### Do's
✓ Use clear variable names: `${num_children}` not `${x}`
✓ Comment complex logic for documentation
✓ Test all paths before deployment
✓ Use sensible defaults

### Don'ts
✗ Don't nest too many levels (hard to understand)
✗ Don't use `relevant` for validation (use `constraint`)
✗ Don't create circular dependencies
✗ Don't hide required answers

---

## Validation and Edge Cases

### Empty/Unanswered Questions
```
relevant: ${name} != ''

(Show if name field is not empty)
```

### Selecting Multiple Items

For `select_multiple` questions:
```
relevant: selected(${colors}, 'red') and selected(${colors}, 'blue')

(Show if both red AND blue selected)
```

### Exact Match vs Substring
```
${country} = 'USA'           (exact: USA only)
${country} != 'USA'          (not USA)
contains(${country}, 'United')  (contains substring)
```

---

## Performance Considerations

- Simple `relevant` expressions are fast
- Complex nested conditions are fine for most forms
- Avoid circular references: question A depends on B, B depends on A
- Very deeply nested (10+ levels) can slow forms slightly
- Test on actual devices before deployment

---

## Testing Skip Logic

**Before Deployment:**
1. Create test cases for each path
2. Test all conditional branches
3. Test rapid selection changes
4. Test empty/required field combinations
5. Test on actual mobile devices

**Example Test Cases:**
```
Test: has_children = yes
Expected: num_children question shows
Actual: ✓ Shows

Test: has_children = no
Expected: num_children question hidden
Actual: ✓ Hides

Test: age = 15, required_if_adult = (hidden)
Expected: Question not shown
Actual: ✓ Not shown
```

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `${variable name}` (space) | Parse error | Use underscore: `${variable_name}` |
| Missing quotes on text | Compare error | Use quotes: `${field} = 'yes'` |
| Case mismatch | Logic fails | Match exactly: `${gender} = 'Female'` |
| Typo in question name | Never shows | Verify name matches survey sheet |
| Too many nested conditions | Confusing | Simplify or break into steps |
| Circular dependency | Unpredictable | Avoid question A depends on B, B on A |

---

## Examples

### Healthcare Survey
```
| type | name | label | relevant |
| select_one yes_no | has_condition | Have chronic condition? | |
| select_one condition_type | condition | Type of condition? | ${has_condition} = 'yes' |
| text | medication | Medications taken | ${has_condition} = 'yes' |
| integer | visits_per_year | Doctor visits annually | ${has_condition} = 'yes' |
```

### Income Survey
```
| type | name | label | relevant |
| select_one yes_no | employed | Are you employed? | |
| decimal | monthly_salary | Monthly salary | ${employed} = 'yes' |
| select_one yes_no | has_other_income | Any other income? | |
| decimal | other_income | Amount of other income | ${has_other_income} = 'yes' |
```

### Education Survey
```
| type | name | label | relevant |
| select_one education_level | education | Education level | |
| text | school_name | School name | ${education} != 'none' |
| integer | graduation_year | Graduation year | selected(${education}, 'university') |
| text | field_of_study | Field of study | selected(${education}, 'university') |
```

### Demographic Survey
```
| type | name | label | relevant |
| integer | age | Age | |
| select_one marital_status | marital_status | Marital status | ${age} >= 18 |
| text | spouse_name | Spouse name | ${marital_status} = 'married' |
| integer | num_children | Number of children | ${marital_status} = 'married' |
```

---

## XPath Reference for Relevant

For complete XPath function reference, see [xpath-expressions.md](xpath-expressions.md).

Common functions in `relevant`:
- `selected()` - Check if choice selected
- `count-selected()` - Count selected items
- `string-length()` - Length of text
- `contains()` - Text contains substring
- `today()` - Current date
- Math operators: `+`, `-`, `*`, `/`
- Comparison: `=`, `!=`, `>`, `<`, `>=`, `<=`
- Logic: `and`, `or`, `not()`
