---
name: creating-seeders
description: Create Laravel database seeder classes for populating databases with test or default data. Use when creating seeders, seeding databases, populating test data, or when user mentions seeders, database seeding, or sample data.
---

# Create Laravel Database Seeders

Create database seeder classes for populating databases with test or default data. Seeders use factories to generate realistic data, running via `php artisan db:seed` for development or `migrate:fresh --seed` for complete rebuilds.

## File Structure

Seeders are stored in database/seeders:

```
database/seeders/DatabaseSeeder.php
database/seeders/{Model}Seeder.php
```

**Examples:**

- `database/seeders/DatabaseSeeder.php` - Main seeder
- `database/seeders/UserSeeder.php`
- `database/seeders/ProductSeeder.php`

## Core Conventions

### 1. Seeder Structure

```php
<?php

declare(strict_types=1);

namespace Database\Seeders;

use App\Models\{Model};
use Illuminate\Database\Seeder;

final class {Model}Seeder extends Seeder
{
    public function run(): void
    {
        {Model}::factory()->count(10)->create();
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final class` modifier
- Extend `Seeder` base class
- Implement `run()` method
- Use factories for data generation
- Type hint `run()` return as `void`

### 2. Using Factories

```php
public function run(): void
{
    // Create multiple records
    User::factory()->count(100)->create();

    // Create with specific attributes
    User::factory()->create([
        'email' => 'admin@example.com',
    ]);

    // Create with states
    User::factory()->count(50)->unverified()->create();
}
```

### 3. Calling Other Seeders

```php
public function run(): void
{
    $this->call([
        UserSeeder::class,
        ProductSeeder::class,
        OrderSeeder::class,
    ]);
}
```

## Examples

### Example 1: Simple DatabaseSeeder

```php
<?php

declare(strict_types=1);

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;

final class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        User::factory()->create([
            'name' => 'Test User',
            'email' => 'test@example.com',
        ]);
    }
}
```

### Example 2: UserSeeder with Multiple Users

```php
<?php

declare(strict_types=1);

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;

final class UserSeeder extends Seeder
{
    public function run(): void
    {
        // Create admin user
        User::factory()->create([
            'name' => 'Admin User',
            'email' => 'admin@example.com',
            'role' => 'admin',
        ]);

        // Create regular users
        User::factory()->count(50)->create();

        // Create unverified users
        User::factory()->count(10)->unverified()->create();

        // Create users with two-factor auth
        User::factory()->count(5)->withTwoFactorAuth()->create();
    }
}
```

### Example 3: Seeder with Relationships

```php
<?php

declare(strict_types=1);

namespace Database\Seeders;

use App\Models\Order;
use App\Models\User;
use Illuminate\Database\Seeder;

final class OrderSeeder extends Seeder
{
    public function run(): void
    {
        // Get all users
        $users = User::all();

        // Create orders for each user
        $users->each(function (User $user): void {
            Order::factory()
                ->count(rand(1, 5))
                ->forUser($user)
                ->create();
        });

        // Create some completed orders
        Order::factory()
            ->count(20)
            ->completed()
            ->create();

        // Create some cancelled orders
        Order::factory()
            ->count(5)
            ->cancelled()
            ->create();
    }
}
```

### Example 4: DatabaseSeeder Calling Multiple Seeders

```php
<?php

declare(strict_types=1);

namespace Database\Seeders;

use Illuminate\Database\Seeder;

final class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
            CategorySeeder::class,
            ProductSeeder::class,
            OrderSeeder::class,
        ]);
    }
}
```

### Example 5: Conditional Seeding

```php
<?php

declare(strict_types=1);

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;

final class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // Only seed in local environment
        if (app()->isLocal()) {
            User::factory()->count(100)->create();

            $this->call([
                ProductSeeder::class,
                OrderSeeder::class,
            ]);
        }

        // Always create admin user
        User::factory()->create([
            'name' => 'Admin',
            'email' => 'admin@example.com',
            'role' => 'admin',
        ]);
    }
}
```

### Example 6: Seeder with Progress Feedback

```php
<?php

declare(strict_types=1);

namespace Database\Seeders;

use App\Models\Product;
use Illuminate\Database\Seeder;

final class ProductSeeder extends Seeder
{
    public function run(): void
    {
        $this->command?->info('Creating products...');

        Product::factory()->count(1000)->create();

        $this->command?->info('Products created successfully!');
    }
}
```

## Using Seeders

### Run All Seeders

```bash
php artisan db:seed
```

### Run Specific Seeder

```bash
php artisan db:seed --class=UserSeeder
```

### Fresh Migration with Seeders

```bash
php artisan migrate:fresh --seed
```

### In Tests

```php
public function test_example(): void
{
    $this->seed();

    // Or specific seeder
    $this->seed(UserSeeder::class);
}
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't create data manually
public function run(): void
{
    User::create([ // ❌ Use factory
        'name' => 'John Doe',
        'email' => 'john@example.com',
        'password' => bcrypt('password'),
    ]);
}

// Don't skip type hints
public function run() // ❌ Type hint : void
{
}

// Don't use mutable class
class UserSeeder extends Seeder // ❌ Use final class
{
}

// Don't hardcode many records
public function run(): void
{
    User::create(['name' => 'User 1', ...]); // ❌ Use factory
    User::create(['name' => 'User 2', ...]);
    User::create(['name' => 'User 3', ...]);
    // ... 100 more times
}

// Don't forget to handle existing data
public function run(): void
{
    User::factory()->count(100)->create(); // May fail if users exist
}
```

### ✅ Do This Instead

```php
// Use factories
public function run(): void
{
    User::factory()->count(100)->create();
}

// Type hint return
public function run(): void

// Use final class
final class UserSeeder extends Seeder

// Use factory with count
public function run(): void
{
    User::factory()->count(100)->create();
}

// Truncate or check for existing data
public function run(): void
{
    if (app()->isLocal()) {
        User::query()->delete();
    }

    User::factory()->count(100)->create();
}
```

## Best Practices

### 1. Idempotent Seeders

Make seeders safe to run multiple times:

```php
public function run(): void
{
    // Delete existing data in development
    if (app()->isLocal()) {
        User::query()->delete();
    }

    User::factory()->count(100)->create();
}
```

### 2. Environment-Specific Seeding

```php
public function run(): void
{
    if (app()->isLocal()) {
        // Large dataset for development
        User::factory()->count(1000)->create();
    } else {
        // Minimal data for production
        User::factory()->create([
            'email' => 'admin@example.com',
        ]);
    }
}
```

### 3. Organized Seeding

```php
final class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // Core data first
        $this->call([
            UserSeeder::class,
            RoleSeeder::class,
        ]);

        // Dependent data second
        $this->call([
            ProductSeeder::class,
            OrderSeeder::class,
        ]);
    }
}
```

## Quality Standards

- All seeders must pass PHPStan level 8
- Code formatted with Pint
- Use factories for data generation
- Idempotent where possible
- Consider environment (local vs production)
- Clear feedback with command info/warn methods
