# Data Model: Fitness Kit Ordering System

**Feature ID**: 001-fitness-kit-ordering  
**Last Updated**: 2025-01-XX

---

## Entity Relationship Diagram

```
┌─────────────────────────┐
│   PromiseFitnessKit     │
├─────────────────────────┤
│ id (PK)                 │
│ name                    │
│ description             │
│ created_at              │
│ updated_at              │
└─────────────────────────┘
           │
           │ has_many
           │
           ▼
┌─────────────────────────┐
│        Order            │
├─────────────────────────┤
│ id (PK)                 │
│ promise_fitness_kit_id  │──┐
│ coupon_code_id          │──┼─┐
│ order_confirmation      │  │ │
│ first_name              │  │ │
│ last_name               │  │ │
│ address1                │  │ │
│ address2                │  │ │
│ city                    │  │ │
│ state                   │  │ │
│ zip                     │  │ │
│ phone                   │  │ │
│ email                   │  │ │
│ description             │  │ │
│ created_at              │  │ │
│ updated_at              │  │ │
└─────────────────────────┘  │ │
           ▲                 │ │
           │ belongs_to      │ │
           └─────────────────┘ │
                               │
           ┌───────────────────┘
           │ belongs_to
           │
           ▼
┌─────────────────────────┐
│      CouponCode         │
├─────────────────────────┤
│ id (PK)                 │
│ code                    │
│ usage                   │
│ created_at              │
│ updated_at              │
└─────────────────────────┘
           │
           │ has_many
           │
           ▼
```

**Relationships:**
- One `PromiseFitnessKit` can have many `Orders`
- One `CouponCode` can have many `Orders` (but only one with usage='used')
- One `Order` belongs to one `PromiseFitnessKit`
- One `Order` belongs to one `CouponCode`

---

## Table Schemas

### promise_fitness_kits

| Column      | Type     | Null | Default | Constraints       | Description                    |
|-------------|----------|------|---------|-------------------|--------------------------------|
| id          | integer  | NO   | -       | PRIMARY KEY       | Auto-incrementing ID           |
| name        | string   | NO   | -       | UNIQUE            | Kit name (also serves as SKU)  |
| description | text     | NO   | -       | -                 | Full product description       |
| created_at  | datetime | NO   | -       | -                 | Record creation timestamp      |
| updated_at  | datetime | NO   | -       | -                 | Record update timestamp        |

**Indexes:**
- PRIMARY KEY: `id`
- UNIQUE INDEX: `name`

**Foreign Keys:**
- None

**Constraints:**
- `name` must be present and unique
- `description` must be present

---

### coupon_codes

| Column     | Type     | Null | Default  | Constraints           | Description                           |
|------------|----------|------|----------|-----------------------|---------------------------------------|
| id         | integer  | NO   | -        | PRIMARY KEY           | Auto-incrementing ID                  |
| code       | string   | NO   | -        | UNIQUE                | Coupon code (e.g., "WELCOME2024")     |
| usage      | string   | NO   | 'unused' | CHECK IN              | Status: "unused" or "used"            |
| created_at | datetime | NO   | -        | -                     | Record creation timestamp             |
| updated_at | datetime | NO   | -        | -                     | Record update timestamp               |

**Indexes:**
- PRIMARY KEY: `id`
- UNIQUE INDEX: `code`

**Foreign Keys:**
- None

**Constraints:**
- `code` must be present and unique (case-insensitive validation in model)
- `usage` must be either "unused" or "used" (CHECK constraint)
- Default value for `usage` is "unused"

**Business Rules:**
- Codes are normalized to uppercase before saving
- Once marked as "used", cannot be reused
- Must remain "unused" to be valid for new orders

---

### orders

| Column                  | Type     | Null | Default | Constraints              | Description                                |
|-------------------------|----------|------|---------|--------------------------|-------------------------------------------|
| id                      | integer  | NO   | -       | PRIMARY KEY              | Auto-incrementing ID                      |
| promise_fitness_kit_id  | integer  | NO   | -       | FOREIGN KEY              | Reference to promise_fitness_kits.id      |
| coupon_code_id          | integer  | NO   | -       | FOREIGN KEY              | Reference to coupon_codes.id              |
| order_confirmation      | integer  | NO   | -       | UNIQUE                   | 6-digit confirmation number (e.g., 000001)|
| first_name              | string   | NO   | -       | -                        | Customer first name                       |
| last_name               | string   | NO   | -       | -                        | Customer last name                        |
| address1                | string   | NO   | -       | -                        | Primary street address                    |
| address2                | string   | YES  | NULL    | -                        | Secondary address (apt, suite)            |
| city                    | string   | NO   | -       | -                        | City name                                 |
| state                   | string   | NO   | -       | LENGTH = 2               | 2-letter US state code (uppercase)        |
| zip                     | string   | NO   | -       | -                        | ZIP code (5-digit or ZIP+4)               |
| phone                   | string   | NO   | -       | LENGTH = 10              | Phone number (10 digits, no formatting)   |
| email                   | string   | NO   | -       | -                        | Customer email address                    |
| description             | text     | YES  | NULL    | -                        | Optional order notes                      |
| created_at              | datetime | NO   | -       | -                        | Record creation timestamp                 |
| updated_at              | datetime | NO   | -       | -                        | Record update timestamp                   |

