# Archetype Templates

concrete structure for each skill archetype with real examples.

## workflow archetype

**structure:**
```
SKILL.md (~150-300 lines)
├── frontmatter (name, description with triggers)
├── when to use (table: use | skip)
├── decision trees (if complex routing needed)
├── workflow (numbered steps with inputs/outputs)
├── verification (commands to confirm completion)
├── references (links to detailed guides)
├── scripts (automation helpers)
└── anti-patterns (common mistakes)

references/
├── workflow-guide.md (detailed step breakdowns)
├── checkpoint-criteria.md (gate conditions)
└── examples.md (annotated walkthroughs)

scripts/
├── setup.sh (environment prep)
├── validate.sh (verification commands)
└── cleanup.sh (post-workflow cleanup)
```

**real examples:** loop, skill-improve, pr-audit

**workflow template signals:**
- sequential steps with dependencies
- checkpoints requiring validation
- multiple phases with handoffs
- state that persists across steps

---

## tool archetype

**structure:**
```
SKILL.md (~100-200 lines)
├── frontmatter (name, description with triggers)
├── when to use (table: use | skip)
├── workflow (input → process → output)
├── formats/constraints (supported inputs)
├── verification (artifact validation)
├── references (format specs, API docs)
├── scripts (deterministic operations)
└── anti-patterns (common mistakes)

references/
├── format-spec.md (schema, constraints)
├── api-reference.md (endpoints, params)
└── examples.md (sample inputs/outputs)

scripts/
├── process.sh (main transformation)
├── validate.sh (output verification)
└── convert.sh (format conversions)
```

**real examples:** imessage, dashboard (scaffold aspect)

**tool template signals:**
- deterministic input → output
- format/API manipulation
- idempotent operations
- artifact production

---

## domain archetype

**structure:**
```
SKILL.md (~100-180 lines)
├── frontmatter (name, description with triggers)
├── when to use (table: use | skip)
├── knowledge areas (what's covered)
├── lookup workflow (how to find info)
├── references (indexed domain docs)
└── anti-patterns (common mistakes)

references/
├── policies.md (rules, guidelines)
├── schemas.md (data structures)
├── faqs.md (common questions)
└── glossary.md (term definitions)
```

**real examples:** emil-kowalski (design domain)

**domain template signals:**
- reference/knowledge lookup
- policies and guidelines
- FAQ retrieval
- no sequential workflow

---

## hybrid patterns

### workflow + tool
workflow orchestrating tool operations.

```
SKILL.md
├── workflow steps reference tool scripts
├── Tool operations embedded in workflow
└── Verification includes artifact checks

Example: skill-create (workflow for creating tools)
```

### workflow + domain
workflow referencing domain knowledge.

```
SKILL.md
├── Workflow steps reference domain docs
├── Domain knowledge informs decisions
└── FAQs embedded in workflow guidance

Example: issue-context (workflow using codebase domain)
```

### tool + domain
tool with domain-specific rules.

```
SKILL.md
├── Tool operations constrained by domain
├── Format specs come from domain docs
└── Validation based on domain rules

Example: metaprompt-factory (tool with XML domain)
```

---

## template selection checklist

| question | yes → | no → |
|----------|-------|------|
| sequential steps? | workflow | → |
| checkpoints/gates? | workflow | → |
| input → transform → output? | tool | → |
| deterministic operations? | tool | → |
| knowledge lookup? | domain | → |
| policies/rules? | domain | → |
| multiple apply? | hybrid | → |

---

## content placement guide

| content type | location | example |
|--------------|----------|---------|
| triggers, anti-triggers | SKILL.md frontmatter | "create skill", "new skill" |
| quick decision logic | SKILL.md decision tree | archetype selection |
| step-by-step instructions | SKILL.md workflow | numbered steps |
| detailed format specs | references/ | api-reference.md |
| reusable commands | scripts/ | validate.sh |
| sample files | assets/ | template.yaml |

---

## sizing guidelines

| archetype | typical SKILL.md | references/ | scripts/ |
|-----------|------------------|-------------|----------|
| workflow | 150-300 lines | 2-4 files | 2-3 |
| tool | 100-200 lines | 1-3 files | 1-2 |
| domain | 100-180 lines | 3-5 files | 0-1 |
| hybrid | 200-370 lines | 3-6 files | 2-4 |

---

## minimum sections by archetype

| archetype | required SKILL.md sections | required references/ |
|-----------|----------------------------|----------------------|
| workflow | when to use, decision trees, workflow, verification, references, scripts, anti-patterns | workflow-guide.md, checkpoint-criteria.md |
| tool | when to use, workflow, formats/constraints, verification, references, scripts, anti-patterns | format-spec.md, api-reference.md |
| domain | when to use, knowledge areas, lookup workflow, references, anti-patterns | policies.md, schemas.md, faqs.md |

## hybrid decision thresholds

| signal | hybrid? | note |
|--------|---------|------|
| 2+ archetypes apply | yes | pick a primary and cross-link |
| workflow steps depend on domain docs | yes | workflow + domain |
| tool output must satisfy policy | yes | tool + domain |
| sequential steps orchestrate tool scripts | yes | workflow + tool |

## template fill checklist

- update frontmatter name/description with triggers
- replace TODOs in SKILL.md and references/
- ensure every reference is linked from SKILL.md
- add 2+ tool examples when workflow/tool
- run `validate-skill.sh` and fix warnings
