# Workflow Automation - Validations

## External Calls Without Idempotency Key

### **Id**
step-missing-idempotency
### **Severity**
error
### **Description**
Stripe/payment calls should use idempotency keys
### **Pattern**
  stripe\.(paymentIntents|charges|transfers)\.(create|update)\(
  
### **Anti Pattern**
  idempotency_key
  
### **Message**
Payment call without idempotency_key. Add idempotency key to prevent duplicate charges on retry.
### **Autofix**


## Email Sending Without Deduplication

### **Id**
email-without-dedup
### **Severity**
warning
### **Description**
Email sends in workflows should check for already-sent
### **Pattern**
  sendEmail|send_email|postmark\.send|sendgrid\.send
  
### **Anti Pattern**
  alreadySent|already_sent|idempotency|checkSent
  
### **Message**
Email sent in workflow without deduplication check. Retries may send duplicate emails.
### **Autofix**


## Temporal Activities Without Timeout

### **Id**
temporal-no-timeout
### **Severity**
error
### **Description**
All Temporal activities need timeout configuration
### **Pattern**
  proxyActivities<
  
### **Anti Pattern**
  startToCloseTimeout|scheduleToCloseTimeout
  
### **Message**
proxyActivities without timeout. Add startToCloseTimeout to prevent indefinite hangs.
### **Autofix**


## Inngest Steps Calling External APIs Without Timeout

### **Id**
inngest-step-no-timeout
### **Severity**
warning
### **Description**
External API calls should have timeouts
### **Pattern**
  step\.run\([^)]+async.*fetch\(|step\.run\([^)]+async.*axios
  
### **Anti Pattern**
  timeout|AbortSignal
  
### **Message**
External API call in step without timeout. Add timeout to prevent workflow hangs.
### **Autofix**


## Random Values in Workflow Code

### **Id**
random-in-workflow
### **Severity**
error
### **Description**
Random values break determinism on replay
### **Pattern**
  Math\.random\(\)|crypto\.randomUUID\(\)|uuid\(\)
  
### **Message**
Random value in workflow code. Move to activity/step or use sideEffect.
### **Autofix**


## Date.now() in Workflow Code

### **Id**
date-now-in-workflow
### **Severity**
error
### **Description**
Current time breaks determinism on replay
### **Pattern**
  Date\.now\(\)|new Date\(\)
  
### **Message**
Current time in workflow code. Use workflow.now() or move to activity/step.
### **Autofix**


## Inngest Function Without onFailure Handler

### **Id**
no-onfailure-handler
### **Severity**
warning
### **Description**
Production functions should have failure handlers
### **Pattern**
  inngest\.createFunction\(
  
### **Anti Pattern**
  onFailure
  
### **Message**
Inngest function without onFailure handler. Add failure handling for production reliability.
### **Autofix**


## Step Without Error Handling

### **Id**
no-try-catch-in-step
### **Severity**
warning
### **Description**
Steps should handle errors gracefully
### **Pattern**
  step\.run\([^)]+async\s*\(\)\s*=>\s*\{[^}]+\}
  
### **Anti Pattern**
  try|catch|NonRetriableError
  
### **Message**
Step without try/catch. Consider handling specific error cases.
### **Autofix**


## Potentially Large Data Returned from Step

### **Id**
large-step-return
### **Severity**
info
### **Description**
Large data in workflow state slows execution
### **Pattern**
  return\s+(await\s+)?fetch|return\s+data|return\s+records
  
### **Message**
Returning potentially large data from step. Consider storing in S3/DB and returning reference.
### **Autofix**


## Retry Without Backoff Configuration

### **Id**
retry-no-backoff
### **Severity**
warning
### **Description**
Retries should use exponential backoff
### **Pattern**
  maximumAttempts:\s*\d+
  
### **Anti Pattern**
  backoffCoefficient|initialInterval
  
### **Message**
Retry configured without backoff. Add backoffCoefficient and initialInterval.
### **Autofix**


## n8n Workflow Without Error Handling

### **Id**
n8n-no-error-trigger
### **Severity**
warning
### **Description**
Production workflows need Error Trigger
### **File Pattern**
*.json
### **Pattern**
  "type":\s*"n8n-nodes-base\.(webhook|schedule)"
  
### **Anti Pattern**
  "type":\s*"n8n-nodes-base\.errorTrigger"
  
### **Message**
n8n workflow without Error Trigger node. Add for production error visibility.
### **Autofix**


## Long Temporal Activity Without Heartbeat

### **Id**
temporal-long-activity-no-heartbeat
### **Severity**
warning
### **Description**
Activities over 10s should heartbeat
### **Pattern**
  startToCloseTimeout:\s*['"]([0-9]+\s*)?(minutes?|hours?)['"]
  
### **Anti Pattern**
  heartbeatTimeout|heartbeat\(
  
### **Message**
Long-running activity without heartbeat. Add heartbeat for cancellation support.
### **Autofix**
