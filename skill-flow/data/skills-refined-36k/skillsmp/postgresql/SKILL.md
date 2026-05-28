---
name: postgresql
description: PostgreSQL database operations including backups, transactions, user management, window functions, materialized views, and extensions.
---

# PostgreSQL — Advanced Operations

**Connection**
```bash
psql -U username -d dbname -h host

```

**Backups**
```bash
pg_dump dbname > backup.sql
pg_restore -d dbname backup.sql
pg_dump -v -d 'postgres://postgres:postgres@localhost:5432/a' -n a -Fd -j 5 -f /backup/backup -t 'a.(test)' --no-acl --no-owner
pg_restore -v -d 'postgres://postgres:postgres@localhost:5432/b' -Fd -j5 /backup/backup --no-acl  --no-owner --disable-triggers
```

**Transactions**
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

**User Management**
```sql
CREATE USER username WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE dbname TO username;
```

## PostgreSQL — Advanced Features

**Window Functions**
```sql
SELECT department, employee, salary,
       AVG(salary) OVER (PARTITION BY department) as avg_dept_salary
FROM employees;
```

**Materialized Views**
```sql
CREATE MATERIALIZED VIEW sales_summary AS
SELECT product, SUM(quantity) FROM sales GROUP BY product;
REFRESH MATERIALIZED VIEW sales_summary;
```

**Extensions**
```sql
CREATE EXTENSION pg_trgm;  -- Fuzzy string matching
CREATE EXTENSION postgis;   -- Geospatial support
```


**Check Long-Running Queries**

```sql
SELECT now() - query_start, *
FROM pg_catalog.pg_stat_activity
WHERE state = 'active'
  AND now() - query_start > interval '5 minute';
```

**Table Disk Size**

```sql

SELECT nspname || '.' || relname AS "relation",
    pg_size_pretty(pg_total_relation_size(C.oid)) AS "total_size"
  FROM pg_class C
  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
  WHERE nspname NOT IN ('pg_catalog', 'information_schema')
    AND C.relkind <> 'i'
    AND nspname !~ '^pg_toast'
  ORDER BY pg_total_relation_size(C.oid) DESC
  LIMIT 20;
```


**Others**

```sql
\x -- format display

\d
\d+
\dt
\d+ <table_name>
\dn

SELECT jsonb_pretty(json_column::jsonb) FROM your_table;

SELECT *
FROM my_table
WHERE my_column ~ '[\u0009-\u000D\u00A0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000]';
SELECT * FROM users WHERE name LIKE 'Leo%';
SELECT * FROM users WHERE name ILIKE 'leo%';
SELECT * FROM users WHERE name SIMILAR TO '(Leo|Luke)%';
SELECT * FROM logs WHERE message ~ 'error|fail';
SELECT * FROM logs WHERE message ~* 'error|fail';
SELECT * FROM logs WHERE message !~ 'success';
SELECT * FROM products WHERE tags @> ARRAY['electronics'];
SELECT * FROM products WHERE ARRAY['electronics'] <@ tags;
SELECT * FROM products WHERE tags && ARRAY['electronics', 'home'];
SELECT data->'name' FROM users;
SELECT data->>'name' FROM users;
SELECT data#>'{address,city}' FROM users;
SELECT * FROM events WHERE timerange @> now();
SELECT * FROM events WHERE timerange && '[2025-01-01,2025-12-31)'::tstzrange;
SELECT * FROM table1 WHERE col1 IS DISTINCT FROM col2;
SELECT * FROM users WHERE role IN ('admin', 'user');

set search_path=public;

create unlogged table unlogged_table (
  id varchar(10) not null
);
alter table
  unlogged_table setlogged;



ALTER TABLE a.test SET SCHEMA b;

```