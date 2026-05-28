# Data Model: Admin Dashboard

## Overview
This document defines the database schema for the admin dashboard feature, including the new Admin model and modifications to existing models for enhanced querying and pagination.

## New Tables

### admins

**Purpose**: Store admin user credentials for dashboard authentication.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY, AUTO INCREMENT | Unique identifier |
| username | string | NOT NULL, UNIQUE | Admin login username |
| password_digest | string | NOT NULL | Bcrypt hashed password |
| created_at | datetime | NOT NULL | Record creation timestamp |
| updated_at | datetime | NOT NULL | Last update timestamp |

**Indexes**:
- `PRIMARY KEY (id)`
- `UNIQUE INDEX idx_admins_username ON admins(username)`

**Validations**:
- username: presence, uniqueness, length 3-50 characters
- password: length minimum 8 characters (on creation/update)

**Sample Data**:
```sql
INSERT INTO admins (username, password_digest, created_at, updated_at) VALUES
  ('admin', '$2a$12$hashed_password_here', NOW(), NOW()),
  ('testadmin', '$2a$12$hashed_password_here', NOW(), NOW());
```

**Notes**:
- No foreign key relationships (admins don't "own" resources)
- Password stored as bcrypt hash via Rails `has_secure_password`
- No email field in v1 (added in future for password reset)
- No role/permission field (all admins have full access)

---

## Modified Tables

### coupon_codes

**Purpose**: Store promotional coupon codes with new auto-generated format.

**Existing Schema**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY, AUTO INCREMENT | Unique identifier |
| code | string | NOT NULL, UNIQUE | Coupon code text |
| usage | string | NOT NULL | Enum: 'unused' or 'used' |
| created_at | datetime | NOT NULL | Record creation timestamp |
| updated_at | datetime | NOT NULL | Last update timestamp |

**New Indexes** (to be added):
- `INDEX idx_coupon_codes_usage ON coupon_codes(usage)` - For filtering by status
- Existing: `UNIQUE INDEX idx_coupon_codes_code ON coupon_codes(code)`
- Existing: `PRIMARY KEY (id)`

**Modified Validations**:
- code: format must match `/\ASK\d+[A-Z]{3}\z/` (e.g., SK187524MYQ)
- usage: must be 'unused' or 'used'

**New Sample Data Format**:
```sql
-- Old format (TEST1, USED001, etc.) replaced with:
INSERT INTO coupon_codes (code, usage, created_at, updated_at) VALUES
  ('SK1000AAA', 'unused', NOW(), NOW()),
  ('SK1001BBB', 'unused', NOW(), NOW()),
  ('SK1002CCC', 'unused', NOW(), NOW()),
  ('SK1003DDD', 'used', NOW(), NOW()),
  ('SK1004EEE', 'used', NOW(), NOW()),
  ('SK1005FFF', 'used', NOW(), NOW()),
  ('SK1006GGG', 'used', NOW(), NOW()),
  ('SK1007HHH', 'used', NOW(), NOW());
```

**Code Generation Logic**:
1. Extract all integers from existing codes: `SK1000AAA` → `1000`
2. Find maximum: `max(1000, 1001, 1002, ...) = 1007`
3. Increment: `1007 + 1 = 1008`
4. Generate 3 random uppercase letters: `XYZ`
5. Concatenate: `SK1008XYZ`
6. If no codes exist, start at `SK1000AAA`

**Deletion Rules**:
- CAN delete if `usage = 'unused'` AND no associated orders
- CANNOT delete if `usage = 'used'` OR has associated order
- Model callback `before_destroy :check_not_used` enforces this

**Associations**:
- `has_many :orders` (implicit through foreign key in orders table)

---

### orders

**Purpose**: Store customer fitness kit orders.

**Existing Schema** (no structural changes):
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY, AUTO INCREMENT | Unique identifier |
| promise_fitness_kit_id | integer | NOT NULL, FOREIGN KEY | Reference to fitness kit |
| coupon_code_id | integer | NOT NULL, FOREIGN KEY | Reference to coupon code |
| first_name | string | NOT NULL | Customer first name |
| last_name | string | NOT NULL | Customer last name |
| address1 | string | NOT NULL | Primary address line |
| address2 | string | NULL | Secondary address line |
| city | string | NOT NULL | City |
| state | string | NOT NULL | State/province |
| zip | string | NOT NULL | Postal code |
| phone | string | NOT NULL | Contact phone |
| email | string | NOT NULL | Contact email |
| description | text | NULL | Special delivery instructions |
| created_at | datetime | NOT NULL | Order timestamp |
| updated_at | datetime | NOT NULL | Last update timestamp |

**New Indexes** (to be added):
- `INDEX idx_orders_created_at ON orders(created_at)` - For sorting newest first
- `INDEX idx_orders_created_at_id ON orders(created_at, id)` - Composite for cursor pagination
- Existing: Foreign key indexes on `promise_fitness_kit_id`, `coupon_code_id`

**Associations**:
- `belongs_to :promise_fitness_kit`
- `belongs_to :coupon_code`

**Scopes**:
- `newest_first` - `ORDER BY created_at DESC`
- `by_cursor(cursor, direction)` - For pagination

**Search Fields**:
- `first_name LIKE '%term%'`
- `last_name LIKE '%term%'`
- `email LIKE '%term%'`
- `coupon_codes.code LIKE '%term%'` (via JOIN)

**Notes**:
- Orders are READ-ONLY in admin interface (no create/update/delete)
- Cursor pagination uses `created_at` + `id` for deterministic ordering
- Search requires JOIN with coupon_codes table

---

## Relationships Diagram

```
┌─────────────────┐
│     admins      │
│─────────────────│
│ id (PK)         │
│ username        │
│ password_digest │
└─────────────────┘
     (no FK relationships)


┌─────────────────────┐         ┌──────────────────────┐
│   coupon_codes      │         │ promise_fitness_kits │
│─────────────────────│         │──────────────────────│
│ id (PK)             │         │ id (PK)              │
│ code (UNIQUE)       │◄────┐   │ name                 │◄────┐
│ usage               │     │   │ description          │     │
└─────────────────────┘     │   │ slug (UNIQUE)        │     │
                            │   └──────────────────────┘     │
                            │                                │
                            │                                │
                     ┌──────┴──────────────────┐            │
                     │       orders            │            │
                     │─────────────────────────│            │
                     │ id (PK)                 │            │
                     │ coupon_code_id (FK)     ├────────────┘
                     │ promise_fitness_kit_id  ├────────────┘
                     │ first_name              │
                     │ last_name               │
                     │ email                   │
                     │ address1, address2      │
                     │ city, state, zip        │
                     │ phone                   │
                     │ description             │
                     │ created_at              │
                     └─────────────────────────┘
```

---

## Migration Files

### 1. CreateAdmins

```ruby
class CreateAdmins < ActiveRecord::Migration[8.0]
  def change
    create_table :admins do |t|
      t.string :username, null: false
      t.string :password_digest, null: false
      t.timestamps
    end
    
    add_index :admins, :username, unique: true
  end
end
```

### 2. AddIndexesToCouponCodes

```ruby
class AddIndexesToCouponCodes < ActiveRecord::Migration[8.0]
  def change
    add_index :coupon_codes, :usage unless index_exists?(:coupon_codes, :usage)
  end
end
```

### 3. AddIndexesToOrdersForPagination

```ruby
class AddIndexesToOrdersForPagination < ActiveRecord::Migration[8.0]
  def change
    add_index :orders, :created_at unless index_exists?(:orders, :created_at)
    add_index :orders, [:created_at, :id], name: 'index_orders_on_created_at_and_id' unless index_exists?(:orders, [:created_at, :id])
  end
end
```

---

## Query Patterns

### Admin Authentication
```sql
-- Find admin by username
SELECT * FROM admins WHERE username = 'admin' LIMIT 1;

-- Verify session (by ID in session cookie)
SELECT * FROM admins WHERE id = 123 LIMIT 1;
```

### Coupon Code Management
```sql
-- List all coupons with filter
SELECT * FROM coupon_codes 
WHERE usage = 'unused' 
ORDER BY id 
LIMIT 26;  -- 25 + 1 for has_more check

-- List coupons with cursor pagination (next page)
SELECT * FROM coupon_codes 
WHERE id > 150  -- cursor from last record
ORDER BY id 
LIMIT 26;

-- List coupons with cursor pagination (previous page)
SELECT * FROM coupon_codes 
WHERE id < 100  -- cursor from first record
ORDER BY id DESC 
LIMIT 26;

-- Search coupons
SELECT * FROM coupon_codes 
WHERE code LIKE '%SK1000%' 
ORDER BY id 
LIMIT 26;

-- Generate next code (find max integer)
SELECT code FROM coupon_codes 
WHERE code LIKE 'SK%' 
ORDER BY CAST(SUBSTR(code, 3, LENGTH(code) - 5) AS INTEGER) DESC 
LIMIT 1;
-- Result: SK1007HHH → extract 1007 → increment to 1008
```

### Order Management
```sql
-- List orders with pagination (newest first)
SELECT orders.*, promise_fitness_kits.name AS kit_name, coupon_codes.code AS coupon_code
FROM orders
INNER JOIN promise_fitness_kits ON orders.promise_fitness_kit_id = promise_fitness_kits.id
INNER JOIN coupon_codes ON orders.coupon_code_id = coupon_codes.id
ORDER BY orders.created_at DESC, orders.id DESC
LIMIT 26;

-- List orders with cursor (next page)
SELECT orders.*, promise_fitness_kits.name, coupon_codes.code
FROM orders
INNER JOIN promise_fitness_kits ON orders.promise_fitness_kit_id = promise_fitness_kits.id
INNER JOIN coupon_codes ON orders.coupon_code_id = coupon_codes.id
WHERE orders.created_at < '2025-01-08 10:00:00'  -- timestamp from cursor record
ORDER BY orders.created_at DESC, orders.id DESC
LIMIT 26;

-- Search orders
SELECT orders.*, promise_fitness_kits.name, coupon_codes.code
FROM orders
INNER JOIN promise_fitness_kits ON orders.promise_fitness_kit_id = promise_fitness_kits.id
INNER JOIN coupon_codes ON orders.coupon_code_id = coupon_codes.id
WHERE orders.first_name LIKE '%John%' 
   OR orders.last_name LIKE '%John%'
   OR orders.email LIKE '%John%'
   OR coupon_codes.code LIKE '%John%'
ORDER BY orders.created_at DESC
LIMIT 26;

-- Dashboard stats
SELECT COUNT(*) FROM orders;

SELECT promise_fitness_kits.name, COUNT(orders.id) AS order_count
FROM orders
INNER JOIN promise_fitness_kits ON orders.promise_fitness_kit_id = promise_fitness_kits.id
GROUP BY promise_fitness_kits.name;

SELECT COUNT(*) FROM coupon_codes WHERE usage = 'unused';
```

---

## Data Integrity Rules

### 1. Coupon Code Deletion Protection
- **Rule**: Cannot delete coupon codes that are referenced by orders
- **Enforcement**: Model callback `before_destroy :check_not_used`
- **Behavior**: Throws `:abort` and adds error to model

### 2. Coupon Code Format
- **Rule**: Must match pattern `SK\d+[A-Z]{3}`
- **Enforcement**: Model validation with regex
- **Example Valid**: SK1000AAA, SK187524MYQ, SK999999ZZZ
- **Example Invalid**: TEST1, sk1000aaa, SK1000AA, 1000AAA

### 3. Username Uniqueness
- **Rule**: Admin usernames must be unique (case-sensitive)
- **Enforcement**: Database unique index + model validation
- **Behavior**: Save fails with validation error

### 4. Password Security
- **Rule**: Passwords must be at least 8 characters
- **Enforcement**: Model validation via `has_secure_password`
- **Storage**: bcrypt hash with cost factor 12

### 5. Order Immutability (Admin Context)
- **Rule**: Admins can only VIEW orders, not modify or delete
- **Enforcement**: Controller only defines `index` and `show` actions
- **Reasoning**: Orders are business records, should not be altered

---

## Performance Optimization

### Index Strategy

1. **admins.username** (unique): Fast login lookup
2. **coupon_codes.usage**: Filter by unused/used without table scan
3. **coupon_codes.code** (unique): Fast search and uniqueness check
4. **orders.created_at**: Fast sorting for newest-first display
5. **orders.[created_at, id]**: Composite index for cursor pagination
6. **Foreign keys**: Auto-indexed by Rails (promise_fitness_kit_id, coupon_code_id)

### Query Optimization

- **Eager Loading**: Use `includes(:promise_fitness_kit, :coupon_code)` to prevent N+1
- **Cursor Pagination**: More efficient than OFFSET for large datasets
- **Limit + 1**: Fetch one extra record to determine if more pages exist
- **Index Coverage**: All WHERE, ORDER BY, and JOIN columns are indexed

### Expected Performance

- Admin login: < 10ms
- Coupon list (25 records): < 20ms
- Order list (25 records with joins): < 30ms
- Search queries: < 50ms (depends on result set size)
- Dashboard stats: < 50ms (simple aggregations)

---

## Data Migration Strategy

### Development Environment
1. Run migrations to create `admins` table and add indexes
2. Update seeds to create admin users with new coupon format
3. Clear existing test coupons, create new format codes
4. Update existing orders to reference new coupon codes

### Production Environment (Future)
1. Run migrations (non-destructive, only adds table/indexes)
2. Create admin users via Rails console (don't commit passwords to seeds)
3. **Decision**: Keep old coupon codes for historical orders OR migrate to new format
4. If migrating codes:
   - Create mapping: OLD_CODE → NEW_FORMAT
   - Update orders.coupon_code_id references
   - Deactivate/delete old codes
5. Generate new codes going forward in new format

### Rollback Plan
- Drop `admins` table
- Remove new indexes on `coupon_codes` and `orders`
- Restore old coupon code format (if migrated)
- All reversible via `rails db:rollback`

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-08  
**Dependencies**: Existing schema from specs 001-003