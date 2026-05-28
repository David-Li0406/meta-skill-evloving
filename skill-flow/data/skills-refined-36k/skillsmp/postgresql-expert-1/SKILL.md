---
name: postgresql-expert
description: Use when editing .sql files, reviewing SQL in Python/JavaScript/TypeScript code, writing database queries, or when user mentions PostgreSQL, SQL validation, query optimization, or database schema.
---

# PostgreSQL 18 Expert

Analyze, validate, and improve PostgreSQL queries with focus on safety, performance, and best practices.

## Activation

Activate this skill when:
- Editing `.sql` files
- SQL queries appear in Python, JavaScript, or TypeScript code
- User asks about PostgreSQL, database queries, or schema design
- Reviewing migrations or database-related code

## Analysis workflow

When encountering SQL:

1. **Identify the context**: Is this a migration, application query, ad-hoc script, or test?
2. **Assess risk level**: Production code requires stricter validation than development scripts
3. **Analyze the query**: Check for issues across all categories below
4. **Provide recommendations**: Be specific and actionable

## Dangerous operations

Flag these operations with warnings and require explicit user confirmation:

### High risk (always flag)
- `DROP DATABASE` - Irreversible data loss
- `DROP TABLE` without transaction wrapper
- `TRUNCATE TABLE` - Fast but unrecoverable without backup
- `DELETE` without `WHERE` clause - Deletes all rows
- `UPDATE` without `WHERE` clause - Updates all rows
- `DROP SCHEMA CASCADE` - Cascading deletions
- `ALTER TABLE ... DROP COLUMN` - Data loss
- Raw string interpolation in queries (SQL injection risk)

### Medium risk (flag in production context)
- `DELETE` or `UPDATE` with broad `WHERE` conditions
- `ALTER TABLE` on large tables without `CONCURRENTLY`
- `CREATE INDEX` without `CONCURRENTLY` on production tables
- `LOCK TABLE` statements
- Transactions without explicit `COMMIT`/`ROLLBACK`

### Context-dependent
- `SELECT *` - Flag in application code, acceptable in ad-hoc queries
- Missing `LIMIT` on potentially large result sets
- Recursive CTEs without termination safeguards

## Performance analysis

Check for and recommend fixes:

### Index issues
- Missing indexes on `WHERE`, `JOIN`, and `ORDER BY` columns
- Unused indexes (if schema context available)
- Over-indexing on write-heavy tables
- Missing covering indexes for frequent queries
- Recommend `INCLUDE` columns for index-only scans

### Query patterns
- N+1 query patterns in application code
- Correlated subqueries that could be JOINs
- `DISTINCT` that indicates missing `GROUP BY` or bad joins
- `ORDER BY` on non-indexed columns with large result sets
- Missing `LIMIT` with `OFFSET` pagination (suggest keyset pagination)
- `COUNT(*)` on large tables (suggest approximate counts)
- `NOT IN` with NULLable columns (use `NOT EXISTS` instead)

### PostgreSQL 18 specific
- Recommend `MERGE` for upsert patterns instead of `ON CONFLICT`
- Use `JSON_TABLE` for complex JSON extraction
- Leverage improved parallel query capabilities
- Use `ANY_VALUE()` aggregate for non-grouped columns
- Recommend virtual generated columns where appropriate

### Execution hints
- Suggest `EXPLAIN ANALYZE` for complex queries
- Recommend `SET` parameters for specific query optimization
- Identify candidates for prepared statements

## Security analysis

### SQL injection
- **Critical**: Flag any string concatenation/interpolation in queries
- Require parameterized queries (`$1`, `%s`, `:param`)
- Check for safe query builders in ORMs

### Privilege issues
- Flag `GRANT ALL` - prefer minimal privileges
- Warn on `SECURITY DEFINER` functions without careful review
- Check for `PUBLIC` schema permissions
- Flag hardcoded credentials

### Data exposure
- Warn on queries returning sensitive columns without filtering
- Flag missing `WHERE` clauses that could expose all data
- Check for proper `LIMIT` on user-facing queries

## Best practices

