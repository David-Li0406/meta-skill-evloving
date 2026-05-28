---
title: Follow PSR-12 Coding Style
impact: MEDIUM
impactDescription: Consistent formatting across the PHP ecosystem
tags: psr, style, formatting, consistency
---

## Follow PSR-12 Coding Style

Inconsistent formatting wastes time in code reviews and makes code harder to read. PSR-12 is the PHP community standard for coding style.

**Incorrect (inconsistent style):**

```php
<?php
namespace App\Services;
use App\Models\User;
use App\Models\Order;

class orderService{
    private $repo;
    function __construct($repo){
        $this->repo=$repo;
    }

    public function CreateOrder($data){
        if($data['quantity']>0){
            return $this->repo->save($data);
        }
        else{
            throw new \Exception('Invalid');
        }
    }
}
```

**Correct (PSR-12 compliant):**

```php
<?php

declare(strict_types=1);

namespace App\Services;

use App\Models\Order;
use App\Models\User;
use App\Repositories\OrderRepositoryInterface;
use InvalidArgumentException;

final class OrderService
{
    public function __construct(
        private OrderRepositoryInterface $repository
    ) {
    }

    public function createOrder(array $data): Order
    {
        if ($data['quantity'] <= 0) {
            throw new InvalidArgumentException('Quantity must be positive');
        }

        return $this->repository->save($data);
    }

    public function findByUser(
        User $user,
        ?string $status = null,
        int $limit = 10
    ): array {
        return $this->repository->findByUser(
            $user,
            $status,
            $limit
        );
    }
}
```

**Key PSR-12 rules:**

```php
<?php
// Opening brace on same line for classes/methods
class Example
{
    // 4 spaces indentation, no tabs
    public function method(): void
    {
        // Control structures: space after keyword, braces on same line
        if ($condition) {
            doSomething();
        } elseif ($other) {
            doOther();
        } else {
            doDefault();
        }

        // No space after function name
        $result = functionCall($arg1, $arg2);

        // Operators surrounded by spaces
        $sum = $a + $b;
        $concat = $str1 . $str2;
    }
}
```

Use PHP-CS-Fixer or PHP_CodeSniffer to automate formatting.

Reference: [PSR-12](https://www.php-fig.org/psr/psr-12/)
