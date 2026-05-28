# Graphile Worker - Validations

## Large Object in Job Payload

### **Id**
job-payload-too-large
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - add_job\([^)]*JSON\.stringify\([^)]+\)\s*\)
  - quickAddJob\([^)]*\{[^}]{500,}\}
  - add_job.*json_build_object\([^)]{500,}\)
### **Message**
Large payload in job data. Store references instead of full objects.
### **Fix Action**
Pass IDs/URLs, fetch data in task handler
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.sql

## Error Caught But Not Rethrown in Task

### **Id**
error-swallowed-in-task
### **Severity**
error
### **Type**
regex
### **Pattern**
  - Task\s*=.*catch\s*\([^)]*\)\s*\{[^}]*console
  - Task.*catch.*\{[^}]*\}(?!.*throw)
### **Message**
Error swallowed in task handler. Job won't retry on failure.
### **Fix Action**
Re-throw errors after logging: catch (e) { logger.error(e); throw e; }
### **Applies To**
  - **/*.ts
  - **/*.js

## Job Added Outside Transaction

### **Id**
add-job-outside-transaction
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await\s+\w+\.create\([^)]+\);\s*\n\s*await\s+.*add_job
  - insert.*commit.*add_job
  - addJob\([^)]+\);\s*\n\s*await\s+db\.
### **Message**
Job queued outside data transaction. Risk of inconsistent state.
### **Fix Action**
Queue job in same transaction as data changes
### **Applies To**
  - **/*.ts
  - **/*.js

## Polling Mode Instead of LISTEN/NOTIFY

### **Id**
polling-enabled
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pollInterval\s*:
  - poll_interval\s*=
  - noHandleSignals\s*:\s*true
### **Message**
Polling mode adds latency. Use LISTEN/NOTIFY for fast job pickup.
### **Fix Action**
Remove polling config, ensure LISTEN/NOTIFY works
### **Applies To**
  - **/*.ts
  - **/*.js

## Job Without Max Attempts Limit

### **Id**
no-max-attempts
### **Severity**
info
### **Type**
regex
### **Pattern**
  - add_job\([^)]+\)(?!.*max_attempts)
  - quickAddJob\([^)]+\)(?!.*maxAttempts)
### **Message**
Job without max_attempts may retry indefinitely on persistent failure.
### **Fix Action**
Set max_attempts based on job type (e.g., 3-5 for API calls)
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.sql

## Cron Schedule Without Timezone

### **Id**
cron-without-timezone
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - parseCronItems\([^)]+\)(?!.*tz)
  - schedule.*pattern.*(?!.*tz)
  - crontab.*\d+\s+\d+\s+\*(?!.*\?tz)
### **Message**
Cron schedule without timezone. Jobs may run at unexpected times.
### **Fix Action**
Add timezone: ?tz=America/New_York or options: { tz: '...' }
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/crontab

## Synchronous Blocking in Async Task

### **Id**
sync-in-task-handler
### **Severity**
error
### **Type**
regex
### **Pattern**
  - Task.*fs\.readFileSync
  - Task.*execSync
  - Task.*\.forEach\(async
### **Message**
Blocking operation in async task handler. Use async alternatives.
### **Fix Action**
Use fs.promises.readFile, exec with promisify, for...of with await
### **Applies To**
  - **/*.ts
  - **/*.js

## Worker Without Graceful Shutdown

### **Id**
missing-graceful-shutdown
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - run\(\{[^}]+\}\)(?!.*SIGTERM|signal)
  - graphile-worker.*(?!.*stop\(\))
### **Message**
Worker without graceful shutdown. In-flight jobs may be lost.
### **Fix Action**
Handle SIGTERM: process.on('SIGTERM', () => runner.stop())
### **Applies To**
  - **/*.ts
  - **/*.js

## Task Function Not Exported

### **Id**
task-file-not-exported
### **Severity**
error
### **Type**
regex
### **Pattern**
  - const\s+\w+:\s*Task\s*=(?!.*export)
  - function\s+\w+\s*\([^)]*helpers[^)]*\)(?!.*export)
### **Message**
Task function not exported. Graphile Worker won't find it.
### **Fix Action**
Export the task: export const taskName: Task = ...
### **Applies To**
  - **/tasks/**/*.ts
  - **/tasks/**/*.js