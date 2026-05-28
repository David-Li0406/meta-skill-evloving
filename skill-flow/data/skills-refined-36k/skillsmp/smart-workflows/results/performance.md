# Performance Benchmarks

See [PERFORMANCE.md](https://github.com/bjoernbethge/mcp-b/blob/main/PERFORMANCE.md) for detailed benchmarks.

## Summary

MCP-B performance optimizations include:

- **Caching**: LRU and TTL-based caching for expensive operations
- **Lazy properties**: Deferred computation for infrequently accessed attributes
- **Batch operations**: Efficient processing of large datasets
- **Memory efficiency**: Generators and streaming for large data

## Running Benchmarks

```bash
python benchmark_performance.py
```
