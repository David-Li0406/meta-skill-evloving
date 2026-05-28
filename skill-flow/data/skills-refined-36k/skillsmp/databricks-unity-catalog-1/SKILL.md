---
name: databricks-unity-catalog
description: Manage Unity Catalog resources including catalogs, schemas, and tables. Handles discovery, creation, updates, and deletions with proper naming conventions and governance. Use when exploring catalogs, creating schemas, managing tables, or setting up data governance.
allowed-tools:
  - Read
model: claude-sonnet-4-5-20250929
user-invocable: true
---

# Databricks Unity Catalog Management

Discover, create, and manage Unity Catalog resources (catalogs, schemas, tables) via MCP tools. Enforces best practices for naming, governance, and metadata.

## When to Use This Skill

- Exploring available catalogs and schemas
- Creating schemas for new projects
- Discovering tables and their metadata
- Setting up data governance (owners, comments)
- Managing table lifecycle (create, update, delete)
- Validating catalog structure before pipeline deployment

## Core Concepts

### Unity Catalog Hierarchy

```
Catalog (highest level)
  └── Schema (database)
      └── Table (data asset)
          ├── Columns
          ├── Properties
          └── Permissions
```

### Resource Naming

**Three-level namespace:** `catalog.schema.table`

**Example:** `ml_production.feature_store.customer_features`

## Discovery Workflows

### Workflow 1: Explore Catalog Structure

Discover what's available in Unity Catalog.

**Pattern:**
1. Use `list_catalogs` MCP tool → Get all catalogs
2. Use `get_catalog` → Get details for specific catalog
3. Use `list_schemas` → Get schemas in catalog
4. Use `list_tables` → Get tables in schema
5. Use `get_table` → Get table details including columns

**Example:**
```python
# User: "What tables are available in my catalog?"

# Step 1: List all catalogs
list_catalogs()
# Returns: [{name: "main", name: "ml_dev", name: "ml_prod", ...}]

# Step 2: List schemas in a catalog
list_schemas(catalog_name="ml_dev")
# Returns: [{name: "bronze", name: "silver", name: "gold", ...}]

# Step 3: List tables in a schema
list_tables(catalog_name="ml_dev", schema_name="silver")
# Returns: [{name: "clean_events", name: "customer_features", ...}]

# Step 4: Get table details
get_table(full_table_name="ml_dev.silver.clean_events")
# Returns: {
#   name: "clean_events",
#   columns: [{name: "event_id", type: "string"}, ...],
#   table_type: "MANAGED",
#   owner: "user@company.com",
#   comment: "Cleaned event data from bronze layer"
# }
```

### Workflow 2: Validate Table Schema

Check table structure before using in pipeline.

**Pattern:**
1. Use `get_table` with full table name
2. Examine columns array
3. Check data types
4. Verify required columns exist

**Example:**
```python
# User: "Check if the customer table has email column"

get_table(full_table_name="ml_prod.gold.customers")
# Returns table metadata including:
# columns: [
#   {name: "customer_id", type: "bigint"},
#   {name: "email", type: "string"},
#   {name: "created_date", type: "date"}
# ]

# Verify: Yes, email column exists with type string
```

## Schema Management

### Workflow 3: Create Schema for New Project

Set up schema with proper naming and metadata.

**Pattern:**
1. Verify catalog exists with `get_catalog`
2. Create schema with `create_schema`:
   - Use lowercase with underscores
   - Add descriptive comment
   - System sets owner automatically
3. Verify creation with `get_schema`

**Example:**
```python
# User: "Create a schema for my ML feature engineering project"

# Step 1: Verify catalog exists
get_catalog(catalog_name="ml_dev")
# Returns: {name: "ml_dev", owner: "...", ...}

# Step 2: Create schema
create_schema(
    catalog_name="ml_dev",
    schema_name="feature_engineering",
    comment="Feature engineering workspace for customer churn prediction model. Contains raw features, engineered features, and training datasets."
)
# Returns: Schema created successfully

# Step 3: Verify
get_schema(full_schema_name="ml_dev.feature_engineering")
# Returns: {
#   name: "feature_engineering",
#   full_name: "ml_dev.feature_engineering",
#   comment: "Feature engineering workspace for...",
#   owner: "user@company.com"
# }
```

### Workflow 4: Update Schema Metadata

Modify schema properties after creation.

