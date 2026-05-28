# Eloquent Patterns

## Query Optimization

### Column Selection

Always use `select()` to limit columns and reduce memory usage:

```php
// Bad - loads all columns
$users = User::all();

// Good - loads only needed columns
$users = User::select(['id', 'name', 'email'])->get();
```

### Eager Loading

Use `with()` to prevent N+1 query problems:

```php
// Bad - N+1 queries
$users = User::all();
foreach ($users as $user) {
    echo $user->posts->count(); // Separate query per user
}

// Good - 2 queries total
$users = User::with('posts')->get();
foreach ($users as $user) {
    echo $user->posts->count();
}
```

### Selective Eager Loading

Load only necessary columns from related models:

```php
User::select(['id', 'name', 'email'])
    ->with(['posts:id,user_id,title', 'profile:user_id,bio'])
    ->get();
```

### Counting Relationships

Use `withCount()` instead of loading relations just to count:

```php
// Bad - loads all comments
$users = User::with('comments')->get();
$count = $users->first()->comments->count();

// Good - only counts
$users = User::withCount('comments')->get();
$count = $users->first()->comments_count;
```

### Large Datasets

Use `chunk()` or `lazy()` for large datasets to reduce memory usage:

```php
// For processing in batches
User::where('active', true)
    ->chunk(100, function ($users) {
        foreach ($users as $user) {
            // Process user
        }
    });

// For iterating with generators (Laravel 8+)
foreach (User::lazy() as $user) {
    // Process one user at a time
}
```

### Complete Optimization Example

```php
User::select(['id', 'name', 'email'])
    ->with(['posts:id,user_id,title'])
    ->withCount('comments')
    ->where('active', true)
    ->orderBy('created_at', 'desc')
    ->lazy();
```

## Relationships

### Define Inverse Relationships

Always define both sides of relationships:

```php
// User model
public function posts(): HasMany
{
    return $this->hasMany(Post::class);
}

// Post model
public function user(): BelongsTo
{
    return $this->belongsTo(User::class);
}
```

### Many-to-Many with Pivot

Use `withTimestamps()` on pivot tables:

```php
public function roles(): BelongsToMany
{
    return $this->belongsToMany(Role::class)
        ->withTimestamps()
        ->withPivot('assigned_by', 'expires_at');
}
```

### Through Relationships

Use `hasOneThrough` and `hasManyThrough` instead of nested queries:

```php
// Country -> User -> Post
public function posts(): HasManyThrough
{
    return $this->hasManyThrough(Post::class, User::class);
}
```

## Scopes

### Local Scopes

Create reusable query logic with local scopes:

```php
// User model
public function scopeActive($query)
{
    return $query->where('active', true);
}

public function scopeRecent($query, int $days = 7)
{
    return $query->where('created_at', '>=', now()->subDays($days));
}

// Usage
User::active()->recent(30)->get();
```

### Scope Naming Convention

Name scopes as adjectives or descriptive states:
- `scopeActive` (not `scopeGetActive`)
- `scopeRecent` (not `scopeGetRecent`)
- `scopePublished` (not `scopeIsPublished`)

### Global Scopes

Use global scopes for constraints that apply to all queries:

```php
class ActiveScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('active', true);
    }
}

// In model
protected static function booted(): void
{
    static::addGlobalScope(new ActiveScope);
}
```

## Accessors and Mutators

### Accessors (Laravel 9+)

Use attribute casting for accessors:

```php
use Illuminate\Database\Eloquent\Casts\Attribute;

protected function fullName(): Attribute
{
    return Attribute::make(
        get: fn () => "{$this->first_name} {$this->last_name}",
    );
}

// Usage
$user->full_name;
```

### Mutators

Use mutators to transform data before saving:

```php
protected function password(): Attribute
{
    return Attribute::make(
        set: fn ($value) => bcrypt($value),
    );
}
```

## Casting

Define attribute casts for automatic type conversion:

```php
protected $casts = [
    'email_verified_at' => 'datetime',
    'is_admin' => 'boolean',
    'settings' => 'array',
    'balance' => 'decimal:2',
];
```
