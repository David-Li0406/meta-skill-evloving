# Sections

## 1. Query Optimization (query)

**Impact:** CRITICAL
**Description:** EXPLAIN analysis, N+1 prevention, efficient pagination. Query optimization is the most impactful way to improve database performance.

## 2. Security (security)

**Impact:** CRITICAL
**Description:** Prepared statements, least privilege access, encryption. Database security prevents SQL injection and protects sensitive data.

## 3. Schema Design (schema)

**Impact:** HIGH
**Description:** Appropriate data types, normalization levels, constraints. Good schema design prevents data anomalies and improves performance.

## 4. Indexing Strategy (index)

**Impact:** HIGH
**Description:** Composite index design, covering indexes, cardinality analysis. Proper indexing dramatically speeds up query execution.

## 5. Transaction Management (txn)

**Impact:** MEDIUM-HIGH
**Description:** ACID compliance, isolation levels, deadlock prevention. Correct transaction handling ensures data integrity.

## 6. Connection Management (conn)

**Impact:** MEDIUM
**Description:** Connection pooling, timeout configuration, max connections. Efficient connection management prevents resource exhaustion.

## 7. Backup & Recovery (backup)

**Impact:** MEDIUM
**Description:** Backup strategies, point-in-time recovery, testing restores. Reliable backups are essential for disaster recovery.

## 8. Replication (repl)

**Impact:** LOW-MEDIUM
**Description:** Master-slave configuration, read replicas, failover. Replication provides high availability and read scaling.
