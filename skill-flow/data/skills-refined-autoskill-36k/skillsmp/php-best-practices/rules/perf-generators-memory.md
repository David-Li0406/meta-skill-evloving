---
title: Use Generators for Large Data Iteration
impact: HIGH
impactDescription: Reduces memory usage from O(n) to O(1) for large datasets
tags: performance, generators, memory, iteration
---

## Use Generators for Large Data Iteration

Loading large datasets into arrays consumes massive memory. Generators yield items one at a time, maintaining constant memory usage regardless of dataset size.

**Incorrect (loads entire dataset into memory):**

```php
<?php
// Loads all 1M rows into memory at once
function getAllUsers(): array {
    $users = [];
    $result = $this->db->query("SELECT * FROM users");
    while ($row = $result->fetch()) {
        $users[] = new User($row); // 1M User objects in memory
    }
    return $users;
}

// Reading large file into memory
function processLogFile(string $path): array {
    $lines = file($path); // 10GB file = 10GB+ memory
    $processed = [];
    foreach ($lines as $line) {
        $processed[] = parseLine($line);
    }
    return $processed;
}
```

**Correct (generators yield items one at a time):**

```php
<?php
// Yields one user at a time - constant memory
function getAllUsers(): Generator {
    $result = $this->db->query("SELECT * FROM users");
    while ($row = $result->fetch()) {
        yield new User($row); // Only 1 User in memory
    }
}

// Usage - still processes all users
foreach (getAllUsers() as $user) {
    processUser($user);
}

// Reading large file line by line
function readLargeFile(string $path): Generator {
    $handle = fopen($path, 'r');
    try {
        while (($line = fgets($handle)) !== false) {
            yield trim($line);
        }
    } finally {
        fclose($handle);
    }
}

// Generating ranges without array allocation
function range_generator(int $start, int $end): Generator {
    for ($i = $start; $i <= $end; $i++) {
        yield $i;
    }
}

// Paginated database queries
function getOrdersInBatches(int $batchSize = 1000): Generator {
    $offset = 0;
    do {
        $batch = $this->db->query(
            "SELECT * FROM orders LIMIT ? OFFSET ?",
            [$batchSize, $offset]
        )->fetchAll();

        foreach ($batch as $order) {
            yield new Order($order);
        }

        $offset += $batchSize;
    } while (count($batch) === $batchSize);
}

// Transforming generator output
function mapGenerator(Generator $gen, callable $fn): Generator {
    foreach ($gen as $item) {
        yield $fn($item);
    }
}
```

Reference: [PHP Generators](https://www.php.net/manual/en/language.generators.php)
