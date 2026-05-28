# Zapier & Make Patterns

## Patterns


---
  #### **Name**
Basic Trigger-Action Pattern
  #### **Description**
Single trigger leads to one or more actions
  #### **When**
Simple notifications, data sync, basic workflows
  #### **Example**
    # BASIC TRIGGER-ACTION:
    
    """
    [Trigger] → [Action]
      e.g., New Email → Create Task
    """
    
    ## Zapier Example
    """
    Zap Name: "Gmail New Email → Todoist Task"
    
    TRIGGER: Gmail - New Email
      - From: specific-sender@example.com
      - Has attachment: yes
    
    ACTION: Todoist - Create Task
      - Project: Inbox
      - Content: {{Email Subject}}
      - Description: From: {{Email From}}
      - Due date: Tomorrow
    """
    
    ## Make Example
    """
    Scenario: "Gmail to Todoist"
    
    [Gmail: Watch Emails] → [Todoist: Create a Task]
    
    Gmail Module:
      - Folder: INBOX
      - From: specific-sender@example.com
    
    Todoist Module:
      - Project ID: (select from dropdown)
      - Content: {{1.subject}}
      - Due String: tomorrow
    """
    
    ## Best Practices:
    - Use descriptive Zap/Scenario names
    - Test with real sample data
    - Use filters to prevent unwanted runs
    

---
  #### **Name**
Multi-Step Sequential Pattern
  #### **Description**
Chain of actions executed in order
  #### **When**
Multi-app workflows, data enrichment pipelines
  #### **Example**
    # MULTI-STEP SEQUENTIAL:
    
    """
    [Trigger] → [Action 1] → [Action 2] → [Action 3]
    Each step's output available to subsequent steps
    """
    
    ## Zapier Multi-Step Zap
    """
    Zap: "New Lead → CRM → Slack → Email"
    
    1. TRIGGER: Typeform - New Entry
       - Form: Lead Capture Form
    
    2. ACTION: HubSpot - Create Contact
       - Email: {{Typeform Email}}
       - First Name: {{Typeform First Name}}
       - Lead Source: "Website Form"
    
    3. ACTION: Slack - Send Channel Message
       - Channel: #sales-leads
       - Message: "New lead: {{Typeform Name}} from {{Typeform Company}}"
    
    4. ACTION: Gmail - Send Email
       - To: {{Typeform Email}}
       - Subject: "Thanks for reaching out!"
       - Body: (template with personalization)
    """
    
    ## Make Scenario
    """
    [Typeform] → [HubSpot] → [Slack] → [Gmail]
    
    - Each module passes data to the next
    - Use {{N.field}} to reference module N's output
    - Add error handlers between critical steps
    """
    

---
  #### **Name**
Conditional Branching Pattern
  #### **Description**
Different actions based on conditions
  #### **When**
Different handling for different data types
  #### **Example**
    # CONDITIONAL BRANCHING:
    
    """
                  ┌→ [Action A] (condition met)
    [Trigger] ───┤
                  └→ [Action B] (condition not met)
    """
    
    ## Zapier Paths (Pro+ required)
    """
    Zap: "Route Support Tickets"
    
    1. TRIGGER: Zendesk - New Ticket
    
    2. PATH A: If priority = "urgent"
       - Slack: Post to #urgent-support
       - PagerDuty: Create incident
    
    3. PATH B: If priority = "normal"
       - Slack: Post to #support
       - Asana: Create task
    
    4. PATH C: Otherwise (catch-all)
       - Slack: Post to #support-overflow
    """
    
    ## Make Router
    """
    [Zendesk: Watch Tickets]
          ↓
    [Router]
       ├── Route 1: priority = urgent
       │     └→ [Slack] → [PagerDuty]
       │
       ├── Route 2: priority = normal
       │     └→ [Slack] → [Asana]
       │
       └── Fallback route
             └→ [Slack: overflow]
    
    # Make's visual router makes complex branching clear
    """
    
    ## Best Practices:
    - Always have a fallback/else path
    - Test each path independently
    - Document which conditions trigger which path
    

