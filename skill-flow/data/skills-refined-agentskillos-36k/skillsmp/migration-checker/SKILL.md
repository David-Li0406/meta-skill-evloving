---
name: migration-checker
description: Validates CakePHP migration files and ensures consistency between migrations, fixtures, and database schemas in multi-database environments
---

# CakePHP Migration Checker

A specialized skill for validating CakePHP migration files and ensuring schema consistency across migrations, fixtures, and actual database schemas.

## Core Validation Areas

### 1. Migration File Structure Validation

**Check migration files for:**
- Proper namespace structure
- Table creation/modification syntax
- Column definitions with correct types
- Index and foreign key definitions

**Migration namespace structure** (multi-tier pattern):
```
config/Migrations/
├── [ProjectDefault]/    # Project account schema
├── [AppDefault]/        # Application account schema
└── [AppClient]/         # Application client schema (multi-tenant)
```


### 2. Migration-Fixture Consistency

**Validate that fixtures match migration schemas:**
- All migration columns exist in fixtures
- Fixture column types match migration definitions
- Required (NOT NULL) columns have values
- Foreign key references are valid

**Example validation:**
```php
// Migration defines:
$table->addColumn('login_name', 'text', ['null' => false]);

// Fixture must have:
'login_name' => 'test_user',  // NOT NULL, so value required
```

### 3. Multi-Tenant Database Patterns

**For multi-tenant projects:**
- Database naming pattern: `[app_prefix]_company_%d`
- Connection pattern validation
- Dynamic connection component usage

**Check for correct patterns:**
```php
// ✅ CORRECT: Dynamic connection
$conn = $this->MessageDeliveryDbAccessor->getUserMessageDeliveryDbConnection($companyId);

// ❌ WRONG: Hardcoded database name
$conn = ConnectionManager::get('[app_prefix]_company_9999');
```


### 4. Schema Cache Management

**Detect when schema cache clearing is needed:**
- After migration modifications
- When fixture-migration mismatches occur
- Following database structure changes

**Suggest cache clearing:**
```bash
rm -rf tmp/cache/models/*
```

### 5. Test Database Configuration

**Validate test database setup:**
- Test database naming conventions
- Proper fixture namespacing
- Connection configuration

**Expected test databases:**
```
test_default_test_session_001  # Account schema
test_client_9999001            # Client schema
test_account                   # Core account
```

## Validation Process

When checking migrations:

1. **Parse migration files** - Extract table and column definitions
2. **Locate corresponding fixtures** - Find fixtures for same tables
3. **Compare schemas** - Identify mismatches
4. **Check multi-tenant patterns** - Validate dynamic connections
5. **Verify test setup** - Ensure test databases configured

## Output Format

```
Migration: [Migration file path]
Table: [Table name]
Status: [✅ CONSISTENT | ❌ INCONSISTENT | ⚠️ WARNING]

Issues found:
- Missing in fixture: [column_name]
- Type mismatch: [column] expects [type1], fixture has [type2]
- Null constraint violation: [column]

Recommendations:
- Clear schema cache: rm -rf tmp/cache/models/*
- Update fixture: [specific changes needed]
```

## Examples

### Example 1: Column missing in fixture
```
Migration: config/Migrations/[AppClient]/20210201000000_ClientInitial.php
Table: applications
Status: ❌ INCONSISTENT

Issues found:
- Missing in fixture: approved_at
- Missing in fixture: approved_by

Recommendations:
- Add to ApplicationsFixture.php:
  'approved_at' => null,
  'approved_by' => null,
```

### Example 2: Type mismatch
```
Migration: config/Migrations/[AppDefault]/20210201000000_DefaultInitial.php
Table: company_users
Status: ❌ INCONSISTENT

Issues found:
- Type mismatch: login_name expects TEXT, fixture has VARCHAR(255)

Recommendations:
- Update fixture to use text type
- Clear schema cache after fix
```

### Example 3: Multi-tenant pattern violation
```
File: src/Model/Table/ApplicationsTable.php
Status: ⚠️ WARNING

Issues found:
- Hardcoded database connection found
- Should use MessageDeliveryDbAccessorComponent

Recommendations:
- Use dynamic connection:
  $conn = $this->MessageDeliveryDbAccessor->getUserMessageDeliveryDbConnection($companyId);
```

## CakePHP-Specific Rules

### Column Type Mappings
```
Migration Type -> Fixture Type
text          -> string (unlimited)
string        -> string (with length)
integer       -> integer
datetime      -> string (ISO format)
boolean       -> boolean (0/1 in MySQL)
decimal       -> string or float
```

### Naming Conventions
- Table names: plural, snake_case
- Foreign keys: singular_id
- Join tables: first_table_second_table
- Timestamps: created, modified

### Reserved Columns
- `id` - Primary key (integer)
- `created` - Creation timestamp
- `modified` - Update timestamp
- `del_flg` - Soft delete flag

## Integration Notes

This skill works best with:
- `fixture-generator` skill for creating compliant fixtures
- `migration-validator` agent for comprehensive checks
- Projects using CakePHP 4.x migrations
- Multi-database architectures

## Usage Scenarios

1. **Before running tests** - Ensure schema consistency
2. **After modifying migrations** - Validate fixture updates
3. **During PR reviews** - Check migration-fixture alignment
4. **Version upgrades** - Verify schema compatibility