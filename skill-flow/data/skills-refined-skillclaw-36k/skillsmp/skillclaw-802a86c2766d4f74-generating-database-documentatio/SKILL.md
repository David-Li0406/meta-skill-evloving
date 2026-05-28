---
name: generating-database-documentation
description: Use this skill when you need to automatically generate comprehensive documentation for existing database schemas, including ERD diagrams and data dictionaries, to support team onboarding, architectural reviews, or data governance.
---

# Skill body

## Overview

This skill empowers Claude to create detailed database documentation from existing database schemas. It leverages the database-documentation-gen plugin to automate the process, saving time and ensuring consistency. The generated documentation includes ERD diagrams, table relationships, and detailed information about database objects.

## How It Works

1. **Activation**: Claude recognizes the user's request for database documentation, ERD diagrams, or a data dictionary, triggering the database-documentation-gen plugin.
2. **Schema Analysis**: The plugin connects to the specified database and analyzes its schema, extracting information about tables, columns, relationships, indexes, triggers, and stored procedures.
3. **Documentation Generation**: The plugin generates comprehensive documentation in various formats, including ERD diagrams, data dictionaries, and interactive HTML documentation.

## When to Use This Skill

This skill activates when you need to:
- Generate documentation for a new or existing database.
- Create ERD diagrams for architectural reviews.
- Produce a data dictionary for data governance purposes.
- Onboard new team members to a database project.

## Examples

### Example 1: Documenting an Existing Database

User request: "Generate database documentation for the 'users' database."

The skill will:
1. Activate the database-documentation-gen plugin.
2. Connect to the 'users' database and analyze its schema.
3. Generate comprehensive documentation, including ERD diagrams and a data dictionary.

### Example 2: Creating an ERD Diagram

User request: "Create an ERD diagram for the 'orders' database."

The skill will:
1. Activate the database-documentation-gen plugin.
2. Connect to the 'orders' database and analyze its schema.
3. Generate the ERD diagram and related documentation.