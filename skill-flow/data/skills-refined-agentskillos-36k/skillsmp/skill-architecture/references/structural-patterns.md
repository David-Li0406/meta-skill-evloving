**Skill**: [Skill Architecture](../SKILL.md)

# Structural Patterns

Four canonical patterns for organizing skill content based on use case.

## Pattern 1: Workflow Pattern

**For**: Sequential multi-step procedures

**Structure**:

- SKILL.md: High-level workflow overview
- references/: Detailed step-by-step instructions
- scripts/: Automation for repeated steps

**Example**: `deployment-workflow`

```
deployment-workflow/
├── SKILL.md (workflow overview)
├── references/
│   ├── staging-deployment.md
│   ├── production-deployment.md
│   └── rollback-procedures.md
└── scripts/
    ├── deploy.sh
    └── healthcheck.py
```

## Pattern 2: Task Pattern

**For**: Specific, bounded tasks

**Structure**:

- SKILL.md: Task definition + execution guidance
- scripts/: Task implementation
- assets/: Templates if needed

**Example**: `pdf-editor`

```
pdf-editor/
├── SKILL.md (rotate, merge, split PDFs)
└── scripts/
    ├── rotate_pdf.py
    ├── merge_pdfs.py
    └── split_pdf.py
```

## Pattern 3: Reference Pattern

**For**: Knowledge repository / domain expertise

**Structure**:

- SKILL.md: Overview + navigation guide
- references/: Comprehensive documentation
- Assets: Schemas, diagrams if applicable

**Example**: `company-policies`

```
company-policies/
├── SKILL.md (policy overview + grep patterns)
└── references/
    ├── hr-policies.md (10k+ words)
    ├── security-policies.md
    └── compliance-guidelines.md
```

**Best practice**: Include grep patterns in SKILL.md for large references:

```markdown
## Finding Information

Use grep to search policies:

- Security: `grep -i "password" references/security-policies.md`
- HR: `grep -i "vacation" references/hr-policies.md`
```

## Pattern 4: Capabilities Pattern

**For**: Tool integrations / API interactions

**Structure**:

- SKILL.md: Capability overview + common tasks
- references/: API docs, schemas
- scripts/: API wrappers
- assets/: Configuration templates

**Example**: `bigquery-integration`

```
bigquery-integration/
├── SKILL.md (query patterns + common tasks)
├── references/
│   └── schema.md (table documentation)
├── scripts/
│   └── query_wrapper.py
└── assets/
    └── config-template.json
```

## Choosing a Pattern

| Use Case           | Pattern      | Key Indicator                            |
| ------------------ | ------------ | ---------------------------------------- |
| Multi-step process | Workflow     | "Then do X, then Y, then Z"              |
| Single capability  | Task         | "Rotate this PDF" or "Deploy to staging" |
| Knowledge base     | Reference    | "What's our policy on X?"                |
| External system    | Capabilities | "Query BigQuery" or "Call API"           |

## Combining Patterns

Complex skills can combine patterns:

```
data-pipeline/
├── SKILL.md (Workflow: ingest → transform → load)
├── references/
│   └── schema.md (Reference: data schemas)
└── scripts/
    ├── ingest.py (Task: data ingestion)
    ├── transform.py (Task: transformations)
    └── load.py (Capabilities: BigQuery upload)
```
