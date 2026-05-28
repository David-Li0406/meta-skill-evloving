# Backend - Validations

## SQL Injection Risk

### **Id**
backend-sql-injection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - `SELECT[^`]*\\$\\{
  - `INSERT[^`]*\\$\\{
  - `UPDATE[^`]*\\$\\{
  - `DELETE[^`]*\\$\\{
  - query\s*\([^)]*\+.*req\.
### **Message**
Potential SQL injection: user input concatenated into query string.
### **Fix Action**
Use parameterized queries ($1, $2) or ORM methods with typed inputs
### **Applies To**
  - *.ts
  - *.js

## Hardcoded Secret

### **Id**
backend-hardcoded-secret
### **Severity**
error
### **Type**
regex
### **Pattern**
  - sk_live_[a-zA-Z0-9]+
  - sk_test_[a-zA-Z0-9]+
  - password\s*[:=]\s*['"][^'"]{8,}['"]
  - api_key\s*[:=]\s*['"][^'"]{16,}['"]
  - secret\s*[:=]\s*['"][^'"]{8,}['"]
### **Message**
Potential hardcoded secret detected. Use environment variables.
### **Fix Action**
Move to environment variable and use process.env.SECRET_NAME
### **Applies To**
  - *.ts
  - *.js
  - *.json

## Unbounded Query

### **Id**
backend-findmany-no-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - findMany\\(\\s*\\)
  - findMany\\(\\s*\\{\\s*where[^}]*\\}\\s*\\)(?!.*take)
### **Message**
Query without limit can return millions of rows. Add take/limit.
### **Fix Action**
Add take: limit parameter, implement pagination
### **Applies To**
  - *.ts
  - *.js

## External Call in Transaction

### **Id**
backend-transaction-external-call
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \\$transaction[^}]*fetch\\(
  - \\$transaction[^}]*axios\\.
  - \\$transaction[^}]*stripe\\.
### **Message**
External API call inside transaction can hold locks for extended time.
### **Fix Action**
Move external calls outside transaction. Use pending states.
### **Applies To**
  - *.ts
  - *.js

## Cascade Delete on Relation

### **Id**
backend-cascade-delete
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - onDelete:\\s*Cascade
  - ON DELETE CASCADE
### **Message**
Cascade delete can cause long transactions on large tables.
### **Fix Action**
Consider soft delete or batched background deletion instead
### **Applies To**
  - *.prisma
  - *.sql

## Async Without Error Handling

### **Id**
backend-no-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - app\\.(?:get|post|put|delete)\\([^)]*,\\s*async\\s*\\([^)]*\\)\\s*=>\\s*\\{(?![^}]*try)
### **Message**
Async route handler without try/catch. Errors may crash or hang.
### **Fix Action**
Wrap in try/catch with next(error), or use asyncHandler wrapper
### **Applies To**
  - *.ts
  - *.js

## Fire and Forget Promise

### **Id**
backend-fire-and-forget
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?<!await\\s)sendEmail\\(
  - (?<!await\\s)createNotification\\(
  - (?<!await\\s)processAsync\\(
### **Message**
Promise not awaited - errors will be silently swallowed.
### **Fix Action**
Await the promise, or use a job queue for background processing
### **Applies To**
  - *.ts
  - *.js

## Auth Endpoint Without Rate Limit

### **Id**
backend-login-no-rate-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - app\.post\(['"].*login['"]
  - app\.post\(['"].*signin['"]
  - app\.post\(['"].*auth['"]
### **Message**
Authentication endpoint may need rate limiting for brute force protection.
### **Fix Action**
Add rate limiting middleware (express-rate-limit with Redis store)
### **Applies To**
  - *.ts
  - *.js

## Await in Loop (N+1 Risk)

### **Id**
backend-loop-await
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for\\s*\\([^)]*\\)\\s*\\{[^}]*await[^}]*find
  - \\.forEach\\([^)]*async[^}]*await[^}]*find
  - \\.map\\([^)]*async[^}]*await[^}]*find
### **Message**
Await inside loop may cause N+1 queries. Consider batching.
### **Fix Action**
Use include for eager loading, or batch with Promise.all and IN clause
### **Applies To**
  - *.ts
  - *.js

## Check-Then-Update Race Condition

### **Id**
backend-check-then-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - if\\s*\\([^)]*\\.balance[^}]*update
  - if\\s*\\([^)]*\\.stock[^}]*update
  - if\\s*\\([^)]*\\.count[^}]*update
### **Message**
Check-then-update pattern is vulnerable to race conditions.
### **Fix Action**
Use atomic update with WHERE condition, or SELECT FOR UPDATE
### **Applies To**
  - *.ts
  - *.js

## Synchronous File Processing

### **Id**
backend-sync-file-processing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await\\s+processImage\\(
  - await\\s+resize\\(
  - await\\s+transcode\\(
  - await\\s+generatePdf\\(
### **Message**
Heavy file processing in request handler may timeout.
### **Fix Action**
Move to background job queue (BullMQ, etc.) and return job ID
### **Applies To**
  - *.ts
  - *.js

## Missing Environment Variable Check

### **Id**
backend-missing-env-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - process\\.env\\.(?!NODE_ENV)[A-Z_]+(?![^;]*\\|\\||[^;]*\\?\\?|[^;]*throw|[^;]*if)
### **Message**
Environment variable used without validation or default.
### **Fix Action**
Add validation: if (!process.env.VAR) throw new Error('VAR required')
### **Applies To**
  - *.ts
  - *.js

## JWT Without Expiry

### **Id**
backend-jwt-no-expiry
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - jwt\\.sign\\([^)]*\\)(?![^;]*expiresIn)
  - sign\([^)]*,\s*['"][^'"]+['"]\s*\)
### **Message**
JWT signed without expiry. Tokens will be valid forever.
### **Fix Action**
Add expiresIn option: jwt.sign(payload, secret, { expiresIn: '1h' })
### **Applies To**
  - *.ts
  - *.js