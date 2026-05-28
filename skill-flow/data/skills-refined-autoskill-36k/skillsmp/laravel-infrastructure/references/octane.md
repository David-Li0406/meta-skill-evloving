# Octane Deep Dive

## Memory Management

### What Causes Leaks

```php
// BAD: Static property accumulating data
class CacheService
{
    private static array $items = [];  // Grows with each request!
    
    public function add(string $key, mixed $value): void
    {
        self::$items[$key] = $value;
    }
}

// GOOD: Use proper cache or request-scoped
class CacheService
{
    public function __construct(
        private Repository $cache
    ) {}
    
    public function add(string $key, mixed $value): void
    {
        $this->cache->put($key, $value, 60);
    }
}
```

### Flushing Singletons

```php
// config/octane.php
'flush' => [
    // Reset these between requests
    App\Services\ShoppingCart::class,
    App\Services\UserPreferences::class,
],

'warm' => [
    // Pre-resolve on worker boot
    App\Services\HeavyService::class,
],
```

## Concurrent Tasks

```php
use Laravel\Octane\Facades\Octane;

// Run tasks concurrently
[$users, $orders] = Octane::concurrently([
    fn () => User::all(),
    fn () => Order::all(),
]);
```

## Ticks (Periodic Tasks)

```php
// In Octane::boot() or service provider
Octane::tick('metrics', fn () => Metrics::record())
    ->seconds(10);
```

## Tables (Shared Memory)

```php
use Laravel\Octane\Facades\Octane;

// Store in shared memory (accessible by all workers)
Octane::table('cache')->set('key', ['value' => 'data']);

$data = Octane::table('cache')->get('key');
```

## Common Issues

### Request State Bleeding

```php
// BAD: Modifying request during handling
public function handle(Request $request)
{
    $request->merge(['processed' => true]);  // Stays for next request!
}

// GOOD: Use fresh data each time
public function handle(Request $request)
{
    $data = array_merge($request->all(), ['processed' => true]);
}
```

### Service Container Issues

```php
// BAD: Storing request in singleton
class UserService
{
    public function __construct(
        public Request $request  // Same request object reused!
    ) {}
}

// GOOD: Get fresh request
class UserService
{
    public function getCurrentUser(): ?User
    {
        return request()->user();
    }
}
```

## Performance Tips

```bash
# Start with optimal settings
php artisan octane:start \
    --workers=4 \
    --task-workers=6 \
    --max-requests=500

# Reload after deployment
php artisan octane:reload
```
