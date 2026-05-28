# Workflows and Validation Patterns

Guide for creating effective workflows with validation and feedback loops in agent skills.

## Table of Contents

- Understanding Workflows in Skills
- Create Verifiable Intermediate Outputs Pattern
- Validate Script Pattern
- Feedback Loop Pattern
- When to Use Validation Patterns
- Implementation Examples
- Common Mistakes

## Understanding Workflows in Skills

Workflows guide Claude through multi-step processes. Well-designed workflows:
- Break complex tasks into clear sequential steps
- Include validation at critical points
- Provide feedback loops for error correction
- Create verifiable intermediate outputs when needed

**Simple workflow** (no validation needed):
```markdown
## Basic data export

1. Load data from database
2. Transform to CSV format
3. Save to file
```

**Complex workflow** (validation critical):
```markdown
## Database migration workflow

1. Verify database connection
2. Create backup
3. **Validate backup integrity** ← validation step
4. Run migration
5. **Verify migration success** ← verification step
6. If verification fails → restore from backup
```

## Create Verifiable Intermediate Outputs Pattern

### What It Is

The plan-validate-execute pattern catches errors early by having Claude create a structured plan file first, then validate that plan with a script before executing it.

**Flow**: analyze → **create plan file** → **validate plan** → execute → verify

### When to Use

Use this pattern when:
- **Batch operations**: Updating 50+ items at once
- **Destructive changes**: Operations that can't be easily undone
- **Complex validation rules**: Business logic too complex for Claude to verify manually
- **High-stakes operations**: Errors have serious consequences

**Don't use** for:
- Single simple operations
- Read-only tasks
- Operations with trivial validation

### Why It Works

**Catches errors early**: Validation finds problems before changes are applied
**Machine-verifiable**: Scripts provide objective verification
**Reversible planning**: Claude can iterate on the plan without touching originals
**Clear debugging**: Error messages point to specific problems

### Implementation Pattern

**Step 1: Define the plan file format**

Choose a structured format (JSON, YAML, or CSV) that's easy to validate:

```json
{
  "changes": [
    {
      "field": "customer_name",
      "old_value": "John Smith",
      "new_value": "John A. Smith"
    },
    {
      "field": "order_total",
      "old_value": "100.00",
      "new_value": "105.00"
    }
  ]
}
```

**Step 2: Create validation script**

Write a script that checks the plan file:

```python
# scripts/validate_changes.py
import json
import sys

def validate_changes(plan_file):
    """Validate change plan before execution."""
    with open(plan_file) as f:
        plan = json.load(f)

    errors = []

    # Check required fields exist
    if "changes" not in plan:
        errors.append("Missing 'changes' key in plan")
        return errors

    # Validate each change
    valid_fields = ["customer_name", "order_total", "signature_date"]
    for i, change in enumerate(plan["changes"]):
        # Check field exists
        if change["field"] not in valid_fields:
            errors.append(
                f"Change {i}: Field '{change['field']}' not found. "
                f"Available fields: {', '.join(valid_fields)}"
            )

        # Check value types
        if change["field"] == "order_total":
            try:
                float(change["new_value"])
            except ValueError:
                errors.append(
                    f"Change {i}: order_total must be numeric, "
                    f"got '{change['new_value']}'"
                )

    return errors

if __name__ == "__main__":
    errors = validate_changes(sys.argv[1])
    if errors:
        print("VALIDATION FAILED:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("OK: All validations passed")
        sys.exit(0)
```

**Step 3: Document the workflow in SKILL.md**

````markdown
## PDF Form Batch Update Workflow

