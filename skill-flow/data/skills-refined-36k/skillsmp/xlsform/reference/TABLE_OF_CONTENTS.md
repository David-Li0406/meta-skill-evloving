# XLSForm Reference - Table of Contents

## By Topic

### Getting Started
- [creating-xlsforms.md](creating-xlsforms.md) - How to generate XLSForm Excel files

### Form Structure
- [survey-sheet.md](survey-sheet.md) - Survey worksheet columns and structure
- [choices-sheet.md](choices-sheet.md) - Choices worksheet for multiple-choice questions
- [settings-sheet.md](settings-sheet.md) - Optional settings and metadata worksheets

### Question Types
- [question-types.md](question-types.md) - All 20+ question types with examples
  - **Text inputs:** text, integer, decimal
  - **Selection:** select_one, select_multiple, rank
  - **Date/Time:** date, time, dateTime
  - **Location:** geopoint, geotrace, geoshape
  - **Media:** image, audio, video, file, barcode
  - **Special:** calculate, note, acknowledge, hidden

### Logic and Control
- [skip-logic.md](skip-logic.md) - Conditional display with `relevant` column
- [calculations.md](calculations.md) - Calculations using `calculate` type and `calculation` column
- [constraints.md](constraints.md) - Validation rules with `constraint` column

### Expressions
- [xpath-expressions.md](xpath-expressions.md) - XPath functions, operators, and syntax

### Advanced Features
- [appearances.md](appearances.md) - Widget customization with `appearance` column
- [cascading-selects.md](cascading-selects.md) - Dependent choice lists with `choice_filter`
- [external-data.md](external-data.md) - Load choices from CSV/XML with `select_one_from_file`
- [multilingual.md](multilingual.md) - Multiple language support with `label::language` syntax

### Best Practices & Troubleshooting
- [best-practices.md](best-practices.md) - Design patterns and recommendations
- [common-errors.md](common-errors.md) - Error messages and solutions

---

## By Use Case

### Generating an XLSForm
**Goal:** Create an XLSForm Excel file from scratch or requirements

1. Read: [creating-xlsforms.md](creating-xlsforms.md) - Learn file structure
2. Plan: Identify questions, types, logic needed
3. Create: Build survey and choices worksheets
4. Generate: Use markdown tables or `create_xlsform.py` script
5. Validate: Run `python scripts/validate_xlsform.py form.xlsx`

### Creating a Simple Survey
**Goal:** Basic form with text, numbers, and multiple-choice questions

1. Start: [creating-xlsforms.md](creating-xlsforms.md) - Understand structure
2. Learn types: [question-types.md](question-types.md) - Pick question types (text, integer, select_one)
3. Add choices: [choices-sheet.md](choices-sheet.md) - Define answer options
4. See example: Look at "Basic Survey" in examples.md
5. Validate: Run `python scripts/validate_xlsform.py form.xlsx`

### Adding Conditional Questions (Skip Logic)
**Goal:** Show/hide questions based on previous answers

1. Read: [skip-logic.md](skip-logic.md) - How `relevant` works
2. Learn expressions: [xpath-expressions.md](xpath-expressions.md) - Write conditions
3. See examples: "Conditional Logic" in examples.md
4. Common patterns:
   - Show if previous = specific value: `${previous_question} = 'option'`
   - Show if number >= threshold: `${age} >= 18`
   - Show if multiple conditions met: `${gender} = 'F' and ${age} < 50`

### Creating Calculations
**Goal:** Automatic computed fields (timestamps, sums, formulas)

1. Read: [calculations.md](calculations.md) - Types of calculations
2. Syntax: [xpath-expressions.md](xpath-expressions.md) - Functions (sum, avg, now, etc.)
3. See example: "Calculations & Validation" in examples.md
4. Common patterns:
   - Timestamp: `calculate` type with `now()`
   - Sum fields: `calculate` with `${field1} + ${field2}`
   - Calculated label: `calculation` column with formula

### GPS and Media Collection
**Goal:** Capture location coordinates or photos/video

1. Types: [question-types.md](question-types.md) - geopoint, geotrace, geoshape, image, audio, video
2. See example: "GPS & Media Collection" in examples.md
3. Key points:
   - geopoint = single lat/long point
   - geotrace = line/path
   - geoshape = polygon area
   - image, audio, video store files

### Multilingual Forms
**Goal:** Support multiple languages

1. Read: [multilingual.md](multilingual.md) - Syntax and setup
2. Syntax: Use `label::English`, `label::French`, etc. in same cell
3. See example: "Multilingual Form" in examples.md
4. Important:
   - One language column per language
   - Device user selects language when opening form
   - Hints can also be translated: `hint::Language`

