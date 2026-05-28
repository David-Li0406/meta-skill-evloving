---
name: db-explore
description: Safe database exploration using Laravel Boost tools. Use for querying data, understanding schema, checking records, and debugging data issues. Auto-triggers on "query database", "check data", "find records", "database query", "show me the data".
---

# Database Exploration Guide

You are helping explore the RentPath database safely using Laravel Boost tools.

## Arguments

This skill accepts optional arguments to specify what to explore:

| Usage                                | Behavior                                 |
| ------------------------------------ | ---------------------------------------- |
| `/db-explore`                        | Show schema overview, common queries     |
| `/db-explore applications`           | Focus on applications table/model        |
| `/db-explore users with profiles`    | Explore users and related profile tables |
| `/db-explore Application::submitted` | Query applications with submitted status |
| `/db-explore "status = 'draft'"`     | Run specific condition                   |
| `/db-explore schema`                 | Show full database schema                |
| `/db-explore relationships`          | Map model relationships                  |

**Argument interpretation:**

- **Table/model name** - Focus exploration on that entity
- **Model::scope** - Use Eloquent scope to filter
- **Condition string** - Apply as WHERE clause
- **Keywords** (`schema`, `relationships`) - Specific exploration mode
- **Multiple tables** - Explore relationships between them

## Tools to Use

| Task              | Tool                                      | Why                             |
| ----------------- | ----------------------------------------- | ------------------------------- |
| View schema       | `laravel-boost` -> `database-schema`      | See tables, columns, indexes    |
| Run queries       | `laravel-boost` -> `database-query`       | Read-only SQL queries           |
| Execute PHP       | `laravel-boost` -> `tinker`               | Eloquent queries, complex logic |
| Check connections | `laravel-boost` -> `database-connections` | List available databases        |

## Quick Start

### 1. View Schema

Use the `database-schema` tool to see table structure:

- All tables and columns
- Data types and constraints
- Indexes and foreign keys
- Filter by table name if needed

### 2. Query Data

Use the `database-query` tool for read-only SQL:

```sql
-- Only SELECT, SHOW, EXPLAIN, DESCRIBE allowed
SELECT * FROM users LIMIT 10;
SHOW TABLES;
DESCRIBE applications;
EXPLAIN SELECT * FROM properties WHERE status = 'vacant';
```

### 3. Eloquent Queries

Use the `tinker` tool for complex queries:

```php
// Find specific records
User::find(1);
Application::where('status', 'submitted')->count();

// With relationships
Property::with('applications')->find(1);

// Complex queries
Application::query()
    ->where('status', 'submitted')
    ->whereHas('property', fn($q) => $q->where('visibility', 'public'))
    ->get();
```

## Key Tables Reference

### Core Entities

| Table               | Purpose         | Key Columns                                           |
| ------------------- | --------------- | ----------------------------------------------------- |
| `users`             | Authentication  | `id`, `email`, `first_name`, `last_name`              |
| `property_managers` | PM profiles     | `user_id`, `type`, `profile_verified_at`              |
| `tenant_profiles`   | Tenant profiles | `user_id`, `employment_status`, `profile_verified_at` |
| `properties`        | Listings        | `property_manager_id`, `status`, `visibility`         |
| `applications`      | Tenant apps     | `property_id`, `tenant_profile_id`, `status`          |

### Supporting Tables

| Table                       | Purpose       | Key Columns                                  |
| --------------------------- | ------------- | -------------------------------------------- |
| `application_co_signers`    | Co-signers    | `application_id`, `first_name`, `email`      |
| `application_guarantors`    | Guarantors    | `application_co_signer_id`, `relationship`   |
| `application_references`    | References    | `application_id`, `type`, `name`             |
| `application_invite_tokens` | Access tokens | `property_id`, `token`, `type`, `expires_at` |
| `leads`                     | Lead tracking | `property_id`, `email`, `status`, `source`   |
| `property_images`           | Photos        | `property_id`, `path`, `is_main`             |
| `conversations`             | Messaging     | `property_id`, participants                  |
| `messages`                  | Messages      | `conversation_id`, `content`, `sender_id`    |

## Common Queries

### User & Profile Queries

```sql
-- Find user with profiles
SELECT u.*, pm.id as pm_id, tp.id as tp_id
FROM users u
LEFT JOIN property_managers pm ON pm.user_id = u.id
LEFT JOIN tenant_profiles tp ON tp.user_id = u.id
WHERE u.email = 'test@example.com';

-- Count users by type
SELECT
    COUNT(DISTINCT pm.user_id) as property_managers,
    COUNT(DISTINCT tp.user_id) as tenants
FROM users u
LEFT JOIN property_managers pm ON pm.user_id = u.id
LEFT JOIN tenant_profiles tp ON tp.user_id = u.id;
```

