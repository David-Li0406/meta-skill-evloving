---
name: filamentphp-testing
description: Expert knowledge for testing FilamentPHP 4.x resources, tables, schemas, actions, and notifications using Pest and Livewire. Use this skill when writing or debugging tests for FilamentPHP components, implementing test coverage for admin panels, or ensuring FilamentPHP features work correctly.
compatibility: Designed for FilamentPHP 4.x with Pest testing framework and Livewire
metadata:
  author: AI Assistant
  version: "1.0.0"
  framework: FilamentPHP 4.x
  testing-framework: Pest
---

# FilamentPHP Testing Skill

This skill provides comprehensive guidance for testing FilamentPHP 4.x applications using Pest and Livewire testing utilities.

## When to Use This Skill

- Writing tests for FilamentPHP resources (Create, Edit, View, List pages)
- Testing FilamentPHP tables (columns, filters, sorting, searching, bulk actions)
- Testing FilamentPHP schemas (forms, infolists, wizards)
- Testing FilamentPHP actions (page actions, table actions, schema actions)
- Testing FilamentPHP notifications
- Implementing test coverage for FilamentPHP relation managers
- Debugging failing FilamentPHP tests

## Core Testing Patterns

### Testing Resources

#### Test Resource List Page
```php
use App\Filament\Resources\Users\Pages\ListUsers;
use App\Models\User;
use function Pest\Livewire\livewire;

it('can load the page', function () {
    $users = User::factory()->count(5)->create();

    livewire(ListUsers::class)
        ->assertOk()
        ->assertCanSeeTableRecords($users);
});
```

#### Test Resource Create Page
```php
use App\Filament\Resources\Users\Pages\CreateUser;
use App\Models\User;
use function Pest\Laravel\assertDatabaseHas;
use function Pest\Livewire\livewire;

it('can create a user', function () {
    $newUserData = User::factory()->make();

    livewire(CreateUser::class)
        ->fillForm([
            'name' => $newUserData->name,
            'email' => $newUserData->email,
        ])
        ->call('create')
        ->assertNotified()
        ->assertRedirect();

    assertDatabaseHas(User::class, [
        'name' => $newUserData->name,
        'email' => $newUserData->email,
    ]);
});
```

#### Test Resource Edit Page
```php
use App\Filament\Resources\Users\Pages\EditUser;
use App\Models\User;
use function Pest\Laravel\assertDatabaseHas;
use function Pest\Livewire\livewire;

it('can load the page', function () {
    $user = User::factory()->create();

    livewire(EditUser::class, [
        'record' => $user->id,
    ])
        ->assertOk()
        ->assertSchemaStateSet([
            'name' => $user->name,
            'email' => $user->email,
        ]);
});

it('can update a user', function () {
    $user = User::factory()->create();
    $newUserData = User::factory()->make();

    livewire(EditUser::class, [
        'record' => $user->id,
    ])
        ->fillForm([
            'name' => $newUserData->name,
            'email' => $newUserData->email,
        ])
        ->call('save')
        ->assertNotified();

    assertDatabaseHas(User::class, [
        'id' => $user->id,
        'name' => $newUserData->name,
        'email' => $newUserData->email,
    ]);
});
```

#### Test Resource View Page
```php
use App\Filament\Resources\Users\Pages\ViewUser;
use App\Models\User;
use function Pest\Livewire\livewire;

it('can load the page', function () {
    $user = User::factory()->create();

    livewire(ViewUser::class, [
        'record' => $user->id,
    ])
        ->assertOk()
        ->assertSchemaStateSet([
            'name' => $user->name,
            'email' => $user->email,
        ]);
});
```

### Testing Tables

#### Test Table Rendering
```php
use function Pest\Livewire\livewire;

it('can render page', function () {
    livewire(ListPosts::class)
        ->assertSuccessful();
});
```

#### Test Table Records Visibility
```php
use function Pest\Livewire\livewire;

it('cannot display trashed posts by default', function () {
    $posts = Post::factory()->count(4)->create();
    $trashedPosts = Post::factory()->trashed()->count(6)->create();

    livewire(PostResource\Pages\ListPosts::class)
        ->assertCanSeeTableRecords($posts)
        ->assertCanNotSeeTableRecords($trashedPosts)
        ->assertCountTableRecords(4);
});
```

