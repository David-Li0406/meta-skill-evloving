---
id: laravel-patterns
name: "PHP Laravel Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# PHP Laravel Patterns

## Overview

Laravel is a modern PHP framework with elegant syntax and powerful features. This methodology covers Laravel architecture, design patterns, and best practices for building robust applications.

## When to Use

- Full-stack web applications
- API backends
- Queue-based processing
- Applications requiring rapid development
- Projects with complex database relationships

## Key Principles

1. **Convention over configuration** - Follow Laravel conventions
2. **Service container** - Dependency injection and IoC
3. **Eloquent ORM** - Active Record pattern
4. **Middleware** - HTTP layer filtering
5. **Artisan CLI** - Powerful command-line tools

## Best Practices

### Project Structure

```
app/
├── Console/
│   └── Commands/
├── Exceptions/
│   └── Handler.php
├── Http/
│   ├── Controllers/
│   │   └── Api/
│   │       └── V1/
│   ├── Middleware/
│   ├── Requests/
│   └── Resources/
├── Models/
├── Services/
├── Repositories/
├── Actions/
├── DTOs/
├── Events/
├── Listeners/
├── Jobs/
├── Mail/
├── Notifications/
├── Policies/
└── Providers/

database/
├── factories/
├── migrations/
└── seeders/

tests/
├── Feature/
└── Unit/
```

### Model Patterns

```php
<?php

namespace App\Models;

use App\Models\Concerns\HasUuid;
use App\Models\Concerns\Searchable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\SoftDeletes;

class User extends Model
{
    use HasFactory, SoftDeletes, HasUuid, Searchable;

    protected $fillable = [
        'name',
        'email',
        'role',
        'organization_id',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected $casts = [
        'email_verified_at' => 'datetime',
        'settings' => 'array',
        'is_active' => 'boolean',
    ];

    // Relationships
    public function organization(): BelongsTo
    {
        return $this->belongsTo(Organization::class);
    }

    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }

    // Scopes
    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }

    public function scopeRole($query, string $role)
    {
        return $query->where('role', $role);
    }

    public function scopeCreatedBetween($query, $from, $to)
    {
        return $query->whereBetween('created_at', [$from, $to]);
    }

    // Accessors & Mutators
    protected function fullName(): Attribute
    {
        return Attribute::make(
            get: fn () => "{$this->first_name} {$this->last_name}",
        );
    }

    protected function email(): Attribute
    {
        return Attribute::make(
            set: fn (string $value) => strtolower($value),
        );
    }

    // Business Logic
    public function isAdmin(): bool
    {
        return $this->role === 'admin';
    }

    public function canManage(User $user): bool
    {
        return $this->isAdmin() || $this->id === $user->manager_id;
    }
}

// app/Models/Concerns/Searchable.php
namespace App\Models\Concerns;

trait Searchable
{
    public function scopeSearch($query, ?string $term)
    {
        if (empty($term)) {
            return $query;
        }

        $columns = $this->searchable ?? ['name'];

        return $query->where(function ($q) use ($columns, $term) {
            foreach ($columns as $column) {
                $q->orWhere($column, 'ILIKE', "%{$term}%");
            }
        });
    }
}
```

### Service Layer

```php
<?php

namespace App\Services;

use App\DTOs\CreateUserDTO;
use App\DTOs\UpdateUserDTO;
use App\Events\UserCreated;
use App\Models\User;
use App\Repositories\UserRepository;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class UserService
{
    public function __construct(
        private UserRepository $repository,
        private NotificationService $notifications,
    ) {}

    public function create(CreateUserDTO $dto): User
    {
        return DB::transaction(function () use ($dto) {
            $user = $this->repository->create([
                'name' => $dto->name,
                'email' => $dto->email,
                'password' => Hash::make($dto->password),
                'organization_id' => $dto->organizationId,
                'role' => $dto->role ?? 'member',
            ]);

            event(new UserCreated($user));

            $this->notifications->sendWelcome($user);

            return $user;
        });
    }

    public function update(User $user, UpdateUserDTO $dto): User
    {
        return DB::transaction(function () use ($user, $dto) {
            $data = array_filter([
                'name' => $dto->name,
                'email' => $dto->email,
                'role' => $dto->role,
            ], fn ($value) => $value !== null);

            $this->repository->update($user, $data);

            return $user->fresh();
        });
    }

    public function delete(User $user): bool
    {
        return DB::transaction(function () use ($user) {
            // Soft delete related data
            $user->posts()->delete();

            return $this->repository->delete($user);
        });
    }
}
```

