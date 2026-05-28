---
name: performance-optimization
description: Use this skill when you need to analyze application performance, identify bottlenecks, and receive optimization recommendations for CPU, memory, and execution time.
---

# Skill body

## Overview

This skill empowers Claude to analyze application performance, pinpoint bottlenecks, and recommend optimizations. It examines CPU usage, memory consumption, and execution time to facilitate targeted improvements.

## How It Works

1. **Identify Application Stack**: Determine the application's technology (e.g., Node.js, Python, Java).
2. **Locate Entry Points**: Identify main application entry points and critical execution paths.
3. **Analyze Performance Metrics**: Examine CPU usage, memory allocation, and execution time to detect bottlenecks.
4. **Generate Profile**: Compile the analysis into a comprehensive performance profile, highlighting areas for optimization.
5. **Remediation Suggestions**: Provide code examples and recommendations to resolve identified bottlenecks.

## When to Use This Skill

This skill activates when you need to:
- Diagnose slow application performance.
- Optimize resource usage (CPU, memory, I/O).
- Proactively prevent performance issues.
- Identify CPU-intensive operations and memory leaks.

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
3. Provide recommendations for optimizing the code, such as using more efficient algorithms or asynchronous operations.

## Best Practices

- **Comprehensive Analysis**: Always analyze all potential bottleneck areas (CPU, memory, I/O) for a complete picture.
- **Prioritize by Severity**: Focus on addressing the most severe bottlenecks first for maximum impact.
- **Test Thoroughly**: After implementing remediation strategies, thoroughly test the application to ensure the bottlenecks are resolved.
- **Realistic Workloads**: Use realistic workloads during profiling to simulate real-world scenarios.