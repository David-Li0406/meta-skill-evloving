# Form Logic

Control form behavior with relevance, constraints, calculations, and defaults.

## Variables and References

Reference previous answers using `${question_name}` syntax:

```
${age} >= 18
${first_name} + " " + ${last_name}
```

### Path References

| Reference | Description |
|-----------|-------------|
| `.` | Current question value |
| `..` | Parent group |
| `/data/group/question` | Absolute path |
| `${question_name}` | Named reference |

---

## Required Fields

| Column | Value | Description |
|--------|-------|-------------|
| `required` | `yes` | Always required |
| `required` | `${condition}` | Conditionally required |
| `required_message` | Custom text | Error message |

### Examples

| type | name | label | required | required_message |
|------|------|-------|----------|------------------|
| text | email | Email | yes | Please enter email |
| text | phone | Phone | ${contact_method}='phone' | Required for phone contact |

---

## Relevance (Skip Logic)

Show/hide questions based on conditions using the `relevant` column.

### Basic Patterns

```
${field} = 'value'              # Exact match
${field} != 'value'             # Not equal
${field} > 10                   # Numeric comparison
${field} != ''                  # Field is not empty
${field} = ''                   # Field is empty
```

### Select Questions

```
selected(${multi_select}, 'option')  # Check if option selected
not(selected(${field}, 'none'))      # None not selected
count-selected(${field}) > 0         # At least one selected
```

### Combined Conditions

```
${age} >= 18 and ${consent} = 'yes'
${status} = 'active' or ${status} = 'pending'
not(${excluded} = 'yes')
```

### Example

| type | name | label | relevant |
|------|------|-------|----------|
| select_one yes_no | has_children | Do you have children? | |
| integer | num_children | How many children? | ${has_children} = 'yes' |
| begin_group | child_info | Child Information | ${has_children} = 'yes' |

---

## Constraints (Validation)

Validate responses using the `constraint` column. Use `.` for current value.

### Numeric Constraints

```
. >= 0                     # Non-negative
. >= 0 and . <= 120       # Age range
. > ${min_value}          # Greater than another field
```

### Text Constraints

```
string-length(.) >= 10                    # Minimum length
string-length(.) <= 100                   # Maximum length
regex(., '[A-Z]{2}[0-9]{6}')             # Pattern match
regex(., '[^@]+@[^@]+\.[^@]+')           # Email format
regex(., '^\+?[0-9]{10,15}$')            # Phone format
```

### Date Constraints

```
. <= today()                              # Not in future
. >= today()                              # Not in past
. >= date('2020-01-01')                   # After specific date
. >= ${start_date}                        # After another date
```

### GPS Constraints

```
selected-at(${geopoint}, 3) < 10         # Accuracy under 10m
```

### Example

| type | name | label | constraint | constraint_message |
|------|------|-------|------------|-------------------|
| integer | age | Age | . >= 0 and . <= 120 | Age must be 0-120 |
| text | email | Email | regex(., '[^@]+@[^@]+\.[^@]+') | Invalid email |
| date | dob | Birth Date | . <= today() | Cannot be future |

---

## Calculations

Use `calculate` type for computed values.

### Basic Calculations

| type | name | calculation |
|------|------|-------------|
| calculate | full_name | concat(${first_name}, ' ', ${last_name}) |
| calculate | bmi | ${weight} div (${height} * ${height}) |
| calculate | age_years | int((today() - ${dob}) div 365.25) |
| calculate | total | ${item1} + ${item2} + ${item3} |

### Conditional Calculations

```
if(${condition}, 'value_if_true', 'value_if_false')
if(${age} >= 18, 'adult', 'minor')
```

### Handling Empty Values

```
coalesce(${field}, 0)                    # Default to 0
if(${field} != '', ${field}, 0)          # Conditional default
```

---

## Default Values

### Static Defaults

| type | name | label | default |
|------|------|-------|---------|
| text | country | Country | Kenya |
| integer | quantity | Quantity | 1 |

### Dynamic Defaults

| type | name | label | default |
|------|------|-------|---------|
| date | visit_date | Visit Date | today() |
| text | enumerator | Enumerator | ${username} |
| dateTime | timestamp | Timestamp | now() |

### Last-Saved Defaults

Reference values from the previous submission:

| type | name | label | default |
|------|------|-------|---------|
| text | village | Village | ${last-saved#village} |
| text | district | District | ${last-saved#district} |

---

## Trigger (Recalculation)

Force recalculation when a specific field changes:

| type | name | calculation | trigger |
|------|------|-------------|---------|
| calculate | updated_at | now() | ${important_field} |
| calculate | status_changed | now() | ${status} |

---

## Read-Only Fields

Prevent editing with `readonly` column:

| type | name | label | readonly | default |
|------|------|-------|----------|---------|
| text | patient_id | Patient ID | yes | concat('P', format-date(today(), '%Y%m%d'), '-', random()) |
| calculate | calculated_field | | yes | ${a} + ${b} |

---

## Soft Constraints (Warnings)

Use note questions with relevance for non-blocking warnings:

| type | name | label | relevant |
|------|------|-------|----------|
| integer | age | Age | |
| note | age_warning | Warning: Age seems unusually high | ${age} > 100 |

---

## Common Logic Patterns

### Age-Based Relevance

```
${age} < 5                    # Under 5
${age} >= 5 and ${age} < 18   # Child 5-17
${age} >= 18                  # Adult
${age} >= 65                  # Senior
```

### Gender-Specific Questions

```
${sex} = 'female'
${sex} = 'female' and ${age} >= 15 and ${age} <= 49  # WRA
```

### Pregnancy-Related

```
${sex} = 'female' and ${pregnant} = 'yes'
${pregnant} = 'yes' and ${weeks_pregnant} >= 28
```

### Date Window

```
. >= today() - 7              # Within last week
. >= today() - 30             # Within last month
(today() - .) <= 365          # Within last year
```
