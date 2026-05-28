# First-Time Setup Guide

## Table of Contents

- [Setup Workflow](#setup-workflow)
- [Enum Detection](#enum-detection)
- [Schema Update Detection](#schema-update-detection)

---

## Setup Workflow

When a user asks about DuckDB data and `duckdb_sql_assets/` doesn't exist:

**Initialization trigger phrases** - These phrases explicitly request setup:
- "initialize an analysis"
- "create assets"
- "initialize your DuckDB skill"
- "use your DuckDB skill in this project"
- "set up duckdb"
- "setup duckdb"

When any of these phrases are used:
1. Check if `duckdb_sql_assets/` exists - if it does, inform user assets already exist
2. If no specific files are mentioned in the request, proceed to step 2 below to prompt for files
3. If files are mentioned, skip the prompt and proceed directly with those files

---

### Step 1: Verify DuckDB CLI

```bash
duckdb -version
```

If the command fails, inform the user:
> "DuckDB CLI is required but not found. Please install it:
> - macOS: `brew install duckdb`
> - Linux: `curl -fsSL https://install.duckdb.org | sh`
> - Other platforms: https://duckdb.org/docs/installation"

Do not proceed until DuckDB is available.

### Step 2: Ask for Files

> "I don't see any DuckDB assets configured. Which data files should I document? I support:
> - `.ddb` files (DuckDB databases with multiple tables)
> - `.csv` files (single table per file, schema auto-inferred)
> - `.parquet` files (single table per file, schema embedded)
>
> You can provide individual file paths or glob patterns (e.g., `data/*.csv`). Please provide the paths."

### Step 3: Handle Glob Patterns (if provided)

- Expand glob to list matching files
- Present list to user: "I found N files matching `pattern`. Should I treat these as:"
  - **Separate tables**: Each file becomes its own table with computed name
  - **Single combined table**: One virtual table that unions all files (must share schema)
- Proceed based on user choice

### Step 4: Ask for Supplementary Documentation

> "Do you have any code or documentation files that explain this data? (e.g., ETL scripts, data dictionaries, README files) This will help me understand the business context."

### Step 5: Generate Assets

- Create `duckdb_sql_assets/` directory
- For each source file, extract schema based on file type:
  - `.ddb`: `duckdb <file> -c ".schema"`
  - `.csv`: `duckdb -c "DESCRIBE SELECT * FROM '<file>';"`
  - `.parquet`: `duckdb -c "DESCRIBE SELECT * FROM '<file>';"`
- Generate `tables_inventory.json` with file paths, file types, and table metadata
- Generate `schema_<filename>.sql` for each source file
- Generate draft `data_dictionary.md` using the template in [data-dictionary-template.md](data-dictionary-template.md)

### Step 6: Detect Likely Enum Columns

See [Enum Detection](#enum-detection) below.

### Step 7: Present Findings for Bulk Approval

- If 1-2 enums found: Ask inline per enum
- If 3+ enums found: Present summary of all detected enums in one message
> "I found 12 potential enums: `orders.status` (4 values: pending, shipped, delivered, cancelled), `customers.role` (2 values: admin, user), ... Should I add all of these to the data dictionary?"

### Step 8: Handle User Response

- If "yes" -> Add all enum documentation to `data_dictionary.md`
- If "show diff first" -> Describe exact changes, then user decides
- If "add only X, Y, Z" -> Add subset specified by user
- If "no" -> Skip all
- Report what was updated after changes are made

---

## Enum Detection

During first-time setup (and on-demand), the skill scans for likely enum columns by sampling data.

### Detection Heuristics

The skill uses these hardcoded thresholds to identify likely enum columns:

- **max_cardinality**: 20 (maximum distinct values)
- **max_ratio**: 0.05 (max 5% unique values in sample)
- **sample_size**: 10000 (rows to sample per table)
- **name_patterns**: Prioritize columns named: status, type, state, category, level, role, kind

A column is flagged as a likely enum if ALL of these are true:

1. **Type**: Column is VARCHAR or TEXT
2. **Cardinality**: `distinct_count <= 20`
3. **Ratio**: `distinct_count / sampled_rows < 0.05` (less than 5%)

Columns matching `name_patterns` are prioritized but not required.

### DuckDB Commands for Enum Detection

**For .ddb files:**
```sql
-- Step 1: Get VARCHAR columns from schema
SELECT column_name, table_name
FROM information_schema.columns
WHERE table_schema = 'main'
  AND data_type IN ('VARCHAR', 'TEXT');

-- Step 2: For each VARCHAR column, check cardinality (with sampling)
WITH sampled AS (
  SELECT column_name FROM table_name LIMIT 10000
)
SELECT
  COUNT(DISTINCT column_name) as distinct_count,
  COUNT(*) as sample_size
FROM sampled;

-- Step 3: If passes thresholds, get distinct values
SELECT DISTINCT column_name
FROM table_name
WHERE column_name IS NOT NULL
LIMIT 25;
```

**For .csv and .parquet files:**
```sql
-- Step 1: Get columns from inferred schema
DESCRIBE SELECT * FROM '/path/to/file.csv';

-- Step 2: For VARCHAR columns, check cardinality (with sampling)
WITH sampled AS (
  SELECT column_name FROM '/path/to/file.csv' LIMIT 10000
)
SELECT
  COUNT(DISTINCT column_name) as distinct_count,
  COUNT(*) as sample_size
FROM sampled;

-- Step 3: If passes thresholds, get distinct values
SELECT DISTINCT column_name
FROM '/path/to/file.csv'
WHERE column_name IS NOT NULL
LIMIT 25;
```

### Re-running Enum Detection

If the user wants different detection thresholds, they can request conversationally:
- "Detect enums with up to 50 values"
- "Re-run enum detection with stricter criteria"
- "Check if the 'notes' column could be an enum"

The skill will adjust the thresholds for that specific request and present findings for approval.

---

## Schema Update Detection

Schema updates are **on-demand only**. Do NOT check for changes automatically on every invocation.

**Trigger phrases** - Only run schema update checks when the user explicitly requests:
- "Refresh the schema"
- "Check for schema changes"
- "Resync the database"
- "Update the assets"
- "Add [filename] to the assets" (supports .ddb, .csv, .parquet, or glob patterns)
- "Update the data dictionary"

### Detect Missing Files

If a source file in `tables_inventory.json` no longer exists:
> "I notice `sales.ddb` no longer exists at the recorded path. Should I remove it from the assets?"

If approved:
- Delete `schema_sales.sql`
- Update `tables_inventory.json`
- Update `data_dictionary.md` (mark tables as removed or delete sections)

### Add New Files

When user says "add [file] to the assets":

**For .ddb files:**
1. Extract schema: `duckdb new_file.ddb -c ".schema"`
2. Create `schema_new_file.sql`
3. Update `tables_inventory.json` with `file_type: "ddb"`
4. Add stub entries to `data_dictionary.md`
5. Run enum detection on new tables
6. Present findings for approval (inline for 1-2 enums, bulk summary for 3+)
7. If approved, update `data_dictionary.md` with enum documentation

**For .csv or .parquet files:**
1. Extract schema: `duckdb -c "DESCRIBE SELECT * FROM '/path/to/file.csv';"`
2. Convert to CREATE TABLE format and save as `schema_<table_name>.sql`
3. Compute table name from filename (lowercase, snake_case, alphanumeric)
4. Update `tables_inventory.json` with `file_type: "csv"` or `"parquet"`
5. Add stub entry to `data_dictionary.md`
6. Run enum detection on VARCHAR columns
7. Present findings for approval

**For glob patterns (e.g., `logs/*.csv`):**
1. Expand glob to list matching files
2. Ask user: "I found N files. Should I treat these as separate tables or a single combined table?"
3. If **separate tables**: Process each file individually as above
4. If **single table**:
   - Extract schema from first file (all files should share schema)
   - Compute table name from glob pattern base
   - Update `tables_inventory.json` with `file_type: "csv_glob"` or `"parquet_glob"`, including `glob_pattern` and `matched_files`
   - Create single schema file and dictionary entry

### Schema Changes

If running schema extraction shows changes:
> "I notice table X has new columns: a, b, c. Should I update the schema files?"

If approved:
- Regenerate affected `schema_<filename>.sql`
- Update `tables_inventory.json`
- If new VARCHAR/TEXT columns are detected, run enum detection
- Ask user if discovered facts should be added to `data_dictionary.md`

### Preserving Data Dictionary Content (CRITICAL)

When updating schema or adding new tables, **never overwrite** `data_dictionary.md`. User-added notes, relationships, and query patterns are valuable and must be preserved.

**Always merge, never replace:**
- Add new table sections for newly discovered tables
- Add new columns to existing table sections
- Preserve ALL existing user-written content: notes, enum values, relationships, query patterns

**For removed tables/columns:**
- Ask user before removing documentation
- Data may have moved to another table or been renamed

**Implementation:**
- Use the Edit tool for surgical updates, NOT the Write tool to regenerate
- When adding a new table, append a new section rather than rewriting the file
