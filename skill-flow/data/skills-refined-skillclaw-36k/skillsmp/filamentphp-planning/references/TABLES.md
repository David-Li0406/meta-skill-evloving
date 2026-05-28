# FilamentPHP Tables Reference

**Version:** FilamentPHP 4.x  
**Last Updated:** January 18, 2026

## Table of Contents

1. [Overview](#overview)
2. [Table Configuration](#table-configuration)
3. [Columns](#columns)
   - [TextColumn](#textcolumn)
   - [IconColumn](#iconcolumn)
   - [ImageColumn](#imagecolumn)
   - [ColorColumn](#colorcolumn)
   - [SelectColumn](#selectcolumn)
   - [ToggleColumn](#togglecolumn)
   - [TextInputColumn](#textinputcolumn)
4. [Search Functionality](#search-functionality)
5. [Filters](#filters)
6. [Sorting](#sorting)
7. [Actions](#actions)
8. [Bulk Actions](#bulk-actions)
9. [Pagination](#pagination)
10. [Reordering](#reordering)
11. [Column Management](#column-management)
12. [Custom Data Sources](#custom-data-sources)
13. [Layout Components](#layout-components)
14. [Global Configuration](#global-configuration)
15. [Best Practices](#best-practices)
16. [Troubleshooting](#troubleshooting)

---

## Overview

FilamentPHP Tables provide a powerful system for displaying, searching, filtering, and manipulating data. Tables are the primary way to present collections of records in resources, relation managers, and custom Livewire components.

### When to Use Tables

- Displaying resource records in list pages
- Managing relationships in relation managers
- Creating custom data tables in pages
- Building admin dashboards with data listings
- Implementing custom Livewire components with tables

### Key Concepts

- **Columns:** Display data from your models
- **Search:** Global and per-column searching
- **Filters:** Query constraints and refinements
- **Actions:** Row-level operations
- **Bulk Actions:** Multi-row operations
- **Sorting:** Column-based ordering
- **Pagination:** Efficient data loading
- **Reordering:** Drag-and-drop record ordering

---

## Table Configuration

### Basic Table Setup

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([
            // Define columns
        ])
        ->filters([
            // Define filters
        ])
        ->recordActions([
            // Define row actions
        ])
        ->toolbarActions([
            // Define toolbar actions
        ]);
}
```

### Define in Resource

```php
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            TextColumn::make('name'),
            TextColumn::make('email'),
        ]);
}
```

### Define in Separate Class

```php
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;

class UsersTable
{
    public static function configure(Table $table): Table
    {
        return $table
            ->columns([
                TextColumn::make('name'),
                TextColumn::make('email'),
            ]);
    }
}
```

---

## Columns

### TextColumn

The most versatile column type for displaying text data.

#### Basic Usage

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('title')
```

#### Label

```php
TextColumn::make('name')
    ->label('Full name')
    ->label(__('columns.name')) // Localized
```

#### Formatting State

```php
TextColumn::make('status')
    ->formatStateUsing(fn (string $state): string => __("statuses.{$state}"))
```

#### Date Formatting

```php
TextColumn::make('created_at')
    ->date()
    ->date('d/m/Y')

TextColumn::make('created_at')
    ->dateTime()
    ->dateTime('d/m/Y H:i:s')

TextColumn::make('created_at')
    ->time()
    ->time('H:i')
```

#### ISO Date Formatting

```php
TextColumn::make('created_at')
    ->isoDate()

TextColumn::make('created_at')
    ->isoDateTime()

TextColumn::make('created_at')
    ->isoTime()
```

#### Money Formatting

```php
TextColumn::make('price')
    ->money()
    ->money('EUR')
```

#### Badges

```php
TextColumn::make('status')
    ->badge()
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'gray',
        'reviewing' => 'warning',
        'published' => 'success',
        'rejected' => 'danger',
    })

// Conditional badge
TextColumn::make('status')
    ->badge(FeatureFlag::active())
```

#### Colors

```php
TextColumn::make('status')
    ->color('primary') // Static

TextColumn::make('status')
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'info',
        'reviewing' => 'warning',
        'published' => 'success',
        default => 'gray',
    })
```

#### Icons

```php
use Filament\Support\Icons\Heroicon;

TextColumn::make('email')
    ->icon(Heroicon::Envelope)
    ->iconColor('primary')
```

#### Copyable

```php
TextColumn::make('email')
    ->copyable()
    ->copyMessage('Copied!')
    ->copyMessageDuration(1500)
    ->copyable(FeatureFlag::active())
```

#### Text Wrapping

```php
TextColumn::make('description')
    ->wrap()
    ->wrap(FeatureFlag::active())
```

#### Line Clamping

```php
TextColumn::make('description')
    ->wrap()
    ->lineClamp(2)
```

#### Character Limit

```php
TextColumn::make('description')
    ->limit(50)
```

#### Word Limit

```php
TextColumn::make('description')
    ->words(10)
```

#### Tooltips

```php
TextColumn::make('description')
    ->limit(50)
    ->tooltip(function (TextColumn $column): ?string {
        $state = $column->getState();

        if (strlen($state) <= $column->getCharacterLimit()) {
            return null;
        }

        return $state;
    })
```

#### Lists with Line Breaks

```php
TextColumn::make('authors.name')
    ->listWithLineBreaks()
    ->limitList(3)
    ->expandableLimitedList()
    ->expandableLimitedList(FeatureFlag::active())
```

#### Bulleted Lists

```php
TextColumn::make('authors.name')
    ->bulleted()
    ->bulleted(FeatureFlag::active())
```

#### HTML Rendering

```php
TextColumn::make('description')
    ->html()
    ->html(FeatureFlag::active())
```

#### Relationship Access

```php
TextColumn::make('author.name')
TextColumn::make('meta.title') // JSON/array column
```

#### Aggregate Counts

```php
TextColumn::make('users_count')->counts('users')

TextColumn::make('users_count')->counts([
    'users' => fn (Builder $query) => $query->where('is_active', true),
])
```

#### Vertical Alignment

```php
TextColumn::make('name')
    ->verticallyAlignStart()
    ->verticallyAlignCenter() // Default
    ->verticallyAlignEnd()

use Filament\Support\Enums\VerticalAlignment;

TextColumn::make('name')
    ->verticalAlignment(VerticalAlignment::Start)
```

#### Clickable Actions

```php
TextColumn::make('title')
    ->action(function (Post $record): void {
        $this->dispatch('open-post-edit-modal', post: $record->getKey());
    })

// With modal
use Filament\Actions\Action;

TextColumn::make('title')
    ->action(
        Action::make('select')
            ->requiresConfirmation()
            ->action(function (Post $record): void {
                $this->dispatch('select-post', post: $record->getKey());
            }),
    )
```

#### Extra Attributes

```php
TextColumn::make('slug')
    ->extraAttributes(['class' => 'slug-column'])
```

---

### IconColumn

Display icons based on column state.

#### Basic Usage

```php
use Filament\Tables\Columns\IconColumn;

IconColumn::make('status')
    ->boolean()
```

#### Dynamic Icons

```php
use Filament\Support\Icons\Heroicon;

IconColumn::make('status')
    ->icon(fn (string $state): Heroicon => match ($state) {
        'draft' => Heroicon::OutlinedPencil,
        'reviewing' => Heroicon::OutlinedClock,
        'published' => Heroicon::OutlinedCheckCircle,
    })
```

#### Static Color

```php
IconColumn::make('status')
    ->color('success')
```

#### Dynamic Color

```php
IconColumn::make('status')
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'info',
        'reviewing' => 'warning',
        'published' => 'success',
        default => 'gray',
    })
```

---

### ImageColumn

Display images from storage or URLs.

#### Basic Usage

```php
use Filament\Tables\Columns\ImageColumn;

ImageColumn::make('avatar')
```

#### Circular Images

```php
ImageColumn::make('avatar')
    ->circular()
```

#### Image Height

```php
ImageColumn::make('avatar')
    ->imageHeight(40)
```

#### Stacked Images

```php
ImageColumn::make('colleagues.avatar')
    ->circular()
    ->stacked()
    ->limit(3)
```

#### Wrapping

```php
ImageColumn::make('colleagues.avatar')
    ->circular()
    ->stacked()
    ->wrap()
```

#### Custom Limited Text Size

```php
use Filament\Support\Enums\TextSize;

ImageColumn::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText(size: TextSize::Large)
```

---

### ColorColumn

Display color swatches.

#### Basic Usage

```php
use Filament\Tables\Columns\ColorColumn;

ColorColumn::make('color')
```

#### Copyable

```php
ColorColumn::make('color')
    ->copyable()
    ->copyMessage('Copied!')
    ->copyMessageDuration(1500)
    ->copyable(FeatureFlag::active())
```

#### Wrapping

```php
ColorColumn::make('color')
    ->wrap()
```

---

### SelectColumn

Inline editable dropdown column.

#### Basic Usage

```php
use Filament\Tables\Columns\SelectColumn;

SelectColumn::make('status')
    ->options([
        'draft' => 'Draft',
        'reviewing' => 'Reviewing',
        'published' => 'Published',
    ])
```

#### Disable Specific Options

```php
SelectColumn::make('status')
    ->options([...])
    ->default('draft')
    ->disableOptionWhen(fn (string $value): bool => $value === 'published')
```

#### Native UI

```php
SelectColumn::make('status')
    ->options([...])
    ->native(false) // Use JavaScript-based select
```

#### Relationship

```php
SelectColumn::make('author_id')
    ->optionsRelationship(name: 'author', titleAttribute: 'name')
```

#### Searchable

```php
SelectColumn::make('author_id')
    ->optionsRelationship(name: 'author', titleAttribute: 'name')
    ->searchableOptions()
    ->searchableOptions(['name', 'email'])
```

#### Search Configuration

```php
SelectColumn::make('author_id')
    ->optionsRelationship(name: 'author', titleAttribute: 'name')
    ->searchableOptions()
    ->optionsSearchPrompt('Search authors by their name or email address')
    ->optionsSearchingMessage('Searching authors...')
    ->noOptionsSearchResultsMessage('No authors found.')
    ->optionsLoadingMessage('Loading authors...')
    ->optionsSearchDebounce(500)
    ->optionsLimit(20)
```

#### Custom Search Results

```php
SelectColumn::make('author_id')
    ->searchableOptions()
    ->getOptionsSearchResultsUsing(fn (string $search): array => User::query()
        ->where('name', 'like', "%{$search}%")
        ->limit(50)
        ->pluck('name', 'id')
        ->all())
    ->getOptionLabelUsing(fn ($value): ?string => User::find($value)?->name)
```

#### Validate Options

```php
SelectColumn::make('author_id')
    ->searchableOptions()
    ->getOptionsSearchResultsUsing(fn (string $search): array => Author::query()
        ->where('name', 'like', "%{$search}%")
        ->limit(50)
        ->pluck('name', 'id')
        ->all())
    ->getOptionLabelUsing(fn (string $value): ?string => Author::find($value)?->name)
```

#### Custom Query

```php
use Illuminate\Database\Eloquent\Builder;

SelectColumn::make('author_id')
    ->optionsRelationship(
        name: 'author',
        titleAttribute: 'name',
        modifyQueryUsing: fn (Builder $query) => $query->withTrashed(),
    )
```

#### Virtual Column for Labels

```php
// Migration
$table->string('full_name')->virtualAs('concat(first_name, \' \', last_name)');

// Column
SelectColumn::make('author_id')
    ->optionsRelationship(name: 'author', titleAttribute: 'full_name')
```

---

### ToggleColumn

Inline editable boolean toggle.

#### Basic Usage

```php
use Filament\Tables\Columns\ToggleColumn;

ToggleColumn::make('is_admin')
```

---

### TextInputColumn

Inline editable text field.

#### Basic Usage

```php
use Filament\Tables\Columns\TextInputColumn;

TextInputColumn::make('name')
```

#### Input Type

```php
TextInputColumn::make('background_color')
    ->type('color')
```

#### Affixes

```php
use Filament\Support\Icons\Heroicon;

TextInputColumn::make('domain')
    ->prefix('https://')
    ->suffix('.com')
    ->prefixIcon(Heroicon::GlobeAlt)
    ->suffixIcon(Heroicon::CheckCircle)
```

#### Icon Colors

```php
TextInputColumn::make('status')
    ->suffixIcon(Heroicon::CheckCircle)
    ->suffixIconColor(function ($state, $record, $column) {
        if ($state === 'active') {
            return 'success';
        }
        return 'gray';
    })
```

#### Lifecycle Hooks

```php
TextInputColumn::make('name')
    ->beforeStateUpdated(function ($record, $state) {
        // Runs before saving
    })
    ->afterStateUpdated(function ($record, $state) {
        // Runs after saving
    })
```

---

## Search Functionality

### Global Search

Enable search across the entire table:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->searchable();
}
```

### Column Search

Enable search on specific columns:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('name')
    ->searchable()
```

### Individual Column Search

Per-column search inputs:

```php
TextColumn::make('name')
    ->searchable(isIndividual: true)
```

### Disable Global Search for Column

```php
TextColumn::make('title')
    ->searchable(isIndividual: true, isGlobal: false)
```

### Search Multiple Columns

```php
TextColumn::make('full_name')
    ->searchable(['first_name', 'last_name'])
```

### Search Relationships

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->searchable(['id', 'author.id']);
}
```

### Custom Search Query

```php
use Illuminate\Database\Eloquent\Builder;

TextColumn::make('full_name')
    ->searchable(query: function (Builder $query, string $search): Builder {
        return $query
            ->where('first_name', 'like', "%{$search}%")
            ->orWhere('last_name', 'like', "%{$search}%");
    })
```

### Table-Level Custom Search

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->searchable([
            'id',
            'author.id',
            function (Builder $query, string $search): Builder {
                if (! is_numeric($search)) {
                    return $query;
                }

                return $query->whereYear('published_at', $search);
            },
        ]);
}
```

### Search on Blur

```php
public static function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->searchOnBlur();
}
```

### Disable Term Splitting

```php
public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->splitSearchTerms(false);
}
```

### Custom Search Placeholder

```php
public static function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->searchPlaceholder('Search (ID, Name)');
}
```

### Persist Search in Session

```php
public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->persistSearchInSession()
        ->persistColumnSearchesInSession();
}
```

### Laravel Scout Integration

```php
use App\Models\Post;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;

public function table(Table $table): Table
{
    return $table
        ->searchUsing(fn (Builder $query, string $search) => 
            $query->whereKey(Post::search($search)->keys())
        );
}
```

---

## Filters

### Basic Filter

```php
use Filament\Tables\Filters\Filter;
use Illuminate\Database\Eloquent\Builder;

Filter::make('is_featured')
    ->query(fn (Builder $query) => $query->where('is_featured', true))
```

### Select Filter

```php
use Filament\Tables\Filters\SelectFilter;

SelectFilter::make('status')
    ->options([
        'draft' => 'Draft',
        'reviewing' => 'Reviewing',
        'published' => 'Published',
    ])
```

### Custom Attribute

```php
SelectFilter::make('status')
    ->options([...])
    ->attribute('status_id')
```

### Relationship Filter

```php
SelectFilter::make('author')
    ->relationship('author', 'name')
    ->searchable()
    ->preload()
```

### Ternary Filter

```php
use Filament\Tables\Filters\TernaryFilter;

TernaryFilter::make('is_admin')

TernaryFilter::make('email_verified_at')
    ->nullable()

TernaryFilter::make('verified')
    ->nullable()
    ->attribute('status_id')
```

### QueryBuilder Filter

```php
use Filament\QueryBuilder\Constraints\TextConstraint;
use Filament\QueryBuilder\Constraints\BooleanConstraint;
use Filament\QueryBuilder\Constraints\SelectConstraint;

// Text constraint
TextConstraint::make('name')
TextConstraint::make('creator.name') // Relationship

// Boolean constraint
BooleanConstraint::make('is_visible')
BooleanConstraint::make('creator.is_admin')

// Select constraint
SelectConstraint::make('status')
    ->options([
        'draft' => 'Draft',
        'reviewing' => 'Reviewing',
        'published' => 'Published',
    ])
    ->searchable()
```

### Nullable Constraints

```php
TextConstraint::make('name')
    ->nullable()
```

### Filter Layouts

```php
use Filament\Tables\Enums\FiltersLayout;
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->filters([...])
        ->filtersLayout(FiltersLayout::AboveContentCollapsible);
}
```

### Filter Grid Columns

```php
public function table(Table $table): Table
{
    return $table
        ->filters([...])
        ->filtersFormColumns(3);
}
```

### Customize Filter Actions

```php
use Filament\Actions\Action;

public function table(Table $table): Table
{
    return $table
        ->filters([...])
        ->filtersTriggerAction(
            fn (Action $action) => $action
                ->button()
                ->label('Filter'),
        )
        ->filtersApplyAction(
            fn (Action $action) => $action
                ->link()
                ->label('Save filters to table'),
        );
}
```

---

## Sorting

### Enable Sorting

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('name')
    ->sortable()
```

### Sort by Multiple Columns

```php
TextColumn::make('full_name')
    ->sortable(['first_name', 'last_name'])
```

### Custom Sort Query

```php
use Illuminate\Database\Eloquent\Builder;

TextColumn::make('full_name')
    ->sortable(query: function (Builder $query, string $direction): Builder {
        return $query
            ->orderBy('last_name', $direction)
            ->orderBy('first_name', $direction);
    })
```

### Default Sort

By column name:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->defaultSort('stock', direction: 'desc');
}
```

By query callback:

```php
use Illuminate\Database\Eloquent\Builder;

public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->defaultSort(function (Builder $query): Builder {
            return $query->orderBy('stock');
        });
}
```

### Persist Sort

```php
public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->persistSortInSession();
}
```

---

## Actions

### Record Actions

Actions displayed for each row:

```php
use App\Models\Post;
use Filament\Actions\Action;

public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->recordActions([
            Action::make('feature')
                ->action(function (Post $record) {
                    $record->is_featured = true;
                    $record->save();
                })
                ->hidden(fn (Post $record): bool => $record->is_featured),
            Action::make('unfeature')
                ->action(function (Post $record) {
                    $record->is_featured = false;
                    $record->save();
                })
                ->visible(fn (Post $record): bool => $record->is_featured),
        ]);
}
```

### Record Action Position

```php
use Filament\Tables\Enums\RecordActionsPosition;

public function table(Table $table): Table
{
    return $table
        ->recordActions([...], position: RecordActionsPosition::BeforeColumns);
}

// Or before checkbox
public function table(Table $table): Table
{
    return $table
        ->recordActions([...], position: RecordActionsPosition::BeforeCells);
}
```

### Toolbar Actions

Actions in the table toolbar:

```php
public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            // Actions here
        ]);
}
```

---

## Bulk Actions

### Basic Bulk Action

```php
use Filament\Actions\BulkAction;
use Illuminate\Database\Eloquent\Collection;

BulkAction::make('delete')
    ->requiresConfirmation()
    ->action(fn (Collection $records) => $records->each->delete())
```

### Grouped Bulk Actions

```php
use Filament\Actions\BulkAction;
use Filament\Actions\BulkActionGroup;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            BulkActionGroup::make([
                BulkAction::make('delete')
                    ->requiresConfirmation()
                    ->action(fn (Collection $records) => $records->each->delete()),
                BulkAction::make('forceDelete')
                    ->requiresConfirmation()
                    ->action(fn (Collection $records) => $records->each->forceDelete()),
            ]),
        ]);
}
```

### Shorthand for Grouped Actions

```php
public function table(Table $table): Table
{
    return $table
        ->groupedBulkActions([
            BulkAction::make('delete')
                ->requiresConfirmation()
                ->action(fn (Collection $records) => $records->each->delete()),
        ]);
}
```

### Deselect After Completion

```php
BulkAction::make('delete')
    ->action(fn (Collection $records) => $records->each->delete())
    ->deselectRecordsAfterCompletion()
```

### Conditional Record Selection

```php
use Illuminate\Database\Eloquent\Model;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([...])
        ->checkIfRecordIsSelectableUsing(
            fn (Model $record): bool => $record->status === Status::Enabled,
        );
}
```

---

## Pagination

### Default Pagination

Tables are paginated by default with options for 10, 25, 50 records per page.

### Custom Pagination Options

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->paginationPageOptions([10, 25, 50, 100]);
}
```

### Paginated While Reordering

```php
public function table(Table $table): Table
{
    return $table
        ->paginatedWhileReordering();
}
```

---

## Reordering

### Enable Reordering

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->reorderable('sort');
}
```

### Different Column Name

```php
public function table(Table $table): Table
{
    return $table
        ->reorderable('order_column');
}
```

### Conditional Reordering

```php
public function table(Table $table): Table
{
    return $table
        ->reorderable('sort', auth()->user()->isAdmin());
}
```

### Reordering Direction

```php
public function table(Table $table): Table
{
    return $table
        ->reorderable('sort', direction: 'desc');
}
```

### Customize Reorder Trigger

```php
use Filament\Actions\Action;

public function table(Table $table): Table
{
    return $table
        ->reorderRecordsTriggerAction(
            fn (Action $action, bool $isReordering) => $action
                ->button()
                ->label($isReordering ? 'Disable reordering' : 'Enable reordering'),
        );
}
```

---

## Column Management

### Toggleable Columns

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('email')
    ->toggleable()

TextColumn::make('id')
    ->toggleable(isToggledHiddenByDefault: true)
```

### Reorderable Columns

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->reorderableColumns();
}
```

### Live Column Manager

```php
public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->reorderableColumns()
        ->deferColumnManager(false);
}
```

### Customize Column Manager

```php
use Filament\Actions\Action;

public function table(Table $table): Table
{
    return $table
        ->filters([...])
        ->columnManagerTriggerAction(
            fn (Action $action) => $action
                ->button()
                ->label('Column Manager'),
        );
}
```

### Column Manager Reset Position

```php
use Filament\Tables\Enums\ColumnManagerResetActionPosition;

public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->columnManagerResetActionPosition(ColumnManagerResetActionPosition::Footer);
}
```

---

## Custom Data Sources

### Using Collections

```php
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;
use Illuminate\Support\Collection;

public function table(Table $table): Table
{
    return $table
        ->records(function (): Collection {
            return collect([
                1 => ['title' => 'First item'],
                2 => ['title' => 'Second item'],
                3 => ['title' => 'Third item'],
            ]);
        })
        ->columns([
            TextColumn::make('title'),
        ]);
}
```

### Using Arrays

```php
public function table(Table $table): Table
{
    return $table
        ->records(function (): array {
            return [
                1 => ['title' => 'First item', 'slug' => 'first-item', 'is_featured' => true],
                2 => ['title' => 'Second item', 'slug' => 'second-item', 'is_featured' => false],
                3 => ['title' => 'Third item', 'slug' => 'third-item', 'is_featured' => true],
            ];
        })
        ->columns([
            TextColumn::make('title'),
            TextColumn::make('slug'),
        ]);
}
```

### Custom Column State for Arrays

```php
TextColumn::make('is_featured')
    ->state(function (array $record): string {
        return $record['is_featured'] ? 'Featured' : 'Not featured';
    })
```

### With Search

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Str;

public function table(Table $table): Table
{
    return $table
        ->records(
            fn (?string $search): Collection => collect([
                1 => ['title' => 'First item'],
                2 => ['title' => 'Second item'],
                3 => ['title' => 'Third item'],
            ])->when(
                filled($search),
                fn (Collection $data): Collection => $data->filter(
                    fn (array $record): bool => str_contains(
                        Str::lower($record['title']),
                        Str::lower($search),
                    ),
                ),
            )
        )
        ->columns([
            TextColumn::make('title'),
        ])
        ->searchable();
}
```

### Individual Column Search

```php
use Illuminate\Support\Str;

public function table(Table $table): Table
{
    return $table
        ->records(
            fn (array $columnSearches): Collection => collect([
                1 => ['title' => 'First item'],
                2 => ['title' => 'Second item'],
                3 => ['title' => 'Third item'],
            ])->when(
                filled($columnSearches['title'] ?? null),
                fn (Collection $data) => $data->filter(
                    fn (array $record): bool => str_contains(
                        Str::lower($record['title']),
                        Str::lower($columnSearches['title'])
                    ),
                ),
            )
        )
        ->columns([
            TextColumn::make('title')
                ->searchable(isIndividual: true),
        ]);
}
```

### External API Example

```php
use Filament\Tables\Columns\ImageColumn;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Filters\SelectFilter;
use Filament\Tables\Table;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Str;

public function table(Table $table): Table
{
    $baseUrl = 'https://dummyjson.com/';

    return $table
        ->records(function (
            ?string $sortColumn,
            ?string $sortDirection,
            ?string $search,
            array $filters,
            int $page,
            int $recordsPerPage
        ) use ($baseUrl): LengthAwarePaginator {
            $category = $filters['category']['value'] ?? null;

            $endpoint = match (true) {
                filled($search) => 'products/search',
                filled($category) => "products/category/{$category}",
                default => 'products',
            };

            $skip = ($page - 1) * $recordsPerPage;

            $params = [
                'limit' => $recordsPerPage,
                'skip' => $skip,
                'select' => 'id,title,brand,category,thumbnail,price,sku,stock',
            ];

            if (filled($search)) {
                $params['q'] = $search;
            }

            if ($endpoint === 'products' && $sortColumn) {
                $params['sortBy'] = $sortColumn;
                $params['order'] = $sortDirection ?? 'asc';
            }

            $response = Http::baseUrl($baseUrl)
                ->get($endpoint, $params)
                ->collect();

            return new LengthAwarePaginator(
                items: $response['products'],
                total: $response['total'],
                perPage: $recordsPerPage,
                currentPage: $page
            );
        })
        ->columns([
            ImageColumn::make('thumbnail')
                ->label('Image'),
            TextColumn::make('title')
                ->sortable(),
            TextColumn::make('brand')
                ->state(fn (array $record): string => Str::title($record['brand'] ?? 'Unknown')),
            TextColumn::make('category')
                ->formatStateUsing(fn (string $state): string => Str::headline($state)),
            TextColumn::make('price')
                ->money(),
            TextColumn::make('sku')
                ->label('SKU'),
            TextColumn::make('stock')
                ->label('Stock')
                ->sortable(),
        ])
        ->filters([
            SelectFilter::make('category')
                ->label('Category')
                ->options(fn (): Collection => Http::baseUrl($baseUrl)
                    ->get('products/categories')
                    ->collect()
                    ->pluck('name', 'slug')
                ),
        ])
        ->searchable();
}
```

### Bulk Actions with Custom Data

```php
use Filament\Actions\BulkAction;
use Illuminate\Support\Arr;

public function table(Table $table): Table
{
    return $table
        ->records(function (): array {
            // Return array data
        })
        ->resolveSelectedRecordsUsing(function (array $keys): array {
            return Arr::only([
                1 => ['title' => 'First item', ...],
                2 => ['title' => 'Second item', ...],
                3 => ['title' => 'Third item', ...],
            ], $keys);
        })
        ->columns([...])
        ->recordActions([
            BulkAction::make('feature')
                ->requiresConfirmation()
                ->action(function (Collection $records): void {
                    // Process records
                }),
        ]);
}
```

### Handle Deselected Keys

```php
public function table(Table $table): Table
{
    return $table
        ->records(function (): array {
            // ...
        })
        ->resolveSelectedRecordsUsing(function (
            array $keys,
            bool $isTrackingDeselectedKeys,
            array $deselectedKeys
        ): array {
            $records = [
                1 => ['title' => 'First item', ...],
                2 => ['title' => 'Second item', ...],
                3 => ['title' => 'Third item', ...],
            ];
            
            if ($isTrackingDeselectedKeys) {
                return Arr::except($records, $deselectedKeys);
            }
            
            return Arr::only($records, $keys);
        })
        ->columns([...])
        ->recordActions([...]);
}
```

---

## Layout Components

### Collapsible Panels

```php
use Filament\Support\Enums\FontWeight;
use Filament\Tables\Columns\Layout\Panel;
use Filament\Tables\Columns\Layout\Split;
use Filament\Tables\Columns\Layout\Stack;
use Filament\Tables\Columns\ImageColumn;
use Filament\Tables\Columns\TextColumn;

[
    Split::make([
        ImageColumn::make('avatar')
            ->circular(),
        TextColumn::make('name')
            ->weight(FontWeight::Bold)
            ->searchable()
            ->sortable(),
    ]),
    Panel::make([
        Stack::make([
            TextColumn::make('phone')
                ->icon('heroicon-m-phone'),
            TextColumn::make('email')
                ->icon('heroicon-m-envelope'),
        ]),
    ])->collapsible(),
]
```

---

## Global Configuration

Configure defaults for all tables:

```php
use Filament\Tables\Enums\FiltersLayout;
use Filament\Tables\Table;

Table::configureUsing(function (Table $table): void {
    $table
        ->reorderableColumns()
        ->filtersLayout(FiltersLayout::AboveContentCollapsible)
        ->paginationPageOptions([10, 25, 50]);
});
```

Add columns globally:

```php
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;

Table::configureUsing(function (Table $table) {
    $table
        ->pushColumns([
            TextColumn::make('created_at')
                ->label('Created')
                ->sortable()
                ->toggleable(isToggledHiddenByDefault: true),

            TextColumn::make('updated_at')
                ->label('Updated')
                ->sortable()
                ->toggleable(isToggledHiddenByDefault: true),
        ]);
});
```

Configure columns globally:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::configureUsing(function (TextColumn $column): void {
    $column->toggleable();
});
```

---

## Best Practices

### 1. **Use Searchable Wisely**
Only make columns searchable when users need to search them.

```php
// Good - searchable on important fields
TextColumn::make('title')
    ->searchable()

// Avoid - unnecessary search on static data
TextColumn::make('status')
    ->searchable() // Not needed for limited options
```

### 2. **Optimize Large Datasets**
Use pagination, deferred loading, and limit search results.

```php
SelectColumn::make('author_id')
    ->searchableOptions()
    ->optionsLimit(50) // Limit results
    ->optionsSearchDebounce(500) // Debounce search
```

### 3. **Provide Clear Labels**
Use descriptive column labels for better UX.

```php
TextColumn::make('created_at')
    ->label('Created Date')
    ->dateTime()
```

### 4. **Use Badges for Status**
Visual indicators improve data scanning.

```php
TextColumn::make('status')
    ->badge()
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'gray',
        'published' => 'success',
        'rejected' => 'danger',
    })
```

### 5. **Leverage Relationships**
Use relationship methods instead of manual queries.

```php
// Good
SelectColumn::make('author_id')
    ->optionsRelationship(name: 'author', titleAttribute: 'name')

// Less ideal
SelectColumn::make('author_id')
    ->options(User::pluck('name', 'id'))
```

### 6. **Conditional Visibility**
Hide columns when appropriate using toggleable.

```php
TextColumn::make('id')
    ->toggleable(isToggledHiddenByDefault: true)

TextColumn::make('updated_at')
    ->toggleable(isToggledHiddenByDefault: true)
```

### 7. **Use Bulk Actions for Efficiency**
Group related bulk operations.

```php
BulkActionGroup::make([
    BulkAction::make('delete')
        ->requiresConfirmation()
        ->action(fn (Collection $records) => $records->each->delete()),
    BulkAction::make('archive')
        ->action(fn (Collection $records) => $records->each->archive()),
])
```

### 8. **Persist User Preferences**
Save search and sort preferences.

```php
public function table(Table $table): Table
{
    return $table
        ->persistSearchInSession()
        ->persistSortInSession();
}
```

### 9. **Custom Column States for Arrays**
When using array data, define custom states.

```php
TextColumn::make('is_featured')
    ->state(function (array $record): string {
        return $record['is_featured'] ? 'Featured' : 'Not featured';
    })
```

### 10. **Global Configuration for Consistency**
Set defaults across all tables.

```php
// In AppServiceProvider
Table::configureUsing(function (Table $table): void {
    $table
        ->paginationPageOptions([10, 25, 50, 100])
        ->persistSearchInSession();
});
```

---

## Troubleshooting

### Columns Not Displaying

**Problem:** Table columns are not visible.

**Solutions:**
1. Check if columns are toggled hidden by default
2. Verify column manager settings
3. Ensure data is being returned

```php
// Make sure column is visible
TextColumn::make('name')
    ->toggleable(isToggledHiddenByDefault: false)
```

---

### Search Not Working

**Problem:** Search functionality doesn't filter results.

**Solutions:**
1. Enable `searchable()` on table
2. Mark columns as searchable
3. Check Scout configuration for Scout-based search

```php
// Enable table search
public function table(Table $table): Table
{
    return $table
        ->searchable();
}

// Mark columns searchable
TextColumn::make('title')
    ->searchable()
```

---

### Slow Performance

**Problem:** Table loading is slow.

**Solutions:**
1. Add eager loading for relationships
2. Limit search results
3. Use pagination appropriately
4. Avoid unnecessary `preload()` on selects

```php
// Eager load relationships
public static function getEloquentQuery(): Builder
{
    return parent::getEloquentQuery()->with(['author', 'category']);
}

// Limit search results
SelectColumn::make('author_id')
    ->searchableOptions()
    ->optionsLimit(50)
```

---

### Sorting Not Working

**Problem:** Column sorting doesn't work.

**Solutions:**
1. Enable `sortable()` on column
2. For virtual columns, provide custom sort query
3. Check database indexes

```php
// Enable sorting
TextColumn::make('name')
    ->sortable()

// Custom sort for virtual columns
TextColumn::make('full_name')
    ->sortable(query: function (Builder $query, string $direction): Builder {
        return $query
            ->orderBy('last_name', $direction)
            ->orderBy('first_name', $direction);
    })
```

---

### Bulk Actions Not Showing

**Problem:** Bulk actions aren't visible.

**Solutions:**
1. Wrap bulk actions in `BulkActionGroup`
2. Check if records are selectable
3. Verify action visibility conditions

```php
// Properly configure bulk actions
public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            BulkActionGroup::make([
                BulkAction::make('delete')
                    ->action(fn (Collection $records) => $records->each->delete()),
            ]),
        ]);
}
```

---

### Filters Not Applying

**Problem:** Filters don't affect table results.

**Solutions:**
1. Verify filter query logic
2. Check filter attribute mapping
3. Ensure filter is not hidden

```php
// Correct filter configuration
Filter::make('is_featured')
    ->query(fn (Builder $query): Builder => $query->where('is_featured', true))
```

---

### Custom Data Source Issues

**Problem:** Custom array/collection data isn't working correctly.

**Solutions:**
1. Define custom column states for array records
2. Implement `resolveSelectedRecordsUsing()` for bulk actions
3. Handle search/filter parameters in records callback

```php
// Custom column state
TextColumn::make('title')
    ->state(fn (array $record): string => $record['title'])

// Resolve selected records
->resolveSelectedRecordsUsing(function (array $keys): array {
    return Arr::only($allRecords, $keys);
})
```

---

## Cross-References

### Related Topics
- [FORMS.md](./FORMS.md) - Form components and validation
- [ACTIONS.md](./ACTIONS.md) - Table actions and bulk actions
- [RESOURCES.md](./RESOURCES.md) - Resource table integration
- [FILTERS.md](./FILTERS.md) - Advanced filter patterns
- [SCHEMAS.md](./SCHEMAS.md) - Layout components

### External Resources
- [FilamentPHP Tables Documentation](https://filamentphp.com/docs/4.x/tables)
- [Laravel Eloquent](https://laravel.com/docs/eloquent)
- [Laravel Scout](https://laravel.com/docs/scout)

---

**End of Tables Reference**
