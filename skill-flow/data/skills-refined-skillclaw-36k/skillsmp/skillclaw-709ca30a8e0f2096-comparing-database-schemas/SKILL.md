---
name: comparing-database-schemas
description: Use this skill when you need to compare database schemas, generate migration scripts, or create rollback procedures for PostgreSQL or MySQL databases.
---

# Skill body

## Overview

This skill empowers you to perform production-grade database schema comparisons, generate safe migration scripts, and create rollback procedures. It simplifies the process of keeping database schemas synchronized across different environments, ensuring data integrity and minimizing downtime during deployments.

## How It Works

1. **Schema Comparison**: The plugin compares the schemas of two specified databases (PostgreSQL or MySQL), identifying differences in tables, columns, indexes, constraints, and triggers.
2. **Migration Script Generation**: Based on the schema differences, the plugin generates a safe migration script that can be used to update the target database schema. The script includes transaction safety to prevent data corruption.
3. **Rollback Procedure Generation**: The plugin generates a rollback procedure that can be used to revert the changes made by the migration script in case of errors.

## When to Use This Skill

This skill activates when you need to:
- Compare database schemas between different environments (e.g., development, staging, production).
- Generate migration scripts to update a database schema to the latest version.
- Create rollback procedures to revert database schema changes.
- Synchronize database schemas across multiple environments to ensure consistency.

## Examples

### Example 1: Generating a Migration Script

User request: "Generate a migration script to update the staging database schema to match production."

The skill will:
1. Connect to both the staging and production databases.
2. Compare the schemas of the two databases using the database-diff-tool plugin.
3. Generate a migration script that updates the staging database schema to match the production schema, including transaction safety.