# XLSForm Structure

XLSForm uses spreadsheet-based design with three essential sheets.

## Survey Sheet (Required)

The main sheet containing form questions.

### Required Columns

| Column | Description |
|--------|-------------|
| `type` | Question type (text, integer, select_one, etc.) |
| `name` | Unique field identifier (no spaces, starts with letter/underscore) |
| `label` | User-visible question text |

### Common Optional Columns

| Column | Description |
|--------|-------------|
| `hint` | Helper text below question |
| `required` | Set to `yes` to make mandatory |
| `required_message` | Custom error when required field empty |
| `relevant` | Show/hide condition (XPath expression) |
| `constraint` | Validation rule (XPath expression) |
| `constraint_message` | Error message for failed constraint |
| `default` | Pre-populated value |
| `readonly` | Set to `yes` to prevent editing |
| `calculation` | Formula for calculated fields |
| `appearance` | Visual styling option |
| `choice_filter` | Filter choices based on previous answers |
| `repeat_count` | Number of repetitions (fixed or dynamic) |

### Example

| type | name | label | required | hint |
|------|------|-------|----------|------|
| text | first_name | First Name | yes | Enter given name |
| text | last_name | Last Name | yes | |
| integer | age | Age (years) | yes | |
| select_one gender | sex | Gender | yes | |

---

## Choices Sheet (Required for select questions)

Defines answer options for select questions.

### Required Columns

| Column | Description |
|--------|-------------|
| `list_name` | Groups related choices (matches select type) |
| `name` | Choice value saved in data |
| `label` | Display text for choice |

### Example

| list_name | name | label |
|-----------|------|-------|
| yes_no | yes | Yes |
| yes_no | no | No |
| gender | male | Male |
| gender | female | Female |
| gender | other | Other |

### Optional Columns

| Column | Description |
|--------|-------------|
| `image` | Image filename for choice |
| `filter_column` | Value for cascading selects |

---

## Settings Sheet (Recommended)

Form metadata and configuration.

### Columns

| Column | Description |
|--------|-------------|
| `form_title` | Display name for the form |
| `form_id` | Unique identifier (max 64 chars, no spaces) |
| `version` | Version string (convention: `yyyymmddrr`) |
| `instance_name` | Expression for naming submissions |
| `default_language` | Default language code |
| `public_key` | Base64-encoded encryption key |
| `submission_url` | Alternative submission endpoint |
| `style` | Form theme (`pages`, `theme-grid`) |
| `auto_send` | Auto-submit when connected |
| `auto_delete` | Delete after successful submission |

### Example

| form_title | form_id | version | default_language |
|------------|---------|---------|------------------|
| Patient Registration | patient_reg | 2024010100 | English (en) |

---

## Naming Conventions

### Field Names

- Use `snake_case` (e.g., `date_of_birth`)
- Start with letter or underscore
- No spaces or special characters
- Be descriptive but concise
- Avoid reserved words

### Form IDs

- Max 64 characters
- No spaces
- Unique within project
- Use lowercase with underscores

---

## File Organization

```
forms/
  app/
    form_name.xlsx           # XLSForm definition
    form_name.xml            # Generated XForm (optional)
    form_name.properties.json # CHT form properties
    form_name-media/         # Media files
      image1.png
      audio1.mp3
  contact/
    person-create.xlsx
    person-edit.xlsx
```
