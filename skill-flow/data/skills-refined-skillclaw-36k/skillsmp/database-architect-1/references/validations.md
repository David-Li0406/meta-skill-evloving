# Database Architect - Validations

## SELECT * Query

### **Id**
select-star
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - SELECT \*
  - findMany\(\)
  - \.all\(\)
### **Message**
SELECT * fetches unnecessary columns.
### **Fix Action**
Select only needed columns explicitly
### **Applies To**
  - **/*.sql
  - **/*.ts
  - **/*.py

## Query Without Pagination

### **Id**
no-pagination
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - SELECT.*(?<!LIMIT)
  - findMany\(\)(?!.*take)
  - find\(\)(?!.*limit)
### **Message**
Query without pagination may return too many rows.
### **Fix Action**
Add LIMIT or pagination parameters
### **Applies To**
  - **/*.sql
  - **/repositories/**/*.ts

## Query on Likely Unindexed Column

### **Id**
missing-index-hint
### **Severity**
info
### **Type**
regex
### **Pattern**
  - WHERE.*created_at
  - WHERE.*updated_at
  - ORDER BY.*created_at(?!.*DESC)
### **Message**
Query may benefit from index on this column.
### **Fix Action**
Verify index exists: CREATE INDEX idx_table_column ON table(column)
### **Applies To**
  - **/*.sql
  - **/queries/**/*.ts

## Reference Column Without Foreign Key

### **Id**
no-foreign-key
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - user_id.*INT(?!.*REFERENCES)
  - organization_id.*UUID(?!.*REFERENCES)
  - _id.*(?<!REFERENCES.*)
### **Message**
Reference column may be missing foreign key constraint.
### **Fix Action**
Add FOREIGN KEY REFERENCES for referential integrity
### **Applies To**
  - **/*.sql
  - **/migrations/**/*.sql

## Structured Data in JSON Column

### **Id**
json-structured-data
### **Severity**
info
### **Type**
regex
### **Pattern**
  - JSONB.*user_id
  - JSON.*status
  - JSONB.*email
### **Message**
Structured data in JSON loses query optimization.
### **Fix Action**
Extract frequently queried fields to columns
### **Applies To**
  - **/*.sql
  - **/schema/**/*.ts

## N+1 Query Pattern

### **Id**
n-plus-one-pattern
### **Severity**
error
### **Type**
regex
### **Pattern**
  - for.*in.*:.*find
  - \.forEach.*findOne
  - map.*prisma\.
### **Message**
Loop with query inside causes N+1 problem.
### **Fix Action**
Use eager loading, joins, or batch queries
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.js

## Foreign Key Without ON DELETE

### **Id**
cascade-delete-missing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - REFERENCES.*\)(?!.*ON DELETE)
### **Message**
Foreign key without ON DELETE may cause issues.
### **Fix Action**
Specify ON DELETE CASCADE, RESTRICT, or SET NULL
### **Applies To**
  - **/*.sql
  - **/migrations/**/*.sql

## Random UUID Primary Key

### **Id**
uuid-random
### **Severity**
info
### **Type**
regex
### **Pattern**
  - gen_random_uuid\(\)
  - uuid_generate_v4\(\)
  - UUID DEFAULT uuid
### **Message**
Random UUIDs cause index fragmentation on high-write tables.
### **Fix Action**
Consider UUIDv7, ULID, or BIGSERIAL for high-write tables
### **Applies To**
  - **/*.sql
  - **/schema/**/*.ts

## Long Transaction Pattern

### **Id**
long-transaction
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - BEGIN.*for
  - transaction.*while
  - \.transaction\(.*for
### **Message**
Long transactions hold locks and block others.
### **Fix Action**
Break into smaller transactions or batches
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.sql

## SQL Injection Risk

### **Id**
raw-sql-injection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - query.*\$\{
  - execute.*\+.*\+
  - raw.*f"
### **Message**
String interpolation in SQL is injection risk.
### **Fix Action**
Use parameterized queries
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.js

## CREATE INDEX Without CONCURRENTLY

### **Id**
index-on-create
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - CREATE INDEX(?!.*CONCURRENTLY)
### **Message**
CREATE INDEX locks table. Use CONCURRENTLY in production.
### **Fix Action**
Use CREATE INDEX CONCURRENTLY for production
### **Applies To**
  - **/migrations/**/*.sql