**Pattern:**
1. Use `update_schema` with full schema name
2. Provide new values for:
   - `comment` - Updated description
   - `owner` - New owner email
   - `new_name` - Rename schema (optional)

**Example:**
```python
# User: "Update the schema description"

update_schema(
    full_schema_name="ml_dev.feature_engineering",
    comment="UPDATED: Feature engineering workspace for customer churn prediction v2. Includes time-series features and demographic aggregations.",
    owner="ml-team@company.com"
)
# Returns: Schema updated successfully
```

## Table Management

### Workflow 5: Get Table Information

Retrieve comprehensive table metadata.

**Pattern:**
1. Use `get_table` with full three-level name
2. Examine returned metadata:
   - Columns and types
   - Table type (MANAGED vs EXTERNAL)
   - Owner and permissions
   - Properties and comments
   - Storage location

**Example:**
```python
# User: "Show me the structure of the features table"

get_table(full_table_name="ml_prod.features.customer_360")
# Returns: {
#   name: "customer_360",
#   catalog_name: "ml_prod",
#   schema_name: "features",
#   table_type: "MANAGED",
#   columns: [
#     {name: "customer_id", type_name: "BIGINT", comment: "Primary key"},
#     {name: "lifetime_value", type_name: "DOUBLE", comment: "Total spend"},
#     {name: "churn_score", type_name: "DOUBLE", comment: "0-1 churn probability"},
#     {name: "last_updated", type_name: "TIMESTAMP", comment: "Feature refresh timestamp"}
#   ],
#   owner: "ml-team@company.com",
#   comment: "360-degree customer features for ML models"
# }
```

### Workflow 6: Delete Table

Remove table from Unity Catalog.

**Pattern:**
1. Confirm with user before deleting
2. Use `delete_table` with full table name
3. For MANAGED tables: data is deleted too
4. For EXTERNAL tables: only metadata removed

**Example:**
```python
# User: "Delete the old test table"

# IMPORTANT: Always confirm deletions
# Ask user: "Are you sure you want to delete ml_dev.test.old_data? This cannot be undone."

# If confirmed:
delete_table(full_table_name="ml_dev.test.old_data")
# Returns: Table deleted successfully
```

### Workflow 7: Delete Schema

Remove schema and all its tables.

**Pattern:**
1. Confirm with user (DANGEROUS operation)
2. List tables in schema first to show what will be deleted
3. Use `delete_schema` with full schema name
4. All tables in schema are deleted too

**Example:**
```python
# User: "Delete the temp schema"

# IMPORTANT: List contents first
list_tables(catalog_name="ml_dev", schema_name="temp")
# Shows: 3 tables will be deleted

# Ask user: "Are you sure? This will delete the schema 'ml_dev.temp' and all 3 tables. This cannot be undone."

# If confirmed:
delete_schema(full_schema_name="ml_dev.temp")
# Returns: Schema deleted successfully
```

## Naming Conventions

### Required Naming Rules

**DO:**
- Use lowercase letters only
- Use underscores to separate words
- Use descriptive names
- Examples:
  - `ml_production`
  - `feature_store`
  - `customer_features`
  - `daily_aggregates`

**DON'T:**
- Use hyphens: `ml-production` ❌
- Use spaces: `ml production` ❌
- Use special characters: `ml_prod!` ❌
- Use camelCase: `mlProduction` ❌
- Use numbers at start: `2024_features` ❌

### Recommended Naming Patterns

**Catalogs:**
- `<domain>_<environment>`: `ml_dev`, `ml_prod`, `analytics_staging`
- `<team>_<purpose>`: `data_eng_pipelines`, `ml_models`

**Schemas:**
- Medallion layers: `bronze`, `silver`, `gold`
- By function: `feature_store`, `models`, `metrics`
- By project: `churn_prediction`, `recommendation_engine`

**Tables:**
- Include domain: `customer_features`, `order_metrics`
- Include grain: `daily_sales`, `hourly_events`
- Include status: `active_users`, `archived_orders`

## Best Practices

### 1. Always Add Comments

Every schema and table should have a descriptive comment explaining:
- What data it contains
- Who owns/maintains it
- When/how it's updated
- Related upstream/downstream dependencies

```python
# Good
create_schema(
    catalog_name="ml_dev",
    schema_name="feature_engineering",
    comment="Feature engineering workspace for churn model v2. Updated daily at 2am UTC. Owned by ML team."
)

# Bad - no comment
create_schema(
    catalog_name="ml_dev",
    schema_name="feature_engineering"
)
```

