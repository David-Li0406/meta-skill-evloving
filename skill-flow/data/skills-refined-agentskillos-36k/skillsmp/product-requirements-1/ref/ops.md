# Operations for Product Requirements Manager

This document describes the supported operations of the `product-requirements` skill.
This skill assumes **one product per repo**. All operations update the repo-scoped
SQLite database and compiled views under `product/` (inside the skill folder).

Install the Python dependencies once per environment to ensure the packaged SQLite build includes FTS5:

```
pip install -r requirements.txt
```

Important: Interactive clarification (asking follow-up questions) is performed by the
agent in chat. The scripts are intentionally deterministic and exist primarily to
persist outcomes (requirements, acceptance criteria, decisions, open questions) and
regenerate views.

## Seed Product

Use this operation when a new product idea is introduced. It creates the product
directory and initial memory. The initialization script:

```bash
python scripts/init_product.py --title "<product title>"
```

The script performs the following actions:

1. Creates a SQLite database at `product/memory.sqlite`.
2. Stores product identity in the `meta` table.
3. Generates human-readable views (`PRODUCT.md`, `BACKLOG.md`, `OPEN_QUESTIONS.md`)
   based on the initial state.
4. Initializes configuration values for question limits (see `config.json`).

## Add Requirement

Use this operation to record a new requirement. The command:

```bash
python scripts/add_requirement.py --description "<requirement>"
```

The script:

1. Inserts a row in the `requirement` table with the description and status
   `PROPOSED`. A unique identifier (e.g., R-001) is assigned.
2. Regenerates the compiled views under `product/views/`.

## Refine Requirement

Use this operation to fill in missing details of an existing requirement.

```bash
python scripts/refine_requirement.py --id <requirement-id>
```

This script:

1. Loads the current requirement and its acceptance criteria.
2. Applies explicit updates provided on the CLI (title/description/status/priority)
   and optionally appends acceptance criteria.
3. Regenerates the compiled views.

Use `python scripts/record_decision.py ...` to persist key decisions, and
`python scripts/add_open_question.py ...` to persist unresolved questions.

## Show Product State

When a user wants to know the current design of a product, run:

```bash
python scripts/query_state.py
```

The script compiles a summary from the database:

* **PRODUCT.md**: the product card (vision, user, core value, constraints).
* **BACKLOG.md**: list of all requirements with IDs, titles, descriptions,
  acceptance summary, status, and priority.
* **OPEN_QUESTIONS.md**: outstanding questions or assumptions that still need
  answers.
* **Decisions**: key decisions and assumptions stored in the `decision` table.

The summary is formatted in Markdown for easy reading. Use this when you or the
user want to review current product design and decide what to do next.

## Question Limits and Self‑Adaptive Behaviour

This skill adapts the number of clarifying questions it asks based on missing
information. To prevent endless questioning or premature completion, the *agent*
should respect the min/max limits configured in `config.json`.