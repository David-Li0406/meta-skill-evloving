---
name: modern-php-development
description: Use this skill for writing idiomatic, high-performance PHP code utilizing modern features and best practices.
---

# Modern PHP Development

Write idiomatic, performant PHP code using modern features and patterns.

## When to use

- Writing PHP code with a focus on performance
- Utilizing PHP 8+ features
- Developing applications with frameworks like Laravel or Symfony
- Implementing memory-efficient data processing

## Focus Areas

- **Generators and Iterators**: Use for memory-efficient data processing.
- **SPL Data Structures**: Utilize structures like `SplQueue`, `SplStack`, and `SplFixedArray` for performance benefits.
- **Modern PHP 8+ Features**: Implement match expressions, enums, attributes, and constructor property promotion.
- **Type System Mastery**: Leverage union types, intersection types, and strict typing.
- **Advanced OOP Patterns**: Apply traits, late static binding, and magic methods.
- **Performance Profiling**: Identify and optimize performance bottlenecks.

## Modern PHP Patterns

### Type System (PHP 8+)

```php
// Union types
function process(int|string $id): array|false {
    // ...
}

// Constructor property promotion
class User {
    public function __construct(
        public readonly string $name,
        public readonly string $email,
        private ?int $age = null,
    ) {}
}

// Enums
enum Status: string {
    case Pending = 'pending';
    case Active = 'active';
    case Completed = 'completed';
}

// Match expression
$result = match($status) {
    Status::Pending => 'Waiting',
    Status::Active => 'In Progress',
    Status::Completed => 'Done',
};
```

### Generators

```php
// Memory-efficient iteration
function readLargeFile(string $path): Generator {
    $handle = fopen($path, 'r');
    while (($line = fgets($handle)) !== false) {
        yield trim($line);
    }
    fclose($handle);
}

// Usage
foreach (readLargeFile('huge.csv') as $line) {
    processLine($line);
}
```

### SPL Data Structures

```php
// Priority queue
$queue = new SplPriorityQueue();
$queue->insert('low', 1);
$queue->insert('high', 10);
$queue->insert('medium', 5);

while (!$queue->isEmpty()) {
    echo $queue->extract(); // high, medium, low
}

// Fixed array (memory efficient)
$arr = new SplFixedArray(1000);
$arr[0] = 'value';
```

### Error Handling

```php
// Custom exceptions
class ValidationException extends Exception {
    public function __construct(
        public readonly string $field,
        string $message,
    ) {
        parent::__construct($message);
    }
}

// Try-catch with multiple types
try {
    process($data);
} catch (ValidationException $e) {
    log("Validation failed: {$e->field}");
} catch (RuntimeException $e) {
    log("Runtime error: {$e->getMessage()}");
} finally {
    cleanup();
}
```

## Best Practices

- Use strict types: `declare(strict_types=1);`
- Follow PSR-12 coding standards
- Prefer built-in functions over custom implementations
- Test edge cases and error conditions thoroughly
- Write self-documenting code with meaningful names

## Examples

**Input:** "Optimize this PHP code"  
**Action:** Profile with Xdebug, use generators, leverage SPL structures.

**Input:** "Modernize to PHP 8"  
**Action:** Add type hints, use match/enums, constructor promotion.