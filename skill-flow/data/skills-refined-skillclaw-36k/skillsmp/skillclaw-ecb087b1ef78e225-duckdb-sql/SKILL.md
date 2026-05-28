---
name: duckdb-sql
description: Use this skill when you need to generate, review, or modify DuckDB SQL queries for data analysis, exploring .ddb, CSV, or Parquet files.
---

# DuckDB SQL Query Assistant

## Core Workflow

### Step 1: Check for Existing Assets

**Your FIRST action must be to check if `duckdb_sql_assets/` exists.**

Even if the user provides direct file paths (e.g., `@file.ddb`), check for existing assets first.

If `duckdb_sql_assets/` exists with the following files:
- `tables_inventory.json`
- `schema_*.sql` files
- `data_dictionary.md`

**NEVER:**
- Run `duckdb` bash commands (no `.schema`, no `DESCRIBE`, no direct queries)
- Open or access `.ddb` files directly
- Regenerate asset files
- Check for schema changes (unless explicitly requested)

**ALWAYS:**
- Read `tables_inventory.json` to understand available tables and file paths
- Read `data_dictionary.md` for business context
- Read relevant `schema_*.sql` files to validate column names
- Generate queries using the documented schema only

The only exception is when the user explicitly requests schema updates using phrases like "refresh the schema" or "update the assets".

### Step 2: Identify Question Type

- **Discovery questions** ("Do we have...?", "Where is...?") -> Search documentation, explain findings
- **Query requests** ("Show me...", "List all...") -> Use a two-step query plan workflow
- **SQL review requests** ("Review this SQL", "Improve this query") -> Use SQL review workflow

### Step 3: If No Assets Exist

Refer to the first-time setup guide for the complete workflow.

## Display-Only by Default

**DO NOT execute queries unless explicitly requested.** Your primary purpose is to **display queries** for the user to review, copy, and run themselves.

- **Default behavior:** Generate and display SQL queries only
- **Execution:** Only run queries when the user explicitly asks (e.g., "run this", "execute it", "show me the results")
- **Why:** Users want to review queries before execution and may want to run them in a different environment.