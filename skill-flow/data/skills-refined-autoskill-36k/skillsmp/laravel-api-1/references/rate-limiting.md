# Rate Limiting

Configure and apply rate limiting to API endpoints.

## Define Rate Limits

Add to `bootstrap/app.php`:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

->withMiddleware(function (Middleware $middleware) {
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });

    RateLimiter::for('api-strict', function (Request $request) {
        return Limit::perMinute(10)->by($request->user()?->id ?: $request->ip());
    });
})
```

## Apply Rate Limiting

```php
// routes/api.php

// Apply to route group
Route::middleware(['throttle:api'])->group(function () {
    Route::get('/posts', [PostController::class, 'index']);
});

// Apply to specific routes
Route::post('/posts', [PostController::class, 'store'])
    ->middleware('throttle:api-strict');
```

## Custom Rate Limits

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});

RateLimiter::for('api-premium', function (Request $request) {
    return $request->user()?->isPremium()
        ? Limit::perMinute(1000)
        : Limit::perMinute(60);
});
```

## Testing Rate Limits

```php
test('rate limits requests', function () {
    $user = User::factory()->create();
    $token = $user->createToken('test')->plainTextToken;

    // Make requests up to rate limit
    for ($i = 0; $i < 61; $i++) {
        $response = $this->withToken($token)->getJson('/api/posts');
    }

    $response->assertStatus(429); // Too Many Requests
});
```
