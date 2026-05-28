# Skill Quick Reference

Fast validation cheat sheet for creating and checking skills. Use this for rapid pre-flight checks.

## YAML Frontmatter Requirements

```yaml
---
name: skill-name-here
description: What it does. When to use it. Trigger keywords.
---
```

**Rules:**
- Delimiters: `---` at start and end
- No tabs (spaces only)
- name: lowercase, hyphens, max 64 chars, gerund form
- description: max 1024 chars, non-empty, includes triggers

**Regex for name:** `^[a-z0-9-]{1,64}$`

---

## 60-Second Validation Checklist

Run through this before finalizing any skill:

### YAML
- [ ] Opening and closing `---` delimiters present
- [ ] name field: lowercase-with-hyphens, under 64 chars, gerund form
- [ ] description field: under 1024 chars, includes both "what" and "when"
- [ ] No tabs (use spaces)

### Content
- [ ] SKILL.md under 500 lines (if over, split with progressive disclosure)
- [ ] Clear "When to Use This Skill" section
- [ ] Numbered workflow steps with subsections
- [ ] Validation checkpoints in workflow
- [ ] No basic programming concepts or standard library docs
- [ ] Consistent terminology throughout

### Structure
- [ ] All referenced files exist
- [ ] File references one level deep (no chains)
- [ ] Forward slashes in paths
- [ ] Supporting files appropriately named

---

## Description Template (Fill-in-the-Blank)

```
[ACTION] [OBJECTS] [PURPOSE]. Use when [SCENARIO 1], [SCENARIO 2],
or when user [PROVIDES DATA FORMAT] or mentions [KEYWORD 1], [KEYWORD 2],
[KEYWORD 3].
```

**Example:**
```
Calculates financial ratios from statement data for investment analysis.
Use when analyzing company performance, evaluating investments, or when
user provides income statements, balance sheets, or mentions financial
ratios, ROE, or profitability metrics.
```

---

## Common Name Patterns

### ✅ Good Patterns
- `processing-[object]` → processing-pdfs
- `analyzing-[domain]` → analyzing-financial-statements
- `validating-[object]` → validating-api-responses
- `generating-[output]` → generating-reports
- `applying-[rules]` → applying-brand-guidelines
- `calculating-[metrics]` → calculating-ratios

### ❌ Avoid
- Generic: helper, utils, tool, processor
- Underscores: process_data
- Not gerund: pdf-processor, data-tool
- Too long: >64 characters

---

## Top 5 Mistakes and Quick Fixes

| Mistake | Quick Fix |
|---------|-----------|
| **Vague description** | Add 3-5 specific trigger keywords and data formats |
| **SKILL.md >500 lines** | Split into SKILL.md (workflow) + supporting files (details) |
| **No validation steps** | Add checklist at end of each workflow step |
| **Includes basic programming** | Delete anything Claude already knows, keep only domain-specific |
| **Deep file nesting** | Flatten: all files referenced directly from SKILL.md |

---

## File Structure Decision Tree

```
Is SKILL.md under 500 lines?
├─ YES → Keep single file ✅
└─ NO → Split it
    │
    ├─ Has detailed reference specs? → Create REFERENCE.md
    ├─ Has complex workflows? → Create workflow-guide.md
    ├─ Has many examples? → Create examples.md
    ├─ Has error scenarios? → Create error-handling.md
    └─ Has validation rules? → Create validation-rules.md
```

---

## Progressive Disclosure Pattern

**SKILL.md (workflow + when to load):**
```markdown
## Step 2: Apply Brand Colors
- Identify document type
- Load color specifications from REFERENCE.md
- Apply to document elements

## When to Load REFERENCE.md
Load when you need:
- Exact RGB/Hex color codes
- Typography specifications
- Template formats
```

**REFERENCE.md (details):**
```markdown
# Brand Color Specifications

## Primary Colors
- Acme Blue: #0066CC (RGB: 0, 102, 204)
- Acme Navy: #003366 (RGB: 0, 51, 102)
[...]
```

---

## Workflow Structure Template

```markdown
## Workflow: [Name]

### Step 1: [Action Name]
Brief description of what happens.

**Actions:**
- [ ] Specific action item
- [ ] Specific action item

**Validation:**
- Check [specific criterion]
- Verify [specific requirement]

### Step 2: [Action Name]
[Repeat pattern...]

**Decision Point:**
- If [condition] → Step 3
- If [other condition] → Step 4
```

