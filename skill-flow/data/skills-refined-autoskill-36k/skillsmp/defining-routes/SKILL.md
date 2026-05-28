---
name: defining-routes
description: Define Laravel routes following RESTful conventions with proper grouping, middleware, and naming. Use when defining routes, creating endpoints, routing requests, or when user mentions routes, routing, endpoints, or route definition.
---

# Define Laravel Routes

Define RESTful routes with proper grouping, middleware, and naming conventions. Routes connect HTTP requests to controllers, organized by purpose in separate files for web, API, and authentication endpoints.

## File Structure

Routes are organized by purpose:

```
routes/web.php       # Web routes (Inertia pages)
routes/api.php       # API routes (JSON responses)
routes/auth.php      # Authentication routes
routes/console.php   # Console commands
routes/channels.php  # Broadcast channels
```

## Core Conventions

### 1. Route Definition Structure

```php
<?php

declare(strict_types=1);

use App\Http\Controllers\{Domain}\{Name}Controller;
use Illuminate\Support\Facades\Route;

Route::get('/', [HomeController::class, 'index'])
    ->name('home');

Route::middleware(['auth', 'verified'])->group(function (): void {
    Route::controller(ResourceController::class)->group(function (): void {
        Route::get('resource', 'index')->name('resource.index');
        Route::post('resource', 'store')->name('resource.store');
    });
});
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Import controller classes at top
- Use `Route` facade
- Name all routes with `->name()`
- Type hint closure parameters as `void`
- Group related routes
- Use RESTful conventions

### 2. RESTful Route Names

```php
Route::get('posts', 'index')->name('posts.index');           // GET
Route::get('posts/create', 'create')->name('posts.create');  // GET
Route::post('posts', 'store')->name('posts.store');          // POST
Route::get('posts/{post}', 'show')->name('posts.show');      // GET
Route::get('posts/{post}/edit', 'edit')->name('posts.edit'); // GET
Route::put('posts/{post}', 'update')->name('posts.update');  // PUT/PATCH
Route::delete('posts/{post}', 'destroy')->name('posts.destroy'); // DELETE
```

### 3. Middleware Groups

```php
Route::middleware(['auth', 'verified'])->group(function (): void {
    // Routes requiring authentication and email verification
});

Route::middleware('guest')->group(function (): void {
    // Routes for guests only
});
```

## Examples

### Example 1: Basic Route Structure

```php
<?php

declare(strict_types=1);

use App\Http\Controllers\Account\AccountAvatarController;
use App\Http\Controllers\Account\AccountController;
use App\Http\Controllers\Account\AccountPreferencesController;
use App\Http\Controllers\Account\AccountSecurityController;
use App\Http\Controllers\DashboardController;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Route;

Route::get('/', fn (): RedirectResponse => to_route('login'));

Route::middleware(['auth', 'verified'])->group(function (): void {
    Route::controller(AccountAvatarController::class)->group(function (): void {
        Route::put('account/avatar', 'update')->name('account.avatar.update');
        Route::delete('account/avatar', 'destroy')->name('account.avatar.destroy');
    });

    Route::controller(AccountController::class)->group(function (): void {
        Route::get('account', 'edit')->name('account.edit');
        Route::put('account', 'update')->name('account.update');
        Route::delete('account', 'destroy')->name('account.destroy');
    });

    Route::controller(AccountPreferencesController::class)->group(function (): void {
        Route::get('account/preferences', 'edit')->name('account.preferences.edit');
        Route::put('account/preferences', 'update')->name('account.preferences.update');
    });

    Route::controller(AccountSecurityController::class)->group(function (): void {
        Route::get('account/security', 'edit')->name('account.security.edit');
    });

    Route::controller(DashboardController::class)->group(function (): void {
        Route::get('dashboard', 'index')->name('dashboard.index');
    });
});

require __DIR__.'/auth.php';
```

### Example 2: API Routes

```php
<?php

declare(strict_types=1);

use App\Http\Controllers\Api\UserController;
use Illuminate\Support\Facades\Route;

Route::prefix('v1')->middleware('auth:sanctum')->group(function (): void {
    Route::controller(UserController::class)->prefix('users')->group(function (): void {
        Route::get('/', 'index')->name('api.users.index');
        Route::post('/', 'store')->name('api.users.store');
        Route::get('{user}', 'show')->name('api.users.show');
        Route::put('{user}', 'update')->name('api.users.update');
        Route::delete('{user}', 'destroy')->name('api.users.destroy');
    });
});
```

### Example 3: Resource Routes

```php
<?php

declare(strict_types=1);

use App\Http\Controllers\PostController;
use Illuminate\Support\Facades\Route;

// All RESTful routes
Route::resource('posts', PostController::class)
    ->middleware('auth');

// Only specific routes
Route::resource('posts', PostController::class)
    ->only(['index', 'show'])
    ->middleware('auth');

// Except specific routes
Route::resource('posts', PostController::class)
    ->except(['destroy'])
    ->middleware('auth');
```

### Example 4: Route Model Binding

```php
<?php

declare(strict_types=1);

