---
title: Prefer String Interpolation Over Concatenation
impact: HIGH
impactDescription: Cleaner code and marginally better performance
tags: performance, strings, interpolation, readability
---

## Prefer String Interpolation Over Concatenation

String concatenation with . creates intermediate strings and is harder to read. Double-quoted string interpolation is cleaner and slightly faster.

**Incorrect (excessive concatenation):**

```php
<?php
// Hard to read with many variables
$message = 'Hello, ' . $firstName . ' ' . $lastName . '! Your order #' . $orderId . ' has been shipped to ' . $address . '.';

// Multiple concatenations create intermediate strings
$sql = 'SELECT * FROM ' . $table . ' WHERE id = ' . $id . ' AND status = ' . $status;

// Confusing quote escaping
$html = '<a href="' . $url . '" class="' . $class . '">' . $text . '</a>';
```

**Correct (clean interpolation):**

```php
<?php
// Easy to read
$message = "Hello, {$firstName} {$lastName}! Your order #{$orderId} has been shipped to {$address}.";

// Use curly braces for complex expressions
$greeting = "Welcome, {$user->getName()}!";
$item = "Item: {$items[$index]['name']}";

// Heredoc for multi-line strings
$email = <<<EMAIL
Dear {$customer->name},

Your order #{$order->id} has been confirmed.

Items:
{$itemsList}

Total: \${$order->total}

Thank you for shopping with us!
EMAIL;

// Nowdoc when no interpolation needed
$sql = <<<'SQL'
SELECT users.*, orders.total
FROM users
JOIN orders ON users.id = orders.user_id
WHERE users.status = :status
SQL;

// sprintf for complex formatting
$message = sprintf(
    'User %s (ID: %d) purchased %d items for $%.2f',
    $user->name,
    $user->id,
    count($items),
    $total
);
```

**Note:** For SQL queries, always use prepared statements regardless of string method.

Use double quotes for variable interpolation, single quotes for literal strings.
