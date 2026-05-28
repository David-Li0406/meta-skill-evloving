# Database Maintenance

## Database Cleanup

### Remove Deleted DocType Tables

```bash
# Preview what would be deleted (dry run)
bench --site development.localhost trim-database --dry-run

# View in JSON format
bench --site development.localhost trim-database --dry-run --format json

# Actually remove tables (with backup)
bench --site development.localhost trim-database --yes

# Remove without backup (faster, for development)
bench --site development.localhost trim-database --yes --no-backup
```

**What it does:**
- Scans database for tables whose DocTypes no longer exist
- Removes orphaned tables left after deleting DocTypes
- Creates automatic backup before deletion (unless `--no-backup`)

**Use when:**
- After deleting DocTypes
- Database contains many old tables
- Cleaning up test environments
- Preparing for production deployment

**Example output:**
```
Following tables will be deleted:
  - tabOld_DocType
  - tabTest_Table
  - tabRemoved_Feature

2 tables deleted
```

### Remove Deleted DocType Columns

```bash
# Preview what would be deleted
bench --site development.localhost trim-tables --dry-run

# View as formatted table
bench --site development.localhost trim-tables --dry-run --format table

# Actually remove columns (with backup)
bench --site development.localhost trim-tables

# Remove without backup (for development)
bench --site development.localhost trim-tables --no-backup
```

**What it does:**
- Scans DocTypes for fields that were removed
- Removes corresponding columns from database tables
- Cleans up schema after field deletions
- Creates backup before modification

**Use when:**
- After removing fields from DocTypes
- Schema cleanup after app updates
- Reducing table size
- Database optimization

**Example output:**
```
DocType: Sales Order
  - Removed column: custom_old_field
  - Removed column: temp_calculation

DocType: Customer
  - Removed column: deprecated_status

3 columns removed from 2 tables
```

### Best Practices

```bash
# Always dry-run first to preview
bench --site development.localhost trim-database --dry-run
bench --site development.localhost trim-tables --dry-run

# In production: keep backups
bench --site development.localhost trim-database --yes

# In development: skip backups for speed
bench --site development.localhost trim-database --yes --no-backup
bench --site development.localhost trim-tables --no-backup
```

## Database Analysis

### Describe Table Statistics

```bash
# Get table overview
bench --site development.localhost describe-database-table --doctype "Sales Order"

# Include column cardinality (slower)
bench --site development.localhost describe-database-table --doctype "Sales Order" --column status
```

**What it shows:**
1. **Schema**: All columns with types and constraints
2. **Indexes**: Existing indexes on the table
3. **Statistics**: Total record count, table size
4. **Column Stats** (if `--column` specified): Distinct values, cardinality

**Example output:**
```
DocType: Sales Order
Table: tabSales Order

Schema:
  - name (varchar(140)) PRIMARY KEY
  - creation (datetime)
  - modified (datetime)
  - status (varchar(140))
  - customer (varchar(140))
  - grand_total (decimal(18,6))
  ...

Indexes:
  - PRIMARY on (name)
  - modified on (modified)
  - idx_status on (status)

Statistics:
  - Total records: 15,432
  - Table size: 2.4 MB
  - Index size: 0.8 MB

Column 'status' (with --column status):
  - Distinct values: 7
  - Cardinality: 99.2%
  - Values: Draft, To Deliver, Completed, Cancelled, ...
```

**Use cases:**
- Performance analysis
- Index planning
- Query optimization
- Understanding table structure
- Capacity planning

**Warning:** Using `--column` on large tables (millions of rows) can be slow as it performs a full table scan.

## Index Management

### Add Database Index

```bash
# Add single column index
bench --site development.localhost add-database-index \
  --doctype "Sales Order" \
  --column status

# Add multi-column index
bench --site development.localhost add-database-index \
  --doctype "Sales Order" \
  --column customer \
  --column status

# Add another single column index (run command again)
bench --site development.localhost add-database-index \
  --doctype "Sales Order" \
  --column transaction_date
```

**What it does:**
- Creates database index on specified column(s)
- Creates a Property Setter to persist the index
- Index survives migrations and updates
- Improves query performance on indexed columns

**Index Types:**
- **Single-column**: One `--column` flag
- **Multi-column**: Multiple `--column` flags (order matters!)
- **Multiple single-column**: Run command multiple times

**Use when:**
- Queries are slow on specific fields
- Filtering/sorting by certain columns
- Foreign key lookups are slow
- Large tables (10,000+ rows)

**Performance impact:**
```
Before index:
  Query time: 2.5s (table scan)

After index:
  Query time: 0.05s (index seek)
```

