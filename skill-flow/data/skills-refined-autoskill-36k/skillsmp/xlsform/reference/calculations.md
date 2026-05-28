# Calculations Reference

Calculations compute values based on other fields. Use the `calculate` question type for hidden fields or the `calculation` column for visible fields.

## Two Ways to Calculate

### 1. calculate Question Type (Hidden)
Hidden field computed from other answers. Not displayed to user, not editable.

```
| type | name | label | calculation |
| integer | price | Unit price | |
| integer | quantity | Quantity | |
| calculate | total | | ${price} * ${quantity} |
```

**Result:** User enters price and quantity. Total auto-computed, hidden, stored in data.

### 2. calculation Column (Visible)
Visible calculated field shown to user as a display value.

```
| type | name | label | calculation |
| integer | price | Unit price | |
| integer | quantity | Quantity | |
| integer | total | Total (calculated) | ${price} * ${quantity} |
```

**Result:** User sees computed total value below quantity field.

---

## Common Formulas

### Math Operations

#### Addition
```
calculation: ${field1} + ${field2}
result: 10 + 5 = 15
```

#### Subtraction
```
calculation: ${income} - ${expenses}
result: 1000 - 200 = 800
```

#### Multiplication
```
calculation: ${price} * ${quantity}
result: 10 * 5 = 50
```

#### Division
```
calculation: ${total} / ${count}
result: 100 / 4 = 25
```

#### Percentage
```
calculation: ${price} * 1.1
result: 100 * 1.1 = 110 (10% increase)

calculation: ${price} * 0.9
result: 100 * 0.9 = 90 (10% discount)

calculation: ${price} * ${tax_percent} / 100
result: 100 * 15 / 100 = 15 (15% tax)
```

---

### Text Operations

#### Concatenation (Join Text)
```
calculation: concat(${first_name}, ' ', ${last_name})
result: concat('John', ' ', 'Smith') = 'John Smith'
```

#### String Length
```
calculation: string-length(${name})
result: string-length('John') = 4
```

#### Substring
```
calculation: substring(${code}, 1, 3)
result: substring('ABC123', 1, 3) = 'ABC'
```

#### Uppercase/Lowercase
```
calculation: translate(${name}, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
result: Converts to uppercase
```

---

### Date Operations

#### Current Date
```
calculation: today()
result: 2024-10-30
```

#### Current DateTime
```
calculation: now()
result: 2024-10-30T14:30:45
```

#### Date Arithmetic
```
calculation: ${date1} - ${date2}
result: Difference in days

calculation: today() - ${dob}
result: Age in days (divide by 365.25 for years)
```

#### Get Date Part
```
calculation: year(${date})
result: 2024

calculation: month(${date})
result: 10

calculation: day(${date})
result: 30
```

---

### Conditional Calculations

#### If/Then/Else
```
calculation: if(${quantity} > 100, ${price} * 0.9, ${price})
result: 10% discount if quantity > 100, else regular price

calculation: if(${age} >= 18, 'adult', 'minor')
result: Returns text based on condition
```

#### Nested Conditions
```
calculation: if(${income} > 5000, 'high', if(${income} > 2000, 'medium', 'low'))
result: Three-tier income classification
```

---

### Aggregate Functions

#### Sum
```
calculation: sum(${field1}, ${field2}, ${field3})
result: ${field1} + ${field2} + ${field3}

calculation: ${quantity1} * ${price1} + ${quantity2} * ${price2}
result: Multiple items total
```

#### Average
```
calculation: (${value1} + ${value2} + ${value3}) / 3
result: Average of three values
```

#### Min/Max
```
calculation: min(${value1}, ${value2}, ${value3})
result: Smallest value

calculation: max(${value1}, ${value2}, ${value3})
result: Largest value
```

---

### Logical Functions

#### Count Selected Items
```
calculation: count-selected(${languages})
result: 2 (if user selected 2 languages)
```

#### Check if Selected
```
calculation: if(selected(${hobbies}, 'reading'), 'likes reading', 'no reading')
result: Check if specific choice selected
```

#### Not
```
calculation: if(not(${has_children} = 'yes'), 'no children', 'has children')
result: Logical negation
```

---

## Real-World Examples