---

## Essential File Organization

### Simple Skill
```
skill-name/
└── SKILL.md (<500 lines)
```

### With Scripts
```
skill-name/
├── SKILL.md
└── script_name.py
```

### With Progressive Disclosure
```
skill-name/
├── SKILL.md (workflow)
└── reference.md (details)
```

### Complex
```
skill-name/
├── SKILL.md (workflow)
├── reference.md
├── examples.md
├── scripts/
│   └── process.py
└── templates/
    └── template.xlsx
```

---

## Validation Checklist Format

### ❌ Too Vague
```markdown
- [ ] Everything looks good
- [ ] No errors
```

### ✅ Specific
```markdown
### Data Quality
- [ ] All required fields present: company_name, fiscal_year, revenue
- [ ] No None/NaN values in numeric fields
- [ ] Dates in ISO format (YYYY-MM-DD)

### Calculations
- [ ] All 15 ratios calculated
- [ ] Profit margin between -100% and 100%
- [ ] No division-by-zero errors

### Output
- [ ] Results formatted per template
- [ ] File naming: {company}_{year}_analysis.xlsx
```

---

## Trigger Keywords Checklist

Good descriptions include triggers from multiple categories:

- [ ] **Task triggers:** "analyzing", "validating", "processing", "generating"
- [ ] **Domain triggers:** "financial statements", "PDFs", "API responses"
- [ ] **Data format triggers:** "JSON files", "Excel spreadsheets", "CSV data"
- [ ] **User language triggers:** "when user mentions [keyword]"

**Example combining all:**
```
Validates API responses against schemas. Use when testing APIs, debugging
integrations, or when user provides JSON responses, API documentation, or
mentions validation, schema verification, or endpoint testing.
```

---

## Conciseness Test

**Ask for every paragraph:** Does Claude already know this?

### ❌ Delete (Claude knows)
- How to parse JSON in Python
- What is a DCF model
- How to use pandas DataFrames
- General programming best practices

### ✅ Keep (Claude doesn't know)
- Your company's proprietary JSON schema
- Your specific DCF assumptions (85% retention rate)
- Your custom pandas calculations
- Your company's internal coding standards

---

## Time-Sensitive Content Fix

### ❌ Avoid
```markdown
If date is after 2024-01-01:
  Use new API endpoint
```

### ✅ Use Instead
```markdown
## Current Approach
Use https://api.example.com/v2/data

## Old Patterns
Previous implementations used /v1/data
Migration to v2 is complete
```

---

## Cross-Platform Path Format

### ❌ Wrong
```
C:\Users\file.txt
scripts\process.py
```

### ✅ Correct
```
C:/Users/file.txt
scripts/process.py
```

**Rule:** Always use forward slashes `/` even on Windows

---

## Skill vs Slash Command Decision

| Choose Skill | Choose Slash Command |
|--------------|---------------------|
| 3+ steps | Single prompt |
| Auto-discovery needed | User explicitly invokes |
| Multiple files | One file sufficient |
| Validation loops | Simple reminder |
| Domain expertise | Quick template |

---

## Pre-Flight Check (30 seconds)

Before considering a skill complete, verify:

1. **YAML valid?** Copy frontmatter to YAML validator
2. **Name format?** Matches `^[a-z0-9-]{1,64}$`
3. **Description triggers?** Has 3+ specific keywords
4. **Length OK?** SKILL.md under 500 lines
5. **No redundancy?** Only domain-specific info
6. **References flat?** One level deep max

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill not loading | Check YAML: delimiters, no tabs, required fields |
| Skill not activating | Add specific triggers to description |
| Too verbose | Remove info Claude knows, keep only company-specific |
| Hard to navigate | Split using progressive disclosure |
| File not found | Check paths use forward slashes, verify files exist |

---

## When to Use Which File

| You Need... | Load... |
|-------------|---------|
| Overall guidance | This quick-reference.md |
| Creating new skill | creation-checklist.md |
| Analyzing existing skill | analysis-framework.md |
| Deep best practices | best-practices.md |
| Examples and patterns | examples.md |
| Blank template | templates/skill-template.md |

---

## Success Criteria

A skill is ready when:
- ✅ Loads without errors (YAML valid)
- ✅ Activates appropriately (good triggers)
- ✅ Instructions followed correctly (clear workflow)
- ✅ Under 500 lines or properly split
- ✅ Only essential information included
- ✅ Team can use it successfully (if project skill)
