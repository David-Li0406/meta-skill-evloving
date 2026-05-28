# Zapier Make Patterns - Sharp Edges

## Using Text Instead of IDs in Dropdown Fields

### **Id**
dropdown-text-vs-id
### **Severity**
critical
### **Situation**
Configuring actions with dropdown selections
### **Symptom**
  "Bad Request" errors. "Invalid value" messages. Action fails
  despite correct-looking input. Works when you select from dropdown,
  fails with dynamic values.
  
### **Why**
  Dropdown menus display human-readable text but send IDs to APIs.
  When you type "Marketing Team" instead of selecting it, Zapier
  tries to send that text as the ID, which the API doesn't recognize.
  
### **Solution**
  # ALWAYS use dropdowns to select, don't type
  
  # If you need dynamic values:
  
  ## Zapier approach:
  1. Add a "Find" or "Search" action first
     - HubSpot: Find Contact → returns contact_id
     - Slack: Find User by Email → returns user_id
  
  2. Use the returned ID in subsequent actions
     - Dropdown: Use Custom Value
     - Select the ID from the search step
  
  ## Make approach:
  1. Add a Search module first
     - Search Contacts: filter by email
     - Returns: contact_id
  
  2. Map the ID to subsequent modules
     - Contact ID: {{2.id}} (from search module)
  
  # Common ID fields that trip people up:
  - User/Member IDs in Slack, Teams
  - Contact/Company IDs in CRMs
  - Project/Folder IDs in project tools
  - Category/Tag IDs in content systems
  
### **Detection Pattern**
  - dropdown
  - select
  - invalid value

## Zap Auto-Disabled at 95% Error Rate

### **Id**
auto-disable-95-error
### **Severity**
critical
### **Situation**
Running a Zap with frequent errors
### **Symptom**
  Zap suddenly stops running. Email notification about auto-disable.
  "This Zap was automatically turned off" message. Data stops syncing.
  
### **Why**
  Zapier automatically disables Zaps that have 95% or higher error
  rate over 7 days. This prevents runaway automation failures from
  consuming your task quota and creating data problems.
  
### **Solution**
  # Prevention:
  
  1. Add error handling steps:
     - Use Path: If error → [Log + Alert]
     - Add fallback actions for failures
  
  2. Use filters to prevent bad data:
     - Only continue if email exists
     - Only continue if amount > 0
     - Filter out test/invalid entries
  
  3. Monitor task history regularly:
     - Check for recurring errors
     - Fix issues before 95% threshold
  
  # Recovery:
  
  1. Check Task History for error patterns
  2. Fix the root cause (auth, bad data, API changes)
  3. Test with sample data
  4. Re-enable the Zap manually
  5. Monitor closely for next 24 hours
  
  # Common causes:
  - Expired authentication tokens
  - API rate limits
  - Changed field names in connected apps
  - Invalid data formats
  
### **Detection Pattern**
  - auto-disable
  - turned off
  - error rate

## Loops Consuming Unexpected Task Counts

### **Id**
task-consumption-loops
### **Severity**
high
### **Situation**
Processing arrays or multiple items
### **Symptom**
  Task quota depleted unexpectedly. One Zap run shows as 100+ tasks.
  Monthly limit reached in days. "You've used X of Y tasks" surprise.
  
### **Why**
  In Zapier, each iteration of a loop counts as separate tasks.
  If a webhook delivers an order with 50 line items and you loop
  through each, that's 50+ tasks for one order.
  
### **Solution**
  # Understand the math:
  
  Order with 10 items, 5 actions per item:
  = 1 trigger + (10 items × 5 actions) = 51 tasks
  
  # Strategies to reduce task usage:
  
  1. Batch operations when possible:
     - Use "Create Many Rows" instead of loop + create
     - Use bulk API endpoints
  
  2. Aggregate before sending:
     - Collect all items
     - Send one summary message, not one per item
  
  3. Filter before looping:
     - Only process items that need action
     - Skip unchanged/duplicate items
  
  4. Consider Make for high-volume:
     - Make uses operations, not tasks per action
     - More cost-effective for loops
  
  # Make approach:
  [Iterator] → [Actions] → [Aggregator]
  - Pay for operations (module executions)
  - Not per-action like Zapier
  
### **Detection Pattern**
  - loop
  - for each
  - line_items
  - iterator

## App Updates Breaking Existing Zaps

### **Id**
api-changes-break-zaps
### **Severity**
high
### **Situation**
App you're connected to releases updates
### **Symptom**
  Working Zap suddenly fails. "Field not found" errors. Different
  data format in outputs. Actions that worked yesterday fail today.
  
### **Why**
  When connected apps update their APIs, field names can change,
  new required fields appear, or data formats shift. Zapier/Make
  integrations may not immediately update to match.
  
### **Solution**
  # When a Zap breaks after app update:
  
  1. Check the Task History for specific errors
  2. Open the Zap editor to see field mapping issues
  3. Re-select the trigger/action to refresh schema
  4. Re-map any fields that show as "unknown"
  5. Test with new sample data
  
  # Prevention:
  
  1. Subscribe to changelog for critical apps
  2. Keep connection authorizations fresh
  3. Test Zaps after major app updates
  4. Document your field mappings
  5. Use test/duplicate Zaps for experiments
  
  # If integration is outdated:
  - Check Zapier/Make status pages
  - Report issue to support
  - Consider webhook alternative temporarily
  
  # Common offenders:
  - CRM field restructures
  - API version upgrades
  - OAuth scope changes
  - New required permissions
  
