---
name: sql
description: This skill should be used when the user asks to "write SQL", "optimize a query", "explain this SQL", or needs help with database queries and SQL best practices.
---

# /sql

Help write, optimize, or explain SQL queries.

## Instructions

When the user provides a SQL query or describes what they need:

1. **Writing SQL**: Generate clean, readable SQL with:
   - Proper indentation and capitalization
   - CTEs over nested subqueries when complex
   - Comments for non-obvious logic

2. **Optimizing SQL**: Look for:
   - Missing indexes (suggest based on WHERE/JOIN columns)
   - N+1 patterns
   - Unnecessary SELECT \*
   - Subqueries that could be JOINs
   - Opportunities for window functions

3. **Explaining SQL**: Break down the query step by step, explaining what each part does

Ask for the database type (PostgreSQL, MySQL, BigQuery, etc.) if not specified.
