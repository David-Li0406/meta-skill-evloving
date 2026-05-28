# Skill Analysis Examples

Examples of common mistakes and patterns to identify when analyzing existing skills.

## Common Mistakes and Fixes

### Mistake 1: Including Information Claude Already Knows

#### ❌ Bad
```markdown
# Processing JSON Data

## What is JSON?
JSON stands for JavaScript Object Notation. It's a lightweight data format
that uses key-value pairs. Here's how to parse JSON in Python:

```python
import json
data = json.loads(string)
```
```

**Problem:** Claude already knows what JSON is and how to parse it

---

#### ✅ Good
```markdown
# Processing JSON Data

## Company-Specific JSON Schema
Our API returns JSON with the following proprietary structure:

```json
{
  "acme_transaction_id": "unique identifier format: ACME-YYYY-NNNNN",
  "legacy_ref": "maps to old system field 'trans_code'",
  "amount_cents": "always in cents, not dollars"
}
```

**Important:** `amount_cents` must be divided by 100 for display.
```

**Why better:** Contains company-specific knowledge Claude doesn't have

---

### Mistake 2: Vague Workflow Steps

#### ❌ Bad
```markdown
## Workflow
1. Get the data
2. Process it
3. Output results
```

**Problem:** No actionable guidance, too vague

---

#### ✅ Good
```markdown
## Workflow

### Step 1: Validate Input Data
- [ ] Check required fields present: `company_name`, `fiscal_year`, `revenue`
- [ ] Verify numeric fields are valid numbers
- [ ] Ensure dates in ISO format (YYYY-MM-DD)

### Step 2: Calculate Ratios
- [ ] Run calculate_ratios.py with validated data
- [ ] Verify output contains all 15 expected ratios
- [ ] Check for calculation errors (None, NaN, Inf)

### Step 3: Generate Report
- [ ] Format results using report-template.md
- [ ] Include industry benchmarks from benchmarks.csv
- [ ] Export to Excel with formatting
```

**Why better:** Specific, actionable, includes validation

---

### Mistake 3: Deep File Nesting

#### ❌ Bad Structure
```
SKILL.md says: "See main-guide.md for details"
main-guide.md says: "For specifics, see detailed-specs.md"
detailed-specs.md says: "For examples, see examples-appendix.md"
```

**Problem:** Agent must load 4 files to get information, context overload

---

#### ✅ Good Structure
```
SKILL.md says: "See detailed-specs.md for API endpoints"
SKILL.md says: "See examples.md for usage examples"

detailed-specs.md: Complete API specifications
examples.md: Complete usage examples
```

**Why better:** One level deep, clear purpose, no chaining

---

### Mistake 4: Time-Sensitive Conditionals

#### ❌ Bad
```markdown
## API Endpoint Selection

If current date is before January 1, 2024:
  Use https://api.example.com/v1/data

If current date is after January 1, 2024:
  Use https://api.example.com/v2/data
```

**Problem:** Will become outdated and confusing

---

#### ✅ Good
```markdown
## API Endpoint Selection

### Current Approach
Use https://api.example.com/v2/data for all requests

### Old Patterns
Previous implementations used /v1/data endpoint.
The v1 endpoint is deprecated and should not be used.
Migration to v2 was completed and all systems now use v2.
```

**Why better:** No dates, clear about current vs old approach

---

### Mistake 5: Missing Validation Steps

#### ❌ Bad
```markdown
## Workflow
1. Load financial data
2. Calculate ratios using calculate_ratios.py
3. Done
```

**Problem:** No validation, errors could go unnoticed

---

#### ✅ Good
```markdown
## Workflow

### Step 1: Load Financial Data
- Load data from provided source
- **Validation:** Verify all required fields present

### Step 2: Calculate Ratios
- Run calculate_ratios.py with data
- **Validation:** Check script exit code is 0
- **Validation:** Verify output contains expected number of ratios
- If validation fails, review error messages and fix data

### Step 3: Verify Results
- [ ] All ratios calculated (no None/NaN values)
- [ ] Results within reasonable ranges
- [ ] Benchmark comparisons loaded successfully
```

