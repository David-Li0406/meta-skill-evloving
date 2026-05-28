---
name: managing-models
description: Create and modify Eloquent models with PHPDoc properties, casts, relationships, and virtual properties. Use when creating models, defining relationships, managing database models, or when user mentions models, Eloquent, database models, or model properties.
---

# Manage Laravel Eloquent Models

Create and modify Eloquent models with PHPDoc properties, casts, relationships, and virtual properties. Models represent database tables with full type safety via PHPDoc annotations, enabling IDE autocompletion and static analysis.

## File Structure

Models are stored in the Models directory:

```
app/Models/{Model}.php
```

**Examples:**

- `app/Models/User.php`
- `app/Models/Order.php`
- `app/Models/Product.php`

## Core Conventions

### 1. Model Structure

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Carbon\CarbonImmutable;
use Database\Factories\{Model}Factory;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Override;

/**
 * @property int $id
 * @property string $name
 * @property ?CarbonImmutable $created_at
 * @property ?CarbonImmutable $updated_at
 */
final class {Model} extends Model
{
    /**
     * @use HasFactory<{Model}Factory>
     */
    use HasFactory;

    #[Override]
    protected function casts(): array
    {
        return [
            'created_at' => 'immutable_datetime',
            'updated_at' => 'immutable_datetime',
        ];
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final class` modifier
- PHPDoc with all `@property` annotations
- Use `CarbonImmutable` for dates
- Type hint `HasFactory` with factory class
- Use `#[Override]` on `casts()` method
- Return array from `casts()` method (not property)

### 2. PHPDoc Properties

Document ALL database columns and virtual properties:

```php
/**
 * @property int $id
 * @property string $name
 * @property string $email
 * @property string $password
 * @property ?string $remember_token
 * @property ?CarbonImmutable $email_verified_at
 * @property ?CarbonImmutable $created_at
 * @property ?CarbonImmutable $updated_at
 */
final class User extends Authenticatable
```

### 3. Virtual Properties (PHP 8.4+)

```php
public ?string $avatarUrl {
    get => $this->avatar_path ? Storage::url($this->avatar_path) : null;
}

public string $firstName {
    get => Str::before($this->name, ' ');
}
```

### 4. Casts

```php
#[Override]
protected function casts(): array
{
    return [
        'email_verified_at' => 'immutable_datetime',
        'password' => 'hashed',
        'two_factor_secret' => 'encrypted',
        'two_factor_recovery_codes' => 'encrypted:array',
        'is_active' => 'boolean',
        'settings' => 'array',
        'status' => OrderStatus::class,
    ];
}
```

## Examples

### Example 1: User Model

```php
<?php

declare(strict_types=1);

namespace App\Models;

use App\Support\TwoFactorAuthentication\Concerns\TwoFactorAuthenticatable;
use Carbon\CarbonImmutable;
use Database\Factories\UserFactory;
use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\MassPrunable;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use Override;

/**
 * @property int $id
 * @property string $name
 * @property string $email
 * @property string $language
 * @property string $password
 * @property ?string $two_factor_secret
 * @property ?list<string> $two_factor_recovery_codes
 * @property ?string $remember_token
 * @property ?string $avatar_path
 * @property ?CarbonImmutable $email_verified_at
 * @property ?CarbonImmutable $two_factor_confirmed_at
 * @property ?CarbonImmutable $created_at
 * @property ?CarbonImmutable $updated_at
 */
final class User extends Authenticatable implements MustVerifyEmail
{
    /**
     * @use HasFactory<UserFactory>
     * @use TwoFactorAuthenticatable<User>
     */
    use HasFactory, MassPrunable, Notifiable, TwoFactorAuthenticatable;

    public ?string $avatarUrl {
        get => $this->avatar_path ? Storage::url($this->avatar_path) : null;
    }

    public string $firstName {
        get => Str::before($this->name, ' ');
    }

    protected $hidden = [
        'password',
        'two_factor_secret',
        'two_factor_recovery_codes',
        'remember_token',
    ];

    /**
     * @var array<string, mixed>
     */
    protected $attributes = [
        'language' => 'en',
        'avatar_path' => null,
    ];

    /**
     * @return Builder<self>
     */
    public function prunable(): Builder
    {
        return self::query()
            ->whereNull('email_verified_at')
            ->where('created_at', '<=', now()->subDay());
    }

    #[Override]
    protected function casts(): array
    {
        return [
            'email_verified_at' => 'immutable_datetime',
            'password' => 'hashed',
            'two_factor_secret' => 'encrypted',
            'two_factor_recovery_codes' => 'encrypted:array',
            'two_factor_confirmed_at' => 'immutable_datetime',
        ];
    }
}
```

### Example 2: Model with Relationships

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Carbon\CarbonImmutable;
use Database\Factories\OrderFactory;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Override;

/**
 * @property int $id
 * @property int $user_id
 * @property string $status
 * @property int $total
 * @property ?CarbonImmutable $created_at
 * @property ?CarbonImmutable $updated_at
 *
 * @property-read User $user
 * @property-read \Illuminate\Database\Eloquent\Collection<int, OrderItem> $items
 */
final class Order extends Model
{
    /**
     * @use HasFactory<OrderFactory>
     */
    use HasFactory;

    /**
     * @return BelongsTo<User, self>
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * @return HasMany<OrderItem, self>
     */
    public function items(): HasMany
    {
        return $this->hasMany(OrderItem::class);
    }

    #[Override]
    protected function casts(): array
    {
        return [
            'status' => OrderStatus::class,
            'total' => 'integer',
            'created_at' => 'immutable_datetime',
            'updated_at' => 'immutable_datetime',
        ];
    }
}
```

### Example 3: Model with Scopes

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Carbon\CarbonImmutable;
use Database\Factories\PostFactory;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Override;

/**
 * @property int $id
 * @property string $title
 * @property bool $is_published
 * @property ?CarbonImmutable $published_at
 * @property ?CarbonImmutable $created_at
 * @property ?CarbonImmutable $updated_at
 */
final class Post extends Model
{
    /**
     * @use HasFactory<PostFactory>
     */
    use HasFactory;

    /**
     * @param  Builder<self>  $query
     * @return Builder<self>
     */
    public function scopePublished(Builder $query): Builder
    {
        return $query->where('is_published', true);
    }

    /**
     * @param  Builder<self>  $query
     * @return Builder<self>
     */
    public function scopeRecent(Builder $query): Builder
    {
        return $query->orderBy('published_at', 'desc');
    }

    #[Override]
    protected function casts(): array
    {
        return [
            'is_published' => 'boolean',
            'published_at' => 'immutable_datetime',
            'created_at' => 'immutable_datetime',
            'updated_at' => 'immutable_datetime',
        ];
    }
}
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't skip PHPDoc properties
final class User extends Model // ❌ Missing @property docs
{
}

// Don't use Carbon instead of CarbonImmutable
/**
 * @property Carbon $created_at // ❌ Use CarbonImmutable
 */

// Don't use $casts property
protected $casts = [ // ❌ Use casts() method
    'created_at' => 'datetime',
];

// Don't skip type hints on relationships
public function user() // ❌ Type hint return
{
    return $this->belongsTo(User::class);
}

// Don't forget #[Override] attribute
protected function casts(): array // ❌ Missing #[Override]

// Don't use mutable classes
class User extends Model // ❌ Use final class
```

### ✅ Do This Instead

```php
// Include full PHPDoc
/**
 * @property int $id
 * @property string $name
 * @property ?CarbonImmutable $created_at
 */
final class User extends Model

// Use CarbonImmutable
/**
 * @property ?CarbonImmutable $created_at
 */

// Use casts() method
#[Override]
protected function casts(): array
{
    return ['created_at' => 'immutable_datetime'];
}

// Type hint relationships
/**
 * @return BelongsTo<User, self>
 */
public function user(): BelongsTo

// Add #[Override] attribute
#[Override]
protected function casts(): array

// Use final class
final class User extends Model
```

## Quality Standards

- All models must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Refactored with Rector
- All properties documented in PHPDoc
- All relationships type hinted
