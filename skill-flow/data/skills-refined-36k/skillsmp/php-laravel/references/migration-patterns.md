# Migration Patterns

## Naming Conventions

### Creating Tables

Format: `create_{table_name}_table`

```bash
php artisan make:migration create_users_table
php artisan make:migration create_posts_table
php artisan make:migration create_user_role_table  # pivot table
```

### Adding Columns

Format: `add_{column_name}_to_{table_name}_table`

```bash
php artisan make:migration add_status_to_orders_table
php artisan make:migration add_bio_and_avatar_to_users_table
```

### Modifying Columns

Format: `modify_{column_name}_in_{table_name}_table` or `change_{description}_in_{table_name}_table`

```bash
php artisan make:migration modify_email_in_users_table
php artisan make:migration change_price_to_decimal_in_products_table
```

### Removing Columns

Format: `drop_{column_name}_from_{table_name}_table` or `remove_{column_name}_from_{table_name}_table`

```bash
php artisan make:migration drop_legacy_id_from_users_table
php artisan make:migration remove_deprecated_columns_from_posts_table
```

### Dropping Tables

Format: `drop_{table_name}_table`

```bash
php artisan make:migration drop_legacy_users_table
```

## Best Practices

### Always Implement Down Method

Provide rollback logic in every migration:

```php
public function up(): void
{
    Schema::create('users', function (Blueprint $table) {
        $table->id();
        $table->string('email')->unique();
        $table->timestamps();
    });
}

public function down(): void
{
    Schema::dropIfExists('users');
}
```

### Foreign Keys

Use `foreignId()->constrained()` for foreign keys:

```php
// Modern approach
$table->foreignId('user_id')->constrained()->onDelete('cascade');

// Equivalent to:
$table->unsignedBigInteger('user_id');
$table->foreign('user_id')->references('id')->on('users')->onDelete('cascade');
```

### Custom Foreign Keys

```php
// Reference different column
$table->foreignId('author_id')->constrained('users');

// Custom constraint name
$table->foreignId('user_id')
    ->constrained()
    ->onDelete('cascade')
    ->name('fk_posts_user');
```

### Indexes

Add indexes on columns used in WHERE, ORDER BY, or JOIN clauses:

```php
$table->string('email')->unique();  // Unique index
$table->string('slug')->index();    // Regular index

// Composite index
$table->index(['user_id', 'created_at']);

// Custom index name
$table->index('email', 'idx_users_email');

// Full-text index (MySQL)
$table->fullText('description');
```

## Common Column Patterns

### Primary Key

```php
$table->id();  // Auto-incrementing BIGINT unsigned
```

### Timestamps

```php
$table->timestamps();           // created_at, updated_at
$table->softDeletes();          // deleted_at
$table->timestamp('published_at')->nullable();
```

### Strings

```php
$table->string('name');              // VARCHAR(255)
$table->string('code', 10);          // VARCHAR(10)
$table->text('description');         // TEXT
$table->longText('content');         // LONGTEXT
```

### Numbers

```php
$table->integer('views');            // INT
$table->bigInteger('population');    // BIGINT
$table->decimal('price', 8, 2);     // DECIMAL(8,2)
$table->float('latitude', 8, 6);    // FLOAT
```

### Booleans

```php
$table->boolean('is_active')->default(true);
```

### JSON

```php
$table->json('settings');
$table->jsonb('metadata');  // PostgreSQL
```

### Enums

```php
// Modern approach (MySQL 8.0.17+)
$table->enum('status', ['draft', 'published', 'archived']);

// Alternative for flexibility
$table->string('status')->default('draft');
```

## Complete Example

```php
public function up(): void
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->string('title');
        $table->string('slug')->unique();
        $table->text('excerpt')->nullable();
        $table->longText('content');
        $table->enum('status', ['draft', 'published', 'archived'])->default('draft');
        $table->timestamp('published_at')->nullable();
        $table->integer('views')->default(0);
        $table->json('meta')->nullable();
        $table->timestamps();
        $table->softDeletes();

        // Indexes
        $table->index(['status', 'published_at']);
        $table->fullText('title');
    });
}

public function down(): void
{
    Schema::dropIfExists('posts');
}
```

## Pivot Tables

### Naming Convention

Alphabetically ordered, singular table names:

```php
// Correct
create_post_tag_table  // post + tag
create_role_user_table // role + user

// Incorrect
create_tags_posts_table
create_user_role_table
```

### Structure

```php
public function up(): void
{
    Schema::create('post_tag', function (Blueprint $table) {
        $table->foreignId('post_id')->constrained()->onDelete('cascade');
        $table->foreignId('tag_id')->constrained()->onDelete('cascade');
        $table->timestamps();  // Optional: for withTimestamps()

        $table->primary(['post_id', 'tag_id']);
    });
}
```

### Pivot with Extra Columns

```php
Schema::create('role_user', function (Blueprint $table) {
    $table->foreignId('role_id')->constrained()->onDelete('cascade');
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->foreignId('assigned_by')->nullable()->constrained('users');
    $table->timestamp('expires_at')->nullable();
    $table->timestamps();

    $table->primary(['role_id', 'user_id']);
});
```

## Modifying Existing Tables

### Adding Columns

```php
public function up(): void
{
    Schema::table('users', function (Blueprint $table) {
        $table->string('phone')->nullable()->after('email');
        $table->boolean('is_verified')->default(false);
    });
}

public function down(): void
{
    Schema::table('users', function (Blueprint $table) {
        $table->dropColumn(['phone', 'is_verified']);
    });
}
```

### Changing Columns

```php
public function up(): void
{
    Schema::table('products', function (Blueprint $table) {
        $table->decimal('price', 10, 2)->change();  // Change precision
        $table->string('name', 500)->change();      // Increase length
    });
}
```

### Renaming Columns

```php
public function up(): void
{
    Schema::table('users', function (Blueprint $table) {
        $table->renameColumn('name', 'full_name');
    });
}

public function down(): void
{
    Schema::table('users', function (Blueprint $table) {
        $table->renameColumn('full_name', 'name');
    });
}
```

## Performance Considerations

### Indexing Strategy

```php
// Good - indexes frequently queried columns
$table->index('email');
$table->index(['user_id', 'created_at']);

// Bad - too many indexes slow down writes
$table->index('every');
$table->index('single');
$table->index('column');
```

### Data Seeding in Migrations

Avoid seeding data in migrations. Use seeders instead:

```php
// Bad
public function up(): void
{
    Schema::create('roles', function (Blueprint $table) {
        // ...
    });

    DB::table('roles')->insert([...]);  // Don't do this
}

// Good - use seeders
php artisan make:seeder RoleSeeder
```
