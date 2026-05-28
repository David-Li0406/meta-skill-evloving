# Drizzle Orm - Validations

## SQL Injection in Template Literal

### **Id**
drizzle-sql-injection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - sql`[^`]*'\$\{[^}]+\}'[^`]*`
  - sql`[^`]*"\\$\\{[^}]+\\}"[^`]*`
### **Message**
Potential SQL injection: user input interpolated with quotes. Use parameterized queries or remove quotes around ${}
### **Fix Action**
Remove quotes around ${variable} - Drizzle will parameterize it automatically
### **Applies To**
  - *.ts
  - *.tsx
  - *.js

## Drizzle Init Without Schema

### **Id**
drizzle-missing-schema
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - drizzle\(\s*\w+\s*\)(?!\s*\.)
  - from 'drizzle-orm/[^']+';[\s\S]{0,100}drizzle\([^,)]+\)[^{]*$
### **Message**
drizzle() called without schema. db.query (relational queries) won't work.
### **Fix Action**
Pass schema to drizzle(): drizzle(client, { schema })
### **Applies To**
  - *.ts
  - *.tsx
  - *.js

## Using serial() Instead of Identity

### **Id**
drizzle-serial-deprecated
### **Severity**
info
### **Type**
regex
### **Pattern**
  - serial\s*\([^)]*\)
### **Message**
serial() is legacy. PostgreSQL recommends identity columns or UUIDs.
### **Fix Action**
Use integer().generatedAlwaysAsIdentity() or uuid().defaultRandom()
### **Applies To**
  - *.ts
  - *.tsx

## Potential N+1 Query in Loop

### **Id**
drizzle-n-plus-one
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for\s*\([^)]*\)\s*\{[^}]*await\s+db\.(select|insert|update|delete)
  - forEach\([^)]*=>[^}]*await\s+db\.
  - \.map\([^)]*=>[^}]*await\s+db\.
### **Message**
Database query inside loop creates N+1 problem. Consider relational queries or batch operations.
### **Fix Action**
Use db.query with 'with' for related data, or batch the query outside the loop
### **Applies To**
  - *.ts
  - *.tsx
  - *.js

## Foreign Key Column Without .references()

### **Id**
drizzle-missing-references
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \w+Id:\s*(?:uuid|integer|text)\([^)]*\)(?!\.references)
  - _id'\)(?:\.[^.]+)*(?!\.references)
### **Message**
Column looks like a foreign key but missing .references(). Relations alone don't create DB constraints.
### **Fix Action**
Add .references(() => otherTable.id) for database-level foreign key
### **Applies To**
  - **/schema.ts
  - **/schema/*.ts

## Select All Columns (No Column Selection)

### **Id**
drizzle-select-star
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \\.select\\(\\)\\.from\\(
### **Message**
Selecting all columns. Consider specifying only needed columns for better performance.
### **Fix Action**
Use .select({ col1: table.col1, col2: table.col2 }) to select specific columns
### **Applies To**
  - *.ts
  - *.tsx
  - *.js

## Using Beta Version of Drizzle

### **Id**
drizzle-beta-version
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - "drizzle-orm":\\s*"[^"]*beta
  - "drizzle-kit":\\s*"[^"]*beta
### **Message**
Using beta version of Drizzle. May have breaking changes and ecosystem incompatibility.
### **Fix Action**
Consider using stable version unless testing beta features
### **Applies To**
  - package.json

## Accessing Properties on limit(1) Result

### **Id**
drizzle-limit-one-access
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\.limit\\(1\\)[^;]*;\\s*\\n[^\\[]*result\\.
  - \\.limit\\(1\\)\\s*;?\\s*$[\\s\\S]{0,50}\\w+\\.(id|name|email|title)
### **Message**
limit(1) returns an array, not single object. Use destructuring [result] or findFirst().
### **Fix Action**
Use const [item] = await query.limit(1) or db.query.table.findFirst()
### **Applies To**
  - *.ts
  - *.tsx
  - *.js

## JSONB Column with Default (Push Bug)

### **Id**
drizzle-jsonb-default
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - jsonb\\([^)]*\\)\\.default\\(
  - json\\([^)]*\\)\\.default\\(
### **Message**
jsonb/json with default may fail with drizzle-kit push. Use generate instead.
### **Fix Action**
Use drizzle-kit generate instead of push, or set default in application code
### **Applies To**
  - **/schema.ts
  - **/schema/*.ts

## Foreign Key Without onDelete Behavior

### **Id**
drizzle-missing-ondelete
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \\.references\\(\\(\\)\\s*=>\\s*\\w+\\.\\w+\\)(?![^)]*onDelete)
### **Message**
Foreign key without onDelete behavior. Consider adding { onDelete: 'cascade' } or similar.
### **Fix Action**
Add onDelete behavior: .references(() => table.id, { onDelete: 'cascade' })
### **Applies To**
  - **/schema.ts
  - **/schema/*.ts

## Raw SQL Execution

### **Id**
drizzle-raw-execute
### **Severity**
info
### **Type**
regex
### **Pattern**
  - db\\.execute\\(\\s*sql
  - \\.execute\\(\\s*`
### **Message**
Using raw SQL execution. Ensure proper parameterization to prevent injection.
### **Fix Action**
Prefer query builder methods. If using raw SQL, use sql placeholder: sql`...${param}...` without quotes
### **Applies To**
  - *.ts
  - *.tsx
  - *.js

## Foreign Key Column Without Index

### **Id**
drizzle-missing-index
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \\.references\\([^)]+\\)(?![\\s\\S]{0,200}index\\([^)]*\\))
### **Message**
Foreign key column might benefit from an index for JOIN performance.
### **Fix Action**
Consider adding an index: export const idx = index('idx_name').on(table.column)
### **Applies To**
  - **/schema.ts
  - **/schema/*.ts

## Transaction Without Await

### **Id**
drizzle-transaction-no-await
### **Severity**
error
### **Type**
regex
### **Pattern**
  - db\\.transaction\\([^)]+\\)(?!\\s*;?\\s*$)(?![\\s\\S]{0,10}await)
### **Message**
Transaction should be awaited. Without await, operations may not complete before continuing.
### **Fix Action**
Add await: await db.transaction(async (tx) => { ... })
### **Applies To**
  - *.ts
  - *.tsx
  - *.js