# FilamentPHP Resources Reference

## Table of Contents

- [Overview](#overview)
- [Basic Resource Creation](#basic-resource-creation)
- [Form Configuration](#form-configuration)
- [Table Configuration](#table-configuration)
- [Navigation & Organization](#navigation--organization)
- [Record Sub-Navigation](#record-sub-navigation)
- [Relationship Management](#relationship-management)
- [Custom Eloquent Queries](#custom-eloquent-queries)
- [Authorization & Policies](#authorization--policies)
- [Custom Pages](#custom-pages)
- [Nested Resources](#nested-resources)
- [Code Quality Tips](#code-quality-tips)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Cross-References](#cross-references)

---

## Overview

Resources are the core building blocks of FilamentPHP admin panels. They provide a complete CRUD (Create, Read, Update, Delete) interface for your Eloquent models, integrating forms, tables, pages, and navigation into a cohesive unit.

### When to Use Resources

- Building admin interfaces for Eloquent models
- Managing database records with full CRUD operations
- Organizing related functionality under a single namespace
- Creating navigation hierarchies and groups
- Implementing authorization and access control

### Key Concepts

- **Resource Classes**: Central configuration for model management
- **Pages**: Individual views for listing, creating, editing, and viewing records
- **Schemas**: Reusable form and table definitions
- **Navigation**: Menu organization and grouping
- **Authorization**: Policy-based access control
- **Relationships**: Managing related models via relation managers

---

## Basic Resource Creation

### Generate a Basic Resource

Use the Artisan command to scaffold a new resource:

```shell
php artisan make:filament-resource Customer
```

This creates the following structure:

```text
Customers/
├── CustomerResource.php
├── Pages/
│   ├── CreateCustomer.php
│   ├── EditCustomer.php
│   └── ListCustomers.php
├── Schemas/
│   └── CustomerForm.php
└── Tables/
    └── CustomersTable.php
```

### Auto-Generate Forms and Tables

Generate a resource with auto-configured forms and tables based on database columns:

```shell
php artisan make:filament-resource Customer --generate
```

This command automatically infers field types and table structures from your database schema.

### Basic Resource Class Structure

```php
namespace App\Filament\Resources;

use App\Filament\Resources\CustomerResource\Pages;
use App\Models\Customer;
use Filament\Resources\Resource;

class CustomerResource extends Resource
{
    protected static ?string $model = Customer::class;

    protected static ?string $navigationIcon = 'heroicon-o-user';

    public static function form(Schema $schema): Schema
    {
        return $schema
            ->components([
                // Form components
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                // Table columns
            ]);
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListCustomers::route('/'),
            'create' => Pages\CreateCustomers::route('/create'),
            'edit' => Pages\EditCustomer::route('/{record}/edit'),
        ];
    }
}
```

---

## Form Configuration

### Using External Form Schema Class

Keep your resource organized by defining forms in separate schema classes:

```php
use App\Filament\Resources\Customers\Schemas\CustomerForm;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return CustomerForm::configure($schema);
}
```

The external schema class:

```php
namespace App\Filament\Resources\Customers\Schemas;

use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;

class CustomerForm
{
    public static function configure(Schema $schema): Schema
    {
        return $schema
            ->components([
                TextInput::make('name')->required(),
                TextInput::make('email')->email()->required(),
                // ...
            ]);
    }
}
```

### Inline Form Definition

For simpler resources, define forms directly in the resource class:

```php
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return $schema
        ->components([
            TextInput::make('name')->required(),
            TextInput::make('email')->email()->required(),
            // ...
        ]);
}
```

### Reusable Form Fields

Create static methods for commonly used field configurations:

```php
namespace App\Filament\Resources\Categories\Schemas;

use Filament\Forms\Components\TextInput;

class CategoryForm
{
    public static function getNameFormField(): TextInput
    {
        return TextInput::make('name')
            ->required()
            ->maxLength(255);
    }

    public static function getSlugFormField(): TextInput
    {
        return TextInput::make('slug')
            ->required()
            ->maxLength(255);
    }
}
```

Use in wizard steps:

```php
use App\Filament\Resources\Categories\Schemas\CategoryForm;
use Filament\Resources\Pages\CreateRecord;

class CreateCategory extends CreateRecord
{
    use CreateRecord\Concerns\HasWizard;

    protected function getSteps(): array
    {
        return [
            Step::make('Name')
                ->schema([
                    CategoryForm::getNameFormField(),
                    CategoryForm::getSlugFormField(),
                ]),
        ];
    }
}
```

---

## Table Configuration

### Using External Table Class

Define tables in separate classes for better organization:

```php
use App\Filament\Resources\Customers\Tables\CustomersTable;
use Filament\Tables\Table;

public static function table(Table $table): Table
{
    return CustomersTable::configure($table);
}
```

The external table class:

```php
namespace App\Filament\Resources\Customers\Tables;

use Filament\Actions\BulkActionGroup;
use Filament\Actions\DeleteBulkAction;
use Filament\Actions\EditAction;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Filters\Filter;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;

class CustomersTable
{
    public static function configure(Table $table): Table
    {
        return $table
            ->columns([
                TextColumn::make('name'),
                TextColumn::make('email'),
                // ...
            ])
            ->filters([
                Filter::make('verified')
                    ->query(fn (Builder $query): Builder => $query->whereNotNull('email_verified_at')),
                // ...
            ])
            ->recordActions([
                EditAction::make(),
            ])
            ->toolbarActions([
                BulkActionGroup::make([
                    DeleteBulkAction::make(),
                ]),
            ]);
    }
}
```

### Inline Table Definition

```php
use Filament\Actions\BulkActionGroup;
use Filament\Actions\DeleteBulkAction;
use Filament\Actions\EditAction;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Filters\Filter;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            TextColumn::make('name'),
            TextColumn::make('email'),
            // ...
        ])
        ->filters([
            Filter::make('verified')
                ->query(fn (Builder $query): Builder => $query->whereNotNull('email_verified_at')),
            // ...
        ])
        ->recordActions([
            EditAction::make(),
        ])
        ->toolbarActions([
            BulkActionGroup::make([
                DeleteBulkAction::make(),
            ]),
        ]);
}
```

### Modifying Table Queries

Customize the Eloquent query for the List page table:

```php
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;

public static function table(Table $table): Table
{
    return $table
        ->modifyQueryUsing(fn (Builder $query) => $query->withoutGlobalScopes());
}
```

---

## Navigation & Organization

### Navigation Icon

Set a custom icon for the resource in the navigation menu:

```php
protected static ?string $navigationIcon = 'heroicon-o-rectangle-stack';
```

Using Heroicon enum:

```php
use Filament\Support\Icons\Heroicon;

protected static string | BackedEnum | null $navigationIcon = Heroicon::OutlinedRectangleStack;
```

### Navigation Group

Organize resources into navigation groups:

```php
protected static ?string $navigationGroup = 'Shop';
```

Using enum for groups:

```php
protected static string | UnitEnum | null $navigationGroup = NavigationGroup::Shop;
```

### Navigation Sorting

Control the order of resources within their group:

```php
protected static ?int $navigationSort = 2;
```

### Navigation Label

Customize the resource's label in the navigation menu:

```php
protected static ?string $navigationLabel = 'Customer Management';
```

---

## Record Sub-Navigation

### Basic Sub-Navigation

Add sub-navigation tabs to individual record pages:

```php
use Filament\Resources\Pages\Page;

public static function getRecordSubNavigation(Page $page): array
{
    return $page->generateNavigationItems([
        ViewCustomer::class,
        EditCustomer::class,
        EditCustomerContact::class,
        ManageCustomerAddresses::class,
        ManageCustomerPayments::class,
    ]);
}
```

### Generating URL for Record Pages

Generate URLs to specific resource pages with record parameters:

```php
use App\Filament\Resources\Customers\CustomerResource;

CustomerResource::getUrl('edit', ['record' => $customer]); // /admin/customers/edit/1
```

---

## Relationship Management

### Relation Managers

Register relation managers in the resource:

```php
public static function getRelations(): array
{
    return [
        RelationManagers\PostsRelationManager::class,
    ];
}
```

### Generating Relation Managers

```bash
php artisan make:filament-relation-manager CategoryResource posts title
```

### Grouping Relation Managers

Organize multiple relation managers into tabs:

```php
use Filament\Resources\RelationManagers\RelationGroup;

public static function getRelations(): array
{
    return [
        RelationGroup::make('Contacts', [
            RelationManagers\IndividualsRelationManager::class,
            RelationManagers\OrganizationsRelationManager::class,
        ]),
    ];
}
```

### Reusing Resource Forms and Tables

Share form and table definitions between resources and relation managers:

```php
use App\Filament\Resources\Blog\Posts\PostResource;
use Filament\Schemas\Schema;
use Filament\Tables\Table;

public function form(Schema $schema): Schema
{
    return PostResource::form($schema);
}

public function table(Table $table): Table
{
    return PostResource::table($table);
}
```

### Accessing Owner Record

Get the parent record in a relation manager:

```php
$this->getOwnerRecord()
```

In static contexts (like form() or table()):

```php
use Filament\Forms;
use Filament\Resources\RelationManagers\RelationManager;
use Filament\Schemas\Schema;

public function form(Schema $schema): Schema
{
    return $schema
        ->components([
            Forms\Components\Select::make('store_id')
                ->options(function (RelationManager $livewire): array {
                    return $livewire->getOwnerRecord()->stores()
                        ->pluck('name', 'id')
                        ->toArray();
                }),
        ]);
}
```

### Relation Pages

Create dedicated pages for managing relationships:

```bash
php artisan make:filament-page ManageCustomerAddresses --resource=CustomerResource --type=ManageRelatedRecords
```

Register in resource:

```php
public static function getPages(): array
{
    return [
        'index' => Pages\ListCustomers::route('/'),
        'create' => Pages\CreateCustomer::route('/create'),
        'view' => Pages\ViewCustomer::route('/{record}'),
        'edit' => Pages\EditCustomer::route('/{record}/edit'),
        'addresses' => Pages\ManageCustomerAddresses::route('/{record}/addresses'),
    ];
}
```

Add to sub-navigation:

```php
use App\Filament\Resources\Customers\Pages;
use Filament\Resources\Pages\Page;

public static function getRecordSubNavigation(Page $page): array
{
    return $page->generateNavigationItems([
        // ...
        Pages\ManageCustomerAddresses::class,
    ]);
}
```

---

## Custom Eloquent Queries

### Basic Query Customization

Override the default Eloquent query:

```php
public static function getEloquentQuery(): Builder
{
    return parent::getEloquentQuery()->where('is_active', true);
}
```

### Removing Global Scopes

Remove all global scopes:

```php
public static function getEloquentQuery(): Builder
{
    return parent::getEloquentQuery()->withoutGlobalScopes();
}
```

Remove specific scopes:

```php
public static function getEloquentQuery(): Builder
{
    return parent::getEloquentQuery()->withoutGlobalScopes([ActiveScope::class]);
}
```

### Retrieving Soft-Deleted Records

Enable access to soft-deleted records:

```php
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\SoftDeletingScope;

public static function getRecordRouteBindingEloquentQuery(): Builder
{
    return parent::getRecordRouteBindingEloquentQuery()
        ->withoutGlobalScopes([
            SoftDeletingScope::class,
        ]);
}
```

### Multi-Tenancy with Global Scopes

Apply tenant-based filtering:

```php
use Illuminate\Database\Eloquent\Builder;

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

---

## Authorization & Policies

### Skip Authorization

Disable all authorization checks for a resource:

```php
protected static bool $shouldSkipAuthorization = true;
```

### Individual Record Authorization

Check policies for each record in bulk actions:

```php
DeleteBulkAction::make()->authorizeIndividualRecords()
```

```php
RestoreBulkAction::make()->authorizeIndividualRecords()
```

```php
ForceDeleteBulkAction::make()->authorizeIndividualRecords()
```

### Bulk Action Authorization

```php
use Filament\Actions\BulkAction;
use Illuminate\Database\Eloquent\Collection;

BulkAction::make('delete')
    ->requiresConfirmation()
    ->authorizeIndividualRecords('delete')
    ->action(fn (Collection $records) => $records->each->delete())
```

---

## Custom Pages

### Creating Custom Pages

Generate a custom page:

```bash
php artisan make:filament-page SortUsers --resource=UserResource
```

### Interacting with Records

Use the `InteractsWithRecord` trait for pages that work with specific records:

```php
use Filament\Resources\Pages\Page;
use Filament\Resources\Pages\Concerns\InteractsWithRecord;

class ManageUser extends Page
{
    use InteractsWithRecord;

    public function mount(int | string $record): void
    {
        $this->record = $this->resolveRecord($record);
    }

    // Access record via: $this->getRecord()
}
```

### Register Custom Page

Add custom pages to the resource:

```php
public static function getPages(): array
{
    return [
        'index' => Pages\ListUsers::route('/'),
        'create' => Pages\CreateUser::route('/create'),
        'sort' => Pages\SortUsers::route('/sort'),
        'manage' => Pages\ManageUser::route('/{record}/manage'),
    ];
}
```

### Singular Resources

For managing single records (like settings):

```php
namespace App\Filament\Pages;

use App\Models\WebsitePage;
use Filament\Actions\Action;
use Filament\Forms\Components\RichEditor;
use Filament\Forms\Components\TextInput;
use Filament\Notifications\Notification;
use Filament\Pages\Page;
use Filament\Schemas\Components\Actions;
use Filament\Schemas\Components\Form;
use Filament\Schemas\Schema;

class ManageHomepage extends Page
{
    protected string $view = 'filament.pages.manage-homepage';

    public ?array $data = [];

    public function mount(): void
    {
        $this->form->fill($this->getRecord()?->attributesToArray());
    }

    public function form(Schema $schema): Schema
    {
        return $schema
            ->components([
                Form::make([
                    TextInput::make('title')
                        ->required()
                        ->maxLength(255),
                    RichEditor::make('content'),
                ])
                    ->livewireSubmitHandler('save')
                    ->footer([
                        Actions::make([
                            Action::make('save')
                                ->submit('save')
                                ->keyBindings(['mod+s']),
                        ]),
                    ]),
            ])
            ->record($this->getRecord())
            ->statePath('data');
    }

    public function save(): void
    {
        $data = $this->form->getState();

        $record = $this->getRecord();

        if (! $record) {
            $record = new WebsitePage();
            $record->is_homepage = true;
        }

        $record->fill($data);
        $record->save();

        if ($record->wasRecentlyCreated) {
            $this->form->record($record)->saveRelationships();
        }

        Notification::make()
            ->success()
            ->title('Saved')
            ->send();
    }

    public function getRecord(): ?WebsitePage
    {
        return WebsitePage::query()
            ->where('is_homepage', true)
            ->first();
    }
}
```

---

## Nested Resources

### Configure Parent Resource

```php
use App\Filament\Resources\Courses\CourseResource;

protected static ?string $parentResource = CourseResource::class;
```

### Configure Related Resource

Set the related resource on a relation manager or page:

```php
use App\Filament\Resources\Courses\Resources\Lessons\LessonResource;

protected static ?string $relatedResource = LessonResource::class;
```

### Custom Relationship Names

```php
use App\Filament\Resources\Courses\CourseResource;
use Filament\Resources\ParentResourceRegistration;

public static function getParentResourceRegistration(): ?ParentResourceRegistration
{
    return CourseResource::asParent()
        ->relationship('lessons')
        ->inverseRelationship('course');
}
```

### Register with URL Parameter

```php
public static function getRelations(): array
{
    return [
        'lessons' => LessonsRelationManager::class,
    ];
}
```

---

## Code Quality Tips

### External Schema Classes

Keep resource classes clean by using external schema classes:

```php
// Resource
use App\Filament\Resources\Customers\Schemas\CustomerForm;
use App\Filament\Resources\Customers\Tables\CustomersTable;

public static function form(Schema $schema): Schema
{
    return CustomerForm::configure($schema);
}

public static function table(Table $table): Table
{
    return CustomersTable::configure($table);
}
```

### Reusable Action Classes

Create custom action classes for reusability:

```php
use App\Filament\Resources\Customers\Actions\EmailCustomerAction;
use Filament\Tables\Table;

public static function configure(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ])
        ->recordActions([
            EmailCustomerAction::make(),
        ]);
}
```

### Directory Organization

Organize resources with subdirectories:

```
Customers/
├── CustomerResource.php
├── Actions/
│   └── EmailCustomerAction.php
├── Pages/
│   ├── CreateCustomer.php
│   ├── EditCustomer.php
│   └── ListCustomers.php
├── Schemas/
│   └── CustomerForm.php
└── Tables/
    └── CustomersTable.php
```

---

## Best Practices

### 1. Use External Schema Classes

Keep resource files focused by extracting form and table definitions:

```php
public static function form(Schema $schema): Schema
{
    return CustomerForm::configure($schema);
}
```

### 2. Leverage Record Sub-Navigation

Provide intuitive navigation for related record pages:

```php
public static function getRecordSubNavigation(Page $page): array
{
    return $page->generateNavigationItems([
        ViewCustomer::class,
        EditCustomer::class,
        ManageCustomerAddresses::class,
    ]);
}
```

### 3. Customize Eloquent Queries Appropriately

Apply scopes and filters where needed:

```php
public static function getEloquentQuery(): Builder
{
    return parent::getEloquentQuery()
        ->where('is_active', true)
        ->with(['category', 'tags']);
}
```

### 4. Group Navigation Logically

Use navigation groups to organize related resources:

```php
protected static ?string $navigationGroup = 'Shop';
protected static ?int $navigationSort = 1;
```

### 5. Use Relationship Features

Leverage relation managers and relation pages for better UX:

```php
public static function getRelations(): array
{
    return [
        RelationManagers\AddressesRelationManager::class,
        RelationManagers\OrdersRelationManager::class,
    ];
}
```

### 6. Implement Proper Authorization

Use policies and authorization checks:

```php
// In policy
public function viewAny(User $user): bool
{
    return $user->hasPermissionTo('view customers');
}

// In resource
DeleteBulkAction::make()->authorizeIndividualRecords()
```

### 7. Handle Soft Deletes Properly

Configure soft delete support:

```php
public static function table(Table $table): Table
{
    return $table
        ->filters([
            TrashedFilter::make(),
        ])
        ->recordActions([
            DeleteAction::make(),
            ForceDeleteAction::make(),
            RestoreAction::make(),
        ]);
}

public static function getRecordRouteBindingEloquentQuery(): Builder
{
    return parent::getRecordRouteBindingEloquentQuery()
        ->withoutGlobalScopes([SoftDeletingScope::class]);
}
```

---

## Troubleshooting

### Records Not Appearing

**Problem**: Records don't show in the list table.

**Solution**: Check for global scopes filtering data:

```php
public static function getEloquentQuery(): Builder
{
    return parent::getEloquentQuery()->withoutGlobalScopes();
}
```

### Navigation Icon Not Showing

**Problem**: Navigation icon doesn't display.

**Solution**: Verify the icon name or use Heroicon enum:

```php
use Filament\Support\Icons\Heroicon;

protected static string | BackedEnum | null $navigationIcon = Heroicon::OutlinedRectangleStack;
```

### Relation Manager Not Showing

**Problem**: Relation manager doesn't appear on edit page.

**Solution**: Ensure it's registered in `getRelations()`:

```php
public static function getRelations(): array
{
    return [
        RelationManagers\PostsRelationManager::class,
    ];
}
```

### Sub-Navigation Not Working

**Problem**: Record sub-navigation tabs don't appear.

**Solution**: Implement `getRecordSubNavigation()` in the resource:

```php
public static function getRecordSubNavigation(Page $page): array
{
    return $page->generateNavigationItems([
        ViewRecord::class,
        EditRecord::class,
    ]);
}
```

### Authorization Errors

**Problem**: Users see "403 Forbidden" errors.

**Solution**: Check policies or skip authorization:

```php
protected static bool $shouldSkipAuthorization = true;
```

Or implement proper policies:

```php
// In CustomerPolicy
public function viewAny(User $user): bool
{
    return true;
}
```

### Custom Page Not Found

**Problem**: Custom page returns 404.

**Solution**: Register the page in `getPages()`:

```php
public static function getPages(): array
{
    return [
        'index' => Pages\ListCustomers::route('/'),
        'custom' => Pages\CustomPage::route('/custom'),
    ];
}
```

### Soft-Deleted Records Not Accessible

**Problem**: Can't view or restore soft-deleted records.

**Solution**: Remove the soft delete scope:

```php
public static function getRecordRouteBindingEloquentQuery(): Builder
{
    return parent::getRecordRouteBindingEloquentQuery()
        ->withoutGlobalScopes([SoftDeletingScope::class]);
}
```

---

## Cross-References

### Related Topics

- **[FORMS.md](FORMS.md)** - Configure resource form fields and validation
- **[TABLES.md](TABLES.md)** - Set up resource tables with columns and actions
- **[ACTIONS.md](ACTIONS.md)** - Add custom actions to resources
- **[SCHEMAS.md](SCHEMAS.md)** - Layout components for forms and tables
- **[PANEL_CONFIGURATION.md](PANEL_CONFIGURATION.md)** - Configure panel-level settings
- **[TENANCY.md](TENANCY.md)** - Implement multi-tenancy in resources
- **[GLOBAL_SEARCH.md](GLOBAL_SEARCH.md)** - Enable global search for resources
- **[TESTING.md](TESTING.md)** - Test resource functionality

### External Documentation

- [FilamentPHP Resources Documentation](https://filamentphp.com/docs/4.x/resources/overview)
- [Laravel Eloquent Documentation](https://laravel.com/docs/eloquent)
- [Laravel Policies Documentation](https://laravel.com/docs/authorization#creating-policies)

---

**Last Updated**: January 18, 2026  
**FilamentPHP Version**: 4.x  
**Status**: Complete
