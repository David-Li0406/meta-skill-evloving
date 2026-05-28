# Choices Sheet Reference

The choices worksheet defines answer options for `select_one`, `select_multiple`, and `rank` questions. Each choice belongs to a named list.

## Required Columns

Every choice must have these three columns:

### list_name
Grouping identifier that ties choices to questions. Must match `select_one list_name` in survey.

**Rules:**
- Alphanumeric + underscore only
- Case-sensitive: `gender`, `Gender` are different lists
- Multiple choices can share same list_name
- Choices with same list_name appear together

**Example:**
```
| list_name | name | label |
| gender | m | Male |
| gender | f | Female |
| gender | o | Other |

In survey:
| type | name | label |
| select_one gender | gender | What is your gender? |
```

**Must Match:**
- Survey worksheet uses: `select_one gender`
- Choices worksheet uses: `list_name = gender`
- If names don't match exactly, form won't work

---

### name
Unique identifier for each choice (within the list). This is stored in data.

**Rules:**
- Alphanumeric + underscore only
- Cannot start with number
- Case-sensitive: `yes`, `Yes` are different
- Unique within the list (no duplicates per list_name)
- NOT displayed to user (label is displayed)

**Valid Examples:**
```
yes, no
m, f, o
high, medium, low
option_1, option_2, option_3
```

**Invalid Examples:**
```
Yes Or No (spaces not allowed)
1, 2, 3 (shouldn't start with number)
Male/Female (special char not allowed)
```

**Data Storage:**
The `name` value is what gets stored in data files:
```
Gender question with choices:
- name: m, label: Male
- name: f, label: Female

If user selects "Male", data stores: m
```

---

### label
Text displayed to user. Can be any language, characters, emoji.

**Rules:**
- Can be any text, emoji, unicode
- Displayed on mobile/web, NOT stored
- Supports translation: `label::language` columns
- Different lists can have same label (e.g., "Yes/No" appears in many lists)
- Can be longer than name

**Examples:**
```
Male
Female
Other
1000-5000 USD
5000+ USD
High school diploma
Bachelor's degree
Master's degree
```

**Why separate name and label?**
- `name` is machine-friendly code: `m`, `f`, `other`
- `label` is human-friendly text: "Male", "Female", "Other"
- Changing label doesn't break data (names are stable)
- Names work in all languages; labels are language-specific

---

## Optional Columns

### image
Display an image instead of (or with) label text.

**Rules:**
- Path to image file relative to .xlsx location
- Can combine with label: both show
- Common for pictorial surveys
- Supported formats: JPEG, PNG

**Example:**
```
| list_name | name | label | image |
| expression | happy | Happy | happy.png |
| expression | neutral | Neutral | neutral.png |
| expression | sad | Sad | sad.png |
```

**File Structure:**
```
form.xlsx
happy.png
neutral.png
sad.png
```

---

### audio
Play audio clip for choice. Icon or play button shown.

**Rules:**
- Path to audio file relative to .xlsx
- Formats: MP3, AMR, WAV (device-dependent)
- Useful for non-literate respondents
- Can combine with label

**Example:**
```
| list_name | name | label | audio |
| animal | cow | Cow | cow_sound.mp3 |
| animal | dog | Dog | dog_sound.mp3 |
```

---

## Multilingual Support

### label::language
Translated label for specific language.

**Rules:**
- Format: `label::` + language code (en, fr, es, sw, ar, etc.)
- One column per language
- Include base `label` column as fallback/default
- Device user selects language; sees matching label

**Example:**
```
| list_name | name | label::en | label::fr | label::es |
| gender | m | Male | Homme | Hombre |
| gender | f | Female | Femme | Mujer |
| yes_no | yes | Yes | Oui | Sí |
| yes_no | no | No | Non | No |
```

**When Device Language = French:**
User sees:
```
Homme
Femme
Oui
Non
```

**When Device Language = English:**
User sees:
```
Male
Female
Yes
No
```

---

## Filtering Columns (for cascading selects)

Choices worksheet can include additional columns used in `choice_filter` expressions in survey.

**Example:**
```
Choices Worksheet:
| list_name | name | label | country | region |
| province | nairobi | Nairobi | kenya | east |
| province | mombasa | Mombasa | kenya | coast |
| province | kampala | Kampala | uganda | central |

Survey Worksheet:
| type | name | label | choice_filter |
| select_one country | country | Country |
| select_one province | province | Province | province in ${country} |

(The 'country' column in choices filters provinces by selected country)
```

See [cascading-selects.md](cascading-selects.md) for full details.

---

## Organization Best Practices

### Group Related Lists
```
| list_name | name | label |
| yes_no | yes | Yes |
| yes_no | no | No |
| gender | m | Male |
| gender | f | Female |
| gender | o | Other |
| education | primary | Primary school |
| education | secondary | Secondary school |
```

