# API Testing Examples

Comprehensive test examples for API endpoints.

## Basic CRUD Tests

### List Resources

```php
test('lists posts with pagination', function () {
    Post::factory()->count(25)->create();

    $response = $this->getJson('/api/posts');

    $response->assertSuccessful()
        ->assertJsonStructure([
            'data' => [
                '*' => ['id', 'title', 'slug', 'created_at'],
            ],
            'links',
            'meta',
        ])
        ->assertJsonCount(20, 'data');
});
```

### Create Resource

```php
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
```

### Update Resource

```php
test('updates post with valid data', function () {
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);
    $token = $user->createToken('test')->plainTextToken;

    $response = $this->withToken($token)
        ->putJson("/api/posts/{$post->id}", [
            'title' => 'Updated Title',
        ]);

    $response->assertSuccessful()
        ->assertJsonFragment(['title' => 'Updated Title']);
});
```

### Delete Resource

```php
test('deletes post', function () {
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);
    $token = $user->createToken('test')->plainTextToken;

    $response = $this->withToken($token)
        ->deleteJson("/api/posts/{$post->id}");

    $response->assertNoContent();
    expect(Post::find($post->id))->toBeNull();
});
```

## Validation Tests

```php
test('validates required fields', function () {
    $user = User::factory()->create();
    $token = $user->createToken('test')->plainTextToken;

    $response = $this->withToken($token)
        ->postJson('/api/posts', []);

    $response->assertUnprocessable()
        ->assertJsonValidationErrors(['title', 'slug', 'content']);
});

test('validates unique fields', function () {
    $user = User::factory()->create();
    $existingPost = Post::factory()->create(['slug' => 'existing-slug']);
    $token = $user->createToken('test')->plainTextToken;

    $response = $this->withToken($token)
        ->postJson('/api/posts', [
            'title' => 'New Post',
            'slug' => 'existing-slug',
            'content' => 'Content',
        ]);

    $response->assertUnprocessable()
        ->assertJsonValidationErrors(['slug']);
});
```

## Authorization Tests

```php
test('prevents unauthorized access', function () {
    $response = $this->postJson('/api/posts', [
        'title' => 'Test',
    ]);

    $response->assertUnauthorized();
});

test('prevents updating others posts', function () {
    $user = User::factory()->create();
    $otherUser = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $otherUser->id]);
    $token = $user->createToken('test')->plainTextToken;

    $response = $this->withToken($token)
        ->putJson("/api/posts/{$post->id}", ['title' => 'Hacked']);

    $response->assertForbidden();
});
```

## Filtering & Search Tests

```php
test('filters posts by status', function () {
    Post::factory()->create(['published' => true]);
    Post::factory()->create(['published' => false]);

    $response = $this->getJson('/api/posts?published=1');

    $response->assertSuccessful()
        ->assertJsonCount(1, 'data');
});

test('searches posts by title', function () {
    Post::factory()->create(['title' => 'Laravel Tutorial']);
    Post::factory()->create(['title' => 'Vue Tutorial']);

    $response = $this->getJson('/api/posts?search=Laravel');

    $response->assertSuccessful()
        ->assertJsonCount(1, 'data')
        ->assertJsonFragment(['title' => 'Laravel Tutorial']);
});
```

## Pagination Tests

```php
test('paginates results', function () {
    Post::factory()->count(50)->create();

    $response = $this->getJson('/api/posts?per_page=15');

    $response->assertSuccessful()
        ->assertJsonCount(15, 'data')
        ->assertJsonStructure(['links', 'meta']);
});
```

## Rate Limiting Tests

```php
test('rate limits requests', function () {
    $user = User::factory()->create();
    $token = $user->createToken('test')->plainTextToken;

    // Make requests up to rate limit
    for ($i = 0; $i < 61; $i++) {
        $response = $this->withToken($token)->getJson('/api/posts');
    }

    $response->assertStatus(429); // Too Many Requests
});
```