#### Test Table Search
```php
use function Pest\Livewire\livewire;

it('can search posts by title', function () {
    $posts = Post::factory()->count(10)->create();
    $title = $posts->first()->title;

    livewire(PostResource\Pages\ListPosts::class)
        ->searchTable($title)
        ->assertCanSeeTableRecords($posts->where('title', $title))
        ->assertCanNotSeeTableRecords($posts->where('title', '!=', $title));
});
```

#### Test Table Filtering
```php
use function Pest\Livewire\livewire;

it('can filter users by locale', function () {
    $users = User::factory()->count(5)->create();

    livewire(ListUsers::class)
        ->assertCanSeeTableRecords($users)
        ->filterTable('locale', $users->first()->locale)
        ->assertCanSeeTableRecords($users->where('locale', $users->first()->locale))
        ->assertCanNotSeeTableRecords($users->where('locale', '!=', $users->first()->locale));
});
```

#### Test Table Sorting
```php
use function Pest\Livewire\livewire;

it('can sort users by name', function () {
    $users = User::factory()->count(5)->create();

    livewire(ListUsers::class)
        ->assertCanSeeTableRecords($users)
        ->sortTable('name')
        ->assertCanSeeTableRecords($users->sortBy('name'), inOrder: true)
        ->sortTable('name', 'desc')
        ->assertCanSeeTableRecords($users->sortByDesc('name'), inOrder: true);
});
```

#### Test Table Column Visibility
```php
use function Pest\Livewire\livewire;

it('shows the correct columns', function () {
    livewire(PostResource\Pages\ListPosts::class)
        ->assertTableColumnVisible('created_at')
        ->assertTableColumnHidden('author');
});
```

#### Test Toggle All Columns
```php
use function Pest\Livewire\livewire;

it('can toggle all columns', function () {
    livewire(PostResource\Pages\ListPosts::class)
        ->toggleAllTableColumns();
});
```

### Testing Actions

#### Test Basic Page Actions
```php
use function Pest\Livewire\livewire;

it('can send invoices', function () {
    $invoice = Invoice::factory()->create();

    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->callAction('send');

    expect($invoice->refresh())
        ->isSent()->toBeTrue();
});
```

#### Test Table Row Actions
```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

it('can send invoice', function () {
    $invoice = Invoice::factory()->create();

    livewire(ListInvoices::class)
        ->callAction(TestAction::make('send')->table($invoice));
});
```

#### Test Table Header Actions
```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

it('can create invoice', function () {
    livewire(ListInvoices::class)
        ->callAction(TestAction::make('create')->table());
});
```

#### Test Table Bulk Actions
```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;
use function Pest\Laravel\assertDatabaseMissing;

it('can bulk delete users', function () {
    $users = User::factory()->count(5)->create();

    livewire(ListUsers::class)
        ->assertCanSeeTableRecords($users)
        ->selectTableRecords($users)
        ->callAction(TestAction::make(DeleteBulkAction::class)->table()->bulk())
        ->assertNotified()
        ->assertCanNotSeeTableRecords($users);

    $users->each(fn (User $user) => assertDatabaseMissing($user));
});
```

#### Test Schema Component Actions
```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

it('can send from schema component', function () {
    $invoice = Invoice::factory()->create();

    livewire(EditInvoice::class)
        ->callAction(TestAction::make('send')->schemaComponent('customer_id'));
});
```

#### Test Nested Actions
```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

it('can access nested action', function () {
    $invoice = Invoice::factory()->create();

    livewire(ManageInvoices::class)
        ->callAction([
            TestAction::make('view')->table($invoice),
            TestAction::make('send')->schemaComponent('customer.name'),
        ]);
});
```

#### Test Prebuilt Action Classes
```php
use Filament\Actions\CreateAction;
use Filament\Actions\DeleteAction;
use Filament\Actions\EditAction;
use function Pest\Livewire\livewire;
use function Pest\Laravel\assertDatabaseMissing;

it('can delete a user', function () {
    $user = User::factory()->create();

    livewire(EditUser::class, [
        'record' => $user->id,
    ])
        ->callAction(DeleteAction::class)
        ->assertNotified()
        ->assertRedirect();

    assertDatabaseMissing($user);
});
```

#### Test Action Visibility and Existence
```php
use function Pest\Livewire\livewire;

it('can only print invoices', function () {
    $invoice = Invoice::factory()->create();

    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionHidden('send')
        ->assertActionVisible('print')
        ->assertActionExists('print')
        ->assertActionDoesNotExist('unsend');
});
```