**Tinker:**

```php
// User with all relationships
User::with(['propertyManager', 'tenantProfile'])->find(1);

// Find by email
User::where('email', 'test@example.com')->first();
```

### Property Queries

```sql
-- Properties by status
SELECT status, COUNT(*) as count
FROM properties
GROUP BY status;

-- Properties with application counts
SELECT p.id, p.title, COUNT(a.id) as app_count
FROM properties p
LEFT JOIN applications a ON a.property_id = p.id
GROUP BY p.id, p.title
ORDER BY app_count DESC
LIMIT 10;

-- Public vacant properties
SELECT id, title, rent_amount, rent_currency
FROM properties
WHERE status = 'vacant' AND visibility = 'public'
ORDER BY created_at DESC
LIMIT 20;
```

**Tinker:**

```php
// With eager loading
Property::with(['propertyManager.user', 'applications'])
    ->where('status', 'vacant')
    ->get();

// With counts
Property::withCount('applications')
    ->orderByDesc('applications_count')
    ->take(10)
    ->get();
```

### Application Queries

```sql
-- Applications by status
SELECT status, COUNT(*) as count
FROM applications
GROUP BY status
ORDER BY count DESC;

-- Recent applications
SELECT a.id, a.status, a.created_at, p.title, u.email
FROM applications a
JOIN properties p ON p.id = a.property_id
JOIN tenant_profiles tp ON tp.id = a.tenant_profile_id
JOIN users u ON u.id = tp.user_id
ORDER BY a.created_at DESC
LIMIT 20;

-- Application funnel
SELECT
    COUNT(*) as total,
    SUM(CASE WHEN status = 'draft' THEN 1 ELSE 0 END) as draft,
    SUM(CASE WHEN status = 'submitted' THEN 1 ELSE 0 END) as submitted,
    SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved,
    SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected
FROM applications;
```

**Tinker:**

```php
// Full application with relationships
Application::with([
    'property',
    'tenantProfile.user',
    'coSigners.guarantors',
    'references'
])->find(1);

// Status distribution
Application::query()
    ->selectRaw('status, count(*) as count')
    ->groupBy('status')
    ->pluck('count', 'status');
```

### Lead Queries

```sql
-- Lead funnel by source
SELECT source, status, COUNT(*) as count
FROM leads
GROUP BY source, status
ORDER BY source, status;

-- Conversion rate
SELECT
    COUNT(*) as total_leads,
    SUM(CASE WHEN status = 'applied' THEN 1 ELSE 0 END) as converted,
    ROUND(SUM(CASE WHEN status = 'applied' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as conversion_rate
FROM leads;
```

### Token Queries

```sql
-- Active tokens
SELECT t.*, p.title
FROM application_invite_tokens t
JOIN properties p ON p.id = t.property_id
WHERE t.expires_at > NOW() OR t.expires_at IS NULL;

-- Token usage
SELECT type, COUNT(*) as count, SUM(use_count) as total_uses
FROM application_invite_tokens
GROUP BY type;
```

## Debugging Queries

### Check Data Integrity

```sql
-- Orphaned applications (no property)
SELECT a.id FROM applications a
LEFT JOIN properties p ON p.id = a.property_id
WHERE p.id IS NULL;

-- Users without profiles
SELECT u.id, u.email
FROM users u
LEFT JOIN property_managers pm ON pm.user_id = u.id
LEFT JOIN tenant_profiles tp ON tp.user_id = u.id
WHERE pm.id IS NULL AND tp.id IS NULL;
```

### Check Recent Activity

```sql
-- Recent registrations
SELECT id, email, created_at
FROM users
ORDER BY created_at DESC
LIMIT 10;

-- Recent applications
SELECT id, status, created_at, updated_at
FROM applications
ORDER BY updated_at DESC
LIMIT 10;
```

## Safety Guidelines

1. **Read-only**: `database-query` only allows SELECT, SHOW, EXPLAIN, DESCRIBE
2. **Use LIMIT**: Always limit result sets to avoid overwhelming output
3. **Prefer Tinker for writes**: If you need to modify data, use Tinker with explicit user approval
4. **No production data exposure**: Be careful not to expose sensitive data in responses

## Documentation References

- `docs/modules/users.md` - User/profile schema
- `docs/modules/properties.md` - Property schema
- `docs/modules/applications.md` - Application schema
- `docs/modules/leads.md` - Lead schema
- `docs/modules/tokens.md` - Token schema
