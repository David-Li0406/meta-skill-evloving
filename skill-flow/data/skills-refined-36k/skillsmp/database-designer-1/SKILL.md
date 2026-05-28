---
name: database-designer
description: Designs database schemas and migrations for PHP/CakePHP applications with multi-tenant support
---

# Database Designer

A specialized skill for designing database schemas, migrations, and multi-tenant architectures for PHP/CakePHP applications.

## Core Responsibilities

### 1. Schema Design Principles

**Normalization Levels:**
```sql
-- 1NF: Atomic values, no repeating groups
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    order_date DATETIME,
    -- Each column contains single value
);

-- 2NF: No partial dependencies
CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- 3NF: No transitive dependencies
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

### 2. CakePHP Migration Format

**Migration File Structure:**
```php
<?php
declare(strict_types=1);

use Migrations\AbstractMigration;

/**
 * Create Users table migration
 */
class CreateUsers extends AbstractMigration
{
    /**
     * Change Method.
     */
    public function change(): void
    {
        // Create table
        $table = $this->table('users');

        // Add columns
        $table->addColumn('email', 'string', [
            'default' => null,
            'limit' => 255,
            'null' => false,
        ])
        ->addColumn('password', 'string', [
            'default' => null,
            'limit' => 255,
            'null' => false,
        ])
        ->addColumn('name', 'string', [
            'default' => null,
            'limit' => 255,
            'null' => false,
        ])
        ->addColumn('company_id', 'integer', [
            'default' => null,
            'null' => false,
        ])
        ->addColumn('status', 'integer', [
            'default' => 1,
            'null' => false,
        ])
        ->addColumn('del_flg', 'integer', [
            'default' => 0,
            'null' => false,
        ])
        ->addColumn('created', 'datetime', [
            'default' => null,
            'null' => false,
        ])
        ->addColumn('modified', 'datetime', [
            'default' => null,
            'null' => false,
        ]);

        // Add indexes
        $table->addIndex(['email'], [
            'name' => 'idx_users_email',
            'unique' => true,
        ])
        ->addIndex(['company_id'], [
            'name' => 'idx_users_company',
        ])
        ->addIndex(['status', 'del_flg'], [
            'name' => 'idx_users_status_del',
        ]);

        // Add foreign keys
        $table->addForeignKey('company_id', 'companys', 'id', [
            'update' => 'CASCADE',
            'delete' => 'RESTRICT',
        ]);

        // Create table
        $table->create();
    }
}
```

### 3. Multi-Tenant Database Architecture

**Pattern 1: Shared Database, Shared Schema:**
```sql
-- All tenants in same tables with company_id
CREATE TABLE applications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT NOT NULL,
    user_id INT NOT NULL,
    status INT DEFAULT 1,
    created DATETIME,
    INDEX idx_company (company_id),
    FOREIGN KEY (company_id) REFERENCES companys(id)
);
```

**Pattern 2: Shared Database, Separate Schema (Multi-Tenant Pattern):**
```sql
-- Account schema (shared)
CREATE DATABASE [app]_account_schema;
USE [app]_account_schema;

CREATE TABLE companys (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    database_name VARCHAR(100)
);

-- Company-specific schemas (per-tenant databases)
CREATE DATABASE [app_prefix]_company_9999;
USE [app_prefix]_company_9999;