#### Test Action Enabled/Disabled State
```php
use function Pest\Livewire\livewire;

it('can only print a sent invoice', function () {
    $invoice = Invoice::factory()->create();

    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionDisabled('send')
        ->assertActionEnabled('print');
});
```

#### Test Action Halted State
```php
use function Pest\Livewire\livewire;

it('stops sending if invoice has no email address', function () {
    $invoice = Invoice::factory(['email' => null])->create();

    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->callAction('send')
        ->assertActionHalted('send');
});
```

#### Test Action Modal Content
```php
use function Pest\Livewire\livewire;

it('confirms the target address before sending', function () {
    $invoice = Invoice::factory()->create();
    $recipientEmail = $invoice->company->primaryContact->email;

    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->mountAction('send')
        ->assertMountedActionModalSee($recipientEmail);
});
```

#### Test Action Pre-filled State
```php
use function Pest\Livewire\livewire;

it('can send invoices to the primary contact by default', function () {
    $invoice = Invoice::factory()->create();
    $recipientEmail = $invoice->company->primaryContact->email;

    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->mountAction('send')
        ->assertSchemaStateSet([
            'email' => $recipientEmail,
        ])
        ->callMountedAction()
        ->assertHasNoFormErrors();

    expect($invoice->refresh())
        ->isSent()->toBeTrue()
        ->recipient_email->toBe($recipientEmail);
});
```

#### Test Action Configuration with Callback
```php
use Filament\Actions\Action;
use function Pest\Livewire\livewire;

it('has the correct description', function () {
    $invoice = Invoice::factory()->create();

    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionExists('send', function (Action $action): bool {
            return $action->getModalDescription() === 'This will send an email...';
        });
});
```

#### Test Action URLs
```php
use function Pest\Livewire\livewire;

it('links to the correct sites', function () {
    $invoice = Invoice::factory()->create();

    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionHasUrl('filament', 'https://filamentphp.com/')
        ->assertActionDoesNotHaveUrl('filament', 'https://github.com/filamentphp/filament')
        ->assertActionShouldOpenUrlInNewTab('filament')
        ->assertActionShouldNotOpenUrlInNewTab('github');
});
```

### Testing Schemas (Forms & Infolists)

#### Test Form Exists
```php
use function Pest\Livewire\livewire;

it('has a form', function () {
    livewire(CreatePost::class)
        ->assertFormExists();
});
```

#### Test Form Field Visibility
```php
use function Pest\Livewire\livewire;

it('has title field', function () {
    livewire(CreatePost::class)
        ->assertSchemaComponentExists('title');
});

it('does not have conditional component', function () {
    livewire(CreatePost::class)
        ->assertSchemaComponentDoesNotExist('no-such-section');
});
```

#### Test Form Field State
```php
use function Pest\Livewire\livewire;

it('has correct enabled/disabled state', function () {
    livewire(CreatePost::class)
        ->assertFormFieldEnabled('title')
        ->assertFormFieldDisabled('slug');
});
```

#### Test Schema State
```php
use Illuminate\Support\Str;
use function Pest\Livewire\livewire;

it('can automatically generate a slug from the title', function () {
    $title = fake()->sentence();

    livewire(CreatePost::class)
        ->fillForm([
            'title' => $title,
        ])
        ->assertSchemaStateSet([
            'slug' => Str::slug($title),
        ]);
});
```

#### Test Schema State with Callback
```php
use Illuminate\Support\Str;
use function Pest\Livewire\livewire;

it('can automatically generate a slug without spaces', function () {
    $title = fake()->sentence();

    livewire(CreatePost::class)
        ->fillForm([
            'title' => $title,
        ])
        ->assertSchemaStateSet(function (array $state): array {
            expect($state['slug'])
                ->not->toContain(' ');
                
            return [
                'slug' => Str::slug($title),
            ];
        });
});
```

#### Test Schema Component Properties
```php
use Filament\Schemas\Components\Section;
use Illuminate\Testing\Assert;
use function Pest\Livewire\livewire;

test('comments section has heading', function () {
    livewire(EditPost::class)
        ->assertSchemaComponentExists(
            'comments-section',
            checkComponentUsing: function (Section $component): bool {
                Assert::assertTrue(
                    $component->getHeading() === 'Comments',
                    'Failed asserting section has correct heading.',
                );
                
                return true;
            },
        );
});
```