### Dependent Choice Lists (Cascading Selects)
**Goal:** Second select_one depends on first (e.g., Country → Province)

1. Read: [cascading-selects.md](cascading-selects.md) - How choice_filter works
2. See example: "Advanced Features" in examples.md
3. Syntax: Use `choice_filter` column with expressions
4. Alternative: [external-data.md](external-data.md) for very large lists

### Validating User Input
**Goal:** Enforce rules (email format, age limits, etc.)

1. Read: [constraints.md](constraints.md) - `constraint` column
2. Expressions: [xpath-expressions.md](xpath-expressions.md) - Comparison operators
3. Add messages: `constraint_message` column for user-friendly errors
4. Common patterns:
   - Email: `.regex(., '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')`
   - Number range: `. >= 0 and . <= 100`
   - Date not in future: `. <= today()`

### Loading Choices from File
**Goal:** Large choice lists from external CSV (e.g., 1000+ hospitals)

1. Read: [external-data.md](external-data.md) - File format and setup
2. Use: `select_one_from_file` question type
3. File: CSV with name and label columns, matches `list_name`
4. See example: "Advanced Features" in examples.md

### Optimizing Form Performance
**Goal:** Fast-loading, responsive forms on older devices

1. Read: [best-practices.md](best-practices.md) - Performance section
2. Key tips:
   - Avoid deeply nested calculations
   - Use choice lists instead of free text
   - Keep repeat groups reasonable (<50 repeats)
   - Test on older/slower devices

### Getting Errors When Converting?
**Goal:** Fix validation and conversion errors

1. Run: `python scripts/validate_xlsform.py form.xlsx`
2. Check: [common-errors.md](common-errors.md) - Look up error message
3. Fix: Apply suggested solution
4. Verify: Run script again, then `convert_to_xform.py`

---

## By Question Type

### Text Input
- [question-types.md#text](question-types.md#text) - text, integer, decimal
- [constraints.md](constraints.md) - Validation (length, format, range)

### Selection
- [question-types.md#selection](question-types.md#selection) - select_one, select_multiple, rank
- [choices-sheet.md](choices-sheet.md) - Define answer options
- [cascading-selects.md](cascading-selects.md) - Dependent lists
- [external-data.md](external-data.md) - Large external lists

### Date/Time
- [question-types.md#datetime](question-types.md#datetime) - date, time, dateTime
- [constraints.md](constraints.md) - Date validation
- [calculations.md](calculations.md) - Date arithmetic

### Location
- [question-types.md#location](question-types.md#location) - geopoint, geotrace, geoshape
- [appearances.md](appearances.md) - Map appearance options

### Media
- [question-types.md#media](question-types.md#media) - image, audio, video, file, barcode
- [appearances.md](appearances.md) - Media quality/format options

### Calculated/Special
- [question-types.md#special](question-types.md#special) - calculate, note, acknowledge, hidden
- [calculations.md](calculations.md) - Calculation syntax

### Ranking
- [question-types.md#ranking](question-types.md#ranking) - rank type
- [appearances.md](appearances.md) - Rank appearance options

---

## Reference Quick Links

### Essential Reading
- **Start here:** [survey-sheet.md](survey-sheet.md) - Understand worksheet structure
- **Question types:** [question-types.md](question-types.md) - All available types
- **Stuck?** [common-errors.md](common-errors.md) - Error solutions

### When You Need Expressions
- **XPath reference:** [xpath-expressions.md](xpath-expressions.md) - Functions, operators, syntax
- **Conditional logic:** [skip-logic.md](skip-logic.md) - Write `relevant` expressions
- **Calculations:** [calculations.md](calculations.md) - Write formulas
- **Validation:** [constraints.md](constraints.md) - Validation rules

### Advanced Topics
- **Appearances:** [appearances.md](appearances.md) - Customize widgets
- **Cascading:** [cascading-selects.md](cascading-selects.md) - Dependent choices
- **External data:** [external-data.md](external-data.md) - CSV/XML lists
- **Languages:** [multilingual.md](multilingual.md) - Multiple language support

### Best Practices
- **Design:** [best-practices.md](best-practices.md) - Form design patterns
- **Performance:** [best-practices.md](best-practices.md#performance) - Fast forms
- **Testing:** [best-practices.md](best-practices.md#testing) - Field deployment
- **Troubleshooting:** [common-errors.md](common-errors.md) - Common issues and fixes
