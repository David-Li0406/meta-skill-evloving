# Panel Configuration Reference

## Table of Contents
- [Overview](#overview)
- [Basic Panel Setup](#basic-panel-setup)
- [Authentication Features](#authentication-features)
- [Multi-Factor Authentication (MFA)](#multi-factor-authentication-mfa)
- [Profile Page Configuration](#profile-page-configuration)
- [SPA Mode & Navigation](#spa-mode--navigation)
- [Sidebar & Topbar Configuration](#sidebar--topbar-configuration)
- [Middleware & Authorization](#middleware--authorization)
- [Assets & Theming](#assets--theming)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)
- [Related Topics](#related-topics)

---

## Overview

Panel configuration is the foundation of any FilamentPHP application. A panel represents an entire admin interface with its own authentication, navigation, resources, and configuration. This reference covers all aspects of configuring Filament panels, from basic setup to advanced features like MFA, SPA mode, and multi-tenancy integration.

### Key Concepts

- **Panel Provider**: Service provider that registers and configures your panel
- **Panel Path**: URL segment where the panel is accessible (e.g., `/admin`)
- **Panel ID**: Unique identifier for the panel (e.g., `admin`, `app`)
- **Authentication**: Built-in features for login, registration, password reset, and email verification
- **SPA Mode**: Single-page application mode for faster navigation
- **Middleware**: Request processing layers for security and customization
- **Assets**: CSS/JS files specific to the panel

### When to Use Panel Configuration

- Setting up a new admin interface
- Configuring authentication flows
- Enabling MFA for enhanced security
- Customizing navigation and layout
- Implementing multi-panel applications
- Optimizing performance with SPA mode

---

## Basic Panel Setup

### Creating a New Panel

Generate a new panel using the Artisan command:

```bash
php artisan make:filament-panel app
```

This creates:
- `app/Providers/Filament/AppPanelProvider.php`
- Registers the provider automatically
- Sets up basic panel configuration

### Configuring Panel Path

Set the URL path where the panel is accessible:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->id('admin')
        ->path('admin');
}
```

**URL Result**: `/admin`

### Panel at Root URL

To make a panel accessible at the root URL:

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->path('');
}
```

⚠️ **Warning**: Ensure no conflicting routes in `routes/web.php`.

### Domain-Specific Panels

Restrict a panel to a specific domain:

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->domain('admin.example.com');
}
```

**Use Case**: Subdomain-based admin interfaces.

### Multiple Panels

Configure different panels for different user types:

```php
// Admin Panel
public function panel(Panel $panel): Panel
{
    return $panel
        ->id('admin')
        ->path('admin')
        ->authGuard('admin');
}

// Staff Panel
public function panel(Panel $panel): Panel
{
    return $panel
        ->id('staff')
        ->path('staff')
        ->authGuard('web');
}
```

---

## Authentication Features

### Basic Authentication Setup

Enable all standard authentication features:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->login()
        ->registration()
        ->passwordReset()
        ->emailVerification()
        ->emailChangeVerification()
        ->profile();
}
```

### Login Configuration

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->login()
        ->loginRouteSlug('login');
}
```

### Registration Configuration

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->registration()
        ->registrationRouteSlug('register');
}
```

### Password Reset Configuration

Configure password reset with custom route slugs:

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->passwordReset()
        ->passwordResetRoutePrefix('password-reset')
        ->passwordResetRequestRouteSlug('request')
        ->passwordResetRouteSlug('reset')
        ->authPasswordBroker('users');
}
```

**Route Structure**:
- Request: `/password-reset/request`
- Reset: `/password-reset/reset`

### Email Verification Configuration

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->emailVerification()
        ->emailVerificationRoutePrefix('email-verification')
        ->emailVerificationPromptRouteSlug('prompt')
        ->emailVerificationRouteSlug('verify');
}
```

### Custom Authentication Route Slugs

Customize all authentication route slugs:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->loginRouteSlug('login')
        ->registrationRouteSlug('register')
        ->passwordResetRoutePrefix('password-reset')
        ->passwordResetRequestRouteSlug('request')
        ->passwordResetRouteSlug('reset')
        ->emailVerificationRoutePrefix('email-verification')
        ->emailVerificationPromptRouteSlug('prompt')
        ->emailVerificationRouteSlug('verify')
        ->emailChangeVerificationRoutePrefix('email-change-verification')
        ->emailChangeVerificationRouteSlug('verify');
}
```

### Custom Authentication Pages

Replace default authentication pages with custom implementations:

```php
use App\Filament\Pages\Auth\EditProfile;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->profile(EditProfile::class);
}
```

**Custom Edit Profile Page**:

```php
<?php

namespace App\Filament\Pages\Auth;

use Filament\Auth\Pages\EditProfile as BaseEditProfile;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;

class EditProfile extends BaseEditProfile
{
    public function form(Schema $schema): Schema
    {
        return $schema
            ->components([
                TextInput::make('username')
                    ->required()
                    ->maxLength(255),
                $this->getNameFormComponent(),
                $this->getEmailFormComponent(),
                $this->getPasswordFormComponent(),
                $this->getPasswordConfirmationFormComponent(),
            ]);
    }
}
```

### Customizing Specific Authentication Fields

Override individual field methods without redefining the entire form:

```php
use Filament\Schemas\Components\Component;

protected function getPasswordFormComponent(): Component
{
    return parent::getPasswordFormComponent()
        ->revealable(false);
}
```

### Authentication Guard Configuration

Specify which authentication guard to use:

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->authGuard('web');
}
```

### Panel Access Control

Implement `FilamentUser` interface to control panel access:

```php
<?php

namespace App\Models;

use Filament\Models\Contracts\FilamentUser;
use Filament\Panel;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable implements FilamentUser
{
    public function canAccessPanel(Panel $panel): bool
    {
        return str_ends_with($this->email, '@yourdomain.com') 
            && $this->hasVerifiedEmail();
    }
}
```

### Panel-Specific Access Control

Grant different access based on panel ID:

```php
public function canAccessPanel(Panel $panel): bool
{
    if ($panel->getId() === 'admin') {
        return str_ends_with($this->email, '@yourdomain.com') 
            && $this->hasVerifiedEmail();
    }

    return true;
}
```

### Guest Access Configuration

Allow guest access by removing authentication:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->authMiddleware([])
        ->widgets([]);
}
```

**Requirements**:
- Remove `Authenticate` middleware from `authMiddleware()`
- Remove `->login()` and other auth features
- Remove `AccountWidget` from widgets

### Guest Read Access via Policies

Allow unauthenticated users to view resources:

```php
// In your Model Policy
public function viewAny(?User $user): bool
{
    return true;
}

public function view(?User $user): bool
{
    return true;
}
```

### Disable Password Reveal

Disable password visibility toggle:

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->revealablePasswords(false);
}
```

---

## Multi-Factor Authentication (MFA)

### App-Based Authentication

Enable authenticator app MFA (Google Authenticator, Authy, etc.):

```php
use Filament\Auth\MultiFactor\App\AppAuthentication;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->profile()
        ->multiFactorAuthentication([
            AppAuthentication::make(),
        ]);
}
```

**Database Migration Required**:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->text('app_authentication_secret')->nullable();
});
```

**User Model Implementation**:

```php
use Filament\Auth\MultiFactor\App\Contracts\HasAppAuthentication;
use Filament\Auth\MultiFactor\App\Concerns\InteractsWithAppAuthentication;
use Filament\Models\Contracts\FilamentUser;
use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable implements 
    FilamentUser, 
    HasAppAuthentication, 
    MustVerifyEmail
{
    use InteractsWithAppAuthentication;
    
    // ...
}
```

### Email-Based Authentication

Enable email code MFA:

```php
use Filament\Auth\MultiFactor\Email\EmailAuthentication;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->profile()
        ->multiFactorAuthentication([
            EmailAuthentication::make(),
        ]);
}
```

**Database Migration Required**:

```php
Schema::table('users', function (Blueprint $table) {
    $table->boolean('has_email_authentication')->default(false);
});
```

**User Model Implementation**:

```php
use Filament\Auth\MultiFactor\Email\Contracts\HasEmailAuthentication;
use Filament\Auth\MultiFactor\Email\Concerns\InteractsWithEmailAuthentication;
use Filament\Models\Contracts\FilamentUser;
use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable implements 
    FilamentUser, 
    HasEmailAuthentication, 
    MustVerifyEmail
{
    use InteractsWithEmailAuthentication;
    
    // ...
}
```

### Require MFA Setup

Force users to configure MFA after login:

```php
use Filament\Auth\MultiFactor\App\AppAuthentication;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->multiFactorAuthentication([
            AppAuthentication::make(),
        ], isRequired: true);
}
```

### Recovery Codes

Enable recovery codes for app authentication:

```php
use Filament\Auth\MultiFactor\App\AppAuthentication;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->multiFactorAuthentication([
            AppAuthentication::make()
                ->recoverable(),
        ]);
}
```

**Database Migration Required**:

```php
Schema::table('users', function (Blueprint $table) {
    $table->text('app_authentication_recovery_codes')->nullable();
});
```

**User Model Implementation**:

```php
use Filament\Auth\MultiFactor\App\Contracts\HasAppAuthentication;
use Filament\Auth\MultiFactor\App\Concerns\InteractsWithAppAuthentication;
use Filament\Auth\MultiFactor\App\Contracts\HasAppAuthenticationRecovery;
use Filament\Auth\MultiFactor\App\Concerns\InteractsWithAppAuthenticationRecovery;
use Filament\Models\Contracts\FilamentUser;
use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable implements 
    FilamentUser, 
    HasAppAuthentication, 
    HasAppAuthenticationRecovery, 
    MustVerifyEmail
{
    use InteractsWithAppAuthentication;
    use InteractsWithAppAuthenticationRecovery;
    
    // ...
}
```

### Custom Recovery Code Count

Set the number of recovery codes generated:

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->multiFactorAuthentication([
            AppAuthentication::make()
                ->recoverable()
                ->recoveryCodeCount(10),
        ]);
}
```

