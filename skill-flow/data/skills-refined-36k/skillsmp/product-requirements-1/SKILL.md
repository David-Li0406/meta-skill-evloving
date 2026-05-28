---
name: product-requirements
description: >
  Turns a single product idea (within this repo) into an evolving requirements
  collection. Use when the user wants to capture product design, add or refine
  requirements, or review the current product design state. Stores process
  memory in SQLite and keeps Markdown views up to date.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Product Requirements Manager (Repo-scoped)

This skill manages product design information for **one product per repo**. It
maintains a requirements collection (a set of requirement items) and the
associated design decisions and open questions.

This skill does not manage engineering tasks or implement code. It only
captures and evolves product requirements.

## Core storage (authoritative)

- SQLite DB: `product/memory.sqlite`
- Views (compiled): `product/views/PRODUCT.md`, `BACKLOG.md`, `OPEN_QUESTIONS.md`

This skill intentionally stores its data **inside the skill folder** so users do not
need to learn an extra top-level directory convention. The Python helper scripts
expect the dependencies listed in `requirements.txt`; install them once per
environment:

```bash
pip install -r requirements.txt
```

This ensures the bundled SQLite build includes FTS5 for multilingual search.

## Operations

### 1) Initialize repo product

Run once per repo:

```bash
python scripts/init_product.py --title "<product name>"
```

### 2) Add a requirement

When the user proposes a new feature/capability:

```bash
python scripts/add_requirement.py --description "<requirement idea>"
```

### 3) Refine a requirement

When the user wants to make a requirement more concrete:

```bash
python scripts/refine_requirement.py --id R-001
```

### 4) Show current product design

When the user asks about current product design or similar questions:

```bash
python scripts/query_state.py
```

### 5) Full-text search

When the user asks for requirements, decisions, or questions containing specific keywords:

```bash
# Search across all scopes
python scripts/search.py --query "payment"

# Search specific scope
python scripts/search.py --query "payment" --scope requirement
python scripts/search.py --query "why change" --scope decision
```

The search backend can be controlled with `--mode {auto,fts,like}` or the
`IDEATE_PM_SEARCH_MODE` environment variable (same values). `auto` uses FTS5 when
available and falls back to fuzzy `LIKE` queries otherwise; `fts` forces FTS5 and
errors or downgrades if the engine is missing; `like` forces the fallback (useful
when matching against older databases).

Optional persistence helpers (use when relevant):

```bash
python scripts/record_decision.py --scope product --question "..." --choice "..."
python scripts/add_open_question.py --scope requirement --ref R-001 --question "..."
```

## Additional resources

- Operation details: [ref/ops.md](ref/ops.md)
- SQLite schema: [ref/schema.md](ref/schema.md)
- View templates: [ref/templates.md](ref/templates.md)