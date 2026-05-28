# Quick Reference

Common patterns, formulas, and cheat sheets.

## Common Calculations

### Age

```
# Age in years
int((today() - ${dob}) div 365.25)

# Age in months
int((today() - ${dob}) div 30.4375)

# Age in days
today() - ${dob}
```

### Names

```
# Full name
concat(${first_name}, ' ', ${last_name})

# With middle name
concat(${first_name}, ' ', coalesce(${middle_name}, ''), ' ', ${last_name})
```

### BMI

```
# Height in cm, weight in kg
round(${weight} div (${height} div 100 * ${height} div 100), 1)

# Height in m
round(${weight} div (${height} * ${height}), 1)
```

### EDD (Estimated Delivery Date)

```
# From LMP
${lmp_date} + 280

# CHT function
add-date(${lmp_date}, 0, 9, 0, 0, 0)
```

### Gestational Age

```
# Weeks pregnant
int((today() - ${lmp_date}) div 7)

# Days pregnant
today() - ${lmp_date}
```

---

## Validation Patterns

### Phone Number

```
regex(., '^\+?[0-9]{10,15}$')
```

### Email

```
regex(., '[^@]+@[^@]+\.[^@]+')
```

### ID Format (2 letters + 6 numbers)

```
regex(., '[A-Z]{2}[0-9]{6}')
```

### Numeric Range

```
. >= 0 and . <= 120    # Age
. > 0 and . <= 300     # Weight kg
. >= 50 and . <= 250   # Height cm
```

### Date Constraints

```
. <= today()           # Not future
. >= today()           # Not past
. >= today() - 365     # Within last year
. >= ${start_date}     # After another date
```

### Text Length

```
string-length(.) >= 3              # Minimum 3 chars
string-length(.) <= 100            # Maximum 100 chars
string-length(.) >= 3 and string-length(.) <= 50   # Range
```

---

## Relevance Patterns

### Basic Conditions

```
${field} = 'value'
${field} != 'value'
${field} != ''
${field} = ''
```

### Numeric

```
${age} < 5
${age} >= 18
${score} > 50 and ${score} <= 100
```

### Multiple Select

```
selected(${symptoms}, 'fever')
selected(${symptoms}, 'cough') or selected(${symptoms}, 'cold')
not(selected(${options}, 'none'))
count-selected(${choices}) >= 2
```

### Combined

```
${age} >= 18 and ${consent} = 'yes'
${status} = 'active' or ${status} = 'pending'
${sex} = 'female' and ${age} >= 15 and ${age} <= 49
```

---

## Question Type Reference

| Type | Use For |
|------|---------|
| `text` | Names, addresses, notes |
| `integer` | Age, count, whole numbers |
| `decimal` | Weight, height, measurements |
| `select_one` | Single choice |
| `select_multiple` | Multiple choices |
| `date` | Dates |
| `time` | Times |
| `dateTime` | Date and time |
| `geopoint` | GPS location |
| `image` | Photos |
| `audio` | Voice recordings |
| `barcode` | Scanning |
| `note` | Display text |
| `calculate` | Hidden calculations |
| `hidden` | Hidden fields |

---

## Appearance Reference

### Text

| Appearance | Result |
|------------|--------|
| `multiline` | Text area |
| `numbers` | Numeric keyboard |
| `masked` | Password style |

### Select

| Appearance | Result |
|------------|--------|
| `minimal` | Dropdown |
| `quick` | Auto-advance |
| `autocomplete` | Searchable |
| `columns` | Multi-column |
| `columns-3` | 3 columns |
| `likert` | Likert scale |
| `map` | Map selection |
| `horizontal` | Side-by-side |

### Date

| Appearance | Result |
|------------|--------|
| `no-calendar` | Spinner |
| `month-year` | Month/year only |
| `year` | Year only |

### Image

| Appearance | Result |
|------------|--------|
| `new` | Camera only |
| `new-front` | Front camera |
| `annotate` | Draw on image |
| `draw` | Sketch |
| `signature` | Signature |

### Geopoint

| Appearance | Result |
|------------|--------|
| `maps` | Show on map |
| `placement-map` | Pick on map |

### Group

| Appearance | Result |
|------------|--------|
| `field-list` | All on one screen |
| `table-list` | Table layout |

---

## Function Reference

### Essential Functions

| Function | Example |
|----------|---------|
| `concat()` | `concat(${a}, ' ', ${b})` |
| `if()` | `if(${x}>0, 'yes', 'no')` |
| `coalesce()` | `coalesce(${val}, 0)` |
| `selected()` | `selected(${q}, 'opt')` |
| `count()` | `count(${repeat})` |
| `sum()` | `sum(${repeat}/value)` |
| `today()` | `today()` |
| `now()` | `now()` |

### String Functions

| Function | Example |
|----------|---------|
| `string-length()` | `string-length(${text})` |
| `contains()` | `contains(${text}, 'word')` |
| `substr()` | `substr(${text}, 0, 5)` |
| `regex()` | `regex(${text}, 'pattern')` |

### Math Functions

| Function | Example |
|----------|---------|
| `round()` | `round(${num}, 2)` |
| `int()` | `int(${decimal})` |
| `abs()` | `abs(${difference})` |
| `pow()` | `pow(${base}, 2)` |

### Date Functions

| Function | Example |
|----------|---------|
| `format-date()` | `format-date(${date}, '%Y-%m-%d')` |
| `decimal-date-time()` | `decimal-date-time(${dt})` |

---

## XLSForm Column Cheat Sheet

### Survey Sheet

| Column | Purpose |
|--------|---------|
| `type` | Question type |
| `name` | Field identifier |
| `label` | Display text |
| `hint` | Helper text |
| `required` | Mandatory (yes/expression) |
| `required_message` | Required error |
| `relevant` | Show/hide condition |
| `constraint` | Validation rule |
| `constraint_message` | Validation error |
| `default` | Default value |
| `calculation` | Calculate formula |
| `appearance` | Visual style |
| `choice_filter` | Filter choices |
| `repeat_count` | Repeat instances |
| `readonly` | Prevent editing |

### Choices Sheet

| Column | Purpose |
|--------|---------|
| `list_name` | Choice group |
| `name` | Value saved |
| `label` | Display text |
| `image` | Choice image |

### Settings Sheet

| Column | Purpose |
|--------|---------|
| `form_title` | Display name |
| `form_id` | Unique ID |
| `version` | Version string |
| `default_language` | Default lang |
| `style` | Form style |
| `public_key` | Encryption key |

---

## File Structure

```
forms/
  app/
    assessment.xlsx
    assessment.properties.json
    assessment-media/
      icon.png
  contact/
    person-create.xlsx
    person-edit.xlsx
```

---

## Testing Checklist

- [ ] All paths through skip logic
- [ ] All constraints with valid/invalid data
- [ ] Required fields
- [ ] Calculations with edge cases
- [ ] Repeats (add, remove, count)
- [ ] External data lookups
- [ ] Media capture
- [ ] GPS accuracy
- [ ] All languages
- [ ] Low-end devices
- [ ] Offline functionality
