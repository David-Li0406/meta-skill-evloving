---
name: supabase-postgres-best-practices
description: Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations to ensure performance and security.
---

# Supabase Postgres Best Practices

Comprehensive performance optimization guide for Postgres, maintained by Supabase. Contains performance rules across 8 categories, prioritized by impact to guide automated query optimization and schema design.

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling or scaling
- Optimizing for Postgres-specific features
- Working with Row-Level Security (RLS)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

## Table of Contents

1. [Query Performance](#query-performance) - **CRITICAL**
   - 1.1 [Add Indexes on WHERE and JOIN Columns](#11-add-indexes-on-where-and-join-columns)
   - 1.2 [Choose the Right Index Type for Your Data](#12-choose-the-right-index-type-for-your-data)
   - 1.3 [Create Composite Indexes for Multi-Column Queries](#13-create-composite-indexes-for-multi-column-queries)
   - 1.4 [Use Covering Indexes to Avoid Table Lookups](#14-use-covering-indexes-to-avoid-table-lookups)
   - 1.5 [Use Partial Indexes for Filtered Queries](#15-use-partial-indexes-for-filtered-queries)

2. [Connection Management](#connection-management) - **CRITICAL**
   - 2.1 [Configure Idle Connection Timeouts](#21-configure-idle-connection-timeouts)
   - 2.2 [Set Appropriate Connection Limits](#22-set-appropriate-connection-limits)
   - 2.3 [Use Connection Pooling for All Applications](#23-use-connection-pooling-for-all-applications)
   - 2.4 [Use Prepared Statements Correctly with Pooling](#24-use-prepared-statements-correctly-with-pooling)

3. [Security & RLS](#security-rls) - **CRITICAL**
   - 3.1 [Apply Principle of Least Privilege](#31-apply-principle-of-least-privilege)
   - 3.2 [Enable Row Level Security for Multi-Tenant Data](#32-enable-row-level-security-for-multi-tenant-data)
   - 3.3 [Optimize RLS Policies for Performance](#33-optimize-rls-policies-for-performance)

4. [Schema Design](#schema-design) - **HIGH**
   - 4.1 [Choose Appropriate Data Types](#41-choose-appropriate-data-types)
   - 4.2 [Index Foreign Key Columns](#42-index-foreign-key-columns)
   - 4.3 [Partition Large Tables for Better Performance](#43-partition-large-tables-for-better-performance)
   - 4.4 [Select Optimal Primary Key Strategy](#44-select-optimal-primary-key-strategy)
   - 4.5 [Use Lowercase Identifiers for Compatibility](#45-use-lowercase-identifiers-for-compatibility)

5. [Concurrency & Locking](#concurrency-locking) - **MEDIUM-HIGH**
   - 5.1 [Keep Transactions Short to Reduce Lock Contention](#51-keep-transactions-short-to-reduce-lock-contention)
   - 5.2 [Prevent Deadlocks with Consistent Lock Ordering](#52-prevent-deadlocks-with-consistent-lock-ordering)
   - 5.3 [Use Advisory Locks for Application-Level Locking](#53-use-advisory-locks-for-application-level-locking)
   - 5.4 [Use SKIP LOCKED for Non-Blocking Queue Processing](#54-use-skip-locked-for-non-blocking-queue-processing)

6. [Data Access Patterns](#data-access-patterns) - **MEDIUM**
   - 6.1 [Batch INSERT Statements for Bulk Data](#61-batch-insert-statements-for-bulk-data)
   - 6.2 [Eliminate N+1 Queries with Batch Loading](#62-eliminate-n1-queries-with-batch-loading)
   - 6.3 [Use Cursor-Based Pagination Instead of OFFSET](#63-use-cursor-based-pagination-instead-of-offset)
   - 6.4 [Use UPSERT for Insert-or-Update Operations](#64-use-upsert-for-insert-or-update-operations)

7. [Monitoring & Diagnostics](#monitoring-diagnostics) - **LOW-MEDIUM**
   - 7.1 [Enable pg_stat_statements for Query Analysis](#71-enable-pgstatstatements-for-query-analysis)
   - 7.2 [Maintain Table Statistics with VACUUM and ANALYZE](#72-maintain-table-statistics-with-vacuum-and-analyze)
   - 7.3 [Use EXPLAIN ANALYZE to Diagnose Slow Queries](#73-use-explain-analyze-to-diagnose-slow-queries)

8. [Advanced Features](#advanced-features) - **LOW**
   - 8.1 [Index JSONB Columns for Efficient Querying](#81-index-jsonb-columns-for-efficient-querying)
   - 8.2 [Use tsvector for Full-Text Search](#82-use-tsvector-for-full-text-search)

---

## 1. Query Performance

**Impact: CRITICAL**

Slow queries, missing indexes, inefficient query plans. The most common source of Postgres performance issues.

### 1.1 Add Indexes on WHERE and JOIN Columns

**Impact: CRITICAL (100-1000x faster queries on large tables)**

Queries filtering or joining on unindexed columns cause full table scans, which become exponentially slower as tables grow.

**Incorrect (sequential scan on large table):**

```sql
-- No index on customer_id causes full table scan
select * from orders where customer_id = 123;
```

**Correct (index scan):**

```sql
-- Create index on frequently filtered column
create index orders_customer_id_idx on orders (customer_id);
select * from orders where customer_id = 123;
```

### 1.2 Choose the Right Index Type for Your Data

**Impact: HIGH (10-100x improvement with correct index type)**

Different index types excel at different query patterns. The default B-tree isn't always optimal.

**Incorrect (B-tree for JSONB containment):**

```sql
create index products_attrs_idx on products (attributes);
```

**Correct (GIN for JSONB):**

```sql
create index products_attrs_idx on products using gin (attributes);
```

### 1.3 Create Composite Indexes for Multi-Column Queries

**Impact: HIGH (5-10x faster multi-column queries)**

When queries filter on multiple columns, a composite index is more efficient than separate single-column indexes.

**Incorrect (separate indexes require bitmap scan):**

```sql
create index orders_status_idx on orders (status);
create index orders_created_idx on orders (created_at);
```

**Correct (composite index):**

```sql
create index orders_status_created_idx on orders (status, created_at);
```

### 1.4 Use Covering Indexes to Avoid Table Lookups

**Impact: MEDIUM-HIGH (2-5x faster queries by eliminating heap fetches)**

Covering indexes include all columns needed by a query, enabling index-only scans that skip the table entirely.

**Incorrect (index scan + heap fetch):**

```sql
create index users_email_idx on users (email);
```

**Correct (index-only scan with INCLUDE):**

```sql
create index users_email_idx on users (email) include (name, created_at);
```

### 1.5 Use Partial Indexes for Filtered Queries

**Impact: HIGH (5-20x smaller indexes, faster writes and queries)**

Partial indexes only include rows matching a WHERE condition, making them smaller and faster when queries consistently filter on the same condition.

**Incorrect (full index includes irrelevant rows):**

```sql
create index users_email_idx on users (email);
```

**Correct (partial index matches query filter):**

```sql
create index users_active_email_idx on users (email) where deleted_at is null;
```

---

## 2. Connection Management

**Impact: CRITICAL**

Connection pooling, limits, and serverless strategies. Critical for applications with high concurrency or serverless deployments.

### 2.1 Configure Idle Connection Timeouts

**Impact: HIGH (Reclaim 30-50% of connection slots from idle clients)**

Idle connections waste resources. Configure timeouts to automatically reclaim them.

**Incorrect (connections held indefinitely):**

```sql
show idle_in_transaction_session_timeout;  -- 0 (disabled)
```

**Correct (automatic cleanup of idle connections):**

```ini
alter system set idle_in_transaction_session_timeout = '30s';
```

### 2.2 Set Appropriate Connection Limits

**Impact: CRITICAL (Prevent database crashes and memory exhaustion)**

Too many connections exhaust memory and degrade performance. Set limits based on available resources.

**Incorrect (unlimited or excessive connections):**

```sql
show max_connections;  -- 500 (way too high for 4GB RAM)
```

**Correct (calculate based on resources):**

```sql
alter system set max_connections = 100;
```

### 2.3 Use Connection Pooling for All Applications

**Impact: CRITICAL (Handle 10-100x more concurrent users)**

Postgres connections are expensive (1-3MB RAM each). Without pooling, applications exhaust connections under load.

**Incorrect (new connection per request):**

```sql
select count(*) from pg_stat_activity;  -- 487 connections!
```

**Correct (connection pooling):**

```sql
-- Use a pooler like PgBouncer between app and database
```

### 2.4 Use Prepared Statements Correctly with Pooling

**Impact: HIGH (Avoid prepared statement conflicts in pooled environments)**

Prepared statements are tied to individual database connections. In transaction-mode pooling, connections are shared, causing conflicts.

**Incorrect (named prepared statements with transaction pooling):**

```sql
prepare get_user as select * from users where id = $1;
```

**Correct (use unnamed statements or session mode):**

```sql
-- Option 1: Use unnamed prepared statements
```

---

## 3. Security & RLS

**Impact: CRITICAL**

Row-Level Security policies, privilege management, and authentication patterns.

### 3.1 Apply Principle of Least Privilege

**Impact: MEDIUM (Reduced attack surface, better audit trail)**

Grant only the minimum permissions required. Never use superuser for application queries.

**Incorrect (overly broad permissions):**

```sql
grant all privileges on all tables in schema public to app_user;
```

**Correct (minimal, specific grants):**

```sql
create role app_readonly nologin;
grant select on public.products, public.categories to app_readonly;
```

### 3.2 Enable Row Level Security for Multi-Tenant Data

**Impact: CRITICAL (Database-enforced tenant isolation, prevent data leaks)**

Row Level Security (RLS) enforces data access at the database level, ensuring users only see their own data.

**Incorrect (application-level filtering only):**

```sql
select * from orders where user_id = $current_user_id;
```

**Correct (database-enforced RLS):**

```sql
alter table orders enable row level security;
```

### 3.3 Optimize RLS Policies for Performance

**Impact: HIGH (5-10x faster RLS queries with proper patterns)**

Poorly written RLS policies can cause severe performance issues. Use subqueries and indexes strategically.

**Incorrect (function called for every row):**

```sql
create policy orders_policy on orders using (auth.uid() = user_id);
```

**Correct (wrap functions in SELECT):**

```sql
create policy orders_policy on orders using ((select auth.uid()) = user_id);
```

---

## 4. Schema Design

**Impact: HIGH**

Table design, index strategies, partitioning, and data type selection. Foundation for long-term performance.

### 4.1 Choose Appropriate Data Types

**Impact: HIGH (50% storage reduction, faster comparisons)**

Using the right data types reduces storage, improves query performance, and prevents bugs.

**Incorrect (wrong data types):**

```sql
create table users (id int, email varchar(255), created_at timestamp);
```

**Correct (appropriate data types):**

```sql
create table users (id bigint generated always as identity primary key, email text, created_at timestamptz);
```

### 4.2 Index Foreign Key Columns

**Impact: HIGH (10-100x faster JOINs and CASCADE operations)**

Postgres does not automatically index foreign key columns. Missing indexes cause slow JOINs and CASCADE operations.

**Incorrect (unindexed foreign key):**

```sql
create table orders (id bigint generated always as identity primary key, customer_id bigint references customers(id) on delete cascade);
```

**Correct (indexed foreign key):**

```sql
create index orders_customer_id_idx on orders (customer_id);
```

### 4.3 Partition Large Tables for Better Performance

**Impact: MEDIUM-HIGH (5-20x faster queries and maintenance on large tables)**

Partitioning splits a large table into smaller pieces, improving query performance and maintenance operations.

**Incorrect (single large table):**

```sql
create table events (id bigint generated always as identity, created_at timestamptz);
```

**Correct (partitioned by time range):**

```sql
create table events (id bigint generated always as identity, created_at timestamptz not null) partition by range (created_at);
```

### 4.4 Select Optimal Primary Key Strategy

**Impact: HIGH (Better index locality, reduced fragmentation)**

Primary key choice affects insert performance, index size, and replication efficiency.

**Incorrect (problematic PK choices):**

```sql
create table users (id serial primary key);
```

**Correct (optimal PK strategies):**

```sql
create table users (id bigint generated always as identity primary key);
```

### 4.5 Use Lowercase Identifiers for Compatibility

**Impact: MEDIUM (Avoid case-sensitivity bugs with tools, ORMs, and AI assistants)**

PostgreSQL folds unquoted identifiers to lowercase. Quoted mixed-case identifiers require quotes forever and cause issues with tools, ORMs, and AI assistants that may not recognize them.

**Incorrect (mixed-case identifiers):**

```sql
CREATE TABLE "Users" ( "userId" bigint PRIMARY KEY );
```

**Correct (lowercase snake_case):**

```sql
CREATE TABLE users ( user_id bigint PRIMARY KEY );
```

---

## 5. Concurrency & Locking

**Impact: MEDIUM-HIGH**

Transaction management, isolation levels, deadlock prevention, and lock contention patterns.

### 5.1 Keep Transactions Short to Reduce Lock Contention

**Impact: MEDIUM-HIGH (3-5x throughput improvement, fewer deadlocks)**

Long-running transactions hold locks that block other queries. Keep transactions as short as possible.

**Incorrect (long transaction with external calls):**

```sql
begin;
select * from orders where id = 1 for update;
```

**Correct (minimal transaction scope):**

```sql
begin;
update orders set status = 'paid' where id = 1;
commit;
```

### 5.2 Prevent Deadlocks with Consistent Lock Ordering

**Impact: MEDIUM-HIGH (Eliminate deadlock errors, improve reliability)**

Deadlocks occur when transactions lock resources in different orders. Always acquire locks in a consistent order.

**Incorrect (inconsistent lock ordering):**

```sql
begin;
update accounts set balance = balance - 100 where id = 1;
update accounts set balance = balance + 100 where id