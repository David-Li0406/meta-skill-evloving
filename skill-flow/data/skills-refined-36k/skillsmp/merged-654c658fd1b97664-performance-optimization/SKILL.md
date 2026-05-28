---
name: performance-optimization
description: Use this skill to analyze and optimize code and system performance, identifying bottlenecks and suggesting improvements.
---

# Performance Optimization

This agent automates the analysis and optimization of code performance, identifying bottlenecks and implementing enhancements across various programming languages and systems.

## Agent Expertise

- Performance profiling and analysis
- Algorithm optimization
- Memory leak detection and prevention
- Database query optimization
- Caching strategies implementation
- Web performance enhancements
- System architecture improvements

## Key Capabilities

1. **Bottleneck Detection**: Analyze code execution paths to find slow operations.
2. **Algorithm Optimization**: Suggest more efficient algorithms and data structures.
3. **Memory Analysis**: Detect memory leaks and excessive allocations.
4. **Database Tuning**: Optimize queries, suggest indexes, and reduce N+1 problems.
5. **Web Performance**: Optimize bundle sizes, implement lazy loading, and code splitting.
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
"Optimize performance of <file_path>"

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
- Implement service workers for caching.
- Optimize asset delivery (compression, CDN).

## Supported Languages

- JavaScript/TypeScript (Node.js, React, Vue, Angular)
- Python (Django, Flask, FastAPI)
- Java (Spring, Hibernate)
- Go
- Rust
- C/C++
- SQL (PostgreSQL, MySQL, MongoDB)

## Tools & Integration

The agent can set up and integrate with:
- Chrome DevTools Performance
- Lighthouse
- Web Vitals
- Node.js profiler
- Python cProfile
- Java JProfiler
- Database EXPLAIN ANALYZE
- Memory profilers (Valgrind, Instruments)

## Best Practices

- Always benchmark before and after optimizations.
- Focus on high-impact optimizations first (80/20 rule).
- Profile in production-like environments.
- Set performance budgets and monitor regressions.
- Document optimization decisions for future reference.

## Performance Metrics

### Query Performance Targets

| Operation | Target | Warning | Critical |
|-----------|--------|---------|----------|
| Simple GET | < 50ms | > 100ms | > 500ms |
| List GET (paginated) | < 100ms | > 200ms | > 1s |
| Complex query | < 200ms | > 500ms | > 2s |
| Create/Update | < 100ms | > 200ms | > 1s |

### Memory Targets

| Metric | Target | Warning |
|--------|--------|---------|
| Gen 0 GC/min | < 10 | > 50 |
| Gen 2 GC/min | < 1 | > 5 |
| LOH allocations | Minimal | Frequent |

## Execution Flow

```
1. Scan Source Files
   ↓
2. Pattern Detection
   - N+1 queries
   - Missing optimizations
   - Memory issues
   ↓
3. Analyze Query Plans (if possible)
   ↓
4. Generate Recommendations
   ↓
5. Prioritize by Impact
   ↓
6. Output Report
```

## Author

**GLINCKER Team**