**Default**: 8 recovery codes

### Disable Recovery Code Regeneration

Prevent users from regenerating recovery codes:

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->multiFactorAuthentication([
            AppAuthentication::make()
                ->recoverable()
                ->regenerableRecoveryCodes(false),
        ]);
}
```

### Customize App Brand Name

Change the issuer name displayed in authenticator apps:

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->multiFactorAuthentication([
            AppAuthentication::make()
                ->brandName('Filament Demo'),
        ]);
}
```

### Email Code Expiration

Set custom expiration time for email codes:

```php
use Filament\Auth\MultiFactor\Email\EmailAuthentication;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->multiFactorAuthentication([
            EmailAuthentication::make()
                ->codeExpiryMinutes(2),
        ]);
}
```

### TOTP Code Window

Configure validity window for time-based codes:

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->multiFactorAuthentication([
            AppAuthentication::make()
                ->codeWindow(4),
        ]);
}
```

**Default Window**: 8 (4 minutes on either side = 8 minutes total)
**Custom Window**: 4 (2 minutes on either side = 4 minutes total)

---

## Profile Page Configuration

### Enable Profile Page

Basic profile page with name, email, and password fields:

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->profile();
}
```

### Profile Page with Sidebar

Include sidebar navigation on the profile page:

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->profile(isSimple: false);
}
```

**Default**: Profile page has no sidebar for tenancy compatibility.

### Custom Profile Page

Use a custom profile page class:

```php
use App\Filament\Pages\Auth\EditProfile;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->profile(EditProfile::class);
}
```

**Example Custom Profile Class**:

```php
<?php

