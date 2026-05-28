# Skill Examples

Complete examples of well-structured skills demonstrating best practices.

## Contents

- [Example 1: Simple Skill (Single File)](#example-1-simple-skill)
- [Example 2: Skill with References](#example-2-skill-with-references)
- [Example 3: Skill with Scripts](#example-3-skill-with-scripts)
- [Example 4: Domain-Specific Skill](#example-4-domain-specific-skill)

---

## Example 1: Simple Skill

A focused skill that fits entirely in SKILL.md (~150 lines).

**Directory structure:**

```
creating-enums/
└── SKILL.md
```

**SKILL.md:**

```yaml
---
name: creating-enums
description: Create PHP backed enums for representing fixed sets of values with type safety. Use when creating enums, defining constants, representing states, or when user mentions enums, enum types, constant values, or state machines.
---
# Creating Enums

Enums represent fixed sets of possible values with full type safety.
## File Location
```

app/Enums/{Domain}/{Name}.php

````

## Structure

```php
<?php

declare(strict_types=1);

namespace App\Enums\{Domain};

enum {Name}: string
{
    case CaseName = 'value';
    case AnotherCase = 'another_value';

    /**
     * @return list<self>
     */
    public static function active(): array
    {
        return [self::CaseName];
    }
}
````

## Conventions

- Use backed enums (`string` or `int`)
- PascalCase for case names
- snake_case for string values
- Add helper methods for grouping cases

## Usage with Eloquent

```php
protected function casts(): array
{
    return ['status' => OrderStatus::class];
}
```

```

**Why this works:**
- Description includes action + triggers + keywords
- Body is concise and actionable
- No verbose explanations
- Under 150 lines total

---

## Example 2: Skill with References

A skill using progressive disclosure for detailed content.

**Directory structure:**
```

creating-actions/
├── SKILL.md
└── references/
├── patterns.md
└── examples.md

````

**SKILL.md:**
```yaml
---
name: creating-actions
description: Create Laravel Action classes for business logic operations following domain-driven design. Use when creating Actions, implementing business logic, handling user operations, or when user mentions Action classes, domain operations, business rules, or service classes.
---

# Creating Actions

Actions encapsulate business logic in single-purpose classes, keeping controllers thin.

## File Location

````

app/Actions/{Domain}/{Name}Action.php

````

## Structure

```php
<?php

declare(strict_types=1);

namespace App\Actions\{Domain};

final readonly class {Name}Action
{
    public function __construct(
        private DependencyOne $dep
    ) {}

    public function handle({Name}Data $data): {ReturnType}
    {
        // Business logic
        return $result;
    }
}
````

## Core Conventions

- Always `final readonly` when using constructor injection
- Single `handle()` method as entry point
- Accept DTOs for external data, primitives for internal
- Return domain objects, never HTTP responses

## Input/Output

**Use DTOs when:**

- Data comes from HTTP requests
- 3+ parameters needed
- Type safety is critical

**Use primitives when:**

- Internal service calls
- Single parameter operations
- Data already validated

## References

- [references/patterns.md](references/patterns.md) - Advanced patterns (composition, transactions, exceptions)
- [references/examples.md](references/examples.md) - Complete working examples from codebase

```

**references/patterns.md** would contain:
- Action composition patterns
- Database transaction handling
- Exception handling strategies
- Private helper methods

**Why this works:**
- Core workflow in SKILL.md (~80 lines)
- Advanced patterns in separate file
- Clear navigation to references
- Each file is focused

---

## Example 3: Skill with Scripts

A skill including executable scripts for deterministic operations.

**Directory structure:**
```

pdf-processing/
├── SKILL.md
├── scripts/
│ ├── extract_text.py
│ └── fill_form.py
└── references/
└── forms.md

````

**SKILL.md:**
```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
---

# PDF Processing

Process PDF documents using Python libraries and bundled scripts.

## Quick Start

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
text = reader.pages[0].extract_text()
````

## Text Extraction

Run the extraction script:

```bash
python scripts/extract_text.py input.pdf output.txt
```

## Form Filling

For PDF forms, see [references/forms.md](references/forms.md) for the complete workflow.

Quick version:

```bash
python scripts/fill_form.py form.pdf data.json output.pdf
```

## Merge PDFs

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as f:
    writer.write(f)
```

```

**Why this works:**
- Scripts executed without loading into context
- Reference file for complex workflow (forms)
- Quick examples in SKILL.md
- Under 100 lines

---

## Example 4: Domain-Specific Skill

A skill with multiple domain variants using progressive disclosure.

**Directory structure:**
```

bigquery-analysis/
├── SKILL.md
└── references/
├── finance.md
├── sales.md
└── product.md

````

**SKILL.md:**
```yaml
---
name: bigquery-analysis
description: Query and analyze BigQuery datasets for business intelligence. Use when analyzing data, writing SQL queries, or when user mentions BigQuery, analytics, metrics, or data analysis.
---

# BigQuery Analysis

Query company datasets with proper schemas and naming conventions.

## Connection

```python
from google.cloud import bigquery
client = bigquery.Client(project="company-data")
````

## Available Datasets

**Finance** - Revenue, ARR, billing metrics
See [references/finance.md](references/finance.md)

**Sales** - Opportunities, pipeline, accounts
See [references/sales.md](references/sales.md)

**Product** - API usage, features, adoption
See [references/product.md](references/product.md)

## Query Pattern

```sql
SELECT
    date,
    metric_name,
    SUM(value) as total
FROM `project.dataset.table`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1, 2
ORDER BY 1
```

## Find Specific Tables

```bash
grep -i "revenue" references/finance.md
grep -i "pipeline" references/sales.md
```

````

**references/finance.md** would contain:
- Table schemas for revenue, billing, ARR
- Common queries for financial metrics
- Field definitions and relationships

**Why this works:**
- Domain selection in SKILL.md
- Detailed schemas in separate files
- Agent reads only relevant domain file
- Grep patterns for discovery in large files

---

## Description Patterns

### Pattern 1: Capability + Triggers + Keywords

```yaml
description: [What it does]. Use when [contexts] or when user mentions [keywords].
````

### Pattern 2: Multiple Capabilities

```yaml
description: [Capability 1], [Capability 2], and [Capability 3]. Use when [context] or when user mentions [keyword1], [keyword2], or [keyword3].
```

### Real Examples

```yaml
# Good: Specific with triggers
description: Create Laravel Form Request classes for validation with toDTO() conversion methods. Use when creating form requests, validating input, handling validation rules, or when user mentions form requests, validation, request validation, or input validation.

# Good: Multiple capabilities
description: Run Laravel quality checks including Rector, Pint, PHPStan, code coverage, and type coverage. Use when ensuring code quality, before committing, running quality checks, or when user mentions quality, checks, Rector, Pint, PHPStan, coverage, or composer checks.

# Bad: Too vague
description: Helps with validation

# Bad: Missing triggers
description: Create form request classes

# Bad: Wrong person
description: I can help you create form requests
```
