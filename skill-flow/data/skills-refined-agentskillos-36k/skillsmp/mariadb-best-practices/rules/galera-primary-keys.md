---
title: All Tables Must Have Primary Keys
impact: MEDIUM-HIGH
impactDescription: Required for Galera Cluster replication to work correctly
tags: galera, primary-key, replication, cluster
---

## All Tables Must Have Primary Keys

Galera Cluster uses primary keys for row identification during replication. Tables without primary keys cause replication issues and certification failures.

**Incorrect (no primary key):**

```sql
-- ❌ No primary key - Galera certification fails
CREATE TABLE logs (
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ❌ Only unique key, not primary
CREATE TABLE settings (
    name VARCHAR(100) UNIQUE,
    value TEXT
);

-- Galera will replicate these tables incorrectly or fail
```

**Correct (explicit primary keys):**

```sql
-- ✓ Auto-increment primary key
CREATE TABLE logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ✓ Natural primary key
CREATE TABLE settings (
    name VARCHAR(100) PRIMARY KEY,
    value TEXT
);

-- ✓ Composite primary key
CREATE TABLE order_items (
    order_id BIGINT UNSIGNED,
    product_id BIGINT UNSIGNED,
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- ✓ UUID primary key (good for distributed)
CREATE TABLE events (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    event_type VARCHAR(50),
    payload JSON
);
```

**Check for missing primary keys:**

```sql
-- Find tables without primary keys
SELECT t.TABLE_NAME
FROM information_schema.TABLES t
LEFT JOIN information_schema.TABLE_CONSTRAINTS c
    ON t.TABLE_NAME = c.TABLE_NAME
    AND c.CONSTRAINT_TYPE = 'PRIMARY KEY'
WHERE t.TABLE_SCHEMA = 'your_database'
    AND t.TABLE_TYPE = 'BASE TABLE'
    AND c.CONSTRAINT_NAME IS NULL;

-- Add primary key to existing table
ALTER TABLE logs ADD COLUMN id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY FIRST;
```

**Galera configuration to enforce:**

```ini
# my.cnf - Warn about tables without PKs
wsrep_certify_nonPK=OFF  # Default ON, set OFF to reject
```

Reference: [Galera Cluster Primary Keys](https://mariadb.com/kb/en/galera-cluster-known-limitations/#tables-without-a-primary-key)
