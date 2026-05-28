---
name: creating-migrations
description: Create Laravel database migrations following conventions for schema changes, indexes, and foreign keys. Use when creating migrations, modifying database schema, adding tables, or when user mentions migrations, database schema, schema changes, or database structure.
---

# Create Laravel Database Migrations

Create database migrations that version schema changes with proper indexes and foreign keys. Migrations run sequentially to evolve the database structure, using timestamped filenames for ordering and descriptive names for clarity.

## File Structure

Migrations are stored in database/migrations:

```
database/migrations/{timestamp}_{description}.php
```

**Examples:**

- `2024_01_01_000000_create_users_table.php`
- `2024_01_02_000000_add_avatar_to_users_table.php`
- `2024_01_03_000000_create_orders_table.php`

## Core Conventions

### 1. Migration Structure

```php
<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('table_name', function (Blueprint $table): void {
            $table->id();
            $table->string('name');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('table_name');
    }
};
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use anonymous class extending `Migration`
- Type hint closure parameter as `Blueprint`
- Type hint closure return as `void`
- Implement both `up()` and `down()` methods
- Use `dropIfExists()` in `down()` method

### 2. Column Types

```php
$table->id();                           // Auto-incrementing primary key
$table->string('email');                // VARCHAR(255)
$table->string('name', 100);            // VARCHAR(100)
$table->text('description');            // TEXT
$table->integer('count');               // INTEGER
$table->boolean('is_active');           // BOOLEAN
$table->timestamp('published_at');      // TIMESTAMP
$table->timestamps();                   // created_at, updated_at
$table->softDeletes();                  // deleted_at
```

### 3. Indexes and Constraints

```php
$table->string('email')->unique();
$table->index('email');
$table->index(['user_id', 'created_at']);

$table->foreignId('user_id')
    ->constrained()
    ->cascadeOnDelete();
```

## Examples

### Example 1: Create Users Table

```php
<?php

declare(strict_types=1);

use App\Support\Localisation\Facades\Localisation;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('users', function (Blueprint $table): void {
            $table->id();
            $table->string('name');
            $table->string('email')->unique();
            $table->string('language')->default(Localisation::getDefaultLocale());
            $table->string('password');
            $table->text('two_factor_secret')->nullable();
            $table->text('two_factor_recovery_codes')->nullable();
            $table->rememberToken();
            $table->string('avatar_path', 2048)->nullable();
            $table->timestamp('email_verified_at')->nullable();
            $table->timestamp('two_factor_confirmed_at')->nullable();
            $table->timestamps();
        });

        Schema::create('password_reset_tokens', function (Blueprint $table): void {
            $table->string('email')->primary();
            $table->string('token');
            $table->timestamp('created_at')->nullable();
        });

        Schema::create('sessions', function (Blueprint $table): void {
            $table->string('id')->primary();
            $table->foreignId('user_id')->nullable()->index();
            $table->string('ip_address', 45)->nullable();
            $table->text('user_agent')->nullable();
            $table->longText('payload');
            $table->integer('last_activity')->index();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('users');
        Schema::dropIfExists('password_reset_tokens');
        Schema::dropIfExists('sessions');
    }
};
```

### Example 2: Create Table with Foreign Keys

```php
<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('orders', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('user_id')
                ->constrained()
                ->cascadeOnDelete();
            $table->string('status')->default('pending');
            $table->integer('total');
            $table->text('notes')->nullable();
            $table->timestamp('completed_at')->nullable();
            $table->timestamp('cancelled_at')->nullable();
            $table->timestamps();

            $table->index(['user_id', 'status']);
            $table->index('created_at');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('orders');
    }
};
```

### Example 3: Add Column to Existing Table

```php
<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table): void {
            $table->string('phone')->nullable()->after('email');
            $table->boolean('is_active')->default(true)->after('email_verified_at');
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table): void {
            $table->dropColumn(['phone', 'is_active']);
        });
    }
};
```

### Example 4: Create Pivot Table

```php
<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('order_product', function (Blueprint $table): void {
            $table->foreignId('order_id')
                ->constrained()
                ->cascadeOnDelete();
            $table->foreignId('product_id')
                ->constrained()
                ->cascadeOnDelete();
            $table->integer('quantity')->default(1);
            $table->integer('price');
            $table->timestamps();

            $table->primary(['order_id', 'product_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('order_product');
    }
};
```

### Example 5: Modify Column

```php
<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table): void {
            $table->string('email', 320)->change();
            $table->text('bio')->nullable()->change();
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table): void {
            $table->string('email', 255)->change();
            $table->string('bio', 500)->nullable()->change();
        });
    }
};
```

## Foreign Key Conventions

```php
// Basic foreign key
$table->foreignId('user_id')->constrained();

// With cascade delete
$table->foreignId('user_id')
    ->constrained()
    ->cascadeOnDelete();

// With cascade update
$table->foreignId('user_id')
    ->constrained()
    ->cascadeOnUpdate();

// With set null
$table->foreignId('user_id')
    ->nullable()
    ->constrained()
    ->nullOnDelete();

// Reference specific table
$table->foreignId('owner_id')
    ->constrained('users')
    ->cascadeOnDelete();
```

## Indexes

```php
// Single column index
$table->index('email');

// Compound index
$table->index(['user_id', 'created_at']);

// Unique index
$table->unique('email');

// Named index
$table->index('email', 'users_email_index');
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't skip type hints on closure
Schema::create('users', function ($table) { // ❌ Type hint Blueprint

// Don't skip return type on closure
Schema::create('users', function (Blueprint $table) { // ❌ Add : void

// Don't use drop() in down()
public function down(): void
{
    Schema::drop('users'); // ❌ Use dropIfExists()
}

// Don't forget indexes
$table->foreignId('user_id')->constrained(); // ❌ Add cascadeOnDelete()

// Don't use class keyword for migration
final class CreateUsersTable extends Migration // ❌ Use anonymous class
{
}

// Don't forget timestamps
$table->id();
$table->string('name');
// ❌ Missing $table->timestamps()
```

### ✅ Do This Instead

```php
// Type hint closure parameter
Schema::create('users', function (Blueprint $table): void {

// Add return type on closure
Schema::create('users', function (Blueprint $table): void {

// Use dropIfExists()
public function down(): void
{
    Schema::dropIfExists('users');
}

// Add appropriate cascades
$table->foreignId('user_id')
    ->constrained()
    ->cascadeOnDelete();

// Use anonymous class
return new class extends Migration
{
}

// Always add timestamps
$table->id();
$table->string('name');
$table->timestamps();
```

## Running Migrations

```bash
# Run migrations
php artisan migrate

# Rollback last batch
php artisan migrate:rollback

# Rollback all migrations
php artisan migrate:reset

# Fresh database (drop all tables)
php artisan migrate:fresh

# Fresh with seeders
php artisan migrate:fresh --seed
```

## Quality Standards

- All migrations must pass PHPStan level 8
- Code formatted with Pint
- Proper foreign key constraints
- Appropriate indexes for query performance
- Reversible migrations (proper `down()` method)
- Named consistently with timestamp prefix
