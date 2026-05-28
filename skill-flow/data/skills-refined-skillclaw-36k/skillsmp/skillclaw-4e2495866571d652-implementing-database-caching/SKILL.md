---
name: implementing-database-caching
description: Use this skill when you need to implement multi-tier database caching solutions to improve performance, reduce database load, or enhance scalability.
---

# Skill body

## Overview

This skill empowers Claude to implement a production-ready multi-tier caching architecture for databases. It leverages Redis for distributed caching, in-memory caching for L1 performance, and CDN for static assets, resulting in significant database load reduction, improved query latency, and enhanced scalability.

## How It Works

1. **Identify Caching Requirements**: Analyze the user's request to determine specific caching needs and database technologies in use.
2. **Implement Caching Layers**: Generate code to implement Redis caching, in-memory caching, and CDN integration based on identified requirements.
3. **Configure Caching Strategies**: Set up appropriate caching strategies such as cache-aside, write-through, or read-through to optimize performance and data consistency.

## When to Use This Skill

This skill activates when you need to:
- Implement a caching layer for a database.
- Improve database query performance.
- Reduce database load.

## Examples

### Example 1: Implementing Redis Caching

User request: "Implement Redis caching for my PostgreSQL database to improve query performance."

The skill will:
1. Generate code to integrate Redis as a caching layer for the PostgreSQL database.
2. Configure cache-aside strategy for frequently accessed data.

### Example 2: Adding In-Memory Caching

User request: "Add an in-memory cache layer to my application to reduce latency for frequently accessed data."

The skill will:
1. Implement an in-memory cache using a suitable library (e.g., `lru-cache` or similar).
2. Configure the application to check the in-memory cache before querying the database.

## Best Practices

- **Cache Invalidation**: Implement proper cache invalidation strategies to ensure data consistency.
- **Cache Key Design**: Design effective cache keys to avoid collisions and ensure efficient cache retrieval.