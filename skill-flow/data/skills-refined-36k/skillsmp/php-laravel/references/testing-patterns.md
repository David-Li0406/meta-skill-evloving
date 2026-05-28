# Testing Patterns with Pest

## Structure

Use Pest's describe/it syntax for organized tests:

```php
describe('UserService', function () {
    beforeEach(function () {
        $this->service = app(UserService::class);
    });

    it('creates user with valid data', function () {
        $data = [
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'password' => 'password123',
        ];

        $user = $this->service->create($data);

        expect($user)
            ->toBeInstanceOf(User::class)
            ->email->toBe('john@example.com');
    });

    it('throws exception for duplicate email', function () {
        User::factory()->create(['email' => 'john@example.com']);

        $this->service->create([
            'name' => 'Jane Doe',
            'email' => 'john@example.com',
            'password' => 'password123',
        ]);
    })->throws(DuplicateEmailException::class);

    it('sends welcome email after creation', function () {
        Mail::fake();

        $user = $this->service->create([
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'password' => 'password123',
        ]);

        Mail::assertSent(WelcomeEmail::class, function ($mail) use ($user) {
            return $mail->hasTo($user->email);
        });
    });
});
```

## Database Testing

### Traits

Use `RefreshDatabase` trait to reset database between tests:

```php
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);
```

### Factories

Use factories with states for test data:

```php
// Database/Factories/UserFactory.php
public function definition(): array
{
    return [
        'name' => fake()->name(),
        'email' => fake()->unique()->safeEmail(),
        'password' => Hash::make('password'),
        'active' => true,
    ];
}

public function inactive(): static
{
    return $this->state(fn (array $attributes) => [
        'active' => false,
    ]);
}

public function admin(): static
{
    return $this->state(fn (array $attributes) => [
        'role' => 'admin',
    ]);
}
```

Usage:

```php
// Create single user
$user = User::factory()->create();

// Create multiple users
$users = User::factory()->count(10)->create();

// Create with state
$admin = User::factory()->admin()->create();
$inactive = User::factory()->inactive()->create();

// Override attributes
$user = User::factory()->create([
    'email' => 'specific@example.com',
]);
```

### Assertions

```php
// Assert record exists
$this->assertDatabaseHas('users', [
    'email' => 'john@example.com',
]);

// Assert record doesn't exist
$this->assertDatabaseMissing('users', [
    'email' => 'deleted@example.com',
]);

// Assert record count
$this->assertDatabaseCount('users', 5);

// Assert soft deleted
$this->assertSoftDeleted('users', [
    'id' => $user->id,
]);
```

## HTTP Testing

### Basic Requests

```php
it('lists all users', function () {
    User::factory()->count(3)->create();

    $response = $this->getJson('/api/users');

    $response
        ->assertStatus(200)
        ->assertJsonCount(3, 'data');
});

it('creates a new user', function () {
    $data = [
        'name' => 'John Doe',
        'email' => 'john@example.com',
        'password' => 'password123',
    ];

    $response = $this->postJson('/api/users', $data);

    $response
        ->assertStatus(201)
        ->assertJsonStructure([
            'id',
            'name',
            'email',
            'created_at',
        ]);

    $this->assertDatabaseHas('users', [
        'email' => 'john@example.com',
    ]);
});
```

### Authentication

```php
it('requires authentication', function () {
    $response = $this->getJson('/api/users');

    $response->assertStatus(401);
});

it('allows authenticated users', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->getJson('/api/users');

    $response->assertStatus(200);
});
```

### Authorization

```php
it('prevents unauthorized updates', function () {
    $user = User::factory()->create();
    $otherUser = User::factory()->create();

    $response = $this->actingAs($user)
        ->putJson("/api/users/{$otherUser->id}", [
            'name' => 'New Name',
        ]);

    $response->assertStatus(403);
});
```

## Mocking

### Facades

```php
it('sends notification', function () {
    Notification::fake();

    $user = User::factory()->create();
    $user->notify(new WelcomeNotification);

    Notification::assertSentTo($user, WelcomeNotification::class);
});

it('uploads file to storage', function () {
    Storage::fake('public');

    $file = UploadedFile::fake()->image('avatar.jpg');

    $this->post('/api/upload', ['file' => $file]);

    Storage::disk('public')->assertExists('avatars/avatar.jpg');
});
```

### Queue Jobs

```php
it('dispatches job', function () {
    Queue::fake();

    $user = User::factory()->create();
    ProcessUserData::dispatch($user);

    Queue::assertPushed(ProcessUserData::class, function ($job) use ($user) {
        return $job->user->id === $user->id;
    });
});
```

## Test Organization

### Datasets

Use datasets to run tests with multiple inputs:

```php
it('validates email format', function ($email, $valid) {
    $response = $this->postJson('/api/users', [
        'name' => 'John Doe',
        'email' => $email,
        'password' => 'password123',
    ]);

    if ($valid) {
        $response->assertStatus(201);
    } else {
        $response->assertStatus(422);
    }
})->with([
    ['john@example.com', true],
    ['invalid-email', false],
    ['missing@', false],
    ['@example.com', false],
]);
```

### Shared Setup

```php
beforeEach(function () {
    $this->user = User::factory()->create();
    $this->actingAs($this->user);
});

it('accesses protected route', function () {
    $response = $this->getJson('/api/profile');
    $response->assertStatus(200);
});
```
