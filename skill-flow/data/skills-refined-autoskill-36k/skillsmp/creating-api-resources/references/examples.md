# API Resource Examples

Complete, production-ready resource examples.

## Example 1: Simple Resource

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\User;
use App\Support\Localisation\Facades\Localisation;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Override;

/**
 * @mixin User
 */
final class UserResource extends JsonResource
{
    /**
     * @return array<string, mixed>
     */
    #[Override]
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'first_name' => $this->firstName,
            'email' => $this->email,
            'email_verified_at' => $this->email_verified_at?->toAtomString(),
            'two_factor_confirmed_at' => $this->two_factor_confirmed_at?->toAtomString(),
            'language' => Localisation::getIso639Locale($this->language),
            'avatar_url' => $this->avatarUrl,
        ];
    }
}
```

## Example 2: Resource with Relationships

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\Order;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Override;

/**
 * @mixin Order
 */
final class OrderResource extends JsonResource
{
    /**
     * @return array<string, mixed>
     */
    #[Override]
    public function toArray(Request $request): array
    {
        return [
            // Core attributes
            'id' => $this->id,
            'order_number' => $this->order_number,
            'total' => $this->total,
            'status' => $this->status->value,
            'created_at' => $this->created_at?->toAtomString(),
            'updated_at' => $this->updated_at?->toAtomString(),

            // Relationships
            'user' => UserResource::make($this->whenLoaded('user')),

            'items' => OrderItemResource::collection($this->whenLoaded('items')),
            'items_count' => $this->whenCounted('items'),
        ];
    }
}
```

## Example 3: Conditional Attributes

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Override;

/**
 * @mixin User
 */
final class UserResource extends JsonResource
{
    /**
     * @return array<string, mixed>
     */
    #[Override]
    public function toArray(Request $request): array
    {
        return [
            // Core attributes
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'middle_name' => $this->whenNotNull($this->middle_name),
            'is_admin' => $this->when($request->user()?->isAdmin(), true),

            // Admin-only attributes
            $this->mergeWhen($request->user()?->isAdmin(), [
                'internal_notes' => $this->internal_notes,
                'last_login_ip' => $this->last_login_ip,
                'created_by_user_id' => $this->created_by_user_id,
            ]),

            'secret_data' => $this->whenHas('secret_data'),
            'created_at' => $this->created_at?->toAtomString(),
            'updated_at' => $this->updated_at?->toAtomString(),

            // Relationships
            'posts' => PostResource::collection($this->whenLoaded('posts')),
            'posts_count' => $this->whenCounted('posts'),

            'comments' => CommentResource::collection($this->whenLoaded('comments')),
            'comments_count' => $this->whenCounted('comments'),
        ];
    }
}
```

## Example 4: Complete Resource with All Patterns

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Override;

/**
 * @mixin User
 */
final class UserResource extends JsonResource
{
    /**
     * @return array<string, mixed>
     */
    #[Override]
    public function toArray(Request $request): array
    {
        return [
            // Core model attributes
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'status' => $this->status->value,
            'is_verified' => $this->email_verified_at !== null,
            'created_at' => $this->created_at?->toAtomString(),
            'updated_at' => $this->updated_at?->toAtomString(),

            // Many relationship with count
            'posts' => PostResource::collection($this->whenLoaded('posts')),
            'posts_count' => $this->whenCounted('posts'),

            // Another many relationship with count
            'comments' => CommentResource::collection($this->whenLoaded('comments')),
            'comments_count' => $this->whenCounted('comments'),

            // Singular relationship (no count needed)
            'team' => TeamResource::make($this->whenLoaded('team')),
        ];
    }
}
```

## Example 5: Custom Resource Collection

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;
use Override;

final class UserCollection extends ResourceCollection
{
    /**
     * @return array<string, mixed>
     */
    #[Override]
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total_active' => User::where('active', true)->count(),
                'generated_at' => now()->toAtomString(),
            ],
        ];
    }
}
```

Usage:

```php
return new UserCollection(User::paginate());
```

## Controller Integration Examples

### Inertia Controllers

**Single resource:**

```php
use App\Http\Resources\UserResource;
use App\Models\User;
use Inertia\Inertia;
use Inertia\Response;

public function show(User $user): Response
{
    return Inertia::render('users/show', [
        'user' => UserResource::make($user),
    ]);
}
```

**Collection:**

```php
public function index(): Response
{
    return Inertia::render('users/index', [
        'users' => UserResource::collection(User::all()),
    ]);
}
```

**Paginated:**

```php
public function index(): Response
{
    $users = User::query()->paginate(15);

    return Inertia::render('users/index', [
        'users' => UserResource::collection($users),
    ]);
}
```

**With relationships and counts:**

```php
public function index(): Response
{
    // Load counts for index page (show "5 posts" without loading all posts)
    $users = User::query()
        ->withCount(['posts', 'comments'])
        ->paginate(15);

    return Inertia::render('users/index', [
        'users' => UserResource::collection($users),
    ]);
}

public function show(User $user): Response
{
    // Load full relationships for detail page
    $user->load(['posts', 'comments', 'team'])
         ->loadCount(['posts', 'comments']);

    return Inertia::render('users/show', [
        'user' => UserResource::make($user),
    ]);
}
```

### API Controllers

**Single resource:**

```php
use App\Http\Resources\UserResource;
use App\Models\User;

public function show(User $user): UserResource
{
    return UserResource::make($user);
}
```

**Collection:**

```php
use Illuminate\Http\Resources\Json\ResourceCollection;

public function index(): ResourceCollection
{
    return UserResource::collection(User::all());
}
```

**Paginated:**

```php
public function index(): ResourceCollection
{
    return UserResource::collection(User::paginate(15));
}
```

### Paginated List with Filters

```php
use App\Http\Resources\UserResource;
use App\Models\User;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Inertia\Response;

public function index(Request $request): Response
{
    $users = User::query()
        ->when(
            $request->search,
            fn ($query) => $query->where('name', 'like', "%{$request->search}%")
        )
        ->when(
            $request->status,
            fn ($query) => $query->where('status', $request->status)
        )
        ->when(
            $request->role,
            fn ($query) => $query->whereHas('roles', fn ($q) => $q->where('name', $request->role))
        )
        ->paginate(15)
        ->withQueryString(); // Preserve query params in pagination links

    return Inertia::render('users/index', [
        'users' => UserResource::collection($users),
        'filters' => $request->only(['search', 'status', 'role']),
    ]);
}
```