---
  #### **Name**
Data Transformation Pattern
  #### **Description**
Clean, format, and transform data between apps
  #### **When**
Apps expect different data formats
  #### **Example**
    # DATA TRANSFORMATION:
    
    ## Zapier Formatter
    """
    Common transformations:
    
    1. Text manipulation:
       - Split text: "John Doe" → First: "John", Last: "Doe"
       - Capitalize: "john" → "John"
       - Replace: Remove special characters
    
    2. Date formatting:
       - Convert: "2024-01-15" → "January 15, 2024"
       - Adjust: Add 7 days to date
    
    3. Numbers:
       - Format currency: 1000 → "$1,000.00"
       - Spreadsheet formula: =SUM(A1:A10)
    
    4. Lookup tables:
       - Map status codes: "1" → "Active", "2" → "Pending"
    """
    
    ## Make Data Functions
    """
    Make has powerful built-in functions:
    
    Text:
      {{lower(1.email)}}           # Lowercase
      {{substring(1.name; 0; 10)}} # First 10 chars
      {{replace(1.text; "-"; "")}} # Remove dashes
    
    Arrays:
      {{first(1.items)}}           # First item
      {{length(1.items)}}          # Count items
      {{map(1.items; "id")}}       # Extract field
    
    Dates:
      {{formatDate(1.date; "YYYY-MM-DD")}}
      {{addDays(now; 7)}}
    
    Math:
      {{round(1.price * 0.8; 2)}}  # 20% discount, 2 decimals
    """
    
    ## Best Practices:
    - Transform early in the workflow
    - Use filters to skip invalid data
    - Log transformations for debugging
    

---
  #### **Name**
Error Handling Pattern
  #### **Description**
Graceful handling of failures
  #### **When**
Any production automation
  #### **Example**
    # ERROR HANDLING:
    
    ## Zapier Error Handling
    """
    1. Built-in retry (automatic):
       - Zapier retries failed actions automatically
       - Exponential backoff for temporary failures
    
    2. Error handling step:
       Zap:
         1. [Trigger]
         2. [Action that might fail]
         3. [Error Handler]
            - If error → [Slack: Alert team]
            - If error → [Email: Send report]
    
    3. Path-based handling:
       [Action] → Path A: Success → [Continue]
                → Path B: Error → [Alert + Log]
    """
    
    ## Make Error Handlers
    """
    Make has visual error handling:
    
    [Module] ──┬── Success → [Next Module]
               │
               └── Error → [Error Handler]
    
    Error handler types:
    1. Break: Stop scenario, send notification
    2. Rollback: Undo completed operations
    3. Commit: Save partial results, continue
    4. Ignore: Skip error, continue with next item
    
    Example:
    [API Call] → Error Handler (Ignore)
               → [Log to Airtable: "Failed: {{error.message}}"]
               → Continue scenario
    """
    
    ## Best Practices:
    - Always add error handlers for external APIs
    - Log errors to a spreadsheet/database
    - Set up Slack/email alerts for critical failures
    - Test failure scenarios, not just success
    

---
  #### **Name**
Batch Processing Pattern
  #### **Description**
Process multiple items efficiently
  #### **When**
Importing data, bulk operations
  #### **Example**
    # BATCH PROCESSING:
    
    ## Zapier Looping
    """
    Zap: "Process Order Items"
    
    1. TRIGGER: Shopify - New Order
       - Returns: order with line_items array
    
    2. LOOPING: For each item in line_items
       - Create inventory adjustment
       - Update product count
       - Log to spreadsheet
    
    Note: Each loop iteration counts as tasks!
    10 items = 10 tasks consumed
    """
    
    ## Make Iterator
    """
    [Webhook: Receive Order]
          ↓
    [Iterator: line_items]
          ↓ (processes each item)
    [Inventory: Adjust Stock]
          ↓
    [Aggregator: Collect Results]
          ↓
    [Slack: Summary Message]
    
    Iterator creates one bundle per item.
    Aggregator combines results back together.
    Use Array Aggregator for collecting processed items.
    """
    
    ## Best Practices:
    - Use aggregators to combine results
    - Consider batch limits (some APIs limit to 100)
    - Watch operation/task counts for cost
    - Add delays for rate-limited APIs
    

