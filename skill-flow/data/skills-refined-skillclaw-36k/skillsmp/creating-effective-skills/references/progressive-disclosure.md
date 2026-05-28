# Progressive Disclosure Patterns

Detailed guidance on implementing progressive disclosure in agent skills.

## Table of Contents

- Three-Level Loading System
- Pattern 1: High-Level Guide with References
- Pattern 2: Domain-Specific Organization
- Pattern 3: Conditional Details
- Pattern 4: Framework/Variant Organization
- Guidelines for Effective Progressive Disclosure
- Common Mistakes to Avoid

## Three-Level Loading System

Skills use a three-level loading system to manage context efficiently:

### Level 1: Metadata (Always Loaded)

**Content**: YAML frontmatter (`name` and `description`)
**Token cost**: ~100 tokens per skill
**When loaded**: At startup, included in system prompt

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

Claude loads this for all installed skills. Lightweight approach means you can install many skills without context penalty.

### Level 2: Instructions (Loaded When Triggered)

**Content**: SKILL.md body
**Token cost**: <5k tokens (keep under 500 lines)
**When loaded**: When user request matches skill description

The main body contains procedural knowledge: workflows, best practices, guidance.

````markdown
# PDF Processing

## Quick start

Use pdfplumber to extract text:

```python
import pdfplumber
with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For advanced form filling, see [FORMS.md](references/FORMS.md).
````

Claude reads SKILL.md from filesystem via bash when the skill triggers.

### Level 3: Resources and Code (Loaded As Needed)

**Content**: Reference files, scripts, assets
**Token cost**: Effectively unlimited
**When loaded**: Only when referenced and needed

```
pdf-skill/
├── SKILL.md (main instructions)
├── references/
│   ├── FORMS.md (form-filling guide)
│   └── REFERENCE.md (detailed API reference)
└── scripts/
    └── fill_form.py (utility script)
```

Claude accesses these only when SKILL.md references them or Claude determines they're needed.

## Pattern 1: High-Level Guide with References

Best for skills with multiple feature areas that aren't always all needed.

### Structure

```
skill-name/
├── SKILL.md (overview + quick start)
└── references/
    ├── FEATURE_A.md (detailed guide for feature A)
    ├── FEATURE_B.md (detailed guide for feature B)
    └── REFERENCE.md (comprehensive API reference)
```

### SKILL.md Example

````markdown
# Document Processing

## Quick start

Basic document creation:

```python
from docx import Document
doc = Document()
doc.add_paragraph("Hello world")
doc.save("output.docx")
```

## Advanced features

**Form filling**: See [references/FORMS.md](references/FORMS.md) for complete guide
**API reference**: See [references/REFERENCE.md](references/REFERENCE.md) for all methods
**Examples**: See [references/EXAMPLES.md](references/EXAMPLES.md) for common patterns
**Tracked changes**: See [references/REDLINING.md](references/REDLINING.md) for working with revisions
````

### When to Use

- Skill has multiple distinct features
- Not all features are used in every request
- Each feature has substantial documentation

### Benefits

- Keep SKILL.md focused on essentials
- Claude loads only relevant feature documentation
- Easy to extend with new features

## Pattern 2: Domain-Specific Organization

Best for skills that work with multiple domains or data sources.

### Structure

```
bigquery-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

### SKILL.md Example

````markdown
# BigQuery Data Analysis

## Available Datasets

**Finance**: Revenue, ARR, billing → See [references/finance.md](references/finance.md)
**Sales**: Opportunities, pipeline, accounts → See [references/sales.md](references/sales.md)
**Product**: API usage, features, adoption → See [references/product.md](references/product.md)
**Marketing**: Campaigns, attribution, email → See [references/marketing.md](references/marketing.md)

## Quick Search

Find specific metrics using grep:

```bash
grep -i "revenue" references/finance.md
grep -i "pipeline" references/sales.md
grep -i "api usage" references/product.md
```

## Query Template

```sql
SELECT
  [columns]
FROM
  [table from domain schema]
WHERE
  [filters]
```

Check the domain reference file for available tables and columns.
````

### When to Use

- Skill works with multiple data domains
- Each domain has distinct schemas or concepts
- User requests typically focus on one domain at a time

### Benefits

- When user asks about sales, Claude only loads sales.md
- Avoids loading irrelevant domain information
- Scales well as you add new domains

## Pattern 3: Conditional Details

Best for skills where basic usage is simple but advanced features are complex.

### Structure

```
skill-name/
├── SKILL.md (basic usage + conditional links)
└── references/
    ├── ADVANCED_FEATURE.md (detailed guide)
    └── OOXML.md (technical details)
```

### SKILL.md Example

````markdown
# DOCX Processing

## Creating Documents

Use docx-js for new documents. See [references/DOCX-JS.md](references/DOCX-JS.md).

## Editing Documents

For simple edits, modify the XML directly.

**For tracked changes**: See [references/REDLINING.md](references/REDLINING.md)
**For OOXML details**: See [references/OOXML.md](references/OOXML.md)

## Basic Template

```python
from docx import Document

doc = Document()
doc.add_heading('Title', 0)
doc.add_paragraph('Content')
doc.save('output.docx')
```
````

