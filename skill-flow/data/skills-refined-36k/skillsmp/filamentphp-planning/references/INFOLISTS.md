# FilamentPHP Infolists Reference

## Table of Contents

- [Overview](#overview)
- [Basic Usage](#basic-usage)
- [TextEntry Component](#textentry-component)
- [IconEntry Component](#iconentry-component)
- [ImageEntry Component](#imageentry-component)
- [ColorEntry Component](#colorentry-component)
- [KeyValueEntry Component](#keyvalueentry-component)
- [RepeatableEntry Component](#repeatableentry-component)
- [Layout & Styling](#layout--styling)
- [Accessing Data](#accessing-data)
- [Custom Entries](#custom-entries)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Cross-References](#cross-references)

---

## Overview

Infolists provide read-only data display components in FilamentPHP. They're ideal for view pages, dashboards, and anywhere you need to present information without allowing edits.

### When to Use Infolists

- Displaying record details on view pages
- Creating read-only dashboards
- Showing related data without edit capabilities
- Presenting formatted data with custom styling
- Building information panels in modals

### Key Concepts

- **Entry Components**: Read-only display elements (TextEntry, IconEntry, etc.)
- **Schema**: Structure defining how data is displayed
- **State**: The actual data being displayed
- **Relationships**: Accessing related model data with dot notation
- **Custom Entries**: Building reusable display components

---

## Basic Usage

### Defining an Infolist

Create an infolist for a FilamentPHP resource view page:

```php
use Filament\Infolists;
use Filament\Schemas\Schema;

public static function infolist(Schema $schema): Schema
{
    return $schema
        ->components([
            Infolists\Components\TextEntry::make('name'),
            Infolists\Components\TextEntry::make('email'),
            Infolists\Components\TextEntry::make('notes')
                ->columnSpanFull(),
        ]);
}
```

### Passing Eloquent Model Data

Populate an infolist with an Eloquent model:

```php
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Schema;

public function productInfolist(Schema $schema): Schema
{
    return $schema
        ->record($this->product)
        ->components([
            TextEntry::make('name'),
            TextEntry::make('category.name'),
            // ...
        ]);
}
```

### Passing Array Data

Use array data instead of Eloquent models:

```php
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Schema;

public function productInfolist(Schema $schema): Schema
{
    return $schema
        ->constantState([
            'name' => 'MacBook Pro',
            'category' => [
                'name' => 'Laptops',
            ],
            // ...
        ])
        ->components([
            TextEntry::make('name'),
            TextEntry::make('category.name'),
            // ...
        ]);
}
```

---

## TextEntry Component

### Basic TextEntry

Display a simple text value:

```php
use Filament\Infolists\Components\TextEntry;

TextEntry::make('title')
```

### Accessing Relationship Data

Use dot notation to access related model attributes:

```php
TextEntry::make('author.name')
```

### Accessing JSON/Array Data

Access JSON column keys:

```php
TextEntry::make('meta.title')
```

### Custom State

Override the default state:

```php
TextEntry::make('title')
    ->state('Hello, world!')
```

Inject current state:

```php
TextEntry::make('currentUserEmail')
    ->state(fn (): string => auth()->user()->email)
```

### Default Values

Set a fallback value when state is empty:

```php
TextEntry::make('title')
    ->default('Untitled')
```

### Placeholder Text

Display placeholder when value is empty:

```php
TextEntry::make('title')
    ->placeholder('Untitled')
```

### Formatting State

Transform the displayed value:

```php
TextEntry::make('status')
    ->formatStateUsing(fn (string $state): string => __("statuses.{$state}"))
```

### HTML & Markdown Rendering

Render HTML content:

```php
TextEntry::make('description')
    ->html()
```

Conditionally render HTML:

```php
TextEntry::make('description')
    ->html(FeatureFlag::active())
```

Render Markdown:

```php
TextEntry::make('description')
    ->markdown()
```

Conditionally render Markdown:

```php
TextEntry::make('description')
    ->markdown(FeatureFlag::active())
```

Render raw HTML (unsafe):

```php
use Illuminate\Support\HtmlString;

TextEntry::make('description')
    ->formatStateUsing(fn (string $state): HtmlString => new HtmlString($state))
```

Using Blade views:

```php
use Illuminate\Contracts\View\View;

TextEntry::make('description')
    ->formatStateUsing(fn (string $state): View => view(
        'filament.infolists.components.description-entry-content',
        ['state' => $state],
    ))
```

### Text Truncation

Limit displayed text length:

```php
TextEntry::make('description')
    ->limit(50)
```

Custom truncation suffix:

```php
TextEntry::make('description')
    ->limit(50, end: ' (more)')
```

Limit by words:

```php
TextEntry::make('description')
    ->words(10)
```

Custom word truncation suffix:

```php
TextEntry::make('description')
    ->words(10, end: ' (more)')
```

### Badge Styling

Display as a badge:

```php
TextEntry::make('status')
    ->badge()
```

Conditionally display as badge:

```php
TextEntry::make('status')
    ->badge(FeatureFlag::active())
```

Badge with dynamic color:

```php
TextEntry::make('status')
    ->badge()
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'gray',
        'reviewing' => 'warning',
        'published' => 'success',
        'rejected' => 'danger',
    })
```

### Text Color

Set static color:

```php
TextEntry::make('status')
    ->color('primary')
```

Dynamic color calculation:

```php
TextEntry::make('status')
    ->color(function ($state, $get, $record, $component, $livewire, $model, $operation) {
        // Dynamic color calculation logic
    })
```

### Icons

Add icon to entry:

```php
use Filament\Support\Icons\Heroicon;

TextEntry::make('email')
    ->icon(Heroicon::Envelope)
```

Customize icon color:

```php
TextEntry::make('email')
    ->icon(Heroicon::Envelope)
    ->iconColor('primary')
```

### Numeric Formatting

Format as number:

```php
TextEntry::make('stock')
    ->numeric()
```

Custom decimal places:

```php
TextEntry::make('stock')
    ->numeric(decimalPlaces: 0)
```

### Lists

Display array as list with line breaks:

```php
TextEntry::make('authors.name')
    ->listWithLineBreaks()
```

Conditionally use line breaks:

```php
TextEntry::make('authors.name')
    ->listWithLineBreaks(FeatureFlag::active())
```

Display as bulleted list:

```php
TextEntry::make('authors.name')
    ->bulleted()
```

Limit list items:

```php
TextEntry::make('authors.name')
    ->listWithLineBreaks()
    ->limitList(3)
```

Expandable limited list:

```php
TextEntry::make('authors.name')
    ->listWithLineBreaks()
    ->limitList(3)
    ->expandableLimitedList()
```

Conditionally expandable:

```php
TextEntry::make('authors.name')
    ->listWithLineBreaks()
    ->limitList(3)
    ->expandableLimitedList(FeatureFlag::active())
```

### Separator for Tags

Split comma-separated values into badges:

```php
TextEntry::make('tags')
    ->badge()
    ->separator(',')
```

### URL Links

Set static URL:

```php
TextEntry::make('title')
    ->url('/about/titles')
```

Dynamic URL from record:

```php
TextEntry::make('title')
    ->url(fn (Post $record): string => route('posts.edit', ['post' => $record]))
```

Using resource URL:

```php
use App\Filament\Posts\PostResource;

TextEntry::make('title')
    ->url(fn (Post $record): string => PostResource::getUrl('edit', ['record' => $record]))
```

Open in new tab:

```php
TextEntry::make('title')
    ->url(fn (Post $record): string => PostResource::getUrl('edit', ['record' => $record]))
    ->openUrlInNewTab()
```

Conditionally open in new tab:

```php
TextEntry::make('title')
    ->url(fn (Post $record): string => PostResource::getUrl('edit', ['record' => $record]))
    ->openUrlInNewTab(FeatureFlag::active())
```

### Tooltips

Add static tooltip:

```php
TextEntry::make('title')
    ->tooltip('Shown at the top of the page')
```

### Date Tooltips

Show formatted dates in tooltips:

```php
TextEntry::make('created_at')
    ->since()
    ->dateTooltip(); // Accepts custom PHP date formatting string

TextEntry::make('created_at')
    ->since()
    ->dateTimeTooltip();

TextEntry::make('created_at')
    ->since()
    ->isoDateTooltip(); // Accepts custom Carbon macro format string

TextEntry::make('created_at')
    ->dateTime()
    ->sinceTooltip();
```

### Aggregates

Display relationship aggregates:

```php
TextEntry::make('users_count')->count('users')
TextEntry::make('users_avg_age')->avg('users', 'age')
TextEntry::make('users_sum_votes')->sum('users', 'votes')
TextEntry::make('users_min_score')->min('users', 'score')
TextEntry::make('users_max_score')->max('users', 'score')
```

---

## IconEntry Component

### Basic Boolean Icon

Display check/X icon based on boolean value:

```php
use Filament\Infolists\Components\IconEntry;

IconEntry::make('is_featured')
    ->boolean()
```

### Custom Icon Colors

Set static color:

```php
IconEntry::make('status')
    ->color('success')
```

Dynamic color based on state:

```php
IconEntry::make('status')
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'info',
        'reviewing' => 'warning',
        'published' => 'success',
        default => 'gray',
    })
```

---

## ImageEntry Component

### Basic Image Display

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('logo')
```

### Circular Images

```php
ImageEntry::make('avatar')
    ->circular()
```

### Custom Image Height

```php
ImageEntry::make('logo')
    ->imageHeight(40)
```

### Stacked Images

Display multiple images as overlapping stacks:

```php
ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
```

Conditionally stacked:

```php
ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked(FeatureFlag::active())
```

Customize overlap:

```php
ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->overlap(2) // 0-8
```

### Limiting Displayed Images

```php
ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
```

Show remaining count:

```php
ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText()
```

Conditionally show remaining:

```php
ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText(FeatureFlag::active())
```

Custom remaining text size:

```php
use Filament\Support\Enums\TextSize;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText(size: TextSize::Large)
```

### Extra Image Attributes

Add HTML attributes to `<img>` element:

```php
ImageEntry::make('logo')
    ->extraImgAttributes([
        'alt' => 'Logo',
        'loading' => 'lazy',
    ])
```

---

## ColorEntry Component

### Basic Color Display

```php
use Filament\Infolists\Components\ColorEntry;

ColorEntry::make('color')
```

Supports HEX, HSL, RGB, and RGBA color formats.

---

## KeyValueEntry Component

### Basic Key-Value Display

```php
use Filament\Infolists\Components\KeyValueEntry;

KeyValueEntry::make('meta')
```

Expected data structure:

```php
[
    'description' => 'Filament is a collection of Laravel packages',
    'og:type' => 'website',
    'og:site_name' => 'Filament',
]
```

### Custom Column Labels

```php
KeyValueEntry::make('meta')
    ->keyLabel('Property name')
    ->valueLabel('Property value')
```

---

## RepeatableEntry Component

### Basic Repeatable Entry

Display nested data structures:

```php
use Filament\Infolists\Components\RepeatableEntry;
use Filament\Infolists\Components\TextEntry;

RepeatableEntry::make('comments')
    ->schema([
        TextEntry::make('author.name'),
        TextEntry::make('title'),
        TextEntry::make('content')
            ->columnSpan(2),
    ])
    ->columns(2)
```

Expected data structure:

```json
[
    {
        "author": {"name": "Jane Doe"},
        "title": "Wow!",
        "content": "Lorem ipsum..."
    },
    {
        "author": {"name": "John Doe"},
        "title": "This isn't working. Help!",
        "content": "Lorem ipsum..."
    }
]
```

### Grid Layout

Display items in a grid:

```php
RepeatableEntry::make('comments')
    ->schema([
        // ...
    ])
    ->grid(2)
```

### Container Styling

Remove card-style container:

```php
RepeatableEntry::make('comments')
    ->schema([
        // ...
    ])
    ->contained(false)
```

### Table Layout

Display as a table:

```php
use Filament\Infolists\Components\IconEntry;
use Filament\Infolists\Components\RepeatableEntry;
use Filament\Infolists\Components\RepeatableEntry\TableColumn;
use Filament\Infolists\Components\TextEntry;

RepeatableEntry::make('comments')
    ->table([
        TableColumn::make('Author'),
        TableColumn::make('Title'),
        TableColumn::make('Published'),
    ])
    ->schema([
        TextEntry::make('author.name'),
        TextEntry::make('title'),
        IconEntry::make('is_published')
            ->boolean(),
    ])
```

### Table Column Configuration

Hide header label:

```php
TableColumn::make('Name')
    ->hiddenHeaderLabel()
```

Wrap header text:

```php
TableColumn::make('Name')
    ->wrapHeader()
```

Set fixed column width:

```php
TableColumn::make('Name')
    ->width('200px')
```

---

## Layout & Styling

### Labels

Set custom label:

```php
TextEntry::make('name')
    ->label('Full name')
```

Translatable label:

```php
TextEntry::make('name')
    ->label(__('entries.name'))
```

Hide label:

```php
TextEntry::make('name')
    ->hiddenLabel()
```

Conditionally hide label:

```php
TextEntry::make('name')
    ->hiddenLabel(FeatureFlag::active())
```

### Inline Labels

Display label inline with entry:

```php
TextEntry::make('name')
    ->inlineLabel()
```

Conditionally inline:

```php
TextEntry::make('name')
    ->inlineLabel(FeatureFlag::active())
```

Apply to entire schema:

```php
use Filament\Schemas\Schema;

public function infolist(Schema $schema): Schema
{
    return $schema
        ->inlineLabel()
        ->components([
            // ...
        ]);
}
```

Apply to section:

```php
use Filament\Infolists\Components\TextInput;
use Filament\Schemas\Components\Section;

Section::make('Details')
    ->inlineLabel()
    ->schema([
        TextInput::make('name'),
        TextInput::make('email'),
        TextInput::make('phone'),
    ])
```

Opt-out individual entry:

```php
use Filament\Infolists\Components\TextInput;
use Filament\Schemas\Components\Section;

Section::make('Details')
    ->inlineLabel()
    ->schema([
        TextInput::make('name'),
        TextInput::make('email'),
        TextInput::make('phone')
            ->inlineLabel(false),
    ])
```

### Content Slots

Add content before label:

```php
use Filament\Schemas\Components\Icon;
use Filament\Support\Icons\Heroicon;

TextEntry::make('name')
    ->beforeLabel(Icon::make(Heroicon::Star))
```

Add content after label:

```php
TextEntry::make('name')
    ->afterLabel([
        Icon::make(Heroicon::Star),
        'This is content after the label',
    ])
```

Add content above label:

```php
TextEntry::make('name')
    ->aboveLabel([
        Icon::make(Heroicon::Star),
        'This is content above the label',
    ])
```

Add content below label:

```php
TextEntry::make('name')
    ->belowLabel([
        Icon::make(Heroicon::Star),
        'This is content below the label',
    ])
```

Add content before entry:

```php
TextEntry::make('name')
    ->beforeContent(Icon::make(Heroicon::Star))
```

Add content after entry:

```php
TextEntry::make('name')
    ->afterContent(Icon::make(Heroicon::Star))
```

Add content above entry:

```php
TextEntry::make('name')
    ->aboveContent([
        Icon::make(Heroicon::Star),
        'This is content above the entry',
    ])
```

Add content below entry:

```php
TextEntry::make('name')
    ->belowContent('This is the user\'s full name.')
```

Using schema components:

```php
use Filament\Schemas\Components\Text;
use Filament\Support\Enums\FontWeight;

TextEntry::make('name')
    ->belowContent(Text::make('This is the user\'s full name.')->weight(FontWeight::Bold))
```

Using actions:

```php
use Filament\Actions\Action;

TextEntry::make('name')
    ->belowContent(Action::make('generate'))
```

### Content Alignment

Align to end:

```php
use Filament\Schemas\Schema;

TextEntry::make('name')
    ->belowContent(Schema::end([
        Icon::make(Heroicon::InformationCircle),
        'Content',
        Action::make('generate'),
    ]))
```

Align to start:

```php
TextEntry::make('name')
    ->afterLabel(Schema::start([
        Icon::make(Heroicon::Star),
        'Content',
    ]))
```

Space between:

```php
TextEntry::make('name')
    ->belowContent(Schema::between([
        Icon::make(Heroicon::InformationCircle),
        'Content',
        Action::make('generate'),
    ]))
```

Using Flex for grouping:

```php
use Filament\Schemas\Components\Flex;

TextEntry::make('name')
    ->belowContent(Schema::between([
        Flex::make([
            Icon::make(Heroicon::InformationCircle)
                ->grow(false),
            'Content',
        ]),
        Action::make('generate'),
    ]))
```

### HTML Attributes

Add extra attributes to entry wrapper:

```php
TextEntry::make('slug')
    ->extraEntryWrapperAttributes(['class' => 'components-locked'])
```

Dynamic attributes:

```php
TextEntry::make('name')
    ->extraEntryWrapperAttributes(fn (string $state): array => ['data-value' => $state])
```

Merge attributes:

```php
TextEntry::make('slug')
    ->extraEntryWrapperAttributes(['class' => 'first-class'], merge: true)
    ->extraEntryWrapperAttributes(['class' => 'second-class'], merge: true)
```

Add attributes to entry itself:

```php
TextEntry::make('slug')
    ->extraAttributes(['class' => 'bg-gray-200'])
```

---

## Accessing Data

### Injecting Current Record

```php
use Illuminate\Database\Eloquent\Model;

function (?Model $record) {
    // Access the Eloquent record
}
```

### Injecting Entry State

```php
function (string $state) {
    // Access the entry's current value
}
```

### Injecting Entry Component

```php
use Filament\Infolists\Components\Entry;

function (Entry $component) {
    // Access the Entry component instance
}
```

### Get Utility

Access other entry values:

```php
use Filament\Schemas\Components\Utilities\Get;

function (Get $get) {
    $email = $get('email');
    // ...
}
```

---

## Custom Entries

### Generate Custom Entry

```bash
php artisan make:filament-infolist-entry AudioPlayerEntry
```

### Define Entry Class

```php
use Filament\Infolists\Components\Entry;

class AudioPlayerEntry extends Entry
{
    protected string $view = 'filament.infolists.components.audio-player-entry';
}
```

### Add Configuration Method

```php
class AudioPlayerEntry extends Entry
{
    protected string $view = 'filament.infolists.components.audio-player-entry';

    protected ?float $speed = null;

    public function speed(?float $speed): static
    {
        $this->speed = $speed;

        return $this;
    }

    public function getSpeed(): ?float
    {
        return $this->speed;
    }
}
```

### Blade View Template

```blade
<x-dynamic-component
    :component="$getEntryWrapperView()"
    :entry="$entry"
>
    {{ $getState() }}
    {{ $getSpeed() }}
    {{ $record->name }}
</x-dynamic-component>
```

### Using Custom Entry

```php
use App\Filament\Infolists\Components\AudioPlayerEntry;

AudioPlayerEntry::make('recording')
    ->speed(0.5)
```

### Utility Injection in Configuration

Support both static values and closures:

```php
use Closure;

class AudioPlayerEntry extends Entry
{
    protected float | Closure | null $speed = null;

    public function speed(float | Closure | null $speed): static
    {
        $this->speed = $speed;

        return $this;
    }

    public function getSpeed(): ?float
    {
        return $this->evaluate($this->speed);
    }
}
```

Use with closure:

```php
AudioPlayerEntry::make('recording')
    ->speed(fn (Conference $record): float => $record->isGlobal() ? 1 : 0.5)
```

### Accessing Context in Blade

Current state:

```blade
{{ $getState() }}
```

Current record:

```blade
{{ $record->name }}
```

Current operation:

```blade
@if ($operation === 'create')
    This is a new conference.
@else
    This is an existing conference.
@endif
```

Other entry values:

```blade
{{ $get('email') }}
```

Livewire component:

```blade
@php
    use Filament\Resources\Users\RelationManagers\ConferencesRelationManager;
@endphp

@if ($this instanceof ConferencesRelationManager)
    You are editing conferences of a user.
@endif
```

Entry instance:

```blade
@if ($entry->isLabelHidden())
    Label is hidden.
@endif
```

---

## Best Practices

### 1. Use Infolists for Read-Only Data

Infolists are optimized for display, not editing:

```php
public static function infolist(Schema $schema): Schema
{
    return $schema
        ->components([
            TextEntry::make('name'),
            TextEntry::make('email'),
        ]);
}
```

### 2. Leverage Dot Notation

Access relationships efficiently:

```php
TextEntry::make('author.name')
TextEntry::make('category.parent.name')
```

### 3. Use Appropriate Entry Types

Choose the right component for your data:

```php
TextEntry::make('name')          // Text
IconEntry::make('is_active')     // Boolean
ImageEntry::make('avatar')       // Image
ColorEntry::make('brand_color')  // Color
KeyValueEntry::make('meta')      // Key-value pairs
```

### 4. Format Data Appropriately

Transform data for better UX:

```php
TextEntry::make('status')
    ->badge()
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'gray',
        'published' => 'success',
    })
```

### 5. Use Global Configuration

Set defaults for all entries:

```php
use Filament\Infolists\Components\TextEntry;

TextEntry::configureUsing(function (TextEntry $entry): void {
    $entry->words(10);
});
```

### 6. Organize with Sections

Group related information:

```php
use Filament\Schemas\Components\Section;

Section::make('Details')
    ->schema([
        TextEntry::make('name'),
        TextEntry::make('email'),
    ])
```

### 7. Add Context with Tooltips

Provide additional information:

```php
TextEntry::make('title')
    ->tooltip('Shown at the top of the page')
```

---

## Troubleshooting

### Entry Shows Empty Value

**Problem**: Entry displays nothing even though data exists.

**Solution**: Check the entry name matches the model attribute:

```php
// Correct
TextEntry::make('email') // matches $model->email

// For relationships, use dot notation
TextEntry::make('author.name') // matches $model->author->name
```

### Relationship Data Not Displaying

**Problem**: Related data doesn't show.

**Solution**: Ensure the relationship is eager-loaded and use dot notation:

```php
// In Resource
public static function getEloquentQuery(): Builder
{
    return parent::getEloquentQuery()->with(['author', 'category']);
}

// In Infolist
TextEntry::make('author.name')
```

### HTML Not Rendering

**Problem**: HTML displays as text.

**Solution**: Enable HTML rendering:

```php
TextEntry::make('description')
    ->html()
```

### Icons Not Showing

**Problem**: Icon aliases not displaying.

**Solution**: Use proper Heroicon reference:

```php
use Filament\Support\Icons\Heroicon;

TextEntry::make('email')
    ->icon(Heroicon::Envelope)
```

### Badge Colors Not Working

**Problem**: Badge displays but colors don't apply.

**Solution**: Ensure `badge()` is called before `color()`:

```php
TextEntry::make('status')
    ->badge()  // Must come first
    ->color('success')
```

### Inline Labels Not Working

**Problem**: Labels still display above entries.

**Solution**: Apply to schema or section, not individual entries:

```php
use Filament\Schemas\Schema;

public function infolist(Schema $schema): Schema
{
    return $schema
        ->inlineLabel()  // Apply globally
        ->components([
            // ...
        ]);
}
```

### Custom Entry Not Found

**Problem**: Custom entry class throws errors.

**Solution**: Verify the view path matches:

```php
class AudioPlayerEntry extends Entry
{
    // Must match: resources/views/filament/infolists/components/audio-player-entry.blade.php
    protected string $view = 'filament.infolists.components.audio-player-entry';
}
```

---

## Cross-References

### Related Topics

- **[FORMS.md](FORMS.md)** - Form components for editable data
- **[TABLES.md](TABLES.md)** - Table columns for listing data
- **[RESOURCES.md](RESOURCES.md)** - Configure resource view pages with infolists
- **[SCHEMAS.md](SCHEMAS.md)** - Layout components for organizing entries
- **[ACTIONS.md](ACTIONS.md)** - Add actions to infolist entries

### External Documentation

- [FilamentPHP Infolists Documentation](https://filamentphp.com/docs/4.x/infolists/overview)
- [FilamentPHP Entry Types](https://filamentphp.com/docs/4.x/infolists/text-entry)
- [Blade Templates](https://laravel.com/docs/blade)

---

**Last Updated**: January 18, 2026  
**FilamentPHP Version**: 4.x  
**Status**: Complete
