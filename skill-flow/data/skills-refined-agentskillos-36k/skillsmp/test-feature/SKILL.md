---
name: test-feature
description: Write Pest PHP feature tests following RentPath conventions. Use for writing new tests, understanding test patterns, using factories, and ensuring proper coverage. Auto-triggers on "write test", "add test", "test this feature", "create test", "test coverage".
---

# Feature Test Writing Guide

You are helping write Pest PHP tests following RentPath conventions.

## Arguments

This skill accepts optional arguments to specify what to test:

| Usage                                    | Behavior                                |
| ---------------------------------------- | --------------------------------------- |
| `/test-feature`                          | Interactive - ask what to test          |
| `/test-feature ApplicationController`    | Write tests for that controller         |
| `/test-feature application submission`   | Write tests for that workflow           |
| `/test-feature Application model`        | Write tests for model logic             |
| `/test-feature the changes we just made` | Test recent implementation              |
| `/test-feature authorization`            | Focus on auth/policy tests              |
| `/test-feature validation`               | Focus on validation tests               |
| `/test-feature edge cases`               | Focus on edge cases for current feature |

**Argument interpretation:**

- **Controller/Model name** - Write tests for that class
- **Workflow description** - Write tests covering that flow
- **Focus area** (`authorization`, `validation`, `edge cases`) - Specific test type
- **Context reference** (`the changes`, `what we did`) - Test recent work

## Before You Start

1. **Check existing tests**: Look at `tests/Feature/` for patterns
2. **Check factories**: Review `database/factories/` for available states
3. **Understand the feature**: What behavior are you testing?

## Tools to Use

| Task              | Tool   | Command/Action                              |
| ----------------- | ------ | ------------------------------------------- |
| Create test       | `Bash` | `php artisan make:test [Name]Test`          |
| View factories    | `Read` | `database/factories/[Model]Factory.php`     |
| Run tests         | `Bash` | `php artisan test --filter=[pattern]`       |
| Run specific file | `Bash` | `php artisan test tests/Feature/[File].php` |
| Check coverage    | `Bash` | `php artisan test --coverage`               |

## Quick Start

### Basic Test Structure

```php
<?php

use App\Models\User;
use App\Models\Property;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

beforeEach(function () {
    $this->user = User::factory()->create();
});

test('user can view property list', function () {
    Property::factory()->count(3)->create();

    $response = $this->actingAs($this->user)
        ->get('/properties');

    $response->assertOk();
    $response->assertInertia(fn ($page) => $page
        ->component('properties/index')
        ->has('properties', 3)
    );
});
```

## Test Coverage Checklist

### For CRUD Operations

```
[ ] Index - list items with pagination
[ ] Index - filter/search works
[ ] Create - form renders
[ ] Create - validation errors
[ ] Create - success creates record
[ ] Show - displays correct item
[ ] Show - 404 for non-existent
[ ] Update - form renders with data
[ ] Update - validation errors
[ ] Update - success updates record
[ ] Delete - removes record
[ ] Delete - handles dependencies
```

### For Workflows

```
[ ] Each status transition
[ ] Invalid transitions rejected
[ ] Authorization at each step
[ ] Side effects triggered (events, notifications)
```

### For Wizards

```
[ ] Each step renders
[ ] Step validation works
[ ] Can navigate between valid steps
[ ] Cannot skip ahead
[ ] Draft saves work
[ ] Final submission works
```

## Running Tests

```bash
# All tests
php artisan test

# Specific file
php artisan test tests/Feature/ApplicationFlowTest.php

# Filter by name
php artisan test --filter="can submit application"

# Filter by describe block
php artisan test --filter="Application Submission"

# With coverage
php artisan test --coverage

# Parallel execution
php artisan test --parallel

# Stop on first failure
php artisan test --stop-on-failure
```

## Detailed Guides

For comprehensive patterns and examples, see the supporting files:

- **[FACTORIES.md](FACTORIES.md)** - Factory states and relationship patterns
- **[PATTERNS.md](PATTERNS.md)** - Test patterns, assertions, describe blocks

## Documentation References

- `tests/Pest.php` - Global test configuration
- `database/factories/` - All model factories
- `.claude/agents/testing-expert.md` - Testing expert agent
- `docs/patterns/wizard.md` - Wizard testing patterns

## Debugging Tips

```php
// Dump response content
$response->dump();
$response->dumpHeaders();
$response->dumpSession();

// Disable exception handling to see full errors
$this->withoutExceptionHandling();

// Debug database state
dd(Application::all()->toArray());

// Check what was validated
dd($response->exception->validator->errors()->toArray());
```
