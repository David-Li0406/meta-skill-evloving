---
name: detecting-memory-leaks
description: Use this skill when you need to identify and resolve potential memory leaks in your application to improve performance and stability.
---

# Skill body

## Overview

This skill helps you identify and resolve memory leaks in your code by analyzing it for common memory leak patterns.

## How It Works

1. **Initiate Analysis**: The user requests memory leak detection.
2. **Code Analysis**: The skill analyzes the codebase for potential memory leak patterns.
3. **Report Generation**: The skill generates a report detailing potential memory leaks and recommended fixes.

## When to Use This Skill

Use this skill to:
- Detect potential memory leaks in your application.
- Analyze memory usage patterns to identify performance bottlenecks.
- Troubleshoot performance issues related to memory leaks.

## Examples

### Example 1: Identifying Event Listener Leaks

User request: "detect memory leaks in my event handling code"

The skill will:
1. Analyze the code for unremoved event listeners.
2. Generate a report highlighting potential event listener leaks and suggesting how to properly remove them.

### Example 2: Analyzing Cache Growth

User request: "analyze memory usage to find excessive cache growth"

The skill will:
1. Analyze cache implementations for unbounded growth.
2. Identify caches that are not properly managed and recommend strategies for limiting their size.

## Best Practices

- **Code Review**: Always review the reported potential leaks to ensure they are genuine issues.
- **Regular Analysis**: Incorporate memory leak detection into your regular development workflow.
- **Targeted Analysis**: Focus your analysis on specific areas of your code that are known to be memory-intensive.

## Integration

This skill can be used in conjunction with other performance analysis tools to provide a comprehensive overview of your application's memory usage.