---
name: creating-controllers
description: Create thin Laravel controllers that delegate to Actions for business logic. Use when creating controllers, handling HTTP requests, routing logic, or when user mentions controllers, HTTP handlers, or request handling.
---

# Create Laravel Controllers

Create thin controllers that delegate business logic to Actions, following RESTful conventions. Controllers handle HTTP concerns like request validation, response formatting, and authorization, while Actions contain the actual business logic.

## File Structure

### Web Controllers (Inertia.js)

```
app/Http/Controllers/{Domain}/{Name}Controller.php
```

### API Controllers

```
app/Http/Controllers/Api/V1/{Domain}/{Name}Controller.php
```

## Core Conventions

### 1. Controller Structure

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\{Domain};

use App\Actions\{Domain}\{Name}Action;
use App\Http\Controllers\Controller;
use App\Http\Requests\{Domain}\{Name}Request;
use Illuminate\Http\RedirectResponse;
use Inertia\Inertia;
use Inertia\Response;

final class {Name}Controller extends Controller
{
    public function index(): Response
    {
        return Inertia::render('{domain}/{page}');
    }

    public function store(
        {Name}Request $request,
        {Name}Action $action
    ): RedirectResponse {
        $result = $action->handle($request->toDTO());

        return redirect()->route('resource.index');
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final class` modifier
- Extend base `Controller` class
- Inject Form Requests for validation
- Inject Actions for business logic
- Keep methods thin (3-7 lines typical)

### 2. Middleware Declaration (Laravel 11+)

```php
use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

final class VerifiedEmailController extends Controller implements HasMiddleware
{
    public static function middleware(): array
    {
        return [
            new Middleware(['signed', 'throttle:6,1'], only: ['store']),
        ];
    }
}
```

### 3. RESTful Actions (Cruddy by Design)

Use only the 7 standard actions:

- `index()` - Display list
- `create()` - Show create form
- `store()` - Store new resource
- `show()` - Display single resource
- `edit()` - Show edit form
- `update()` - Update resource
- `destroy()` - Delete resource

**If you need a custom action, create a new controller instead.** See [references/cruddy-design.md](references/cruddy-design.md) for detailed patterns.

### 4. Dependency Injection

**Method Injection (Preferred for Actions):**

```php
public function store(
    RegisterRequest $request,
    RegisterUserAction $action
): RedirectResponse {
    $user = $action->handle($request->toDTO());
    return redirect('dashboard');
}
```

**CurrentUser Attribute:**

```php
use Illuminate\Container\Attributes\CurrentUser;

public function update(
    #[CurrentUser] User $user,
    UpdateAccountRequest $request,
    UpdateAccountAction $action
): RedirectResponse {
    $action->handle($user, $request->toDTO());
    return back();
}
```

### 5. Invokable Controllers

For single-action controllers:

```php
final class ProvisionServerController extends Controller
{
    public function __invoke(
        ProvisionServerRequest $request,
        ProvisionServerAction $action
    ): RedirectResponse {
        $server = $action->handle($request->toDTO());
        return redirect()->route('servers.show', $server);
    }
}
```

**Route:** `Route::post('/server', ProvisionServerController::class);`

### 6. Inertia Rendering

```php
public function edit(User $user): Response
{
    return Inertia::render('account/general', [
        'user' => UserResource::make($user),
    ]);
}
```

- Page names match route structure: `auth/register`, `account/general`
- Always pass data through API Resources

## Response Types

### Inertia Responses

```php
use Inertia\Response;

public function create(): Response
{
    return Inertia::render('page/name', ['prop' => $value]);
}
```

### Redirect Responses

```php
use Illuminate\Http\RedirectResponse;

public function store(): RedirectResponse
{
    return redirect()->route('resource.index');
    return back();
}
```

### JSON Responses (API)

See [references/api-controllers.md](references/api-controllers.md) for API response patterns.

## Anti-Patterns

### Don't Do This

```php
// Don't put business logic in controllers
public function store(Request $request)
{
    $user = User::create([...]); // Use Action
    Mail::send(...);             // Use Action
}

// Don't inject Request directly for validation
public function store(Request $request) // Use FormRequest
{
    $validated = $request->validate([...]);
}

// Don't add custom actions
final class PodcastsController extends Controller
{
    public function updateCoverImage($id) { }   // Custom action
    public function listEpisodes($id) { }       // Custom action
}
```

### Do This Instead

```php
// Delegate to Actions
public function store(
    RegisterRequest $request,
    RegisterUserAction $action
): RedirectResponse {
    $user = $action->handle($request->toDTO());
    return redirect('dashboard');
}

// Use Form Requests
public function store(RegisterRequest $request)

// Create new controllers with standard actions
final class PodcastCoverImageController extends Controller
{
    public function update($id) { }
}

final class PodcastEpisodesController extends Controller
{
    public function index($id) { }
}
```

## Quality Standards

- All controllers must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Covered by feature tests (see `writing-feature-tests` skill)
- Follow Cruddy by Design: only 7 standard RESTful actions
- Delegate all business logic to Actions
- Use Form Requests with `toDTO()` for validation

## References

- [references/examples.md](references/examples.md) - Complete working controller examples
- [references/cruddy-design.md](references/cruddy-design.md) - Detailed Cruddy by Design patterns
- [references/api-controllers.md](references/api-controllers.md) - API controller patterns and responses
