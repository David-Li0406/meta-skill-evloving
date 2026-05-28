---
name: jikime-lang-php
description: PHP 8.3+ development specialist covering Laravel 11, Symfony 7, Eloquent ORM, and modern PHP patterns. Use when developing PHP APIs, web applications, or Laravel/Symfony projects.
version: 1.0.0
tags: ["language", "php", "laravel", "symfony", "eloquent", "web"]
triggers:
  keywords: ["php", "laravel", "symfony", "eloquent", "composer", "피에이치피"]
  phases: ["run"]
  agents: ["backend"]
  languages: ["php"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
user-invocable: false
---

# PHP Development Guide

PHP 8.3+ / Laravel 11 개발을 위한 간결한 가이드.

## Quick Reference

| 용도 | 도구 | 특징 |
|------|------|------|
| Framework | **Laravel 11** | 풀스택, Eloquent |
| Framework | **Symfony 7** | 컴포넌트 기반 |
| Testing | **PHPUnit** | 표준 테스팅 |
| Testing | **Pest** | 모던 문법 |

## Project Setup

```bash
# Laravel
composer create-project laravel/laravel project
cd project && php artisan serve

# Symfony
composer create-project symfony/skeleton project
cd project && symfony server:start
```

## Laravel Patterns

### Controller

```php
class UserController extends Controller
{
    public function __construct(
        private UserService $userService
    ) {}

    public function index(): JsonResponse
    {
        return response()->json(
            $this->userService->all()
        );
    }

    public function show(int $id): JsonResponse
    {
        $user = $this->userService->find($id);

        return $user
            ? response()->json($user)
            : response()->json(['error' => 'Not found'], 404);
    }

    public function store(StoreUserRequest $request): JsonResponse
    {
        $user = $this->userService->create($request->validated());

        return response()->json($user, 201);
    }
}
```

### Form Request

```php
class StoreUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'min:2', 'max:100'],
            'email' => ['required', 'email', 'unique:users'],
            'password' => ['required', 'min:8', 'confirmed'],
        ];
    }
}
```

### Eloquent Model

```php
class User extends Model
{
    use HasFactory;

    protected $fillable = ['name', 'email', 'password'];

    protected $hidden = ['password'];

    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            'password' => 'hashed',
        ];
    }

    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

### Service Layer

```php
class UserService
{
    public function __construct(
        private User $user
    ) {}

    public function all(): Collection
    {
        return $this->user->with('posts')->get();
    }

    public function find(int $id): ?User
    {
        return $this->user->find($id);
    }

    public function create(array $data): User
    {
        return DB::transaction(function () use ($data) {
            return $this->user->create($data);
        });
    }
}
```

## PHP 8.3 Features

### Constructor Property Promotion

```php
class User
{
    public function __construct(
        public readonly string $name,
        public readonly string $email,
        private ?int $id = null,
    ) {}
}
```

### Named Arguments

```php
$user = new User(
    name: 'John',
    email: 'john@example.com',
);
```

### Match Expression

```php
$result = match ($status) {
    'pending' => 'Processing',
    'approved' => 'Approved',
    'rejected' => 'Rejected',
    default => 'Unknown',
};
```

### Enums

```php
enum Status: string
{
    case Pending = 'pending';
    case Approved = 'approved';
    case Rejected = 'rejected';

    public function label(): string
    {
        return match ($this) {
            self::Pending => 'Processing',
            self::Approved => 'Approved',
            self::Rejected => 'Rejected',
        };
    }
}
```

## Testing with Pest

```php
uses(RefreshDatabase::class);

it('creates a user', function () {
    $response = $this->postJson('/api/users', [
        'name' => 'John',
        'email' => 'john@example.com',
        'password' => 'password123',
        'password_confirmation' => 'password123',
    ]);

    $response->assertStatus(201)
        ->assertJsonPath('name', 'John');

    $this->assertDatabaseHas('users', ['email' => 'john@example.com']);
});

it('validates required fields', function () {
    $response = $this->postJson('/api/users', []);

    $response->assertStatus(422)
        ->assertJsonValidationErrors(['name', 'email', 'password']);
});
```

## Project Structure

```
app/
├── Http/
│   ├── Controllers/
│   └── Requests/
├── Models/
├── Services/
└── Repositories/
routes/
├── api.php
└── web.php
tests/
├── Feature/
└── Unit/
```

## Best Practices

- **Type Hints**: 모든 메서드에 타입 힌트
- **Readonly**: 불변 프로퍼티에 readonly 사용
- **Service Layer**: 비즈니스 로직 분리
- **Form Request**: 유효성 검사 분리
- **Pest**: 가독성 좋은 테스트 작성

---

Last Updated: 2026-01-21
Version: 2.0.0
