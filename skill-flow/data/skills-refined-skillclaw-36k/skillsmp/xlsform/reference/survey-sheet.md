# Survey Sheet Reference

The survey worksheet defines all questions, their types, labels, and behavior. This is the main worksheet in any XLSForm.

## Required Columns

Every survey worksheet must have these three columns:

### type
Question type (text, integer, select_one, etc.). Determines input method and data storage.

**Rules:**
- Must be valid XLSForm question type
- Some types require parameters: `select_one list_name`, `select_multiple list_name`, `begin repeat`, `end repeat`, `begin group`, `end group`
- Case-sensitive: `text` (valid), `Text` (error)

**Examples:**
```
text
integer
select_one gender
select_multiple languages
calculate
note
geopoint
image
```

**Invalid Examples:**
```
Text (wrong case)
select (missing list_name)
number (should be integer or decimal)
question (not a valid type)
```

---

### name
Unique variable identifier for the question. Used in data storage, expressions, and code.

**Rules:**
- Alphanumeric characters + underscore only
- Cannot start with number
- Cannot contain spaces, special characters, or unicode
- Max 255 characters
- Unique within the form (no duplicates)
- Case-sensitive: `age`, `Age`, `AGE` are three different names

**Valid Examples:**
```
respondent_name
age
q1_gender
num_children_under_5
has_electricity
```

**Invalid Examples:**
```
respondent-name (hyphen not allowed)
respondent name (space not allowed)
respondent'name (apostrophe not allowed)
2q_age (can't start with number)
respondent@name (special character not allowed)
```

**Data Reference:**
Question names are used in expressions and calculations:
```
relevant: ${age} >= 18
calculation: ${price} * ${quantity}
choice_filter: choice_filter in ${country}
```

---

### label
Question text displayed to users. Can include unicode, special characters, emoji.

**Rules:**
- Can be any text, any language
- Displayed on mobile/web
- Supports translation via `label::language` columns
- Can reference other questions: `You are ${age} years old`
- Can include line breaks (Excel cell → Wrap text)
- No hard character limit, practical max ~500 chars

**Examples:**
```
What is your name?
Age in years
Do you have children?
Marque los servicios disponibles:
نام خود را وارد کنید
```

**Dynamic Labels:**
```
Label text: You are ${age} years old
Label text: Select your ${country} province:
```

---

## Optional Columns

### hint
Helpful text displayed below label (clarification, example, instruction).

**Rules:**
- Smaller text than label
- Often gray/muted in display
- Can reference other questions
- Supports translation: `hint::language`
- Good for examples and clarification

**Examples:**
```
Please provide your full name
Enter age in completed years
e.g., john@example.com
Utilisez le format YYYY-MM-DD
```

**Use When:**
- Label needs clarification
- Example format helps: "YYYY-MM-DD"
- Special instructions: "Press home to stop recording"
- Don't use: if label is clear and self-explanatory

---

### relevant
Controls visibility: question appears only if condition is true.

**Rules:**
- XPath expression (see [xpath-expressions.md](xpath-expressions.md))
- References other questions: `${variable_name}`
- Empty/missing = always visible
- Expressions are case-sensitive

**Common Patterns:**
```
${previous_question} = 'yes'
${age} >= 18 and ${age} <= 65
selected(${languages}, 'english')
${income} > 0
```

**When Question Hidden:**
- Not shown in form
- Not required/validated
- No data stored (unless data pre-filled)
- Can still be referenced in other expressions

---

### required
Whether question must be answered before proceeding.

**Values:**
```
yes        (required, must answer)
no         (optional, can skip)
(empty)    (optional, same as 'no')
${condition}  (conditionally required)
```

**Examples:**
```
| type | name | label | required |
| text | name | Full name | yes |
| select_one | country | Country | yes |
| text | middlename | Middle name | no |
| integer | num_children | Children | ${has_children} = 'yes' |
```

