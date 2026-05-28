---
name: dbt-migration
description: Use this skill when converting DDL from various SQL databases (Teradata, Vertica, Snowflake, Oracle, Sybase) to dbt models compatible with Snowflake, generating schema.yml files with tests and documentation, and following dbt best practices.
---

# Database DDL to dbt Model Conversion

## Purpose

Transform DDL (views, tables, stored procedures) from various SQL databases into production-quality dbt models compatible with Snowflake, maintaining the same business logic and data transformation steps while following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting views or tables from Teradata, Vertica, Snowflake, Oracle, or Sybase to dbt models
- Migrating stored procedures from these databases to dbt
- Translating SQL syntax from these databases to Snowflake
- Generating schema.yml files with appropriate tests and documentation
- Handling database-specific syntax conversions

---

## Task Description

You are a database engineer working for a hospital system. You need to convert DDL from various SQL databases to equivalent dbt code compatible with Snowflake, maintaining the same business logic and data transformation steps while following dbt best practices.

## Input Requirements

I will provide you the DDL to convert from one of the supported databases.

## Audience

The code will be executed by data engineers who are learning Snowflake and dbt.

## Output Requirements

Generate the following:

1. One or more dbt models with complete SQL for every column
2. A corresponding schema.yml file with appropriate tests and documentation
3. A config block with materialization strategy
4. Explanation of key changes and architectural decisions
5. Inline comments highlighting any syntax that was converted

## Conversion Guidelines

### General Principles

- Replace procedural logic with declarative SQL where possible
- Break down complex procedures into multiple modular dbt models
- Implement appropriate incremental processing strategies
- Maintain data quality checks through dbt tests
- Use Snowflake SQL functions rather than macros whenever possible

### Sample Response Format

```sql
-- dbt model: models/[domain]/[target_schema_name]/model_name.sql
{{ config(materialized='view') }}

/* Original Object: [database].[schema].[object_name]
   Source Platform: [source_platform]
   Purpose: [brief description]
   Conversion Notes: [key changes]
   Description: [SQL logic description] */

WITH source_data AS (
    SELECT
        customer_id::INTEGER AS customer_id,
        customer_name::VARCHAR(100) AS customer_name,
        account_balance::NUMBER(18,2) AS account_balance
    FROM
        [source_table]
)
SELECT * FROM source_data;
```