namespace App\Filament\Pages\Auth;

use Filament\Auth\Pages\EditProfile as BaseEditProfile;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;

class EditProfile extends BaseEditProfile
{
    public function form(Schema $schema): Schema
    {
        return $schema
            ->components([
                TextInput::make('username')
                    ->required()
                    ->maxLength(255),
                $this->getNameFormComponent(),
                $this->getEmailFormComponent(),
                $this->getPasswordFormComponent(),
                $this->getPasswordConfirmationFormComponent(),
            ]);
    }
}
```

---

## SPA Mode & Navigation

### Enable SPA Mode

Use Livewire's `wire:navigate` for faster page transitions:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->spa();
}
```

**Benefits**:
- Faster page transitions
- Loading bar for longer requests
- Preserves scroll position
- Reduces server load

### SPA with Prefetching

Prefetch pages on link hover for instant navigation:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->spa(hasPrefetching: true);
}
```

⚠️ **Warning**: Use cautiously with heavy pages to avoid high bandwidth/server load.

### SPA URL Exceptions

Exclude specific URLs from SPA navigation:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->spa()
        ->spaUrlExceptions(fn (): array => [
            url('/admin'),
        ]);
}
```

### SPA URL Exceptions with Resources

Exclude resource URLs:

```php
use App\Filament\Resources\Posts\PostResource;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->spa()
        ->spaUrlExceptions(fn (): array => [
            url('/admin'),
            PostResource::getUrl(),
        ]);
}
```

