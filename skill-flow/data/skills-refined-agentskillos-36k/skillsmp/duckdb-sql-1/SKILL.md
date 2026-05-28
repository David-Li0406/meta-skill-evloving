---
name: duckdb-sql
description: Generate DuckDB SQL queries. Use when user asks about DuckDB queries, data analysis, exploring .ddb database files, CSV files, Parquet files, wants help editing/improving SQL, asks to use the duckdb skill, references duckdb assets, or wants to initialize/setup duckdb analysis.
allowed-tools: Read, Grep, Glob, Bash
---

# DuckDB SQL Query Assistant

Generate SQL queries for DuckDB databases, CSV files, and Parquet files.

## Reference Files

- **[Query patterns](references/query-patterns.md)**: Multi-file queries, common SQL patterns, CSV handling
- **[DuckDB syntax](references/duckdb-syntax.md)**: Data types, functions, CLI commands
- **[Setup guide](references/setup-guide.md)**: First-time setup, enum detection, schema updates
- **[Data dictionary template](references/data-dictionary-template.md)**: Template for generating data_dictionary.md

---

## Core Workflow

### Step 1: Check for Existing Assets

**Your FIRST action must be to check if `duckdb_sql_assets/` exists.**

Even if the user provides direct file paths (e.g., `@file.ddb`), check for existing assets first.

If `duckdb_sql_assets/` exists with `tables_inventory.json`, `schema_*.sql`, and `data_dictionary.md`:

**NEVER:**
- Run `duckdb` bash commands (no `.schema`, no `DESCRIBE`, no direct queries)
- Open or access `.ddb` files directly
- Regenerate asset files
- Check for schema changes (unless explicitly requested)

**ALWAYS:**
- Read `tables_inventory.json` for available tables and file paths
- Read `data_dictionary.md` for business context
- Read relevant `schema_*.sql` files to validate column names
- Generate queries using documented schema only

