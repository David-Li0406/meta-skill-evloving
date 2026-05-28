# Dusk Browser Testing

## Setup

```bash
composer require laravel/dusk --dev
php artisan dusk:install
```

## Basic Browser Test

```php
<?php

namespace Tests\Browser;

use App\Models\User;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class LoginTest extends DuskTestCase
{
    /**
     * Test successful login flow.
     */
    public function test_user_can_login(): void
    {
        $user = User::factory()->create();

        $this->browse(function (Browser $browser) use ($user) {
            $browser
                ->visit('/login')
                ->type('email', $user->email)
                ->type('password', 'password')
                ->press('Login')
                ->assertPathIs('/dashboard')
                ->assertSee('Welcome');
        });
    }
}
```

## Element Selectors

```php
$browser
    // By ID
    ->type('#email', 'test@example.com')
    
    // By name attribute
    ->type('email', 'test@example.com')
    
    // By CSS selector
    ->click('.btn-primary')
    
    // By Dusk selector (recommended)
    ->click('@submit-button');  // Uses dusk="submit-button" attribute
```

```blade
{{-- In your Blade template --}}
<button dusk="submit-button">Submit</button>
```

## Assertions

```php
$browser
    // URL
    ->assertPathIs('/dashboard')
    ->assertPathBeginsWith('/admin')
    ->assertQueryStringHas('page', '1')
    
    // Content
    ->assertSee('Welcome')
    ->assertDontSee('Error')
    ->assertSeeIn('.alert', 'Success')
    
    // Elements
    ->assertPresent('#modal')
    ->assertMissing('.error-message')
    ->assertVisible('.dropdown-menu')
    ->assertEnabled('@submit-button')
    ->assertDisabled('@submit-button')
    
    // Form values
    ->assertInputValue('email', 'test@example.com')
    ->assertChecked('remember')
    ->assertNotChecked('terms')
    ->assertSelected('country', 'TR');
```

## Waiting

```php
$browser
    // Wait for element
    ->waitFor('.loaded-content')
    ->waitFor('.modal', 10)  // 10 seconds max
    
    // Wait until missing
    ->waitUntilMissing('.loading-spinner')
    
    // Wait for text
    ->waitForText('Success')
    
    // Wait for JavaScript
    ->waitUntil('window.loaded === true')
    
    // Wait for reload
    ->waitForReload()
    
    // Pause (debugging only)
    ->pause(1000);  // 1 second
```

## Form Interactions

```php
$browser
    // Type
    ->type('email', 'test@example.com')
    ->clear('email')
    ->append('email', '.uk')
    
    // Select
    ->select('country', 'TR')
    ->select('tags', ['php', 'laravel'])  // Multiple
    
    // Checkbox/Radio
    ->check('remember')
    ->uncheck('newsletter')
    ->radio('plan', 'premium')
    
    // File upload
    ->attach('avatar', __DIR__.'/fixtures/avatar.jpg')
    
    // Buttons
    ->press('Submit')
    ->click('@cancel-button');
```

## Screenshots

```php
public function test_dashboard_layout(): void
{
    $this->browse(function (Browser $browser) {
        $browser
            ->loginAs(User::factory()->create())
            ->visit('/dashboard')
            ->screenshot('dashboard-layout')  // Saved to tests/Browser/screenshots/
            ->assertSee('Dashboard');
    });
}

// On failure, screenshots are automatically saved
```

## Multiple Browsers

```php
public function test_real_time_chat(): void
{
    $userA = User::factory()->create();
    $userB = User::factory()->create();

    $this->browse(function (Browser $browserA, Browser $browserB) use ($userA, $userB) {
        $browserA
            ->loginAs($userA)
            ->visit('/chat');

        $browserB
            ->loginAs($userB)
            ->visit('/chat')
            ->type('message', 'Hello!')
            ->press('Send');

        $browserA
            ->waitForText('Hello!')
            ->assertSee('Hello!');
    });
}
```

## Authentication

```php
$browser
    // Login as existing user
    ->loginAs(User::find(1))
    ->loginAs($user)
    
    // Logout
    ->logout();
```

## Running Dusk Tests

```bash
# Run all Dusk tests
php artisan dusk

# Specific file
php artisan dusk tests/Browser/LoginTest.php

# Filter by name
php artisan dusk --filter=test_user_can_login

# With specific environment
php artisan dusk --env=dusk.local
```
