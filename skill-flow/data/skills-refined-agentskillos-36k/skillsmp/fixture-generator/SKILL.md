---
name: fixture-generator
description: Generates CakePHP test fixtures from migration files, ensuring schema consistency and following project conventions including Configure::read usage
---

# Fixture Generator

A specialized skill for generating CakePHP test fixtures that perfectly match migration schemas and follow project-specific conventions.

## Generation Principles

### 1. Schema-First Approach

**Always generate fixtures from migration files:**
- Migration is the single source of truth
- Extract column definitions, types, and constraints
- Preserve all NOT NULL requirements
- Include all columns defined in migration

### 2. Configure::read() Integration

**Use configuration constants instead of hardcoded values:**
```php
<?php
declare(strict_types=1);

namespace App\Test\Fixture\[AppClient];

use App\Test\Fixture\[AppClient]TestFixture;
use Cake\Core\Configure;  // REQUIRED: Add use statement

class ApplicationsFixture extends [AppClient]TestFixture
{
    public $table = 'applications';

    public function init(): void
    {
        $this->records = [
            [
                'id' => 1,
                'status' => Configure::read('Applications.status.applying'), // ✅
                'del_flg' => Configure::read('Common.del_flg.off'),         // ✅
                // ... other fields
            ],
        ];
        parent::init();
    }
}
```

### 3. Multi-Database Fixture Organization

**Pattern** (namespace based on database schema):
```
tests/Fixture/
├── [ProjectDefault]/     # Project account fixtures
│   └── AgentsFixture.php
├── [AppDefault]/         # Application account fixtures
│   └── CompanysFixture.php
└── [AppClient]/          # Application client fixtures (multi-tenant)
    └── ApplicationsFixture.php
```


### 4. Base Fixture Class Extension

**Pattern** (extend appropriate base class):
```php
class AgentsFixture extends [ProjectDefault]TestFixture
class CompanysFixture extends [AppDefault]TestFixture
class ApplicationsFixture extends [AppClient]TestFixture
```


## Generation Rules

### Column Type Mappings

```
Migration Type    -> Fixture Value Example
-----------------------------------------
integer          -> 1
string(255)      -> 'test_value'
text             -> 'longer test content'
datetime         -> '2024-01-01 00:00:00'
date             -> '2024-01-01'
boolean          -> true (or 1 for MySQL)
decimal(10,2)    -> '99.99'
json             -> '{"key": "value"}'
```

### Required Fields Handling

**NOT NULL columns must have values:**
```php
// Migration:
$table->addColumn('company_name', 'string', ['null' => false]);

// Fixture must include:
'company_name' => 'Test Company',  // Cannot be null
```

### Foreign Key References

**Use consistent test IDs:**
```php
// Constants for test IDs
define('PHPUNIT_COMPANY_ID', 9999);
define('PHPUNIT_USER_ID', 1);

// In fixture:
'eco_company_id' => PHPUNIT_COMPANY_ID,
'created_by' => PHPUNIT_USER_ID,
```

### Common Configuration Keys

**Frequently used Configure::read() keys:**
```php
// Status values
Configure::read('Applications.status.applying')      // 申請中
Configure::read('Applications.status.applied')       // 申請済
Configure::read('Applications.status.non_approval')  // 非承認
Configure::read('Applications.status.cancelled')     // キャンセル

// Common flags
Configure::read('Common.del_flg.off')    // 0 - Active
Configure::read('Common.del_flg.on')     // 1 - Deleted
Configure::read('Common.display_flg.on')  // 1 - Display
Configure::read('Common.display_flg.off') // 0 - Hidden

// Account types
Configure::read('Account.account_type.toc')      // 1
Configure::read('Account.account_type.master')   // 2
Configure::read('Account.account_type.enduser')  // 3
```

## Generation Process

### Step 1: Parse Migration File
```php
// Input: config/Migrations/[AppClient]/20210201000000_ClientInitial.php
$table->addColumn('application_no', 'string', [
    'default' => null,
    'limit' => 255,
    'null' => false,
]);
$table->addColumn('status', 'integer', [
    'default' => null,
    'null' => false,
]);
```

### Step 2: Generate Fixture Structure
```php
<?php
declare(strict_types=1);

namespace App\Test\Fixture\[AppClient];

use App\Test\Fixture\[AppClient]TestFixture;
use Cake\Core\Configure;

class ApplicationsFixture extends [AppClient]TestFixture
{
    public $table = 'applications';

    public function init(): void
    {
        $this->records = [
            [
                'id' => 1,
                'application_no' => 'TEST-001',
                'status' => Configure::read('Applications.status.applying'),
                'created' => '2024-01-01 00:00:00',
                'modified' => '2024-01-01 00:00:00',
            ],
        ];
        parent::init();
    }
}
```

## Special Cases

### 1. Password Fields
```php
// Use bcrypt hash for passwords
'password' => '$2y$10$YQzcRLmz9Wdum7mQvzXGYOJPABqMJqiaY.Fd.FzhHXHG2b8sNNSPa',
// This is hash of 'password123'
```

### 2. JSON Fields
```php
// Store as JSON string
'metadata' => '{"key": "value", "nested": {"data": true}}',
```

### 3. Multi-Tenant Company ID
```php
// Always use test company constant
'company_id' => PHPUNIT_COMPANY_ID,  // 9999
```

### 4. Timestamps
```php
// Use consistent test timestamps
'created' => '2024-01-01 00:00:00',
'modified' => '2024-01-01 00:00:00',
```

## Example Generations

### Example 1: User Fixture
```php
// Migration has: login_name (text), mail (string), eco_company_id (integer)
// Generated fixture:
[
    'id' => 1,
    'login_name' => 'test_user',
    'mail' => 'test@example.com',
    'eco_company_id' => PHPUNIT_COMPANY_ID,
    'del_flg' => Configure::read('Common.del_flg.off'),
    'created' => '2024-01-01 00:00:00',
    'modified' => '2024-01-01 00:00:00',
]
```

### Example 2: Application Fixture
```php
// Complex fixture with relationships
[
    'id' => 1,
    'application_no' => 'APP-2024-001',
    'applicant_name' => '申請者太郎',
    'status' => Configure::read('Applications.status.applying'),
    'eco_company_id' => PHPUNIT_COMPANY_ID,
    'apply_category_id' => 1,
    'area_id' => 1,
    'del_flg' => Configure::read('Common.del_flg.off'),
    'created_by' => PHPUNIT_USER_ID,
    'created' => '2024-01-01 00:00:00',
    'modified' => '2024-01-01 00:00:00',
]
```

## Integration Notes

- Works with `cakephp-migration-checker` skill for validation
- Compatible with CakePHP 4.x fixture system
- Supports multi-database test environments
- Follows strict testing principles that ensure tests guarantee production code behavior

## Usage Commands

Generate fixture from migration:
```bash
# Analyze migration and create fixture
Read migration file: config/Migrations/[AppClient]/[timestamp]_[Name].php
Generate fixture at: tests/Fixture/[AppClient]/[TableName]Fixture.php
```

Validate generated fixture:
```bash
# Check if fixture matches migration schema
Compare column definitions
Verify Configure::read usage
Ensure all NOT NULL fields have values
```