### Index Best Practices

```bash
# 1. Analyze first
bench --site development.localhost describe-database-table --doctype "Sales Order"

# 2. Check existing indexes before adding

# 3. Add index on commonly filtered columns
bench --site development.localhost add-database-index \
  --doctype "Sales Order" \
  --column status

# 4. Multi-column for compound queries
# Good for: WHERE customer = X AND status = Y
bench --site development.localhost add-database-index \
  --doctype "Sales Order" \
  --column customer \
  --column status

# 5. Avoid over-indexing (indexes slow down inserts/updates)
```

### When to Add Indexes

**Good candidates:**
- Status fields (`status`, `workflow_state`)
- Foreign keys (`customer`, `supplier`, `item_code`)
- Date fields used in ranges (`transaction_date`, `posting_date`)
- Frequently filtered fields
- Fields used in JOINs

**Avoid indexing:**
- Unique fields (name, already has PRIMARY index)
- Rarely queried fields
- High-cardinality text fields
- Fields that change frequently

## Database Optimization Workflow

### Complete Cleanup Process

```bash
# 1. Create backup first
bench --site development.localhost backup

# 2. Analyze current state
bench --site development.localhost describe-database-table --doctype "Sales Order"

# 3. Remove orphaned tables (dry run first)
bench --site development.localhost trim-database --dry-run
bench --site development.localhost trim-database --yes

# 4. Remove orphaned columns (dry run first)
bench --site development.localhost trim-tables --dry-run
bench --site development.localhost trim-tables

# 5. Add indexes for performance
bench --site development.localhost add-database-index \
  --doctype "Sales Order" \
  --column status

# 6. Verify improvements
bench --site development.localhost describe-database-table --doctype "Sales Order"
```

### Regular Maintenance Schedule

```bash
# Weekly: Clean up deleted data
bench --site development.localhost trim-database --yes --no-backup
bench --site development.localhost trim-tables --no-backup

# Monthly: Analyze and optimize
bench --site development.localhost describe-database-table --doctype "Sales Order"
# Add indexes as needed

# After major updates: Full cleanup
bench --site development.localhost backup
bench --site development.localhost trim-database --yes
bench --site development.localhost trim-tables
```

## Advanced Database Operations

### Analyze Multiple Tables

```bash
# Create script to analyze all important doctypes
for doctype in "Sales Order" "Purchase Order" "Item" "Customer" "Supplier"; do
  echo "=== $doctype ==="
  bench --site development.localhost describe-database-table --doctype "$doctype"
  echo ""
done
```

### Bulk Index Creation

```bash
# Add indexes to multiple fields
FIELDS="status customer transaction_date posting_date"
for field in $FIELDS; do
  bench --site development.localhost add-database-index \
    --doctype "Sales Order" \
    --column $field
done
```

### Export Table Statistics

```bash
# Export as JSON for analysis
bench --site development.localhost trim-database --dry-run --format json > orphaned-tables.json

bench --site development.localhost trim-tables --dry-run --format json > orphaned-columns.json
```

## Troubleshooting

### Index Already Exists

If you get an error about existing index:
```bash
# Check existing indexes first
bench --site development.localhost describe-database-table --doctype "Sales Order"

# Index might already exist - check Property Setters
# Or remove via database console if needed
```

### Trim Operations Failing

```bash
# Check for foreign key constraints
bench --site development.localhost mariadb

# In MariaDB console:
SHOW CREATE TABLE tabOld_DocType;
# Look for FOREIGN KEY constraints

# May need to drop foreign keys first
```

### Performance Not Improving

```bash
# Verify index is being used
bench --site development.localhost mariadb

# In MariaDB console:
EXPLAIN SELECT * FROM `tabSales Order` WHERE status = 'Draft';
# Should show "Using index" in Extra column

# If not, check:
# 1. Query syntax
# 2. Index column matches WHERE clause
# 3. Table statistics are up to date
ANALYZE TABLE `tabSales Order`;
```

### Large Table Cleanup

For very large tables (millions of rows):

```bash
# 1. Create backup
bench --site development.localhost backup --with-files

# 2. Use dry-run to verify
bench --site development.localhost trim-tables --dry-run

# 3. Consider maintenance window for production
bench --site production.example.com set-maintenance-mode on

# 4. Run cleanup
bench --site production.example.com trim-tables

# 5. Re-enable site
bench --site production.example.com set-maintenance-mode off

# 6. Optimize tables
bench --site production.example.com mariadb
# In console: OPTIMIZE TABLE `tabSales Order`;
```
