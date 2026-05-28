# FilamentPHP Forms Reference

**Version:** FilamentPHP 4.x  
**Last Updated:** January 18, 2026

## Table of Contents

1. [Overview](#overview)
2. [Basic Components](#basic-components)
   - [TextInput](#textinput)
   - [Select](#select)
   - [Toggle](#toggle)
   - [Checkbox](#checkbox)
   - [Radio](#radio)
3. [Advanced Components](#advanced-components)
   - [FileUpload](#fileupload)
   - [RichEditor](#richeditor)
   - [DatePicker](#datepicker)
   - [ColorPicker](#colorpicker)
   - [KeyValue](#keyvalue)
   - [Repeater](#repeater)
   - [Builder](#builder)
4. [Relationship Integration](#relationship-integration)
5. [Dynamic Fields](#dynamic-fields)
6. [Validation](#validation)
7. [Field Lifecycle](#field-lifecycle)
8. [Global Configuration](#global-configuration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Overview

FilamentPHP Forms provide a powerful, fluent API for building complex forms in Laravel applications. Forms are the primary way users input data in Filament resources, pages, and modals.

### When to Use Forms

- Creating and editing resource records
- Building custom pages with data input
- Adding fields to modals and slide-overs
- Implementing wizards and multi-step processes
- Capturing user preferences and settings

### Key Concepts

- **Schema-based:** Forms are defined using a schema array of components
- **Reactive:** Fields can respond to changes in other fields using `live()`
- **Validation:** Built-in Laravel validation with fluent methods
- **Relationships:** Direct integration with Eloquent relationships
- **Customizable:** Extensive methods for styling and behavior

---

## Basic Components

### TextInput

The most common form field for single-line text entry.

#### Basic Usage

```php
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->required()
    ->maxLength(255)
```

#### Input Types

```php
// Email input
TextInput::make('email')
    ->email()
    ->required()

// Password input
TextInput::make('password')
    ->password()
    ->revealable()

// Numeric input
TextInput::make('age')
    ->numeric()
    ->minValue(1)
    ->maxValue(100)

// Telephone input
TextInput::make('phone')
    ->tel()
    ->telRegex('/^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\/0-9]*$/')

// URL input
TextInput::make('website')
    ->url()
    ->suffixIcon(Heroicon::GlobeAlt)
```

#### Conditional Input Types

```php
use Filament\Forms\Components\TextInput;

TextInput::make('text')
    ->email(FeatureFlag::active())
    ->numeric(FeatureFlag::active())
    ->password(FeatureFlag::active())
```

#### Length Validation

```php
TextInput::make('name')
    ->minLength(2)
    ->maxLength(255)
    ->length(8) // Exact length
```

#### Autocapitalize

```php
TextInput::make('name')
    ->autocapitalize('words')
```

#### Affixes (Prefix & Suffix)

```php
TextInput::make('domain')
    ->prefix('https://')
    ->suffix('.com')
    ->prefixIcon(Heroicon::GlobeAlt)
    ->suffixIcon(Heroicon::CheckCircle)
```

#### Placeholder

```php
TextInput::make('name')
    ->placeholder('John Doe')
```

#### Read-Only

```php
TextInput::make('name')
    ->readOnly()
    ->readOnly(FeatureFlag::active())
```

#### Copyable

```php
TextInput::make('apiKey')
    ->label('API key')
    ->copyable()
    ->copyable(FeatureFlag::active())
```

#### Datalist (Autocomplete Suggestions)

```php
TextInput::make('manufacturer')
    ->datalist([
        'BMW',
        'Ford',
        'Mercedes-Benz',
        'Porsche',
        'Toyota',
        'Volkswagen',
    ])
```

#### Input Masking

```php
use Filament\Support\RawJs;

TextInput::make('cardNumber')
    ->mask(RawJs::make(<<<'JS'
        $input.startsWith('34') || $input.startsWith('37') 
            ? '9999 999999 99999' 
            : '9999 9999 9999 9999'
    JS))
```

---

### Select

Dropdown selection component for single or multiple choices.

#### Basic Usage

```php
use Filament\Forms\Components\Select;

Select::make('status')
    ->options([
        'draft' => 'Draft',
        'reviewing' => 'Reviewing',
        'published' => 'Published',
    ])
    ->default('draft')
```

#### Searchable

```php
Select::make('author_id')
    ->label('Author')
    ->options(User::query()->pluck('name', 'id'))
    ->searchable()
    ->searchable(FeatureFlag::active())
```

#### Multiple Selection

```php
Select::make('technologies')
    ->multiple()
    ->options([
        'tailwind' => 'Tailwind CSS',
        'alpine' => 'Alpine.js',
        'laravel' => 'Laravel',
        'livewire' => 'Laravel Livewire',
    ])
```

#### Reorderable Multiple

```php
Select::make('technologies')
    ->multiple()
    ->reorderable()
    ->options([...])
```

#### Native vs JavaScript UI

```php
Select::make('status')
    ->options([...])
    ->native(false) // Use JavaScript-based select
```

#### Allow HTML in Options

```php
Select::make('technology')
    ->options([
        'tailwind' => '<span class="text-blue-500">Tailwind</span>',
        'alpine' => '<span class="text-green-500">Alpine</span>',
    ])
    ->searchable()
    ->allowHtml()
    ->allowHtml(FeatureFlag::active())
```

#### Icons

```php
use Filament\Support\Icons\Heroicon;

Select::make('domain')
    ->suffixIcon(Heroicon::GlobeAlt)
```

---

### Toggle

Boolean switch component.

#### Basic Usage

```php
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
```

#### Accepted Validation

```php
Toggle::make('terms_of_service')
    ->accepted()
    ->accepted(FeatureFlag::active())
```

#### Inline Label

```php
Toggle::make('is_admin')
    ->inlineLabel()
```

---

### Checkbox

Single checkbox component for boolean values.

#### Basic Usage

```php
use Filament\Forms\Components\Checkbox;

Checkbox::make('is_admin')
```

#### Accepted Validation

```php
Checkbox::make('terms_of_service')
    ->accepted()
    ->accepted(FeatureFlag::active())
```

#### Declined Validation

```php
Checkbox::make('is_under_18')
    ->declined()
    ->declined(FeatureFlag::active())
    ->declined(function (string $operation, Get $get) {
        return $operation === 'create' || $get('some_other_field') === 'specific_value';
    })
```

---

### Radio

Radio button group for single selection.

#### Basic Usage

```php
use Filament\Forms\Components\Radio;

Radio::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published'
    ])
```

---

## Advanced Components

### FileUpload

File and image upload component with extensive customization.

#### Basic Usage

```php
use Filament\Forms\Components\FileUpload;

FileUpload::make('attachment')
```

#### Multiple Files

```php
FileUpload::make('attachments')
    ->multiple()
    ->multiple(FeatureFlag::active())
```

#### Reorderable

```php
FileUpload::make('attachments')
    ->multiple()
    ->reorderable()
    ->reorderable(FeatureFlag::active())
```

#### Append Files

```php
FileUpload::make('attachments')
    ->multiple()
    ->appendFiles()
    ->appendFiles(FeatureFlag::active())
```

#### Image Configuration

```php
FileUpload::make('avatar')
    ->image()
    ->imageEditor()
    ->imagePreviewHeight('250')
    ->circular()
```

---

### RichEditor

WYSIWYG content editor with TipTap integration.

#### Basic Usage

```php
use Filament\Forms\Components\RichEditor;

RichEditor::make('content')
```

#### Toolbar Buttons

```php
RichEditor::make('content')
    ->toolbarButtons([
        ['bold', 'italic', 'underline', 'strike'],
        ['h2', 'h3'],
        ['bulletList', 'orderedList'],
    ])
```

#### Floating Toolbars

```php
RichEditor::make('content')
    ->floatingToolbars([
        'paragraph' => [
            'bold', 'italic', 'underline', 'strike',
        ],
        'heading' => [
            'h1', 'h2', 'h3',
        ],
    ])
```

#### Text Colors

```php
use Filament\Forms\Components\RichEditor\TextColor;

RichEditor::make('content')
    ->textColors([
        'brand' => TextColor::make('Brand', '#0ea5e9', darkColor: '#38bdf8'),
        'warning' => TextColor::make('Warning', '#f59e0b', darkColor: '#fbbf24'),
    ])
    ->customTextColors()
```

#### Merge Tags

```php
RichEditor::make('content')
    ->mergeTags([
        'name' => 'Full name',
        'today' => 'Today\'s date',
    ])
    ->activePanel('mergeTags')
```

#### Mentions

```php
use Filament\Forms\Components\RichEditor\MentionProvider;

RichEditor::make('content')
    ->mentions([
        MentionProvider::make('@')
            ->getSearchResultsUsing(fn (string $search): array => User::query()
                ->where('name', 'like', "%{$search}%")
                ->orderBy('name')
                ->limit(10)
                ->pluck('name', 'id')
                ->all())
            ->getLabelsUsing(fn (array $ids): array => User::query()
                ->whereIn('id', $ids)
                ->pluck('name', 'id')
                ->all()),
    ])
```

---

### DatePicker

Date and time selection component.

#### Basic Date Picker

```php
use Filament\Forms\Components\DatePicker;

DatePicker::make('date_of_birth')
    ->native(false)
```

#### Date Time Picker

```php
use Filament\Forms\Components\DateTimePicker;

DateTimePicker::make('published_at')
    ->native(false)
```

#### Time Picker

```php
use Filament\Forms\Components\TimePicker;

TimePicker::make('start_time')
```

#### Close on Date Selection

```php
DateTimePicker::make('date')
    ->native(false)
    ->closeOnDateSelection()
    ->closeOnDateSelection(FeatureFlag::active())
```

#### Read-Only

```php
DatePicker::make('date_of_birth')
    ->readOnly()
    ->readOnly(FeatureFlag::active())
```

---

### ColorPicker

Color selection component.

#### Basic Usage

```php
use Filament\Forms\Components\ColorPicker;

ColorPicker::make('color')
```

---

### KeyValue

Key-value pair editor for JSON or array data.

#### Basic Usage

```php
use Filament\Forms\Components\KeyValue;

KeyValue::make('meta')
```

#### Custom Labels

```php
KeyValue::make('meta')
    ->keyLabel('Property name')
    ->valueLabel('Property value')
```

#### Custom Placeholders

```php
KeyValue::make('meta')
    ->keyPlaceholder('Property name')
    ->valuePlaceholder('Property value')
```

---

### Repeater

Repeatable field groups for hasMany relationships or arrays.

#### Basic Usage

```php
use Filament\Forms\Components\Repeater;
use Filament\Forms\Components\TextInput;

Repeater::make('qualifications')
    ->schema([
        TextInput::make('name')
            ->required(),
        TextInput::make('institution')
            ->required(),
    ])
```

#### Simple Repeater (Single Field)

```php
Repeater::make('invitations')
    ->simple(
        TextInput::make('email')
            ->email()
            ->required(),
    )
```

#### Min/Max Items

```php
Repeater::make('qualifications')
    ->schema([...])
    ->minItems(1)
    ->maxItems(5)
```

#### Distinct Field Values

```php
Repeater::make('answers')
    ->schema([
        Checkbox::make('is_correct')
            ->distinct(),
            // or
            ->fixIndistinctState(),
    ])
```

#### Relationship

```php
Repeater::make('qualifications')
    ->relationship()
    ->schema([...])
```

#### Mutate Relationship Data

```php
Repeater::make('qualifications')
    ->relationship()
    ->schema([...])
    ->mutateRelationshipDataBeforeFillUsing(function (array $data): array {
        $data['user_id'] = auth()->id();
        return $data;
    })
```

---

### Builder

Block-based content builder.

#### Basic Usage

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // Define blocks here
    ])
```

#### Min/Max Items

```php
Builder::make('content')
    ->blocks([...])
    ->minItems(1)
    ->maxItems(5)
```

#### Reorderable with Buttons

```php
Builder::make('content')
    ->blocks([...])
    ->reorderableWithButtons()
    ->reorderableWithButtons(FeatureFlag::active())
```

---

## Relationship Integration

### BelongsTo Relationship

#### Basic Select

```php
use Filament\Forms\Components\Select;

Select::make('author_id')
    ->relationship(name: 'author', titleAttribute: 'name')
    ->searchable()
    ->preload()
```

#### Conditional Preload

```php
Select::make('author_id')
    ->relationship(name: 'author', titleAttribute: 'name')
    ->searchable()
    ->preload(FeatureFlag::active())
```

#### Custom Label Callback

```php
use Illuminate\Database\Eloquent\Model;

Select::make('author_id')
    ->relationship(
        name: 'author',
        modifyQueryUsing: fn (Builder $query) => $query->orderBy('first_name')->orderBy('last_name'),
    )
    ->getOptionLabelFromRecordUsing(fn (Model $record) => "{$record->first_name} {$record->last_name}")
    ->searchable(['first_name', 'last_name'])
```

#### Ignore Current Record

```php
Select::make('parent_id')
    ->relationship(name: 'parent', titleAttribute: 'name', ignoreRecord: true)
```

#### Create Option Form

```php
Select::make('author_id')
    ->relationship(name: 'author', titleAttribute: 'name')
    ->createOptionForm([
        TextInput::make('name')
            ->required(),
        TextInput::make('email')
            ->required()
            ->email(),
    ])
```

#### Edit Option Form

```php
Select::make('author_id')
    ->relationship(name: 'author', titleAttribute: 'name')
    ->editOptionForm([
        TextInput::make('name')
            ->required(),
        TextInput::make('email')
            ->required()
            ->email(),
    ])
```

---

### BelongsToMany Relationship

#### CheckboxList

```php
use Filament\Forms\Components\CheckboxList;

CheckboxList::make('technologies')
    ->relationship(titleAttribute: 'name')
    ->bulkToggleable()
    ->bulkToggleable(FeatureFlag::active())
```

#### Pivot Data

```php
CheckboxList::make('primaryTechnologies')
    ->relationship(name: 'technologies', titleAttribute: 'name')
    ->pivotData([
        'is_primary' => true,
    ])
```

#### Custom Query

```php
use Illuminate\Database\Eloquent\Builder;

CheckboxList::make('technologies')
    ->relationship(
        titleAttribute: 'name',
        modifyQueryUsing: fn (Builder $query) => $query->withTrashed(),
    )
```

#### Allow HTML

```php
CheckboxList::make('technology')
    ->options([
        'tailwind' => '<span class="text-blue-500">Tailwind</span>',
        'alpine' => '<span class="text-green-500">Alpine</span>',
    ])
    ->searchable()
    ->allowHtml()
    ->allowHtml(FeatureFlag::active())
```

#### Searchable

```php
CheckboxList::make('technology')
    ->options([...])
    ->searchable()
```

---

### HasOne/HasMany Relationships

#### Group Component

```php
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Group;

Group::make()
    ->relationship('customer')
    ->schema([
        TextInput::make('name')
            ->label('Customer')
            ->required(),
        TextInput::make('email')
            ->label('Email address')
            ->email()
            ->required(),
    ])
```

#### Fieldset Component

```php
use Filament\Schemas\Components\Fieldset;

Fieldset::make('Metadata')
    ->relationship('metadata')
    ->schema([
        TextInput::make('title'),
        Textarea::make('description'),
        FileUpload::make('image'),
    ])
```

#### Conditional Saving

```php
Group::make()
    ->relationship(
        'customer',
        condition: fn (?array $state): bool => filled($state['name']),
    )
    ->schema([
        TextInput::make('name')
            ->label('Customer'),
        TextInput::make('email')
            ->label('Email address')
            ->email()
            ->requiredWith('name'),
    ])
```

---

## Dynamic Fields

### Live Updates

Make fields reactive to changes:

```php
use Filament\Forms\Components\Select;

Select::make('status')
    ->options([...])
    ->live()
```

#### Live on Blur

```php
TextInput::make('username')
    ->live(onBlur: true)
```

---

### Conditional Visibility

#### Using hidden()

```php
use Filament\Schemas\Components\Utilities\Get;
use Filament\Forms\Components\Checkbox;
use Filament\Forms\Components\TextInput;

Checkbox::make('is_company')
    ->live()

TextInput::make('company_name')
    ->hidden(fn (Get $get): bool => ! $get('is_company'))
```

#### Using visible()

```php
TextInput::make('company_name')
    ->visible(fn (Get $get): bool => $get('is_company'))
```

#### Using hiddenJs() for Client-Side

```php
use Filament\Forms\Components\Select;
use Filament\Forms\Components\Toggle;

Select::make('role')
    ->options([
        'user' => 'User',
        'staff' => 'Staff',
    ])

Toggle::make('is_admin')
    ->hiddenJs(<<<'JS'
        $get('role') !== 'staff'
        JS)
```

#### Using visibleJs() for Client-Side

```php
Toggle::make('is_admin')
    ->visibleJs(<<<'JS'
        $get('role') === 'staff'
        JS)
```

#### Hide/Show on Operations

```php
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->hiddenOn('create')
    ->hiddenOn(['create', 'edit'])
    ->visibleOn('create')
    ->visibleOn(['create', 'edit'])
```

---

### Dynamic Schema

Render different fields based on select value:

```php
use Filament\Forms\Components\FileUpload;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Utilities\Get;

Select::make('type')
    ->options([
        'employee' => 'Employee',
        'freelancer' => 'Freelancer',
    ])
    ->live()
    ->afterStateUpdated(fn (Select $component) => $component
        ->getContainer()
        ->getComponent('dynamicTypeFields')
        ->getChildSchema()
        ->fill())
    
Grid::make(2)
    ->schema(fn (Get $get): array => match ($get('type')) {
        'employee' => [
            TextInput::make('employee_number')
                ->required(),
            FileUpload::make('badge')
                ->image()
                ->required(),
        ],
        'freelancer' => [
            TextInput::make('hourly_rate')
                ->numeric()
                ->required()
                ->prefix('€'),
            FileUpload::make('contract')
                ->required(),
        ],
        default => [],
    })
    ->key('dynamicTypeFields')
```

---

### Dependent Fields

#### Dependent Options

```php
use Filament\Schemas\Components\Utilities\Get;
use Filament\Forms\Components\Select;

Select::make('category')
    ->options([
        'web' => 'Web development',
        'mobile' => 'Mobile development',
        'design' => 'Design',
    ])
    ->live()

Select::make('sub_category')
    ->options(fn (Get $get): array => match ($get('category')) {
        'web' => [
            'frontend_web' => 'Frontend development',
            'backend_web' => 'Backend development',
        ],
        'mobile' => [
            'ios_mobile' => 'iOS development',
            'android_mobile' => 'Android development',
        ],
        'design' => [
            'app_design' => 'Panel design',
            'marketing_website_design' => 'Marketing website design',
        ],
        default => [],
    })
```

#### From Eloquent Models

```php
use Filament\Schemas\Components\Utilities\Get;
use Filament\Forms\Components\Select;
use Illuminate\Support\Collection;

Select::make('category')
    ->options(Category::query()->pluck('name', 'id'))
    ->live()
    
Select::make('sub_category')
    ->options(fn (Get $get): Collection => SubCategory::query()
        ->where('category', $get('category'))
        ->pluck('name', 'id'))
```

#### Dependent Labels

```php
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Utilities\Get;

TextInput::make('name')
    ->live()
    
TextInput::make('email')
    ->label(fn (Get $get): string => filled($get('name')) 
        ? "Email address for {$get('name')}" 
        : 'Email address')
```

---

### Conditional Requirements

```php
use Filament\Schemas\Components\Utilities\Get;
use Filament\Forms\Components\TextInput;

TextInput::make('company_name')
    ->live(onBlur: true)
    
TextInput::make('vat_number')
    ->required(fn (Get $get): bool => filled($get('company_name')))
```

---

## Validation

### Fluent Validation Methods

```php
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->required()
    ->maxLength(255)
    ->minLength(2)
    ->unique(Category::class, 'slug', fn ($record) => $record)
```

### Custom Validation Attribute

```php
TextInput::make('name')
    ->validationAttribute('full name')
```

### Numeric Validation

```php
TextInput::make('number')
    ->numeric()
    ->minValue(1)
    ->maxValue(100)
```

### Date Validation

```php
Field::make('start_date')->after('tomorrow')
Field::make('end_date')->after('start_date')
```

### Conditional Validation

```php
TextInput::make('password')
    ->password()
    ->required(fn (string $operation): bool => $operation === 'create')
```

### RequiredIf/RequiredWith

```php
Field::make('name')->requiredIf('field', 'value')
Field::make('name')->requiredWith('field,another_field')
Field::make('name')->requiredWithAll('field,another_field')
Field::make('name')->requiredWithout('field')
Field::make('name')->requiredWithoutAll('field,another_field')
```

### Prohibited

```php
Field::make('name')->prohibited()
```

---

## Field Lifecycle

### After State Updated

```php
use Filament\Forms\Components\TextInput;

TextInput::make('name')
    ->afterStateUpdated(function (?string $state, ?string $old) {
        // Custom logic
    })
```

### After State Updated (JavaScript)

```php
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Utilities\Set;

TextInput::make('name')
    ->afterStateUpdatedJs(<<<'JS'
        $set('email', ($state ?? '').replaceAll(' ', '.').toLowerCase() + '@example.com')
        JS)
    
TextInput::make('email')
    ->label('Email address')
```

### Partial Rendering

```php
TextInput::make('name')
    ->live()
    ->partiallyRenderComponentsAfterStateUpdated(['email'])
```

### Self-Render Only

```php
TextInput::make('name')
    ->live()
    ->partiallyRenderAfterStateUpdated()
    ->belowContent(fn (Get $get): ?string => filled($get('name')) 
        ? "Hi, {$get('name')}!" 
        : null)
```

---

## Global Configuration

Configure defaults for all instances:

```php
use Filament\Forms\Components\TextInput;

TextInput::configureUsing(function (TextInput $component): void {
    $component->telRegex('/^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\/0-9]*$/');
});
```

---

## Best Practices

### 1. **Use Fluent Validation**
Prefer fluent validation methods over manual rules for better DX and automatic frontend validation.

```php
// Good
TextInput::make('name')
    ->required()
    ->maxLength(255)

// Less ideal
TextInput::make('name')
    ->rules(['required', 'max:255'])
```

### 2. **Leverage Relationships**
Use the `relationship()` method for cleaner code and automatic data handling.

```php
// Good
Select::make('author_id')
    ->relationship(name: 'author', titleAttribute: 'name')

// Less ideal  
Select::make('author_id')
    ->options(User::pluck('name', 'id'))
```

### 3. **Use Live Updates Wisely**
Only mark fields as `live()` when necessary to avoid unnecessary server requests.

```php
// Use live() for dependent fields
Select::make('country')
    ->live() // Necessary for cities dropdown
    
Select::make('city')
    ->options(fn (Get $get) => City::where('country_id', $get('country'))->pluck('name', 'id'))
```

### 4. **Organize Complex Forms**
Extract form field definitions to separate methods or classes for reusability.

```php
class CategoryForm
{
    public static function getNameFormField(): TextInput
    {
        return TextInput::make('name')
            ->required()
            ->live()
            ->afterStateUpdated(fn ($state, callable $set) => $set('slug', Str::slug($state)));
    }
    
    public static function getSlugFormField(): TextInput
    {
        return TextInput::make('slug')
            ->disabled()
            ->required()
            ->unique(Category::class, 'slug', fn ($record) => $record);
    }
}
```

### 5. **Use Client-Side Logic When Possible**
For simple visibility logic, use `hiddenJs()` or `visibleJs()` to avoid server requests.

```php
// Client-side (better performance)
Toggle::make('is_admin')
    ->visibleJs(<<<'JS'
        $get('role') === 'staff'
        JS)

// Server-side (less performant)
Toggle::make('is_admin')
    ->live()
    ->visible(fn (Get $get): bool => $get('role') === 'staff')
```

### 6. **Handle Password Fields Carefully**
Hash passwords and conditionally save them:

```php
use Illuminate\Support\Facades\Hash;

TextInput::make('password')
    ->password()
    ->dehydrateStateUsing(fn (string $state): string => Hash::make($state))
    ->saved(fn (?string $state): bool => filled($state))
    ->required(fn (string $operation): bool => $operation === 'create')
```

### 7. **Prevent Unwanted Saves**
Use `saved(false)` for fields that shouldn't persist:

```php
TextInput::make('password_confirmation')
    ->password()
    ->saved(false)
```

### 8. **Add Helper Content**
Use slots for additional context:

```php
TextInput::make('name')
    ->belowContent('This is the user\'s full name.')
    ->aboveErrorMessage(Icon::make(Heroicon::Star))
```

### 9. **Inline Labels for Space**
Use inline labels for compact forms:

```php
use Filament\Schemas\Components\Section;

Section::make('Details')
    ->inlineLabel()
    ->schema([
        TextInput::make('name'),
        TextInput::make('email'),
    ])
```

### 10. **Configure Globally Where Appropriate**
Set consistent defaults across your app:

```php
// In AppServiceProvider
TextInput::configureUsing(function (TextInput $component): void {
    $component
        ->autocapitalize('words')
        ->maxLength(255);
});
```

---

## Troubleshooting

### Field Not Saving

**Problem:** Field value is not being persisted to database.

**Solutions:**
1. Check if `saved(false)` is set
2. Verify mass assignment (`$fillable` in model)
3. Ensure field name matches database column
4. Check for `dehydrated(false)` setting

```php
// Make sure field is savable
TextInput::make('name')
    ->saved() // Default is true
    ->dehydrated() // Default is true
```

---

### Live Updates Not Working

**Problem:** Field changes don't trigger reactivity.

**Solutions:**
1. Add `live()` to the controlling field
2. Check network requests in browser DevTools
3. Verify `Get` utility is injected properly

```php
// Parent field must be live
Select::make('country')
    ->live() // Required!
    
// Child field reacts to parent
Select::make('city')
    ->options(fn (Get $get) => ...)
```

---

### Validation Not Working

**Problem:** Custom validation rules aren't being applied.

**Solutions:**
1. Ensure field is `required()` if needed
2. Check validation attribute name
3. Verify model casts for boolean/numeric fields

```php
// Ensure validation is properly configured
TextInput::make('email')
    ->email() // Add email validation
    ->required() // Make required
    ->validationAttribute('email address') // Custom error message attribute
```

---

### Relationship Not Loading

**Problem:** Select field doesn't show relationship options.

**Solutions:**
1. Verify relationship exists on model
2. Check titleAttribute column exists
3. Add `preload()` for immediate loading

```php
// Ensure relationship is configured
Select::make('author_id')
    ->relationship(name: 'author', titleAttribute: 'name')
    ->searchable()
    ->preload() // Load immediately
```

---

### Performance Issues with Many Options

**Problem:** Select field is slow with many options.

**Solutions:**
1. Make the select `searchable()`
2. Don't use `preload()` with large datasets
3. Implement custom search with `getSearchResultsUsing()`
4. Use `optionsLimit()` to restrict results

```php
Select::make('author_id')
    ->searchable()
    ->getSearchResultsUsing(fn (string $search): array => User::query()
        ->where('name', 'like', "%{$search}%")
        ->limit(50)
        ->pluck('name', 'id')
        ->all())
    ->getOptionLabelUsing(fn ($value): ?string => User::find($value)?->name)
```

---

### Dynamic Fields Not Rendering

**Problem:** Conditional fields don't appear/disappear correctly.

**Solutions:**
1. Ensure controlling field has `live()`
2. Add `afterStateUpdated()` to reset dependent fields
3. Use `key()` on dynamic components
4. Call `fill()` to reset nested components

```php
Select::make('type')
    ->options([...])
    ->live()
    ->afterStateUpdated(fn (Select $component) => $component
        ->getContainer()
        ->getComponent('dynamicFields')
        ->getChildSchema()
        ->fill())

Grid::make()
    ->schema(fn (Get $get): array => ...)
    ->key('dynamicFields') // Important!
```

---

### Repeater Data Not Saving

**Problem:** Repeater items aren't being saved to database.

**Solutions:**
1. Check if relationship is defined on model
2. Verify pivot table exists for many-to-many
3. Ensure `relationship()` is called on Repeater
4. Check mass assignment on related model

```php
// With relationship
Repeater::make('qualifications')
    ->relationship() // Required for relationships!
    ->schema([...])
```

---

### RichEditor Content Not Rendering

**Problem:** Rich content doesn't display properly.

**Solutions:**
1. Use `RichContentRenderer` for display
2. Configure merge tags/custom blocks
3. Register rich content on model

```php
use Filament\Forms\Components\RichEditor\RichContentRenderer;

// In view/infolist
RichContentRenderer::make($record->content)
    ->mergeTags([
        'name' => $record->user->name,
    ])
    ->toHtml()
```

---

## Cross-References

### Related Topics
- [TABLES.md](./TABLES.md) - Table columns and filters
- [SCHEMAS.md](./SCHEMAS.md) - Layout components (Grid, Section, Fieldset)
- [ACTIONS.md](./ACTIONS.md) - Form actions and buttons
- [VALIDATION.md](./VALIDATION.md) - Advanced validation patterns
- [RESOURCES.md](./RESOURCES.md) - Form integration in resources

### External Resources
- [FilamentPHP Forms Documentation](https://filamentphp.com/docs/4.x/forms)
- [Laravel Validation](https://laravel.com/docs/validation)
- [TipTap Editor](https://tiptap.dev)

---

**End of Forms Reference**