**Conditional Required:**
```
required: ${household_members} > 0
(require input only if household has members)
```

---

### constraint
Validation rule. Answer must satisfy expression to proceed.

**Rules:**
- XPath expression
- `.` refers to current field value
- Empty = no validation
- Shows error on invalid answer
- Must include `constraint_message`

**Common Patterns:**
```
. >= 0                         (non-negative)
. >= 0 and . <= 100            (range 0-100)
. <= today()                   (not in future)
regex(., '^\d{10}$')           (10-digit number)
selected(., 'option')          (contains option)
```

**Full Example:**
```
| type | name | label | constraint | constraint_message |
| integer | age | Age | . >= 0 and . <= 150 | Age must be 0-150 |
| date | dob | Birth date | . <= today() | Date cannot be future |
| text | email | Email | .regex(., '^[^@]+@[^@]+\.[^@]+$') | Invalid email |
```

---

### constraint_message
Error message displayed when constraint fails.

**Rules:**
- Only used if `constraint` column present
- Should explain why answer invalid (user-friendly)
- Empty message = generic error
- Can reference field: `Age must be between 0 and ${max_age}`

**Best Practices:**
```
✓ Bad: Age must be 0-150
✗ Bad: Constraint failed
✓ Good: Please enter an age between 0 and 150 years
✓ Good: Email must be in format: name@example.com
✓ Good: Date cannot be in the future
```

---

### calculation
Formula computed from other fields. Visible on display.

**Rules:**
- For regular questions (text, integer, etc.)
- `.` in context of display, not a required field
- Result shown to user
- Use `calculate` type for hidden calculations

**Example:**
```
| type | name | label | calculation |
| integer | price | Unit price |
| integer | quantity | Quantity |
| integer | total | Total | ${price} * ${quantity} |
```

**Common Formulas:**
```
${field1} + ${field2}          (sum)
${field1} * ${field2} / 100    (percentage)
${price} * 1.15                (with tax)
if(${condition}, A, B)         (conditional)
round(${value}, 2)             (rounding)
concat(${first}, ' ', ${last}) (combine text)
```

---

### default
Pre-filled value for question. User can override.

**Rules:**
- Can be text, number, or expression
- Expression: `${variable_name}` or functions like `now()`, `today()`
- Used for initial load, not recalculated
- Not stored permanently if question not visible

**Examples:**
```
| type | name | label | default |
| text | country | Country | Kenya |
| hidden | form_version | | 2.5 |
| date | survey_date | Today's date | today() |
| dateTime | start_time | Start time | now() |
| text | enumerator | Enumerator | ${auth_username} |
```

---

### appearance
Customizes input widget/display method.

**Rules:**
- Question type specific
- Multiple values separated by space: `appearance: multiline new`
- See [appearances.md](appearances.md) for full reference

**Examples:**
```
| type | name | label | appearance |
| text | description | Description | multiline |
| select_one | country | Country | vertical |
| image | photo | Photo | new |
| geopoint | location | Location | maps |
```

---

### repeat_count
Limits number of repeats in repeat group (optional).

**Rules:**
- Used in `begin repeat` row
- Can be number or expression
- Limits how many times user can repeat

**Example:**
```
| type | name | label | repeat_count |
| begin repeat | children | Children | 10 |
| text | child_name | Name |
| end repeat | | |

(User can add max 10 children)
```

**Dynamic Limit:**
```
repeat_count: ${num_children}
(User specifies number, then repeats that many times)
```

---

### choice_filter
Filters choice list based on another field. Used for cascading selects.

**Rules:**
- For `select_one` and `select_multiple` types
- XPath expression filtering choices worksheet
- Choices worksheet must have filtering column
- See [cascading-selects.md](cascading-selects.md) for full examples

**Example:**
```
| type | name | label | choice_filter |
| select_one country | country | Country |
| select_one province | province | Province | province in ${country} |

Choices worksheet has 'country' column matching country names.
```

