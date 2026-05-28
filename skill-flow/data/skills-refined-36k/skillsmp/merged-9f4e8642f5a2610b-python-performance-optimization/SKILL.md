---
name: python-performance-optimization
description: Use this skill when writing, reviewing, or refactoring Python code (>=3.11) to ensure optimal performance patterns across various aspects like concurrency, memory management, and data structures.
---

# Python Performance Optimization Guidelines

Comprehensive performance optimization guide for Python 3.11+ applications. Contains 45 rules across multiple categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Python async/await code
- Processing large datasets or files
- Implementing caching and memoization
- Choosing data structures for performance
- Reviewing code for performance issues

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
- `io-async-file-operations` - Use async file I/O for non-blocking operations.
- `io-connection-pooling` - Use connection pooling for database and HTTP clients.
- `io-streaming-large-files` - Stream large files instead of loading into memory.

### 2. Async Concurrency (CRITICAL)
- `async-avoid-blocking-calls` - Avoid blocking calls in async code.
- `async-gather-independent-operations` - Use asyncio.gather() for independent operations.
- `async-taskgroup-structured-concurrency` - Use TaskGroup for structured concurrency.

### 3. Memory Management (HIGH)
- `mem-avoid-intermediate-lists` - Avoid intermediate lists in pipelines.
- `mem-generators-lazy-evaluation` - Use generators for lazy evaluation.
- `mem-string-interning` - Leverage string interning for repeated strings.

### 4. Data Structures (HIGH)
- `ds-deque-for-queues` - Use deque for O(1) queue operations.
- `ds-set-for-membership` - Use Set for O(1) membership testing.
- `ds-namedtuple-immutable-records` - Use NamedTuple for immutable lightweight records.

### 5. Algorithm Efficiency (MEDIUM-HIGH)
- `algo-avoid-repeated-computation` - Cache expensive computations in loops.
- `algo-list-comprehension` - Use list comprehensions over manual loops.
- `algo-string-join` - Use str.join() for string concatenation.

### 6. Concurrency Model (MEDIUM)
- `conc-asyncio-queues` - Use asyncio.Queue for producer-consumer patterns.
- `conc-choose-right-model` - Choose the right concurrency model.

### 7. Serialization (MEDIUM)
- `serial-avoid-pickle-security` - Avoid pickle for untrusted data.
- `serial-orjson-over-json` - Use orjson for high-performance JSON.

### 8. Caching and Memoization (LOW-MEDIUM)
- `cache-lru-cache-decorator` - Use lru_cache for expensive pure functions.
- `cache-cached-property` - Use cached_property for expensive computed attributes.

### 9. Runtime Tuning (LOW)
- `runtime-avoid-global-lookups` - Avoid repeated global and module lookups.
- `runtime-profile-before-optimizing` - Profile before optimizing.

## How to Use

Read individual reference files for detailed explanations and code examples. Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## References

1. [Python 3.11 Release Notes](https://docs.python.org/3/whatsnew/3.11.html)
2. [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
3. [Python Wiki - Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
4. [Real Python - Async IO](https://realpython.com/async-io-python/)
5. [JetBrains - Performance Hacks](https://blog.jetbrains.com/pycharm/2025/11/10-smart-performance-hacks-for-faster-python-code/)