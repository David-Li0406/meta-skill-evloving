# Multi-Tenancy Reference

## Table of Contents
- [Overview](#overview)
- [Basic Tenancy Setup](#basic-tenancy-setup)
- [Tenant Model Configuration](#tenant-model-configuration)
- [User Model Configuration](#user-model-configuration)
- [Tenant Middleware & Scopes](#tenant-middleware--scopes)
- [Tenant Routing & URLs](#tenant-routing--urls)
- [Tenant Menu & Navigation](#tenant-menu--navigation)
- [Tenant Registration & Profile](#tenant-registration--profile)
- [Resource Tenant Configuration](#resource-tenant-configuration)
- [Tenant Billing Integration](#tenant-billing-integration)
- [Advanced Tenancy Patterns](#advanced-tenancy-patterns)
- [Troubleshooting](#troubleshooting)
- [Related Topics](#related-topics)

---

## Overview

Multi-tenancy in FilamentPHP allows you to build applications where multiple organizations (tenants) share the same application instance but have completely isolated data. Each tenant has its own space within the application, and users can belong to multiple tenants with different permissions for each.

### Key Concepts

- **Tenant**: An organization, team, workspace, or any entity that owns data
- **Tenant Model**: Eloquent model representing a tenant (e.g., `Team`, `Organization`)
- **Tenant Ownership**: Relationship between users and tenants
- **Tenant Scoping**: Filtering data to show only current tenant's records
- **Tenant Menu**: UI component for switching between tenants
- **Tenant Isolation**: Ensuring data cannot be accessed across tenants

### When to Use Multi-Tenancy

- SaaS applications serving multiple organizations
- Team collaboration platforms
- Agency/client management systems
- Multi-location business management
- Any application requiring data isolation between groups

### FilamentPHP Tenancy Features

- Built-in tenant switching interface
- Automatic relationship filtering
- Tenant-aware URL routing
- Tenant registration flows
- Tenant profile management
- Billing integration (Spark)
- Global scope support
- Custom middleware integration

---

## Basic Tenancy Setup

### Minimal Tenancy Configuration

Enable basic multi-tenancy with a tenant model:

```php
use App\Models\Team;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenant(Team::class);
}
```

This enables:
- Tenant selection during login
- Tenant menu for switching
- Automatic tenant scoping for resources
- Tenant-aware URLs

### Complete Tenancy Example

Full setup with user implementation:

```php
// Panel Configuration
use App\Models\Team;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenant(Team::class)
        ->tenantRegistration()
        ->tenantProfile()
        ->tenantMenuItems([
            // Custom menu items
        ]);
}
```

```php
// User Model
<?php

namespace App\Models;

use Filament\Models\Contracts\FilamentUser;
use Filament\Models\Contracts\HasTenants;
use Filament\Panel;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Support\Collection;

class User extends Authenticatable implements FilamentUser, HasTenants
{
    public function teams(): BelongsToMany
    {
        return $this->belongsToMany(Team::class);
    }

    public function getTenants(Panel $panel): Collection
    {
        return $this->teams;
    }

    public function canAccessTenant(Model $tenant): bool
    {
        return $this->teams()->whereKey($tenant)->exists();
    }

    public function canAccessPanel(Panel $panel): bool
    {
        return true;
    }
}
```

---

## Tenant Model Configuration

### Basic Tenant Model

Minimal tenant model implementation:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Team extends Model
{
    protected $fillable = ['name'];

    public function members(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

### Custom Tenant Display Name

Implement `HasName` contract for custom naming:

```php
<?php

namespace App\Models;

use Filament\Models\Contracts\HasName;
use Illuminate\Database\Eloquent\Model;

class Team extends Model implements HasName
{
    public function getFilamentName(): string
    {
        return "{$this->name} {$this->subscription_plan}";
    }
}
```

**Example Output**: "Acme Inc Pro" instead of just "Acme Inc"

### Tenant Switcher Label

Add a label above the tenant name in the switcher:

```php
<?php

namespace App\Models;

use Filament\Models\Contracts\HasCurrentTenantLabel;
use Illuminate\Database\Eloquent\Model;

class Team extends Model implements HasCurrentTenantLabel
{
    public function getCurrentTenantLabel(): string
    {
        return 'Active team';
    }
}
```

**Output**: Shows "Active team" label in the tenant menu

### Tenant Avatar

Configure tenant avatars:

```php
<?php

namespace App\Models;

use Filament\Models\Contracts\HasAvatar;
use Illuminate\Database\Eloquent\Model;

class Team extends Model implements HasAvatar
{
    public function getFilamentAvatarUrl(): ?string
    {
        return $this->avatar_url;
    }
}
```

**Note**: Filament checks `avatar_url` attribute automatically. Implement this method for custom logic.

---

## User Model Configuration

### Implementing HasTenants Interface

Complete user model setup for multi-tenancy:

```php
<?php

namespace App\Models;

use Filament\Models\Contracts\FilamentUser;
use Filament\Models\Contracts\HasTenants;
use Filament\Panel;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Support\Collection;

class User extends Authenticatable implements FilamentUser, HasTenants
{
    // Define tenant relationship
    public function teams(): BelongsToMany
    {
        return $this->belongsToMany(Team::class);
    }

    // Get all tenants user belongs to
    public function getTenants(Panel $panel): Collection
    {
        return $this->teams;
    }

    // Validate tenant access
    public function canAccessTenant(Model $tenant): bool
    {
        return $this->teams()->whereKey($tenant)->exists();
    }

    // Panel access control
    public function canAccessPanel(Panel $panel): bool
    {
        return true;
    }
}
```

### Setting Default Tenant

Implement `HasDefaultTenant` to control initial tenant selection:

```php
<?php

namespace App\Models;

use Filament\Models\Contracts\FilamentUser;
use Filament\Models\Contracts\HasDefaultTenant;
use Filament\Models\Contracts\HasTenants;
use Filament\Panel;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Support\Collection;

class User extends Authenticatable implements 
    FilamentUser, 
    HasDefaultTenant, 
    HasTenants
{
    public function getDefaultTenant(Panel $panel): ?Model
    {
        return $this->latestTeam;
    }

    public function latestTeam(): BelongsTo
    {
        return $this->belongsTo(Team::class, 'latest_team_id');
    }

    // ... other methods
}
```

**Use Cases**:
- Redirect to user's last active team
- Default to user's primary organization
- Select based on user preferences

---

## Tenant Middleware & Scopes

### Creating Tenant Middleware

Generate middleware for applying tenant scopes:

```bash
php artisan make:middleware ApplyTenantScopes
```

### Implementing Tenant Scopes

Apply global scopes to models based on current tenant:

```php
<?php

namespace App\Http\Middleware;

use App\Models\Author;
use Closure;
use Filament\Facades\Filament;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Http\Request;

class ApplyTenantScopes
{
    public function handle(Request $request, Closure $next)
    {
        Author::addGlobalScope(
            'tenant',
            fn (Builder $query) => $query->whereBelongsTo(Filament::getTenant()),
        );

        return $next($request);
    }
}
```

### Registering Tenant Middleware

**Basic Registration** (runs on page load):

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantMiddleware([
            ApplyTenantScopes::class,
        ]);
}
```

**Persistent Registration** (runs on every request including AJAX):

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantMiddleware([
            ApplyTenantScopes::class,
        ], isPersistent: true);
}
```

### Accessing Current Tenant

Get the active tenant in your code:

```php
use Filament\Facades\Filament;

$tenant = Filament::getTenant();
```

**Usage Examples**:
```php
// In a controller or page
$team = Filament::getTenant();
$users = $team->members;

// In a resource
public static function getEloquentQuery(): Builder
{
    return parent::getEloquentQuery()
        ->where('team_id', Filament::getTenant()->id);
}
```

---

## Tenant Routing & URLs

### Default URL Structure

With basic tenant configuration:

```
/admin/{tenant}/posts
/admin/1/posts
```

### Using Slug Instead of ID

Replace tenant ID with a slug in URLs:

```php
use App\Models\Team;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenant(Team::class, slugAttribute: 'slug');
}
```

**Result**:
```
/admin/acme-inc/posts
```

**Tenant Model Requirement**:
```php
class Team extends Model
{
    protected $fillable = ['name', 'slug'];
}
```

### Custom Tenant Route Prefix

Add a prefix between panel path and tenant identifier:

```php
use App\Models\Team;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->path('admin')
        ->tenant(Team::class)
        ->tenantRoutePrefix('team');
}
```

**Result**:
```
/admin/team/1/posts
/admin/team/acme-inc/posts (with slug)
```

### Subdomain-Based Tenancy

Use subdomains to identify tenants:

```php
use App\Models\Team;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenant(Team::class, slugAttribute: 'slug')
        ->tenantDomain('{tenant:slug}.example.com');
}
```

**Result**:
```
acme-inc.example.com/posts
widget-corp.example.com/posts
```

**Requirements**:
- Wildcard DNS configuration
- `slug` column on tenant model
- Web server configuration for wildcard domains

### Full Domain Routing

Each tenant has its own domain:

```php
use App\Models\Team;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenant(Team::class, slugAttribute: 'domain')
        ->tenantDomain('{tenant:domain}');
}
```

**Result**:
```
acme-inc.com/posts
widget-corp.net/posts
subdomain.example.com/posts
```

**Tenant Model**:
```php
class Team extends Model
{
    protected $fillable = ['name', 'domain'];
}
```

---

## Tenant Menu & Navigation

### Hide Tenant Menu

Disable tenant menu if users belong to one tenant:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantMenu(false);
}
```

### Enable Tenant Search

Add search to tenant menu (auto-enabled for 10+ tenants):

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->searchableTenantMenu();
}
```

**Force Disable**:
```php
->searchableTenantMenu(false)
```

### Custom Tenant Menu Items

Add custom actions to the tenant menu:

```php
use App\Filament\Pages\Settings;
use Filament\Actions\Action;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantMenuItems([
            Action::make('settings')
                ->url(fn (): string => Settings::getUrl())
                ->icon('heroicon-m-cog-8-tooth'),
        ]);
}
```

### Customize Default Menu Items

**Profile Link**:

```php
use Filament\Actions\Action;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantMenuItems([
            'profile' => fn (Action $action) => $action->label('Edit team profile'),
        ]);
}
```

**Registration Link**:

```php
use Filament\Actions\Action;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantMenuItems([
            'register' => fn (Action $action) => $action->label('Register new team'),
        ]);
}
```

**Billing Link**:

```php
use Filament\Actions\Action;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantMenuItems([
            'billing' => fn (Action $action) => $action->label('Manage subscription'),
        ]);
}
```

### Conditional Menu Item Visibility

Show/hide menu items based on permissions:

```php
use Filament\Actions\Action;

Action::make('settings')
    ->url(fn (): string => Settings::getUrl())
    ->icon('heroicon-m-cog-8-tooth')
    ->visible(fn (): bool => auth()->user()->can('manage-team'))
```

**Using hidden()**:

```php
Action::make('settings')
    ->hidden(fn (): bool => ! auth()->user()->can('manage-team'))
```

### POST Requests from Menu Items

Execute POST requests from menu items:

```php
use Filament\Actions\Action;

Action::make('lockSession')
    ->url(fn (): string => route('lock-session'))
    ->postToUrl()
```

---

## Tenant Registration & Profile

### Enable Tenant Registration

Allow users to create new tenants:

```php
use App\Filament\Pages\Tenancy\RegisterTeam;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantRegistration(RegisterTeam::class);
}
```

### Custom Registration Page

Create a custom tenant registration page:

```php
<?php

namespace App\Filament\Pages\Tenancy;

use App\Models\Team;
use Filament\Forms\Components\TextInput;
use Filament\Pages\Tenancy\RegisterTenant;
use Filament\Schemas\Schema;

class RegisterTeam extends RegisterTenant
{
    public static function getLabel(): string
    {
        return 'Register team';
    }

    public function form(Schema $schema): Schema
    {
        return $schema
            ->components([
                TextInput::make('name')
                    ->required()
                    ->maxLength(255),
                TextInput::make('slug')
                    ->required()
                    ->unique()
                    ->maxLength(255),
            ]);
    }

    protected function handleRegistration(array $data): Team
    {
        $team = Team::create($data);

        $team->members()->attach(auth()->user());

        return $team;
    }
}
```

### Enable Tenant Profile

Allow users to edit tenant details:

```php
use App\Filament\Pages\Tenancy\EditTeamProfile;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantProfile(EditTeamProfile::class);
}
```

### Custom Profile Page

Create a custom tenant profile page:

```php
<?php

namespace App\Filament\Pages\Tenancy;

use Filament\Forms\Components\TextInput;
use Filament\Pages\Tenancy\EditTenantProfile;
use Filament\Schemas\Schema;

class EditTeamProfile extends EditTenantProfile
{
    public static function getLabel(): string
    {
        return 'Team profile';
    }

    public function form(Schema $schema): Schema
    {
        return $schema
            ->components([
                TextInput::make('name')
                    ->required()
                    ->maxLength(255),
                TextInput::make('slug')
                    ->required()
                    ->unique(ignoreRecord: true)
                    ->maxLength(255),
            ]);
    }
}
```

---

## Resource Tenant Configuration

### Default Tenant Scoping

By default, all resources are tenant-scoped. Resources automatically filter to current tenant.

### Disable Tenant Scoping for a Resource

Make a resource shared across tenants:

```php
use Filament\Resources\Resource;

class CategoryResource extends Resource
{
    protected static bool $isScopedToTenant = false;

    // ...
}
```

**Use Cases**:
- Global settings
- Shared reference data
- Multi-tenant admin resources

### Global Opt-In Tenancy Model

Disable tenancy by default, enable per-resource:

```php
// In a service provider boot() method
use Filament\Resources\Resource;

Resource::scopeToTenant(false);
```

**Enable for specific resource**:

```php
use Filament\Resources\Resource;

class PostResource extends Resource
{
    protected static bool $isScopedToTenant = true;

    // ...
}
```

### Custom Tenant Relationship Name

Override default relationship name for resources:

```php
use Filament\Resources\Resource;

class PostResource extends Resource
{
    protected static ?string $tenantRelationshipName = 'blogPosts';

    // ...
}
```

**Tenant Model**:
```php
class Team extends Model
{
    public function blogPosts()
    {
        return $this->hasMany(Post::class);
    }
}
```

### Custom Ownership Relationship

Change the relationship used to determine record ownership:

**Global Configuration**:

```php
use App\Models\Team;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenant(Team::class, ownershipRelationship: 'owner');
}
```

**Per-Resource Configuration**:

```php
use Filament\Resources\Resource;

class PostResource extends Resource
{
    protected static ?string $tenantOwnershipRelationshipName = 'owner';

    // ...
}
```

**Post Model**:
```php
class Post extends Model
{
    public function owner()
    {
        return $this->belongsTo(Team::class, 'team_id');
    }
}
```

---

## Tenant Billing Integration

### Laravel Spark Integration

Install Spark billing provider:

```bash
composer require filament/spark-billing-provider
```

Configure panel:

```php
use Filament\Billing\Providers\SparkBillingProvider;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantBillingProvider(new SparkBillingProvider());
}
```

### Custom Billing Route Slug

Customize the billing URL:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantBillingRouteSlug('billing');
}
```

**Result**: `/admin/{tenant}/billing`

### Require Active Subscription

Enforce subscription requirement:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->requiresTenantSubscription();
}
```

**Behavior**: Redirects unsubscribed users to billing page.

### Per-Resource Subscription Requirement

Override global setting per resource/page:

```php
use Filament\Resources\Resource;
use Filament\Panel;

class PostResource extends Resource
{
    public static function isTenantSubscriptionRequired(Panel $panel): bool
    {
        return true;
    }

    // ...
}
```

### Custom Billing Provider

Create a custom billing provider:

```php
<?php

namespace App\Billing;

use App\Http\Middleware\RedirectIfUserNotSubscribed;
use Filament\Billing\Providers\Contracts\BillingProvider;
use Illuminate\Http\RedirectResponse;

class ExampleBillingProvider implements BillingProvider
{
    public function getRouteAction(): string
    {
        return function (): RedirectResponse {
            return redirect('https://billing.example.com');
        };
    }

    public function getSubscribedMiddleware(): string
    {
        return RedirectIfUserNotSubscribed::class;
    }
}
```

**Register**:

```php
use App\Billing\ExampleBillingProvider;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantBillingProvider(new ExampleBillingProvider());
}
```

---

## Advanced Tenancy Patterns

### Simple One-to-Many Tenancy

For users belonging to a single team, use Eloquent global scopes:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    protected static function booted(): void
    {
        static::addGlobalScope('team', function (Builder $query) {
            if (auth()->hasUser()) {
                $query->where('team_id', auth()->user()->team_id);
                // or with a `team` relationship defined:
                $query->whereBelongsTo(auth()->user()->team);
            }
        });
    }
}
```

**Automatically Set Tenant ID**:

```php
<?php

namespace App\Observers;

use App\Models\Post;

class PostObserver
{
    public function creating(Post $post): void
    {
        if (auth()->hasUser()) {
            $post->team_id = auth()->user()->team_id;
            // or with a `team` relationship defined:
            $post->team()->associate(auth()->user()->team);
        }
    }
}
```

**Register Observer**:

```php
// In a service provider boot() method
use App\Models\Post;
use App\Observers\PostObserver;

Post::observe(PostObserver::class);
```

### Multi-Tenant Validation

Use scoped validation to respect tenant boundaries:

```php
use Filament\Forms\Components\TextInput;

TextInput::make('email')
    ->scopedUnique()
```

**With Custom Query**:

```php
use Filament\Forms\Components\TextInput;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\SoftDeletingScope;

TextInput::make('email')
    ->scopedUnique(modifyQueryUsing: function (Builder $query) {
        return $query->withoutGlobalScope(SoftDeletingScope::class);
    })
```

**Scoped Exists Validation**:

```php
use Filament\Forms\Components\TextInput;

TextInput::make('category_id')
    ->scopedExists()
```

### Tenant-Aware Actions

Scope relationship actions to current tenant:

```php
use Filament\Actions\AssociateAction;
use Illuminate\Database\Eloquent\Builder;

AssociateAction::make()
    ->recordSelectOptionsQuery(fn (Builder $query) => $query->whereBelongsTo(auth()->user()))
```

### Excluding Global Scopes

Remove tenant scopes when needed:

**Disable All Scopes**:

```php
public static function getEloquentQuery(): Builder
{
    return parent::getEloquentQuery()->withoutGlobalScopes();
}
```

**Disable Specific Scopes**:

```php
public static function getEloquentQuery(): Builder
{
    return parent::getEloquentQuery()->withoutGlobalScopes([TenantScope::class]);
}
```

---

## Troubleshooting

### Common Issues

#### Tenant Menu Not Showing

**Symptoms**: No tenant switcher visible

**Solutions**:
1. Verify `->tenant(Team::class)` is configured
2. Check user implements `HasTenants` interface
3. Ensure `getTenants()` returns a non-empty collection
4. Confirm panel authentication is working

#### Cannot Access Tenant Data

**Symptoms**: 403 errors or empty results

**Solutions**:
1. Check `canAccessTenant()` implementation
2. Verify user-tenant relationship exists in database
3. Test middleware is registered correctly
4. Ensure global scopes are properly applied

#### Wrong Tenant Selected

**Symptoms**: User sees incorrect tenant after login

**Solutions**:
1. Implement `HasDefaultTenant` interface
2. Check `getDefaultTenant()` logic
3. Verify `latest_team_id` or similar column
4. Clear session and test again

#### Tenant Scopes Not Working

**Symptoms**: Seeing data from other tenants

**Solutions**:
1. Verify middleware is registered with `isPersistent: true`
2. Check global scope implementation
3. Ensure `Filament::getTenant()` returns correct tenant
4. Test resource has `$isScopedToTenant = true` (default)

#### Subdomain Routing Issues

**Symptoms**: 404 errors on tenant subdomains

**Solutions**:
1. Configure wildcard DNS: `*.example.com → your-server-ip`
2. Configure web server for wildcard domains
3. Verify `tenantDomain()` configuration
4. Check `slug` or `domain` column exists on tenant model
5. Test DNS propagation

### Performance Issues

#### Slow Tenant Switching

**Optimizations**:
1. Eager load tenant relationships
2. Cache tenant data
3. Use database indexes on tenant foreign keys
4. Optimize tenant query in `getTenants()`

#### Memory Usage with Many Tenants

**Solutions**:
1. Paginate tenant lists in custom menus
2. Use lazy loading for tenant relationships
3. Implement tenant search
4. Limit tenant count per user

### Security Concerns

#### Tenant Data Leakage

**Preventions**:
1. Always use persistent tenant middleware
2. Implement comprehensive global scopes
3. Test cross-tenant access attempts
4. Use scoped validation rules
5. Audit tenant access logs

#### Subdomain Hijacking

**Preventions**:
1. Validate tenant slugs/domains on registration
2. Reserve system subdomains
3. Implement slug/domain uniqueness validation
4. Monitor DNS configuration changes

---

## Related Topics

- **[PANEL_CONFIGURATION.md](PANEL_CONFIGURATION.md)**: Panel setup and tenant menu configuration
- **[RESOURCES.md](RESOURCES.md)**: Resource tenant scoping and configuration
- **[FORMS.md](FORMS.md)**: Tenant-aware form validation
- **[ACTIONS.md](ACTIONS.md)**: Tenant-scoped actions and relationships
- **[CODE_QUALITY.md](CODE_QUALITY.md)**: Multi-tenancy best practices and patterns
- **[TESTING.md](TESTING.md)**: Testing multi-tenant applications

---

**Last Updated**: January 18, 2026  
**FilamentPHP Version**: 4.x  
**Status**: Complete ✅
