---
name: laravel-api
description: Build RESTful APIs with Eloquent API Resources, pagination, versioning, and rate limiting. Use this when creating API endpoints or transforming data for JSON responses.
allowed-tools: Bash,Read,Write,Edit,Glob,Grep
---

# Laravel API Development

Build production-ready RESTful APIs following Laravel best practices and conventions.

## Discovery

**Check existing API setup:**
1. Look for existing API routes in `routes/api.php`
2. Check `app/Http/Resources/` for existing Resource patterns
3. Review middleware in `bootstrap/app.php` for API-specific settings
4. Determine if API versioning is used (e.g., `v1/`, `v2/` prefixes)

**Follow existing conventions!**

## Workflow

### 1. Create Resources

```bash
php artisan make:resource [Model]Resource --no-interaction
php artisan make:resource [Model]Collection --no-interaction  # Optional
```

**Basic Resource:**
```php
namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class PostResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'slug' => $this->slug,
            'published_at' => $this->published_at?->toISOString(),
            'author' => new UserResource($this->whenLoaded('author')),
            'tags' => TagResource::collection($this->whenLoaded('tags')),
            'created_at' => $this->created_at->toISOString(),
        ];
    }
}
```

**Resource Collection (optional):**
```php
namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class PostCollection extends ResourceCollection
{
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total' => $this->total(),
                'count' => $this->count(),
            ],
        ];
    }
}
```

### 2. Create Controller

```bash
php artisan make:controller Api/[Model]Controller --api --no-interaction
```

**RESTful Controller Pattern:**
```php
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\{Store[Model]Request, Update[Model]Request};
use App\Http\Resources\{[Model]Resource, [Model]Collection};
use App\Models\[Model];
use Illuminate\Http\{JsonResponse, Response};

class [Model]Controller extends Controller
{
    public function index(): [Model]Collection
    {
        $items = [Model]::query()
            ->with(['author', 'tags'])  // Eager load!
            ->latest()
            ->paginate(20);

        return new [Model]Collection($items);
    }

    public function store(Store[Model]Request $request): JsonResponse
    {
        $item = [Model]::create($request->validated());

        return (new [Model]Resource($item))
            ->response()
            ->setStatusCode(201);
    }

    public function show([Model] $item): [Model]Resource
    {
        $item->load(['author', 'tags']);
        return new [Model]Resource($item);
    }

    public function update(Update[Model]Request $request, [Model] $item): [Model]Resource
    {
        $item->update($request->validated());
        return new [Model]Resource($item->fresh());
    }

    public function destroy([Model] $item): Response
    {
        $item->delete();
        return response()->noContent();
    }
}
```

### 3. Create Form Requests

```bash
php artisan make:request Api/Store[Model]Request --no-interaction
```

```php
namespace App\Http\Requests\Api;

use Illuminate\Foundation\Http\FormRequest;

class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return auth()->check();
    }

    public function rules(): array
    {
        return [
            'title' => 'required|string|max:255',
            'slug' => 'required|string|unique:posts,slug',
            'content' => 'required|string',
            'category_id' => 'required|exists:categories,id',
            'tags' => 'array',
            'tags.*' => 'exists:tags,id',
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'A post title is required',
            'slug.unique' => 'This slug is already in use',
        ];
    }
}
```

### 4. Define Routes

```php
// routes/api.php
use App\Http\Controllers\Api\PostController;

// Simple resource routing
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('posts', PostController::class);
});

// Manual routes with versioning
Route::prefix('v1')->group(function () {
    Route::get('/posts', [PostController::class, 'index']);
    Route::post('/posts', [PostController::class, 'store'])->middleware('auth:sanctum');
    Route::get('/posts/{post}', [PostController::class, 'show']);
    Route::put('/posts/{post}', [PostController::class, 'update'])->middleware('auth:sanctum');
    Route::delete('/posts/{post}', [PostController::class, 'destroy'])->middleware('auth:sanctum');
});
```

### 5. Write Tests

```php
use App\Models\{User, Post};

test('creates post with valid data', function () {
    $user = User::factory()->create();
    $token = $user->createToken('test')->plainTextToken;

    $response = $this->withToken($token)
        ->postJson('/api/posts', [
            'title' => 'Test Post',
            'slug' => 'test-post',
            'content' => 'Test content',
        ]);

    $response->assertCreated()
        ->assertJsonFragment(['title' => 'Test Post']);

    expect(Post::where('title', 'Test Post')->exists())->toBeTrue();
});

test('validates required fields', function () {
    $user = User::factory()->create();
    $token = $user->createToken('test')->plainTextToken;

    $response = $this->withToken($token)->postJson('/api/posts', []);

    $response->assertUnprocessable()
        ->assertJsonValidationErrors(['title', 'slug', 'content']);
});
```

**For more test examples, see:** `references/testing-examples.md`

## Pagination

### Standard Pagination

