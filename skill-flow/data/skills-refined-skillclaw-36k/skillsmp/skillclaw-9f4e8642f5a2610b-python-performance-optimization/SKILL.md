---
name: python-performance-optimization
description: Use this skill when writing, reviewing, or refactoring Python code (version 3.11+) to ensure optimal performance patterns across various aspects like I/O, concurrency, and memory management.
---

# Python Performance Optimization Guidelines

This skill provides comprehensive performance optimization guidelines for Python 3.11+ applications, containing rules across multiple categories prioritized by their impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Python async/await code
- Processing large datasets or files
- Implementing caching and memoization
- Choosing data structures for performance
- Reviewing Python code for performance issues

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | I/O Patterns | CRITICAL | `io-` |
| 2 | Async Concurrency | CRITICAL | `async-` |
| 3 | Memory Management | HIGH | `mem-` |
| 4 | Data Structures | HIGH | `ds-` |
| 5 | Algorithm Efficiency | MEDIUM-HIGH | `algo-` |
| 6 | Concurrency Model | MEDIUM | `conc-` |
| 7 | Serialization | MEDIUM | `serial-` |
| 8 | Caching and Memoization | LOW-MEDIUM | `cache-` |
| 9 | Runtime Tuning | LOW | `runtime-` |

## Quick Reference

### 1. I/O Patterns (CRITICAL)
- Use async file I/O for non-blocking operations
- Batch database operations to reduce round trips
- Use connection pooling for database and HTTP clients
- Stream large files instead of loading into memory
- Use buffered I/O for frequent small writes

### 2. Async Concurrency (CRITICAL)
- Avoid async overhead for CPU-bound work
- Avoid blocking calls in async code
- Store references to fire-and-forget tasks
- Use asyncio.gather() for independent operations
- Use semaphores for concurrency limiting
- Use TaskGroup for structured concurrency

### 3. Memory Management (HIGH)
- Avoid intermediate lists in pipelines
- Use generators for lazy evaluation

### 4. Data Structures (HIGH)
- Use `defaultdict` to avoid key existence checks
- Use `bisect` for O(log n) sorted list operations

### 5. Algorithm Efficiency (MEDIUM-HIGH)
- Optimize algorithms for better performance

### 6. Concurrency Model (MEDIUM)
- Implement effective concurrency models for better resource management

### 7. Serialization (MEDIUM)
- Optimize serialization methods for performance

### 8. Caching and Memoization (LOW-MEDIUM)
- Implement caching strategies to improve performance

### 9. Runtime Tuning (LOW)
- Adjust runtime parameters for optimal performance