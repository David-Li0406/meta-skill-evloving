# Schema (repo-scoped)

This skill assumes **one product per repo**. The SQLite database at
`product/memory.sqlite` (inside the skill folder) is the source of truth.

## Tables

### `meta`

Repo-level product identity and settings.

| Column | Type |
|---|---|
| `key` | TEXT PRIMARY KEY |
| `value` | TEXT |

Common keys:

- `title`
- `vision`
- `constraints`

### `requirement`

Requirement items (the “set elements”).

| Column | Type |
|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT |
| `req_id` | TEXT UNIQUE |
| `title` | TEXT |
| `description` | TEXT |
| `status` | TEXT |
| `priority` | TEXT |
| `created_at` | DATETIME |
| `updated_at` | DATETIME |

`status` values: `PROPOSED`, `READY`, `DONE`.

### `acceptance`

Acceptance criteria for a requirement.

| Column | Type |
|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT |
| `requirement_id` | INTEGER |
| `text` | TEXT |
| `type` | TEXT |
| `created_at` | DATETIME |

`type` values: `CHECKLIST`, `GWT`.

### `decision`

Design decisions and assumptions.

| Column | Type |
|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT |
| `scope_type` | TEXT |
| `scope_ref` | TEXT |
| `question` | TEXT |
| `choice` | TEXT |
| `rationale` | TEXT |
| `confidence` | REAL |
| `created_at` | DATETIME |

`scope_type` values: `product`, `requirement`.

`scope_ref` is `product` or a `req_id` (e.g., `R-001`).

### `open_question`

Unresolved questions.

| Column | Type |
|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT |
| `scope_type` | TEXT |
| `scope_ref` | TEXT |
| `question` | TEXT |
| `severity` | TEXT |
| `created_at` | DATETIME |
`resolved_by_decision_id` | INTEGER |

## FTS5 Virtual Tables

Full-text search tables using SQLite FTS5 extension. These use the
**external content** pattern: the original tables hold the data, and the
FTS5 virtual tables maintain the search index. Triggers keep them in sync.

### `requirement_fts`

Search index for requirements. Automatically synced via triggers.

| Column | Type |
|---|---|
| `req_id` | TEXT |
| `title` | TEXT |
| `description` | TEXT |

**Content**: References `requirement` table via `content_rowid='id'`.

**Triggers**: `requirement_ai` (INSERT), `requirement_au` (UPDATE), `requirement_ad` (DELETE)

### `decision_fts`

Search index for design decisions. Automatically synced via triggers.

| Column | Type |
|---|---|
| `question` | TEXT |
| `choice` | TEXT |
| `rationale` | TEXT |

**Content**: References `decision` table via `content_rowid='id'`.

**Triggers**: `decision_ai` (INSERT), `decision_au` (UPDATE)

### `open_question_fts`

Search index for open questions. Automatically synced via triggers.

| Column | Type |
|---|---|
| `question` | TEXT |

**Content**: References `open_question` table via `content_rowid='id'`.

**Triggers**: `open_question_ai` (INSERT), `open_question_au` (UPDATE)

### `entity` and `edge`

Optional graph layer (terms, roles, data objects).

`entity(id, type, name, payload_json)`

`edge(id, src_entity_id, rel, dst_entity_id, evidence_ref, created_at)`
