---
name: relational-db-general
description: Principles for relational database design, including normalization, naming conventions, keys, and ACID compliance.
---

# General Relational Database Principles

This skill provides core guidelines for designing and interacting with relational databases (MySQL, PostgreSQL, etc.).

## When to use this skill
- Designing new database schemas (DDL).
- Reviewing or refactoring existing tables.
- Writing complex SQL queries that involve joins or transactions.
- troubleshooting data integrity issues.

## 1. Naming Conventions
- **Tables**: Plural_snake_case (e.g., `users`, `order_items`).
- **Columns**: snake_case (e.g., `is_active`, `created_at`).
- **Primary Keys**: `id` (or `product_id` if strictly required by convention, but `id` preferred for simplicity).
- **Foreign Keys**: `singular_table_name_id` (e.g., `user_id` references `users.id`).
- **Indexes**: `idx_table_columns`; **Unique**: `uniq_table_columns`.

## 2. Normalization Rules
- **1NF**: Atomic values, no repeating groups.
- **2NF**: No partial dependencies (all non-key columns depend on the full PK).
- **3NF**: No transitive dependencies (depend only on the key, nothing but the key).
- **Exceptions**: Denormalize only for proven performance bottlenecks (e.g., caching counts), and document widely.

## 3. Keys & Constraints
- **Primary Keys**: Always use a Primary Key (integer/bigint AUTO_INCREMENT or UUID).
- **Foreign Keys**: Enforce referential integrity at the database level (`ON DELETE RESTRICT` or `CASCADE`).
- **Unique Constraints**: Enforce uniqueness in DB, not just application code.
- **Not Null**: Default to `NOT NULL` unless optionality is strictly required.

## 4. ACID Compliance
- **Atomicity**: Wrap related writes in a Transaction (`BEGIN` ... `COMMIT`).
- **Consistency**: Data must meet validation rules at all times.
- **Isolation**: Understand isolation levels (e.g., Read Committed vs. Serializable).
- **Durability**: Committed data is permanent.

## 5. Performance Tips
- Index columns used in `WHERE`, `JOIN`, and `ORDER BY`.
- Avoid `SELECT *`.
- Use correct data types (e.g., `TINYINT` for booleans, `DECIMAL` for currency).