### Naming conventions
- Tables: `snake_case`, plural (`users`, `order_items`)
- Columns: `snake_case`, singular descriptive names
- Indexes: `idx_{table}_{columns}`
- Constraints: `{table}_{type}_{columns}` (e.g., `users_pk_id`, `orders_fk_user_id`)
- Functions: `snake_case` with verb prefix

### Schema design
- Require primary keys on all tables
- Recommend `UUID` or `BIGSERIAL` for primary keys
- Suggest appropriate data types (e.g., `TIMESTAMPTZ` over `TIMESTAMP`)
- Flag `TEXT` without length consideration
- Recommend `NOT NULL` constraints with defaults
- Suggest `CHECK` constraints for data validation
- Use `GENERATED ALWAYS AS IDENTITY` over `SERIAL`

### Query style
- Use explicit `JOIN` syntax (not comma joins)
- Qualify column names in multi-table queries
- Use CTEs for complex queries (readability)
- Prefer `COALESCE` over `CASE WHEN ... IS NULL`
- Use `FILTER` clause with aggregates instead of `CASE`

### Transaction handling
- Wrap DDL in transactions
- Use `BEGIN`/`COMMIT` explicitly in scripts
- Recommend savepoints for complex transactions
- Check for proper error handling around transactions

## Embedded SQL detection

### Python patterns
```python
# Detect SQL in:
cursor.execute("SELECT ...")
connection.execute(text("SELECT ..."))
session.execute("SELECT ...")
pd.read_sql("SELECT ...", conn)
engine.execute("SELECT ...")

# String patterns:
sql = "SELECT ..."
query = f"SELECT ... WHERE id = {id}"  # FLAG: injection risk
query = "SELECT ... WHERE id = %s"     # OK: parameterized
```

### JavaScript/TypeScript patterns
```typescript
// Detect SQL in:
pool.query("SELECT ...")
client.query("SELECT ...")
knex.raw("SELECT ...")
prisma.$queryRaw`SELECT ...`
sequelize.query("SELECT ...")

// String patterns:
const sql = `SELECT ... WHERE id = ${id}`  // FLAG: injection risk
const sql = "SELECT ... WHERE id = $1"     // OK: parameterized
```

## Response format

When analyzing SQL, structure response as:

### Summary
Brief overview of what the query/schema does.

### Issues found
List issues by severity:
- **Critical**: Must fix before use (injection, data loss risk)
- **Warning**: Should fix (performance, security concerns)
- **Suggestion**: Consider improving (best practices)

### Recommendations
Specific, actionable fixes with code examples.

### Improved version
Provide corrected SQL when applicable.

## Examples

### Dangerous query detection
```sql
-- User wrote:
DELETE FROM users;

-- Response:
-- CRITICAL: DELETE without WHERE clause will remove ALL rows from users table.
-- This is irreversible without a backup.
--
-- If intentional, use TRUNCATE (faster) or add explicit WHERE:
DELETE FROM users WHERE deleted_at < NOW() - INTERVAL '90 days';
```

### Performance recommendation
```sql
-- User wrote:
SELECT * FROM orders WHERE customer_id = 123 ORDER BY created_at DESC;

-- Response:
-- WARNING: SELECT * in application code - specify needed columns
-- SUGGESTION: Add index for this query pattern:
CREATE INDEX CONCURRENTLY idx_orders_customer_created
ON orders (customer_id, created_at DESC);

-- Improved:
SELECT id, total, status, created_at
FROM orders
WHERE customer_id = $1
ORDER BY created_at DESC
LIMIT 50;
```

### SQL injection detection
```python
# User wrote:
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# Response:
# CRITICAL: SQL injection vulnerability - user input directly interpolated
#
# Fix using parameterized query:
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

## PostgreSQL 18 features to recommend

When applicable, suggest modern PostgreSQL 18 features:

- `MERGE` statement for complex upserts
- `JSON_TABLE` for structured JSON querying
- Improved `COPY` with error handling (`ON_ERROR`)
- `ANY_VALUE()` aggregate function
- Enhanced parallel query execution
- Virtual generated columns
- Improved statistics for better query planning
