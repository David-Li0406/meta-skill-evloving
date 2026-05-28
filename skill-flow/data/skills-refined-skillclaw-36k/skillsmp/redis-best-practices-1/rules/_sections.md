# Section Metadata

This file defines the sections and their order for the Redis Best Practices guide.

## Sections

| # | Prefix | Name | Impact | Description |
|---|--------|------|--------|-------------|
| 1 | `ds-` | Data Structures | CRITICAL | Choosing and using the right Redis data types |
| 2 | `key-` | Key Design | CRITICAL | Key naming, sizing, and expiration patterns |
| 3 | `conn-` | Connection Management | HIGH | Connection pooling, pipelining, and resilience |
| 4 | `cmd-` | Commands & Patterns | HIGH | Command usage, transactions, and Lua scripts |
| 5 | `memory-` | Memory Management | MEDIUM-HIGH | Memory limits, eviction, and optimization |
| 6 | `persist-` | Persistence | MEDIUM | RDB snapshots and AOF configuration |
| 7 | `cluster-` | Clustering & HA | MEDIUM | Redis Cluster, Sentinel, and replication |
| 8 | `perf-` | Performance & Monitoring | LOW-MEDIUM | SLOWLOG, INFO, and performance tuning |

## Impact Levels

- **CRITICAL**: Issues that can cause outages, data loss, or severe performance degradation
- **HIGH**: Significant performance or reliability impact
- **MEDIUM-HIGH**: Notable performance improvements
- **MEDIUM**: Good practices that improve efficiency
- **LOW-MEDIUM**: Nice-to-have optimizations
- **LOW**: Minor improvements
