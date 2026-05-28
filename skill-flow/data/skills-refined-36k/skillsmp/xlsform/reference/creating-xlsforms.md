# Creating XLSForms Reference

Guide for generating XLSForm Excel files from scratch or from user requirements.

## XLSForm File Structure

An XLSForm is a standard Excel (.xlsx) file with specific worksheet structure:

### Required Worksheets

1. **survey** - Contains all questions and form logic
2. **choices** - Contains answer options for select questions

### Optional Worksheets

3. **settings** - Form metadata (title, ID, version)

---

## Creating the survey Worksheet

### Required Columns

Every survey worksheet MUST have:

| Column | Purpose | Example |
|--------|---------|---------|
| type | Question type | text, integer, select_one |
| name | Variable name | age, respondent_name |
| label | Question text | What is your name? |

### Common Optional Columns

| Column | Purpose | Example |
|--------|---------|---------|
| hint | Helper text | Enter age in years |
| relevant | Skip logic | ${has_children} = 'yes' |
| required | Mandatory field | yes, no |
| constraint | Validation rule | . >= 0 and . <= 150 |
| constraint_message | Error message | Age must be 0-150 |
| calculation | Formula | ${price} * ${quantity} |
| appearance | Widget style | multiline, maps |
| default | Pre-filled value | today() |

### Example survey Worksheet

```
| type | name | label | hint | required |
|------|------|-------|------|----------|
| text | respondent_name | What is your name? | Please provide full name | yes |
| integer | age | How old are you? | Age in years | yes |
| select_one gender | gender | What is your gender? | | yes |
| date | visit_date | Date of visit | Format: YYYY-MM-DD | yes |
| note | thank_you | Thank you for completing this survey | | |
```

---

## Creating the choices Worksheet

### Required Columns

| Column | Purpose | Example |
|--------|---------|---------|
| list_name | Groups choices | gender, yes_no |
| name | Choice identifier | m, f, yes, no |
| label | Choice text | Male, Female, Yes, No |

### Example choices Worksheet

```
| list_name | name | label |
|-----------|------|-------|
| gender | m | Male |
| gender | f | Female |
| gender | o | Other |
| yes_no | yes | Yes |
| yes_no | no | No |
```

**Important:** The `list_name` must match the parameter in `select_one` or `select_multiple` types:
- Survey: `select_one gender` → Choices: `list_name = gender`

---

## Creating the settings Worksheet (Optional)

### Common Settings

```
| form_title | form_id | version | default_language |
|------------|---------|---------|------------------|
| Community Survey | comm_survey_2024 | 1.0 | en |
```

Most simple forms don't need a settings worksheet.

---

## Step-by-Step Form Creation

### Step 1: Define Requirements

Before creating the form, identify:
- What questions to ask
- What data types (text, number, location, etc.)
- Any conditional logic (skip patterns)
- Any calculations or validations needed
- Languages required

### Step 2: Create survey Worksheet

1. Start with required columns: type, name, label
2. Add one row per question
3. Add optional columns as needed (hint, relevant, constraint, etc.)
4. Use valid question types (see [question-types.md](question-types.md))
5. Ensure names are unique and alphanumeric + underscore

### Step 3: Create choices Worksheet

1. Add all select_one and select_multiple choice lists
2. Group related choices by list_name
3. Ensure list_name matches survey type parameter
4. Make choice names unique within each list

### Step 4: Add settings (Optional)

1. Create settings worksheet if needed
2. Add form_title, form_id, version
3. Set default_language if multilingual

### Step 5: Validate

Run validation script:
```bash
python scripts/validate_xlsform.py your_form.xlsx
```

---

## Output Format for Claude

When generating XLSForms, present each worksheet as a markdown table:

### Template Format

```markdown
# XLSForm: [Form Title]

## survey worksheet

| type | name | label | hint | required |
|------|------|-------|------|----------|
| [type] | [name] | [label] | [hint] | [yes/no] |
| ... | ... | ... | ... | ... |

## choices worksheet

| list_name | name | label |
|-----------|------|-------|
| [list] | [code] | [text] |
| ... | ... | ... |

## settings worksheet

| form_title | form_id | version |
|------------|---------|---------|
| [title] | [id] | [ver] |
```

### Complete Example

