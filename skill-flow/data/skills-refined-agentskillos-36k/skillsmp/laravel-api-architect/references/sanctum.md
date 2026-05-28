# Sanctum Authentication

## Token Authentication

```php
// Generate token with abilities
$token = $user->createToken('api-token', ['orders:read', 'orders:write']);
$plainTextToken = $token->plainTextToken;

// Check abilities in controller
if ($request->user()->tokenCan('orders:write')) {
    // Allow write operation
}

// Revoke tokens
$user->currentAccessToken()->delete();      // Current token
$user->tokens()->delete();                   // All tokens
```

## Protected Routes

```php
// routes/api.php
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('orders', OrderController::class);
    Route::post('logout', [AuthController::class, 'logout']);
});

// Optional auth (guest or authenticated)
Route::middleware('auth:sanctum')->group(function () {
    Route::get('profile', [ProfileController::class, 'show']);
});
```

## Login/Register Flow

```php
<?php


namespace App\Http\Controllers\Api;

use App\Http\Requests\LoginRequest;
use App\Http\Requests\RegisterRequest;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;
use Symfony\Component\HttpFoundation\Response;

final class AuthController extends Controller
{
    public function register(RegisterRequest $request): JsonResponse
    {
        $user = User::query()->create([
            'name' => $request->validated('name'),
            'email' => $request->validated('email'),
            'password' => Hash::make($request->validated('password')),
        ]);

        $token = $user->createToken('api-token')->plainTextToken;

        return response()->json([
            'user' => new UserResource($user),
            'token' => $token,
        ], Response::HTTP_CREATED);
    }

    public function login(LoginRequest $request): JsonResponse
    {
        $user = User::query()
            ->where('email', $request->validated('email'))
            ->first();

        if (! $user || ! Hash::check($request->validated('password'), $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['The provided credentials are incorrect.'],
            ]);
        }

        $token = $user->createToken('api-token')->plainTextToken;

        return response()->json([
            'user' => new UserResource($user),
            'token' => $token,
        ]);
    }

    public function logout(): JsonResponse
    {
        auth()->user()->currentAccessToken()->delete();

        return response()->json(null, Response::HTTP_NO_CONTENT);
    }
}
```

## Token Abilities (Scopes)

```php
// Define abilities when creating token
$token = $user->createToken('api-token', [
    'orders:read',
    'orders:write', 
    'profile:read',
    'profile:write',
]);

// Middleware for ability check
Route::get('orders', [OrderController::class, 'index'])
    ->middleware('ability:orders:read');

Route::post('orders', [OrderController::class, 'store'])
    ->middleware('ability:orders:write');

// Multiple abilities (all required)
Route::middleware('abilities:orders:read,orders:write');
```

## Rate Limiting

```php
// bootstrap/app.php
->withMiddleware(function (Middleware $middleware) {
    $middleware->api([
        'throttle:api',
    ]);
})

// routes/api.php - Custom rate limit
Route::middleware('throttle:60,1')->group(function () {
    // 60 requests per minute
});
```
