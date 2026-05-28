---
title: Use API Resources for Transformation
impact: MEDIUM-HIGH
impactDescription: Consistent, maintainable API responses
tags: api, resources, transformation, json
---

## Use API Resources for Transformation

Direct model serialization exposes internal structure and lacks control. API Resources provide consistent, documented response formats.

**Incorrect (direct model return):**

```php
<?php

class UserController extends Controller
{
    public function show(User $user)
    {
        // ❌ Exposes all attributes including sensitive ones
        // ❌ Database column names leak to API
        // ❌ No control over nested relations
        return $user->load('posts');
    }

    public function index()
    {
        // ❌ Inconsistent response format
        return User::all();
    }
}
```

**Correct (API Resources):**

```php
<?php

// app/Http/Resources/UserResource.php
class UserResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'avatar_url' => $this->avatar_url,
            'created_at' => $this->created_at->toISOString(),

            // Conditional attributes
            'email_verified' => $this->when(
                $request->user()?->is_admin,
                $this->email_verified_at !== null
            ),

            // Conditional relations
            'posts' => PostResource::collection(
                $this->whenLoaded('posts')
            ),

            // Computed attributes
            'posts_count' => $this->when(
                $this->posts_count !== null,
                $this->posts_count
            ),
        ];
    }
}

// Controller
class UserController extends Controller
{
    public function show(User $user)
    {
        return new UserResource($user->load('posts'));
    }

    public function index()
    {
        return UserResource::collection(
            User::paginate(15)
        );
    }
}
```

**Resource collections with metadata:**

```php
<?php

class UserCollection extends ResourceCollection
{
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total_users' => User::count(),
                'active_users' => User::where('active', true)->count(),
            ],
        ];
    }
}

// Usage
return new UserCollection(User::paginate(15));
```

**Wrapping and additional data:**

```php
<?php

// Disable wrapping for single resource
UserResource::withoutWrapping();

// Add additional data
return (new UserResource($user))
    ->additional([
        'meta' => [
            'permissions' => $user->permissions,
        ],
    ]);
```

Reference: [API Resources](https://laravel.com/docs/eloquent-resources)