**Indexes:**
- PRIMARY KEY: `id`
- UNIQUE INDEX: `order_confirmation`
- INDEX: `promise_fitness_kit_id`
- INDEX: `coupon_code_id`
- INDEX: `email`
- INDEX: `created_at`

**Foreign Keys:**
- `promise_fitness_kit_id` → `promise_fitness_kits.id`
  - ON DELETE: RESTRICT (cannot delete kit with orders)
- `coupon_code_id` → `coupon_codes.id`
  - ON DELETE: RESTRICT (cannot delete coupon with orders)

**Constraints:**
- All required fields must be present (see Null column)
- `state` must be exactly 2 characters (validated in model against US states)
- `phone` must be exactly 10 characters (validated in model)
- `zip` must match format: 5 digits or ZIP+4 (validated in model)
- `email` must be valid email format (validated in model)
- `order_confirmation` must be unique and auto-generated
- `coupon_code_id` must reference an unused coupon at creation time

**Business Rules:**
- `order_confirmation` auto-generated sequentially (1, 2, 3...)
- Displayed to users with leading zeros (000001, 000002, 000003...)
- `phone` accepts dashes in form input but stores only digits
- `email` normalized to lowercase
- `state` normalized to uppercase
- On successful creation, associated coupon's usage changes to "used"
- Creation is transactional: if order fails, coupon remains "unused"

---

## Data Types and Storage

### String vs Text
- **string**: Variable-length, indexed, max ~255 chars
  - Used for: names, codes, single-line addresses, phone, email, state, zip
- **text**: Large text fields, not typically indexed
  - Used for: kit descriptions, order notes

### Integer vs String for IDs
- **integer**: Used for all primary keys and foreign keys (Rails default)
- **order_confirmation**: Integer for efficient querying and sorting
  - Stored as integer, formatted for display with leading zeros

### Phone Number Storage
- **Type**: string (10 characters)
- **Storage**: Digits only (e.g., "4155551234")
- **Display**: Formatted as "(415) 555-1234"
- **Rationale**: String preserves potential leading zeros, fixed length for validation

### ZIP Code Storage
- **Type**: string
- **Storage**: With or without dash (e.g., "94102" or "94102-1234")
- **Rationale**: Preserves leading zeros (e.g., "02134" in Massachusetts)

---

## Migration Order

Execute in this order to satisfy foreign key constraints:

1. **create_promise_fitness_kits** (no dependencies)
2. **create_coupon_codes** (no dependencies)
3. **create_orders** (depends on promise_fitness_kits and coupon_codes)

---

## Sample Data Structure

### Fitness Kits (3 records)
```ruby
[
  { id: 1, name: "Beginner Strength Kit", description: "Perfect for..." },
  { id: 2, name: "Cardio Endurance Kit", description: "Boost your..." },
  { id: 3, name: "Flexibility & Recovery Kit", description: "Essential tools..." }
]
```

### Coupon Codes (10 records)
```ruby
[
  { id: 1, code: "WELCOME2024", usage: "unused" },
  { id: 2, code: "FITNESS50", usage: "unused" },
  { id: 3, code: "NEWYEAR", usage: "unused" },
  { id: 4, code: "SPRING25", usage: "unused" },
  { id: 5, code: "HEALTH100", usage: "unused" },
  { id: 6, code: "USED001", usage: "used" },
  { id: 7, code: "USED002", usage: "used" },
  { id: 8, code: "USED003", usage: "used" },
  { id: 9, code: "USED004", usage: "used" },
  { id: 10, code: "USED005", usage: "used" }
]
```

### Orders (5 records)
```ruby
[
  {
    id: 1,
    promise_fitness_kit_id: 1,
    coupon_code_id: 6,
    order_confirmation: 1, # Displayed as "000001"
    first_name: "John",
    last_name: "Doe",
    address1: "123 Main St",
    address2: nil,
    city: "San Francisco",
    state: "CA",
    zip: "94102",
    phone: "4155551234",
    email: "john.doe@example.com",
    description: nil
  },
  # ... 4 more orders
]
```

