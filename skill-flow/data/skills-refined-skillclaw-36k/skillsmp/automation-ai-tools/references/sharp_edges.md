# Automation - Sharp Edges

## Task Explosion

### **Id**
task-explosion
### **Summary**
Automation costs can explode unexpectedly
### **Severity**
critical
### **Tools Affected**
  - zapier
  - make
### **Situation**
Per-task pricing meets high-volume triggers
### **Why**
  Per-task pricing seems cheap until:
  - Trigger fires more often than expected
  - Loop creates thousands of tasks
  - Retry logic multiplies tasks
  - Webhook receives spam
  
  One bad automation can burn your monthly quota in hours.
  
### **Solution**
  1. Understand exactly what counts as a "task"
  2. Add filters BEFORE actions (Zapier) to reduce tasks
  3. Set up usage alerts at 50%, 75%, 90%
  4. Review task-heavy automations weekly
  5. Use n8n or Activepieces for unlimited execution
  6. Batch operations where possible
  
### **Symptoms**
  - Hit monthly limit mid-month
  - Unexpected billing spike
  - Automations paused due to quota

## Hidden Operation Costs

### **Id**
hidden-operation-costs
### **Summary**
Each step in Make costs operations
### **Severity**
medium
### **Tools Affected**
  - make
### **Situation**
Complex scenarios use more operations than expected
### **Why**
  In Make, every module = operations:
  - A 10-step scenario = 10 operations per run
  - Iterators multiply operations
  - Routers add operations
  - Error handlers add operations
  
  What looks like 1 automation can be 50+ operations.
  
### **Solution**
  1. Count operations before deploying
  2. Use aggregators to batch
  3. Minimize modules where possible
  4. Consider operation limits per scenario
  5. Monitor operations dashboard
  
### **Symptoms**
  - Operations run out faster than expected
  - Simple automation uses many operations

## Silent Failures

### **Id**
silent-failures
### **Summary**
Automations fail silently without notification
### **Severity**
high
### **Tools Affected**
  - zapier
  - make
  - n8n
### **Situation**
Automation breaks but nobody knows
### **Why**
  Common failure scenarios:
  - API changes without notice
  - Auth tokens expire
  - Rate limits hit
  - Data format changes
  - Service downtime
  
  Without monitoring, business processes just stop.
  
### **Solution**
  1. Set up error notifications (Slack, email)
  2. Monitor key automations dashboard
  3. Test regularly (monthly health checks)
  4. Have manual fallback processes
  5. Use error handling paths
  
### **Symptoms**
  - Discover failure days later
  - Missing data nobody noticed
  - Customer complaints reveal broken automation

## Webhook Fragility

### **Id**
webhook-fragility
### **Summary**
Webhook automations break when source changes
### **Severity**
high
### **Tools Affected**
  - zapier
  - make
  - n8n
### **Situation**
Third-party changes webhook format
### **Why**
  Webhooks break when:
  - Sender updates their API
  - Field names change
  - Data types change
  - New required fields added
  - IP addresses change
  
  You don't control the source, so you can't prevent changes.
  
### **Solution**
  1. Use official integrations when possible
  2. Add validation on incoming data
  3. Handle missing fields gracefully
  4. Monitor webhook-triggered automations closely
  5. Have fallback data sources
  
### **Symptoms**
  - Automation suddenly errors
  - Fields missing in output
  - Wrong data processing

## Rate Limit Hell

### **Id**
rate-limit-hell
### **Summary**
API rate limits break automations at scale
### **Severity**
high
### **Tools Affected**
  - zapier
  - make
  - n8n
### **Situation**
Automation hits API limits during batch operations
### **Why**
  Most APIs have rate limits:
  - Salesforce: 100K/day
  - HubSpot: 100/10 seconds
  - Slack: varies by endpoint
  - Google: quotas everywhere
  
  Batch processing hits limits fast.
  
### **Solution**
  1. Know rate limits for every API you use
  2. Add delays between calls
  3. Batch during off-peak hours
  4. Use bulk APIs when available
  5. Implement retry with exponential backoff
  6. Consider upgrading API tier
  
### **Symptoms**
  - 429 Too Many Requests errors
  - Partial batch processing
  - Automation pauses unexpectedly

## Data Loss On Error

### **Id**
data-loss-on-error
### **Summary**
Failed automations can lose data
### **Severity**
critical
### **Tools Affected**
  - zapier
  - make
  - n8n
### **Situation**
Automation fails mid-process, data is lost
### **Why**
  When automation fails:
  - Data from webhook is lost
  - Partial updates create inconsistency
  - No automatic recovery
  - No transaction rollback
  
  Lost data = lost business.
  
