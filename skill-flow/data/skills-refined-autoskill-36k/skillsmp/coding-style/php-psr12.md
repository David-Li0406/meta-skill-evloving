---
name: PHP PSR-12 規範
description: PHP 官方編碼標準
---

# PSR-12 編碼規範

## 基本規則

- 縮排：4 空格
- 行寬：120 字元
- 檔案結尾：一個空行
- 關鍵字：小寫 (`true`, `false`, `null`)

## 命名空間與 Use

```php
<?php

declare(strict_types=1);

namespace App\Controllers;

use App\Models\User;
use App\Services\AuthService;
use Psr\Http\Message\ResponseInterface as Response;

class UserController
{
    // ...
}
```

## 類別

```php
class UserController extends Controller implements AuthenticatedInterface
{
    private AuthService $authService;

    public function __construct(AuthService $authService)
    {
        $this->authService = $authService;
    }

    public function index(): Response
    {
        // ...
    }

    private function validateUser(User $user): bool
    {
        // ...
    }
}
```

## 控制結構

```php
// if-else
if ($condition) {
    // ...
} elseif ($otherCondition) {
    // ...
} else {
    // ...
}

// switch
switch ($value) {
    case 1:
        // ...
        break;
    case 2:
        // ...
        // no break
    default:
        // ...
        break;
}

// foreach
foreach ($items as $key => $value) {
    // ...
}
```

## 函式與方法

```php
public function foo(
    int $arg1,
    string $arg2,
    ?array $arg3 = null,
): bool {
    // ...
}

// 閉包
$closure = function (int $x, int $y) use ($z): int {
    return $x + $y + $z;
};

// 箭頭函式
$double = fn(int $x): int => $x * 2;
```

---

## 工具

```bash
# PHP_CodeSniffer
composer require --dev squizlabs/php_codesniffer
./vendor/bin/phpcs --standard=PSR12 src/

# PHP-CS-Fixer
composer require --dev friendsofphp/php-cs-fixer
./vendor/bin/php-cs-fixer fix src/
```
