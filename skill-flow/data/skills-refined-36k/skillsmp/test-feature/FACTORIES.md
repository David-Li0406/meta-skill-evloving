# Factory Reference

Complete reference for RentPath model factories and their states.

## UserFactory

```php
User::factory()->create();                           // Verified user
User::factory()->unverified()->create();             // Unverified
User::factory()->withTenantProfile()->create();      // With tenant profile
User::factory()->withPropertyManager()->create();    // With PM profile
User::factory()
    ->withTenantProfile(verified: true)
    ->create();                                      // Verified tenant
```

## TenantProfileFactory

```php
TenantProfile::factory()->create();                  // Basic profile
TenantProfile::factory()->verified()->create();      // Verified
TenantProfile::factory()->rejected('reason')->create();
TenantProfile::factory()->employed()->create();
TenantProfile::factory()->student()->create();
TenantProfile::factory()->withGuarantor()->create();
```

## PropertyFactory

```php
Property::factory()->create();                       // Public, vacant
Property::factory()->draft()->create();
Property::factory()->vacant()->create();
Property::factory()->leased()->create();
Property::factory()->public()->create();
Property::factory()->unlisted()->create();
Property::factory()->private()->create();
Property::factory()->requiresToken()->create();
Property::factory()->inviteOnly()->create();
Property::factory()->notAcceptingApplications()->create();
```

## ApplicationFactory

```php
Application::factory()->create();                    // Draft
Application::factory()->draft()->create();
Application::factory()->submitted()->create();
Application::factory()->underReview()->create();
Application::factory()->visitScheduled()->create();
Application::factory()->approved()->create();
Application::factory()->rejected()->create();
Application::factory()->withdrawn()->create();
```

## Relationship Factories

### Create with Specific Relationships

```php
// Using for() method
Application::factory()
    ->for($property)
    ->for($tenantProfile)
    ->create();

// Using array
FeatureItem::factory()->create(['user_id' => $this->user->id]);
```

### Create with Nested Relationships

```php
$user = User::factory()
    ->has(TenantProfile::factory()->verified())
    ->create();
```

### Create Multiple

```php
Property::factory()
    ->count(5)
    ->for($propertyManager)
    ->create();
```

## Factory State Combinations

```php
// Combine multiple states
Property::factory()
    ->vacant()
    ->public()
    ->create();

Application::factory()
    ->for($property)
    ->for($tenantProfile)
    ->submitted()
    ->create();
```

## Creating Complete Test Hierarchies

```php
// Create user with tenant profile and application
$user = User::factory()->withTenantProfile()->create();
$property = Property::factory()->vacant()->public()->create();
$application = Application::factory()
    ->for($property)
    ->for($user->tenantProfile)
    ->submitted()
    ->create();
```

```php
// Create property manager with properties
$pm = User::factory()->withPropertyManager()->create();
$properties = Property::factory()
    ->count(3)
    ->for($pm->propertyManager)
    ->create();
```