**Note**: Requires exact URL matching including domain and protocol.

### SPA URL Exceptions with Wildcards

Use wildcard patterns to exclude URL hierarchies:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->spa()
        ->spaUrlExceptions([
            '*/admin/posts/*',
        ]);
}
```

### Unsaved Changes Alerts

Warn users about unsaved changes before navigation:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->unsavedChangesAlerts();
}
```

**Applies To**:
- Create and Edit resource pages
- Open action modals

---

## Sidebar & Topbar Configuration

### Top Navigation

Switch from sidebar to top navigation:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->topNavigation();
}
```

### Collapsible Sidebar on Desktop

Allow users to collapse the sidebar:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->sidebarCollapsibleOnDesktop();
}
```

**Behavior**: Sidebar shows navigation icons when collapsed.

### Fully Collapsible Sidebar on Desktop

Completely hide the sidebar when collapsed:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->sidebarFullyCollapsibleOnDesktop();
}
```

**Behavior**: Sidebar and icons completely hidden when collapsed.

### Custom Sidebar Width

Set a custom sidebar width:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->sidebarWidth('40rem');
}
```

### Custom Collapsed Sidebar Width

Set width for collapsed sidebar:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->sidebarCollapsibleOnDesktop()
        ->collapsedSidebarWidth('9rem');
}
```

### Replace Sidebar/Topbar Livewire Components

Use custom Livewire components:

```php
use App\Livewire\Sidebar;
use App\Livewire\Topbar;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->sidebarLivewireComponent(Sidebar::class)
        ->topbarLivewireComponent(Topbar::class);
}
```

### Disable Navigation

Remove navigation entirely:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->navigation(false);
}
```

### Custom Navigation Groups

Define navigation groups with labels and icons:

```php
use Filament\Navigation\NavigationGroup;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->navigationGroups([
            NavigationGroup::make()
                ->label('Shop')
                ->icon('heroicon-o-shopping-cart'),
            NavigationGroup::make()
                ->label('Blog')
                ->icon('heroicon-o-pencil'),
            NavigationGroup::make()
                ->label(fn (): string => __('navigation.settings'))
                ->icon('heroicon-o-cog-6-tooth')
                ->collapsed(),
        ]);
}
```

### Collapsible Navigation Groups

Enable/disable collapsible navigation groups globally:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->collapsibleNavigationGroups(false);
}
```

### Refresh Sidebar Programmatically

**From Livewire Component**:

```php
$this->dispatch('refresh-sidebar');
```

**From Action Closure**:

```php
use Filament\Actions\Action;
use Livewire\Component;

Action::make('create')
    ->action(function (Component $livewire) {
        // ...
        
        $livewire->dispatch('refresh-sidebar');
    })
```

**From Alpine.js**:

```html
<button x-on:click="$dispatch('refresh-sidebar')" type="button">
    Refresh Sidebar
</button>
```

**From JavaScript**:

```javascript
window.dispatchEvent(new CustomEvent('refresh-sidebar'));
```

---

## Middleware & Authorization

### Authentication Middleware

Apply middleware to authenticated routes:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->authMiddleware([
            // ...
        ]);
}
```