The only exception: user explicitly requests schema refresh (see [setup guide](references/setup-guide.md#schema-update-detection)).

### Step 2: Identify Question Type

- **Discovery questions** ("Do we have...?", "Where is...?") -> Search documentation, explain findings
- **Query requests** ("Show me...", "List all...") -> Use two-step query plan workflow
- **SQL review requests** ("Review this SQL", "Improve this query") -> Use SQL review workflow

### Step 3: If No Assets Exist

See [First-Time Setup](references/setup-guide.md#setup-workflow) for the complete workflow.

---

## Display-Only by Default

**DO NOT execute queries unless explicitly requested.** Your primary purpose is to display queries for the user to review and run themselves.

- **Default:** Generate and display SQL only
- **Execute:** Only when user says "run this", "execute it", "show me the results"

---

## Asset Directory

**Terminology:** "assets", "the assets", "duckdb assets" = `duckdb_sql_assets/` directory.

Contents:
- `tables_inventory.json` - Manifest of source files and table metadata
- `schema_<filename>.sql` - Schema files (one per source file)
- `data_dictionary.md` - Semantic documentation of tables and fields

---

## Supported File Types

| File Type | Extension | Tables per File | Schema Source |
|-----------|-----------|-----------------|---------------|
| DuckDB Database | `.ddb` | Multiple | Native schema via `.schema` |
| CSV | `.csv` | Single | Auto-inferred by DuckDB |
| Parquet | `.parquet` | Single | Embedded in file |

**Table naming for CSV/Parquet:** Convert filename to lowercase snake_case (e.g., `My Transactions-2024.csv` -> `my_transactions_2024`).

---

## Query Execution Model

All queries run in an **in-memory DuckDB session** (`duckdb` with no file argument).

| File Type | How to Reference | Example |
|-----------|------------------|---------|
| `.ddb` table | `_db_alias.tablename` after ATTACH | `_db_sales.customers` |
| CSV file | File path in quotes | `'data/transactions.csv'` |
| Parquet file | File path in quotes | `'data/events.parquet'` |
| Glob pattern | Glob in quotes | `'logs/*.csv'` |

### ATTACH Alias Convention

Use `_db_` prefix + filename slug: `sales.ddb` -> `AS _db_sales`

### Standard Query Preamble

```sql
-- Setup: Attach database files
ATTACH IF NOT EXISTS 'data/sales.ddb' AS _db_sales (READ_ONLY);

-- Query
SELECT c.name, o.total_amount
FROM _db_sales.customers c
JOIN _db_sales.orders o ON c.customer_id = o.customer_id;
```

**Path convention:** Use relative paths by default for portability.

See [query-patterns.md](references/query-patterns.md#multi-file-queries) for more examples.

---

## Schema Validation (CRITICAL)

Before generating ANY SQL, validate every table and column against asset files only:

1. Verify all table names exist in `tables_inventory.json` or schema files
2. Verify all column names exist in `schema_<filename>.sql`
3. Verify column types match usage
4. Verify JOIN columns exist on both sides

**If you cannot find a table or column, DO NOT use it.** Instead:
- Tell user the field doesn't exist
- Suggest similar fields that DO exist
- Ask for clarification

**Common hallucination patterns to avoid:**
- Assuming `name` exists (check for `first_name`, `product_name`, etc.)
- Assuming `user_id` when it might be `profile_id` or `customer_id`
- Inventing status values not in the data

---

## Query Generation - Two-Step Workflow

**ALWAYS present a query plan first** before writing SQL.

### Step 1: Present Query Plan

```
**Query Plan:**
- **Attach statements needed:**
  - `ATTACH IF NOT EXISTS 'data/sales.ddb' AS _db_sales (READ_ONLY)`
- **Tables:**
  - _db_sales.customers (c) - Customer records [from sales.ddb]
  - _db_sales.orders (o) - Order transactions [from sales.ddb]
- **Joins:**
  - _db_sales.customers -> _db_sales.orders on customer_id
- **Filters:**
  - Optional: date range on order_date
- **Output:** Returns order details with customer names

Does this plan look correct?
```

If ambiguous, present multiple options and let user choose.

### Step 2: Generate SQL After Approval

Provide:
1. **The SQL query** - formatted and ready to copy/run
2. **Brief explanation** - what it does in plain English
3. **Parameters** - values that might need adjustment
4. **Warnings** (if any) - performance concerns, assumptions

---

## Modifying Existing SQL

When user provides SQL to modify:

1. Understand the original query
2. Identify changes needed
3. Make minimal changes - preserve user's style
4. Explain what changed and why

---

## Reviewing User SQL

### Review Checklist

1. **Correctness** - Tables/columns exist? JOINs correct? Aggregations grouped properly?
2. **Performance** - `SELECT *` when specific columns suffice? Unnecessary subqueries? Filters applied early?
3. **Readability** - Aliases consistent? Formatting clean?
4. **Best Practices** - Explicit columns? Proper NULL handling? Date ranges correct?

### Response Format

```
**Review of your SQL:**

- **Correct:** [things that are right]

- **Issues found:**
1. [Issue] - [Why it's a problem]

- **Suggestions:**
1. [Improvement] - [Benefit]

**Improved version:**
[Corrected SQL if needed]

**Changes:**
- [Change 1]: [Why]
```

### Common Issues to Check

- Missing JOINs or Cartesian products
- Wrong JOIN type (INNER vs LEFT)
- Ambiguous columns without alias
- Type mismatches without CAST
- Off-by-one dates (using `<=` instead of `<`)
- GROUP BY errors
- NULL gotchas (`= NULL` instead of `IS NULL`)

---

## Query Quality Guidelines

### Column Selection
- Use explicit column names, not `SELECT *`
- Include table aliases (e.g., `c` for customers)
- Add appropriate WHERE clauses

### Enum Values
- Use ONLY values documented in data dictionary
- If unsure, say so rather than guessing

### Date/Time Handling
- Use DuckDB functions: `current_date`, `INTERVAL`, `date_trunc()`
- For ranges: `>= start AND < end` (half-open interval)
- String concatenation: `||` operator

### NULL Handling
- Use `IS NULL` / `IS NOT NULL`
- Consider whether NULLs should be included
- Use `COALESCE()` for defaults

---

## Learning and Adding Facts

When you discover new information about the data:

- **1-2 facts**: Ask inline "Should I add this to the data dictionary?"
- **3+ facts**: Present summary and ask for bulk decision
- **If approved**: Use Edit tool to update `data_dictionary.md`

---

## Safety Guidelines

- Generate ONLY read-only queries (SELECT statements)
- NEVER generate INSERT, UPDATE, DELETE, DROP, TRUNCATE
- If user asks for data modification, explain you can only generate read queries
- Always validate columns exist before using them
- When unsure about data meaning, ask rather than guess

---

## tables_inventory.json Format

```json
{
  "generated_at": "2025-12-11T17:30:00Z",
  "duckdb_version": "v1.3.2",
  "sources": [
    {
      "file_path": "data/sales.ddb",
      "file_name": "sales.ddb",
      "file_type": "ddb",
      "tables": ["customers", "orders"]
    },
    {
      "file_path": "data/transactions.csv",
      "file_name": "transactions.csv",
      "file_type": "csv",
      "tables": ["transactions"]
    }
  ],
  "tables": {
    "customers": {
      "source_file": "sales.ddb",
      "file_type": "ddb",
      "columns": [
        {"name": "customer_id", "type": "INTEGER"},
        {"name": "name", "type": "VARCHAR"}
      ]
    }
  }
}
```

**File type values:** `ddb`, `csv`, `parquet`, `csv_glob`, `parquet_glob`
