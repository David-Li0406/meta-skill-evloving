# Testing Implementation Guide

Step-by-step instructions for testing a new feature.

## 1. Create Test File

```bash
php artisan make:test FeatureItemTest --no-interaction
```

## 2. Feature Test Template

```php
<?php

use App\Models\User;
use App\Models\FeatureItem;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

beforeEach(function () {
    $this->user = User::factory()->create();
});

describe('Feature Items CRUD', function () {
    test('user can view their items', function () {
        FeatureItem::factory()->count(3)->create(['user_id' => $this->user->id]);

        $response = $this->actingAs($this->user)
            ->get('/feature-items');

        $response->assertOk();
        $response->assertInertia(fn ($page) => $page
            ->component('feature-items/index')
            ->has('items.data', 3)
        );
    });

    test('user can view create form', function () {
        $response = $this->actingAs($this->user)
            ->get('/feature-items/create');

        $response->assertOk();
        $response->assertInertia(fn ($page) => $page
            ->component('feature-items/create')
        );
    });

    test('user can create item', function () {
        $response = $this->actingAs($this->user)
            ->post('/feature-items', [
                'title' => 'Test Item',
                'description' => 'Test description',
                'status' => 'draft',
            ]);

        $response->assertRedirect();
        $this->assertDatabaseHas('feature_items', [
            'user_id' => $this->user->id,
            'title' => 'Test Item',
        ]);
    });

    test('user can view their item', function () {
        $item = FeatureItem::factory()->create(['user_id' => $this->user->id]);

        $response = $this->actingAs($this->user)
            ->get("/feature-items/{$item->id}");

        $response->assertOk();
        $response->assertInertia(fn ($page) => $page
            ->component('feature-items/show')
            ->has('item')
        );
    });

    test('user can update their item', function () {
        $item = FeatureItem::factory()->create(['user_id' => $this->user->id]);

        $response = $this->actingAs($this->user)
            ->put("/feature-items/{$item->id}", [
                'title' => 'Updated Title',
                'description' => 'Updated description',
                'status' => 'active',
            ]);

        $response->assertRedirect();
        expect($item->fresh()->title)->toBe('Updated Title');
    });

    test('user can delete their item', function () {
        $item = FeatureItem::factory()->create(['user_id' => $this->user->id]);

        $response = $this->actingAs($this->user)
            ->delete("/feature-items/{$item->id}");

        $response->assertRedirect();
        $this->assertDatabaseMissing('feature_items', ['id' => $item->id]);
    });
});

describe('Feature Items Authorization', function () {
    test('user cannot view other user\'s item', function () {
        $otherUser = User::factory()->create();
        $item = FeatureItem::factory()->create(['user_id' => $otherUser->id]);

        $response = $this->actingAs($this->user)
            ->get("/feature-items/{$item->id}");

        $response->assertForbidden();
    });

    test('user cannot update other user\'s item', function () {
        $otherUser = User::factory()->create();
        $item = FeatureItem::factory()->create(['user_id' => $otherUser->id]);

        $response = $this->actingAs($this->user)
            ->put("/feature-items/{$item->id}", [
                'title' => 'Hacked Title',
                'status' => 'active',
            ]);

        $response->assertForbidden();
    });

    test('user cannot delete other user\'s item', function () {
        $otherUser = User::factory()->create();
        $item = FeatureItem::factory()->create(['user_id' => $otherUser->id]);

        $response = $this->actingAs($this->user)
            ->delete("/feature-items/{$item->id}");

        $response->assertForbidden();
    });

    test('guest is redirected to login', function () {
        $response = $this->get('/feature-items');

        $response->assertRedirect('/login');
    });
});

describe('Feature Items Validation', function () {
    test('validates required fields', function () {
        $response = $this->actingAs($this->user)
            ->post('/feature-items', [
                'title' => '',
                'status' => '',
            ]);

        $response->assertSessionHasErrors(['title', 'status']);
    });

    test('validates title max length', function () {
        $response = $this->actingAs($this->user)
            ->post('/feature-items', [
                'title' => str_repeat('a', 256),
                'status' => 'draft',
            ]);

        $response->assertSessionHasErrors('title');
    });

    test('validates status values', function () {
        $response = $this->actingAs($this->user)
            ->post('/feature-items', [
                'title' => 'Test',
                'status' => 'invalid-status',
            ]);

        $response->assertSessionHasErrors('status');
    });
});
```

## 3. Test Coverage Checklist

### CRUD Operations

```
[ ] Index - list items with pagination
[ ] Index - only shows user's items (not others')
[ ] Create - form renders
[ ] Create - validation errors for invalid data
[ ] Create - success creates record
[ ] Show - displays correct item
[ ] Show - 404 for non-existent
[ ] Edit - form renders with existing data
[ ] Update - validation errors
[ ] Update - success updates record
[ ] Delete - removes record
```

### Authorization

```
[ ] Guest redirected to login
[ ] User can access own resources
[ ] User cannot access other users' resources
[ ] User cannot modify other users' resources
```

### Validation

```
[ ] Required fields validated
[ ] Max length enforced
[ ] Enum/choice values enforced
[ ] Custom validation rules (if any)
```

## 4. Running Tests

```bash
# Run all tests
php artisan test

# Run specific file
php artisan test tests/Feature/FeatureItemTest.php

# Run with filter
php artisan test --filter="can create item"

# Run describe block
php artisan test --filter="Feature Items CRUD"

# With coverage
php artisan test --coverage

# Stop on first failure
php artisan test --stop-on-failure
```

## 5. Factory Best Practices

### Use States for Different Scenarios

```php
// In tests
FeatureItem::factory()->active()->create();
FeatureItem::factory()->archived()->create();
FeatureItem::factory()->count(5)->create();
```

### Use Relationships

```php
// Create with specific user
FeatureItem::factory()->create(['user_id' => $this->user->id]);

// Or use for() method
FeatureItem::factory()->for($this->user)->create();
```

## 6. Debugging Tests

```php
// Dump response
$response->dump();
$response->dumpHeaders();
$response->dumpSession();

// Debug database state
dd(FeatureItem::all()->toArray());

// Disable exception handling to see full errors
$this->withoutExceptionHandling();

// Check validation errors
dd($response->exception->validator->errors()->toArray());
```