**Why better:** Validation at each step, clear success criteria

---

## Validation Checklist Examples

### ❌ Vague Checklist
```markdown
## Validation
- [ ] Everything looks good
- [ ] No errors
- [ ] Results are correct
```

**Problem:** Not actionable, no specific criteria

---

### ✅ Specific Checklist
```markdown
## Validation Checklist

### Data Quality
- [ ] All required fields present (company_name, fiscal_year, revenue, expenses)
- [ ] No None or NaN values in numeric fields
- [ ] Dates in correct format (YYYY-MM-DD)
- [ ] Revenue > 0 and Expenses >= 0

### Calculation Verification
- [ ] All 15 ratios calculated successfully
- [ ] Profit Margin between -100% and 100%
- [ ] Current Ratio > 0
- [ ] Debt/Equity Ratio >= 0
- [ ] No division-by-zero errors

### Output Requirements
- [ ] Results formatted in specified template
- [ ] Industry benchmarks included
- [ ] Comparison charts generated
- [ ] Excel file created with proper formatting
- [ ] File naming follows convention: {company}_{year}_financial_analysis.xlsx
```

**Why better:** Specific, measurable, actionable criteria

---

## Quality Assessment Patterns

### YAML Frontmatter Red Flags

#### Name Issues
- ❌ Contains underscores: `process_data`
- ❌ Contains capitals: `ProcessData`
- ❌ Not gerund: `pdf-processor`
- ❌ Too vague: `helper`, `utils`, `tool`
- ❌ Too long: Over 64 characters

#### Description Issues
- ❌ No triggers: "Processes documents"
- ❌ Only "what", no "when": "Calculates financial ratios"
- ❌ Too technical without context: "Implements DCF using WACC"
- ❌ Over 1024 characters

### Content Red Flags

#### Structure Issues
- ❌ SKILL.md over 700 lines without progressive disclosure
- ❌ No "When to Use This Skill" section
- ❌ Workflow steps not numbered
- ❌ No validation checkpoints
- ❌ Deep file nesting (3+ levels)

#### Content Quality Issues
- ❌ Explains basic programming concepts
- ❌ Documents standard library functions
- ❌ Contains date-based conditionals
- ❌ Windows-specific paths (backslashes)
- ❌ Inconsistent terminology
- ❌ No company-specific information

#### Organization Issues
- ❌ Referenced files don't exist
- ❌ Orphaned files (created but never referenced)
- ❌ No clear when-to-load guidance for supporting files
- ❌ Scripts without error handling
- ❌ Dependencies not documented

---

## Analysis Checklist by Severity

### Critical Issues (Skill Won't Load/Work)
- [ ] YAML syntax invalid (missing delimiters, tabs, malformed)
- [ ] Name field missing or invalid format
- [ ] Description field empty
- [ ] Referenced files don't exist
- [ ] File named incorrectly (not SKILL.md)

### Major Issues (Skill Works But Significantly Suboptimal)
- [ ] Description has no triggers or very vague
- [ ] SKILL.md over 700 lines without splitting
- [ ] No clear workflow structure
- [ ] Missing critical validation steps
- [ ] Deep file nesting (3+ levels)
- [ ] Poor activation targeting (too broad or too narrow)
- [ ] Inconsistent terminology throughout
- [ ] No when-to-load guidance for supporting files

### Minor Issues (Could Be Improved)
- [ ] Description could be more specific
- [ ] SKILL.md 500-700 lines (consider splitting)
- [ ] Some redundant content
- [ ] Missing optional examples
- [ ] Terminology slightly inconsistent
- [ ] Could benefit from more validation checkpoints
- [ ] File organization could be clearer

---

## Conciseness Assessment

### Delete (Claude Already Knows)
- ❌ How to parse JSON in Python
- ❌ What DCF valuation means
- ❌ How to use pandas DataFrames
- ❌ General programming best practices
- ❌ Standard library documentation
- ❌ Basic software engineering principles
- ❌ Common design patterns
- ❌ How to write functions/classes

