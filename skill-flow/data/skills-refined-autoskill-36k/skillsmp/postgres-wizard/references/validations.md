# Postgres Wizard - Validations

## SELECT * in Production Code

### **Id**
select-star
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - SELECT\s+\*\s+FROM
  - \.select\(\s*\*\s*\)
### **Message**
SELECT * fetches all columns. Wastes I/O, prevents covering indexes.
### **Fix Action**
List specific columns needed: SELECT id, name, created_at FROM
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.sql

## Foreign Key Without Index

### **Id**
missing-index-on-foreign-key
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - REFERENCES\s+\w+\s*\([^)]+\)(?!.*INDEX)
  - FOREIGN KEY\s*\([^)]+\)\s*REFERENCES(?!.*INDEX)
### **Message**
Foreign key without index. JOINs and cascade deletes will be slow.
### **Fix Action**
Create index on foreign key column
### **Applies To**
  - **/*.sql
  - **/migrations/**/*.py

## Query Without LIMIT

### **Id**
query-without-limit
### **Severity**
info
### **Type**
regex
### **Pattern**
  - SELECT[^;]+FROM[^;]+WHERE[^;]+(?!LIMIT)[^;]*;
  - \.find\(\{[^}]*\}\)(?!.*limit)
  - \.filter\([^)]+\)(?!.*\[:|\[0:|\.first)
### **Message**
Query without LIMIT may return unbounded results.
### **Fix Action**
Add LIMIT clause or implement pagination
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.sql

## LIKE Query With Leading Wildcard

### **Id**
like-without-index
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - LIKE\s*'%[^']+'
  - LIKE\\s*\\$[0-9]+(?=.*%)
  - ILIKE\s*'%
### **Message**
LIKE with leading wildcard can't use index. Will scan entire table.
### **Fix Action**
Use full-text search (tsvector), trigram index, or restructure query
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.sql

## SQL String Concatenation

### **Id**
no-prepared-statement
### **Severity**
error
### **Type**
regex
### **Pattern**
  - execute\s*\(\s*f"[^"]*\{[^}]+\}
  - execute\s*\(\s*f'[^']*\{[^}]+\}
  - query\s*\+\s*["'][^"']+["']\s*\+
  - `SELECT.*\$\{.*\}`
### **Message**
SQL string concatenation. SQL injection vulnerability.
### **Fix Action**
Use parameterized queries: execute(sql, (param,))
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Transaction Per Item in Loop

### **Id**
transaction-in-loop
### **Severity**
error
### **Type**
regex
### **Pattern**
  - for.*:.*await.*commit\(\)
  - for.*:.*await.*execute\(
  - \.forEach.*await.*query\(
### **Message**
Transaction per item in loop. N transactions instead of 1.
### **Fix Action**
Batch operations in single transaction or use executemany/COPY
### **Applies To**
  - **/*.py
  - **/*.ts

## Creating Connection Per Request

### **Id**
missing-connection-pool
### **Severity**
error
### **Type**
regex
### **Pattern**
  - async def.*:.*asyncpg\.connect\(
  - def.*:.*psycopg2\.connect\(
  - new Pool\(\)(?!.*max:)
### **Message**
Creating connection per request. Use connection pool.
### **Fix Action**
Use asyncpg.create_pool() or PgBouncer
### **Applies To**
  - **/*.py
  - **/*.ts

## Query Without Timeout

### **Id**
no-timeout-on-query
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - execute\([^)]+\)(?!.*timeout)
  - fetch\([^)]+\)(?!.*timeout)
  - \.query\([^)]+\)(?!.*timeout)
### **Message**
Query without timeout. Runaway query can block pool connections.
### **Fix Action**
Set statement_timeout or pass timeout parameter
### **Applies To**
  - **/*.py
  - **/*.ts

## ORDER BY Random/Expression

### **Id**
order-by-without-index
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ORDER BY\s+RANDOM\(\)
  - ORDER BY\s+\w+\s*\+\s*\w+
  - ORDER BY\s+LOWER\(
### **Message**
ORDER BY expression can't use index. May be slow on large result sets.
### **Fix Action**
Create expression index or limit result set first
### **Applies To**
  - **/*.sql
  - **/*.py
  - **/*.ts

## COUNT(*) to Check Existence

### **Id**
count-star-for-existence
### **Severity**
info
### **Type**
regex
### **Pattern**
  - COUNT\(\*\)\s*>\s*0
  - count\(\*\)\s*[!=]=\s*0
  - len\(.*SELECT.*COUNT
### **Message**
COUNT(*) scans all matching rows. EXISTS is faster for existence check.
### **Fix Action**
Use EXISTS(SELECT 1 FROM ... WHERE ... LIMIT 1)
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.sql

## Unbounded IN Clause

### **Id**
unbounded-in-clause
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - WHERE\s+\w+\s+IN\s*\(\s*SELECT
  - IN\s*\(\s*\$[0-9]+\s*\)
  - IN\s*\(\s*%s\s*\)
### **Message**
IN clause with subquery or parameter may be unbounded.
### **Fix Action**
Use JOIN instead of IN subquery, or limit array size
### **Applies To**
  - **/*.sql
  - **/*.py
  - **/*.ts

## JSON Extraction in WHERE Without Index

### **Id**
json-extract-in-where
### **Severity**
info
### **Type**
regex
### **Pattern**
  - WHERE.*->>'[^']+'
  - WHERE.*->'[^']+'
  - data\['[^']+'\]\s*==
### **Message**
JSON path in WHERE clause. Ensure GIN or expression index exists.
### **Fix Action**
Create index: CREATE INDEX ON t ((data->>'key'))
### **Applies To**
  - **/*.sql
  - **/*.py
  - **/*.ts