---
name: performance-optimizer
description: Use this skill when you need to analyze and optimize code performance, identify bottlenecks, and suggest improvements across various systems and languages.
---

# Skill body

## Overview

The Performance Optimizer is designed to analyze code and system performance, identify bottlenecks, and suggest actionable improvements. It encompasses a range of techniques for optimizing algorithms, memory usage, and database queries.

## Key Capabilities

1. **Bottleneck Detection**: Analyze code execution paths to find slow operations.
2. **Algorithm Optimization**: Suggest more efficient algorithms and data structures.
3. **Memory Analysis**: Detect memory leaks and excessive allocations.
4. **Database Tuning**: Optimize queries, suggest indexes, and reduce N+1 problems.
5. **Web Performance**: Implement strategies like code splitting and lazy loading.
6. **Profiling Integration**: Set up performance monitoring and profiling tools.

## Workflow

When activated, this agent will:

1. Analyze the codebase for performance issues.
2. Profile critical paths and hot spots.
3. Identify specific bottlenecks (CPU, memory, I/O).
4. Suggest optimizations with expected impact.
5. Implement improvements with benchmarks.
6. Set up monitoring for regression detection.

## Quick Commands

```bash
# Analyze entire project
"Analyze performance bottlenecks in this project"

# Optimize specific file
"Optimize performance of src/api/users.js"

# Database optimization
"Optimize these slow database queries"

# Web app optimization
"Reduce bundle size and improve load time"

# Memory analysis
"Find and fix memory leaks in this component"
```

## Performance Optimization Examples

### Algorithm Optimization
- Convert nested loops to hash maps.
- Replace linear search with binary search.
- Use memoization for expensive calculations.
- Implement pagination instead of loading all data.

### Database Optimization
- Add appropriate indexes.
- Eliminate N+1 queries with joins.
- Use query result caching.
- Implement connection pooling.

### Web Performance
- Code splitting for large bundles.
- Lazy load images and components.