---

## Query Patterns

### Common Queries

**Find all available fitness kits:**
```ruby
PromiseFitnessKit.ordered_by_name
# SELECT * FROM promise_fitness_kits ORDER BY name
```

**Find unused coupon codes:**
```ruby
CouponCode.unused
# SELECT * FROM coupon_codes WHERE usage = 'unused'
```

**Find order by confirmation number:**
```ruby
Order.find_by(order_confirmation: 1)
# SELECT * FROM orders WHERE order_confirmation = 1 LIMIT 1
```

**Get order with related data (prevent N+1):**
```ruby
Order.includes(:promise_fitness_kit, :coupon_code).find(params[:id])
# SELECT * FROM orders WHERE id = ?
# SELECT * FROM promise_fitness_kits WHERE id IN (?)
# SELECT * FROM coupon_codes WHERE id IN (?)
```

**Recent orders:**
```ruby
Order.recent.includes(:promise_fitness_kit)
# SELECT * FROM orders ORDER BY created_at DESC
```

**Validate coupon availability:**
```ruby
CouponCode.find_by(code: "WELCOME2024", usage: "unused")
# SELECT * FROM coupon_codes WHERE code = 'WELCOME2024' AND usage = 'unused' LIMIT 1
```

---

## Database Performance Considerations

### Indexes
- **promise_fitness_kits.name**: UNIQUE index for fast lookups and prevent duplicates
- **coupon_codes.code**: UNIQUE index for fast validation and prevent duplicates
- **orders.order_confirmation**: UNIQUE index for fast lookups by confirmation number
- **orders.promise_fitness_kit_id**: Index for joins and associations
- **orders.coupon_code_id**: Index for joins and associations
- **orders.email**: Index for potential admin searches
- **orders.created_at**: Index for sorting recent orders

### Query Optimization
- Use `includes()` to eager load associations
- Use `find_by()` instead of `where().first` for single record lookups
- Use database-level constraints to enforce data integrity
- Use scopes for reusable query patterns

### Concurrent Access
- **Order Confirmation Generation**: Use database transaction with lock to prevent duplicate numbers
- **Coupon Usage**: Use optimistic locking or transaction to prevent race conditions
- **Foreign Key Constraints**: Database enforces referential integrity

---

## Data Integrity Rules

### Database Level
1. NOT NULL constraints on required fields
2. UNIQUE constraints on `name`, `code`, `order_confirmation`
3. CHECK constraint on `usage` enum values
4. FOREIGN KEY constraints with RESTRICT on delete
5. Indexes for query performance and uniqueness

### Application Level (Model Validations)
1. Presence validations
2. Format validations (email, phone, zip)
3. Length validations (state = 2, phone = 10)
4. Inclusion validations (state in US_STATES list, usage in enum)
5. Custom validations (coupon must be unused)
6. Callbacks for normalization and auto-generation

### Transactional Integrity
- Order creation and coupon marking wrapped in database transaction
- If order creation fails, coupon remains "unused"
- If coupon marking fails, order creation rolls back
- Atomic order confirmation number generation

---

## Schema Version Control

All schema changes tracked via Rails migrations:
- Timestamped migration files
- Reversible migrations (up/down methods)
- Schema.rb represents current database state
- Never modify existing migrations after merge to main

---

## Backup and Recovery Considerations

- **SQLite Database File**: Single file (`db/production.sqlite3`)
- **Backup Strategy**: Regular file-system backups of database file
- **Point-in-Time Recovery**: Not natively supported in SQLite
- **Migration to PostgreSQL**: Consider for high-traffic production use

---

## Data Validation Summary

| Field                   | Required | Format/Rules                              |
|-------------------------|----------|-------------------------------------------|
| kit.name                | Yes      | Unique, any string                        |
| kit.description         | Yes      | Any text                                  |
| coupon.code             | Yes      | Unique, uppercase, alphanumeric           |
| coupon.usage            | Yes      | "unused" or "used"                        |
| order.first_name        | Yes      | Any string                                |
| order.last_name         | Yes      | Any string                                |
| order.address1          | Yes      | Any string                                |
| order.address2          | No       | Any string                                |
| order.city              | Yes      | Any string                                |
| order.state             | Yes      | 2-letter US state code                    |
| order.zip               | Yes      | 12345 or 12345-6789                       |
| order.phone             | Yes      | Exactly 10 digits                         |
| order.email             | Yes      | Valid email format                        |
| order.description       | No       | Any text                                  |
| order.order_confirmation| Yes      | Auto-generated, unique integer            |

---

**Status**: Complete  
**Ready for Implementation**: Yes