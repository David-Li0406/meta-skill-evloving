# Architecture Patterns

## Service Layer Pattern

### Structure

Place business logic in Service classes, not controllers. Keep controllers thin with a maximum of 10 lines per method.

```php
// app/Services/UserService.php
class UserService
{
    public function __construct(
        private readonly UserRepository $users,
        private readonly NotificationService $notifications
    ) {}

    public function createUser(array $data): User
    {
        $user = $this->users->create($data);
        $this->notifications->sendWelcomeEmail($user);
        return $user;
    }

    public function updateProfile(User $user, array $data): User
    {
        return $this->users->update($user, $data);
    }
}
```

### Dependency Injection

Use constructor injection with readonly properties (PHP 8.x):

```php
class OrderService
{
    public function __construct(
        private readonly OrderRepository $orders,
        private readonly PaymentGateway $payments,
        private readonly InventoryService $inventory,
        private readonly NotificationService $notifications
    ) {}
}
```

### Service Registration

Register services in `app/Providers/AppServiceProvider.php`:

```php
public function register(): void
{
    $this->app->singleton(UserService::class);
    $this->app->singleton(OrderService::class);
}
```

## Repository Pattern

Use repositories for complex queries or when ORM abstraction is beneficial.

### When to Use Repositories

- Complex query logic that is reused across multiple services
- Potential need to switch ORMs in the future
- Query logic that requires significant testing
- Domain-driven design architectures

### When NOT to Use Repositories

- Simple CRUD operations (use models directly)
- Single-use queries (keep in service classes)
- Over-abstraction without clear benefit

### Repository Structure

```php
// app/Repositories/UserRepository.php
class UserRepository
{
    public function findByEmail(string $email): ?User
    {
        return User::where('email', $email)->first();
    }

    public function getActiveUsers(): Collection
    {
        return User::select(['id', 'name', 'email'])
            ->where('active', true)
            ->with('profile')
            ->get();
    }

    public function create(array $data): User
    {
        return User::create($data);
    }
}
```

### Key Principles

- Keep Eloquent code in repositories, never in controllers
- Return Collections or Models, never plain arrays
- Use type hints for all parameters and return values
- Maintain consistent method naming: `findBy*`, `getActive*`, `create*`