use App\Http\Controllers\PostController;
use App\Models\Post;
use Illuminate\Support\Facades\Route;

// Automatic binding (by ID)
Route::get('posts/{post}', [PostController::class, 'show'])
    ->name('posts.show');

// Custom binding (by slug)
Route::get('posts/{post:slug}', [PostController::class, 'show'])
    ->name('posts.show');

// Scoped binding
Route::get('users/{user}/posts/{post}', [PostController::class, 'show'])
    ->scopeBindings()
    ->name('users.posts.show');
```

### Example 5: Grouped Routes with Prefixes

```php
<?php

declare(strict_types=1);

use App\Http\Controllers\Admin\DashboardController;
use App\Http\Controllers\Admin\UserController;
use Illuminate\Support\Facades\Route;

Route::prefix('admin')
    ->middleware(['auth', 'admin'])
    ->name('admin.')
    ->group(function (): void {
        Route::get('/', [DashboardController::class, 'index'])
            ->name('dashboard');

        Route::controller(UserController::class)->prefix('users')->group(function (): void {
            Route::get('/', 'index')->name('users.index');
            Route::get('{user}', 'show')->name('users.show');
        });
    });
```

### Example 6: Authentication Routes (auth.php)

```php
<?php

declare(strict_types=1);

use App\Http\Controllers\Auth\AuthenticatedSessionController;
use App\Http\Controllers\Auth\EmailVerificationNotificationController;
use App\Http\Controllers\Auth\EmailVerificationPromptController;
use App\Http\Controllers\Auth\NewPasswordController;
use App\Http\Controllers\Auth\PasswordResetLinkController;
use App\Http\Controllers\Auth\RegisteredUserController;
use App\Http\Controllers\Auth\VerifyEmailController;
use Illuminate\Support\Facades\Route;

Route::middleware('guest')->group(function (): void {
    Route::controller(RegisteredUserController::class)->group(function (): void {
        Route::get('register', 'create')->name('register');
        Route::post('register', 'store');
    });

    Route::controller(AuthenticatedSessionController::class)->group(function (): void {
        Route::get('login', 'create')->name('login');
        Route::post('login', 'store');
    });

    Route::controller(PasswordResetLinkController::class)->group(function (): void {
        Route::get('forgot-password', 'create')->name('password.request');
        Route::post('forgot-password', 'store')->name('password.email');
    });

    Route::controller(NewPasswordController::class)->group(function (): void {
        Route::get('reset-password/{token}', 'create')->name('password.reset');
        Route::post('reset-password', 'store')->name('password.store');
    });
});

Route::middleware('auth')->group(function (): void {
    Route::get('verify-email', EmailVerificationPromptController::class)
        ->name('verification.notice');

    Route::get('verify-email/{id}/{hash}', VerifyEmailController::class)
        ->middleware(['signed', 'throttle:6,1'])
        ->name('verification.verify');

    Route::post('email/verification-notification', EmailVerificationNotificationController::class)
        ->middleware('throttle:6,1')
        ->name('verification.send');

    Route::post('logout', [AuthenticatedSessionController::class, 'destroy'])
        ->name('logout');
});
```

## Route Helpers

### Generating URLs

```php
// Named route
route('posts.show', ['post' => 1]);
// Output: https://example.com/posts/1

// Named route with query params
route('posts.index', ['sort' => 'name']);
// Output: https://example.com/posts?sort=name

// To route (redirects)
to_route('dashboard');
```

### Checking Current Route

```php
// In Blade
@if(request()->routeIs('posts.index'))
    <!-- Active -->
@endif

// In Controllers
if (request()->routeIs('posts.*')) {
    // All posts routes
}
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't use closures for complex logic
Route::get('/', function () { // ❌ Use controller
    $users = User::all();
    return view('home', ['users' => $users]);
});

// Don't skip route names
Route::get('posts', [PostController::class, 'index']); // ❌ Add ->name()

// Don't skip type hints on closures
Route::group(function () { // ❌ Type hint : void

// Don't use inconsistent naming
Route::get('user-profile', ...)->name('userProfile'); // ❌ Use kebab-case URL, dot notation name

// Don't define routes in controllers
class PostController {
    public function __construct() {
        Route::get('posts', ...); // ❌ Define in routes file
    }
}

// Don't skip middleware
Route::get('admin/dashboard', ...); // ❌ Add auth middleware
```

### ✅ Do This Instead

```php
// Use controller methods
Route::get('/', [HomeController::class, 'index']);

// Name all routes
Route::get('posts', [PostController::class, 'index'])
    ->name('posts.index');

// Type hint closures
Route::group(function (): void {

// Use consistent naming
Route::get('user-profile', ...)->name('user.profile');

// Define routes in route files
// routes/web.php
Route::get('posts', [PostController::class, 'index']);

// Apply middleware
Route::get('admin/dashboard', ...)
    ->middleware(['auth', 'admin']);
```

## Quality Standards

- All route files must pass PHPStan level 8
- Code formatted with Pint
- All routes must be named
- Use RESTful conventions
- Group related routes
- Apply appropriate middleware
- Use route model binding
- Type hint all closures