---
  #### **Name**
Scheduled Automation Pattern
  #### **Description**
Time-based triggers instead of events
  #### **When**
Daily reports, periodic syncs, batch jobs
  #### **Example**
    # SCHEDULED AUTOMATION:
    
    ## Zapier Schedule Trigger
    """
    Zap: "Daily Sales Report"
    
    TRIGGER: Schedule by Zapier
      - Every: Day
      - Time: 8:00 AM
      - Timezone: America/New_York
    
    ACTIONS:
      1. Google Sheets: Get rows (yesterday's sales)
      2. Formatter: Calculate totals
      3. Gmail: Send report to team
    """
    
    ## Make Scheduled Scenarios
    """
    Scenario Schedule Options:
      - Run once (manual)
      - At regular intervals (every X minutes)
      - Advanced: Cron expression (0 8 * * *)
    
    [Scheduled Trigger: Every day at 8 AM]
          ↓
    [Google Sheets: Search Rows]
          ↓
    [Iterator: Process each row]
          ↓
    [Aggregator: Sum totals]
          ↓
    [Gmail: Send Report]
    """
    
    ## Best Practices:
    - Consider timezone differences
    - Add buffer time for long-running jobs
    - Log execution times for monitoring
    - Don't schedule at exactly midnight (busy period)
    

## Anti-Patterns


---
  #### **Name**
Text in Dropdown Fields
  #### **Description**
Entering text when IDs are expected
  #### **Why**
    Dropdown menus in Zapier/Make expect IDs, not display text.
    "Marketing Team" fails but "team_12345" works. This is the
    most common cause of Zap failures.
    
  #### **Instead**
    Always use the dropdown to select options. If you must use
    dynamic values, first look up the ID with a search action.
    

---
  #### **Name**
No Error Handling
  #### **Description**
Assuming actions always succeed
  #### **Why**
    APIs fail. Rate limits hit. Auth expires. Without error handling,
    failures cascade or go unnoticed. 95% error rate auto-disables Zaps.
    
  #### **Instead**
    Add error handlers for external APIs. Log failures. Alert on
    critical errors. Test failure scenarios.
    

---
  #### **Name**
Hardcoded Values
  #### **Description**
Magic numbers and strings throughout
  #### **Why**
    When IDs change, email addresses update, or values need adjustment,
    you have to find and update every occurrence.
    
  #### **Instead**
    Use lookup tables for mappings. Store configuration in a
    spreadsheet that's read at runtime. Document all values.
    

---
  #### **Name**
No Testing
  #### **Description**
Going live without testing
  #### **Why**
    Production data is unpredictable. Edge cases exist. That field
    that's "always filled" is sometimes empty. Testing prevents
    embarrassing automation failures.
    
  #### **Instead**
    Test with real sample data. Test each path/branch. Test error
    scenarios. Use test/staging accounts when available.
    

---
  #### **Name**
Ignoring Rate Limits
  #### **Description**
Sending unlimited requests to APIs
  #### **Why**
    Many APIs have rate limits (100 requests/minute, etc.). Hitting
    limits causes failures, temporary bans, or degraded service.
    
  #### **Instead**
    Add delays between actions. Use batch operations when available.
    Check API documentation for limits. Build retry logic.
    

---
  #### **Name**
Monolithic Mega-Zaps
  #### **Description**
One automation that does everything
  #### **Why**
    Hard to debug, hard to modify, hard to understand. When it
    fails, the entire workflow stops. Changes risk breaking
    unrelated functionality.
    
  #### **Instead**
    Break into focused automations. Use webhooks to chain Zaps.
    One automation per logical workflow.
    