# Test Patterns Reference

Common test patterns and assertions for RentPath.

## Describe Block Pattern

```php
describe('Application Submission', function () {
    beforeEach(function () {
        $this->tenant = User::factory()->withTenantProfile()->create();
        $this->property = Property::factory()->vacant()->public()->create();
    });

    test('tenant can submit application', function () {
        $application = Application::factory()
            ->for($this->property)
            ->for($this->tenant->tenantProfile)
            ->draft()
            ->create();

        $response = $this->actingAs($this->tenant)
            ->post("/applications/{$application->id}/submit");

        $response->assertRedirect();
        expect($application->fresh()->status)->toBe('submitted');
    });

    test('cannot submit already submitted application', function () {
        $application = Application::factory()
            ->for($this->property)
            ->for($this->tenant->tenantProfile)
            ->submitted()
            ->create();

        $response = $this->actingAs($this->tenant)
            ->post("/applications/{$application->id}/submit");

        $response->assertForbidden();
    });
});
```

## Authentication Testing

```php
test('guest is redirected to login', function () {
    $response = $this->get('/dashboard');
    $response->assertRedirect('/login');
});

test('authenticated user can access dashboard', function () {
    $response = $this->actingAs($this->user)
        ->get('/dashboard');
    $response->assertOk();
});
```

## Authorization Testing

```php
test('user cannot view other user\'s application', function () {
    $otherUser = User::factory()->withTenantProfile()->create();
    $application = Application::factory()
        ->for($otherUser->tenantProfile)
        ->create();

    $response = $this->actingAs($this->user)
        ->get("/applications/{$application->id}");

    $response->assertForbidden();
});

test('owner can view their application', function () {
    $application = Application::factory()
        ->for($this->user->tenantProfile)
        ->create();

    $response = $this->actingAs($this->user)
        ->get("/applications/{$application->id}");

    $response->assertOk();
});
```

## Validation Testing

```php
test('validates required fields', function () {
    $response = $this->actingAs($this->user)
        ->post('/properties', [
            'title' => '',  // Required field empty
        ]);

    $response->assertSessionHasErrors('title');
});

test('validates field format', function () {
    $response = $this->actingAs($this->user)
        ->post('/properties', [
            'rent_amount' => 'not-a-number',
        ]);

    $response->assertSessionHasErrors('rent_amount');
});
```

## Subdomain Testing

```php
test('manager can access manager portal', function () {
    $user = User::factory()->withPropertyManager(verified: true)->create();
    $managerUrl = 'http://manager.' . config('app.domain');

    $response = $this->actingAs($user)
        ->get("{$managerUrl}/properties");

    $response->assertOk();
});

test('tenant cannot access manager portal', function () {
    $user = User::factory()->withTenantProfile()->create();
    $managerUrl = 'http://manager.' . config('app.domain');

    $response = $this->actingAs($user)
        ->get("{$managerUrl}/properties");

    $response->assertForbidden();
});
```

## Inertia Response Testing

```php
use Inertia\Testing\AssertableInertia as Assert;

test('returns correct page component', function () {
    $response = $this->actingAs($this->user)
        ->get('/properties');

    $response->assertInertia(fn (Assert $page) => $page
        ->component('properties/index')
    );
});

test('passes expected props', function () {
    Property::factory()->count(3)->create();

    $response = $this->actingAs($this->user)
        ->get('/properties');

    $response->assertInertia(fn (Assert $page) => $page
        ->has('properties', 3)
        ->has('properties.0', fn (Assert $prop) => $prop
            ->has('id')
            ->has('title')
            ->has('status')
            ->etc()
        )
    );
});
```

## File Upload Testing

```php
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('user can upload document', function () {
    Storage::fake('s3-private');

    $file = UploadedFile::fake()->create('document.pdf', 1024);

    $response = $this->actingAs($this->user)
        ->post('/profile/documents', [
            'id_document' => $file,
        ]);

    $response->assertOk();
    Storage::disk('s3-private')->assertExists('documents/' . $file->hashName());
});
```

## Database State Testing

```php
test('creates application in database', function () {
    $response = $this->actingAs($this->tenant)
        ->post("/properties/{$this->property->id}/apply", [
            'message' => 'I am interested',
        ]);

    $this->assertDatabaseHas('applications', [
        'property_id' => $this->property->id,
        'tenant_profile_id' => $this->tenant->tenantProfile->id,
        'status' => 'draft',
    ]);
});

test('deletes application from database', function () {
    $application = Application::factory()
        ->for($this->tenant->tenantProfile)
        ->draft()
        ->create();

    $response = $this->actingAs($this->tenant)
        ->delete("/applications/{$application->id}");

    $this->assertDatabaseMissing('applications', [
        'id' => $application->id,
    ]);
});
```

## HTTP Assertions

```php
$response->assertOk();                    // 200
$response->assertCreated();               // 201
$response->assertRedirect('/path');       // 302
$response->assertForbidden();             // 403
$response->assertNotFound();              // 404
$response->assertSessionHasErrors('field');
```

## Database Assertions

```php
$this->assertDatabaseHas('applications', [
    'property_id' => $property->id,
    'status' => 'submitted',
]);

$this->assertDatabaseMissing('applications', [
    'id' => $application->id,
]);

$this->assertDatabaseCount('applications', 1);
```

## Pest Expectations

```php
expect($value)->toBe($expected);
expect($value)->toEqual($expected);
expect($value)->toBeTrue();
expect($value)->toBeFalse();
expect($value)->toBeNull();
expect($value)->not->toBe($expected);
expect($array)->toHaveCount(5);
expect($string)->toContain('substring');
```