### Keep (Claude Doesn't Know)
- ✅ Company's proprietary JSON schema
- ✅ Specific DCF assumptions (85% retention rate, 3-year projection)
- ✅ Custom pandas calculations with company formulas
- ✅ Company's internal coding standards
- ✅ Internal API endpoints and authentication
- ✅ Proprietary data formats
- ✅ Company policies and thresholds
- ✅ Custom tool specifications

---

## Activation and Discovery Assessment

### Good Trigger Patterns
- ✅ Task-based: "analyzing", "validating", "processing", "generating"
- ✅ Domain-based: "financial statements", "API responses", "PDFs"
- ✅ Data format-based: "JSON files", "CSV data", "Excel spreadsheets"
- ✅ User language-based: "when user mentions [specific keywords]"
- ✅ Context-based: "when working with", "when creating", "when debugging"

### Poor Trigger Patterns
- ❌ Too generic: "helps with documents"
- ❌ Only technical jargon: "implements WACC calculations"
- ❌ No user language patterns
- ❌ Missing data format triggers
- ❌ No concrete action verbs

---

## Progressive Disclosure Assessment

### Good Progressive Disclosure
```markdown
# SKILL.md (250 lines)
## Workflow
1. Validate input
2. Process data (see processing-guide.md for detailed rules)
3. Generate output (see output-formats.md for specifications)

## When to Load Supporting Files
- processing-guide.md: Load when you need detailed validation rules
- output-formats.md: Load when formatting output
```

**Why good:**
- ✅ Main workflow clear and concise
- ✅ Supporting files loaded on-demand
- ✅ Clear guidance on when to load
- ✅ One level deep

### Poor Progressive Disclosure
```markdown
# SKILL.md (900 lines)
## Workflow
1. Validate input
   [200 lines of validation details]
2. Process data
   [400 lines of processing rules]
3. Generate output
   [300 lines of format specifications]
```

**Why poor:**
- ❌ Monolithic file, information overload
- ❌ All details loaded upfront
- ❌ Hard to navigate
- ❌ Over 500-line target

---

## Cross-Platform Compatibility Check

### Path Format Issues
- ❌ `C:\Users\file.txt` (Windows-specific)
- ❌ `scripts\process.py` (Windows-style backslash)
- ❌ Hardcoded platform paths

### Correct Path Format
- ✅ `C:/Users/file.txt` (forward slash works everywhere)
- ✅ `scripts/process.py` (forward slash)
- ✅ Relative paths with forward slashes

### Tool Availability Issues
- ❌ "Use jq to process JSON" (assumes tool installed)
- ✅ "Use jq if available, otherwise use Python json module"

---

## Documentation Completeness Check

### Required Documentation
- [ ] "When to Use This Skill" section present
- [ ] Clear workflow with numbered steps
- [ ] Validation criteria included
- [ ] Dependencies documented (if any)
- [ ] Success criteria defined

### Recommended Documentation
- [ ] Usage examples provided
- [ ] Error handling documented
- [ ] Supporting files purpose explained
- [ ] Troubleshooting guidance included
- [ ] Output format specified

### Nice-to-Have Documentation
- [ ] Edge cases documented
- [ ] Performance considerations noted
- [ ] Limitations clearly stated
- [ ] Version history (for frequently updated skills)

---

## Summary: Key Analysis Questions

When analyzing a skill, ask:

### Activation
- Will this activate when it should?
- Will it avoid false activations?
- Are triggers specific enough to be discoverable?

### Structure
- Is SKILL.md under 500 lines?
- If longer, is progressive disclosure used appropriately?
- Are workflows clear and actionable?

### Content
- Does it include only information Claude doesn't already know?
- Is terminology consistent throughout?
- Are validation steps included?

### Quality
- Would this work reliably across different scenarios?
- Is error handling addressed?
- Are dependencies documented?

### Usability
- Could someone else use this skill successfully?
- Is the workflow easy to follow?
- Are success criteria clear?