---

### read_only
Makes question display-only, not editable.

**Rules:**
- Values: `yes` (read-only), `no` or empty (editable)
- User can see value but cannot change
- Useful for displaying calculated results or audit fields

**Example:**
```
| type | name | label | read_only |
| calculate | timestamp | Submitted at | yes |
| text | country | Country | yes |
```

---

## Optional Multilingual Columns

### label::language
Translated label for specific language.

**Rules:**
- Format: `label::` + language code (en, fr, es, sw, etc.)
- One column per language
- Device user selects language; sees matching `label::language`
- Include base `label` column as fallback

**Example:**
```
| label | label::en | label::fr | label::es |
| What is your name? | What is your name? | Quel est votre nom? | ¿Cuál es su nombre? |
```

### hint::language
Translated hint for specific language.

**Example:**
```
| hint | hint::en | hint::fr |
| Please provide full name | Please provide full name | Veuillez fournir le nom complet |
```

---

## Column Organization

**Recommended column order:**
1. type
2. name
3. label (or `label` + `label::languages`)
4. hint (or `hint` + `hint::languages`)
5. relevant
6. required
7. constraint
8. constraint_message
9. calculation
10. choice_filter
11. appearance
12. default
13. repeat_count
14. read_only

**Notes:**
- Column order doesn't matter to XLSForm parser
- Logical order helps human reading and maintenance
- Delete unused columns to reduce clutter

---

## Special Row Types

### type: begin repeat
Starts a repeating section.

```
| type | name | label | repeat_count |
| begin repeat | household_members | Household members | 20 |
```

### type: end repeat
Ends a repeating section.

```
| type | name | label |
| end repeat | |  |
```

### type: begin group
Starts a grouped section (visual organization).

```
| type | name | label | appearance |
| begin group | demographics | Demographics | field-list |
```

### type: end group
Ends a grouped section.

```
| type | name | label |
| end group | | |
```

---

## Row Limits and Best Practices

| Aspect | Limit | Notes |
|--------|-------|-------|
| Max questions | No hard limit | 500+ questions = slow forms |
| Max label length | ~500 chars | Practical limit for mobile display |
| Max name length | 255 chars | Rare in practice |
| Max hint length | ~300 chars | Practical limit |
| Max nested repeats | 5+ levels | Becomes complex beyond 2-3 levels |
| Max repeat count | ~100-200 | Device memory, performance limits |
| Max choice lists | ~5000 choices | Practical limit, consider file-based |

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Name has spaces | Parse error | Use underscores: `first_name` |
| Name starts with number | Parse error | Start with letter: `q1_age` |
| Duplicate names | Only first used | Rename to unique values |
| `select_one` without `list_name` | Parse error | Use format: `select_one gender` |
| `${variable_name}` in label | Not replaced | Variables only work in calculations |
| Missing `constraint_message` | Cryptic error | Always include message with constraint |
| Nested repeats 3+ levels | Complex logic | Flatten or reconsider structure |
| Very large choice lists | Slow form | Use `select_one_from_file` for 1000+ |

---

## Examples

### Simple Survey
```
| type | name | label | required |
| text | name | Full name | yes |
| integer | age | Age | yes |
| select_one gender | gender | Gender | yes |
```

### With Skip Logic
```
| type | name | label | relevant | required |
| select_one | has_income | Do you have income? | | yes |
| decimal | income | Monthly income | ${has_income} = 'yes' | ${has_income} = 'yes' |
```

### With Calculations
```
| type | name | label | constraint | calculation |
| decimal | price | Unit price | . > 0 |
| integer | quantity | Quantity | . > 0 |
| decimal | total | Total (calc) | | ${price} * ${quantity} |
```

### With Multilingual Support
```
| type | name | label::en | label::fr | hint::en | hint::fr |
| text | name | What is your name? | Quel est votre nom? | Full name | Nom complet |
```
