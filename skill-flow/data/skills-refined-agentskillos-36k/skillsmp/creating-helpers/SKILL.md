---
name: creating-helpers
description: Create global PHP helper functions for common utility operations. Use when creating helper functions, utility functions, or when user mentions helpers, global functions, or utility methods.
---

# Create Laravel Helpers

Create global PHP helper functions for common utility operations. Helpers are simple, pure functions for formatting, string manipulation, and convenience wrappers. For complex logic with dependencies or side effects, use Action classes instead.

## File Structure

Helpers are defined in:

```
app/Helpers/Helpers.php
```

This file is autoloaded via `composer.json`:

```json
"autoload": {
    "files": [
        "app/Helpers/Helpers.php"
    ]
}
```

## Core Conventions

### 1. Helper Function Structure

```php
<?php

declare(strict_types=1);

if (! function_exists('helper_name')) {
    function helper_name(string $param): string
    {
        // Implementation
        return $result;
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Wrap in `function_exists()` check
- Use snake_case for function names
- Full type hints on parameters and return type
- Keep functions simple and focused

### 2. Naming Conventions

- Use descriptive snake_case names
- Prefix with domain if specific: `user_avatar_url()`, `order_total()`
- Keep generic helpers unprefixed: `money()`, `percentage()`

## Examples

### Example 1: Route Helper

```php
if (! function_exists('route_is')) {
    /**
     * Determine if the current route matches the given patterns.
     */
    function route_is(string ...$patterns): bool
    {
        return request()->routeIs(...$patterns);
    }
}
```

### Example 2: Formatting Helper

```php
if (! function_exists('money')) {
    /**
     * Format a value as money.
     */
    function money(int|float $amount, string $currency = 'USD'): string
    {
        return number_format($amount, 2) . ' ' . $currency;
    }
}
```

### Example 3: Domain Helper

```php
if (! function_exists('user_avatar_url')) {
    /**
     * Get the avatar URL for a user.
     */
    function user_avatar_url(User $user): ?string
    {
        return $user->avatar_path
            ? Storage::url($user->avatar_path)
            : null;
    }
}
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't skip function_exists check
function helper_name() {} // ❌ Wrap in check

// Don't omit type hints
function format_date($date) {} // ❌ Type hint

// Don't create complex helpers
function process_entire_order($order) {
    // 50 lines of logic ❌ Use Action class
}

// Don't use camelCase
function userName() {} // ❌ Use snake_case
```

### ✅ Do This Instead

```php
// Always use function_exists
if (! function_exists('helper_name')) {
    function helper_name(string $param): string {}
}

// Type hint everything
function format_date(Carbon $date): string {}

// Keep simple
function user_initials(User $user): string {
    return strtoupper(substr($user->name, 0, 1));
}

// Use snake_case
function user_name(User $user): string {}
```

## Helpers vs Actions

| Use Helper                     | Use Action                        |
| ------------------------------ | --------------------------------- |
| Pure formatting/transformation | Requires dependency injection     |
| No side effects                | Has side effects (DB, API, email) |
| Under 10 lines                 | Complex business logic            |
| No mocking needed              | Testing requires mocks            |

## Quality Standards

- All helpers must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Add PHPDoc describing purpose
- Keep functions pure (no side effects) when possible
