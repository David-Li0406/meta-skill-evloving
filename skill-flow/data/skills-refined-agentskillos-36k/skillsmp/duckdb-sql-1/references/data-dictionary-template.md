# Data Dictionary Template

Use this structure when generating `data_dictionary.md`.

---

## Header Section

```markdown
# Data Dictionary

**Version:** 1.0
**Generated:** YYYY-MM-DD
**Source Files:** data/sales.ddb, data/inventory.ddb

## Table of Contents

### By Domain
- **sales**: Order processing and transactions
  - [customers](#customers)
  - [orders](#orders)
- **inventory**: Product and stock management
  - [products](#products)
  - [stock](#stock)

### All Tables
- [customers](#customers)
- [orders](#orders)
- [products](#products)
- [stock](#stock)
```

---

## Domain Overview Section

```markdown
## Domains Overview

### Sales
Order processing and transactions.

**Tables:** `customers`, `orders`, `order_items`

### Inventory
Product and stock management.

**Tables:** `products`, `stock`, `warehouses`
```

---

## Table Entry Template

For each table, include ALL of these sections:

```markdown
### tablename

**Purpose:** What this table stores and why it exists.

**Source file:** data/sales.ddb

**Also known as:** synonyms users might use (e.g., "transactions", "purchases")

**Relationships:**
- Belongs to customer (customers.customer_id)
- Has many order_items (order_items.order_id)

**Important Query Patterns:**
- Active orders: `WHERE status != 'cancelled'`
- Recent orders: `WHERE order_date >= current_date - INTERVAL '30 days'`

**Fields:**

| Field | Type | Purpose | Notes |
|-------|------|---------|-------|
| order_id | INTEGER | Primary key | Auto-increment |
| customer_id | INTEGER | Foreign key to customers | Required |
| order_date | DATE | When order was placed | |
| status | VARCHAR | Order status | Enum: see below |
| total_amount | DECIMAL(10,2) | Order total | |

**Enum Values:**

*status:*
- `pending` - Order received, not yet processed
- `processing` - Order being prepared
- `shipped` - Order sent to customer
- `delivered` - Order received by customer
- `cancelled` - Order cancelled
```
