---
title: Use Composer Autoloader Instead of require_once
impact: HIGH
impactDescription: Loads classes on demand, improves maintainability
tags: performance, autoloading, composer, psr-4
---

## Use Composer Autoloader Instead of require_once

Manual require/include statements are error-prone and load files whether needed or not. Composer's PSR-4 autoloader loads classes on demand.

**Incorrect (manual includes):**

```php
<?php
// Manual includes - brittle and slow
require_once 'src/Models/User.php';
require_once 'src/Models/Order.php';
require_once 'src/Services/PaymentService.php';
require_once 'src/Services/EmailService.php';
// ... 50 more includes

// Conditional include - still inefficient
if ($needsPayment) {
    require_once 'src/Services/PaymentService.php';
}

// Include from class - anti-pattern
class OrderController {
    public function create() {
        require_once 'src/Models/Order.php';
        $order = new Order();
    }
}
```

**Correct (Composer autoloading):**

```json
{
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "Tests\\": "tests/"
        }
    }
}
```

```php
<?php
// index.php - single require
require_once __DIR__ . '/vendor/autoload.php';

// Classes loaded automatically when first used
use App\Models\User;
use App\Models\Order;
use App\Services\PaymentService;

// Only User is loaded here
$user = new User();

// Order and PaymentService loaded only when used
if ($user->hasCart()) {
    $order = new Order();
    $payment = new PaymentService();
}
```

**Directory structure:**

```
src/
├── Models/
│   ├── User.php      # App\Models\User
│   └── Order.php     # App\Models\Order
├── Services/
│   ├── PaymentService.php
│   └── EmailService.php
└── Controllers/
    └── OrderController.php
```

**Optimize for production:**

```bash
# Generate optimized autoloader
composer dump-autoload --optimize --classmap-authoritative
```

Reference: [Composer Autoloading](https://getcomposer.org/doc/04-schema.md#autoload)
