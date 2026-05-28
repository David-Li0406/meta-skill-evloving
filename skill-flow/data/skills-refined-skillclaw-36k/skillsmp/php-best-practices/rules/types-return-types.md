---
title: Always Declare Return Types
impact: MEDIUM-HIGH
impactDescription: Documents intent and catches inconsistent returns
tags: types, return, documentation, safety
---

## Always Declare Return Types

Missing return types hide bugs where functions return unexpected values. Return types document intent and catch mismatches at compile time.

**Incorrect (no return types):**

```php
<?php
// No return type - unclear what to expect
function findUser($id) {
    $user = $this->repository->find($id);
    if (!$user) {
        return null; // Or was it supposed to throw?
    }
    return $user;
}

// Inconsistent returns undetected
function calculateDiscount($order) {
    if ($order->isVip()) {
        return 0.2; // float
    }
    if ($order->total > 100) {
        return "10%"; // string! Bug undetected
    }
    // Missing return - returns null
}

// Caller has no IDE support
$discount = calculateDiscount($order);
$finalPrice = $price * (1 - $discount); // May fail
```

**Correct (explicit return types):**

```php
<?php
declare(strict_types=1);

// Clear nullable return
function findUser(int $id): ?User {
    return $this->repository->find($id);
}

// Or throw instead of null
function findUserOrFail(int $id): User {
    $user = $this->repository->find($id);
    if (!$user) {
        throw new NotFoundException(User::class, $id);
    }
    return $user;
}

// Consistent returns enforced
function calculateDiscount(Order $order): float {
    if ($order->isVip()) {
        return 0.2;
    }
    if ($order->total > 100) {
        return 0.1;
    }
    return 0.0; // Must return float
}

// Void for side-effect functions
function sendEmail(User $user, string $message): void {
    $this->mailer->send($user->email, $message);
    // No return statement needed
}

// Never return type (PHP 8.1+)
function throwError(string $message): never {
    throw new RuntimeException($message);
}

// Union types when multiple returns are valid
function getValue(string $key): string|int|null {
    return $this->cache->get($key);
}
```

Return types enable IDE autocomplete and static analysis tools.
