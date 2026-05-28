# Testing - FilamentPHP 4.x Reference

## Table of Contents
1. [Overview](#overview)
2. [Test Environment Setup](#test-environment-setup)
3. [Testing Resources](#testing-resources)
4. [Testing Tables](#testing-tables)
5. [Testing Forms & Schemas](#testing-forms--schemas)
6. [Testing Actions](#testing-actions)
7. [Testing Relation Managers](#testing-relation-managers)
8. [Testing Notifications](#testing-notifications)
9. [Advanced Testing Patterns](#advanced-testing-patterns)
10. [Pest Datasets](#pest-datasets)
11. [Troubleshooting](#troubleshooting)
12. [Cross-References](#cross-references)

---

## Overview

**Purpose**: Testing FilamentPHP applications ensures resources, forms, tables, actions, and notifications work correctly. FilamentPHP provides extensive testing support through Pest and PHPUnit.

**Key Concepts**:
- **Livewire Testing**: FilamentPHP components are Livewire components
- **Pest Framework**: Modern testing framework with expressive syntax
- **RefreshDatabase**: Clean database state for each test
- **Authentication**: Simulate logged-in users with `actingAs()`
- **Assertions**: Verify component state, form data, table records, actions

**Common Use Cases**:
- Test resource CRUD operations (create, read, update, delete)
- Validate form submissions and error handling
- Verify table filtering, sorting, and searching
- Test action execution and modal behavior
- Ensure notifications are sent correctly

---

## Test Environment Setup

### Pest Configuration

```php
// tests/Pest.php
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(
    Tests\TestCase::class,
    RefreshDatabase::class,
)->in('Feature');

// Optional: Set default panel for all tests
uses()->beforeEach(function () {
    Filament::setCurrentPanel('admin');
})->in('Feature/Filament');
```

### Authentication Setup

**PHPUnit Style**:
```php
// tests/TestCase.php or individual test
use App\Models\User;

protected function setUp(): void
{
    parent::setUp();
    
    $this->actingAs(User::factory()->create());
}
```

**Pest Style**:
```php
// tests/Feature/Filament/SomeTest.php
use App\Models\User;

beforeEach(function () {
    $user = User::factory()->create();
    actingAs($user);
});
```

### Set Current Panel

```php
// When testing components directly (not via HTTP)
use Filament\Facades\Filament;

Filament::setCurrentPanel('admin'); // Where 'admin' is the panel ID
```

**Example with Specific Panel**:
```php
use Filament\Facades\Filament;

beforeEach(function () {
    Filament::setCurrentPanel('app');
    actingAs(User::factory()->create());
});
```

---

## Testing Resources

### Test Create Page Loads

```php
use App\Filament\Resources\Users\Pages\CreateUser;
use App\Models\User;

it('can load the page', function () {
    livewire(CreateUser::class)
        ->assertOk();
});
```

### Test Record Creation

```php
use App\Filament\Resources\Users\Pages\CreateUser;
use App\Models\User;
use function Pest\Laravel\assertDatabaseHas;

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

### Test Create Form Validation

```php
use App\Filament\Resources\Users\Pages\CreateUser;
use App\Models\User;
use Illuminate\Support\Str;

it('validates the form data', function (array $data, array $errors) {
    $newUserData = User::factory()->make();
    
    livewire(CreateUser::class)
        ->fillForm([
            'name' => $newUserData->name,
            'email' => $newUserData->email,
            ...$data,
        ])
        ->call('create')
        ->assertHasFormErrors($errors)
        ->assertNotNotified()
        ->assertNoRedirect();
})->with([
    '`name` is required' => [['name' => null], ['name' => 'required']],
    '`name` is max 255 characters' => [['name' => Str::random(256)], ['name' => 'max']],
    '`email` is a valid email address' => [['email' => Str::random()], ['email' => 'email']],
    '`email` is required' => [['email' => null], ['email' => 'required']],
    '`email` is max 255 characters' => [['email' => Str::random(256)], ['email' => 'max']],
]);
```

### Test Edit Page Loads

```php
use App\Filament\Resources\Users\Pages\EditUser;
use App\Models\User;

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
```

### Test Record Update

```php
use App\Filament\Resources\Users\Pages\EditUser;
use App\Models\User;
use function Pest\Laravel\assertDatabaseHas;

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

### Test Edit Form Validation

```php
use App\Filament\Resources\Users\Pages\EditUser;
use App\Models\User;
use Illuminate\Support\Str;

it('validates the form data', function (array $data, array $errors) {
    $user = User::factory()->create();
    $newUserData = User::factory()->make();
    
    livewire(EditUser::class, [
        'record' => $user->id,
    ])
        ->fillForm([
            'name' => $newUserData->name,
            'email' => $newUserData->email,
            ...$data,
        ])
        ->call('save')
        ->assertHasFormErrors($errors)
        ->assertNotNotified();
})->with([
    '`name` is required' => [['name' => null], ['name' => 'required']],
    '`name` is max 255 characters' => [['name' => Str::random(256)], ['name' => 'max']],
    '`email` is a valid email address' => [['email' => Str::random()], ['email' => 'email']],
    '`email` is required' => [['email' => null], ['email' => 'required']],
    '`email` is max 255 characters' => [['email' => Str::random(256)], ['email' => 'max']],
]);
```

### Test Record Deletion

```php
use App\Filament\Resources\Users\Pages\EditUser;
use App\Models\User;
use Filament\Actions\DeleteAction;
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

### Test View Page Loads

```php
use App\Filament\Resources\Users\Pages\ViewUser;
use App\Models\User;

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

### Test List Page Loads

```php
use App\Filament\Resources\Users\Pages\ListUsers;
use App\Models\User;

it('can load the page', function () {
    $users = User::factory()->count(5)->create();
    
    livewire(ListUsers::class)
        ->assertOk()
        ->assertCanSeeTableRecords($users);
});
```

---

## Testing Tables

### Test Table Rendering

```php
use function Pest\Livewire\livewire;

it('can render page', function () {
    livewire(ListPosts::class)
        ->assertSuccessful();
});
```

### Test Table Record Visibility

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

### Test Table Search

```php
use App\Filament\Resources\Users\Pages\ListUsers;
use App\Models\User;

it('can search users by `name` or `email`', function () {
    $users = User::factory()->count(5)->create();
    
    livewire(ListUsers::class)
        ->assertCanSeeTableRecords($users)
        ->searchTable($users->first()->name)
        ->assertCanSeeTableRecords($users->take(1))
        ->assertCanNotSeeTableRecords($users->skip(1))
        ->searchTable($users->last()->email)
        ->assertCanSeeTableRecords($users->take(-1))
        ->assertCanNotSeeTableRecords($users->take($users->count() - 1));
});
```

### Test Full Table Search

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

### Test Individual Column Search

```php
use function Pest\Livewire\livewire;

it('can search posts by title column', function () {
    $posts = Post::factory()->count(10)->create();
    $title = $posts->first()->title;
    
    livewire(PostResource\Pages\ListPosts::class)
        ->searchTableColumns(['title' => $title])
        ->assertCanSeeTableRecords($posts->where('title', $title))
        ->assertCanNotSeeTableRecords($posts->where('title', '!=', $title));
});
```

### Test Table Sorting

```php
use App\Filament\Resources\Users\Pages\ListUsers;
use App\Models\User;

it('can sort users by `name`', function () {
    $users = User::factory()->count(5)->create();
    
    livewire(ListUsers::class)
        ->assertCanSeeTableRecords($users)
        ->sortTable('name')
        ->assertCanSeeTableRecords($users->sortBy('name'), inOrder: true)
        ->sortTable('name', 'desc')
        ->assertCanSeeTableRecords($users->sortByDesc('name'), inOrder: true);
});
```

### Test Table Sorting with Database

```php
use function Pest\Livewire\livewire;

it('can sort posts by title', function () {
    Post::factory()->count(10)->create();
    
    $sortedPostsAsc = Post::query()->orderBy('title')->get();
    $sortedPostsDesc = Post::query()->orderBy('title', 'desc')->get();
    
    livewire(PostResource\Pages\ListPosts::class)
        ->sortTable('title')
        ->assertCanSeeTableRecords($sortedPostsAsc, inOrder: true)
        ->sortTable('title', 'desc')
        ->assertCanSeeTableRecords($sortedPostsDesc, inOrder: true);
});
```

### Test Table Filtering

```php
use App\Filament\Resources\Users\Pages\ListUsers;
use App\Models\User;

it('can filter users by `locale`', function () {
    $users = User::factory()->count(5)->create();
    
    livewire(ListUsers::class)
        ->assertCanSeeTableRecords($users)
        ->filterTable('locale', $users->first()->locale)
        ->assertCanSeeTableRecords($users->where('locale', $users->first()->locale))
        ->assertCanNotSeeTableRecords($users->where('locale', '!=', $users->first()->locale));
});
```

### Test Boolean Filter

```php
use function Pest\Livewire\livewire;

it('can filter posts by `is_published`', function () {
    $posts = Post::factory()->count(10)->create();
    
    livewire(PostResource\Pages\ListPosts::class)
        ->assertCanSeeTableRecords($posts)
        ->filterTable('is_published')
        ->assertCanSeeTableRecords($posts->where('is_published', true))
        ->assertCanNotSeeTableRecords($posts->where('is_published', false));
});
```

### Test Filter with Value

```php
use function Pest\Livewire\livewire;

it('can filter posts by `author_id`', function () {
    $posts = Post::factory()->count(10)->create();
    $authorId = $posts->first()->author_id;
    
    livewire(PostResource\Pages\ListPosts::class)
        ->assertCanSeeTableRecords($posts)
        ->filterTable('author_id', $authorId)
        ->assertCanSeeTableRecords($posts->where('author_id', $authorId))
        ->assertCanNotSeeTableRecords($posts->where('author_id', '!=', $authorId));
});
```

### Test Filter Visibility

```php
use function Pest\Livewire\livewire;

it('shows the correct filters', function () {
    livewire(PostsTable::class)
        ->assertTableFilterVisible('created_at')
        ->assertTableFilterHidden('author');
});
```

### Test Filter Existence

```php
use function Pest\Livewire\livewire;

it('has an author filter', function () {
    livewire(PostResource\Pages\ListPosts::class)
        ->assertTableFilterExists('author');
});
```

### Test Filter with Truth Test

```php
use function Pest\Livewire\livewire;
use Filament\Tables\Filters\SelectFilter;

it('has an author filter', function () {
    livewire(PostResource\Pages\ListPosts::class)
        ->assertTableFilterExists('author', function (SelectFilter $column): bool {
            return $column->getLabel() === 'Select author';
        });
});
```

### Test Removing Filters

```php
use function Pest\Livewire\livewire;

it('filters list by published', function () {
    $posts = Post::factory()->count(10)->create();
    $unpublishedPosts = $posts->where('is_published', false)->get();
    
    livewire(PostsTable::class)
        ->filterTable('is_published')
        ->assertCanNotSeeTableRecords($unpublishedPosts)
        ->removeTableFilter('is_published')
        ->assertCanSeeTableRecords($posts);
});
```

### Test Removing All Filters

```php
use function Pest\Livewire\livewire;

it('can remove all table filters', function () {
    $posts = Post::factory()->count(10)->forAuthor()->create();
    
    $unpublishedPosts = $posts->where('is_published', false)
        ->where('author_id', $posts->first()->author->getKey());
    
    livewire(PostsTable::class)
        ->filterTable('is_published')
        ->filterTable('author', $author)
        ->assertCanNotSeeTableRecords($unpublishedPosts)
        ->removeTableFilters()
        ->assertCanSeeTableRecords($posts);
});
```

### Test Resetting Filters

```php
use function Pest\Livewire\livewire;

it('can reset table filters', function () {
    $posts = Post::factory()->count(10)->create();
    
    livewire(PostResource\Pages\ListPosts::class)
        ->resetTableFilters();
});
```

### Test Column Visibility

```php
use function Pest\Livewire\livewire;

it('shows the correct columns', function () {
    livewire(PostResource\Pages\ListPosts::class)
        ->assertTableColumnVisible('created_at')
        ->assertTableColumnHidden('author');
});
```

### Test Column Existence

```php
use function Pest\Livewire\livewire;

it('has an author column', function () {
    livewire(PostResource\Pages\ListPosts::class)
        ->assertTableColumnExists('author');
});
```

### Test Column with Truth Test

```php
use function Pest\Livewire\livewire;
use Filament\Tables\Columns\TextColumn;

it('has an author column', function () {
    $post = Post::factory()->create();
    
    livewire(PostResource\Pages\ListPosts::class)
        ->assertTableColumnExists('author', function (TextColumn $column): bool {
            return $column->getDescriptionBelow() === $post->subtitle;
        }, $post);
});
```

### Test Column Rendering

```php
use function Pest\Livewire\livewire;

it('can render post titles', function () {
    Post::factory()->count(10)->create();
    
    livewire(PostResource\Pages\ListPosts::class)
        ->assertCanRenderTableColumn('title');
});

it('can not render post comments', function () {
    Post::factory()->count(10)->create();
    
    livewire(PostResource\Pages\ListPosts::class)
        ->assertCanNotRenderTableColumn('comments');
});
```

### Test Column State

```php
use function Pest\Livewire\livewire;

it('can get post author names', function () {
    $posts = Post::factory()->count(10)->create();
    $post = $posts->first();
    
    livewire(PostResource\Pages\ListPosts::class)
        ->assertTableColumnStateSet('author.name', $post->author->name, record: $post)
        ->assertTableColumnStateNotSet('author.name', 'Anonymous', record: $post);
});
```

### Test Column Formatted State

```php
use function Pest\Livewire\livewire;

it('can get post author names', function () {
    $post = Post::factory(['name' => 'John Smith'])->create();
    
    livewire(PostResource\Pages\ListPosts::class)
        ->assertTableColumnFormattedStateSet('author.name', 'Smith, John', record: $post)
        ->assertTableColumnFormattedStateNotSet('author.name', $post->author->name, record: $post);
});
```

### Test Column Description

```php
use function Pest\Livewire\livewire;

it('has the correct descriptions above and below author', function () {
    $post = Post::factory()->create();
    
    livewire(PostsTable::class)
        ->assertTableColumnHasDescription('author', 'Author! ↓↓↓', $post, 'above')
        ->assertTableColumnHasDescription('author', 'Author! ↑↑↑', $post)
        ->assertTableColumnDoesNotHaveDescription('author', 'Author! ↑↑↑', $post, 'above')
        ->assertTableColumnDoesNotHaveDescription('author', 'Author! ↓↓↓', $post);
});
```

### Test Column Extra Attributes

```php
use function Pest\Livewire\livewire;

it('displays author in red', function () {
    $post = Post::factory()->create();
    
    livewire(PostsTable::class)
        ->assertTableColumnHasExtraAttributes('author', ['class' => 'text-danger-500'], $post)
        ->assertTableColumnDoesNotHaveExtraAttributes('author', ['class' => 'text-primary-500'], $post);
});
```

### Test Select Column Options

```php
use function Pest\Livewire\livewire;

it('has the correct statuses', function () {
    $post = Post::factory()->create();
    
    livewire(PostsTable::class)
        ->assertTableSelectColumnHasOptions('status', ['unpublished' => 'Unpublished', 'published' => 'Published'], $post)
        ->assertTableSelectColumnDoesNotHaveOptions('status', ['archived' => 'Archived'], $post);
});
```

### Test Column Summaries

```php
use function Pest\Livewire\livewire;

it('can average values in a column', function () {
    $posts = Post::factory()->count(10)->create();
    
    livewire(PostResource\Pages\ListPosts::class)
        ->assertCanSeeTableRecords($posts)
        ->assertTableColumnSummarySet('rating', 'average', $posts->avg('rating'));
});
```

### Test Pagination-Specific Summaries

```php
use function Pest\Livewire\livewire;

it('can average values in a column', function () {
    $posts = Post::factory()->count(20)->create();
    
    livewire(PostResource\Pages\ListPosts::class)
        ->assertCanSeeTableRecords($posts->take(10))
        ->assertTableColumnSummarySet('rating', 'average', $posts->take(10)->avg('rating'), isCurrentPaginationPageOnly: true);
});
```

### Test Range Summary

```php
use function Pest\Livewire\livewire;

it('can average values in a column', function () {
    $posts = Post::factory()->count(10)->create();
    
    livewire(PostResource\Pages\ListPosts::class)
        ->assertCanSeeTableRecords($posts)
        ->assertTableColumnSummarySet('rating', 'range', [$posts->min('rating'), $posts->max('rating')]);
});
```

### Test Toggling Columns

```php
use function Pest\Livewire\livewire;

it('can toggle all columns', function () {
    livewire(PostResource\Pages\ListPosts::class)
        ->toggleAllTableColumns();
});

it('can toggle all columns off', function () {
    livewire(PostResource\Pages\ListPosts::class)
        ->toggleAllTableColumns(false);
});
```

### Test Bulk Delete

```php
use App\Filament\Resources\Users\Pages\ListUsers;
use App\Models\User;
use Filament\Actions\Testing\TestAction;
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

---

## Testing Forms & Schemas

### Test Form Exists

```php
use function Pest\Livewire\livewire;

it('has a form', function () {
    livewire(CreatePost::class)
        ->assertFormExists();
});
```

### Fill Form with Data

```php
use function Pest\Livewire\livewire;

livewire(CreatePost::class)
    ->fillForm([
        'title' => fake()->sentence(),
        // ...
    ]);
```

### Test Form Validation

```php
use function Pest\Livewire\livewire;

it('can validate input', function () {
    livewire(CreatePost::class)
        ->fillForm([
            'title' => null,
        ])
        ->call('create')
        ->assertHasFormErrors(['title' => 'required']);
});
```

### Test No Validation Errors

```php
use function Pest\Livewire\livewire;

livewire(CreatePost::class)
    ->fillForm([
        'title' => fake()->sentence(),
        // ...
    ])
    ->call('create')
    ->assertHasNoFormErrors();
```

### Test Form State

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

### Test Form State with Callback

```php
use Filament\Forms\Components\Repeater;
use function Pest\Livewire\livewire;

$undoRepeaterFake = Repeater::fake();

livewire(EditPost::class, ['record' => $post])
    ->assertSchemaStateSet(function (array $state) {
        expect($state['quotes'])
            ->toHaveCount(2);
    });

$undoRepeaterFake();
```

### Test Schema Component Exists

```php
use function Pest\Livewire\livewire;

test('comments section exists', function () {
    livewire(EditPost::class)
        ->assertSchemaComponentExists('comments-section');
});
```

### Test Schema Component Does Not Exist

```php
use function Pest\Livewire\livewire;

it('does not have a conditional component', function () {
    livewire(CreatePost::class)
        ->assertSchemaComponentDoesNotExist('no-such-section');
});
```

### Test Schema Component with Callback

```php
use Filament\Schemas\Components\Section;
use function Pest\Livewire\livewire;

test('comments section has heading', function () {
    livewire(EditPost::class)
        ->assertSchemaComponentExists(
            'comments-section',
            checkComponentUsing: function (Section $component): bool {
                return $component->getHeading() === 'Comments';
            },
        );
});
```

### Test Field Visibility

```php
use function Pest\Livewire\livewire;

test('title is visible', function () {
    livewire(CreatePost::class)
        ->assertFormFieldVisible('title');
});

test('title is hidden', function () {
    livewire(CreatePost::class)
        ->assertFormFieldHidden('title');
});
```

### Test Field Enabled/Disabled

```php
use function Pest\Livewire\livewire;

test('title is enabled', function () {
    livewire(CreatePost::class)
        ->assertFormFieldEnabled('title');
});

test('title is disabled', function () {
    livewire(CreatePost::class)
        ->assertFormFieldDisabled('title');
});
```

### Test Field Exists

```php
use function Pest\Livewire\livewire;

it('has a title field', function () {
    livewire(CreatePost::class)
        ->assertFormFieldExists('title');
});
```

### Test Field Configuration

```php
use function Pest\Livewire\livewire;

it('has a title field', function () {
    livewire(CreatePost::class)
        ->assertFormFieldExists('title', function (TextInput $field): bool {
            return $field->isDisabled();
        });
});
```

### Test Field Does Not Exist

```php
use function Pest\Livewire\livewire;

it('does not have a conditional field', function () {
    livewire(CreatePost::class)
        ->assertFormFieldDoesNotExist('no-such-field');
});
```

### Test Wizard Navigation

```php
use function Pest\Livewire\livewire;

it('moves to next wizard step', function () {
    livewire(CreatePost::class)
        ->goToNextWizardStep()
        ->assertHasFormErrors(['title']);
});

it('moves to next wizard step', function () {
    livewire(CreatePost::class)
        ->goToPreviousWizardStep()
        ->assertHasFormErrors(['title']);
});

it('moves to the wizards second step', function () {
    livewire(CreatePost::class)
        ->goToWizardStep(2)
        ->assertWizardCurrentStep(2);
});
```

### Test Wizard with Multiple Schemas

```php
use function Pest\Livewire\livewire;

it('moves to next wizard step only for fooForm', function () {
    livewire(CreatePost::class)
        ->goToNextWizardStep(schema: 'fooForm')
        ->assertHasFormErrors(['title'], schema: 'fooForm');
});
```

### Test Repeater State

```php
use Filament\Forms\Components\Repeater;
use function Pest\Livewire\livewire;

$undoRepeaterFake = Repeater::fake();

livewire(EditPost::class, ['record' => $post])
    ->assertSchemaStateSet([
        'quotes' => [
            [
                'content' => 'First quote',
            ],
            [
                'content' => 'Second quote',
            ],
        ],
    ]);

$undoRepeaterFake();
```

### Test Builder State

```php
use Filament\Forms\Components\Builder;
use function Pest\Livewire\livewire;

$undoBuilderFake = Builder::fake();

livewire(EditPost::class, ['record' => $post])
    ->assertSchemaStateSet([
        'content' => [
            [
                'type' => 'heading',
                'data' => [
                    'content' => 'Hello, world!',
                    'level' => 'h1',
                ],
            ],
            [
                'type' => 'paragraph',
                'data' => [
                    'content' => 'This is a test post.',
                ],
            ],
        ],
    ]);

$undoBuilderFake();
```

### Test Repeater Actions

```php
use App\Models\Quote;
use Filament\Forms\Components\Repeater;
use function Pest\Livewire\livewire;

$quote = Quote::first();

livewire(EditPost::class, ['record' => $post])
    ->callAction(TestAction::make('sendQuote')->schemaComponent('quotes')->arguments([
        'item' => "record-{$quote->getKey()}",
    ]))
    ->assertNotified('Quote sent!');
```

---

## Testing Actions

### Test Basic Action

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

### Test Action with Data

```php
use function Pest\Livewire\livewire;

it('can send invoices', function () {
    $invoice = Invoice::factory()->create();
    
    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->callAction('send', data: [
            'email' => $email = fake()->email(),
        ])
        ->assertHasNoFormErrors();
    
    expect($invoice->refresh())
        ->isSent()->toBeTrue()
        ->recipient_email->toBe($email);
});
```

### Test Prebuilt Action

```php
use Filament\Actions\CreateAction;
use function Pest\Livewire\livewire;

livewire(ManageInvoices::class)
    ->callAction(CreateAction::class);
```

### Test Custom Action Class

```php
use App\Filament\Resources\Invoices\Actions\SendInvoiceAction;
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

$invoice = Invoice::factory()->create();

livewire(ManageInvoices::class)
    ->callAction(TestAction::make(SendInvoiceAction::class)->table($invoice));
```

### Test Table Action

```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

$invoice = Invoice::factory()->create();

livewire(ListInvoices::class)
    ->callAction(TestAction::make('send')->table($invoice));

livewire(ListInvoices::class)
    ->assertActionVisible(TestAction::make('send')->table($invoice));

livewire(ListInvoices::class)
    ->assertActionExists(TestAction::make('send')->table($invoice));
```

### Test Header Action

```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

livewire(ListInvoices::class)
    ->callAction(TestAction::make('create')->table());

livewire(ListInvoices::class)
    ->assertActionVisible(TestAction::make('create')->table());

livewire(ListInvoices::class)
    ->assertActionExists(TestAction::make('create')->table());
```

### Test Bulk Action

```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

$invoices = Invoice::factory()->count(3)->create();

livewire(ListInvoices::class)
    ->selectTableRecords($invoices->pluck('id')->toArray())
    ->callAction(TestAction::make('send')->table()->bulk());

livewire(ListInvoices::class)
    ->assertActionVisible(TestAction::make('send')->table()->bulk());

livewire(ListInvoices::class)
    ->assertActionExists(TestAction::make('send')->table()->bulk());
```

### Test Schema Component Action

```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

$invoice = Invoice::factory()->create();

livewire(EditInvoice::class)
    ->callAction(TestAction::make('send')->schemaComponent('customer_id'));

livewire(EditInvoice::class)
    ->assertActionVisible(TestAction::make('send')->schemaComponent('customer_id'));

livewire(EditInvoice::class)
    ->assertActionExists(TestAction::make('send')->schemaComponent('customer_id'));
```

### Test Nested Actions

```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

$invoice = Invoice::factory()->create();

livewire(ManageInvoices::class)
    ->callAction([
        TestAction::make('view')->table($invoice),
        TestAction::make('send')->schemaComponent('customer.name'),
    ]);

livewire(ManageInvoices::class)
    ->assertActionVisible([
        TestAction::make('view')->table($invoice),
        TestAction::make('send')->schemaComponent('customer.name'),
    ]);

livewire(ManageInvoices::class)
    ->assertActionExists([
        TestAction::make('view')->table($invoice),
        TestAction::make('send')->schemaComponent('customer.name'),
    ]);
```

### Test Action with Arguments

```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

$invoice = Invoice::factory()->create();

livewire(ManageInvoices::class)
    ->callAction(TestAction::make('send')->arguments(['invoice' => $invoice->getKey()]));

livewire(ManageInvoices::class)
    ->assertActionVisible(TestAction::make('send')->arguments(['invoice' => $invoice->getKey()]));

livewire(ManageInvoices::class)
    ->assertActionExists(TestAction::make('send')->arguments(['invoice' => $invoice->getKey()]));
```

### Test Action Visibility

```php
use function Pest\Livewire\livewire;

it('can only print invoices', function () {
    $invoice = Invoice::factory()->create();
    
    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionHidden('send')
        ->assertActionVisible('print');
});
```

### Test Action Hidden

```php
use function Pest\Livewire\livewire;

it('can not send invoices', function () {
    $invoice = Invoice::factory()->create();
    
    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionHidden('send');
});
```

### Test Action Existence

```php
use function Pest\Livewire\livewire;

it('can send but not unsend invoices', function () {
    $invoice = Invoice::factory()->create();
    
    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionExists('send')
        ->assertActionDoesNotExist('unsend');
});
```

### Test Actions in Order

```php
use function Pest\Livewire\livewire;

it('can have actions in order', function () {
    $invoice = Invoice::factory()->create();
    
    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionsExistInOrder(['send', 'export']);
});
```

### Test Action Enabled/Disabled

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

### Test Action Label

```php
use function Pest\Livewire\livewire;

it('send action has correct label', function () {
    $invoice = Invoice::factory()->create();
    
    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionHasLabel('send', 'Email Invoice')
        ->assertActionDoesNotHaveLabel('send', 'Send');
});
```

### Test Action Icon

```php
use function Pest\Livewire\livewire;

it('when enabled the send button has correct icon', function () {
    $invoice = Invoice::factory()->create();
    
    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionEnabled('send')
        ->assertActionHasIcon('send', 'envelope-open')
        ->assertActionDoesNotHaveIcon('send', 'envelope');
});
```

### Test Action Color

```php
use function Pest\Livewire\livewire;

it('actions display proper colors', function () {
    $invoice = Invoice::factory()->create();
    
    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionHasColor('delete', 'danger')
        ->assertActionDoesNotHaveColor('print', 'danger');
});
```

### Test Action URL

```php
use function Pest\Livewire\livewire;

it('links to the correct Filament sites', function () {
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

### Test Action Halted

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

### Test Action Modal Content

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

### Test Pre-filled Action Data

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

### Test Action Form Pre-fill

```php
use function Pest\Livewire\livewire;

it('can send invoices', function () {
    $invoice = Invoice::factory()->create();
    
    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->mountAction('send')
        ->fillForm([
            'email' => $email = fake()->email(),
        ]);
});
```

### Test Action Form Validation

```php
use function Pest\Livewire\livewire;

it('can validate invoice recipient email', function () {
    $invoice = Invoice::factory()->create();
    
    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->callAction('send', data: [
            'email' => Str::random(),
        ])
        ->assertHasFormErrors(['email' => ['email']]);
});
```

### Test Action with Callback

```php
use Filament\Actions\Action;
use function Pest\Livewire\livewire;

it('has the correct description', function () {
    $invoice = Invoice::factory()->create();
    
    livewire(EditInvoice::class, [
        'invoice' => $invoice,
    ])
        ->assertActionExists('send', function (Action $action): bool {
            return $action->getModalDescription() === 'This will send an email to the customer\'s primary address, with the invoice attached as a PDF';
        });
});
```

### Test Form Actions

```php
use App\Filament\Resources\Users\Pages\CreateUser;
use App\Models\User;
use Filament\Actions\Testing\TestAction;

it('can create a user and verify their email address', function () {
    livewire(CreateUser::class)
        ->fillForm([
            'name' => 'Test User',
            'email' => 'test@example.com',
        ])
        ->callAction(TestAction::make('createAndVerifyEmail')->schemaComponent('form-actions', schema: 'content'));
    
    expect(User::query()->where('email', 'test@example.com')->first())
        ->hasVerifiedEmail()->toBeTrue();
});
```

---

## Testing Relation Managers

### Test Relation Manager Renders

```php
use App\Filament\Resources\Users\Pages\EditUser;
use App\Filament\Resources\Users\RelationManagers\PostsRelationManager;
use App\Models\User;

it('can load the relation manager', function () {
    $user = User::factory()->create();
    
    livewire(EditUser::class, [
        'record' => $user->id,
    ])
        ->assertSeeLivewire(PostsRelationManager::class);
});
```

### Test Relation Manager Loads Data

```php
use App\Filament\Resources\Users\Pages\EditUser;
use App\Filament\Resources\Users\RelationManagers\PostsRelationManager;
use App\Models\Post;
use App\Models\User;

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

### Test Relation Manager Create Action

```php
use App\Filament\Resources\Users\Pages\EditUser;
use App\Filament\Resources\Users\RelationManagers\PostsRelationManager;
use App\Models\Post;
use App\Models\User;
use Filament\Actions\Testing\TestAction;
use function Pest\Laravel\assertDatabaseHas;

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

---

## Testing Notifications

### Test Notification Sent (Livewire Helper)

```php
use function Pest\Livewire\livewire;

it('sends a notification', function () {
    livewire(CreatePost::class)
        ->assertNotified();
});
```

### Test Notification Sent (Facade)

```php
use Filament\Notifications\Notification;

it('sends a notification', function () {
    Notification::assertNotified();
});
```

### Test Notification Sent (Helper Function)

```php
use function Filament\Notifications\Testing\assertNotified;

it('sends a notification', function () {
    assertNotified();
});
```

### Test assertNotNotified

```php
use function Pest\Livewire\livewire;

it('validates the form data', function (array $data, array $errors) {
    $newUserData = User::factory()->make();
    
    livewire(CreateUser::class)
        ->fillForm([
            'name' => $newUserData->name,
            'email' => $newUserData->email,
            ...$data,
        ])
        ->call('create')
        ->assertHasFormErrors($errors)
        ->assertNotNotified()
        ->assertNoRedirect();
})->with([
    '`name` is required' => [['name' => null], ['name' => 'required']],
]);
```

---

## Advanced Testing Patterns

### Define Custom Action Name

**Using Attribute**:
```php
use Filament\Actions\Action;
use Filament\Actions\ActionName;

#[ActionName('send')]
class SendInvoiceAction
{
    public static function make(): Action
    {
        return Action::make('send')
            ->requiresConfirmation()
            ->action(function () {
                // ...
            });
    }
}
```

**Using getDefaultName**:
```php
use Filament\Actions\Action;

class SendInvoiceAction extends Action
{
    public static function getDefaultName(): string
    {
        return 'send';
    }
    
    protected function setUp(): void
    {
        parent::setUp();
        
        $this
            ->requiresConfirmation()
            ->action(function () {
                // ...
            });
    }
}
```

### Multi-Tenant Testing

```php
use Filament\Facades\Filament;

beforeEach(function () {
    $tenant = Team::factory()->create();
    $user = User::factory()->create();
    
    // Associate user with tenant
    $user->teams()->attach($tenant);
    
    // Set current tenant
    Filament::setTenant($tenant);
    
    actingAs($user);
});

it('can only see tenant posts', function () {
    $tenantPosts = Post::factory()->count(3)->create([
        'team_id' => Filament::getTenant()->id,
    ]);
    
    $otherPosts = Post::factory()->count(2)->create([
        'team_id' => Team::factory()->create()->id,
    ]);
    
    livewire(ListPosts::class)
        ->assertCanSeeTableRecords($tenantPosts)
        ->assertCanNotSeeTableRecords($otherPosts);
});
```

### Test with Permissions/Policies

```php
use App\Models\User;
use Spatie\Permission\Models\Role;

beforeEach(function () {
    $role = Role::create(['name' => 'editor']);
    $user = User::factory()->create();
    $user->assignRole('editor');
    
    actingAs($user);
});

it('editors can edit posts', function () {
    $post = Post::factory()->create();
    
    livewire(EditPost::class, [
        'record' => $post->id,
    ])
        ->assertOk()
        ->assertActionExists('save');
});

it('editors cannot delete posts', function () {
    $post = Post::factory()->create();
    
    livewire(EditPost::class, [
        'record' => $post->id,
    ])
        ->assertActionHidden('delete');
});
```

### Test Custom Table

```php
use App\Livewire\ListProducts;
use App\Models\Shop\Product;

it('can render products table', function () {
    Product::factory()->count(10)->create();
    
    livewire(ListProducts::class)
        ->assertSuccessful()
        ->assertCanRenderTableColumn('name');
});
```

### Test Multiple Forms

```php
use function Pest\Livewire\livewire;

it('can submit both forms independently', function () {
    $post = Post::factory()->create();
    
    livewire(EditPost::class, ['record' => $post])
        // Test post form
        ->fillForm([
            'title' => 'Updated Title',
        ], 'postData')
        ->assertSchemaStateSet([
            'title' => 'Updated Title',
        ], 'postData')
        
        // Test comment form
        ->fillForm([
            'name' => 'John Doe',
            'email' => 'john@example.com',
        ], 'commentData')
        ->assertSchemaStateSet([
            'name' => 'John Doe',
            'email' => 'john@example.com',
        ], 'commentData');
});
```

---

## Pest Datasets

### Basic Dataset Usage

```php
use Illuminate\Support\Str;

it('validates the form data', function (array $data, array $errors) {
    $newUserData = User::factory()->make();
    
    livewire(CreateUser::class)
        ->fillForm([
            'name' => $newUserData->name,
            'email' => $newUserData->email,
            ...$data,
        ])
        ->call('create')
        ->assertHasFormErrors($errors)
        ->assertNotNotified()
        ->assertNoRedirect();
})->with([
    '`name` is required' => [['name' => null], ['name' => 'required']],
    '`name` is max 255 characters' => [['name' => Str::random(256)], ['name' => 'max']],
    '`email` is a valid email address' => [['email' => Str::random()], ['email' => 'email']],
    '`email` is required' => [['email' => null], ['email' => 'required']],
    '`email` is max 255 characters' => [['email' => Str::random(256)], ['email' => 'max']],
]);
```

### Shared Dataset

```php
// tests/Datasets/UserData.php
dataset('invalid_user_data', [
    '`name` is required' => [['name' => null], ['name' => 'required']],
    '`name` is max 255 characters' => [['name' => Str::random(256)], ['name' => 'max']],
    '`email` is a valid email address' => [['email' => Str::random()], ['email' => 'email']],
    '`email` is required' => [['email' => null], ['email' => 'required']],
    '`email` is max 255 characters' => [['email' => Str::random(256)], ['email' => 'max']],
]);

// tests/Feature/Filament/CreateUserTest.php
it('validates create form data', function (array $data, array $errors) {
    // ...
})->with('invalid_user_data');

// tests/Feature/Filament/EditUserTest.php
it('validates edit form data', function (array $data, array $errors) {
    // ...
})->with('invalid_user_data');
```

---

## Troubleshooting

### Tests Fail with "Panel not found"

**Problem**: Tests throw errors about missing panel

**Solution**:
```php
use Filament\Facades\Filament;

beforeEach(function () {
    Filament::setCurrentPanel('admin'); // Set correct panel ID
    actingAs(User::factory()->create());
});
```

### Tests Fail with "Unauthenticated"

**Problem**: Tests require authentication but user not set

**Solution**:
```php
use App\Models\User;

beforeEach(function () {
    actingAs(User::factory()->create());
});
```

### Table Records Not Visible in Tests

**Problem**: `assertCanSeeTableRecords()` fails but records exist

**Solutions**:
1. Check tenant scoping:
   ```php
   beforeEach(function () {
       $tenant = Team::factory()->create();
       Filament::setTenant($tenant);
       actingAs(User::factory()->create());
   });
   ```

2. Check policies/permissions:
   ```php
   it('can see posts', function () {
       // Create posts belonging to authenticated user
       $posts = Post::factory()->count(5)->create([
           'user_id' => auth()->id(),
       ]);
       
       livewire(ListPosts::class)
           ->assertCanSeeTableRecords($posts);
   });
   ```

### Form Validation Not Working

**Problem**: `assertHasFormErrors()` fails

**Solutions**:
1. Check field names match validation rules:
   ```php
   // Form field
   TextInput::make('email')
   
   // Validation rule
   'email' => 'required|email'
   
   // Test
   ->assertHasFormErrors(['email' => 'required'])
   ```

2. Ensure validation runs:
   ```php
   livewire(CreateUser::class)
       ->fillForm(['email' => null])
       ->call('create') // Must call action to trigger validation
       ->assertHasFormErrors(['email' => 'required']);
   ```

### Actions Not Found in Tests

**Problem**: `assertActionExists()` fails

**Solutions**:
1. Check action name:
   ```php
   // Action definition
   Action::make('send')
   
   // Test
   ->assertActionExists('send') // Use exact name
   ```

2. Check action visibility:
   ```php
   // Action may be hidden
   Action::make('delete')
       ->hidden(fn ($record) => !auth()->user()->can('delete', $record))
   
   // Test with proper permissions
   ```

3. Use TestAction for table/bulk actions:
   ```php
   use Filament\Actions\Testing\TestAction;
   
   livewire(ListInvoices::class)
       ->callAction(TestAction::make('send')->table($invoice));
   ```

### Repeater/Builder Tests Fail

**Problem**: UUID keys cause inconsistent test results

**Solution**: Use fake() methods:
```php
use Filament\Forms\Components\Repeater;
use Filament\Forms\Components\Builder;

$undoRepeaterFake = Repeater::fake();
$undoBuilderFake = Builder::fake();

// Run tests...

$undoRepeaterFake();
$undoBuilderFake();
```

### Database Not Refreshing

**Problem**: Tests interfere with each other

**Solution**:
```php
// tests/Pest.php
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(
    Tests\TestCase::class,
    RefreshDatabase::class, // Add this trait
)->in('Feature');
```

---

## Cross-References

### Related Documentation
- [RESOURCES.md](RESOURCES.md) - Resource structure and CRUD operations
- [TABLES.md](TABLES.md) - Table configuration for list pages
- [FORMS.md](FORMS.md) - Form schemas and validation
- [ACTIONS.md](ACTIONS.md) - Action configuration and behavior
- [NOTIFICATIONS.md](NOTIFICATIONS.md) - Notification system
- [PANEL_CONFIGURATION.md](PANEL_CONFIGURATION.md) - Panel setup and authentication
- [TENANCY.md](TENANCY.md) - Multi-tenancy testing patterns

### External Resources
- [Pest Documentation](https://pestphp.com/docs)
- [Laravel Testing Docs](https://laravel.com/docs/11.x/testing)
- [Livewire Testing Docs](https://livewire.laravel.com/docs/testing)
- [FilamentPHP Testing Docs](https://filamentphp.com/docs/4.x/testing)

### Common Patterns
- **Resource Testing**: Test create, edit, delete pages with validation
- **Table Testing**: Test search, filter, sort, bulk actions
- **Form Testing**: Test field visibility, validation, state
- **Action Testing**: Test modals, data submission, side effects
- **Multi-Tenant**: Scope tests to current tenant
- **Permissions**: Test with different user roles and policies

---

**Last Updated**: January 2024  
**FilamentPHP Version**: 4.x  
**Larament Project**: Laravel + FilamentPHP + React/Inertia  
**Testing Framework**: Pest (PHP 8.1+)
