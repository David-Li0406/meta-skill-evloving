---
name: redis-best-practices
description: Redis performance optimization and best practices guidelines for data structures, key design, connection management, and caching patterns. Use when writing, reviewing, or refactoring code that interacts with Redis, designing cache strategies, optimizing commands, or implementing high-performance data operations. Triggers on tasks involving Redis, caching, session storage, pub/sub, key-value stores, or in-memory database performance.
license: MIT
metadata:
  author: Redis
  version: "1.0.0"
---

# Redis Best Practices

Comprehensive performance optimization guide for Redis applications, containing 43 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Choosing Redis data structures
- Designing key naming conventions
- Managing connections and pooling
- Writing or optimizing Redis commands
- Implementing caching patterns
- Configuring memory management
- Setting up persistence (RDB/AOF)
- Building clustered or highly available deployments
- Monitoring Redis performance

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Data Structures | CRITICAL | `ds-` |
| 2 | Key Design | CRITICAL | `key-` |
| 3 | Connection Management | HIGH | `conn-` |
| 4 | Commands & Patterns | HIGH | `cmd-` |
| 5 | Memory Management | MEDIUM-HIGH | `memory-` |
| 6 | Persistence | MEDIUM | `persist-` |
| 7 | Clustering & High Availability | MEDIUM | `cluster-` |
| 8 | Performance & Monitoring | LOW-MEDIUM | `perf-` |

## Quick Reference

### 1. Data Structures (CRITICAL)

- `ds-use-hashes-for-objects` - Store objects as Hashes, not multiple keys
- `ds-choose-right-type` - Match data structure to access pattern
- `ds-use-sets-for-unique` - Use Sets for unique collections
- `ds-use-sorted-sets-for-ranking` - Use Sorted Sets for leaderboards/rankings
- `ds-use-lists-for-queues` - Use Lists for queues and stacks
- `ds-use-streams-for-logs` - Use Streams for event logs and messaging

### 2. Key Design (CRITICAL)

- `key-use-namespacing` - Use colon-separated namespacing
- `key-keep-names-short` - Balance readability with memory efficiency
- `key-set-expiration` - Always set TTL on cache keys
- `key-avoid-large-keys` - Keep values under recommended limits
- `key-use-scan-not-keys` - Never use KEYS in production
- `key-design-for-access` - Design keys around access patterns

### 3. Connection Management (HIGH)

- `conn-use-connection-pool` - Always use connection pooling
- `conn-use-pipelining` - Batch commands with pipelining
- `conn-handle-reconnection` - Implement proper reconnection logic
- `conn-configure-timeouts` - Set appropriate connection timeouts
- `conn-use-dedicated-connections` - Separate connections for pub/sub

### 4. Commands & Patterns (HIGH)

- `cmd-avoid-keys-command` - Use SCAN instead of KEYS
- `cmd-use-multi-for-atomicity` - Use transactions for atomic operations
- `cmd-use-lua-scripts` - Use Lua scripts for complex atomic operations
- `cmd-avoid-blocking-commands` - Understand blocking command implications
- `cmd-use-batch-operations` - Use MGET/MSET for multiple keys
- `cmd-implement-distributed-locks` - Use Redlock for distributed locking

### 5. Memory Management (MEDIUM-HIGH)

- `memory-configure-maxmemory` - Always set maxmemory limit
- `memory-choose-eviction-policy` - Select appropriate eviction policy
- `memory-optimize-data-types` - Use memory-efficient encodings
- `memory-monitor-fragmentation` - Monitor and handle fragmentation
- `memory-use-lazy-free` - Enable lazy freeing for large deletions

### 6. Persistence (MEDIUM)

- `persist-understand-rdb-aof` - Choose between RDB and AOF
- `persist-configure-fsync` - Balance durability vs performance
- `persist-use-rdb-for-backups` - Use RDB snapshots for backups
- `persist-aof-rewrite` - Configure AOF rewrite properly
- `persist-test-recovery` - Regularly test backup recovery

### 7. Clustering & High Availability (MEDIUM)

- `cluster-use-sentinel` - Use Sentinel for HA without clustering
- `cluster-understand-sharding` - Understand Redis Cluster hash slots
- `cluster-handle-redirects` - Handle MOVED and ASK redirects
- `cluster-use-replica-reads` - Offload reads to replicas
- `cluster-plan-resharding` - Plan for cluster resharding

### 8. Performance & Monitoring (LOW-MEDIUM)

- `perf-use-slowlog` - Monitor slow commands with SLOWLOG
- `perf-monitor-memory` - Track memory usage and trends
- `perf-use-info-command` - Use INFO for comprehensive stats
- `perf-monitor-latency` - Track and diagnose latency issues
- `perf-benchmark-properly` - Use redis-benchmark correctly

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/ds-use-hashes-for-objects.md
rules/key-use-namespacing.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
