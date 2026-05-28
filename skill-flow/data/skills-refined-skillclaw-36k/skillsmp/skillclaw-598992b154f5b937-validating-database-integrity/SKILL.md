---
name: validating-database-integrity
description: Use this skill when you need to implement data validation, enforce constraints, or improve data quality within a database.
---

# Skill body

## Overview

This skill utilizes the data-validation-engine plugin to ensure database integrity by automatically validating data types, ranges, formats, referential integrity, and business rules. It empowers users to implement comprehensive data validation at both the database and application levels.

## How It Works

1. **Rule Definition**: Analyze the request to identify specific data validation requirements (e.g., data types, ranges, formats).
2. **Validation Implementation**: Use the data-validation-engine plugin to generate and apply the necessary validation rules to the database schema or application logic.
3. **Verification**: Confirm the successful implementation of the validation rules and report any errors or conflicts.

## When to Use This Skill

This skill activates when you need to:
- Implement data validation for a new database schema.
- Enforce data integrity constraints on existing database tables.
- Validate data input within an application to prevent invalid data from being stored.

## Examples

### Example 1: Implementing Data Type Validation

User request: "Implement data validation to ensure the 'age' column in the 'users' table is an integer."

The skill will:
1. Use the data-validation-engine plugin to add a constraint to the 'users' table, enforcing that the 'age' column must contain integer values.
2. Verify that the constraint is active and prevents non-integer values from being inserted into the 'age' column.

### Example 2: Validating Email Format

User request: "Add data validation to ensure the 'email' column in the 'customers' table contains a valid email address format."

The skill will:
1. Use the data-validation-engine plugin to add a constraint to the 'customers' table, using a regular expression to validate the format of the 'email' column.
2. Test the constraint with valid and invalid email addresses to ensure it functions correctly.

## Best Practices
- Regularly review and update validation rules to adapt to changing data requirements.
- Test validation rules thoroughly to ensure they work as intended before deployment.