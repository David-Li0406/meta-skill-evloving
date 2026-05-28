---
name: implementing-database-audit-logging
description: Use this skill when you need to track database changes for compliance and security monitoring by implementing audit logging.
---

## Overview

This skill automates the process of setting up database audit logging. It helps users choose an appropriate auditing strategy and provides a basic audit table schema, simplifying the implementation of robust audit trails for compliance and debugging purposes.

## How It Works

1. **Identify Request**: Detects user intent to implement database audit logging.
2. **Present Audit Strategies**: Offers a selection of auditing strategies: Trigger-Based, Application-Level, Change Data Capture (CDC), and Database Logs.
3. **Generate Audit Table Schema**: Provides a basic SQL schema for an audit log table.

## When to Use This Skill

This skill activates when you need to:
- Implement database audit logging for compliance requirements.
- Track changes to specific database tables.
- Debug data inconsistencies by reviewing historical changes.
- Securely monitor database activity.

## Instructions

### Step 1: Define Audit Requirements
1. Identify tables requiring audit logging based on compliance needs.
2. Determine events to audit (INSERT, UPDATE, DELETE, SELECT for sensitive data).
3. Define which columns contain sensitive data requiring audit.
4. Document retention requirements for audit logs.
5. Identify users/roles whose actions need auditing.

### Step 2: Choose Audit Strategy
1. **Trigger-Based Auditing**: Best for comprehensive row-level tracking.
   - Pros: Automatic, captures all changes.
   - Cons: Performance overhead, complex maintenance.
2. **Application-Level Auditing**: Best for selective auditing.
   - Pros: Flexible, lower overhead.
   - Cons: Requires application changes.
3. **Change Data Capture (CDC)**: Best for real-time streaming.
   - Pros: Minimal performance impact, real-time analysis.
   - Cons: Complex setup.
4. **Native Database Logs**: Best for general monitoring.
   - Pros: No setup, captures everything.
   - Cons: High volume, difficult to query.

### Step 3: Design Audit Table Schema
1. Create an audit log table with core columns:
   - `audit_id` (primary key), `table_name`, `action` (INSERT/UPDATE/DELETE)
   - `record_id` (reference to audited record), `old_values` (JSON), `new_values` (JSON)
   - `changed_by` (user), `changed_at` (timestamp), `client_ip`, `application_context`
2. Add indexes on `table_name`, `changed_at`, `changed_by` for query performance.
3. Partition the audit table by date for efficient archival.

### Step 4: Implement Audit Mechanism
1. For trigger-based: Create AFTER INSERT/UPDATE/DELETE triggers on each table.
2. Capture old and new row values as JSON in the trigger body.
3. Record user context (CURRENT_USER, application user, IP address).
4. Handle trigger failures gracefully.

### Step 5: Configure Audit Log Management
1. Set up automated archival of old audit logs.
2. Implement audit log analysis queries for compliance reports.
3. Create alerts for suspicious activities.
4. Document audit log query procedures for compliance auditors.

### Step 6: Validate Audit Implementation
1. Perform test operations on audited tables.
2. Verify audit log entries are created with complete data.
3. Test audit log queries for performance.
4. Confirm audit logs cannot be modified by regular users.

## Best Practices

- **Strategy Selection**: Choose the audit logging strategy that best suits your application's needs and performance requirements.
- **Data Sensitivity**: Consider the sensitivity of the data being audited and implement appropriate security measures.
- **Retention Policy**: Define a clear retention policy for audit logs to manage storage and comply with regulatory requirements.

## Integration

This skill can be used in conjunction with other database management plugins to automate the creation of triggers or configure CDC pipelines. It also integrates with logging and monitoring tools to provide a centralized view of database activity.