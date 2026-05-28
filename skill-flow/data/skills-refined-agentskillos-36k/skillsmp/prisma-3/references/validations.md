# Prisma - Validations

## New PrismaClient Per Request

### **Id**
new-client-per-request
### **Severity**
high
### **Type**
regex
### **Pattern**
async function.*\{[^}]*new PrismaClient\(\)
### **Message**
Creating PrismaClient per request causes connection exhaustion.
### **Fix Action**
Use singleton pattern from lib/prisma.ts
### **Applies To**
  - *.ts
  - *.js

## Foreign Key Without Index

### **Id**
missing-index-foreign-key
### **Severity**
medium
### **Type**
regex
### **Pattern**
@relation\(fields:\s*\[(\w+)\]
### **Negative Pattern**
@@index\(\[\1\]\)
### **Message**
Foreign key fields should have an index for query performance.
### **Fix Action**
Add @@index([fieldName]) to the model
### **Applies To**
  - schema.prisma

## FindMany Without Select

### **Id**
no-select-on-list
### **Severity**
low
### **Type**
regex
### **Pattern**
findMany\(\s*\{[^}]*where:
### **Negative Pattern**
select:|include:
### **Message**
Consider using select to limit returned fields for performance.
### **Fix Action**
Add select: { id: true, ... } for specific fields
### **Applies To**
  - *.ts

## Await in Loop (N+1 Risk)

### **Id**
loop-with-await
### **Severity**
high
### **Type**
regex
### **Pattern**
for.*\{[^}]*await prisma\.
### **Message**
Await in loop may cause N+1 queries. Consider batching.
### **Fix Action**
Use include for relations or batch with findMany/updateMany
### **Applies To**
  - *.ts
  - *.js

## Prisma Query Without Error Handling

### **Id**
no-error-handling
### **Severity**
medium
### **Type**
regex
### **Pattern**
await prisma\.\w+\.\w+\(
### **Negative Pattern**
try|catch|\.catch
### **Message**
Prisma queries should have error handling.
### **Fix Action**
Wrap in try/catch or add .catch() handler
### **Applies To**
  - *.ts
  - *.js

## Cascade Delete Without Comment

### **Id**
cascade-without-review
### **Severity**
medium
### **Type**
regex
### **Pattern**
onDelete:\s*Cascade
### **Message**
Cascade delete can remove more data than intended. Ensure this is desired.
### **Fix Action**
Add comment explaining cascade behavior or consider soft delete
### **Applies To**
  - schema.prisma

## Email/Username Without Unique

### **Id**
missing-unique-constraint
### **Severity**
high
### **Type**
regex
### **Pattern**
(email|username)\s+String(?!.*@unique)
### **Message**
Email and username fields should typically be unique.
### **Fix Action**
Add @unique attribute to field
### **Applies To**
  - schema.prisma

## Model Without updatedAt

### **Id**
no-updated-at
### **Severity**
low
### **Type**
regex
### **Pattern**
model \w+ \{[^}]*createdAt
### **Negative Pattern**
updatedAt
### **Message**
Model has createdAt but no updatedAt. Consider adding for tracking.
### **Fix Action**
Add updatedAt DateTime @updatedAt
### **Applies To**
  - schema.prisma

## Potential SQL Injection

### **Id**
raw-sql-injection
### **Severity**
high
### **Type**
regex
### **Pattern**
\$queryRaw`[^`]*\$\{[^}]+\}[^`]*`
### **Negative Pattern**
Prisma\.sql
### **Message**
Use parameterized queries or Prisma.sql for raw SQL to prevent injection.
### **Fix Action**
Use Prisma.sql template or parameterized $queryRaw
### **Applies To**
  - *.ts
  - *.js