### 2. Use MANAGED Tables by Default

Unless you have external data in cloud storage:
- Use MANAGED tables (Databricks manages storage)
- Data deleted when table dropped
- Simpler governance

Use EXTERNAL only when:
- Data shared across multiple systems
- Need independent data lifecycle
- Existing data in cloud storage

### 3. Set Proper Owners

- Individual for personal dev: `user@company.com`
- Team/group for shared: `ml-team@company.com`
- Enables proper governance and access control

### 4. Verify Before Using

Always verify structure before using tables:
```python
# Before writing pipeline
table_info = get_table(full_table_name="catalog.schema.table")

# Check required columns exist
required_columns = {"customer_id", "purchase_date", "amount"}
actual_columns = {col["name"] for col in table_info["columns"]}

if not required_columns.issubset(actual_columns):
    missing = required_columns - actual_columns
    print(f"ERROR: Missing required columns: {missing}")
```

### 5. Use Three-Level Names

Always use full names for clarity:
```python
# Good - explicit
get_table(full_table_name="ml_prod.features.customer_360")

# Bad - ambiguous
# "features" table in which catalog/schema?
```

## Integration with Other Skills

### Called By
- `databricks-ml-pipeline` - Creates schemas for models and features
- `databricks-data-engineering` - Creates medallion architecture schemas (bronze, silver, gold)

### Works With
- `databricks-testing` - Tests against discovered tables

## Common Patterns

### Pattern: Set Up Medallion Architecture

```python
# Create bronze, silver, gold schemas for data pipeline

catalog = "de_prod"

# Bronze layer - raw data
create_schema(
    catalog_name=catalog,
    schema_name="bronze",
    comment="Raw ingested data with minimal transformation. Append-only. Retained for 90 days."
)

# Silver layer - cleaned data
create_schema(
    catalog_name=catalog,
    schema_name="silver",
    comment="Cleaned and validated data. Deduplicated, type-cast, quality-checked. Retained for 1 year."
)

# Gold layer - business aggregates
create_schema(
    catalog_name=catalog,
    schema_name="gold",
    comment="Business-ready aggregates and metrics. Optimized for analytics queries. Retained for 3 years."
)
```

### Pattern: Audit Schema Contents

```python
# User: "Show me all tables in the feature store"

# Get schema details
schema_info = get_schema(full_schema_name="ml_prod.feature_store")
print(f"Schema: {schema_info['full_name']}")
print(f"Owner: {schema_info['owner']}")
print(f"Comment: {schema_info['comment']}")

# List all tables
tables = list_tables(catalog_name="ml_prod", schema_name="feature_store")

print(f"\nTables ({len(tables)}):")
for table in tables:
    # Get details for each
    table_info = get_table(full_table_name=f"ml_prod.feature_store.{table['name']}")
    print(f"  - {table_info['name']}")
    print(f"    Type: {table_info['table_type']}")
    print(f"    Columns: {len(table_info['columns'])}")
    print(f"    Comment: {table_info.get('comment', 'No description')}")
```

## Troubleshooting

### Issue: Catalog Not Found
**Error:** "Catalog 'xyz' does not exist"

**Solution:**
- Use `list_catalogs()` to see available catalogs
- Check spelling and case (must be lowercase)
- Verify you have access to catalog

### Issue: Schema Already Exists
**Error:** "Schema 'catalog.schema' already exists"

**Solution:**
- Use `get_schema()` to check if exists
- Use `update_schema()` to modify instead of create
- Use different name or delete existing first

### Issue: Invalid Name
**Error:** "Invalid name: contains invalid characters"

**Solution:**
- Use only lowercase letters, numbers, underscores
- No hyphens, spaces, or special characters
- Don't start with numbers

## Security Reminders

- Never grant overly broad permissions
- Use least-privilege access
- Set appropriate owners for governance
- Document who has access in comments

## Summary

This skill manages Unity Catalog resources:
- **Discovery**: Explore catalogs, schemas, tables
- **Creation**: Set up schemas with proper naming and governance
- **Updates**: Modify metadata, owners, comments
- **Deletion**: Remove schemas/tables (with confirmation)
- **Best practices**: Naming conventions, comments, MANAGED tables, proper ownership

Use this skill to set up catalog structure before building pipelines with other skills.