### Repository Pattern

```php
<?php

namespace App\Repositories;

use App\Models\User;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;

interface UserRepositoryInterface
{
    public function find(int $id): ?User;
    public function findByEmail(string $email): ?User;
    public function all(): Collection;
    public function paginate(array $filters = [], int $perPage = 15): LengthAwarePaginator;
    public function create(array $data): User;
    public function update(User $user, array $data): bool;
    public function delete(User $user): bool;
}

class UserRepository implements UserRepositoryInterface
{
    public function __construct(
        private User $model
    ) {}

    public function find(int $id): ?User
    {
        return $this->model->find($id);
    }

    public function findByEmail(string $email): ?User
    {
        return $this->model->where('email', $email)->first();
    }

    public function all(): Collection
    {
        return $this->model->all();
    }

    public function paginate(array $filters = [], int $perPage = 15): LengthAwarePaginator
    {
        $query = $this->model->query();

        if (!empty($filters['search'])) {
            $query->search($filters['search']);
        }

        if (!empty($filters['role'])) {
            $query->role($filters['role']);
        }

        if (!empty($filters['status'])) {
            $query->where('is_active', $filters['status'] === 'active');
        }

        $sortColumn = $filters['sort'] ?? 'created_at';
        $sortDirection = $filters['direction'] ?? 'desc';
        $query->orderBy($sortColumn, $sortDirection);

        return $query->paginate($perPage);
    }

    public function create(array $data): User
    {
        return $this->model->create($data);
    }

    public function update(User $user, array $data): bool
    {
        return $user->update($data);
    }

    public function delete(User $user): bool
    {
        return $user->delete();
    }
}
```

### Form Requests

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\Password;

class CreateUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', User::class);
    }

    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'min:2', 'max:100'],
            'email' => [
                'required',
                'email',
                Rule::unique('users')->where('organization_id', $this->user()->organization_id),
            ],
            'password' => ['required', Password::defaults()],
            'role' => ['sometimes', Rule::in(['admin', 'moderator', 'member'])],
        ];
    }

    public function messages(): array
    {
        return [
            'email.unique' => 'A user with this email already exists in your organization.',
        ];
    }

    public function toDTO(): CreateUserDTO
    {
        return new CreateUserDTO(
            name: $this->validated('name'),
            email: $this->validated('email'),
            password: $this->validated('password'),
            organizationId: $this->user()->organization_id,
            role: $this->validated('role'),
        );
    }
}

class UpdateUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('update', $this->route('user'));
    }

    public function rules(): array
    {
        return [
            'name' => ['sometimes', 'string', 'min:2', 'max:100'],
            'email' => [
                'sometimes',
                'email',
                Rule::unique('users')
                    ->where('organization_id', $this->user()->organization_id)
                    ->ignore($this->route('user')),
            ],
            'role' => ['sometimes', Rule::in(['admin', 'moderator', 'member'])],
        ];
    }

    public function toDTO(): UpdateUserDTO
    {
        return new UpdateUserDTO(
            name: $this->validated('name'),
            email: $this->validated('email'),
            role: $this->validated('role'),
        );
    }
}
```

### API Resources

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'role' => $this->role,
            'is_active' => $this->is_active,
            'created_at' => $this->created_at->toIso8601String(),
            'updated_at' => $this->updated_at->toIso8601String(),

            // Conditional relationships
            'organization' => new OrganizationResource($this->whenLoaded('organization')),
            'posts_count' => $this->when(
                $this->posts_count !== null,
                $this->posts_count
            ),

            // Conditional attributes
            'settings' => $this->when(
                $request->user()?->id === $this->id,
                $this->settings
            ),
        ];
    }
}

class UserCollection extends ResourceCollection
{
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total' => $this->total(),
                'per_page' => $this->perPage(),
                'current_page' => $this->currentPage(),
                'last_page' => $this->lastPage(),
            ],
        ];
    }
}
```

