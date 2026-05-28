# Passport OAuth2

## When to Use Passport

- Third-party applications need API access
- OAuth2 authorization flows required
- Machine-to-machine authentication
- Complex scope management needed

## Installation

```bash
composer require laravel/passport
php artisan passport:install
php artisan passport:keys
```

## Personal Access Tokens

```php
// Generate token
$token = $user->createToken('Personal Access Token', ['orders:read'])->accessToken;

// In controller
$user = auth()->user();
$token = $user->token();  // Current token
```

## Client Credentials Grant (Machine-to-Machine)

```php
// Create client
php artisan passport:client --client

// Request token
POST /oauth/token
{
    "grant_type": "client_credentials",
    "client_id": "client-id",
    "client_secret": "client-secret",
    "scope": "orders:read"
}

// Middleware
Route::middleware('client')->group(function () {
    // Client credentials routes
});
```

## Scopes

```php
// AuthServiceProvider boot()
Passport::tokensCan([
    'orders:read' => 'Read orders',
    'orders:write' => 'Create and update orders',
    'admin' => 'Administrator access',
]);

// Middleware
Route::get('orders', [OrderController::class, 'index'])
    ->middleware(['auth:api', 'scope:orders:read']);

// Check in controller
if ($request->user()->tokenCan('orders:write')) {
    // Allow
}
```

## Token Lifetimes

```php
// AuthServiceProvider boot()
Passport::tokensExpireIn(now()->addDays(15));
Passport::refreshTokensExpireIn(now()->addDays(30));
Passport::personalAccessTokensExpireIn(now()->addMonths(6));
```