Copy this checklist and track your progress:

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create change plan (edit changes.json)
- [ ] Step 3: Validate plan (run validate_changes.py)
- [ ] Step 4: Apply changes (run apply_changes.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**

Run: `python scripts/analyze_form.py input.pdf`

This extracts form fields and saves to `fields.json`.

**Step 2: Create change plan**

Create `changes.json` with the updates to apply:

```json
{
  "changes": [
    {"field": "customer_name", "new_value": "John Smith"},
    {"field": "order_total", "new_value": "150.00"}
  ]
}
```

**Step 3: Validate plan**

Run: `python scripts/validate_changes.py changes.json`

**CRITICAL**: Do NOT proceed if validation fails. Fix the errors in `changes.json` and validate again.

**Step 4: Apply changes**

Run: `python scripts/apply_changes.py input.pdf changes.json output.pdf`

**Step 5: Verify output**

Run: `python scripts/verify_output.py output.pdf`

If verification fails, review the error messages and return to Step 2.
````

### Make Validation Scripts Verbose

Provide specific, actionable error messages:

**Bad** (vague):
```python
if field not in valid_fields:
    errors.append("Invalid field")
```

**Good** (specific):
```python
if field not in valid_fields:
    errors.append(
        f"Field '{field}' not found. "
        f"Available fields: {', '.join(valid_fields)}"
    )
```

Specific messages help Claude fix issues without guessing.

## Validate Script Pattern

### What It Is

A simpler pattern than plan-validate-execute. Just run a validation script after each significant operation.

**Flow**: execute → **validate** → if errors, fix and repeat

### When to Use

Use this pattern when:
- Editing structured data (XML, JSON, configuration files)
- Generating code that must compile or pass linting
- Creating documents with strict formatting requirements
- Any operation where correctness can be programmatically verified

### Implementation Pattern

**Step 1: Create validation script**

```python
# scripts/validate.py
import sys
import xml.etree.ElementTree as ET

def validate_xml(file_path):
    """Validate XML structure and required elements."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        return [f"XML parse error: {e}"]

    errors = []

    # Check required elements
    if root.find("document") is None:
        errors.append("Missing required element: <document>")

    if root.find("body") is None:
        errors.append("Missing required element: <body>")

    return errors

if __name__ == "__main__":
    errors = validate_xml(sys.argv[1])
    if errors:
        print("VALIDATION FAILED:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("OK")
        sys.exit(0)
```

**Step 2: Document in SKILL.md**

````markdown
## Document editing process

1. Make your edits to `word/document.xml`
2. **Validate immediately**: `python scripts/validate.py word/document.xml`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues in the XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python scripts/pack.py unpacked_dir/ output.docx`
6. Test the output document
````

### Key Principle

**Validate after EVERY significant change**, not just at the end. This catches errors early when they're easier to fix.

## Feedback Loop Pattern

### What It Is

A general pattern for iterative improvement: do something → check quality → fix issues → repeat.

**Pattern**: Run validator → fix errors → repeat until clean

### When to Use

Use for tasks where:
- Quality can be objectively measured
- Multiple iterations improve results
- Errors are common but fixable

**Examples**:
- Code that must pass linting
- Documents that must follow style guidelines
- Data that must meet quality standards
- Outputs that must match a template

### Implementation: Code-Based Feedback Loop

````markdown
## Code generation workflow

1. Generate the initial code
2. **Run linter**: `pylint generated_code.py`
3. If linting fails:
   - Review each error message
   - Fix the issues
   - Run linter again
4. **Only proceed when linting passes**
5. Run tests: `pytest tests/`
````

### Implementation: Reference-Based Feedback Loop

For tasks without executable validators, use reference documents:

````markdown
## Content review process

1. Draft your content following the guidelines in STYLE_GUIDE.md
2. Review against the checklist:
   - Check terminology consistency
   - Verify examples follow the standard format
   - Confirm all required sections are present
3. If issues found:
   - Note each issue with specific section reference
   - Revise the content
   - Review the checklist again
4. Only proceed when all requirements are met
5. Finalize and save the document
````

The "validator" is STYLE_GUIDE.md, and Claude performs the check by reading and comparing.

## When to Use Validation Patterns

### Decision Framework

**Use plan-validate-execute when**:
- Batch operations (>10 items)
- Destructive changes (deletes, overwrites)
- Complex business rules
- High error cost

**Use validate script when**:
- Structured data editing
- Format compliance required
- Programmatic validation possible
- Medium error cost

**Use feedback loop when**:
- Quality improvement through iteration
- Multiple valid approaches
- Subjective quality criteria
- Low to medium error cost

**Skip validation when**:
- Single simple operations
- Read-only tasks
- Low error cost
- Quick exploratory work

### Cost-Benefit Analysis

**Validation adds value when**:
- Error cost > time to write validator
- Operation runs repeatedly
- Errors are common
- Manual checking is tedious

**Skip validation when**:
- One-time operation
- Errors are obvious and harmless
- Manual review is quick
- Operation is trivial

## Implementation Examples

### Example 1: PDF Form Batch Update (Plan-Validate-Execute)

**Problem**: Update 50 form fields based on spreadsheet data. Without validation, Claude might reference non-existent fields or apply incorrect values.

**Solution**:

````markdown
## Batch form update workflow

**Step 1: Analyze**
```bash
python scripts/analyze_form.py template.pdf > fields.json
```

**Step 2: Create plan**

Review `data.xlsx` and create `changes.json`:
```json
{
  "updates": [
    {"form_field": "customer_name", "spreadsheet_column": "Name"},
    {"form_field": "order_date", "spreadsheet_column": "Date"}
  ]
}
```

**Step 3: Validate plan**
```bash
python scripts/validate_mapping.py changes.json fields.json data.xlsx
```

This checks:
- All form fields exist in the PDF
- All spreadsheet columns exist in the Excel file
- Data types are compatible

**Step 4: Execute**
```bash
python scripts/apply_updates.py template.pdf data.xlsx changes.json output.pdf
```

**Step 5: Verify**
```bash
python scripts/verify_output.py output.pdf changes.json
```
````

### Example 2: OOXML Document Editing (Validate Script)

**Problem**: Editing Office Open XML files requires valid XML. Small syntax errors break the document.

**Solution**:

````markdown
## DOCX editing workflow

1. Unpack the .docx file:
   ```bash
   python scripts/unpack.py input.docx unpacked_dir/
   ```

2. Make your edits to `unpacked_dir/word/document.xml`

3. **Validate immediately** after each edit:
   ```bash
   python scripts/validate_xml.py unpacked_dir/
   ```

4. If validation fails:
   - Read the error message carefully
   - Fix the XML syntax or structure
   - Validate again
   - **Repeat until validation passes**

5. Only when validation passes, repack:
   ```bash
   python scripts/pack.py unpacked_dir/ output.docx
   ```

6. Test by opening output.docx in Word
````

### Example 3: Code Generation (Feedback Loop)

**Problem**: Generated code often has style issues or minor bugs that linting can catch.

**Solution**:

````markdown
## API client generation

1. Generate the client code based on OpenAPI spec
2. Save to `generated_client.py`
3. **Run linter**:
   ```bash
   pylint generated_client.py
   ```
4. Review linting errors and fix issues:
   - Import order problems → reorganize imports
   - Line length violations → break long lines
   - Type hint issues → add or fix type hints
5. **Run linter again** until score >9.0
6. **Run tests**:
   ```bash
   pytest tests/test_client.py
   ```
7. If tests fail, fix issues and return to step 3
````

### Example 4: Report Generation (Reference-Based)

**Problem**: Reports must follow company style guide. No executable validator exists.

**Solution**:

````markdown
## Generate quarterly report

1. Gather data from sources in DATASOURCES.md
2. Draft report following structure in TEMPLATE.md
3. **Self-review** against STYLE_GUIDE.md:
   - Terminology: Check all terms match GLOSSARY.md
   - Formatting: Verify headings, bullets, spacing match TEMPLATE.md
   - Completeness: Confirm all required sections present
4. For each issue found:
   - Note the section and specific problem
   - Make the correction
   - Review that section again
5. **Final check**: Read entire report against checklist in STYLE_GUIDE.md
6. Only when all items pass, save final version
````

## Common Mistakes

### Mistake 1: Validation Too Late

**Problem**: Waiting until the end to validate means many errors accumulate.

**Bad**:
```markdown
1. Edit 50 files
2. Make complex changes
3. Validate everything at the end
```

**Good**:
```markdown
1. Edit file 1
2. Validate file 1
3. Edit file 2
4. Validate file 2
[repeat]
```

Validate after each unit of work, not after all work.

### Mistake 2: Vague Validation Errors

**Problem**: Generic error messages don't help Claude fix issues.

**Bad**:
```python
if error:
    print("Validation failed")
```

**Good**:
```python
if field not in valid_fields:
    print(f"Field '{field}' not found in form")
    print(f"Available fields: {', '.join(valid_fields)}")
    print(f"Check line {line_num} in changes.json")
```

### Mistake 3: No Workflow Checklist

**Problem**: Complex workflows are hard to track mentally.

**Bad**:
```markdown
## Process

Follow these steps to update the forms...
[long prose description]
```

**Good**:
````markdown
## Process

Copy this checklist:
```
- [ ] Step 1: Analyze
- [ ] Step 2: Create plan
- [ ] Step 3: Validate plan
- [ ] Step 4: Execute
- [ ] Step 5: Verify
```

**Step 1: Analyze**
...
````

Checklists help both Claude and users track progress.

### Mistake 4: Skipping Validation for "Simple" Tasks

**Problem**: Assuming a task is too simple to need validation.

Even simple operations benefit from validation when:
- They run frequently
- Errors are annoying to fix manually
- Correctness matters

**Example**: Validating JSON files before git commit prevents pushing broken config.

### Mistake 5: Validation Without Clear Recovery

**Problem**: Script says "validation failed" but doesn't explain how to fix it or what to do next.

**Bad**:
```markdown
Run validation. If it fails, fix the errors.
```

**Good**:
```markdown
Run validation: `python scripts/validate.py input.json`

If validation fails:
1. Read the error message carefully - it shows the exact problem
2. Edit `input.json` to fix the issue
3. Run validation again
4. Repeat until validation passes
5. Only then proceed to the next step

If you can't resolve a validation error, see [references/validation-errors.md](references/validation-errors.md) for common issues and solutions.
```

## Summary

**Create verifiable intermediate outputs** (plan-validate-execute):
- Use for batch operations and high-stakes changes
- Create structured plan file
- Validate plan before execution
- Iterate on plan without touching originals

**Validate script pattern**:
- Use for structured data and format compliance
- Validate after each significant change
- Provide specific error messages
- Repeat until validation passes

**Feedback loop pattern**:
- Use for iterative quality improvement
- Check quality after each iteration
- Fix issues and repeat
- Can use scripts or reference documents

**Key principle**: Validate early and often. Catch errors before they compound.

**Implementation tips**:
- Make validators verbose with specific errors
- Provide workflow checklists for complex processes
- Validate after each unit of work, not at the end
- Explain recovery process when validation fails
