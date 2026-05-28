# XLSForm Examples

This document shows 6 complete, working XLSForm examples. Copy the survey and choices worksheets to start building your own forms.

---

## Example 1: Basic Survey Form

**Use case:** Simple questionnaire with text, numbers, and yes/no questions.

### Survey Worksheet

| type | name | label | hint |
|------|------|-------|------|
| text | respondent_name | What is your name? | Please provide your full name |
| integer | age | How old are you? | Enter age in years |
| select_one gender | gender | What is your gender? | |
| text | email | Email address | example@domain.com |
| select_one yes_no | consent | Do you agree to participate? | |
| note | thank_you | Thank you for completing this survey | |

### Choices Worksheet

| list_name | name | label |
|-----------|------|-------|
| gender | male | Male |
| gender | female | Female |
| gender | other | Other |
| yes_no | yes | Yes |
| yes_no | no | No |

### Key Points
- `note` type displays static text, doesn't collect data
- `text` type accepts any input; use `constraint` for validation (see example 3)
- Each choice must have unique `name` but `label` is what users see

---

## Example 2: Conditional Logic Form

**Use case:** Questions that appear only if certain conditions are met (skip logic).

### Survey Worksheet

| type | name | label | relevant |
|------|------|-------|----------|
| select_one yes_no | has_children | Do you have children? | |
| integer | num_children | How many children? | ${has_children} = 'yes' |
| select_one age_group | youngest_age | Age of youngest child | ${has_children} = 'yes' |
| select_one yes_no | has_income | Do you have income? | |
| decimal | monthly_income | Monthly income (dollars) | ${has_income} = 'yes' |
| text | income_source | What is your income source? | ${has_income} = 'yes' and ${monthly_income} > 0 |

### Choices Worksheet

| list_name | name | label |
|-----------|------|-------|
| yes_no | yes | Yes |
| yes_no | no | No |
| age_group | 0_2 | 0-2 years |
| age_group | 3_5 | 3-5 years |
| age_group | 6_12 | 6-12 years |
| age_group | 13_17 | 13-17 years |

### Key Points
- `relevant` column controls visibility
- Expressions use XPath syntax: `${variable_name}` references other questions
- Multiple conditions: `${condition1} = 'value' and ${condition2} >= threshold`
- Questions hidden by `relevant` don't store data; skip logic keeps forms short

---

## Example 3: Calculations & Validation Form

**Use case:** Budget tracking with calculations and validation rules.

### Survey Worksheet

| type | name | label | constraint | constraint_message | calculation |
|------|------|-------|-----------|-------------------|------------|
| integer | income | Monthly income | . >= 0 | Income must be a positive number | |
| integer | rent | Rent/housing | . >= 0 | Rent must be a positive number | |
| integer | food | Food and groceries | . >= 0 | Food must be a positive number | |
| integer | utilities | Utilities | . >= 0 | Utilities must be a positive number | |
| integer | other | Other expenses | . >= 0 | Other expenses must be a positive number | |
| calculate | total_expenses | | | | ${rent} + ${food} + ${utilities} + ${other} |
| note | balance_display | Balance: ${income} - ${total_expenses} = ${income} - ${total_expenses} | | | |
| integer | target_savings | How much do you want to save monthly? | . >= 0 | Must be positive | |
| text | budget_status | Budget status | | | if(${income} - ${total_expenses} >= ${target_savings}, 'On track', 'Need to reduce expenses') |

### Choices Worksheet
(None needed for this example)

### Key Points
- `constraint` uses XPath expressions; `.` refers to the current field
- `constraint_message` appears if validation fails
- `calculation` column creates visible calculated fields
- `calculate` question type creates hidden calculations
- `calculate` question displays value in label using `${variable_name}`
- Formulas: basic math (+, -, *, /), functions (sum, avg, min, max), conditionals (if statements)

---

## Example 4: GPS and Media Collection Form

**Use case:** Field monitoring with location tracking and photo evidence.

### Survey Worksheet

| type | name | label | appearance | required |
|------|------|-------|-----------|----------|
| text | site_id | Site ID | | yes |
| geopoint | site_location | Mark site location | maps | yes |
| geotrace | walked_area | Trace the monitored area | | |
| date | visit_date | Date of visit | | yes |
| select_one site_condition | condition | Overall site condition | | yes |
| image | site_photo | Photo of site | | |
| audio | field_notes | Audio notes | | |
| integer | damage_count | Number of damaged items | . >= 0 | |
| text | damage_description | Describe damage | | |
| video | damage_video | Video of damage | | |
| note | completion | Thank you for this report | | |

### Choices Worksheet

| list_name | name | label |
|-----------|------|-------|
| site_condition | good | Good condition |
| site_condition | fair | Fair condition |
| site_condition | poor | Poor condition |

### Key Points
- `geopoint` captures latitude/longitude at a single point
- `geotrace` records a path/line (e.g., boundary walk)
- `geoshape` records a polygon (e.g., plot boundary) — not shown here
- `appearance` column customizes widgets (e.g., maps for GPS)
- `image`, `audio`, `video` store files; device handles capture
- `required` column (yes/no) enforces mandatory fields
- GPS requires GPS hardware; most modern phones have it

---

## Example 5: Multilingual Form

**Use case:** International survey supporting English, French, and Spanish.

### Survey Worksheet

