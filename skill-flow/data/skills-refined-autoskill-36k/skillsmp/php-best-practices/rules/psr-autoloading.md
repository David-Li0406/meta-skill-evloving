---
title: Use PSR-4 Autoloading Structure
impact: MEDIUM
impactDescription: Standard autoloading enables interoperability
tags: psr, autoloading, namespaces, composer
---

## Use PSR-4 Autoloading Structure

Non-standard autoloading breaks with Composer and other tools. PSR-4 maps namespace prefixes to directories, enabling seamless autoloading.

**Incorrect (non-standard structure):**

```php
<?php
// File: classes/user_model.php
class user_model {
    // Underscore naming, no namespace
}

// File: inc/helpers.php
function get_user() { /* ... */ }

// Manual includes required
require_once 'classes/user_model.php';
require_once 'inc/helpers.php';
```

**Correct (PSR-4 structure):**

```json
// composer.json
{
    "autoload": {
        "psr-4": {
            "App\\": "src/",
            "App\\Tests\\": "tests/"
        }
    }
}
```

```php
<?php
// File: src/Models/User.php
// Namespace matches directory structure

declare(strict_types=1);

namespace App\Models;

final class User
{
    public function __construct(
        public readonly int $id,
        public readonly string $name,
        public readonly string $email
    ) {
    }
}

// File: src/Services/UserService.php
declare(strict_types=1);

namespace App\Services;

use App\Models\User;
use App\Repositories\UserRepositoryInterface;

final class UserService
{
    public function __construct(
        private UserRepositoryInterface $repository
    ) {
    }
}

// File: src/Http/Controllers/UserController.php
declare(strict_types=1);

namespace App\Http\Controllers;

use App\Services\UserService;

final class UserController
{
    // ...
}
```

**Directory structure:**

```
project/
├── composer.json
├── src/
│   ├── Models/
│   │   └── User.php              # App\Models\User
│   ├── Services/
│   │   └── UserService.php       # App\Services\UserService
│   ├── Repositories/
│   │   ├── UserRepositoryInterface.php
│   │   └── UserRepository.php
│   └── Http/
│       └── Controllers/
│           └── UserController.php
└── tests/
    └── Services/
        └── UserServiceTest.php   # App\Tests\Services\UserServiceTest
```

Run `composer dump-autoload` after changing composer.json autoload settings.

Reference: [PSR-4](https://www.php-fig.org/psr/psr-4/)
