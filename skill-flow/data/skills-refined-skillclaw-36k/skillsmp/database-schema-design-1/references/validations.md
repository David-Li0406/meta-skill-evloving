# Database Schema Design - Validations

## Float Type for Financial Data

### **Id**
schema-float-for-money
### **Severity**
error
### **Type**
regex
### **Pattern**
  - Float.*price
  - Float.*amount
  - Float.*balance
  - Float.*cost
  - Float.*total
  - Float.*fee
  - Float.*payment
  - DOUBLE.*price
  - REAL.*amount
### **Message**
Float/Double for money causes rounding errors. Use Decimal or integer cents.
### **Fix Action**
Change to Decimal @db.Decimal(10, 2) or store as integer cents
### **Applies To**
  - *.prisma
  - schema.prisma
  - *.sql

## Foreign Key Without Index

### **Id**
schema-missing-fk-index
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - @relation\\(fields:\\s*\\[[^\\]]+\\][^}]*\\)(?![^}]*@@index)
### **Message**
Foreign key without index causes slow JOINs and DELETE locks.
### **Fix Action**
Add @@index([foreignKeyColumn]) to the model
### **Applies To**
  - *.prisma
  - schema.prisma

## Cascade Delete on Relation

### **Id**
schema-cascade-delete
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - onDelete:\\s*Cascade
  - ON DELETE CASCADE
### **Message**
Cascade delete can lock tables for extended time on large datasets.
### **Fix Action**
Consider soft delete or background job for cleanup instead
### **Applies To**
  - *.prisma
  - schema.prisma
  - *.sql

## UUID Without Version Specification

### **Id**
schema-uuid-no-version
### **Severity**
info
### **Type**
regex
### **Pattern**
  - @default\\(uuid\\(\\)\\)
  - gen_random_uuid\(\)(?!.*v7)
### **Message**
Consider UUID v7 for better index performance (time-ordered).
### **Fix Action**
For distributed systems, use UUID v7 via middleware or dbgenerated
### **Applies To**
  - *.prisma
  - schema.prisma
  - *.sql

## Timestamp Without Timezone

### **Id**
schema-timestamp-no-tz
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - DateTime(?!.*@db\\.Timestamptz)
  - TIMESTAMP(?!TZ| WITH TIME ZONE)
### **Message**
Timestamp without timezone causes confusion in multi-region systems.
### **Fix Action**
Use DateTime @db.Timestamptz for PostgreSQL, always store UTC
### **Applies To**
  - *.prisma
  - schema.prisma
  - *.sql

## String Without Length Limit

### **Id**
schema-varchar-no-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - String(?!.*@db\\.VarChar)
  - VARCHAR(?!\\s*\\()
  - TEXT.*name|TEXT.*title|TEXT.*email
### **Message**
String without length limit allows unexpectedly large values.
### **Fix Action**
Add @db.VarChar(n) with reasonable max length
### **Applies To**
  - *.prisma
  - schema.prisma
  - *.sql

## Missing updatedAt Timestamp

### **Id**
schema-no-updated-at
### **Severity**
info
### **Type**
regex
### **Pattern**
  - model\\s+\\w+\\s*\\{[^}]*createdAt[^}]*(?!updatedAt)[^}]*\\}
### **Message**
Model has createdAt but no updatedAt - common pattern for tracking changes.
### **Fix Action**
Add updatedAt DateTime @updatedAt
### **Applies To**
  - *.prisma
  - schema.prisma

## Type Discriminator Pattern

### **Id**
schema-polymorphic-discriminator
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Type\\s+String.*Id\\s+String
  - commentableType|parentType|ownerType
  - able_type.*able_id
### **Message**
Type discriminator polymorphism prevents foreign key enforcement.
### **Fix Action**
Use exclusive arc pattern with separate nullable FKs and CHECK constraint
### **Applies To**
  - *.prisma
  - schema.prisma
  - *.ts
  - *.js

## Enum ADD VALUE with Usage in Same Migration

### **Id**
schema-enum-migration-same-tx
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ALTER TYPE.*ADD VALUE[^;]*;[^;]*INSERT
  - ALTER TYPE.*ADD VALUE[^;]*;[^;]*UPDATE
### **Message**
New enum value cannot be used in same transaction as ALTER TYPE ADD VALUE.
### **Fix Action**
Split into two separate migrations - add value first, then use it
### **Applies To**
  - *.sql

## DROP COLUMN Without Safety Check

### **Id**
schema-drop-column-no-backup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - DROP COLUMN(?! IF EXISTS)
  - DROP TABLE(?! IF EXISTS)
### **Message**
Destructive migration without IF EXISTS. Ensure rollback plan exists.
### **Fix Action**
Add IF EXISTS, verify rollback script, backup data before running
### **Applies To**
  - *.sql

## Migration with Await in Loop

### **Id**
schema-migration-loop-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for\\s*\\([^)]*\\)\\s*\\{[^}]*await[^}]*update
  - \\.forEach\\([^)]*async[^}]*await[^}]*update
  - \\.map\\([^)]*async[^}]*await[^}]*update
### **Message**
Migration loops with await run N queries. Use single UPDATE statement.
### **Fix Action**
Replace loop with single SQL UPDATE or use executeRaw with batching
### **Applies To**
  - *.ts
  - *.js

## Email/Username Without Unique Constraint

### **Id**
schema-missing-unique-constraint
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - email\\s+String(?!.*@unique)
  - username\\s+String(?!.*@unique)
  - slug\\s+String(?!.*@unique)
### **Message**
Email/username/slug columns typically need unique constraints.
### **Fix Action**
Add @unique or @@unique([column, deletedAt]) for soft delete
### **Applies To**
  - *.prisma
  - schema.prisma

## Soft Delete Column Without Index

### **Id**
schema-soft-delete-no-index
### **Severity**
info
### **Type**
regex
### **Pattern**
  - deletedAt\\s+DateTime\\?(?![^}]*@@index.*deletedAt)
### **Message**
deletedAt column without index makes filtering deleted records slow.
### **Fix Action**
Add @@index([deletedAt]) or partial index WHERE deletedAt IS NULL
### **Applies To**
  - *.prisma
  - schema.prisma