---
name: creating-api-resources
description: Create Laravel JSON API Resource classes for formatting HTTP responses with type safety. Use when creating API resources, formatting JSON responses, transforming models to JSON, or when user mentions API resources, JSON responses, resource transformers, or response formatting.
---

# Create Laravel API Resources

Create JSON API Resource classes that transform Eloquent models into consistent HTTP responses. Resources provide type-safe formatting for both single models and collections, with built-in support for pagination and conditional attribute inclusion.

## Quick Reference

**Create a resource:**

- Single model: `UserResource::make($user)`
- Collection: `UserResource::collection($users)`
- Paginated: `UserResource::collection($users->paginate())`

**Inertia usage:**

```php
Inertia::render('page', [
    'user' => UserResource::make($user),
    'users' => UserResource::collection($users),
]);
```

**Common methods:**

- `when($condition, $value)` - Conditional attributes
- `whenLoaded('relation')` - Conditional relationships (N+1 prevention)
- `whenCounted('relation')` - Relationship counts
- `mergeWhen($condition, [...])` - Multiple conditional attributes
- `whenNotNull($value)` - Null-safe conditionals

## File Structure

```
app/Http/Resources/{Model}Resource.php
```

Examples:

- `app/Http/Resources/UserResource.php`
- `app/Http/Resources/OrderResource.php`

## Core Conventions

### Resource Structure

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use App\Models\{Model};
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Override;

/**
 * @mixin {Model}
 */
final class {Model}Resource extends JsonResource
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
            'created_at' => $this->created_at?->toAtomString(),
        ];
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final class` modifier
- Add `@mixin` PHPDoc for IDE support
- Use `#[Override]` attribute on `toArray()`
- Type hint return as `array<string, mixed>`
- Format dates with `toAtomString()` consistently

### Attribute Organization

Organize with core model properties first, then relationships:

```php
public function toArray(Request $request): array
{
    return [
        // Core attributes
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'status' => $this->status->value,
        'created_at' => $this->created_at?->toAtomString(),

        // Relationships (each group separated by blank line)
        'posts' => PostResource::collection($this->whenLoaded('posts')),
        'posts_count' => $this->whenCounted('posts'),

        'comments' => CommentResource::collection($this->whenLoaded('comments')),
        'comments_count' => $this->whenCounted('comments'),

        'team' => TeamResource::make($this->whenLoaded('team')),
    ];
}
```

**Key principles:**

- Core model attributes always first
- Blank line separates core from relationships
- Include both collection and count for many relationships
- Each relationship group separated by blank line
- Singular relationships don't need counts

## Data Wrapping Behavior

This project has `JsonResource::withoutWrapping()` enabled.

**Single resources** return unwrapped:

```json
{
  "id": 1,
  "name": "John Doe"
}
```

**Paginated responses** still wrap automatically with `data`, `links`, and `meta`.

## Resource Collections

**Use `UserResource::collection()` when:**

- Simple list transformation
- Standard pagination
- Default response structure

**Create custom `UserCollection extends ResourceCollection` when:**

- Need custom meta data
- Custom top-level response structure

## Common Patterns

### Pattern 1: Optional Relationships

Use `whenLoaded()` to prevent N+1 queries:

```php
'posts' => PostResource::collection($this->whenLoaded('posts')),
'posts_count' => $this->whenCounted('posts'),
```

**Controller usage:**

```php
// Without relationships - posts not included
$users = User::query()->paginate();

// With relationships - posts included
$user->load('posts');

// With counts only
$users = User::query()->withCount('posts')->paginate();
```

### Pattern 2: Conditional Attributes

```php
'middle_name' => $this->whenNotNull($this->middle_name),
'is_admin' => $this->when($request->user()?->isAdmin(), true),

// Multiple conditional attributes
$this->mergeWhen($request->user()?->isAdmin(), [
    'internal_notes' => $this->internal_notes,
    'last_login_ip' => $this->last_login_ip,
]),
```

### Pattern 3: Controller Integration

```php
public function index(): Response
{
    $users = User::query()
        ->withCount(['posts', 'comments'])
        ->paginate(15);

    return Inertia::render('users/index', [
        'users' => UserResource::collection($users),
    ]);
}

public function show(User $user): Response
{
    $user->load(['posts', 'comments', 'team'])
         ->loadCount(['posts', 'comments']);

    return Inertia::render('users/show', [
        'user' => UserResource::make($user),
    ]);
}
```

## Anti-Patterns

### Don't Do This

```php
// Missing @mixin
final class UserResource extends JsonResource // ❌

// Missing #[Override]
public function toArray(Request $request): array // ❌

// Return all model attributes
return $this->resource->toArray(); // ❌ Explicit fields only

// Inconsistent date formatting
'created_at' => $this->created_at, // ❌ Format dates
'updated_at' => $this->updated_at->format('Y-m-d'), // ❌ Use toAtomString()

// Use new instead of ::make()
'user' => new UserResource($this->user), // ❌ Use ::make()

// Eager load inside resources (N+1)
'posts' => PostResource::collection($this->posts), // ❌ Use whenLoaded()

// Mix attributes and relationships
'id' => $this->id,
'posts' => ..., // ❌ Keep relationships at end
'name' => $this->name,

// Forget relationship counts
'posts' => PostResource::collection($this->whenLoaded('posts')), // ❌ Add posts_count
```

### Do This Instead

```php
/**
 * @mixin User
 */
final class UserResource extends JsonResource
{
    #[Override]
    public function toArray(Request $request): array
    {
        return [
            // Core attributes first
            'id' => $this->id,
            'name' => $this->name,
            'created_at' => $this->created_at?->toAtomString(),

            // Relationships at end
            'posts' => PostResource::collection($this->whenLoaded('posts')),
            'posts_count' => $this->whenCounted('posts'),
        ];
    }
}
```

## Quality Standards

- All Resources must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Consistent date formatting with `toAtomString()`
- Consistent instantiation with `::make()` and `::collection()`
- Feature tests for all resources

## References

- `references/examples.md` - Full production-ready resource examples
- `references/testing.md` - Feature test examples for resources