```php
public function index(): JsonResponse
{
    $posts = Post::with('author')
        ->latest()
        ->paginate(20);  // or paginate($request->input('per_page', 20))

    return PostResource::collection($posts)->response();
}
```

**Response format:**
```json
{
    "data": [...],
    "links": {
        "first": "http://api.example.com/posts?page=1",
        "last": "http://api.example.com/posts?page=5",
        "prev": null,
        "next": "http://api.example.com/posts?page=2"
    },
    "meta": {
        "current_page": 1,
        "per_page": 20,
        "total": 100
    }
}
```

### Cursor Pagination (real-time data)

```php
$posts = Post::latest('id')->cursorPaginate(20);
return PostResource::collection($posts)->response();
```

## Response Patterns

### Success Responses

```php
// 200 OK
return new PostResource($post);

// 201 Created
return (new PostResource($post))
    ->response()
    ->setStatusCode(201);

// 204 No Content
return response()->noContent();

// Custom JSON
return response()->json([
    'message' => 'Post published successfully',
    'data' => new PostResource($post),
], 200);
```

### Error Responses

```php
// 404 Not Found
return response()->json(['message' => 'Post not found'], 404);

// 422 Validation Error (automatic with Form Requests)

// 403 Forbidden
return response()->json(['message' => 'Unauthorized'], 403);
```

## Authentication (Sanctum)

### Setup

```bash
php artisan install:api --no-interaction
```

### Issue Tokens

```php
public function login(LoginRequest $request): JsonResponse
{
    $user = User::where('email', $request->email)->first();

    if (!$user || !Hash::check($request->password, $user->password)) {
        return response()->json(['message' => 'Invalid credentials'], 401);
    }

    $token = $user->createToken('api-token')->plainTextToken;

    return response()->json([
        'token' => $token,
        'user' => new UserResource($user),
    ]);
}
```

### Protect Routes

```php
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('posts', PostController::class);
});

// Get current user
Route::get('/user', function (Request $request) {
    return new UserResource($request->user());
})->middleware('auth:sanctum');
```

## Best Practices

### Resource Optimization

```php
// ✅ Use whenLoaded to avoid N+1
'author' => new UserResource($this->whenLoaded('author')),

// ✅ Use when for conditional fields
'is_featured' => $this->when($request->user()?->isAdmin(), $this->is_featured),

// ✅ Hide sensitive data
'email' => $this->when($request->user()?->id === $this->id, $this->email),
```

### Eager Loading

```php
// ✅ Always eager load relationships
$posts = Post::with(['author', 'tags'])->paginate(20);

// ❌ Never do this (N+1 queries)
$posts = Post::paginate(20);
// Then in resource: new UserResource($this->author) - N+1!
```

### Response Consistency

```php
// ✅ Consistent date formatting
'created_at' => $this->created_at->toISOString(),

// ✅ Explicit null handling
'published_at' => $this->published_at?->toISOString(),

// ✅ Consistent naming (snake_case for JSON)
'comments_count' => $this->comments_count,
```

## Advanced Topics

For advanced patterns, see references:

- **Rate limiting** → `references/rate-limiting.md`
- **Filtering & searching** → `references/filtering-searching.md`
- **Comprehensive test examples** → `references/testing-examples.md`

## Quick Reference

### HTTP Status Codes

| Code | Method | Usage |
|------|--------|-------|
| 200 | GET, PUT, PATCH | Success |
| 201 | POST | Resource created |
| 204 | DELETE | Success, no content |
| 401 | * | Unauthenticated |
| 403 | * | Forbidden |
| 404 | GET, PUT, PATCH, DELETE | Not found |
| 422 | POST, PUT, PATCH | Validation failed |
| 429 | * | Rate limit exceeded |

### Resource Methods

| Method | Route | Controller Method | Description |
|--------|-------|-------------------|-------------|
| GET | `/posts` | `index()` | List all |
| POST | `/posts` | `store()` | Create new |
| GET | `/posts/{id}` | `show()` | Show one |
| PUT/PATCH | `/posts/{id}` | `update()` | Update |
| DELETE | `/posts/{id}` | `destroy()` | Delete |

## Output Checklist

- ✅ **API Resources** created for all models
- ✅ **Form Requests** validate all inputs
- ✅ **Eager loading** prevents N+1 queries
- ✅ **Rate limiting** configured (if needed)
- ✅ **Authentication** with Sanctum (if needed)
- ✅ **Pagination** on list endpoints
- ✅ **Tests** cover all endpoints
- ✅ **Consistent responses** (dates, naming, structure)

## Important Reminders

- **ALWAYS** use API Resources (never return models directly)
- **ALWAYS** use Form Requests for validation
- **ALWAYS** eager load relationships to prevent N+1
- **ALWAYS** paginate list endpoints
- **ALWAYS** use `whenLoaded()` in resources
- **NEVER** expose sensitive data in responses
- **NEVER** return models directly (use Resources)
- **CHECK** existing API patterns before creating new ones