### **Solution**
  1. Log incoming data before processing
  2. Use queues for critical data
  3. Implement idempotency
  4. Store raw data, process separately
  5. Regular backups of critical systems
  
### **Symptoms**
  - Missing records
  - Partially updated data
  - Can't recover failed items

## Duplicate Creation

### **Id**
duplicate-creation
### **Summary**
Automations create duplicates on retry
### **Severity**
high
### **Tools Affected**
  - zapier
  - make
  - n8n
### **Situation**
Retry logic creates duplicate records
### **Why**
  When automations retry:
  - Record was created but confirmation failed
  - Retry creates second record
  - No deduplication logic
  - Each retry = another duplicate
  
  Duplicates corrupt your data.
  
### **Solution**
  1. Check if record exists before creating
  2. Use unique identifiers
  3. Implement upsert logic
  4. Add deduplication step
  5. Regular duplicate cleanup process
  
### **Symptoms**
  - Duplicate contacts in CRM
  - Double charges
  - Duplicate messages sent

## Over Permissioned Connections

### **Id**
over-permissioned-connections
### **Summary**
Automation connections have too many permissions
### **Severity**
high
### **Tools Affected**
  - zapier
  - make
  - n8n
### **Situation**
OAuth connections request admin access
### **Why**
  When connecting apps:
  - Often requests full access
  - "Just in case" permissions
  - Hard to scope down later
  - Security risk if compromised
  
  Over-permissioned = over-exposed.
  
### **Solution**
  1. Use minimum necessary permissions
  2. Create dedicated automation accounts
  3. Review permissions regularly
  4. Remove unused connections
  5. Use API keys with limited scope when possible
  
### **Symptoms**
  - Automation account is admin
  - Connection can do more than needed
  - Security audit flags permissions

## Secret Exposure

### **Id**
secret-exposure
### **Summary**
Secrets exposed in automation logs
### **Severity**
high
### **Tools Affected**
  - zapier
  - make
  - n8n
### **Situation**
API keys, passwords visible in run history
### **Why**
  Automation platforms log everything:
  - Input data logged
  - Output data logged
  - Error messages include data
  - Shared team access
  
  Secrets in data = secrets exposed.
  
### **Solution**
  1. Never pass secrets as data
  2. Use built-in secret management
  3. Mask sensitive fields
  4. Limit run history access
  5. Audit logs for exposed secrets
  
### **Symptoms**
  - API keys visible in run history
  - Passwords in error messages

## Automation Sprawl

### **Id**
automation-sprawl
### **Summary**
Too many automations become unmanageable
### **Severity**
medium
### **Tools Affected**
  - zapier
  - make
  - n8n
### **Situation**
Hundreds of automations, nobody knows what's running
### **Why**
  Automation sprawl happens:
  - Easy to create, hard to maintain
  - People leave, automations stay
  - No documentation
  - Overlapping/conflicting automations
  - "Shadow IT" automations
  
  Unmaintained automations are liability.
  
### **Solution**
  1. Automation inventory and ownership
  2. Naming conventions
  3. Regular audit (quarterly)
  4. Document critical automations
  5. Centralize in team/folder structure
  6. Sunset unused automations
  
### **Symptoms**
  - Don't know what automations exist
  - Conflicting automations
  - Automations nobody owns

## Complex Dependency Chains

### **Id**
complex-dependency-chains
### **Summary**
Automations that trigger automations create chaos
### **Severity**
medium
### **Tools Affected**
  - zapier
  - make
  - n8n
### **Situation**
Automation A triggers B triggers C... debugging is impossible
### **Why**
  Chained automations are hard to:
  - Debug (which one failed?)
  - Monitor (no single view)
  - Reason about (side effects)
  - Test (complex dependencies)
  
  Complexity compounds exponentially.
  
### **Solution**
  1. Prefer single multi-step automations
  2. Document dependency chains
  3. Use queues for decoupling
  4. Add correlation IDs for tracing
  5. Limit chain depth (max 2-3)
  
### **Symptoms**
  - Error but can't find source
  - Unexpected cascading effects
  - Can't understand data flow

## Testing Nightmare

### **Id**
testing-nightmare
### **Summary**
Can't easily test automations before deploy
### **Severity**
medium
### **Tools Affected**
  - zapier
  - make
  - n8n
### **Situation**
Pushing automation live and hoping it works
### **Why**
  Testing challenges:
  - No staging environments
  - Can't simulate triggers easily
  - Test data affects production
  - No automated testing
  
  Deploy and pray is not a strategy.
  
### **Solution**
  1. Use test mode with sample data
  2. Create test versions of automations
  3. Use filter conditions for testing
  4. Separate test data/accounts
  5. n8n: use dev/prod environments
  
### **Symptoms**
  - Broke production with change
  - Can't test without affecting real data
  - Surprises after deploy