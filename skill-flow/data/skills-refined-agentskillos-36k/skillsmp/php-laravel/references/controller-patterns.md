# Controller Patterns

## Resource Controllers

### Generate Resource Controllers

Use artisan to generate REST-compliant controllers:

```bash
php artisan make:controller UserController --resource
```

### REST Conventions

Follow strict REST conventions:

| Method | URI | Action | Purpose |
|--------|-----|--------|---------|
| GET | /users | index | List all users |
| GET | /users/create | create | Show create form |
| POST | /users | store | Create new user |
| GET | /users/{id} | show | Show single user |
| GET | /users/{id}/edit | edit | Show edit form |
| PUT/PATCH | /users/{id} | update | Update user |
| DELETE | /users/{id} | destroy | Delete user |

### HTTP Status Codes

Return proper HTTP status codes:

```php
// 200 OK - successful GET, PUT, PATCH
return response()->json($data, 200);

// 201 Created - successful POST
return response()->json($user, 201);

// 204 No Content - successful DELETE
return response()->noContent();

// 400 Bad Request - validation failed
return response()->json(['errors' => $errors], 400);

// 401 Unauthorized - authentication failed
return response()->json(['message' => 'Unauthorized'], 401);

// 403 Forbidden - authorization failed
return response()->json(['message' => 'Forbidden'], 403);

// 404 Not Found - resource not found
return response()->json(['message' => 'Not found'], 404);

// 422 Unprocessable Entity - validation errors
return response()->json(['errors' => $validator->errors()], 422);

// 500 Internal Server Error
return response()->json(['message' => 'Server error'], 500);
```

## Thin Controllers

Keep controller methods under 10 lines by delegating to services:

```php
class UserController extends Controller
{
    public function __construct(
        private readonly UserService $users
    ) {}

    public function store(StoreUserRequest $request)
    {
        $user = $this->users->create($request->validated());
        return response()->json($user, 201);
    }

    public function update(UpdateUserRequest $request, User $user)
    {
        $updated = $this->users->update($user, $request->validated());
        return response()->json($updated);
    }

    public function destroy(User $user)
    {
        $this->users->delete($user);
        return response()->noContent();
    }
}
```

## Form Requests

### Generate Form Requests

```bash
php artisan make:request StoreUserRequest
```

### Structure

Always use Form Requests for validation, never validate in controllers:

```php
class StoreUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', User::class);
    }

    public function rules(): array
    {
        return [
            'email' => ['required', 'email', 'unique:users'],
            'password' => ['required', Password::defaults()],
            'name' => ['required', 'string', 'max:255'],
        ];
    }

    public function messages(): array
    {
        return [
            'email.unique' => 'This email is already registered.',
            'password.required' => 'A password is required.',
        ];
    }

    public function attributes(): array
    {
        return [
            'email' => 'email address',
        ];
    }
}
```

### Authorization Logic

Place authorization in `authorize()` method:

```php
public function authorize(): bool
{
    // Check if user can create resources
    return $this->user()->can('create', User::class);

    // Check if user can update specific resource
    $user = $this->route('user');
    return $this->user()->can('update', $user);

    // Check role-based permission
    return $this->user()->hasRole('admin');
}
```

### Custom Validation Rules

```php
public function rules(): array
{
    return [
        'email' => [
            'required',
            'email',
            Rule::unique('users')->ignore($this->user),
        ],
        'role' => ['required', Rule::in(['admin', 'user', 'guest'])],
        'age' => ['required', 'integer', 'min:18', 'max:120'],
    ];
}
```

### Preparing Data

Use `prepareForValidation()` to transform input before validation:

```php
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->title),
        'user_id' => auth()->id(),
    ]);
}
```

## Route Model Binding

### Implicit Binding

```php
// Route
Route::get('/users/{user}', [UserController::class, 'show']);

// Controller - User is automatically resolved
public function show(User $user)
{
    return response()->json($user);
}
```

### Custom Key

```php
// In User model
public function getRouteKeyName(): string
{
    return 'slug';
}

// Now /users/{slug} works
```

### Explicit Binding

```php
// In RouteServiceProvider
Route::bind('user', function ($value) {
    return User::where('slug', $value)->firstOrFail();
});
```

## API Resources

Use API Resources to transform models for JSON responses:

```php
php artisan make:resource UserResource
```

```php
class UserResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at->toDateTimeString(),
            'posts_count' => $this->posts_count,
            'posts' => PostResource::collection($this->whenLoaded('posts')),
        ];
    }
}
```

Usage:

```php
return UserResource::collection($users);
return new UserResource($user);
```
