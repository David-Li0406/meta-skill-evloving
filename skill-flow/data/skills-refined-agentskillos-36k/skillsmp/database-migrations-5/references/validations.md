# Database Migrations - Validations

## NOT NULL without DEFAULT on existing table

### **Id**
not-null-without-default
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - ADD\s+COLUMN.*NOT\s+NULL(?!.*DEFAULT)
  - ALTER\s+COLUMN.*SET\s+NOT\s+NULL
### **Message**
Adding NOT NULL without DEFAULT locks table for rewrite
### **Fix Action**
Add DEFAULT clause or use multi-step migration
### **Applies To**
  - *.sql

## Column rename detected

### **Id**
column-rename
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - RENAME\s+COLUMN
  - RENAME\s+TO
### **Message**
Column rename breaks backwards compatibility
### **Fix Action**
Use expand-contract pattern instead
### **Applies To**
  - *.sql

## Column drop without backup plan

### **Id**
column-drop
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - DROP\s+COLUMN
### **Message**
Dropping column is irreversible - ensure data is backed up
### **Fix Action**
Verify data migrated, add to down migration
### **Applies To**
  - *.sql

## Table drop detected

### **Id**
table-drop
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - DROP\s+TABLE
### **Message**
Dropping table is irreversible - ensure data is backed up
### **Fix Action**
Archive data first, verify no remaining dependencies
### **Applies To**
  - *.sql

## CREATE INDEX without CONCURRENTLY

### **Id**
index-not-concurrent
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - CREATE\s+INDEX(?!\s+CONCURRENTLY)
  - CREATE\s+UNIQUE\s+INDEX(?!\s+CONCURRENTLY)
### **Message**
Non-concurrent index creation blocks writes
### **Fix Action**
Use CREATE INDEX CONCURRENTLY
### **Applies To**
  - *.sql

## DROP INDEX without CONCURRENTLY

### **Id**
drop-index-not-concurrent
### **Severity**
info
### **Type**
regex
### **Pattern**
  - DROP\s+INDEX(?!\s+CONCURRENTLY)
### **Message**
Non-concurrent index drop may block queries
### **Fix Action**
Use DROP INDEX CONCURRENTLY for large tables
### **Applies To**
  - *.sql

## UPDATE without WHERE or LIMIT

### **Id**
unbounded-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - UPDATE\s+\w+\s+SET(?!.*WHERE)(?!.*LIMIT)
### **Message**
Unbounded UPDATE may lock table for extended period
### **Fix Action**
Add WHERE clause or batch with LIMIT
### **Applies To**
  - *.sql

## DELETE without WHERE or LIMIT

### **Id**
unbounded-delete
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - DELETE\s+FROM\s+\w+(?!.*WHERE)(?!.*LIMIT)
### **Message**
Unbounded DELETE may lock table for extended period
### **Fix Action**
Add WHERE clause or batch with LIMIT
### **Applies To**
  - *.sql

## Column type change detected

### **Id**
type-change
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ALTER\s+COLUMN.*TYPE
  - ALTER\s+COLUMN.*SET\s+DATA\s+TYPE
### **Message**
Type change may require table rewrite
### **Fix Action**
Test on production-size data, plan for downtime
### **Applies To**
  - *.sql

## ENUM type creation

### **Id**
enum-creation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - CREATE\s+TYPE.*ENUM
### **Message**
ENUMs are hard to modify later
### **Fix Action**
Consider using VARCHAR with CHECK constraint instead
### **Applies To**
  - *.sql

## Prisma db push in production

### **Id**
prisma-db-push
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - prisma\s+db\s+push
  - npx\s+prisma\s+db\s+push
### **Message**
db push bypasses migration system - use migrate deploy
### **Fix Action**
Use prisma migrate deploy for production
### **Applies To**
  - *.sh
  - *.yml
  - *.yaml
  - Dockerfile

## Drizzle push in production

### **Id**
drizzle-push
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - drizzle-kit\s+push
  - npx\s+drizzle-kit\s+push
### **Message**
drizzle push bypasses migration system
### **Fix Action**
Use drizzle-kit generate + migrate for production
### **Applies To**
  - *.sh
  - *.yml
  - *.yaml
  - Dockerfile