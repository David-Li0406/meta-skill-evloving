---
title: Use Union Types Over mixed
impact: MEDIUM-HIGH
impactDescription: Provides type safety while allowing flexibility
tags: types, union, mixed, safety
---

## Use Union Types Over mixed

The `mixed` type accepts anything, providing no type safety. Union types specify exactly which types are valid, enabling IDE support and catching errors.

**Incorrect (mixed loses type information):**

```php
<?php
// mixed accepts anything - no safety
function process(mixed $value): mixed {
    // Could be string, int, array, object, null, callable...
    return $value;
}

// No IDE support or static analysis
$result = process($data);
$result->method(); // May crash at runtime

// Array of mixed - no element type info
function getItems(): array {
    return $this->items;
}
```

**Correct (union types specify valid types):**

```php
<?php
declare(strict_types=1);

// Union type - only these types valid
function process(string|int|float $value): string {
    return match (true) {
        is_string($value) => $value,
        is_int($value) => (string) $value,
        is_float($value) => number_format($value, 2),
    };
}

// Nullable union
function findById(string|int $id): ?User {
    return $this->repository->find($id);
}

// Union with classes
function setLogger(LoggerInterface|NullLogger $logger): void {
    $this->logger = $logger;
}

// Return union types
function getValue(string $key): string|int|bool|null {
    return $this->config[$key] ?? null;
}

// Intersection types (PHP 8.1+)
function process(Countable&Traversable $items): int {
    return count($items);
}

// DNF types (PHP 8.2+)
function handle((Countable&Traversable)|array $items): void {
    foreach ($items as $item) {
        $this->process($item);
    }
}

// Typed arrays with docblocks when union not sufficient
/** @param array<int, User> $users */
function processUsers(array $users): void {
    foreach ($users as $user) {
        $user->notify(); // IDE knows $user is User
    }
}

// Use generics in docblocks for complex types
/** @return Collection<string, Order> */
function getOrders(): Collection {
    return $this->orders;
}
```

Reserve `mixed` for truly dynamic APIs where any type is valid.

Reference: [PHP Union Types](https://www.php.net/manual/en/language.types.declarations.php#language.types.declarations.union)
