# Controller Examples

Complete working examples demonstrating controller patterns.

## Contents

- [Resource Controller](#resource-controller)
- [Nested Resource Controller](#nested-resource-controller)
- [QueryBuilder Controller](#querybuilder-controller)
- [Pivot Resource Controller](#pivot-resource-controller)
- [Invokable Controller](#invokable-controller)
- [API Controller](#api-controller)

---

## Resource Controller

From the codebase: `app/Http/Controllers/Auth/RegisteredUserController.php`

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\Auth;

use App\Actions\Auth\RegisterUserAction;
use App\Http\Controllers\Controller;
use App\Http\Requests\Auth\RegisterRequest;
use Illuminate\Http\RedirectResponse;
use Inertia\Inertia;
use Inertia\Response;

final class RegisteredUserController extends Controller
{
    public function create(): Response
    {
        return Inertia::render('auth/register');
    }

    public function store(
        RegisterRequest $request,
        RegisterUserAction $action
    ): RedirectResponse {
        $user = $action->handle($request->toDTO());

        auth('web')->login($user);

        $request->session()->regenerate();  // Security: Prevent session fixation

        return redirect('dashboard');
    }
}
```

**Key Points:**

- Only 2 methods: `create()` and `store()`
- Delegates to `RegisterUserAction` for business logic
- Session regeneration for security after login
- Type-safe with FormRequest and typed returns

---

## Nested Resource Controller

Example of "properties edited independently" pattern:

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\Account;

use App\Actions\User\UpdateUserPhoneAction;
use App\Http\Controllers\Controller;
use App\Http\Requests\Account\UpdatePhoneRequest;
use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Http\RedirectResponse;
use App\Models\User;

final class AccountPhoneController extends Controller
{
    public function update(
        UpdatePhoneRequest $request,
        #[CurrentUser] User $user,
        UpdateUserPhoneAction $action
    ): RedirectResponse {
        $action->handle($user, $request->toDTO());

        return back();
    }

    public function destroy(
        #[CurrentUser] User $user,
        UpdateUserPhoneAction $action
    ): RedirectResponse {
        $action->handle($user, new UpdateUserPhoneData(phone: null));

        return back();
    }
}
```

**Key Points:**

- Phone number edited separately from main account details
- Uses `#[CurrentUser]` for type-safe authenticated user
- Both `update` and `destroy` use same Action with different DTOs
- Follows "nested resource" pattern (account -> phone)

---

## QueryBuilder Controller

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Http\Resources\UserResource;
use App\Models\User;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Inertia\Response;
use Spatie\QueryBuilder\QueryBuilder;

final class DashboardController extends Controller
{
    public function index(Request $request): Response
    {
        $users = QueryBuilder::for(User::class)
            ->allowedFilters(['name', 'email'])
            ->allowedSorts(['name', 'created_at'])
            ->paginate($request->integer('per_page', 10))
            ->withQueryString();

        return Inertia::render('dashboard/index', [
            'users' => UserResource::collection($users),
        ]);
    }
}
```

**Note:** For advanced QueryBuilder patterns (search callbacks, DateFilter, dynamic operators, `getSorts()`/`getFilters()` helpers), see `app/Http/Controllers/DashboardController.php` in the codebase.

---

## Pivot Resource Controller

Treating a many-to-many relationship as its own resource:

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Actions\Subscription\SubscribeAction;
use App\Actions\Subscription\UnsubscribeAction;
use App\Http\Controllers\Controller;
use App\Models\Podcast;
use App\Models\User;
use Illuminate\Http\RedirectResponse;
use Inertia\Inertia;
use Inertia\Response;

final class UserPodcastSubscriptionController extends Controller
{
    // List user's podcast subscriptions
    public function index(User $user): Response
    {
        $subscriptions = $user->podcastSubscriptions()
            ->with('podcast')
            ->get();

        return Inertia::render('subscriptions/index', [
            'subscriptions' => $subscriptions,
        ]);
    }

    // Subscribe user to podcast
    public function store(
        User $user,
        Podcast $podcast,
        SubscribeAction $action
    ): RedirectResponse {
        $action->handle($user, $podcast);

        return back();
    }

    // Unsubscribe user from podcast
    public function destroy(
        User $user,
        Podcast $podcast,
        UnsubscribeAction $action
    ): RedirectResponse {
        $action->handle($user, $podcast);

        return back();
    }
}
```

**Routes:**

```php
Route::get('/users/{user}/subscriptions', [UserPodcastSubscriptionController::class, 'index']);
Route::post('/users/{user}/podcasts/{podcast}/subscription', [UserPodcastSubscriptionController::class, 'store']);
Route::delete('/users/{user}/podcasts/{podcast}/subscription', [UserPodcastSubscriptionController::class, 'destroy']);
```

**Key Points:**

- Treats `user_podcast` pivot as its own resource: "subscription"
- All route parameters are type-hinted and auto-resolved
- Each method follows RESTful conventions
- Business logic delegated to Actions

---

## Invokable Controller

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Actions\Report\GenerateReportAction;
use App\Http\Controllers\Controller;
use App\Http\Requests\GenerateReportRequest;
use Illuminate\Http\RedirectResponse;

final class GenerateReportController extends Controller
{
    public function __invoke(
        GenerateReportRequest $request,
        GenerateReportAction $action
    ): RedirectResponse {
        $report = $action->handle($request->toDTO());

        return redirect()->route('reports.show', $report);
    }
}
```

**Route:**

```php
Route::post('/reports/generate', GenerateReportController::class);
```

**When to use:** Single-purpose operations that don't fit standard CRUD pattern.

---

## API Controller

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\Api\V1;

use App\Actions\User\CreateUserAction;
use App\Http\Controllers\Controller;
use App\Http\Requests\Api\V1\StoreUserRequest;
use App\Http\Resources\V1\UserResource;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Symfony\Component\HttpFoundation\Response;

final class UserController extends Controller
{
    public function index(): JsonResponse
    {
        $users = User::paginate(15);

        return UserResource::collection($users)->response();
    }

    public function store(
        StoreUserRequest $request,
        CreateUserAction $action
    ): JsonResponse {
        $user = $action->handle($request->toDTO());

        return UserResource::make($user)
            ->response()
            ->setStatusCode(Response::HTTP_CREATED);
    }

    public function show(User $user): UserResource
    {
        return UserResource::make($user);
    }

    public function update(
        User $user,
        UpdateUserRequest $request,
        UpdateUserAction $action
    ): UserResource {
        $user = $action->handle($user, $request->toDTO());

        return UserResource::make($user);
    }

    public function destroy(User $user): JsonResponse
    {
        $user->delete();

        return response()->noContent();
    }
}
```

**Note:** This is a versioned API controller under `Api/V1/` namespace.
