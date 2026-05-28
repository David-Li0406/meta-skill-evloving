# Migration Specialist - Validations

## Index Creation Without CONCURRENTLY

### **Id**
non-concurrent-index
### **Severity**
error
### **Type**
regex
### **Pattern**
  - CREATE INDEX(?!\s+CONCURRENTLY)
  - CREATE UNIQUE INDEX(?!\s+CONCURRENTLY)
### **Message**
CREATE INDEX without CONCURRENTLY locks table writes.
### **Fix Action**
Use CREATE INDEX CONCURRENTLY for online index creation
### **Applies To**
  - **/*.sql
  - **/migrations/**/*

## Dropping Column Without Expand Phase

### **Id**
direct-column-drop
### **Severity**
error
### **Type**
regex
### **Pattern**
  - DROP COLUMN(?!.*--.*expand)
  - ALTER TABLE.*DROP.*COLUMN
### **Message**
Dropping column immediately may break running code.
### **Fix Action**
Use expand-contract: stop using column in code first, then drop
### **Applies To**
  - **/*.sql
  - **/migrations/**/*

## Adding NOT NULL Without Default Value

### **Id**
not-null-without-default
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ADD COLUMN.*NOT NULL(?!.*DEFAULT)
  - ALTER.*SET NOT NULL(?!.*DEFAULT)
### **Message**
Adding NOT NULL without default fails if rows exist.
### **Fix Action**
Add default value or backfill before adding constraint
### **Applies To**
  - **/*.sql
  - **/migrations/**/*

## Changing Column Type Directly

### **Id**
alter-column-type
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ALTER COLUMN.*TYPE
  - MODIFY COLUMN.*TO
### **Message**
Changing column type may lock table and lose data.
### **Fix Action**
Use expand-contract: add new column, migrate, drop old
### **Applies To**
  - **/*.sql
  - **/migrations/**/*

## Migration Without Rollback

### **Id**
no-rollback-migration
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - def upgrade(?!.*def downgrade)
  - exports\.up(?!.*exports\.down)
### **Message**
Migration without rollback function.
### **Fix Action**
Add downgrade/down function for rollback capability
### **Applies To**
  - **/migrations/**/*.py
  - **/migrations/**/*.js

## Update Without LIMIT or Batching

### **Id**
unbounded-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - UPDATE.*SET(?!.*LIMIT|.*WHERE.*IN.*SELECT.*LIMIT)
  - UPDATE.*WHERE(?!.*LIMIT)
### **Message**
Unbounded UPDATE may take too long on large tables.
### **Fix Action**
Use batched updates with LIMIT or chunk by ID range
### **Applies To**
  - **/*.sql
  - **/migrations/**/*

## Foreign Key Without NOT VALID

### **Id**
fk-without-not-valid
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ADD CONSTRAINT.*FOREIGN KEY(?!.*NOT VALID)
  - REFERENCES.*\)(?!.*NOT VALID)
### **Message**
Adding FK validates all rows, holding lock.
### **Fix Action**
Add with NOT VALID, then VALIDATE CONSTRAINT separately
### **Applies To**
  - **/*.sql
  - **/migrations/**/*

## Cascade Delete on Large Table

### **Id**
cascade-delete
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ON DELETE CASCADE
  - ON UPDATE CASCADE
### **Message**
Cascade operations can affect many rows unexpectedly.
### **Fix Action**
Consider soft deletes or application-level cascades for control
### **Applies To**
  - **/*.sql
  - **/migrations/**/*

## TRUNCATE in Migration

### **Id**
truncate-in-migration
### **Severity**
error
### **Type**
regex
### **Pattern**
  - TRUNCATE TABLE
  - TRUNCATE.*CASCADE
### **Message**
TRUNCATE in migration loses data permanently.
### **Fix Action**
Use DELETE with conditions, or ensure this is intended
### **Applies To**
  - **/*.sql
  - **/migrations/**/*

## Renaming Table Directly

### **Id**
rename-table-direct
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ALTER TABLE.*RENAME TO
  - RENAME TABLE
### **Message**
Renaming table breaks running code referencing old name.
### **Fix Action**
Use view as alias, or expand-contract pattern
### **Applies To**
  - **/*.sql
  - **/migrations/**/*

## Migration Without Transaction

### **Id**
no-transaction-migration
### **Severity**
info
### **Type**
regex
### **Pattern**
  - BEGIN(?!.*COMMIT|.*ROLLBACK)
  - START TRANSACTION(?!.*COMMIT)
### **Message**
Migration may not be transactional. Partial failure possible.
### **Fix Action**
Ensure migration runs in transaction or is idempotent
### **Applies To**
  - **/*.sql
  - **/migrations/**/*

## Hardcoded Batch Size in Migration

### **Id**
hardcoded-table-size-assumption
### **Severity**
info
### **Type**
regex
### **Pattern**
  - LIMIT\s+\d{5,}
  - batch_size\s*=\s*\d{5,}
### **Message**
Large batch sizes may cause memory or timeout issues.
### **Fix Action**
Test batch size on production-scale data
### **Applies To**
  - **/*.sql
  - **/migrations/**/*