### Persistent Authentication Middleware

Run middleware on every Livewire AJAX request:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->authMiddleware([
            // ...
        ], isPersistent: true);
}
```

### Panel Middleware

Apply middleware to all panel routes (initial page load only):

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->middleware([
            // ...
        ]);
}
```

### Persistent Panel Middleware

Run middleware on all panel requests including AJAX:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->middleware([
            // ...
        ], isPersistent: true);
}
```

### Tenant Middleware

Apply middleware to tenant-aware routes:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->tenantMiddleware([
            // ...
        ]);
}
```

### Persistent Tenant Middleware

Run tenant middleware on all requests:

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

### Strict Authorization Mode

Throw exceptions for missing policies:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->strictAuthorization();
}
```

**Behavior**: Filament throws exceptions if required policy methods don't exist.

---

## Assets & Theming

### Register Panel-Specific Assets

Add custom CSS and JavaScript files:

```php
use Filament\Panel;
use Filament\Support\Assets\Css;
use Filament\Support\Assets\Js;

public function panel(Panel $panel): Panel
{
    return $panel
        ->assets([
            Css::make('custom-stylesheet', resource_path('css/custom.css')),
            Js::make('custom-script', resource_path('js/custom.js')),
        ]);
}
```

**Required**: Run `php artisan filament:assets` after registration.

### Vite Theme

Register a Vite-compiled theme:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->viteTheme('resources/css/filament/admin/theme.css');
}
```

**Vite Configuration**:

```javascript
input: [
    // ...
    'resources/css/filament/admin/theme.css',
]
```

**Build**: Run `npm run build`

### Predefined Colors

Configure panel colors:

```php
use Filament\Panel;
use Filament\Support\Colors\Color;

public function panel(Panel $panel): Panel
{
    return $panel
        ->colors([
            'danger' => Color::Rose,
            'gray' => Color::Gray,
            'info' => Color::Blue,
            'primary' => Color::Indigo,
            'success' => Color::Emerald,
            'warning' => Color::Orange,
        ]);
}
```

### Dark Mode Configuration

**Enable Dark Mode** (default):

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->darkMode(true);
}
```

**Disable Dark Mode**:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->darkMode(false);
}
```

### Default Theme Mode

Set initial theme mode (override system preference):

```php
use Filament\Enums\ThemeMode;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->defaultThemeMode(ThemeMode::Light);
}
```

**Options**: `ThemeMode::Light`, `ThemeMode::Dark`

---

## Advanced Configuration

### Maximum Content Width

Set panel-wide maximum content width:

```php
use Filament\Panel;
use Filament\Support\Enums\Width;

public function panel(Panel $panel): Panel
{
    return $panel
        ->maxContentWidth(Width::Full);
}
```

**Options**: 
- `Width::ExtraSmall`
- `Width::Small`
- `Width::Medium`
- `Width::Large`
- `Width::ExtraLarge`
- `Width::TwoExtraLarge`
- `Width::ThreeExtraLarge`
- `Width::FourExtraLarge`
- `Width::FiveExtraLarge`
- `Width::SixExtraLarge`
- `Width::SevenExtraLarge` (default)
- `Width::Full`
- `Width::Screen`

### Simple Page Max Content Width

Set maximum width for simple pages (login, registration):

```php
use Filament\Panel;
use Filament\Support\Enums\Width;

public function panel(Panel $panel): Panel
{
    return $panel
        ->simplePageMaxContentWidth(Width::Small);
}
```

**Default**: `Width::Large`

### Sub-Navigation Position

Configure default sub-navigation position:

```php
use Filament\Pages\Enums\SubNavigationPosition;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->subNavigationPosition(SubNavigationPosition::End);
}
```

**Options**:
- `SubNavigationPosition::Start` (default)
- `SubNavigationPosition::End`
- `SubNavigationPosition::Top` (renders as tabs)

### Database Transactions

**Enable Globally**:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->databaseTransactions();
}
```

**Opt-In Per Page**:

```php
use Filament\Resources\Pages\CreateRecord;

