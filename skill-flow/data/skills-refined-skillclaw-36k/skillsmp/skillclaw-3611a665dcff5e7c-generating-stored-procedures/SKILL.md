---
name: generating-stored-procedures
description: Use this skill when you need to create production-ready stored procedures, functions, triggers, or custom database logic for PostgreSQL, MySQL, or SQL Server.
---

# Skill body

## Overview

This skill empowers Claude to generate efficient, production-ready stored procedures, functions, and triggers for various database systems. It helps implement complex business logic, enforce data integrity, and optimize database performance directly within the database.

## How It Works

1. **Identify Requirements**: Analyze the user's request to understand the desired functionality, database system, and any specific constraints.
2. **Generate Code**: Use the stored-procedure-generator plugin to create the appropriate SQL code for the stored procedure, function, or trigger.
3. **Present Code**: Present the generated SQL code to the user for review and deployment.

## When to Use This Skill

This skill activates when you need to:
- Implement complex business rules within a database.
- Enforce data integrity constraints beyond simple foreign keys.
- Optimize database performance by minimizing network round trips.
- Implement atomic transactions for data consistency.

## Examples

### Example 1: Generating a Stored Procedure for Order Processing

User request: "generate stored procedure to process orders in PostgreSQL"

The skill will:
1. Analyze the request and determine the need for a PostgreSQL stored procedure for order processing.
2. Generate the SQL code for a stored procedure that handles order creation, validation, and updates.
3. Present the generated SQL code to the user.

### Example 2: Creating a Trigger for Auditing Data Changes

User request: "create a trigger in MySQL to audit changes to the 'products' table"

The skill will:
1. Analyze the request and determine the need for a MySQL trigger on the 'products' table.
2. Generate the SQL code for a trigger that logs changes (inserts, updates, deletes) to a separate audit table.
3. Present the generated SQL code to the user.

## Best Practices

- **Database Choice**: Specify the target database system clearly to ensure the generated code is compatible.