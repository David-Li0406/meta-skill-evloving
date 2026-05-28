# Skill Improvement Examples: Descriptions and Names

Before/After transformations for improving skill descriptions, names, and discoverability.

## Transformation 1: Vague to Specific

### ❌ Before
```yaml
---
name: document-helper
description: Helps with various document tasks
---

# Document Helper

This skill helps with documents. Use it when working with documents.

## What It Does
- Processes documents
- Formats content
- Validates things
```

**Problems:**
- Vague name ("helper")
- No specific triggers
- Unclear capabilities
- No actionable workflow

---

### ✅ After
```yaml
---
name: processing-pdfs
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when user mentions PDFs, document extraction, form filling, or PDF manipulation.
---

# Processing PDFs

Extract text, tables, and forms from PDF documents.

## When to Use This Skill
- User provides or mentions PDF files
- Task involves extracting data from PDFs
- Need to fill PDF forms programmatically
- Merging or splitting PDF documents

## Workflow

### Step 1: Identify PDF Task
Determine operation type:
- Extract text → Use PyPDF2 extraction
- Extract tables → Use tabula-py
- Fill forms → Use pdfrw
- Merge/split → Use PyPDF2 operations

### Step 2: Execute Operation
[Specific steps for each operation type...]
```

**Improvements:**
- ✅ Specific name and domain
- ✅ Clear capabilities listed
- ✅ Multiple specific triggers
- ✅ Actionable workflow with tools

---

## Transformation 2: Improving Description Specificity

### ❌ Before
```yaml
description: Processes financial data for analysis
```

**Problems:**
- Too vague
- No triggers
- No context for when to activate

---

### ✅ After
```yaml
description: Calculates key financial ratios and metrics from financial statement data for investment analysis. Use when analyzing company performance, evaluating investments, or when user provides income statements, balance sheets, or cash flow statements.
```

**Improvements:**
- ✅ Specific functionality: "calculates key financial ratios"
- ✅ Clear purpose: "for investment analysis"
- ✅ Multiple triggers: "analyzing company performance", "evaluating investments"
- ✅ Data format triggers: "income statements, balance sheets, cash flow statements"

---

## Transformation 3: Fixing Name Issues

### ❌ Before
```yaml
name: financial_data_processor_v2
```

**Problems:**
- Underscores not allowed
- Not gerund form
- Version suffix inappropriate

---

### ✅ After
```yaml
name: analyzing-financial-statements
```

**Improvements:**
- ✅ Gerund form ("analyzing")
- ✅ Hyphens instead of underscores
- ✅ No version suffix
- ✅ Clear and descriptive

---

## Key Patterns: Description and Name Improvements

### Fix Vague Names
- ❌ Bad: helper, utils, processor, manager, handler
- ✅ Good: processing-pdfs, analyzing-financial-statements, validating-json-schemas

### Add Specific Triggers to Descriptions
Include 3-5 triggers:
- **Task-based**: "analyzing", "evaluating", "processing"
- **Data format**: "PDF files", "income statements", "JSON data"
- **User language**: "when user mentions PDFs", "when working with financial data"
- **Context**: "for investment analysis", "to validate API responses"

### Description Formula
```
[What it does] + [specific capabilities] + Use when [trigger 1], [trigger 2], or when user [trigger 3].
```

**Example:**
"Extracts and transforms data from XML files including parsing, validation, and XPath queries. Use when working with XML data, processing configuration files, or when user mentions XML, XPath, or data extraction."
