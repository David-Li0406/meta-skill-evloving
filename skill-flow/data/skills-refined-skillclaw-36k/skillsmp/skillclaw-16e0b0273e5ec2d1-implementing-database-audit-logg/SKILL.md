---
name: implementing-database-audit-logging
description: Use this skill when you need to implement database audit logging to track changes and ensure compliance with regulations.
---

# Skill body

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
   - Pros: Automatic, no application changes, captures all changes.
   - Cons: Performance overhead, complex trigger maintenance.
2. **Application-Level Auditing**: Best for selective auditing.
   - Pros: Flexible, lower database overhead, easier debugging.
   - Cons: Requires application changes, can miss direct database changes.
3. **Change Data Capture (CDC)**: Best for real-time streaming.
   - Pros: Minimal performance impact, real-time analysis, external processing.
   - Cons: Complex setup, requires CDC infrastructure.
4. **Native Database Logs**: Best for general monitoring.
   - Pros: No setup, captures everything, built-in.
   - Cons: High volume, limited retention, difficult to query.

### Step 3: Design Audit Table Schema
1. Create an audit log table with these core columns:
   - `audit_id` (primary key), `table_name`, `action` (INSERT/UPDATE/DELETE)
   - `record_id` (reference to audited record), `old_values` (JSON), `new_values` (JSON).

## Best Practices

- **Strategy Selection**: Choose the audit logging strategy that best suits your application's needs and performance requirements. Trigger-based auditing can impact performance, while CDC might require more complex infrastructure.
- **Data Sensitivity**: Consider the sensitivity of the data being audited and ensure compliance with relevant regulations (e.g., GDPR, HIPAA).