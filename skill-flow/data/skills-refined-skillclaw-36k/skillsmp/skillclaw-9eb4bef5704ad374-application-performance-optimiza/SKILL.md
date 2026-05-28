---
name: application-performance-optimization
description: Use this skill when you need to analyze and optimize application performance by identifying bottlenecks in CPU, memory, I/O, and execution time.
---

# Skill body

## Overview

This skill empowers Claude to analyze application performance, pinpoint bottlenecks, and recommend optimizations. It examines CPU usage, memory consumption, I/O operations, and execution time to enhance resource utilization and improve overall application speed and responsiveness.

## How It Works

1. **Architecture Analysis**: Claude analyzes the application's architecture and data flow to understand potential bottlenecks.
2. **Bottleneck Identification**: The skill identifies bottlenecks across CPU, memory, I/O, database, lock contention, and resource exhaustion.
3. **Performance Metrics Analysis**: It examines CPU usage, memory allocation, and execution time to detect performance issues.
4. **Remediation Suggestions**: Claude provides remediation strategies with code examples to resolve the identified bottlenecks.

## When to Use This Skill

This skill activates when you need to:
- Diagnose slow application performance.
- Analyze application performance for bottlenecks.
- Optimize resource usage (CPU, memory, I/O, database).
- Identify CPU-intensive operations and memory leaks.
- Proactively prevent performance issues.

## Examples

### Example 1: Diagnosing Slow Database Queries

User request: "detect bottlenecks in my database queries"

The skill will:
1. Analyze database query performance and identify slow-running queries.
2. Suggest optimizations like indexing or query rewriting to improve database performance.

### Example 2: Identifying Memory Leaks

User request: "analyze performance and find memory leaks"

The skill will:
1. Profile memory usage patterns to identify potential memory leaks.
2. Provide code examples and recommendations to fix the memory leaks.

### Example 3: Optimizing CPU Usage

User request: "Profile my Python script and find the most CPU-intensive functions."

The skill will:
1. Analyze the script's CPU usage.
2. Generate a profile identifying the functions consuming the most CPU time.

## Best Practices

- **Comprehensive Analysis**: Always analyze all potential bottleneck areas (CPU, memory, I/O, database) for a complete picture.
- **Prioritize by Severity**: Focus on addressing the most severe bottlenecks first for maximum impact.
- **Test Thoroughly**: After implementing remediation strategies, thoroughly test the application to ensure performance improvements.
- **Use Realistic Workloads**: During profiling, simulate real-world scenarios for accurate results.