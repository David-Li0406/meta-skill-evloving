---
title: Use Constructor Property Promotion
impact: LOW-MEDIUM
impactDescription: Reduces boilerplate in class definitions
tags: php8, constructor, promotion, modern
---

## Use Constructor Property Promotion

Traditional property declaration requires repeating property names three times. PHP 8's constructor promotion combines declaration, assignment, and typing in one place.

**Incorrect (verbose traditional style):**

```php
<?php
class User
{
    private int $id;
    private string $name;
    private string $email;
    private ?string $phone;
    private bool $isActive;
    private DateTimeInterface $createdAt;

    public function __construct(
        int $id,
        string $name,
        string $email,
        ?string $phone,
        bool $isActive,
        DateTimeInterface $createdAt
    ) {
        $this->id = $id;
        $this->name = $name;
        $this->email = $email;
        $this->phone = $phone;
        $this->isActive = $isActive;
        $this->createdAt = $createdAt;
    }

    public function getId(): int
    {
        return $this->id;
    }

    // ... more getters
}
```

**Correct (constructor property promotion):**

```php
<?php
declare(strict_types=1);

final class User
{
    public function __construct(
        private readonly int $id,
        private readonly string $name,
        private readonly string $email,
        private readonly ?string $phone = null,
        private readonly bool $isActive = true,
        private readonly DateTimeInterface $createdAt = new DateTimeImmutable()
    ) {
    }

    // Getters only if needed for public access
    public function getId(): int
    {
        return $this->id;
    }
}

// With readonly properties (PHP 8.1+)
final readonly class OrderItem
{
    public function __construct(
        public int $productId,
        public int $quantity,
        public float $price
    ) {
    }

    public function getTotal(): float
    {
        return $this->quantity * $this->price;
    }
}

// Mix promoted and non-promoted
final class Service
{
    private array $cache = [];

    public function __construct(
        private readonly Repository $repository,
        private readonly LoggerInterface $logger
    ) {
    }
}

// Default values supported
final class Config
{
    public function __construct(
        public readonly string $host = 'localhost',
        public readonly int $port = 3306,
        public readonly int $timeout = 30
    ) {
    }
}
```

Constructor promotion works with all visibility modifiers and the `readonly` keyword.

Reference: [PHP Constructor Promotion](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)