### Controller

```php
<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\CreateUserRequest;
use App\Http\Requests\UpdateUserRequest;
use App\Http\Resources\UserCollection;
use App\Http\Resources\UserResource;
use App\Models\User;
use App\Services\UserService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    public function __construct(
        private UserService $userService
    ) {
        $this->authorizeResource(User::class);
    }

    public function index(Request $request): UserCollection
    {
        $users = $this->userService->paginate(
            filters: $request->only(['search', 'role', 'status', 'sort', 'direction']),
            perPage: $request->integer('per_page', 15)
        );

        return new UserCollection($users);
    }

    public function show(User $user): UserResource
    {
        return new UserResource($user->load('organization'));
    }

    public function store(CreateUserRequest $request): JsonResponse
    {
        $user = $this->userService->create($request->toDTO());

        return (new UserResource($user))
            ->response()
            ->setStatusCode(201);
    }

    public function update(UpdateUserRequest $request, User $user): UserResource
    {
        $user = $this->userService->update($user, $request->toDTO());

        return new UserResource($user);
    }

    public function destroy(User $user): JsonResponse
    {
        $this->userService->delete($user);

        return response()->json(null, 204);
    }
}
```

### Testing

```php
<?php

namespace Tests\Feature\Api\V1;

use App\Models\Organization;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UserControllerTest extends TestCase
{
    use RefreshDatabase;

    private User $admin;
    private Organization $organization;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->admin = User::factory()
            ->for($this->organization)
            ->create(['role' => 'admin']);
    }

    public function test_can_list_users(): void
    {
        User::factory(5)->for($this->organization)->create();

        $response = $this->actingAs($this->admin)
            ->getJson('/api/v1/users');

        $response->assertOk()
            ->assertJsonCount(6, 'data')
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'name', 'email', 'role', 'created_at'],
                ],
                'meta' => ['total', 'per_page', 'current_page'],
            ]);
    }

    public function test_can_create_user(): void
    {
        $data = [
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'password' => 'SecurePass123!',
            'role' => 'member',
        ];

        $response = $this->actingAs($this->admin)
            ->postJson('/api/v1/users', $data);

        $response->assertCreated()
            ->assertJsonPath('data.email', 'john@example.com');

        $this->assertDatabaseHas('users', [
            'email' => 'john@example.com',
            'organization_id' => $this->organization->id,
        ]);
    }

    public function test_validates_unique_email(): void
    {
        User::factory()->for($this->organization)->create([
            'email' => 'existing@example.com',
        ]);

        $response = $this->actingAs($this->admin)
            ->postJson('/api/v1/users', [
                'name' => 'Test',
                'email' => 'existing@example.com',
                'password' => 'SecurePass123!',
            ]);

        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['email']);
    }
}
```

## Anti-patterns

### Avoid: Fat Controllers

```php
// BAD - too much logic in controller
public function store(Request $request)
{
    $validated = $request->validate([...]);
    $user = User::create($validated);
    $user->password = Hash::make($validated['password']);
    $user->save();
    Mail::to($user)->send(new WelcomeMail($user));
    event(new UserCreated($user));
    return new UserResource($user);
}

// GOOD - delegate to service
public function store(CreateUserRequest $request)
{
    $user = $this->userService->create($request->toDTO());
    return new UserResource($user);
}
```

### Avoid: N+1 Queries

```php
// BAD - N+1 query
$users = User::all();
foreach ($users as $user) {
    echo $user->organization->name; // Query per user
}

// GOOD - eager loading
$users = User::with('organization')->get();
```

## References

- [Laravel Documentation](https://laravel.com/docs)
- [Laravel Best Practices](https://github.com/alexeymezenin/laravel-best-practices)
- [Laravel News](https://laravel-news.com/)
- [Laracasts](https://laracasts.com/)
