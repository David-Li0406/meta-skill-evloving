---
name: creating-service-providers
description: Create Laravel Service Provider classes for binding services, registering singletons, and application bootstrapping. Use when creating service providers, binding interfaces, registering services, or when user mentions service providers, dependency injection, service container, or application bootstrapping.
---

# Create Laravel Service Providers

Create Service Providers for binding services to the container, registering singletons, and bootstrapping application components. Service Providers are the central place to configure application services and extend Laravel's functionality.

## File Structure

Service Providers are stored in the Providers directory:

```
app/Providers/{Name}ServiceProvider.php
```

**Examples:**

- `app/Providers/AppServiceProvider.php`
- `app/Providers/TwoFactorAuthenticationServiceProvider.php`
- `app/Providers/ImageProcessorServiceProvider.php`

## Core Conventions

### 1. Service Provider Structure

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Override;

final class {Name}ServiceProvider extends ServiceProvider
{
    #[Override]
    public function register(): void
    {
        // Bind services, interfaces, and singletons
    }

    public function boot(): void
    {
        // Bootstrap services, register mixins, etc.
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final class` modifier
- Extend `ServiceProvider` base class
- Use `#[Override]` on `register()` method
- Use `register()` for bindings
- Use `boot()` for bootstrapping
- Register provider in `bootstrap/providers.php`

### 2. Binding Services

```php
#[Override]
public function register(): void
{
    $this->app->singleton(ServiceInterface::class, ServiceImplementation::class);

    $this->app->bind(AnotherInterface::class, AnotherImplementation::class);
}
```

### 3. Conditional Registration

```php
#[Override]
public function register(): void
{
    // @codeCoverageIgnoreStart

    if ($this->app->isLocal()) {
        $this->app->register(TelescopeServiceProvider::class);
    }

    // @codeCoverageIgnoreEnd
}
```

## Examples

### Example 1: AppServiceProvider

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use App\Mixins\RequestMixin;
use Carbon\CarbonImmutable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Http\Request;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\Date;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Vite;
use Illuminate\Support\ServiceProvider;
use Override;
use ReflectionException;

final class AppServiceProvider extends ServiceProvider
{
    #[Override]
    public function register(): void
    {
        // @codeCoverageIgnoreStart

        if ($this->app->isLocal()) {
            $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
            $this->app->register(TelescopeServiceProvider::class);
        }

        // @codeCoverageIgnoreEnd
    }

    /**
     * @throws ReflectionException
     */
    public function boot(): void
    {
        $this->configureCommands();
        $this->configureModels();
        $this->configureVite();
        $this->configureDates();
        $this->configureMixins();
        $this->configurePagination();
    }

    private function configureCommands(): void
    {
        DB::prohibitDestructiveCommands($this->app->isProduction());
    }

    private function configureModels(): void
    {
        Model::unguard();
        Model::shouldBeStrict(! $this->app->isProduction());
        Model::automaticallyEagerLoadRelationships();
    }

    private function configureVite(): void
    {
        Vite::usePrefetchStrategy('aggressive');
    }

    private function configureDates(): void
    {
        Date::use(CarbonImmutable::class);
    }

    /**
     * @throws ReflectionException
     */
    private function configureMixins(): void
    {
        Request::mixin(new RequestMixin);
    }

    private function configurePagination(): void
    {
        $this->app->extend(LengthAwarePaginator::class, function (LengthAwarePaginator $paginator): LengthAwarePaginator {
            // Ensures there are not too many links in the pagination
            $paginator->onEachSide(1);

            return $paginator;
        });
    }
}
```

### Example 2: Service with Interface Binding

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use App\Support\ImageProcessor\Contracts\ImageProcessor;
use App\Support\ImageProcessor\Providers\Intervention\InterventionImageProcessor;
use Illuminate\Support\ServiceProvider;
use Override;

final class ImageProcessorServiceProvider extends ServiceProvider
{
    #[Override]
    public function register(): void
    {
        $this->app->singleton(ImageProcessor::class, InterventionImageProcessor::class);
    }
}
```

### Example 3: Service Provider with Configuration

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use App\Support\TwoFactorAuthentication\Contracts\TwoFactorAuthentication;
use App\Support\TwoFactorAuthentication\Providers\Google2FA\GoogleTwoFactorAuthentication;
use Illuminate\Container\Attributes\Config;
use Illuminate\Support\ServiceProvider;
use Override;

final class TwoFactorAuthenticationServiceProvider extends ServiceProvider
{
    #[Override]
    public function register(): void
    {
        $this->app->singleton(TwoFactorAuthentication::class, function ($app): GoogleTwoFactorAuthentication {
            return new GoogleTwoFactorAuthentication(
                issuer: $app->make(#[Config('app.name')] string),
            );
        });
    }
}
```

### Example 4: Service Provider with Deferrable Loading

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use App\Services\PaymentGateway;
use App\Services\StripePaymentGateway;
use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;
use Override;

final class PaymentServiceProvider extends ServiceProvider implements DeferrableProvider
{
    #[Override]
    public function register(): void
    {
        $this->app->singleton(PaymentGateway::class, StripePaymentGateway::class);
    }

    /**
     * @return list<class-string>
     */
    #[Override]
    public function provides(): array
    {
        return [PaymentGateway::class];
    }
}
```

## Registering Service Providers

Add to `bootstrap/providers.php`:

```php
return [
    App\Providers\AppServiceProvider::class,
    App\Providers\ImageProcessorServiceProvider::class,
    App\Providers\TwoFactorAuthenticationServiceProvider::class,
];
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't skip #[Override] on register()
public function register(): void // ❌ Missing #[Override]

// Don't put business logic in providers
public function boot(): void
{
    User::query()->where('active', false)->delete(); // ❌ No business logic
}

// Don't bind in boot() method
public function boot(): void
{
    $this->app->singleton(Service::class); // ❌ Use register()
}

// Don't skip @codeCoverageIgnore for conditional registration
if ($this->app->isLocal()) { // ❌ Add @codeCoverageIgnore
    $this->app->register(TelescopeServiceProvider::class);
}

// Don't use mutable class
class AppServiceProvider extends ServiceProvider // ❌ Use final class
```

### ✅ Do This Instead

```php
// Use #[Override] on register()
#[Override]
public function register(): void

// Keep providers focused on service registration
public function boot(): void
{
    $this->configureModels();
    $this->configureDates();
}

// Bind in register() method
#[Override]
public function register(): void
{
    $this->app->singleton(Service::class);
}

// Wrap conditional registration
#[Override]
public function register(): void
{
    // @codeCoverageIgnoreStart

    if ($this->app->isLocal()) {
        $this->app->register(TelescopeServiceProvider::class);
    }

    // @codeCoverageIgnoreEnd
}

// Use final class
final class AppServiceProvider extends ServiceProvider
```

## Quality Standards

- All service providers must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Refactored with Rector
- Covered by tests where applicable
- Conditional registrations wrapped with `@codeCoverageIgnore`