### **Detection Pattern**
  - field not found
  - unknown field
  - connection

## Authentication Tokens Expiring

### **Id**
auth-expiration
### **Severity**
high
### **Situation**
Using OAuth connections to apps
### **Symptom**
  "Authentication failed" errors. "Please reconnect" messages.
  Zaps fail after weeks of working. Multiple apps fail simultaneously.
  
### **Why**
  OAuth tokens expire. Some apps require re-authentication every
  60-90 days. If the user who connected the app leaves the company,
  their connection may stop working.
  
### **Solution**
  # Immediate fix:
  1. Go to Settings → Apps
  2. Find the app with issues
  3. Reconnect (re-authorize)
  4. Test affected Zaps
  
  # Prevention:
  
  1. Use service accounts for connections
     - Don't connect with personal accounts
     - Use shared team email/account
  
  2. Monitor connection health
     - Check Apps page regularly
     - Set calendar reminders for known expiration
  
  3. Document who connected what
     - Track in spreadsheet
     - Handoff process when people leave
  
  4. Prefer connections that don't expire
     - API keys over OAuth when available
     - Long-lived tokens
  
  # Zapier Enterprise:
  - Admin controls for managing connections
  - SSO integration
  - Centralized connection management
  
### **Detection Pattern**
  - authentication
  - reconnect
  - expired
  - unauthorized

## Webhooks Missing or Duplicating Events

### **Id**
webhook-reliability
### **Severity**
medium
### **Situation**
Using webhooks as triggers
### **Symptom**
  Some events never trigger the Zap. Same event triggers multiple
  times. Inconsistent automation behavior. "Works sometimes."
  
### **Why**
  Webhooks are fire-and-forget. If Zapier's receiving endpoint is
  slow or unavailable, the webhook may fail. Some systems retry
  webhooks, causing duplicates. Network issues lose events.
  
### **Solution**
  # Handle duplicates:
  
  1. Add deduplication logic:
     - Filter: Only continue if ID not in Airtable
     - First action: Check if already processed
  
  2. Use idempotency:
     - Store processed IDs
     - Skip if ID exists
  
  ## Zapier example:
  [Webhook Trigger]
     ↓
  [Airtable: Find Records] - search by event_id
     ↓
  [Filter: Only continue if not found]
     ↓
  [Process Event]
     ↓
  [Airtable: Create Record] - store event_id
  
  # Handle missed events:
  
  1. Use polling triggers for critical data
     - Less real-time but more reliable
     - Catches events during downtime
  
  2. Implement reconciliation:
     - Scheduled Zap to check for gaps
     - Compare source data to processed data
  
  3. Check source system retry settings:
     - Some systems retry on failure
     - Configure retry count/timing
  
### **Detection Pattern**
  - webhook
  - catch hook
  - duplicate
  - missing

## Make Operations Consumed by Error Retries

### **Id**
make-operation-limits
### **Severity**
medium
### **Situation**
Scenarios with failing modules
### **Symptom**
  Operations quota depleted quickly. Scenario runs "succeeded" but
  used many operations. Same scenario running more than expected.
  
### **Why**
  Make counts operations per module execution, including failed
  attempts and retries. Error handler modules consume operations.
  Scenarios that fail and retry can use 3-5x expected operations.
  
### **Solution**
  # Understand operation counting:
  
  Successful run: Each module = 1 operation
  Failed + retry (3x): 3 operations for that module
  Error handler: Additional operation per handler module
  
  # Reduce operation waste:
  
  1. Add error handlers that break early:
     [Module] → Error → [Break] (1 additional op)
     vs
     [Module] → Error → [Log] → [Alert] → [Update] (3+ ops)
  
  2. Use ignore instead of retry when appropriate:
     - If failure is expected (record exists)
     - If retrying won't help (bad data)
  
  3. Pre-validate before expensive operations:
     [Check Data] → Filter → [API Call]
     - Fail fast before consuming operations
  
  4. Optimize scenario scheduling:
     - Don't run every minute if hourly is enough
     - Use webhooks for real-time when possible
  
  # Monitor usage:
  - Check Operations dashboard
  - Set up usage alerts
  - Review high-consumption scenarios
  
### **Detection Pattern**
  - operation
  - quota
  - usage

## Timezone Mismatches in Scheduled Triggers

### **Id**
timezone-confusion
### **Severity**
medium
### **Situation**
Setting up scheduled automations
### **Symptom**
  Zap runs at wrong time. "9 AM" trigger fires at 2 PM. Different
  behavior on different days. DST causes hour shifts.
  
### **Why**
  Zapier shows times in your local timezone but may store in UTC.
  If you change timezones or DST occurs, scheduled times shift.
  Team members in different zones see different times.
  
### **Solution**
  # Best practices:
  
  1. Explicitly set timezone in schedule:
     - Don't rely on browser detection
     - Use business timezone, not personal
  
  2. Document in Zap name:
     - "Daily Report 9AM EST"
     - Include timezone in description
  
  3. Test around DST transitions:
     - Schedule changes at DST boundaries
     - Verify times before/after change
  
  4. For global teams:
     - Use UTC as standard
     - Convert to local in descriptions
  
  5. Consider buffer times:
     - Don't schedule at exactly midnight
     - Avoid on-the-hour (busy periods)
  
  ## Make timezone handling:
  - Scenarios use account timezone setting
  - formatDate() function respects timezone
  - Use parseDate() with explicit timezone
  
### **Detection Pattern**
  - schedule
  - timezone
  - time
  - daily