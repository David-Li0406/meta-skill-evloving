# Example: XLSX Spreadsheet Operations

**Source**: https://github.com/anthropics/skills/tree/main/document-skills/xlsx
**Pattern**: Production standards with zero-tolerance quality policy
**Use case**: Creating and editing Excel spreadsheets with financial modeling standards

## Key Sections from SKILL.md

### Requirements for Outputs (Upfront Section)

**All Excel files:**
- **Zero Formula Errors**: MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- **Preserve Existing Templates**: EXACTLY match existing format when modifying files

**Financial models:**
- Color Coding Standards
- Number Formatting Standards
- Formula Construction Rules

### Color Coding Standards

#### Industry-Standard Color Conventions
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs users will change
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention

### Number Formatting Standards

- **Years**: Format as text strings (e.g., "2024" not "2,024")
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers
- **Zeros**: Use number formatting to make all zeros "-"
- **Percentages**: Default to 0.0% format (one decimal)
- **Negative numbers**: Use parentheses (123) not minus -123

### CRITICAL: Use Formulas, Not Hardcoded Values

**❌ WRONG - Hardcoding Calculated Values**:
```python
# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000
```

**✅ CORRECT - Using Excel Formulas**:
```python
# Good: Let Excel calculate the sum
sheet['B10'] = '=SUM(B2:B9)'
```

### Common Workflow

1. Choose tool: pandas for data, openpyxl for formulas/formatting
2. Create/Load: Create new workbook or load existing file
3. Modify: Add/edit data, formulas, and formatting
4. Save: Write to file
5. **Recalculate formulas (MANDATORY IF USING FORMULAS)**:
   ```bash
   python recalc.py output.xlsx
   ```
6. Verify and fix any errors (script returns JSON with error details)

### Formula Verification Checklist

**Essential Verification:**
- [ ] Test 2-3 sample references: Verify they pull correct values
- [ ] Column mapping: Confirm Excel columns match (column 64 = BL, not BK)
- [ ] Row offset: Remember Excel rows are 1-indexed

**Common Pitfalls:**
- [ ] NaN handling: Check for null values
- [ ] Division by zero: Check denominators (#DIV/0!)
- [ ] Wrong references: Verify all cell references (#REF!)

### Interpreting recalc.py Output

```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,
  "total_formulas": 42,
  "error_summary": {
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

### Code Style Guidelines

```markdown
**IMPORTANT**: When generating Python code for Excel operations:
- Write minimal, concise Python code without unnecessary comments
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements
```

## Analysis

**What makes this work**:

1. **Zero-tolerance policy**: "ZERO formula errors" is non-negotiable
2. **Industry conventions**: Color coding from real financial modeling practice
3. **Mandatory validation**: recalc.py verification required before completion
4. **Formula vs hardcode emphasis**: Entire section dedicated to this critical distinction
5. **Verification checklists**: Quick checks to ensure formulas work
6. **JSON error format**: Structured output from validation script

## Unique Features

**Requirements Upfront**:
Starts with "Requirements for Outputs" section before any workflows. Sets standards first.

**Zero Formula Errors Policy**:
Absolute requirement stated multiple times throughout the document.

**Color Coding Standards**:
Industry-standard conventions with exact RGB values:
- Blue = inputs
- Black = formulas
- Green = cross-sheet
- Red = external files

**Formula vs Hardcode Section**:
Entire "CRITICAL" section showing wrong and right approaches with code examples.

**recalc.py Mandatory Workflow**:
Explicit requirement to run recalculation script after any formula work.

**JSON Error Output**:
Structured format showing error types, counts, and specific cell locations.

**Code Style Guidelines**:
Explicit instructions to write "minimal, concise Python code without unnecessary comments."

## Pattern Type

**Production quality with validation** - Enforces industry standards and automated validation.

## Key Takeaways

1. **Zero-tolerance policies work** - "ZERO formula errors" is clear and enforceable
2. **Industry standards matter** - Color coding from real financial modeling
3. **Automated validation** - recalc.py enforces quality without manual checking
4. **Formula vs hardcode** - Critical distinction emphasized with entire section
5. **Verification checklists** - Quick checks for common pitfalls
6. **Structured error output** - JSON format enables programmatic error handling
7. **Domain-specific rules** - Formatting conventions specific to finance
8. **Code style guidance** - Even covers how to write the Python code itself
