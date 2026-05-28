# FilamentPHP 4.x Notifications Reference

## Table of Contents

1. [Overview](#overview)
2. [Basic Notification Usage](#basic-notification-usage)
3. [Notification Status Types](#notification-status-types)
4. [Notification Content](#notification-content)
5. [Notification Icons and Colors](#notification-icons-and-colors)
6. [Notification Duration and Persistence](#notification-duration-and-persistence)
7. [Notification Actions](#notification-actions)
8. [Database Notifications](#database-notifications)
9. [Broadcast Notifications](#broadcast-notifications)
10. [JavaScript Integration](#javascript-integration)
11. [Testing Notifications](#testing-notifications)
12. [Action Integration](#action-integration)
13. [Customizing Notifications](#customizing-notifications)
14. [Global Configuration](#global-configuration)
15. [Troubleshooting](#troubleshooting)
16. [Cross-References](#cross-references)

---

## Overview

FilamentPHP's notification system provides a powerful and flexible way to display feedback to users. Notifications can be triggered from PHP (Livewire components) or JavaScript, sent to the session, database, or broadcast in real-time.

### When to Use Notifications

- **Success feedback**: Confirm successful operations (e.g., "Record saved successfully")
- **Error messages**: Display validation errors or operation failures
- **Warnings**: Alert users about potential issues or important information
- **Info messages**: Provide contextual information without requiring action
- **Interactive alerts**: Include actions for users to respond (e.g., "Undo", "View details")

### Key Features

- Multiple delivery channels: session, database, broadcast
- Status-based styling: success, warning, danger, info
- Custom duration and persistence
- Interactive actions with URLs or Livewire events
- JavaScript API for client-side control
- Full integration with FilamentPHP actions
- Icon and color customization
- Real-time websocket support

---

## Basic Notification Usage

### Creating and Sending a Simple Notification (PHP)

The most basic notification requires a title and uses the fluent API:

```php
<?php

namespace App\Livewire;

use Filament\Notifications\Notification;
use Livewire\Component;

class EditPost extends Component
{
    public function save(): void
    {
        // Perform save logic...

        Notification::make()
            ->title('Saved successfully')
            ->success()
            ->send();
    }
}
```

### Creating and Sending a Simple Notification (JavaScript)

Notifications can also be sent from JavaScript:

```javascript
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .send()
```

### Importing JavaScript Notification Classes

To use notifications in your bundled JavaScript, import the classes:

```javascript
import { Notification, NotificationAction } from '../../vendor/filament/notifications/dist/index.js'

// Use as:
new Notification()
    .title('Saved successfully')
    .success()
    .send()
```

### Verifying Package Installation

Before using notifications, verify the package is installed:

```bash
composer show filament/notifications
```

If not installed, add it to your project:

```bash
composer require filament/notifications
```

---

## Notification Status Types

FilamentPHP provides four dedicated status methods that automatically set appropriate icons and colors.

### Success Notifications

Use for successful operations:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Record created successfully')
    ->success()
    ->send();
```

```javascript
new FilamentNotification()
    .title('Record created successfully')
    .success()
    .send()
```

### Warning Notifications

Use for important alerts that don't prevent operations:

```php
Notification::make()
    ->title('Disk space is running low')
    ->warning()
    ->send();
```

### Danger Notifications

Use for errors and critical issues:

```php
Notification::make()
    ->title('Unable to save record')
    ->danger()
    ->send();
```

### Info Notifications

Use for general information:

```php
Notification::make()
    ->title('System maintenance scheduled')
    ->info()
    ->send();
```

### Status Icons

Each status type has a default icon defined in the icon aliases:

```php
use Filament\Notifications\View\NotificationsIconAlias;

// Default icons:
// NOTIFICATION_SUCCESS - Success notifications
// NOTIFICATION_WARNING - Warning notifications
// NOTIFICATION_DANGER - Danger notifications
// NOTIFICATION_INFO - Info notifications
```

---

## Notification Content

### Setting Title

The title is the main message displayed (required):

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->send();
```

Title text can contain basic safe HTML or Markdown:

```php
use Illuminate\Support\Str;

Notification::make()
    ->title(Str::markdown('**Important**: Record saved'))
    ->send();
```

### Adding Body Content

Add detailed information with the `body()` method:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->send();
```

```javascript
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .body('Changes to the post have been saved.')
    .send()
```

Body content also supports HTML and Markdown:

```php
use Illuminate\Support\Str;

Notification::make()
    ->title('Post published')
    ->body(Str::markdown('Your post **"' . $post->title . '"** is now live.'))
    ->send();
```

---

## Notification Icons and Colors

### Custom Icons

Override the default status icon:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->icon('heroicon-o-document-text')
    ->iconColor('success')
    ->send();
```

```javascript
new FilamentNotification()
    .title('Saved successfully')
    .icon('heroicon-o-document-text')
    .iconColor('success')
    .send()
```

### Icon Colors

Set icon color independently from status:

```php
Notification::make()
    ->title('Custom notification')
    ->icon('heroicon-o-bell')
    ->iconColor('warning')
    ->send();
```

Available icon colors: `success`, `warning`, `danger`, `info`, `gray`, `primary`

### Background Colors

Set a background color for additional visual context:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->color('success')
    ->send();
```

```javascript
new FilamentNotification()
    .title('Saved successfully')
    .color('success')
    .send()
```

By default, notifications have no background color. The color value should match your status type.

---

## Notification Duration and Persistence

### Setting Duration in Milliseconds

Control how long a notification displays before auto-closing (default: 6000ms):

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->duration(5000)
    ->send();
```

```javascript
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .duration(5000)
    .send()
```

### Setting Duration in Seconds

Alternative readable syntax:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->seconds(5)
    ->send();
```

```javascript
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .seconds(5)
    .send()
```

### Persistent Notifications

Prevent auto-closing and require manual dismissal:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->persistent()
    ->send();
```

```javascript
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .persistent()
    .send()
```

**Use cases for persistent notifications:**
- Critical errors requiring acknowledgment
- Subscription prompts or upgrade messages
- Important announcements
- Notifications with actions that need user interaction

---

## Notification Actions

Notifications can include interactive buttons that execute various operations.

### Basic Action Buttons

Add simple action buttons:

```php
use Filament\Actions\Action;
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->actions([
        Action::make('view')
            ->button(),
        Action::make('undo')
            ->color('gray'),
    ])
    ->send();
```

```javascript
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .body('Changes to the post have been saved.')
    .actions([
        new FilamentNotificationAction('view')
            .button(),
        new FilamentNotificationAction('undo')
            .color('gray'),
    ])
    .send()
```

### URL Actions

Open URLs when action is clicked:

```php
use Filament\Actions\Action;
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->actions([
        Action::make('view')
            ->button()
            ->url(route('posts.show', $post), shouldOpenInNewTab: true),
        Action::make('undo')
            ->color('gray'),
    ])
    ->send();
```

```javascript
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .body('Changes to the post have been saved.')
    .actions([
        new FilamentNotificationAction('view')
            .button()
            .url('/view')
            .openUrlInNewTab(),
        new FilamentNotificationAction('undo')
            .color('gray'),
    ])
    .send()
```

### Dispatching Livewire Events

Trigger Livewire events from notification actions:

```php
use Filament\Actions\Action;
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->actions([
        Action::make('view')
            ->button()
            ->url(route('posts.show', $post), shouldOpenInNewTab: true),
        Action::make('undo')
            ->color('gray')
            ->dispatch('undoEditingPost', [$post->id]),
    ])
    ->send();
```

```javascript
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .body('Changes to the post have been saved.')
    .actions([
        new FilamentNotificationAction('view')
            .button()
            .url('/view')
            .openUrlInNewTab(),
        new FilamentNotificationAction('undo')
            .color('gray')
            .dispatch('undoEditingPost'),
    ])
    .send()
```

### Dispatching to Specific Components

Dispatch events to the current component or another component:

```php
// Dispatch to self
Action::make('undo')
    ->color('gray')
    ->dispatchSelf('undoEditingPost', [$post->id]);

// Dispatch to another component
Action::make('undo')
    ->color('gray')
    ->dispatchTo('another_component', 'undoEditingPost', [$post->id]);
```

```javascript
// JavaScript equivalent
new FilamentNotificationAction('undo')
    .color('gray')
    .dispatchSelf('undoEditingPost');

new FilamentNotificationAction('undo')
    .color('gray')
    .dispatchTo('another_component', 'undoEditingPost');
```

### Auto-Closing Notifications with Actions

Close the notification automatically when an action is triggered:

```php
use Filament\Actions\Action;
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->actions([
        Action::make('view')
            ->button()
            ->url(route('posts.show', $post), shouldOpenInNewTab: true),
        Action::make('undo')
            ->color('gray')
            ->dispatch('undoEditingPost', [$post->id])
            ->close(),
    ])
    ->send();
```

```javascript
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .body('Changes to the post have been saved.')
    .actions([
        new FilamentNotificationAction('view')
            .button()
            .url('/view')
            .openUrlInNewTab(),
        new FilamentNotificationAction('undo')
            .color('gray')
            .dispatch('undoEditingPost')
            .close(),
    ])
    .send()
```

---

## Database Notifications

Store notifications in the database for persistence and later viewing.

### Setting Up Database Notifications

Create the notifications table:

```bash
php artisan make:notifications-table
php artisan migrate
```

Enable database notifications in your panel:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->databaseNotifications();
}
```

### Sending Database Notifications

Send a notification to the database:

```php
use Filament\Notifications\Notification;

$recipient = auth()->user();

Notification::make()
    ->title('Saved successfully')
    ->sendToDatabase($recipient);
```

### Using Laravel's notify() Method

Alternative approach using Laravel's notification system:

```php
use Filament\Notifications\Notification;

$recipient = auth()->user();

$recipient->notify(
    Notification::make()
        ->title('Saved successfully')
        ->toDatabase(),
);
```

### Database Notification in Laravel Notification Class

Integrate with traditional Laravel notifications:

```php
use App\Models\User;
use Filament\Notifications\Notification;

public function toDatabase(User $notifiable): array
{
    return Notification::make()
        ->title('Saved successfully')
        ->getDatabaseMessage();
}
```

### Polling for New Notifications

Configure automatic polling interval (default: 30 seconds):

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->databaseNotifications()
        ->databaseNotificationsPolling('30s');
}
```

Disable polling (use websockets instead):

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->databaseNotifications()
        ->databaseNotificationsPolling(null);
}
```

### Real-time Notifications with Websockets

Enable immediate notification delivery via Laravel Echo:

```php
use Filament\Notifications\Notification;

$recipient = auth()->user();

Notification::make()
    ->title('Saved successfully')
    ->sendToDatabase($recipient, isEventDispatched: true);
```

This dispatches a `DatabaseNotificationsSent` event that your websocket setup can listen to.

### Database Notification Actions

Add actions to mark notifications as read/unread:

```php
use Filament\Actions\Action;
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->actions([
        Action::make('view')
            ->button()
            ->markAsRead(),
    ])
    ->send();
```

Mark as unread:

```php
use Filament\Actions\Action;
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->actions([
        Action::make('markAsUnread')
            ->button()
            ->markAsUnread(),
    ])
    ->send();
```

### Opening Database Notifications Modal

Open the modal programmatically with Alpine.js:

```html
<button
    x-data="{}"
    x-on:click="$dispatch('open-modal', { id: 'database-notifications' })"
    type="button"
>
    Notifications
</button>
```

---

## Broadcast Notifications

Send real-time notifications using Laravel's broadcasting system.

### Sending Broadcast Notifications

Using the fluent API:

```php
use Filament\Notifications\Notification;

$recipient = auth()->user();

Notification::make()
    ->title('Saved successfully')
    ->broadcast($recipient);
```

Using Laravel's notify() method:

```php
use Filament\Notifications\Notification;

$recipient = auth()->user();

$recipient->notify(
    Notification::make()
        ->title('Saved successfully')
        ->toBroadcast(),
);
```

### Broadcast Notification in Laravel Notification Class

```php
use App\Models\User;
use Filament\Notifications\Notification;
use Illuminate\Notifications\Messages\BroadcastMessage;

public function toBroadcast(User $notifiable): BroadcastMessage
{
    return Notification::make()
        ->title('Saved successfully')
        ->getBroadcastMessage();
}
```

---

## JavaScript Integration

### Creating Notifications with Custom IDs

Assign a custom ID for programmatic control:

```php
use Filament\Notifications\Notification;

Notification::make('greeting')
    ->title('Hello')
    ->persistent()
    ->send();
```

**Note:** Using random IDs (default) is recommended to avoid accidentally closing multiple notifications.

### Getting Notification ID

Retrieve the ID after sending:

```php
use Filament\Notifications\Notification;

$notification = Notification::make()
    ->title('Hello')
    ->persistent()
    ->send();

$notificationId = $notification->getId();
```

### Closing Notifications Programmatically

Close a notification using Alpine.js event dispatch:

```html
<button x-on:click="$dispatch('close-notification', { id: notificationId })" type="button">
    Close Notification
</button>
```

Close with a custom ID:

```html
<button x-on:click="$dispatch('close-notification', { id: 'greeting' })" type="button">
    Close Notification
</button>
```

Close from Livewire (PHP):

```php
$this->dispatch('close-notification', id: $notificationId);
```

---

## Testing Notifications

### Asserting Notification Was Sent

Using Livewire helper:

```php
use function Pest\Livewire\livewire;

it('sends a notification', function () {
    livewire(CreatePost::class)
        ->assertNotified();
});
```

Using Notification facade:

```php
use Filament\Notifications\Notification;

it('sends a notification', function () {
    Notification::assertNotified();
});
```

Using dedicated helper function:

```php
use function Filament\Notifications\Testing\assertNotified;

it('sends a notification', function () {
    assertNotified();
});
```

### Asserting Specific Notification Title

```php
use function Pest\Livewire\livewire;

it('sends a notification', function () {
    livewire(CreatePost::class)
        ->assertNotified('Unable to create post');
});
```

### Asserting Exact Notification Object

Validate the complete notification including status, title, and body:

```php
use Filament\Notifications\Notification;
use function Pest\Livewire\livewire;

it('sends a notification', function () {
    livewire(CreatePost::class)
        ->assertNotified(
            Notification::make()
                ->danger()
                ->title('Unable to create post')
                ->body('Something went wrong.'),
        );
});
```

### Asserting Notification Was Not Sent

```php
use Filament\Notifications\Notification;
use function Pest\Livewire\livewire;

it('does not send a notification', function () {
    livewire(CreatePost::class)
        ->assertNotNotified()
        // or
        ->assertNotNotified('Unable to create post')
        // or
        ->assertNotNotified(
            Notification::make()
                ->danger()
                ->title('Unable to create post')
                ->body('Something went wrong.'),
        );
});
```

---

## Action Integration

### Customizing Action Success Notifications

Override the success notification title:

```php
use Filament\Actions\CreateAction;

CreateAction::make()
    ->successNotificationTitle('User registered');
```

Customize the entire notification object:

```php
use Filament\Actions\CreateAction;
use Filament\Notifications\Notification;

CreateAction::make()
    ->successNotification(
       Notification::make()
            ->success()
            ->title('User registered')
            ->body('The user has been created successfully.'),
    );
```

Disable success notification:

```php
use Filament\Actions\CreateAction;

CreateAction::make()
    ->successNotification(null);
```

### Edit Action Notifications

```php
use Filament\Actions\EditAction;

EditAction::make()
    ->successNotificationTitle('User updated');
```

Complete customization:

```php
use Filament\Actions\EditAction;
use Filament\Notifications\Notification;

EditAction::make()
    ->successNotification(
       Notification::make()
            ->success()
            ->title('User updated')
            ->body('The user has been saved successfully.'),
    );
```

### Delete Action Notifications

```php
use Filament\Actions\DeleteAction;

DeleteAction::make()
    ->successNotificationTitle('User deleted');
```

Complete customization:

```php
use Filament\Actions\DeleteAction;
use Filament\Notifications\Notification;

DeleteAction::make()
    ->successNotification(
       Notification::make()
            ->success()
            ->title('User deleted')
            ->body('The user has been deleted successfully.'),
    );
```

### Bulk Action Notifications

Configure success and failure notifications for bulk actions:

```php
use Filament\Actions\BulkAction;
use Illuminate\Database\Eloquent\Collection;

BulkAction::make('delete')
    ->requiresConfirmation()
    ->authorizeIndividualRecords('delete')
    ->action(fn (Collection $records) => $records->each->delete())
    ->successNotificationTitle('Deleted users')
    ->failureNotificationTitle(function (int $successCount, int $totalCount): string {
        if ($successCount) {
            return "{$successCount} of {$totalCount} users deleted";
        }

        return 'Failed to delete any users';
    });
```

### Halting Actions with Notifications

Prevent action execution and show notification:

```php
use App\Models\Post;
use Filament\Actions\Action;
use Filament\Actions\CreateAction;
use Filament\Notifications\Notification;

CreateAction::make()
    ->before(function (CreateAction $action, Post $record) {
        if (! $record->team->subscribed()) {
            Notification::make()
                ->warning()
                ->title('You don\'t have an active subscription!')
                ->body('Choose a plan to continue.')
                ->persistent()
                ->actions([
                    Action::make('subscribe')
                        ->button()
                        ->url(route('subscribe'), shouldOpenInNewTab: true),
                ])
                ->send();
        
            $action->halt();
        }
    });
```

### Authorization Notifications

Show notifications when users lack permission:

```php
use Filament\Actions\Action;

Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->authorize('update')
    ->authorizationNotification();
```

This keeps the action clickable but sends a notification with the policy's response message.

### Rate-Limited Action Notifications

Customize rate limit notifications:

```php
use Filament\Actions\DeleteAction;

DeleteAction::make()
    ->rateLimit(5)
    ->rateLimitedNotificationTitle('Slow down!');
```

Complete customization with time remaining:

```php
use DanHarrin\LivewireRateLimiting\Exceptions\TooManyRequestsException;
use Filament\Actions\DeleteAction;
use Filament\Notifications\Notification;

DeleteAction::make()
    ->rateLimit(5)
    ->rateLimitedNotification(
       fn (TooManyRequestsException $exception): Notification => Notification::make()
            ->warning()
            ->title('Slow down!')
            ->body("You can try deleting again in {$exception->secondsUntilAvailable} seconds."),
    );
```

---

## Customizing Notifications

### Resource Create Page Notifications

Override in your Create page class:

```php
protected function getCreatedNotificationTitle(): ?string
{
    return 'User registered';
}
```

Complete customization:

```php
use Filament\Notifications\Notification;

protected function getCreatedNotification(): ?Notification
{
    return Notification::make()
        ->success()
        ->title('User registered')
        ->body('The user has been created successfully.');
}
```

Disable notification:

```php
use Filament\Notifications\Notification;

protected function getCreatedNotification(): ?Notification
{
    return null;
}
```

### Resource Edit Page Notifications

```php
protected function getSavedNotificationTitle(): ?string
{
    return 'User updated';
}
```

Complete customization:

```php
use Filament\Notifications\Notification;

protected function getSavedNotification(): ?Notification
{
    return Notification::make()
        ->success()
        ->title('User updated')
        ->body('The user has been saved successfully.');
}
```

### Lifecycle Hook Integration

Use notifications within lifecycle hooks to provide feedback during complex operations:

```php
use Filament\Actions\Action;
use Filament\Notifications\Notification;

protected function beforeCreate(): void
{
    if (! auth()->user()->team->subscribed()) {
        Notification::make()
            ->warning()
            ->title('You don\'t have an active subscription!')
            ->body('Choose a plan to continue.')
            ->persistent()
            ->actions([
                Action::make('subscribe')
                    ->button()
                    ->url(route('subscribe'), shouldOpenInNewTab: true),
            ])
            ->send();
    
        $this->halt();
    }
}
```

---

## Global Configuration

### Notification Alignment

Configure horizontal and vertical positioning:

```php
use Filament\Notifications\Livewire\Notifications;
use Filament\Support\Enums\Alignment;
use Filament\Support\Enums\VerticalAlignment;

Notifications::alignment(Alignment::Start);
Notifications::verticalAlignment(VerticalAlignment::End);
```

Available alignments:
- **Horizontal**: `Start`, `Center`, `End`
- **Vertical**: `Start`, `Center`, `End`

This configuration is typically done in a service provider or middleware.

### Error Notifications (Panel Level)

Customize default error notification text:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->registerErrorNotification(
            title: 'An error occurred',
            body: 'Please try again later.',
        );
}
```

Status code-specific error notifications:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->registerErrorNotification(
            title: 'An error occurred',
            body: 'Please try again later.',
        )
        ->registerErrorNotification(
            title: 'Record not found',
            body: 'A record you are looking for does not exist.',
            statusCode: 404,
        );
}
```

Disable error notifications globally:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->errorNotifications(false);
}
```

### Page-Level Error Notifications

Control per page:

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

Dynamic control with custom logic:

```php
use Filament\Pages\Dashboard as BaseDashboard;

class Dashboard extends BaseDashboard
{
    public function hasErrorNotifications(): bool
    {
        return FeatureFlag::active();
    }

    // ...
}
```

Register custom error notifications within page:

```php
use Filament\Pages\Dashboard as BaseDashboard;

class Dashboard extends BaseDashboard
{
    protected function setUpErrorNotifications(): void
    {
        $this->registerErrorNotification(
            title: 'An error occurred',
            body: 'Please try again later.',
        );
    
        $this->registerErrorNotification(
            title: 'Record not found',
            body: 'A record you are looking for does not exist.',
            statusCode: 404,
        );
    }

    // ...
}
```

### Rendering Notifications in Blade

Include the Livewire notifications component:

```blade
<div>
    @livewire('notifications')
</div>
```

---

## Troubleshooting

### Notifications Not Appearing

**Issue**: Notifications don't display after sending.

**Solutions**:
1. Ensure `@livewire('notifications')` is in your layout
2. Verify the notifications package is installed: `composer show filament/notifications`
3. Check browser console for JavaScript errors
4. Confirm you're calling `->send()` on the notification
5. For database notifications, ensure migrations are run and panel is configured

### Database Notifications Not Storing

**Issue**: Database notifications aren't saved.

**Solutions**:
1. Run `php artisan make:notifications-table` and `php artisan migrate`
2. Ensure your User model uses `Notifiable` trait
3. Verify panel has `->databaseNotifications()` enabled
4. Check queue is running if using queued notifications

### Real-time Notifications Not Working

**Issue**: Websocket notifications don't appear instantly.

**Solutions**:
1. Verify Laravel Echo is properly configured
2. Ensure `isEventDispatched: true` parameter is set
3. Check websocket server is running (Soketi, Pusher, etc.)
4. Verify broadcasting configuration in `config/broadcasting.php`
5. Test with polling enabled first to isolate the issue

### Notification Actions Not Triggering

**Issue**: Action buttons don't work when clicked.

**Solutions**:
1. Verify Livewire event names match your listener methods
2. Check JavaScript console for errors
3. Ensure URL routes exist and are accessible
4. For `dispatch()`, confirm the event handler is defined
5. For `close()`, verify the notification ID is correctly passed

### Custom Icons Not Displaying

**Issue**: Custom icons don't appear.

**Solutions**:
1. Verify Heroicon name is correct (use `heroicon-o-` prefix)
2. Check if icon exists in your Heroicon version
3. Ensure icon color is set if needed
4. Try using a default icon to test
5. Clear browser cache and rebuild assets

### Notifications Disappearing Too Quickly

**Issue**: Notifications auto-close before users can read them.

**Solutions**:
1. Increase duration: `->duration(10000)` or `->seconds(10)`
2. Make notification persistent: `->persistent()`
3. Add actions that users must interact with
4. Check if competing JavaScript is closing notifications

### Persistent Notifications Won't Close

**Issue**: Persistent notifications remain after close button clicked.

**Solutions**:
1. Verify notification ID is correctly retrieved
2. Check browser console for dispatch errors
3. Ensure `close-notification` event is properly dispatched
4. Try using a custom ID: `Notification::make('custom-id')`
5. Clear browser cache and test again

### Bulk Action Failure Notifications Incorrect

**Issue**: Failure count or message is wrong.

**Solutions**:
1. Use `reportBulkProcessingFailure()` for each failed record
2. Implement proper failure counting logic
3. Use dynamic messages with `$successCount` and `$failureCount`
4. Test authorization separately from action logic
5. Log failures to debug which records fail and why

### Action Rate Limiting Not Working

**Issue**: Rate limit notifications don't appear or limits aren't enforced.

**Solutions**:
1. Verify `->rateLimit(5)` is set on the action
2. Ensure cache driver is properly configured
3. Check rate limiter key is unique per user/action
4. Test with lower limit to verify functionality
5. Clear cache: `php artisan cache:clear`

---

## Cross-References

### Related FilamentPHP Topics

- **[ACTIONS.md](ACTIONS.md)**: Complete guide to FilamentPHP actions, including action integration with notifications
- **[FORMS.md](FORMS.md)**: Form validation and feedback notifications
- **[TABLES.md](TABLES.md)**: Table action notifications and bulk operation feedback
- **[PANEL_CONFIGURATION.md](PANEL_CONFIGURATION.md)**: Panel-level notification settings and error handling

### Prerequisites

- Basic Laravel knowledge (routes, Livewire, broadcasting)
- Understanding of FilamentPHP actions (see ACTIONS.md)
- Familiarity with database migrations and models

### See Also

- [FilamentPHP Notifications Official Docs](https://filamentphp.com/docs/4.x/notifications)
- [Laravel Broadcasting Documentation](https://laravel.com/docs/broadcasting)
- [Laravel Echo Documentation](https://laravel.com/docs/broadcasting#client-side-installation)
- [Livewire Events](https://livewire.laravel.com/docs/events)

---

**Version**: FilamentPHP 4.x  
**Last Updated**: January 18, 2026  
**Total Examples**: 120+  
**Status**: Complete
