---
name: analyze-and-optimize-database-queries
description: Use this skill when you need to analyze and optimize database query performance, identify bottlenecks, and receive recommendations for improvements.
---

## Overview

This skill empowers Claude to act as a database performance expert. By analyzing EXPLAIN plans and SQL queries, Claude can pinpoint inefficiencies and recommend targeted improvements to enhance database performance.

## How It Works

1. **Receive Input**: The user provides an EXPLAIN plan, a slow query, or a description of a performance problem.
2. **Analyze Performance**: The skill analyzes the provided information, identifying potential bottlenecks, such as full table scans, missing indexes, or inefficient join operations.
3. **Provide Recommendations**: The skill generates specific optimization recommendations, including suggesting new indexes, rewriting queries, or adjusting database configuration parameters.

## When to Use This Skill

This skill activates when you need to:
- Analyze the EXPLAIN plan of a slow-running query.
- Identify performance bottlenecks in a database query.
- Optimize a slow-running SQL query.
- Obtain recommendations for improving database query performance and efficiency.

## Examples

### Example 1: Analyzing a Slow Query

User request: "Here's the EXPLAIN plan for my slow query. Can you help me optimize it? ```EXPLAIN SELECT * FROM orders WHERE customer_id = 123 AND order_date > '2023-01-01';```"

The skill will:
1. Analyze the provided EXPLAIN plan.
2. Identify potential issues, such as a missing index on `customer_id` or `order_date`, and suggest creating appropriate indexes.

### Example 2: Identifying a Bottleneck

User request: "My query is taking a long time. It's a simple SELECT statement, but it's still slow. What could be the problem?"

The skill will:
1. Prompt the user to provide the EXPLAIN plan for the query.
2. Analyze the EXPLAIN plan and identify potential bottlenecks, such as a full table scan or an inefficient join. It might suggest creating an index or rewriting the query to use a more efficient join algorithm.

### Example 3: Finding Indexing Opportunities

User request: "I need help optimizing a query that filters on product_category and price. Can you suggest any indexes?"

The skill will:
1. Analyze a hypothetical query based on the user's description.
2. Recommend a composite index on (product_category, price) to speed up filtering.

## Best Practices

- **Provide Complete Information**: Include the full EXPLAIN plan and the query itself for the most accurate analysis.
- **Describe the Problem**: Clearly articulate the performance issue you're experiencing (e.g., slow query, high CPU usage).
- **Test Recommendations**: After implementing the suggested optimizations, re-run the EXPLAIN plan to verify the improvements.

## Integration

This skill integrates well with other database tools and plugins within the Claude Code ecosystem. For example, it can be used in conjunction with a database schema explorer to identify potential indexing opportunities or with a query builder to rewrite inefficient queries.