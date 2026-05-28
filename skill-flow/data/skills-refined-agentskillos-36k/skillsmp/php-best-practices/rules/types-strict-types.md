---
title: Declare strict_types=1 in All Files
impact: MEDIUM-HIGH
impactDescription: Catches type errors early instead of silent coercion
tags: types, strict, safety, declaration
---

## Declare strict_types=1 in All Files

Without strict types, PHP silently coerces values, leading to subtle bugs. Strict typing catches mismatches immediately at the call site.

**Incorrect (coercive typing hides bugs):**

```php
<?php
// No strict_types - PHP coerces silently

function calculateTotal(int $quantity, float $price): float {
    return $quantity * $price;
}

// These all work but may not be intended:
calculateTotal("5", "19.99");  // Strings coerced to numbers
calculateTotal(5.9, 19.99);    // 5.9 truncated to 5
calculateTotal(true, 10);       // true becomes 1

function processUser(int $id): void {
    // $id could be "123abc" coerced to 123
    $this->repository->find($id);
}

processUser("not_a_number"); // Becomes 0 silently!
```

**Correct (strict typing catches errors):**

```php
<?php
declare(strict_types=1);

function calculateTotal(int $quantity, float $price): float {
    return $quantity * $price;
}

// These now throw TypeError:
calculateTotal("5", 19.99);    // TypeError: must be int
calculateTotal(5.9, 19.99);    // TypeError: must be int

// Only exact types accepted:
calculateTotal(5, 19.99);      // Works
calculateTotal(5, 20);         // Works - int auto-widens to float

function processUser(int $id): void {
    $this->repository->find($id);
}

processUser("abc"); // TypeError immediately, not silent 0

// Explicit conversion when needed
$quantity = (int) $_POST['quantity'];
$price = (float) $_POST['price'];

// With validation
$quantity = filter_var($_POST['quantity'], FILTER_VALIDATE_INT);
if ($quantity === false) {
    throw new ValidationException('Invalid quantity');
}

calculateTotal($quantity, $price);
```

Add `declare(strict_types=1);` as the first statement in every PHP file.

Reference: [PHP Strict Types](https://www.php.net/manual/en/language.types.declarations.php#language.types.declarations.strict)
