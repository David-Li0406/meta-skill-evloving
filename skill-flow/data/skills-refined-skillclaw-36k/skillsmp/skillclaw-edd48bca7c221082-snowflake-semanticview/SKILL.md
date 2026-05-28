---
name: snowflake-semanticview
description: Use this skill when you need to create, alter, and validate Snowflake semantic views using the Snowflake CLI (snow). It guides you through building or troubleshooting semantic views and validating DDL against Snowflake.
---

# Snowflake Semantic Views

## One-Time Setup

- Verify Snowflake CLI installation by opening a new terminal and running `snow --help`.
- If Snowflake CLI is missing or the user cannot install it, direct them to [Snowflake CLI Installation](https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation).
- Configure a Snowflake connection with `snow connection add` as per [Configure Connections](https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections#add-a-connection).
- Use the configured connection for all validation and execution steps.

## Workflow For Each Semantic View Request

1. Confirm the target database, schema, role, warehouse, and final semantic view name.
2. Ensure the model follows a star schema (facts with conformed dimensions).
3. Draft the semantic view DDL using the official syntax from [Create Semantic View](https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view).
4. Populate synonyms and comments for each dimension, fact, and metric:
   - Read Snowflake table/view/column comments first (preferred source):
     - [Comment Syntax](https://docs.snowflake.com/en/sql-reference/sql/comment).
   - If comments or synonyms are missing, ask whether you can create them, whether the user wants to provide text, or whether you should draft suggestions for approval.
5. Use SELECT statements with DISTINCT and LIMIT (maximum 1000 rows) to discover relationships between fact and dimension tables, identify column data types, and create more meaningful comments and synonyms for columns.
6. Create a temporary validation name (e.g., append `__tmp_validate`) while keeping the same database and schema.
7. Always validate by sending the DDL to Snowflake via Snowflake CLI before finalizing:
   - Use `snow sql` to execute the statement with the configured connection.
   - If flags differ by version, check `snow sql --help` and use the connection option shown there.
8. If validation fails, iterate on the DDL and re-run the validation step until it succeeds.
9. Apply the final DDL (create or alter) using the real semantic view name.
10. Run a sample query against the final semantic view to confirm it works as expected.
11. Clean up any temporary semantic view created during validation.

## Synonyms And Comments (Required)

- Use the semantic view syntax for synonyms and comments:

```
WITH SYNONYMS [ = ] ( 'synonym' [ , ... ] )
COMMENT = 'comment_about_dim_fact_or_metric'
```

- Treat synonyms as informational only; do not use them as identifiers.