### Alphabetical Order (Optional)
Easier to find choices, but not required:
```
| list_name | name | label |
| country | tz | Tanzania |
| country | ug | Uganda |
| country | ke | Kenya |
```

### Meaningful Names
Use descriptive names, not just numbers:
```
✓ Good:   very_satisfied, somewhat_satisfied, not_satisfied
✗ Poor:   1, 2, 3
✓ Good:   high_income, medium_income, low_income
✗ Poor:   option_a, option_b, option_c
```

---

## Common Patterns

### Yes/No List
```
| list_name | name | label |
| yes_no | yes | Yes |
| yes_no | no | No |
```

### Likert Scale
```
| list_name | name | label |
| satisfaction | very_satisfied | Very satisfied |
| satisfaction | somewhat_satisfied | Somewhat satisfied |
| satisfaction | neutral | Neither |
| satisfaction | somewhat_dissatisfied | Somewhat dissatisfied |
| satisfaction | very_dissatisfied | Very dissatisfied |
```

### Numeric Range
```
| list_name | name | label |
| age_group | 0_5 | 0-5 years |
| age_group | 6_12 | 6-12 years |
| age_group | 13_17 | 13-17 years |
| age_group | 18_30 | 18-30 years |
| age_group | 30_plus | 30+ years |
```

### Income Brackets
```
| list_name | name | label |
| income | 0_500 | Under $500 |
| income | 500_1000 | $500-$1000 |
| income | 1000_2000 | $1000-$2000 |
| income | 2000_plus | $2000+ |
```

### Days of Week
```
| list_name | name | label |
| day_of_week | mon | Monday |
| day_of_week | tue | Tuesday |
| day_of_week | wed | Wednesday |
| day_of_week | thu | Thursday |
| day_of_week | fri | Friday |
| day_of_week | sat | Saturday |
| day_of_week | sun | Sunday |
```

### Multiple Languages
```
| list_name | name | label::en | label::fr | label::sw |
| gender | m | Male | Homme | Mwanamume |
| gender | f | Female | Femme | Mwanamke |
| yes_no | yes | Yes | Oui | Ndiyo |
| yes_no | no | No | Non | Hapana |
```

---

## Limits and Performance

| Aspect | Limit | Notes |
|--------|-------|-------|
| Choices per list | No hard limit | ~100 reasonable, 1000+ consider file-based |
| Total lists | No hard limit | ~50-100 typical |
| Label length | ~500 chars | Practical mobile display limit |
| Total choices worksheet size | ~1MB | Very large lists slow form loading |
| Choice names | 255 chars max | Rare in practice |

**If You Have 1000+ Choices:**
Use `select_one_from_file` to load from external CSV instead of worksheet. See [external-data.md](../reference/external-data.md).

---

## Validation and Errors

### list_name mismatch
```
Survey: select_one gender
Choices: list_name = Gender (different case!)
ERROR: Choices not found
FIX: Make list_name match exactly (case-sensitive)
```

### Duplicate Choice Names
```
| list_name | name | label |
| gender | m | Male |
| gender | m | Homme (ERROR: duplicate 'm')
```

### Choice not found in survey
```
Choices defined for: gender, education, location
Survey uses: gender, education, marital_status
WARNING: marital_status has no choices
```

### Invalid list_name or name
```
list_name: "Age Group" (space not allowed)
name: "1st" (starts with number)
ERROR: Invalid names
FIX: Use underscores: age_group, option_1st
```

---

## Examples

### Simple Binary Choice
```
| list_name | name | label |
| yes_no | yes | Yes |
| yes_no | no | No |

Survey:
| type | name | label |
| select_one yes_no | consent | Do you agree? |
```

### Multiple Separate Lists
```
| list_name | name | label |
| gender | m | Male |
| gender | f | Female |
| gender | o | Other |
| education | primary | Primary |
| education | secondary | Secondary |
| education | tertiary | Tertiary |

Survey:
| type | name | label |
| select_one gender | gender | Gender |
| select_one education | education | Education level |
```

### Multilingual with Image
```
| list_name | name | label::en | label::fr | image |
| emotion | happy | Happy | Heureux | happy.png |
| emotion | sad | Sad | Triste | sad.png |
| emotion | angry | Angry | En colère | angry.png |
```

### Cascading (Country → Province)
```
| list_name | name | label | country |
| province | nairobi | Nairobi | kenya |
| province | mombasa | Mombasa | kenya |
| province | kampala | Kampala | uganda |
| province | jinja | Jinja | uganda |

Survey:
| type | name | label | choice_filter |
| select_one country | country | Country |
| select_one province | province | Province | province in ${country} |
```
