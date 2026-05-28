---
name: creating-factories
description: Create Laravel model factories with type-safe state methods for generating test data. Use when creating factories, generating test data, seeding databases, or when user mentions factories, test data, fake data, or model factories.
---

# Create Laravel Model Factories

Create model factories with type-safe state methods for generating test data. Factories produce realistic model instances for testing, with composable state methods that configure specific scenarios like admin users or unpublished posts.

## File Structure

Factories are stored in the database/factories directory:

```
database/factories/{Model}Factory.php
```

**Examples:**

- `database/factories/UserFactory.php`
- `database/factories/OrderFactory.php`
- `database/factories/ProductFactory.php`

## Core Conventions

### 1. Factory Structure

```php
<?php

declare(strict_types=1);

namespace Database\Factories;

use App\Models\{Model};
use Illuminate\Database\Eloquent\Factories\Factory;
use Override;

/**
 * @extends Factory<{Model}>
 */
final class {Model}Factory extends Factory
{
    protected $model = {Model}::class;

    #[Override]
    public function definition(): array
    {
        return [
            'field' => fake()->word(),
        ];
    }

    public function stateName(): self
    {
        return $this->state(fn (array $attributes): array => [
            'field' => 'specific-value',
        ]);
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final class` modifier
- Extend `Factory` base class
- Add `@extends Factory<Model>` PHPDoc
- Set `protected $model` property
- Use `#[Override]` on `definition()` method
- Type hint state methods returning `self`
- Use `fake()` helper for fake data

### 2. Definition Method

```php
#[Override]
public function definition(): array
{
    return [
        'name' => fake()->name(),
        'email' => fake()->unique()->safeEmail(),
        'password' => Hash::make('password'),
        'created_at' => now(),
    ];
}
```

### 3. State Methods

```php
public function unverified(): self
{
    return $this->state(fn (array $attributes): array => [
        'email_verified_at' => null,
    ]);
}

public function admin(): self
{
    return $this->state(fn (array $attributes): array => [
        'role' => 'admin',
    ]);
}
```

## Examples

### Example 1: User Factory

```php
<?php

declare(strict_types=1);

namespace Database\Factories;

use App\Models\User;
use App\Support\Localisation\Facades\Localisation;
use App\Support\TwoFactorAuthentication\Facades\TwoFactorAuthentication;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;
use Override;

/**
 * @extends Factory<User>
 */
final class UserFactory extends Factory
{
    protected $model = User::class;

    #[Override]
    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'language' => Localisation::getDefaultLocale(),
            'password' => Hash::make('password'),
            'two_factor_secret' => null,
            'two_factor_recovery_codes' => null,
            'remember_token' => Str::random(10),
            'avatar_path' => null,
            'email_verified_at' => now(),
            'two_factor_confirmed_at' => null,
        ];
    }

    public function unverified(): self
    {
        return $this->state(fn (array $attributes): array => [
            'email_verified_at' => null,
        ]);
    }

    public function withTwoFactorAuth(): self
    {
        return $this->state(fn (array $attributes): array => [
            'two_factor_secret' => TwoFactorAuthentication::generateSecretKey(),
            'two_factor_recovery_codes' => ['recovery-code-1', 'recovery-code-2'],
            'two_factor_confirmed_at' => now(),
        ]);
    }

    public function withUnconfirmedTwoFactorAuth(): self
    {
        return $this->state(fn (array $attributes): array => [
            'two_factor_secret' => TwoFactorAuthentication::generateSecretKey(),
            'two_factor_recovery_codes' => ['recovery-code-1', 'recovery-code-2'],
        ]);
    }

    public function withAvatar(): self
    {
        return $this->state(fn (array $attributes): array => [
            'avatar_path' => UploadedFile::fake()->image('avatar.jpg')->storePublicly('avatars', 'public'),
        ]);
    }
}
```

### Example 2: Factory with Relationships

```php
<?php

declare(strict_types=1);

namespace Database\Factories;

use App\Models\Order;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
use Override;

/**
 * @extends Factory<Order>
 */
final class OrderFactory extends Factory
{
    protected $model = Order::class;

    #[Override]
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'total' => fake()->numberBetween(1000, 100000),
            'status' => 'pending',
            'notes' => fake()->sentence(),
        ];
    }

    public function completed(): self
    {
        return $this->state(fn (array $attributes): array => [
            'status' => 'completed',
            'completed_at' => now(),
        ]);
    }

    public function cancelled(): self
    {
        return $this->state(fn (array $attributes): array => [
            'status' => 'cancelled',
            'cancelled_at' => now(),
        ]);
    }

    public function forUser(User $user): self
    {
        return $this->state(fn (array $attributes): array => [
            'user_id' => $user->id,
        ]);
    }
}
```

### Example 3: Factory with Enums

```php
<?php

declare(strict_types=1);

namespace Database\Factories;

use App\Enums\PostStatus;
use App\Models\Post;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
use Override;

/**
 * @extends Factory<Post>
 */
final class PostFactory extends Factory
{
    protected $model = Post::class;

    #[Override]
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'title' => fake()->sentence(),
            'body' => fake()->paragraphs(3, true),
            'status' => PostStatus::Draft,
            'published_at' => null,
        ];
    }

    public function published(): self
    {
        return $this->state(fn (array $attributes): array => [
            'status' => PostStatus::Published,
            'published_at' => now(),
        ]);
    }

    public function draft(): self
    {
        return $this->state(fn (array $attributes): array => [
            'status' => PostStatus::Draft,
            'published_at' => null,
        ]);
    }
}
```

## Using Factories

### In Tests

```php
// Create single model
$user = User::factory()->create();

// Create with attributes
$user = User::factory()->create([
    'email' => 'test@example.com',
]);

// Create with state
$user = User::factory()->unverified()->create();

// Create multiple
$users = User::factory()->count(10)->create();

// Make without persisting
$user = User::factory()->make();

// Chain states
$user = User::factory()
    ->unverified()
    ->withTwoFactorAuth()
    ->create();
```

### In Seeders

```php
User::factory()->count(100)->create();

Order::factory()
    ->count(50)
    ->completed()
    ->create();
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't skip @extends PHPDoc
final class UserFactory extends Factory // ❌ Missing @extends

// Don't skip #[Override] on definition()
public function definition(): array // ❌ Missing #[Override]

// Don't skip type hint on state methods
public function unverified() // ❌ Type hint return as self
{
    return $this->state([...]);
}

// Don't use actual data in definition()
public function definition(): array
{
    return [
        'email' => 'test@example.com', // ❌ Use fake()
    ];
}

// Don't forget $model property
final class UserFactory extends Factory
{
    // ❌ Missing protected $model
}

// Don't use mutable class
class UserFactory extends Factory // ❌ Use final class
```

### ✅ Do This Instead

```php
// Include @extends PHPDoc
/**
 * @extends Factory<User>
 */
final class UserFactory extends Factory

// Use #[Override] on definition()
#[Override]
public function definition(): array

// Type hint state methods
public function unverified(): self
{
    return $this->state(fn (array $attributes): array => [...]);
}

// Use fake() helper
public function definition(): array
{
    return [
        'email' => fake()->safeEmail(),
    ];
}

// Set $model property
protected $model = User::class;

// Use final class
final class UserFactory extends Factory
```

## Quality Standards

- All factories must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Refactored with Rector
- Use `fake()` for all generated data
- Provide useful state methods for common scenarios
