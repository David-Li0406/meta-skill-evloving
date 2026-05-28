---
name: creating-model-mixins
description: Create PHP trait mixins for reusable model behavior and request extensions. Use when creating mixins, adding traits to models, extending request behavior, or when user mentions mixins, traits, reusable behavior, or model extensions.
---

# Create Model Mixins and Traits

Create PHP traits for reusable model behavior and request extensions. Model concerns add shared functionality like UUID support or soft deletes, while request mixins extend the Request class with custom helper methods.

## File Structure

Mixins are organized by what they extend:

```
app/Mixins/{Class}Mixin.php
app/Models/Concerns/{Name}.php
```

**Examples:**

- `app/Mixins/RequestMixin.php` - Extends Request class
- `app/Models/Concerns/HasUuid.php` - Adds UUID support
- `app/Support/TwoFactorAuthentication/Concerns/TwoFactorAuthenticatable.php` - Adds 2FA

## Core Conventions

### 1. Request Mixin Structure

```php
<?php

declare(strict_types=1);

namespace App\Mixins;

use Closure;
use Illuminate\Http\Request;

/**
 * @mixin Request
 */
final class RequestMixin
{
    public function methodName(): Closure
    {
        /**
         * @return ReturnType
         */
        return function (): ReturnType {
            // $this refers to Request instance
            return $this->query('key');
        };
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final class` for mixins
- Add `@mixin` PHPDoc for IDE support
- Methods return `Closure`
- Closures must have PHPDoc return type
- Register in service provider with `Request::mixin(new RequestMixin)`

### 2. Model Trait Structure

```php
<?php

declare(strict_types=1);

namespace App\Models\Concerns;

/**
 * @template TModel of \Illuminate\Database\Eloquent\Model
 */
trait TraitName
{
    public function methodName(): ReturnType
    {
        // Trait logic
    }

    protected function bootTraitName(): void
    {
        // Model boot logic
    }
}
```

**Key Requirements:**

- Use `trait` keyword
- Add `@template` PHPDoc for generic model type
- Prefix boot method with `boot{TraitName}`
- Full type hints on all methods

## Examples

### Example 1: Request Mixin

```php
<?php

declare(strict_types=1);

namespace App\Mixins;

use Closure;
use Illuminate\Http\Request;

/**
 * @mixin Request
 */
final class RequestMixin
{
    public function getSorts(): Closure
    {
        /**
         * @return array<int, array{id: string, desc: bool}>
         */
        return function (?string $default = null): array {
            $sortQuery = $this->query('sort', $default);

            if (is_string($sortQuery)) {
                $sorts = explode(',', $sortQuery);

                $sorts = array_map(function (string $value): array {
                    $value = trim($value);
                    $desc = str_starts_with($value, '-');
                    $id = ltrim($value, '-');

                    return [
                        'id' => $id,
                        'desc' => $desc,
                    ];
                }, $sorts);

                return array_filter($sorts, fn (array $sort): bool => $sort['id'] !== '');
            }

            return [];
        };
    }

    public function getFilters(): Closure
    {
        /**
         * @return array<int, array{id: string, value: string}>
         */
        return function (?array $default = null): array {
            $filters = $this->query('filter', $default);

            if (is_array($filters)) {
                $filters = array_map(fn (mixed $value, string $key): array => [
                    'id' => $key,
                    'value' => is_array($value) ? implode(',', $value) : $value,
                ], $filters, array_keys($filters));

                return array_filter($filters, fn (array $filter): bool => $filter['id'] !== '');
            }

            return [];
        };
    }
}
```

### Example 2: Model Trait with Boot

```php
<?php

declare(strict_types=1);

namespace App\Models\Concerns;

use Illuminate\Support\Str;

/**
 * @template TModel of \Illuminate\Database\Eloquent\Model
 */
trait HasUuid
{
    protected static function bootHasUuid(): void
    {
        static::creating(function ($model): void {
            if (! $model->uuid) {
                $model->uuid = (string) Str::uuid();
            }
        });
    }

    public function getRouteKeyName(): string
    {
        return 'uuid';
    }
}
```

### Example 3: Complex Model Trait (Two-Factor Auth)

```php
<?php

declare(strict_types=1);

namespace App\Support\TwoFactorAuthentication\Concerns;

use App\Support\TwoFactorAuthentication\Facades\TwoFactorAuthentication;

/**
 * @template TModel of \Illuminate\Database\Eloquent\Model
 */
trait TwoFactorAuthenticatable
{
    public function confirmTwoFactorAuth(): void
    {
        $this->forceFill([
            'two_factor_confirmed_at' => now(),
        ])->save();
    }

    public function disableTwoFactorAuth(): void
    {
        $this->forceFill([
            'two_factor_secret' => null,
            'two_factor_recovery_codes' => null,
            'two_factor_confirmed_at' => null,
        ])->save();
    }

    public function hasEnabledTwoFactorAuth(): bool
    {
        return $this->two_factor_secret !== null
            && $this->two_factor_confirmed_at !== null;
    }

    public function twoFactorQrCodeSvg(): string
    {
        if (! $this->two_factor_secret) {
            return '';
        }

        return TwoFactorAuthentication::generateQrCodeSvg(
            $this->email,
            $this->two_factor_secret
        );
    }
}
```

## Registering Mixins

### In Service Provider

```php
use App\Mixins\RequestMixin;
use Illuminate\Http\Request;

public function boot(): void
{
    Request::mixin(new RequestMixin);
}
```

## Using Traits in Models

```php
use App\Models\Concerns\HasUuid;
use App\Support\TwoFactorAuthentication\Concerns\TwoFactorAuthenticatable;

/**
 * @use TwoFactorAuthenticatable<User>
 */
final class User extends Authenticatable
{
    use HasUuid, TwoFactorAuthenticatable;
}
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't forget @mixin on mixins
final class RequestMixin // ❌ Missing @mixin

// Don't skip PHPDoc on closure return type
public function getSorts(): Closure
{
    return function (): array { // ❌ Missing PHPDoc
        return [];
    };
}

// Don't use mutable state in mixins
final class RequestMixin
{
    private array $data = []; // ❌ No state

    public function getData(): Closure
    {
        return function (): array {
            return $this->data; // ❌ Refers to mixin, not Request
        };
    }
}

// Don't skip @template on traits
trait HasUuid // ❌ Missing @template
{
}
```

### ✅ Do This Instead

```php
// Include @mixin
/**
 * @mixin Request
 */
final class RequestMixin

// Add PHPDoc to closures
public function getSorts(): Closure
{
    /**
     * @return array<int, array{id: string, desc: bool}>
     */
    return function (): array {
        return [];
    };
}

// Keep mixins stateless
final class RequestMixin
{
    public function getData(): Closure
    {
        return function (): array {
            return $this->query('data'); // ✅ Uses $this = Request
        };
    }
}

// Add @template to traits
/**
 * @template TModel of \Illuminate\Database\Eloquent\Model
 */
trait HasUuid
```

## Quality Standards

- All mixins and traits must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Refactored with Rector
- Covered by tests where applicable