```markdown
# XLSForm: Health Survey

## survey worksheet

| type | name | label | hint | required |
|------|------|-------|------|----------|
| text | patient_name | Patient name | Full name | yes |
| integer | age | Age | In years | yes |
| select_one gender | gender | Gender | | yes |
| select_one yes_no | has_symptoms | Do you have any symptoms? | | yes |
| text | symptom_description | Describe symptoms | | no |
| date | visit_date | Date of visit | | yes |
| calculate | timestamp | | now() | |

## choices worksheet

| list_name | name | label |
|-----------|------|-------|
| gender | m | Male |
| gender | f | Female |
| gender | o | Other |
| yes_no | yes | Yes |
| yes_no | no | No |

## settings worksheet

| form_title | form_id | version |
|------------|---------|---------|
| Health Survey | health_survey_2024 | 1.0 |
```

---

## Common Form Patterns

### Simple Yes/No Survey

```
survey:
| type | name | label |
| select_one yes_no | q1 | Question 1? |
| select_one yes_no | q2 | Question 2? |

choices:
| list_name | name | label |
| yes_no | yes | Yes |
| yes_no | no | No |
```

### Demographics Form

```
survey:
| type | name | label |
| text | name | Full name |
| integer | age | Age |
| select_one gender | gender | Gender |
| select_one marital_status | marital_status | Marital status |

choices:
| list_name | name | label |
| gender | m | Male |
| gender | f | Female |
| marital_status | single | Single |
| marital_status | married | Married |
| marital_status | divorced | Divorced |
| marital_status | widowed | Widowed |
```

### Conditional Survey

```
survey:
| type | name | label | relevant |
| select_one yes_no | has_children | Do you have children? | |
| integer | num_children | How many? | ${has_children} = 'yes' |
| text | oldest_child_name | Oldest child's name | ${has_children} = 'yes' |

choices:
| list_name | name | label |
| yes_no | yes | Yes |
| yes_no | no | No |
```

---

## Converting Tables to Excel

Users can convert markdown tables to Excel in multiple ways:

### Method 1: Copy-Paste
1. Copy table from markdown
2. Open Excel
3. Paste into worksheet
4. Adjust column widths

### Method 2: CSV Import
1. Convert table to CSV format
2. Open Excel → Import CSV
3. Name worksheet appropriately (survey, choices, settings)

### Method 3: Python Script
Use the included `create_xlsform.py` script:
```bash
python scripts/create_xlsform.py survey.csv choices.csv -o form.xlsx
```

---

## Best Practices for Form Generation

### Question Names
- Use descriptive names: `patient_age` not `q1`
- Use underscores for spaces: `visit_date` not `visitdate`
- Keep names short but meaningful
- Avoid reserved words: `type`, `name`, `label`

### Question Labels
- Use clear, concise language
- Ask one thing per question
- Use active voice: "What is..." not "What's..."
- Avoid jargon unless necessary

### Choice Names
- Use short codes: `m`, `f`, `o` (not `male`, `female`, `other`)
- Or use descriptive names: `very_satisfied`, `satisfied`
- Be consistent within form

### Required vs Optional
- Mark critical fields as required
- Leave optional fields as not required
- Don't over-require (frustrating for users)

### Hints
- Provide examples: "e.g., 2024-10-30"
- Clarify units: "in kilograms", "in years"
- Explain special cases: "Select all that apply"

---

## Validation Checklist

Before delivering form:
- [ ] All required columns present (type, name, label)
- [ ] Question names unique
- [ ] Question names alphanumeric + underscore
- [ ] Choice list_name matches survey types
- [ ] No duplicate choice names per list
- [ ] Relevant expressions reference existing questions
- [ ] Calculation syntax valid
- [ ] Constraint expressions valid
- [ ] Settings worksheet included if needed

---

## Troubleshooting Generation Issues

### Missing Choices
**Problem:** select_one without matching choices
**Fix:** Add choices worksheet with list_name matching survey

### Invalid Names
**Problem:** Question names with spaces or special chars
**Fix:** Use underscores, alphanumeric only

### Wrong Type
**Problem:** Using "number" instead of "integer" or "decimal"
**Fix:** Use valid types from [question-types.md](question-types.md)

### Missing Required Columns
**Problem:** Survey missing type, name, or label
**Fix:** Add all three required columns

---

## See Also

- [examples.md](../examples.md) - 6 complete working XLSForms
- [question-types.md](question-types.md) - All question types
- [survey-sheet.md](survey-sheet.md) - Survey worksheet reference
- [choices-sheet.md](choices-sheet.md) - Choices worksheet reference
- [best-practices.md](best-practices.md) - Design recommendations
