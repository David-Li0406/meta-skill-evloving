# Testing API Resources

Feature test examples for API resources.

## Basic Resource Tests

```php
use App\Http\Resources\UserResource;
use App\Models\Post;
use App\Models\User;

it('transforms user resource correctly', function () {
    $user = User::factory()->create([
        'name' => 'John Doe',
        'email' => 'john@example.com',
    ]);

    $resource = UserResource::make($user);
    $array = $resource->toArray(request());

    expect($array)
        ->toHaveKey('id', $user->id)
        ->toHaveKey('name', 'John Doe')
        ->toHaveKey('email', 'john@example.com')
        ->toHaveKey('created_at')
        ->and($array['created_at'])->toContain('T'); // ISO 8601 format
});

it('includes relationships when loaded', function () {
    $user = User::factory()
        ->has(Post::factory()->count(3))
        ->create();

    $user->load('posts');

    $resource = UserResource::make($user);
    $array = $resource->toArray(request());

    expect($array)
        ->toHaveKey('posts')
        ->and($array['posts'])->toHaveCount(3);
});

it('excludes relationships when not loaded', function () {
    $user = User::factory()->create();

    $resource = UserResource::make($user);
    $array = $resource->toArray(request());

    expect($array)->not->toHaveKey('posts');
});

it('includes counts when loaded', function () {
    $user = User::factory()
        ->has(Post::factory()->count(5))
        ->create();

    $user->loadCount('posts');

    $resource = UserResource::make($user);
    $array = $resource->toArray(request());

    expect($array)
        ->toHaveKey('posts_count', 5)
        ->not->toHaveKey('posts'); // Count loaded, but not full relationship
});

it('transforms collections correctly', function () {
    $users = User::factory()->count(3)->create();

    $collection = UserResource::collection($users);
    $array = $collection->toArray(request());

    expect($array)->toHaveCount(3);
});

it('includes conditional attributes based on permissions', function () {
    $admin = User::factory()->admin()->create();
    $user = User::factory()->create(['internal_notes' => 'Secret note']);

    // As admin - should see internal notes
    actingAs($admin);
    $resource = UserResource::make($user);
    $array = $resource->toArray(request());

    expect($array)->toHaveKey('internal_notes', 'Secret note');

    // As regular user - should not see internal notes
    actingAs($user);
    $resource = UserResource::make($user);
    $array = $resource->toArray(request());

    expect($array)->not->toHaveKey('internal_notes');
});
```

## Date Formatting Tests

```php
it('formats dates in ISO 8601 format', function () {
    $user = User::factory()->create([
        'created_at' => '2024-01-15 10:30:00',
        'updated_at' => '2024-01-16 14:45:00',
    ]);

    $resource = UserResource::make($user);
    $array = $resource->toArray(request());

    expect($array['created_at'])
        ->toContain('2024-01-15')
        ->toContain('T') // ISO 8601 separator
        ->toContain('10:30:00');
});

it('handles null dates gracefully', function () {
    $user = User::factory()->create([
        'email_verified_at' => null,
    ]);

    $resource = UserResource::make($user);
    $array = $resource->toArray(request());

    expect($array['email_verified_at'])->toBeNull();
});
```

## Nested Resource Tests

```php
it('transforms nested resources correctly', function () {
    $user = User::factory()
        ->has(Post::factory()->count(2)->hasComments(3))
        ->create();

    $user->load('posts.comments');

    $resource = UserResource::make($user);
    $array = $resource->toArray(request());

    expect($array['posts'])
        ->toHaveCount(2)
        ->each->toHaveKey('comments')
        ->each(fn ($post) => $post->toHaveCount('comments', 3));
});
```

## Pagination Tests

```php
it('preserves pagination structure', function () {
    User::factory()->count(25)->create();

    $users = User::paginate(10);
    $resource = UserResource::collection($users);

    $response = $resource->response()->getData(true);

    expect($response)
        ->toHaveKey('data')
        ->toHaveKey('links')
        ->toHaveKey('meta')
        ->and($response['data'])->toHaveCount(10)
        ->and($response['meta']['total'])->toBe(25)
        ->and($response['meta']['per_page'])->toBe(10);
});
```

## Controller Integration Tests

```php
it('returns user resource from show endpoint', function () {
    $user = User::factory()->create(['name' => 'Jane Doe']);

    $this->actingAs($user)
        ->get(route('users.show', $user))
        ->assertOk()
        ->assertInertia(fn ($page) => $page
            ->component('users/show')
            ->has('user', fn ($user) => $user
                ->where('id', $user->id)
                ->where('name', 'Jane Doe')
                ->etc()
            )
        );
});

it('returns paginated user collection from index endpoint', function () {
    User::factory()->count(20)->create();
    $admin = User::factory()->admin()->create();

    $this->actingAs($admin)
        ->get(route('users.index'))
        ->assertOk()
        ->assertInertia(fn ($page) => $page
            ->component('users/index')
            ->has('users.data', 15) // Default pagination
            ->has('users.meta')
            ->has('users.links')
        );
});
```