class CreatePost extends CreateRecord
{
    protected ?bool $hasDatabaseTransactions = true;

    // ...
}
```

**Opt-Out Per Page**:

```php
use Filament\Resources\Pages\CreateRecord;

class CreatePost extends CreateRecord
{
    protected ?bool $hasDatabaseTransactions = false;

    // ...
}
```

**Opt-In Per Action**:

```php
CreateAction::make()
    ->databaseTransaction()
```

**Opt-Out Per Action**:

```php
CreateAction::make()
    ->databaseTransaction(false)
```

### Error Notifications

**Disable Globally**:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->errorNotifications(false);
}
```

**Control Per Page**:

```php
use Filament\Pages\Dashboard as BaseDashboard;

class Dashboard extends BaseDashboard
{
    protected ?bool $hasErrorNotifications = true;
    // or
    protected ?bool $hasErrorNotifications = false;

    // ...
}
```

### Boot Lifecycle Hook

Execute code on every panel request:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->bootUsing(function (Panel $panel) {
            // Custom initialization logic
        });
}
```

**Runs**: After all service providers have booted.

### Default Edit Page Redirect

Set global redirect behavior after editing:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->resourceEditPageRedirect('index'); // or 'view'
}
```

---

## Troubleshooting

### Common Issues

#### Panel Not Accessible

**Symptoms**: 404 error when accessing panel URL

**Solutions**:
1. Clear route cache: `php artisan route:clear`
2. Verify panel path configuration
3. Check domain configuration
4. Ensure panel provider is registered in `config/app.php`

#### Authentication Redirect Loop

**Symptoms**: Continuous redirects between login and dashboard

**Solutions**:
1. Verify `canAccessPanel()` implementation
2. Check authentication guard configuration
3. Ensure email verification is complete (if enabled)
4. Clear authentication session: `php artisan session:flush`

#### MFA Setup Not Showing

**Symptoms**: MFA options not visible in profile

**Solutions**:
1. Ensure `->profile()` is enabled
2. Verify database migrations are run
3. Check user model implements required interfaces
4. Confirm traits are used in user model

#### SPA Mode Not Working

**Symptoms**: Full page reloads instead of SPA transitions

**Solutions**:
1. Check `wire:navigate` is enabled in custom views
2. Verify no conflicting JavaScript
3. Clear browser cache
4. Check SPA URL exceptions aren't excluding pages

#### Assets Not Loading

**Symptoms**: Custom CSS/JS not appearing

**Solutions**:
1. Run `php artisan filament:assets`
2. Clear cache: `php artisan cache:clear`
3. Verify asset paths are correct
4. Check file permissions
5. Run `npm run build` for Vite assets

### Performance Issues

#### Slow Panel Loading

**Optimizations**:
1. Enable SPA mode
2. Use deferred loading for widgets
3. Optimize database queries
4. Enable caching for navigation
5. Consider lazy loading for resources

#### High Memory Usage

**Solutions**:
1. Reduce widget polling frequency
2. Limit table pagination options
3. Use database transactions selectively
4. Optimize relationship loading

### Security Concerns

#### Unauthorized Access

**Preventions**:
1. Implement `FilamentUser` interface properly
2. Use strict authorization mode
3. Apply appropriate middleware
4. Enable MFA for sensitive panels
5. Regular security audits

---

## Related Topics

- **[RESOURCES.md](RESOURCES.md)**: Resource configuration and CRUD operations
- **[FORMS.md](FORMS.md)**: Form components and validation
- **[TABLES.md](TABLES.md)**: Table configuration and features
- **[TENANCY.md](TENANCY.md)**: Multi-tenancy setup and tenant management
- **[ACTIONS.md](ACTIONS.md)**: Action configuration and customization
- **[NOTIFICATIONS.md](NOTIFICATIONS.md)**: Notification system
- **[WIDGETS.md](WIDGETS.md)**: Widget configuration and custom widgets
- **[CODE_QUALITY.md](CODE_QUALITY.md)**: Best practices and organization patterns

---

**Last Updated**: January 18, 2026  
**FilamentPHP Version**: 4.x  
**Status**: Complete ✅