### When to Use

- Basic usage covers 80% of cases
- Advanced features are infrequently needed
- Advanced features have substantial complexity

### Benefits

- Most users see only what they need
- Advanced users can access detailed information
- SKILL.md remains approachable for common cases

## Pattern 4: Framework/Variant Organization

Best for skills supporting multiple frameworks, platforms, or implementation variants.

### Structure

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

### SKILL.md Example

````markdown
# Cloud Deployment

## Workflow

1. Choose cloud provider based on requirements
2. Review provider-specific patterns
3. Follow deployment steps for chosen provider

## Provider Selection

**AWS**: See [references/aws.md](references/aws.md) for ECS, Lambda, EC2 patterns
**GCP**: See [references/gcp.md](references/gcp.md) for Cloud Run, Functions, GCE patterns
**Azure**: See [references/azure.md](references/azure.md) for Container Instances, Functions, VMs

## General Deployment Steps

1. Build container image
2. Push to registry
3. Deploy to chosen platform
4. Configure networking and permissions
5. Verify deployment

Provider-specific implementation details are in the respective reference files.
````

### When to Use

- Skill supports multiple frameworks or platforms
- Each variant has distinct patterns and syntax
- User chooses one variant per request

### Benefits

- Core workflow stays unified
- Claude loads only the chosen variant's details
- Easy to add support for new frameworks

## Guidelines for Effective Progressive Disclosure

### Keep SKILL.md Under 500 Lines

Target: 300-400 lines for most skills. This leaves room for context without dominating it.

### Use Clear Navigation

Make it obvious what content exists and where to find it:

```markdown
## Advanced Features

**Feature A**: See [references/feature-a.md](references/feature-a.md) - Description
**Feature B**: See [references/feature-b.md](references/feature-b.md) - Description
```

### Keep References One Level Deep

**Bad** (nested references):
```markdown
# SKILL.md
See [advanced.md](references/advanced.md)...

# references/advanced.md
See [details.md](references/details.md)...

# references/details.md
Here's the actual information...
```

**Good** (one level deep):
```markdown
# SKILL.md

**Basic usage**: [instructions in SKILL.md]
**Advanced features**: See [references/advanced.md](references/advanced.md)
**API reference**: See [references/api.md](references/api.md)
**Examples**: See [references/examples.md](references/examples.md)
```

### Structure Long Reference Files

For files longer than 100 lines, include table of contents:

```markdown
# API Reference

## Table of Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
- Code examples

## Authentication and Setup
...
```

This ensures Claude can see the full scope even when previewing with partial reads.

### Avoid Duplication

Information should live in either SKILL.md or references, not both.

**Prefer references for**:
- Detailed schemas
- Comprehensive API documentation
- Extensive examples
- Domain-specific details

**Keep in SKILL.md**:
- Essential procedural instructions
- Core workflow guidance
- Navigation to references
- Quick start examples

### Use Descriptive File Names

**Good**:
- `references/database-schemas.md`
- `references/api-authentication.md`
- `references/error-handling-patterns.md`

**Bad**:
- `references/doc1.md`
- `references/stuff.md`
- `references/misc.md`

## Common Mistakes to Avoid

### Mistake 1: Putting Everything in SKILL.md

**Problem**: SKILL.md becomes 2000+ lines, always consuming huge context.

**Solution**: Extract detailed content to references. Keep SKILL.md focused on essentials.

### Mistake 2: Too Many Small Files

**Problem**: 50 tiny reference files, each 10-20 lines.

**Solution**: Group related content. One `database-schemas.md` is better than 10 tiny table files.

### Mistake 3: No Clear Navigation

**Problem**: Reference files exist but aren't mentioned in SKILL.md.

**Solution**: Always link to references from SKILL.md with clear descriptions.

### Mistake 4: Duplicate Information

**Problem**: Same content appears in both SKILL.md and reference files.

**Solution**: Choose one location. Usually references for details, SKILL.md for workflow.

### Mistake 5: Nested References

**Problem**: references/advanced.md references references/details.md

**Solution**: Keep all references one level from SKILL.md. Flatten the structure.

## Example: Well-Designed Progressive Disclosure

```
excel-analysis/
├── SKILL.md (~400 lines)
└── references/
    ├── formulas.md (comprehensive formula reference)
    ├── pivot-tables.md (pivot table guide)
    ├── charts.md (chart creation patterns)
    └── data-validation.md (validation rules)
```

**SKILL.md**:
````markdown
---
name: excel-analysis
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
---

# Excel Analysis

## Quick Start

Read Excel file:
```python
import pandas as pd
df = pd.read_excel('data.xlsx')
```

## Core Workflows

**Data analysis**: Load, transform, analyze with pandas
**Pivot tables**: See [references/pivot-tables.md](references/pivot-tables.md)
**Charts**: See [references/charts.md](references/charts.md)
**Formulas**: See [references/formulas.md](references/formulas.md)

## Basic Analysis Template

[Template here]
````

**Result**:
- Metadata always loaded (~100 tokens)
- SKILL.md loaded when triggered (~2k tokens)
- References loaded only when needed (0 tokens until accessed)

Total context: ~100 tokens at rest, ~2.1k when triggered, more only if needed.