| type | name | label::English | label::Français | label::Español | hint::English | hint::Français | hint::Español |
|------|------|---|---|---|---|---|---|
| text | respondent_name | What is your name? | Quel est votre nom? | ¿Cuál es su nombre? | Please provide full name | Veuillez fournir votre nom complet | Por favor proporcione su nombre completo |
| select_one language | preferred_language | Preferred language | Langue préférée | Idioma preferido | | | |
| integer | age | How old are you? | Quel âge avez-vous? | ¿Cuántos años tienes? | Age in years | Âge en années | Edad en años |
| select_one yes_no | consent | Do you agree? | Acceptez-vous? | ¿Está de acuerdo? | | | |

### Choices Worksheet

| list_name | name | label::English | label::Français | label::Español |
|-----------|------|---|---|---|
| language | english | English | English | English |
| language | french | French | Français | Francés |
| language | spanish | Spanish | Español | Español |
| yes_no | yes | Yes | Oui | Sí |
| yes_no | no | No | Non | No |

### Key Points
- Column naming: `label::Language`, `hint::Language`, `label` (default)
- All language columns live in same worksheet, separated by columns
- Choices can be translated; users see labels in their device language
- Device language set in phone settings determines which form language shows
- Hints support translation too: `hint::Français`
- Character encoding must support all languages (UTF-8)

---

## Example 6: Advanced Features Form

**Use case:** Household survey with repeat groups, cascading selects, and external data.

### Survey Worksheet

| type | name | label | relevant | choice_filter |
|------|------|-------|----------|---------------|
| text | household_id | Household ID | | |
| select_one yes_no | has_members | Does household have other members? | | |
| begin repeat | household_members | Other household members | ${has_members} = 'yes' | |
| text | member_name | Member name | | |
| integer | member_age | Member age | | |
| select_one relationship | member_relationship | Relationship to respondent | | |
| end repeat | | | | |
| select_one countries | country | Country | | |
| select_one province | province | Province/State | | province in ${country} |
| select_one_from_file hospitals_list | health_facility | Nearest health facility | | |
| date | survey_date | Survey date | | |
| calculate | timestamp | | | now() |

### Choices Worksheet

| list_name | name | label | country | province |
|-----------|------|-------|---------|----------|
| relationship | parent | Parent | | |
| relationship | child | Child | | |
| relationship | sibling | Sibling | | |
| relationship | spouse | Spouse | | |
| countries | kenya | Kenya | | |
| countries | uganda | Uganda | | |
| countries | tanzania | Tanzania | | |
| province | nairobi | Nairobi | kenya | |
| province | mombasa | Mombasa | kenya | |
| province | kampala | Kampala | uganda | |
| province | jinja | Jinja | uganda | |
| province | dar | Dar es Salaam | tanzania | |
| province | dodoma | Dodoma | tanzania | |

### External Data File: hospitals_list.csv

```csv
name,label
hospital_01,Nairobi General Hospital
hospital_02,Kenyatta National Hospital
hospital_03,Kampala Hospital
facility_04,Mbarara Hospital
facility_05,Dodoma Regional Hospital
```

Place `hospitals_list.csv` in same folder as XLSForm .xlsx file.

### Key Points

**Repeat Groups:**
- `begin repeat` and `end repeat` enclose repeating fields
- Users add multiple members without duplicating form structure
- Data: nested rows per household

**Cascading Selects:**
- `choice_filter` column filters choices based on other questions
- Syntax: `province in ${country}` filters provinces by selected country
- Fourth column in choices sheet matches filter field (country, province)
- Choices with matching country value appear for province question

**External Data:**
- `select_one_from_file` loads choices from CSV file instead of worksheet
- CSV must have `name` and `label` columns matching choice structure
- Use for large lists (1000+) to keep Excel file small and portable
- File location: same folder as .xlsx, or URL/remote path

**Timestamp:**
- `calculate` type with `now()` captures date/time automatically
- Hidden field, not displayed to user
- Useful for audit trails, server submissions

---

## Adapting Examples for Your Use Case

**Starting from Example 1 (Basic):**
- Add more question types from [question-types.md](../SKILL.md#five-key-concepts)
- Add constraints for validation (Example 3)
- Add skip logic (Example 2)

**Adding interactivity:**
- Use `relevant` for conditional questions (Example 2)
- Use `choice_filter` for cascading selects (Example 6)
- Use `constraint` for validation (Example 3)

**Adding media/location:**
- Add `geopoint`, `image`, `audio`, `video` (Example 4)
- Use `appearance` column to customize widgets

**Scaling up:**
- Use `begin repeat`/`end repeat` for multiple records (Example 6)
- Use `select_one_from_file` for large choice lists (Example 6)
- Use external CSV/XML files to keep worksheet manageable

**Multiple languages:**
- Copy Example 5 structure
- Add `label::Language` columns for each language
- Test on device to confirm language display

---

## Testing Your Form

1. **Validate structure:**
   ```bash
   python scripts/validate_xlsform.py your_form.xlsx
   ```

2. **Convert to XForm:**
   ```bash
   python scripts/convert_to_xform.py your_form.xlsx
   ```

3. **Test on mobile:**
   - Upload to ODK Central, KoBoToolbox, or local ODK Collect
   - Test all conditional logic paths
   - Test all constraints with invalid input
   - Check text wrapping on small screens

4. **Common issues:**
   - Check [common-errors.md](../reference/common-errors.md) for solutions
   - Validate question `name` fields match exactly in relevant/calculation expressions
   - Ensure choice `list_name` values match survey `select_one` or `select_multiple` type

---

## Converting to XForm XML

Your .xlsx converts to .xml (XForm) before deployment:

```bash
python scripts/convert_to_xform.py your_form.xlsx -o your_form.xml
```

The .xml file is what ODK Collect, KoBoToolbox, etc. actually use. XLSForm is human-friendly Excel; XForm is the machine format.
