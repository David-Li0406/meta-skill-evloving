---
name: data-modeling
description: Expert guide to defining enterprise-grade data models in Simple Configuration Language (SCL).
---
# Data Modeling Skill

## 1. Introduction
The Data Layer is the foundation. You define your schema in `apps/<app>/tables.scl`.

**Golden Rules:**
1.  **NO SQL:** You never write `CREATE TABLE`.
2.  **No Arrays:** Use lists `"a", "b"` NOT `["a", "b"]`.
3.  **No UUID Type:** Use `:string` with `id_prefix`.

## 2. Table Definition
```scl
table user, users {
  default :id, :timestamps, :userstamps
  id_prefix "USR"
  display_field full_name

  required email, :string {
    length 1..100
    unique true
  }
}
```

## 3. Field Types & Constraints (Exhaustive)
Derived from `scl-grammar.txt`.

### Textual
*   `:string`
    *   `length: 100` (Max) or `2..100` (Range)
    *   `hash: true` (Store as hash, e.g. passwords)
    *   `secret: true` (Encrypted at rest)
    *   `multiline: true` (Text area UI)
    *   `unique: true`
*   `:char`
    *   Same constraints as `:string`.
*   `:enum`
    *   `values "Draft", "Active"` (**NO SPACES** in values)

### Numeric
*   `:integer` (4-byte), `:smallint` (2-byte), `:bigint` (8-byte)
    *   `default 0`, `min 0`, `max 100`
*   `:float` (Real)
*   `:decimal` (Currency/Precision)
    *   `digits 10` (Total precision)
    *   `decimals 2` (Scale)

### Boolean
*   `:boolean` (`true` / `false`)
    *   `default true`

### Temporal
*   `:date` (Date only)
*   `:time` (Time only)
*   `:datetime` (Timestamptz)

### Structured
*   `:json`, `:jsonb` (Arbitrary JSON)
*   `:document` (File Attachments)
    *   `multiple: true`
    *   `allowed_types: "pdf", "jpg", "image/png"`
    *   `max_size: "10MB"`
*   `:version` (Semver string)

## 4. Relationships

### In-App
```scl
# Parent
has :many, orders {
  table order
}

# Child
belongs :to, user {
  required true
}
```

### Cross-App (Advanced)
Referencing tables in other installed applications.

**1. The `belongs :to` (in `tables.scl`)**
```scl
belongs :to, job_site {
  # Fully qualified table name
  table com_bnv_administration.job_site
  required true
}
```

**2. The `has :many` (in `records/30_links.scl`)**
Since you cannot edit the external app's `tables.scl`, you must use a Relationship Record.

```scl
set dev_simple_system.table_relationship, link_site_to_jobs {
  name "jobs"
  kind has
  cardinality many

  # Source = External Table
  source_table_id `$var('meta') |> $jq(...)`
  # Target = My Table
  target_table_id `$var('meta') |> $jq(...)`
}
```

## 5. Indexes
```scl
index email { unique true }
index status, created_at { }
```
