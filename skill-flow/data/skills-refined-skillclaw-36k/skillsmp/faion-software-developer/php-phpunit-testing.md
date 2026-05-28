---
id: php-phpunit-testing
name: "PHPUnit Testing"
domain: PHP
skill: faion-software-developer
category: "backend"
---

## PHPUnit Testing

### Problem
Test Laravel applications effectively.

### Framework: Feature Tests

```php
<?php
// tests/Feature/UserControllerTest.php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UserControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_can_list_users(): void
    {
        $users = User::factory()->count(5)->create();

        $response = $this->getJson('/api/v1/users');

        $response->assertOk()
            ->assertJsonCount(5, 'data')
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'name', 'email', 'created_at']
                ],
                'meta' => ['current_page', 'total']
            ]);
    }

    public function test_can_create_user(): void
    {
        $userData = [
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'password' => 'password123',
        ];

        $response = $this->postJson('/api/v1/users', $userData);

        $response->assertCreated()
            ->assertJsonPath('data.name', 'John Doe')
            ->assertJsonPath('data.email', 'john@example.com');

        $this->assertDatabaseHas('users', [
            'email' => 'john@example.com'
        ]);
    }

    public function test_create_user_validates_email(): void
    {
        $userData = [
            'name' => 'John Doe',
            'email' => 'invalid-email',
            'password' => 'password123',
        ];

        $response = $this->postJson('/api/v1/users', $userData);

        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['email']);
    }

    public function test_can_update_user(): void
    {
        $user = User::factory()->create();

        $response = $this->putJson("/api/v1/users/{$user->id}", [
            'name' => 'Updated Name',
        ]);

        $response->assertOk()
            ->assertJsonPath('data.name', 'Updated Name');
    }

    public function test_can_delete_user(): void
    {
        $user = User::factory()->create();

        $response = $this->deleteJson("/api/v1/users/{$user->id}");

        $response->assertNoContent();
        $this->assertSoftDeleted('users', ['id' => $user->id]);
    }
}
```

### Unit Tests

```php
<?php
// tests/Unit/Services/UserServiceTest.php

namespace Tests\Unit\Services;

use App\Models\User;
use App\Repositories\UserRepository;
use App\Services\UserService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Mockery;
use Tests\TestCase;

class UserServiceTest extends TestCase
{
    use RefreshDatabase;

    private UserService $service;
    private UserRepository $repository;

    protected function setUp(): void
    {
        parent::setUp();
        $this->repository = new UserRepository(new User());
        $this->service = new UserService($this->repository);
    }

    public function test_create_hashes_password(): void
    {
        $user = $this->service->create([
            'name' => 'John',
            'email' => 'john@example.com',
            'password' => 'plaintext',
        ]);

        $this->assertNotEquals('plaintext', $user->password);
        $this->assertTrue(\Hash::check('plaintext', $user->password));
    }

    public function test_create_fires_event(): void
    {
        \Event::fake();

        $this->service->create([
            'name' => 'John',
            'email' => 'john@example.com',
            'password' => 'password',
        ]);

        \Event::assertDispatched(\App\Events\UserCreated::class);
    }
}
```

### Agent

faion-backend-agent