### Budget Calculator
```
| type | name | label | calculation |
| integer | income | Monthly income |
| integer | rent | Rent | |
| integer | food | Food | |
| integer | utilities | Utilities | |
| integer | other | Other expenses | |
| calculate | total_expenses | | ${rent} + ${food} + ${utilities} + ${other} |
| calculate | remaining | | ${income} - total_expenses |
| note | balance | Balance: ${remaining} | |
```

### Tax Calculator
```
| type | name | label | calculation |
| decimal | subtotal | Subtotal | |
| decimal | tax_rate | Tax rate (%) | 15 |
| calculate | tax | | ${subtotal} * ${tax_rate} / 100 |
| calculate | total | | ${subtotal} + ${tax} |
```

### Age Calculator
```
| type | name | label | calculation |
| date | dob | Birth date | |
| calculate | age_years | | floor((today() - ${dob}) / 365.25) |
| calculate | age_days | | today() - ${dob} |
```

### Household Census
```
| type | name | label | calculation |
| begin repeat | members | Household members | |
| text | member_name | Name | |
| integer | age | Age | |
| end repeat | | |
| calculate | hh_count | | count(${members}) |
| calculate | avg_age | | sum(${members}/age) / ${hh_count} |
```

### Discount Calculator
```
| type | name | label | calculation |
| decimal | original_price | Original price | |
| select_one discount_type | discount_type | Discount type | |
| decimal | discount_amount | Discount | |
| calculate | final_price | | if(${discount_type} = 'percent', ${original_price} * (1 - ${discount_amount}/100), ${original_price} - ${discount_amount}) |
```

---

## Calculation Syntax Rules

### Variable Reference
```
${variable_name}   (reference another question)
${variable_name} + 10
```

### Operators
```
+ - * / %         (math)
= != > < >= <=    (comparison)
and or not()      (logic)
( )               (grouping)
```

### Functions
```
sum()           (add values)
concat()        (join text)
if()            (conditional)
today()         (current date)
now()           (current datetime)
floor()         (round down)
round()         (round to nearest)
string-length() (text length)
selected()      (check choice)
count-selected()(count choices)
```

### String Literals
```
'text string'   (use single quotes for text)
"also works"    (double quotes also ok)
```

---

## Performance and Limits

| Aspect | Limit | Notes |
|--------|-------|-------|
| Expression length | ~2000 chars | Very long formulas slow form |
| Nesting depth | 10+ levels | Deeply nested can be slow |
| Functions per formula | No limit | But performance degrades with many |
| Decimal precision | 15+ digits | Device-dependent |
| Date range | 1900-2100 | Most platforms support this |

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `${field name}` (space) | Parse error | Use underscore: `${field_name}` |
| Missing quotes on text | Parse error | Use quotes: `if(..., 'text', ...)` |
| `sum(${a} + ${b})` | Wrong result | Use: `${a} + ${b}` or `sum(${a}, ${b})` |
| Division by zero | Error | Use conditional: `if(${count} > 0, ${sum}/${count}, 0)` |
| Typo in function | Unknown function | Check spelling: `today()` not `Today()` |
| Circular reference | Error | Don't reference a field from its own calculation |
| No decimal for float | Integer result | Use `${value} * 1.0` to force decimal |

---

## Testing Calculations

**Before Deployment:**
1. Test with various input values
2. Test edge cases (zero, negative, large numbers)
3. Test with empty/missing fields
4. Verify decimal precision
5. Test on actual mobile device

**Example Test Cases:**
```
Input: price=100, quantity=2
Expected: total = 200
Actual: ✓ 200

Input: price=100, quantity=0
Expected: total = 0
Actual: ✓ 0

Input: price=0, quantity=100
Expected: total = 0
Actual: ✓ 0

Input: price=-10 (negative)
Expected: total = -100 or error
Actual: [Device-dependent]
```

---

## Advanced: Using Repeat Group Calculations

```
| type | name | label | calculation |
| begin repeat | purchases | Purchases | |
| text | item_name | Item | |
| integer | quantity | Quantity | |
| decimal | unit_price | Unit price | |
| calculate | item_total | | ${quantity} * ${unit_price} |
| end repeat | | |
| calculate | grand_total | | sum(${purchases}/item_total) |
```

**Logic:**
- Each repeat calculates item_total
- Grand total sums all item_totals

---

## See Also

- [xpath-expressions.md](xpath-expressions.md) - Complete function reference
- [skip-logic.md](skip-logic.md) - Using `relevant` with conditions
- [constraints.md](constraints.md) - Validation formulas
