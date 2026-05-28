# Trigger Dev - Validations

## Task without logging

### **Id**
trigger-task-no-logging
### **Severity**
warning
### **Type**
regex
### **Pattern**
task\(\{[^}]*run:\s*async[^}]*\}\)(?![\s\S]*logger\.)
### **Message**
Task has no logging. Add logger.log() calls for debugging in production.
### **Fix Action**
Import { logger } from '@trigger.dev/sdk/v3' and add log statements
### **Applies To**
  - **/trigger/**/*.ts
  - **/jobs/**/*.ts
  - **/tasks/**/*.ts

## Task without error handling

### **Id**
trigger-task-no-error-handling
### **Severity**
error
### **Type**
regex
### **Pattern**
task\(\{[^}]*run:\s*async[^}]*\}\)(?![\s\S]*try[\s\S]*catch)
### **Message**
Task lacks explicit error handling. Unhandled errors may cause unclear failures.
### **Fix Action**
Wrap task logic in try/catch and log errors with context
### **Applies To**
  - **/trigger/**/*.ts
  - **/jobs/**/*.ts
  - **/tasks/**/*.ts

## Task without concurrency limit

### **Id**
trigger-no-concurrency-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
task\(\{[^}]*\}\)(?![\s\S]*concurrencyLimit)
### **Message**
Task has no concurrency limit. High load may overwhelm downstream services.
### **Fix Action**
Add queue: { concurrencyLimit: 10 } to protect APIs and databases
### **Applies To**
  - **/trigger/**/*.ts
  - **/jobs/**/*.ts
  - **/tasks/**/*.ts

## Date object in trigger payload

### **Id**
trigger-date-in-payload
### **Severity**
error
### **Type**
regex
### **Pattern**
\.trigger\([^)]*new Date\(
### **Message**
Date objects are serialized to strings. Use ISO string format instead.
### **Fix Action**
Use date.toISOString() instead of new Date()
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Class instance in trigger payload

### **Id**
trigger-class-in-payload
### **Severity**
error
### **Type**
regex
### **Pattern**
\.trigger\([^)]*new [A-Z][a-zA-Z]+\(
### **Message**
Class instances lose methods when serialized. Use plain objects.
### **Fix Action**
Convert class instance to plain object before triggering
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Task without explicit ID

### **Id**
trigger-missing-task-id
### **Severity**
error
### **Type**
regex
### **Pattern**
task\(\{(?![^}]*id:)
### **Message**
Task must have an explicit id property for registration.
### **Fix Action**
Add id: 'my-task-name' to task definition
### **Applies To**
  - **/trigger/**/*.ts
  - **/jobs/**/*.ts
  - **/tasks/**/*.ts

## Trigger.dev API key hardcoded

### **Id**
trigger-api-key-hardcoded
### **Severity**
critical
### **Type**
regex
### **Pattern**
tr_[a-zA-Z0-9_]+
### **Message**
Trigger.dev API key should not be hardcoded - use TRIGGER_SECRET_KEY env var
### **Fix Action**
Remove hardcoded key and use process.env.TRIGGER_SECRET_KEY
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx

## Using raw OpenAI SDK instead of integration

### **Id**
trigger-raw-sdk-openai
### **Severity**
warning
### **Type**
regex
### **Pattern**
import.*from\s*['"]openai['"]
### **Message**
Consider using @trigger.dev/openai for automatic retries and rate limiting
### **Fix Action**
Replace with: import { openai } from '@trigger.dev/openai'
### **Applies To**
  - **/trigger/**/*.ts
  - **/jobs/**/*.ts
  - **/tasks/**/*.ts

## Using raw Anthropic SDK instead of integration

### **Id**
trigger-raw-sdk-anthropic
### **Severity**
warning
### **Type**
regex
### **Pattern**
import.*from\s*['"]@anthropic-ai/sdk['"]
### **Message**
Consider using @trigger.dev/anthropic for automatic retries and rate limiting
### **Fix Action**
Replace with: import { anthropic } from '@trigger.dev/anthropic'
### **Applies To**
  - **/trigger/**/*.ts
  - **/jobs/**/*.ts
  - **/tasks/**/*.ts

## wait.for inside loop

### **Id**
trigger-wait-in-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
for\s*\([^)]*\)\s*\{[\s\S]*?wait\.for
### **Message**
wait.for in loops creates many checkpoints. Consider batching instead.
### **Fix Action**
Batch items and use fewer waits, or split into subtasks
### **Applies To**
  - **/trigger/**/*.ts
  - **/jobs/**/*.ts
  - **/tasks/**/*.ts

## Task without retry configuration

### **Id**
trigger-no-retry-config
### **Severity**
info
### **Type**
regex
### **Pattern**
task\(\{[^}]*\}\)(?![\s\S]*retry:)
### **Message**
Task uses default retry config. Consider explicit retry settings.
### **Fix Action**
Add retry: { maxAttempts: 3, minTimeoutInMs: 1000 } for explicit control
### **Applies To**
  - **/trigger/**/*.ts
  - **/jobs/**/*.ts
  - **/tasks/**/*.ts

## Scheduled task without timezone

### **Id**
trigger-schedule-no-timezone
### **Severity**
warning
### **Type**
regex
### **Pattern**
schedules\.task\([^)]*cron:[^}]*\}(?![\s\S]*timezone)
### **Message**
Scheduled task has no timezone. Will use UTC by default.
### **Fix Action**
Add timezone option if specific timezone is needed
### **Applies To**
  - **/trigger/**/*.ts
  - **/jobs/**/*.ts
  - **/tasks/**/*.ts

## Large object in trigger payload

### **Id**
trigger-large-payload-warning
### **Severity**
warning
### **Type**
regex
### **Pattern**
\.trigger\(\{[^}]{500,}\}\)
### **Message**
Large payloads slow task processing. Pass IDs and fetch data in task.
### **Fix Action**
Store large data externally and pass only identifiers
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Synchronous blocking operation in task

### **Id**
trigger-sync-call-in-task
### **Severity**
warning
### **Type**
regex
### **Pattern**
run:\s*async[^}]*\{[\s\S]*?(fs\.readFileSync|fs\.writeFileSync|execSync)
### **Message**
Synchronous operations block the task. Use async alternatives.
### **Fix Action**
Use fs.promises or util.promisify for async operations
### **Applies To**
  - **/trigger/**/*.ts
  - **/jobs/**/*.ts
  - **/tasks/**/*.ts

## Direct env access without validation

### **Id**
trigger-env-direct-access
### **Severity**
warning
### **Type**
regex
### **Pattern**
process\.env\.[A-Z_]+(?![!?])
### **Message**
Environment variables should be validated. Missing vars cause runtime errors.
### **Fix Action**
Add non-null assertion or validate at startup: process.env.KEY!
### **Applies To**
  - **/trigger/**/*.ts
  - **/jobs/**/*.ts
  - **/tasks/**/*.ts