#### Test Wizard Navigation
```php
use function Pest\Livewire\livewire;

it('moves to next wizard step', function () {
    livewire(CreatePost::class)
        ->goToNextWizardStep()
        ->assertHasFormErrors(['title']);
});
```

#### Test Repeater/Builder Item Count
```php
use Filament\Forms\Components\Repeater;
use function Pest\Livewire\livewire;

it('has correct number of items', function () {
    $post = Post::factory()->create();
    
    $undoRepeaterFake = Repeater::fake();

    livewire(EditPost::class, ['record' => $post])
        ->assertSchemaStateSet(function (array $state) {
            expect($state['quotes'])
                ->toHaveCount(2);
        });

    $undoRepeaterFake();
});
```

#### Test Repeater Actions
```php
use App\Models\Quote;
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

it('can send quote', function () {
    $post = Post::factory()->create();
    $quote = Quote::first();

    livewire(EditPost::class, ['record' => $post])
        ->callAction(TestAction::make('sendQuote')->schemaComponent('quotes')->arguments([
            'item' => "record-{$quote->getKey()}",
        ]))
        ->assertNotified('Quote sent!');
});
```

### Testing Notifications

#### Test Notification Sent
```php
use Filament\Notifications\Notification;
use function Filament\Notifications\Testing\assertNotified;
use function Pest\Livewire\livewire;

// Using Livewire helper
it('sends a notification', function () {
    livewire(CreatePost::class)
        ->assertNotified();
});

// Using dedicated helper
it('sends a notification', function () {
    assertNotified();
});

// Using Notification facade
it('sends a notification', function () {
    Notification::assertNotified();
});
```

#### Test Notification Not Sent
```php
use Filament\Notifications\Notification;
use function Pest\Livewire\livewire;

it('does not send a notification', function () {
    livewire(CreatePost::class)
        ->assertNotNotified()
        // or with specific title
        ->assertNotNotified('Unable to create post')
        // or with exact notification object
        ->assertNotNotified(
            Notification::make()
                ->danger()
                ->title('Unable to create post')
                ->body('Something went wrong.'),
        );
});
```

#### Test Exact Notification Object
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

### Testing Relation Managers

#### Test Relation Manager Renders
```php
use App\Filament\Resources\Users\Pages\EditUser;
use App\Filament\Resources\Users\RelationManagers\PostsRelationManager;
use App\Models\User;
use function Pest\Livewire\livewire;

it('can load the relation manager', function () {
    $user = User::factory()->create();

    livewire(EditUser::class, [
        'record' => $user->id,
    ])
        ->assertSeeLivewire(PostsRelationManager::class);
});
```

#### Test Relation Manager Data
```php
use App\Filament\Resources\Users\Pages\EditUser;
use App\Filament\Resources\Users\RelationManagers\PostsRelationManager;
use App\Models\Post;
use App\Models\User;
use function Pest\Livewire\livewire;

it('can load the relation manager', function () {
    $user = User::factory()
        ->has(Post::factory()->count(5))
        ->create();

    livewire(PostsRelationManager::class, [
        'ownerRecord' => $user,
        'pageClass' => EditUser::class,
    ])
        ->assertOk()
        ->assertCanSeeTableRecords($user->posts);
});
```

#### Test Relation Manager Actions
```php
use App\Filament\Resources\Users\Pages\EditUser;
use App\Filament\Resources\Users\RelationManagers\PostsRelationManager;
use App\Models\Post;
use App\Models\User;
use Filament\Actions\Testing\TestAction;
use function Pest\Laravel\assertDatabaseHas;
use function Pest\Livewire\livewire;

it('can create a post', function () {
    $user = User::factory()->create();
    $newPostData = Post::factory()->make();

    livewire(PostsRelationManager::class, [
        'ownerRecord' => $user,
        'pageClass' => EditUser::class,
    ])
        ->callAction(TestAction::make(CreateAction::class)->table(), [
            'title' => $newPostData->title,
            'content' => $newPostData->content,
        ])
        ->assertNotified();

    assertDatabaseHas(Post::class, [
        'title' => $newPostData->title,
        'content' => $newPostData->content,
        'user_id' => $user->id,
    ]);
});
```

## Important Testing Conventions

