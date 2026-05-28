---
name: creating-middleware
description: Create Laravel HTTP middleware for request/response processing. Use when creating middleware, filtering requests, modifying responses, or when user mentions middleware, request filters, or HTTP processing.
---

# Create Laravel Middleware

Create HTTP middleware for request/response processing, filtering, and modification. Middleware intercepts requests before they reach controllers, enabling cross-cutting concerns like authentication, locale setting, and response transformation.

## File Structure

```
app/Http/Middleware/{Name}.php
```

**Examples:**

- `app/Http/Middleware/SetLocale.php`
- `app/Http/Middleware/HandleInertiaRequests.php`
- `app/Http/Middleware/EnsureUserIsAdmin.php`

## Core Conventions

### 1. Middleware Structure

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

final class {Name}
{
    public function handle(Request $request, Closure $next): Response
    {
        // Before logic

        $response = $next($request);

        // After logic

        return $response;
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final class` modifier
- `handle()` method with Request, Closure, and Response types
- Call `$next($request)` to continue pipeline
- Return Response

### 2. Registration

Register in `bootstrap/app.php`:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'set.locale' => \App\Http\Middleware\SetLocale::class,
    ]);
})
```

## Examples

### Example 1: Request Modification

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use App\Support\Localisation\Localisation;
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

final class SetLocale
{
    public function __construct(
        private Localisation $localisation
    ) {}

    public function handle(Request $request, Closure $next): Response
    {
        $locale = $request->user()?->language
            ?? $this->localisation->getDefaultLocale();

        app()->setLocale($locale);

        return $next($request);
    }
}
```

### Example 2: Response Modification (Inertia)

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Inertia\Middleware;
use Symfony\Component\HttpFoundation\Response;

final class HandleInertiaRequests extends Middleware
{
    public function share(Request $request): array
    {
        return [
            ...parent::share($request),
            'auth' => [
                'user' => $request->user()
                    ? UserResource::make($request->user())
                    : null,
            ],
            'flash' => [
                'success' => $request->session()->get('success'),
                'error' => $request->session()->get('error'),
            ],
        ];
    }
}
```

### Example 3: Authorization Check

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

final class EnsureUserIsAdmin
{
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->isAdmin()) {
            abort(403, 'Access denied.');
        }

        return $next($request);
    }
}
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't forget to call $next()
public function handle(Request $request, Closure $next): Response
{
    // Do something
    return response('Done'); // ❌ Must call $next()
}

// Don't put business logic here
public function handle(Request $request, Closure $next): Response
{
    User::create([...]); // ❌ Use Action in controller
    return $next($request);
}

// Don't skip type hints
public function handle($request, $next) // ❌ Type hint
```

### ✅ Do This Instead

```php
// Always call $next()
public function handle(Request $request, Closure $next): Response
{
    $response = $next($request);
    return $response;
}

// Keep logic simple
public function handle(Request $request, Closure $next): Response
{
    if (! $request->user()) {
        return redirect('login');
    }
    return $next($request);
}

// Full type hints
public function handle(Request $request, Closure $next): Response
```

## Quality Standards

- All middleware must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Refactored with Rector
- Covered by feature tests
