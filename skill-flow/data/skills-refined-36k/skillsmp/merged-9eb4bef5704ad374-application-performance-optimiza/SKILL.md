---
name: application-performance-optimization
description: Use this skill when you need to analyze and optimize application performance by identifying bottlenecks in CPU, memory, I/O, and execution time.
---

# Application Performance Optimization

This skill provides automated assistance for analyzing and optimizing application performance.

## Overview

This skill empowers Claude to detect performance bottlenecks across various layers of an application, including CPU usage, memory consumption, I/O operations, and execution time. It assists in optimizing resource utilization and improving overall application speed and responsiveness.

## How It Works

1. **Architecture Analysis**: Claude analyzes the application's architecture and data flow to understand potential bottlenecks.
2. **Bottleneck Identification**: The skill identifies bottlenecks in CPU, memory, I/O, database, lock contention, and resource exhaustion.
3. **Performance Metrics Analysis**: It examines CPU usage, memory allocation, and execution time to detect performance issues.
4. **Remediation Suggestions**: Claude provides remediation strategies with code examples to resolve identified bottlenecks and improve performance.

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
- **Realistic Workloads**: Use realistic workloads during profiling to simulate real-world scenarios.
- **Iterative Optimization**: Apply optimizations iteratively and re-profile to measure improvements.
- **Test Thoroughly**: After implementing remediation strategies, thoroughly test the application to ensure the bottlenecks are resolved and no new issues are introduced.

## Integration

This skill can be used in conjunction with code generation and editing plugins to automatically implement the suggested remediation strategies directly within the application's source code. It also integrates with monitoring and logging tools to provide real-time performance data.

## Prerequisites

- Appropriate file access permissions
- Required dependencies installed

## Instructions

1. Invoke this skill when the trigger conditions are met.
2. Provide necessary context and parameters.
3. Review the generated output.
4. Apply modifications as needed.

## Output

The skill produces structured output relevant to the task.

## Error Handling

- Invalid input: Prompts for correction.
- Missing dependencies: Lists required components.
- Permission errors: Suggests remediation steps.

## Resources

- Project documentation
- Related skills and commands