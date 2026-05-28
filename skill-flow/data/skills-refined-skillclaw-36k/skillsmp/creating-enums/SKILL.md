---
name: creating-enums
description: Create PHP backed enums for representing fixed sets of values with type safety. Use when creating enums, defining constants, representing states, or when user mentions enums, enum types, constant values, or state machines.
---

# Create Laravel Enums

Create PHP backed enums that represent fixed sets of possible values with full type safety. Enums provide compile-time validation for status codes, roles, and categories, with methods for labels, colors, and other presentation logic.

## File Structure

Enums are organized by domain context:

```
app/Enums/{Domain}/{Name}.php
```

**Examples:**

- `app/Enums/Horizon/Queue.php`
- `app/Enums/Order/OrderStatus.php`
- `app/Enums/User/Role.php`

## Core Conventions

### 1. Enum Structure

```php
<?php

declare(strict_types=1);

namespace App\Enums\{Domain};

enum {Name}: string
{
    case CaseName = 'value';
    case AnotherCase = 'another_value';
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use backed enums with `string` or `int` type
- PascalCase for case names
- snake_case for string values (following Laravel conventions)

### 2. Helper Methods

Add static helper methods for common operations:

```php
enum Queue: string
{
    case Default = 'default';
    case Notifications = 'notifications';
    case Reports = 'reports';

    /**
     * @return list<self>
     */
    public static function short(): array
    {
        return [
            self::Default,
            self::Notifications,
        ];
    }

    /**
     * @return list<self>
     */
    public static function long(): array
    {
        return [
            self::Reports,
        ];
    }
}
```

## Examples

### Example 1: Simple String Enum

```php
<?php

declare(strict_types=1);

namespace App\Enums\User;

enum Role: string
{
    case Admin = 'admin';
    case Editor = 'editor';
    case Viewer = 'viewer';
}
```

### Example 2: Enum with Helper Methods

```php
<?php

declare(strict_types=1);

namespace App\Enums\Order;

enum OrderStatus: string
{
    case Pending = 'pending';
    case Processing = 'processing';
    case Completed = 'completed';
    case Cancelled = 'cancelled';

    /**
     * @return list<self>
     */
    public static function active(): array
    {
        return [
            self::Pending,
            self::Processing,
        ];
    }

    /**
     * @return list<self>
     */
    public static function terminal(): array
    {
        return [
            self::Completed,
            self::Cancelled,
        ];
    }

    public function isActive(): bool
    {
        return in_array($this, self::active(), true);
    }

    public function isTerminal(): bool
    {
        return in_array($this, self::terminal(), true);
    }
}
```

### Example 3: Integer Enum

```php
<?php

declare(strict_types=1);

namespace App\Enums\User;

enum AccountType: int
{
    case Free = 0;
    case Pro = 1;
    case Enterprise = 2;

    public function isPremium(): bool
    {
        return $this === self::Pro || $this === self::Enterprise;
    }
}
```

## Usage in Models

Enums work seamlessly with Eloquent casts:

```php
final class Order extends Model
{
    protected function casts(): array
    {
        return [
            'status' => OrderStatus::class,
        ];
    }
}

// Usage
$order->status = OrderStatus::Processing;
if ($order->status->isActive()) {
    // ...
}
```

## Usage in Database Migrations

```php
$table->enum('status', ['pending', 'processing', 'completed', 'cancelled'])
      ->default('pending');

// Or use string column for flexibility
$table->string('status')->default('pending');
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't use non-backed enums (no type)
enum Status
{
    case Pending;
    case Completed;
}

// Don't use class constants instead
final class OrderStatus
{
    public const PENDING = 'pending'; // ❌ Use enum
}

// Don't use inconsistent casing
enum Status: string
{
    case pending = 'pending'; // ❌ Use PascalCase
}
```

### ✅ Do This Instead

```php
// Use backed enums
enum Status: string
{
    case Pending = 'pending';
    case Completed = 'completed';
}

// Use PascalCase for cases
enum OrderStatus: string
{
    case Pending = 'pending';
    case Processing = 'processing';
}
```

## Quality Standards

- All enums must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Refactored with Rector
- PHPDoc for return types on helper methods