CREATE TABLE applications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    -- No company_id needed, database is company-specific
    user_id INT NOT NULL,
    status INT DEFAULT 1
);
```


### 4. Table Design Patterns

**Standard Business Table:**
```sql
CREATE TABLE orders (
    -- Primary key
    id INT PRIMARY KEY AUTO_INCREMENT,

    -- Foreign keys
    user_id INT NOT NULL,
    company_id INT NOT NULL,

    -- Business fields
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10,2) DEFAULT 0.00,
    status INT DEFAULT 1,
    order_date DATE NOT NULL,

    -- Metadata
    del_flg INT DEFAULT 0,
    created DATETIME NOT NULL,
    created_by INT,
    modified DATETIME NOT NULL,
    modified_by INT,

    -- Indexes
    INDEX idx_user (user_id),
    INDEX idx_company (company_id),
    INDEX idx_status_del (status, del_flg),
    INDEX idx_order_date (order_date),

    -- Foreign keys
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (company_id) REFERENCES companys(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Association Table (Many-to-Many):**
```sql
CREATE TABLE users_roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    created DATETIME NOT NULL,

    -- Unique constraint for relationship
    UNIQUE KEY unique_user_role (user_id, role_id),

    -- Indexes for lookups
    INDEX idx_user (user_id),
    INDEX idx_role (role_id),

    -- Foreign keys with CASCADE
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
) ENGINE=InnoDB;
```

**Audit/History Table:**
```sql
CREATE TABLE order_histories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    action VARCHAR(50) NOT NULL, -- 'create', 'update', 'delete'
    old_values JSON,
    new_values JSON,
    changed_by INT,
    changed_at DATETIME NOT NULL,

    INDEX idx_order (order_id),
    INDEX idx_changed_at (changed_at),

    FOREIGN KEY (order_id) REFERENCES orders(id)
) ENGINE=InnoDB;
```

### 5. Data Types and Constraints

**Column Type Selection:**
```sql
-- Strings
name VARCHAR(255)         -- Variable length, max 255
description TEXT          -- Large text, no limit
code CHAR(10)            -- Fixed length
email VARCHAR(255)        -- Email addresses

-- Numbers
id INT                    -- Primary keys
quantity INT              -- Whole numbers
price DECIMAL(10,2)       -- Money (10 digits, 2 decimal)
percentage FLOAT          -- Floating point
big_number BIGINT        -- Large integers

-- Dates
created DATETIME          -- Date and time
birth_date DATE          -- Date only
start_time TIME          -- Time only
year YEAR                -- Year only

-- Binary
image BLOB               -- Binary data
file MEDIUMBLOB          -- Larger binary
document LONGBLOB        -- Very large binary

-- JSON (MySQL 5.7+)
settings JSON            -- Structured data
metadata JSON            -- Flexible schema
```

**Constraints:**
```sql
-- NOT NULL
email VARCHAR(255) NOT NULL

-- UNIQUE
email VARCHAR(255) UNIQUE

-- DEFAULT
status INT DEFAULT 1
created DATETIME DEFAULT CURRENT_TIMESTAMP

-- CHECK (MySQL 8.0+)
age INT CHECK (age >= 0 AND age <= 150)
status INT CHECK (status IN (1, 2, 3))

-- Foreign Key
FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE RESTRICT   -- Prevent deletion
    ON UPDATE CASCADE    -- Update child records
```

### 6. Index Design

**Index Types and Usage:**
```sql
-- Primary key (automatic unique index)
PRIMARY KEY (id)

-- Unique index
UNIQUE INDEX idx_email (email)

-- Composite index (order matters!)
INDEX idx_company_status (company_id, status)

-- Full-text index (for search)
FULLTEXT INDEX idx_description (description)

-- Spatial index (for geometry)
SPATIAL INDEX idx_location (location)
```

**Index Strategy:**
```sql
-- Frequent WHERE conditions
SELECT * FROM users WHERE company_id = ?;
-- Need: INDEX (company_id)

-- Sorting
SELECT * FROM orders ORDER BY created DESC;
-- Need: INDEX (created)

-- Joins
SELECT * FROM users u
JOIN orders o ON u.id = o.user_id;
-- Need: INDEX on orders(user_id)

-- Covering index (all data in index)
SELECT id, email FROM users WHERE company_id = ?;
-- Need: INDEX (company_id, id, email)
```

### 7. Migration Management

**Migration Naming Convention:**
```
YYYYMMDDHHMMSS_ActionDescription.php

Examples:
20240101120000_CreateUsersTable.php
20240102130000_AddEmailToUsers.php
20240103140000_AlterUsersAddIndex.php
20240104150000_DropOldUsersTable.php
```

**Migration Operations:**
```php
// Add column
$table->addColumn('new_field', 'string', [
    'after' => 'existing_field',
    'null' => true,
]);

// Modify column
$table->changeColumn('field_name', 'text', [
    'null' => false,
]);

// Remove column
$table->removeColumn('old_field');

// Add index
$table->addIndex(['field1', 'field2'], [
    'name' => 'idx_custom_name',
]);

// Remove index
$table->removeIndex(['field_name']);

// Add foreign key
$table->addForeignKey('user_id', 'users', 'id');

// Remove foreign key
$table->dropForeignKey('user_id');
```

### 8. Multi-Database Migration

**Database-Specific Migrations:**
```bash
# Directory structure (multi-tier pattern)
config/Migrations/
├── [ProjectDefault]/     # Project account database
├── [AppDefault]/         # Application account database
└── [AppClient]/          # Company-specific database (per-tenant)
```


**Migration with Database Context:**
```php
// [AppClient] migration (company-specific)
class CreateApplications extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('applications');

        // No company_id needed in company-specific DB
        $table->addColumn('user_id', 'integer')
              ->addColumn('status', 'integer');

        $table->create();
    }
}
```

## Database Patterns

### 1. Soft Delete Pattern
```sql
-- Add del_flg column
ALTER TABLE users ADD COLUMN del_flg INT DEFAULT 0;

-- Query active records
SELECT * FROM users WHERE del_flg = 0;

-- Soft delete
UPDATE users SET del_flg = 1, modified = NOW() WHERE id = ?;
```

### 2. Status Management Pattern
```sql
-- Status column with constants
CREATE TABLE applications (
    id INT PRIMARY KEY,
    status INT NOT NULL,
    -- 1: applying, 2: applied, 3: approved, 4: rejected
    CHECK (status IN (1, 2, 3, 4))
);

-- Query by status
SELECT * FROM applications
WHERE status = 1  -- Configure::read('Application.Status.applying')
```

### 3. Hierarchical Data Pattern
```sql
-- Self-referencing for tree structure
CREATE TABLE categories (
    id INT PRIMARY KEY,
    parent_id INT NULL,
    name VARCHAR(255),
    lft INT,  -- For nested set model
    rght INT,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);
```

### 4. Audit Trail Pattern
```sql
-- Separate audit table
CREATE TABLE audit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    model VARCHAR(100),
    foreign_key INT,
    action VARCHAR(20),
    user_id INT,
    change_data JSON,
    created DATETIME,
    INDEX idx_model_key (model, foreign_key)
);
```

## Performance Optimization

### 1. Query Optimization
```sql
-- Use EXPLAIN to analyze
EXPLAIN SELECT * FROM orders WHERE user_id = 1;

-- Optimize with proper index
CREATE INDEX idx_user_status ON orders(user_id, status);

-- Avoid SELECT *
SELECT id, name, email FROM users;  -- Better

-- Use LIMIT for pagination
SELECT * FROM orders LIMIT 20 OFFSET 40;
```

### 2. Table Optimization
```sql
-- Analyze table statistics
ANALYZE TABLE orders;

-- Optimize table (rebuild)
OPTIMIZE TABLE orders;

-- Check table health
CHECK TABLE orders;

-- Repair if needed
REPAIR TABLE orders;
```

### 3. Partitioning Strategy
```sql
-- Range partitioning by date
CREATE TABLE orders (
    id INT,
    order_date DATE,
    ...
) PARTITION BY RANGE (YEAR(order_date)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025)
);
```

## Output Examples

### Example 1: User Management Schema
```sql
-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    company_id INT NOT NULL,
    status INT DEFAULT 1,
    last_login DATETIME,
    login_count INT DEFAULT 0,
    del_flg INT DEFAULT 0,
    created DATETIME NOT NULL,
    modified DATETIME NOT NULL,

    INDEX idx_email (email),
    INDEX idx_company_status (company_id, status, del_flg),

    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (company_id) REFERENCES companys(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Example 2: Order System Schema
```sql
-- Orders master
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    total DECIMAL(10,2) DEFAULT 0.00,
    status INT DEFAULT 1,
    created DATETIME NOT NULL,

    INDEX idx_user (user_id),
    INDEX idx_created (created DESC),

    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order details
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,

    INDEX idx_order (order_id),

    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

## Best Practices

1. **Use InnoDB**: For transaction support and foreign keys
2. **UTF8MB4**: For full Unicode support including emoji
3. **Consistent Naming**: Use snake_case for tables and columns
4. **Add Indexes**: For WHERE, JOIN, ORDER BY columns
5. **Avoid NULLs**: When possible, use DEFAULT values
6. **Document Schema**: Comment complex relationships
7. **Version Control**: Track all migrations in Git

Remember: Database design is the foundation of application performance and data integrity.