### Use Pest's Livewire Helper
Always import and use `Pest\Livewire\livewire` function for FilamentPHP tests:
```php
use function Pest\Livewire\livewire;
```

### Use RefreshDatabase
All FilamentPHP tests should use the `RefreshDatabase` trait or Pest's `uses()`:
```php
uses(RefreshDatabase::class);
```

### Test Structure
Follow this pattern for FilamentPHP resource tests:
```php
<?php

use App\Filament\Resources\Users\Pages\ListUsers;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use function Pest\Laravel\assertDatabaseHas;
use function Pest\Livewire\livewire;

uses(RefreshDatabase::class);

it('can load the page', function () {
    // Test implementation
});

it('can create a user', function () {
    // Test implementation
});

// More tests...
```

### Respect Permissions
When testing resources with policies or permissions:
```php
use function Pest\Laravel\actingAs;

it('authorized user can delete', function () {
    $user = User::factory()->create();
    $admin = User::factory()->admin()->create();

    actingAs($admin);

    livewire(EditUser::class, ['record' => $user->id])
        ->callAction(DeleteAction::class)
        ->assertNotified();
});
```

### Use Factory Pattern
Always use factories to create test data:
```php
$user = User::factory()->create();
$newUserData = User::factory()->make();
```

## Common Assertion Methods

### Livewire Assertions
- `assertOk()` - Assert successful page load
- `assertNotified()` - Assert notification was shown
- `assertRedirect()` - Assert redirect occurred
- `assertSuccessful()` - Assert component rendered successfully

### Table Assertions
- `assertCanSeeTableRecords($records)` - Assert records visible
- `assertCanNotSeeTableRecords($records)` - Assert records not visible
- `assertCountTableRecords($count)` - Assert record count
- `assertTableColumnVisible($column)` - Assert column visible
- `assertTableColumnHidden($column)` - Assert column hidden
- `assertTableColumnFormattedStateSet($column, $value, record: $record)`

### Schema Assertions
- `assertSchemaStateSet($data)` - Assert form/infolist data
- `assertSchemaComponentExists($key)` - Assert component exists
- `assertSchemaComponentDoesNotExist($key)` - Assert component doesn't exist
- `assertFormFieldEnabled($field)` - Assert field is enabled
- `assertFormFieldDisabled($field)` - Assert field is disabled
- `assertFormExists()` - Assert form exists
- `assertHasFormErrors($fields)` - Assert form has errors
- `assertHasNoFormErrors()` - Assert no form errors

### Action Assertions
- `assertActionExists($action)` - Assert action exists
- `assertActionDoesNotExist($action)` - Assert action doesn't exist
- `assertActionVisible($action)` - Assert action visible
- `assertActionHidden($action)` - Assert action hidden
- `assertActionEnabled($action)` - Assert action enabled
- `assertActionDisabled($action)` - Assert action disabled
- `assertActionHalted($action)` - Assert action was halted
- `assertActionHasUrl($action, $url)` - Assert action has URL
- `assertMountedActionModalSee($content)` - Assert modal content

### Database Assertions
- `assertDatabaseHas($model, $data)` - Assert record exists
- `assertDatabaseMissing($model)` - Assert record doesn't exist

## Tips and Best Practices

1. **Test One Thing at a Time**: Each test should focus on a single behavior
2. **Use Descriptive Test Names**: Use `it('can perform action')` format
3. **Clean Test Data**: Use factories and RefreshDatabase
4. **Test Happy and Sad Paths**: Test both success and failure scenarios
5. **Test Permissions**: Verify authorization works correctly
6. **Test Notifications**: Assert user feedback is displayed
7. **Test Redirects**: Verify navigation after actions
8. **Use Type Hinting**: Import classes for better IDE support
9. **Chain Assertions**: Livewire tests support method chaining
10. **Test Table State**: Verify filters, sorting, and searching work

## Common Patterns in Arabic UI Apps

Since this app uses Arabic UI:
- Test RTL layout rendering
- Verify Arabic text appears correctly
- Test date/time formatting for Arabic locale
- Verify currency formatting (EGP)
- Test Arabic validation messages

## References

- [FilamentPHP 4.x Testing Documentation](https://filamentphp.com/docs/4.x/testing)
- [Pest Documentation](https://pestphp.com/)
- [Laravel Testing Documentation](https://laravel.com/docs/testing)
- [Livewire Testing Documentation](https://livewire.laravel.com/docs/testing)
