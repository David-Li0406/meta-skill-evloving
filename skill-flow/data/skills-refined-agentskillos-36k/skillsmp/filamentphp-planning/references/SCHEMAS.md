# FilamentPHP Schemas & Layout Components

## Overview

FilamentPHP's Schema system provides powerful layout components for organizing forms, tables, infolists, and custom content. This reference covers all layout components including Grid, Section, Fieldset, Tabs, Wizard, Split, and responsive layout techniques.

**When to Use Schemas:**
- Organizing complex forms with multiple fields
- Creating responsive layouts across devices
- Grouping related fields into sections or fieldsets
- Building multi-step wizards
- Creating tabbed interfaces
- Controlling field positioning and column spans

**Key Concepts:**
- Schema components define the structure and layout
- Responsive breakpoints control layout across devices
- Column spans determine field widths within grids
- Global configuration via `configureUsing()`
- Layout components can be nested for complex structures

## Table of Contents

1. [Basic Schema Structure](#basic-schema-structure)
2. [Grid Layout Component](#grid-layout-component)
3. [Section Component](#section-component)
4. [Fieldset Component](#fieldset-component)
5. [Tabs Component](#tabs-component)
6. [Wizard Component](#wizard-component)
7. [Split and Flex Layouts](#split-and-flex-layouts)
8. [Column Spans and Positioning](#column-spans-and-positioning)
9. [Responsive Layouts](#responsive-layouts)
10. [Container Breakpoints](#container-breakpoints)
11. [Component Spacing](#component-spacing)
12. [Inline Labels](#inline-labels)
13. [Collapsible Components](#collapsible-components)
14. [Global Configuration](#global-configuration)
15. [Custom Components](#custom-components)
16. [Troubleshooting](#troubleshooting)

---

## Basic Schema Structure

### Defining a Schema

Schemas are defined using the `Schema` object with the `components()` method:

```php
use Filament\Forms\Components\Checkbox;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Section;

$schema
    ->components([
        Grid::make(2)
            ->schema([
                Section::make('Details')
                    ->schema([
                        TextInput::make('name'),
                        Select::make('position')
                            ->options([
                                'developer' => 'Developer',
                                'designer' => 'Designer',
                            ]),
                        Checkbox::make('is_admin'),
                    ]),
                Section::make('Auditing')
                    ->schema([
                        TextEntry::make('created_at')
                            ->dateTime(),
                        TextEntry::make('updated_at')
                            ->dateTime(),
                    ]),
            ]),
    ])
```

### Schema Method in Resources

```php
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;

public static function configure(Schema $schema): Schema
{
    return $schema
        ->components([
            TextInput::make('name')->required(),
            TextInput::make('email')->email()->required(),
            // ...
        ]);
}
```

### Schema in Livewire Components

```php
use Filament\Schemas\Schema;

public function productSchema(Schema $schema): Schema
{
    return $schema
        ->components([
            // ...
        ]);
}
```

---

## Grid Layout Component

### Basic Grid with Column Count

Create responsive grids using the `Grid` component:

```php
use Filament\Schemas\Components\Grid;

Grid::make()
    ->columns(2)
    ->schema([
        // ...
    ])
```

This creates a 2-column grid on `lg` breakpoint and higher, with smaller devices defaulting to 1 column.

### Responsive Grid with Breakpoints

Define different column counts for various breakpoints:

```php
Grid::make()
    ->columns([
        'default' => 1,
        'sm' => 2,
        'md' => 3,
        'lg' => 4,
        'xl' => 6,
        '2xl' => 8,
    ])
    ->schema([
        // ...
    ])
```

**Available breakpoints:**
- `default` - For devices smaller than the smallest specified breakpoint
- `sm` - Small devices (640px+)
- `md` - Medium devices (768px+)
- `lg` - Large devices (1024px+)
- `xl` - Extra large devices (1280px+)
- `2xl` - Extra extra large devices (1536px+)

### Dynamic Grid Columns

Use a callback to calculate columns dynamically:

```php
Grid::make()
    ->columns(function (Get $get, ?string $model, string $operation) {
        if ($operation === 'create') {
            return 1;
        }
        return 2;
    })
    ->schema([
        // ...
    ])
```

**Available utilities for injection:**
- `$component` - Component instance
- `$get` - Function for retrieving schema data
- `$livewire` - Livewire component
- `$model` - Eloquent model FQN
- `$operation` - Operation type (create/edit/view)
- `$record` - Eloquent record instance

### Grid with Column Span Control

Control individual component widths within the grid:

```php
use Filament\Tables\Columns\Layout\Grid;
use Filament\Tables\Columns\Layout\Stack;
use Filament\Tables\Columns\TextColumn;

Grid::make([
    'lg' => 2,
    '2xl' => 5,
])
    ->schema([
        Stack::make([
            TextColumn::make('name'),
            TextColumn::make('job'),
        ])->columnSpan([
            'lg' => 'full',
            '2xl' => 2,
        ]),
        TextColumn::make('phone')
            ->icon('heroicon-m-phone')
            ->columnSpan([
                '2xl' => 2,
            ]),
        TextColumn::make('email')
            ->icon('heroicon-m-envelope'),
    ])
```

### Table Content Grid Layout

Arrange table records in a grid format:

```php
use Filament\Tables\Columns\Layout\Stack;
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([
            Stack::make([
                // Columns
            ]),
        ])
        ->contentGrid([
            'md' => 2,
            'xl' => 3,
        ]);
}
```

Supports breakpoints from `sm` to `2xl` with 1-12 columns per row.

### Grid Spacing Control

#### Dense Layout

Reduce spacing between components by 50%:

```php
Grid::make()
    ->dense()
    ->schema([
        // ...
    ])
```

#### Remove Spacing

Remove all gaps between components:

```php
Grid::make()
    ->gap(false)
    ->schema([
        // ...
    ])
```

---

## Section Component

Sections organize fields into labeled groups with optional descriptions and collapsibility.

### Basic Section

```php
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->schema([
        // ...
    ])
```

Both `make()` and `description()` accept static values or callback functions for dynamic content.

### Headerless Section Card

Create a section without header for visual grouping:

```php
Section::make()
    ->schema([
        // ...
    ])
```

### Section with Grid Columns

```php
Section::make('Heading')
    ->schema([
        // ...
    ])
    ->columns(2)
```

Accepts static integers or dynamic callbacks with utility injection.

### Responsive Section Columns

```php
Section::make()
    ->columns([
        'sm' => 3,
        'xl' => 6,
        '2xl' => 8,
    ])
    ->schema([
        TextInput::make('name')
            ->columnSpan([
                'default' => 1,
                'sm' => 2,
                'xl' => 3,
                '2xl' => 4,
            ])
            ->columnOrder([
                'default' => 2,
                'xl' => 1,
            ]),
        TextInput::make('email')
            ->columnSpan([
                'default' => 1,
                'xl' => 2,
            ])
            ->columnOrder([
                'default' => 1,
                'xl' => 2,
            ]),
        // ...
    ])
```

### Collapsible Section

Allow users to hide/show section content:

```php
Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
```

### Collapsed by Default

```php
Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
    ->collapsed()
```

### Conditional Collapsibility

```php
Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible(FeatureFlag::active())
    ->collapsed(FeatureFlag::active())
```

### Persist Collapsed State

Store collapsed state in local storage:

```php
Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
    ->persistCollapsed()
```

### Aside Layout

Position heading/description on the left with components on the right:

```php
Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->aside()
    ->schema([
        // ...
    ])
```

Conditional aside layout:

```php
Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->aside(FeatureFlag::active())
    ->schema([
        // ...
    ])
```

### Compact Section

Reduce visual footprint for nested sections:

```php
Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->schema([
        // ...
    ])
    ->compact()
```

### Section with Header Actions

Add actions to the section header:

```php
Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->afterHeader([
        Action::make('test'),
    ])
    ->schema([
        // ...
    ])
```

### Section with Footer Components

Add components to the section footer:

```php
Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->schema([
        // ...
    ])
    ->footer([
        Action::make('test'),
    ])
```

### Full Width Section

Make section span entire grid width:

```php
Section::make('Full Width Section')
    ->columnSpanFull()
    ->schema([
        // ...
    ])
```

### Inline Labels in Section

Display all field labels inline:

```php
Section::make('Details')
    ->inlineLabel()
    ->schema([
        TextInput::make('name'),
        TextInput::make('email')
            ->label('Email address'),
        TextInput::make('phone')
            ->label('Phone number'),
    ])
```

---

## Fieldset Component

Fieldsets group fields with a labeled border.

### Basic Fieldset

```php
use Filament\Schemas\Components\Fieldset;

Fieldset::make('Label')
    ->schema([
        // ...
    ])
```

### Responsive Fieldset Columns

```php
Fieldset::make('Label')
    ->columns([
        'default' => 1,
        'md' => 2,
        'xl' => 3,
    ])
    ->schema([
        // ...
    ])
```

### Borderless Fieldset

Remove the container border:

```php
Fieldset::make('Label')
    ->contained(false)
    ->schema([
        // ...
    ])
```

### Full Width Fieldset

```php
Fieldset::make('User Details')
    ->columnSpanFull()
    ->schema([
        // ...
    ])
```

---

## Tabs Component

Create tabbed interfaces for organizing content.

### Basic Tabs

```php
use Filament\Schemas\Components\Tabs;
use Filament\Schemas\Components\Tabs\Tab;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 2')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 3')
            ->schema([
                // ...
            ]),
    ])
```

The first tab is active by default.

### Tab with Columns

```php
Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ])
            ->columns(3),
        // ...
    ])
```

### Tab with Icon

```php
use Filament\Support\Enums\IconPosition;
use Filament\Support\Icons\Heroicon;

Tabs::make('Tabs')
    ->tabs([
        Tab::make('Notifications')
            ->icon(Heroicon::Bell)
            ->iconPosition(IconPosition::After)
            ->schema([
                // ...
            ]),
        // ...
    ])
```

### Set Active Tab

```php
Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 2')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 3')
            ->schema([
                // ...
            ]),
    ])
    ->activeTab(2)
```

Index is 0-based, so `2` activates the third tab.

### Vertical Tabs

```php
Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 2')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 3')
            ->schema([
                // ...
            ]),
    ])
    ->vertical()
```

Conditional vertical layout:

```php
Tabs::make('Tabs')
    ->tabs([
        // ...
    ])
    ->vertical(FeatureFlag::active())
```

### Disable Tab Scrolling

Group overflow tabs into a dropdown:

```php
Tabs::make('Tabs')
    ->tabs([
        // ...
    ])
    ->scrollable(false)
```

### Tabs Without Container

Remove the card-styled wrapper:

```php
Tabs::make('Tabs')
    ->tabs([
        Tab::make('Tab 1')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 2')
            ->schema([
                // ...
            ]),
        Tab::make('Tab 3')
            ->schema([
                // ...
            ]),
    ])
    ->contained(false)
```

---

## Wizard Component

Create multi-step forms with navigation and validation.

### Basic Wizard

```php
use Filament\Schemas\Components\Wizard;
use Filament\Schemas\Components\Wizard\Step;

Wizard::make([
    Step::make('Order')
        ->schema([
            // ...
        ]),
    Step::make('Delivery')
        ->schema([
            // ...
        ]),
    Step::make('Payment')
        ->schema([
            // ...
        ]),
])
```

### Wizard Step with Columns

```php
Wizard::make([
    Step::make('Order')
        ->columns(2)
        ->schema([
            // ...
        ]),
    // ...
])
```

### Wizard Step with Description

```php
protected function getSteps(): array
{
    return [
        Step::make('Name')
            ->description('Give the category a clear and unique name')
            ->schema([
                TextInput::make('name')
                    ->required()
                    ->live()
                    ->afterStateUpdated(fn ($state, callable $set) => $set('slug', Str::slug($state))),
                TextInput::make('slug')
                    ->disabled()
                    ->required()
                    ->unique(Category::class, 'slug', fn ($record) => $record),
            ]),
        Step::make('Description')
            ->description('Add some extra details')
            ->schema([
                MarkdownEditor::make('description')
                    ->columnSpan('full'),
            ]),
        Step::make('Visibility')
            ->description('Control who can view it')
            ->schema([
                Toggle::make('is_visible')
                    ->label('Visible to customers.')
                    ->default(true),
            ]),
    ];
}
```

---

## Split and Flex Layouts

### Split Layout

Stack columns on mobile, display side-by-side on larger screens:

```php
use Filament\Support\Enums\FontWeight;
use Filament\Tables\Columns\Layout\Split;
use Filament\Tables\Columns\TextColumn;

Split::make([
    ImageColumn::make('avatar')
        ->circular(),
    TextColumn::make('name')
        ->weight(FontWeight::Bold)
        ->searchable()
        ->sortable(),
    TextColumn::make('email'),
])
```

### Split with Breakpoint Control

Define when columns start appearing side-by-side:

```php
Split::make([
    ImageColumn::make('avatar')
        ->circular(),
    TextColumn::make('name')
        ->weight(FontWeight::Bold)
        ->searchable()
        ->sortable(),
    TextColumn::make('email'),
])->from('md')
```

Columns stack below `md` breakpoint and appear horizontally from `md` onwards.

### Split with Stack

Vertically group multiple columns within a split:

```php
use Filament\Tables\Columns\Layout\Stack;

Split::make([
    ImageColumn::make('avatar')
        ->circular(),
    TextColumn::make('name')
        ->weight(FontWeight::Bold)
        ->searchable()
        ->sortable(),
    Stack::make([
        TextColumn::make('phone')
            ->icon('heroicon-m-phone'),
        TextColumn::make('email')
            ->icon('heroicon-m-envelope'),
    ]),
])
```

### Prevent Column Growth

Control column widths in split layouts:

```php
Split::make([
    ImageColumn::make('avatar')
        ->circular()
        ->grow(false),
    TextColumn::make('name')
        ->weight(FontWeight::Bold)
        ->searchable()
        ->sortable(),
    TextColumn::make('email'),
])
```

The avatar won't consume extra whitespace, allowing other columns to expand.

### Flex Layout

Create flexible width layouts with precise growth control:

```php
use Filament\Forms\Components\Textarea;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Toggle;
use Filament\Schemas\Components\Section;
use Filament\Schemas\Components\Flex;

Flex::make([
    Section::make([
        TextInput::make('title'),
        Textarea::make('content'),
    ]),
    Section::make([
        Toggle::make('is_published'),
        Toggle::make('is_featured'),
    ])->grow(false),
])->from('md')
```

The first section grows to fill space, the second maintains natural width.

---

## Column Spans and Positioning

### Static Column Span

Specify how many columns a component occupies:

```php
TextInput::make('name')
    ->columnSpan(2)
```

Applies on `lg` breakpoint and higher; smaller devices default to 1 column.

### Full Width

Make a component span all columns:

```php
RichEditor::make('content')
    ->columnSpan('full')
```

Or use the helper method:

```php
Section::make('Full Width Section')
    ->columnSpanFull()
```

### Responsive Column Spans

Define different spans for various breakpoints:

```php
TextInput::make('description')
    ->columnSpan(['md' => 2, 'xl' => 4])
```

### Column Span with Breakpoint Arrays

```php
TextInput::make('name')
    ->columnSpan([
        'default' => 1,
        'sm' => 2,
        'xl' => 3,
        '2xl' => 4,
    ])
```

### Column Start Position

Control where a component starts in the grid:

```php
Grid::make()
    ->columns([
        'sm' => 3,
        'xl' => 6,
        '2xl' => 8,
    ])
    ->schema([
        TextInput::make('name')
            ->columnStart([
                'sm' => 2,
                'xl' => 3,
                '2xl' => 4,
            ]),
        // ...
    ])
```

The input always starts halfway through the grid.

### Column Order

Change visual order of components:

```php
Grid::make()
    ->columns(3)
    ->schema([
        TextInput::make('first')
            ->columnOrder(3), // Appears last
        TextInput::make('second')
            ->columnOrder(1), // Appears first
        TextInput::make('third')
            ->columnOrder(2), // Appears second
    ])
```

### Responsive Column Order

Different orders at different breakpoints:

```php
Grid::make()
    ->columns([
        'sm' => 2,
        'lg' => 3,
    ])
    ->schema([
        TextInput::make('title')
            ->columnOrder([
                'default' => 1,
                'lg' => 3,
            ]),
        TextInput::make('description')
            ->columnOrder([
                'default' => 2,
                'lg' => 1,
            ]),
        TextInput::make('category')
            ->columnOrder([
                'default' => 3,
                'lg' => 2,
            ]),
    ])
```

### Dynamic Column Order

Use closure for conditional ordering:

```php
->columnOrder(fn () => 1)
```

Available utilities: `$component`, `$get`, `$livewire`, `$model`, `$operation`, `$record`.

---

## Responsive Layouts

### V4 Breaking Change: Layout Components

**IMPORTANT:** In FilamentPHP v4, Grid, Section, and Fieldset components consume **one column by default** instead of full width.

To make them span all columns:

```php
use Filament\Schemas\Components\Fieldset;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Section;

Fieldset::make()
    ->columnSpanFull();
    
Grid::make()
    ->columnSpanFull();

Section::make()
    ->columnSpanFull();
```

### Preserve v3 Behavior Globally

In your service provider's `boot()` method:

```php
use Filament\Schemas\Components\Fieldset;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Section;

Fieldset::configureUsing(fn (Fieldset $fieldset) => $fieldset
    ->columnSpanFull());

Grid::configureUsing(fn (Grid $grid) => $grid
    ->columnSpanFull());

Section::configureUsing(fn (Section $section) => $section
    ->columnSpanFull());
```

### Mobile-First Responsive Design

Define base layout for mobile, then override at larger breakpoints:

```php
Grid::make()
    ->columns(['md' => 2, 'xl' => 4])
    ->schema([
        // Components default to 1 column on mobile
    ])
```

### Complex Responsive Patterns

```php
Section::make()
    ->columns([
        'default' => 1,  // Mobile: 1 column
        'sm' => 2,       // Small: 2 columns
        'md' => 3,       // Medium: 3 columns
        'lg' => 4,       // Large: 4 columns
        'xl' => 6,       // XL: 6 columns
        '2xl' => 8,      // 2XL: 8 columns
    ])
    ->schema([
        TextInput::make('field1')
            ->columnSpan([
                'default' => 1,
                'md' => 2,
                'xl' => 3,
            ]),
        // More fields...
    ])
```

---

## Container Breakpoints

Container breakpoints use element size rather than viewport size.

### Enable Grid Container

```php
Grid::make()
    ->gridContainer()
    ->columns([
        '@md' => 3,
        '@xl' => 4,
    ])
    ->schema([
        // ...
    ])
```

**Container breakpoints:**
- `@md` - Container width ≥ 448px
- `@xl` - Container width ≥ 576px

### Container Breakpoints on Fields

```php
Grid::make()
    ->gridContainer()
    ->columns([
        '@md' => 3,
        '@xl' => 4,
    ])
    ->schema([
        TextInput::make('name')
            ->columnSpan([
                '@md' => 2,
                '@xl' => 3,
            ])
            ->columnOrder([
                'default' => 2,
                '@xl' => 1,
            ]),
        TextInput::make('email')
            ->columnOrder([
                'default' => 1,
                '@xl' => 2,
            ]),
        // ...
    ])
```

### Fallback Breakpoints

Support browsers without container query support using `!@` prefix:

```php
Grid::make()
    ->gridContainer()
    ->columns([
        '@md' => 3,
        '@xl' => 4,
        '!@md' => 2,  // Viewport fallback
        '!@xl' => 3,  // Viewport fallback
    ])
    ->schema([
        // ...
    ])
```

### Combined Container and Fallback Breakpoints

```php
Grid::make()
    ->gridContainer()
    ->columns([
        '@md' => 3,
        '@xl' => 4,
        '!@md' => 2,
        '!@xl' => 3,
    ])
    ->schema([
        TextInput::make('name')
            ->columnSpan([
                '@md' => 2,
                '@xl' => 3,
                '!@md' => 2,
                '!@xl' => 2,
            ])
            ->columnOrder([
                'default' => 2,
                '@xl' => 1,
                '!@xl' => 1,
            ]),
        TextInput::make('email')
            ->columnOrder([
                'default' => 1,
                '@xl' => 2,
                '!@xl' => 2,
            ]),
        // ...
    ])
```

---

## Component Spacing

### Dense Layout

Reduce spacing by 50%:

```php
Grid::make()
    ->dense()
    ->schema([
        // ...
    ])
```

### Remove All Spacing

```php
Grid::make()
    ->gap(false)
    ->schema([
        // ...
    ])
```

### Custom Attributes for Styling

Add custom CSS classes or attributes:

```php
Section::make()
    ->extraAttributes(['class' => 'custom-section-style'])
```

---

## Inline Labels

### Enable Inline Labels on Schema

Display all labels inline throughout the schema:

```php
use Filament\Schemas\Schema;

public function form(Schema $schema): Schema
{
    return $schema
        ->inlineLabel()
        ->components([
            // ...
        ]);
}
```

For infolists:

```php
public function infolist(Schema $schema): Schema
{
    return $schema
        ->inlineLabel()
        ->components([
            // ...
        ]);
}
```

### Inline Labels on Section

Apply inline labels to all fields in a section:

```php
Section::make('Details')
    ->inlineLabel()
    ->schema([
        TextInput::make('name'),
        TextInput::make('email')
            ->label('Email address'),
        TextInput::make('phone')
            ->label('Phone number'),
    ])
```

### Override Inline Labels on Individual Fields

Opt out of inline labels for specific fields:

```php
Section::make('Details')
    ->inlineLabel()
    ->schema([
        TextInput::make('name'),
        TextInput::make('email')
            ->label('Email address'),
        TextInput::make('phone')
            ->label('Phone number')
            ->inlineLabel(false),  // Label above field
    ])
```

---

## Collapsible Components

### Collapsible Sections

```php
Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
    ->collapsed()  // Collapsed by default
    ->persistCollapsed()  // Remember state in local storage
```

### Collapsible Panels in Tables

```php
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

### Expand Panel by Default

```php
Panel::make([
    Split::make([
        TextColumn::make('phone')
            ->icon('heroicon-m-phone'),
        TextColumn::make('email')
            ->icon('heroicon-m-envelope'),
    ])->from('md'),
])->collapsed(false)
```

### Collapsible Repeater Items

```php
use Filament\Forms\Components\Repeater;

Repeater::make('qualifications')
    ->schema([
        // ...
    ])
    ->collapsible()
    ->collapsed()
```

Conditional collapsibility:

```php
Repeater::make('qualifications')
    ->schema([
        // ...
    ])
    ->collapsible(FeatureFlag::active())
    ->collapsed(FeatureFlag::active())
```

---

## Global Configuration

### Configure Component Defaults Globally

Use `configureUsing()` in a service provider's `boot()` method:

```php
use Filament\Schemas\Components\Section;

Section::configureUsing(function (Section $section): void {
    $section
        ->columns(2);
});
```

### Override Global Configuration

Individual instances can override global settings:

```php
Section::make()
    ->columns(1)  // Overrides global default of 2
```

### Global Configuration Examples

#### All Sections Full Width

```php
use Filament\Schemas\Components\Section;

Section::configureUsing(fn (Section $section) => $section
    ->columnSpanFull());
```

#### All Grids Dense by Default

```php
use Filament\Schemas\Components\Grid;

Grid::configureUsing(fn (Grid $grid) => $grid
    ->dense());
```

#### All Sections Collapsible

```php
Section::configureUsing(fn (Section $section) => $section
    ->collapsible());
```

### Global Table Configuration

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

---

## Custom Components

### Create Custom Layout Component

```php
use Filament\Schemas\Components\Component;

class Chart extends Component
{
    protected string $view = 'filament.schemas.components.chart';

    public static function make(): static
    {
        return app(static::class);
    }
}
```

### Add Configuration Methods

```php
class Chart extends Component
{
    protected string $view = 'filament.schemas.components.chart';
    protected ?string $heading = null;

    public static function make(): static
    {
        return app(static::class);
    }

    public function heading(?string $heading): static
    {
        $this->heading = $heading;
        return $this;
    }

    public function getHeading(): ?string
    {
        return $this->heading;
    }
}
```

### Blade Template for Custom Component

```blade
<div>
    {{ $getHeading() }}
</div>
```

### Using Custom Component

```php
use App\Filament\Schemas\Components\Chart;

Chart::make()
    ->heading('Sales')
```

### Custom Component with Child Schema

```php
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\View;

View::make('filament.schemas.components.chart')
    ->schema([
        TextInput::make('subtotal'),
        TextInput::make('total'),
    ])
```

Render child schema in Blade:

```blade
<div>
    {{ $getChildSchema() }}
</div>
```

### Custom View Component in Tables

```php
use Filament\Tables\Columns\Layout\View;
use Filament\Tables\Columns\TextColumn;

View::make('users.table.collapsible-row-content')
    ->collapsible()
```

With embedded components:

```php
View::make('users.table.collapsible-row-content')
    ->components([
        TextColumn::make('email')
            ->icon('heroicon-m-envelope'),
    ])
    ->collapsible()
```

Blade template:

```blade
<div class="px-4 py-3 bg-gray-100 rounded-lg">
    @foreach ($getComponents() as $layoutComponent)
        {{ $layoutComponent
            ->record($getRecord())
            ->recordKey($getRecordKey())
            ->rowLoop($getRowLoop())
            ->renderInLayout() }}
    @endforeach
</div>
```

---

## Advanced Patterns

### Dynamic Field Sets Based on Selection

Render different components based on a select field:

```php
use Filament\Forms\Components\FileUpload;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Utilities\Get;

Select::make('type')
    ->options([
        'employee' => 'Employee',
        'freelancer' => 'Freelancer'
    ])
    ->live()
    ->afterStateUpdated(fn (Select $component) => $component
        ->getContainer()
        ->getComponent('dynamicTypeFields')
        ->getChildSchema()
        ->fill());
    
Grid::make(2)
    ->schema(fn (Get $get): array => match ($get('type')) {
        'employee' => [
            TextInput::make('employee_number')
                ->required(),
            FileUpload::make('badge')
                ->image()
                ->required()
        ],
        'freelancer' => [
            TextInput::make('hourly_rate')
                ->numeric()
                ->required()
                ->prefix('€'),
            FileUpload::make('contract')
                ->required()
        ],
        default => []
    })
    ->key('dynamicTypeFields');
```

### FusedGroup for Inline Fields

Group fields horizontally without gaps:

```php
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\FusedGroup;

FusedGroup::make([
    TextInput::make('city')
        ->placeholder('City')
        ->columnSpan(2),
    Select::make('country')
        ->placeholder('Country')
        ->options([
            // ...
        ]),
])
    ->label('Location')
    ->columns(3)
```

### Filter Form Schema Customization

```php
use Filament\Schemas\Components\Section;
use Filament\Tables\Filters\Filter;
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->filters([
            Filter::make('is_featured'),
            Filter::make('published_at'),
            Filter::make('author'),
        ])
        ->filtersFormColumns(2)
        ->filtersFormSchema(fn (array $filters): array => [
            Section::make('Visibility')
                ->description('These filters affect the visibility of the records in the table.')
                ->schema([
                    $filters['is_featured'],
                    $filters['published_at'],
                ])
                ->columns(2)
                ->columnSpanFull(),
            $filters['author'],
        ]);
}
```

### Repeater with Grid Layout

```php
Repeater::make('qualifications')
    ->schema([
        // ...
    ])
    ->grid(2)
```

Dynamic grid with closures:

```php
Repeater::make('qualifications')
    ->schema([
        // ...
    ])
    ->grid(fn (Get $get) => $get('type') === 'detailed' ? 3 : 2)
```

### Widget Grid Configuration

```php
public function getHeaderWidgetsColumns(): int | array
{
    return [
        'md' => 4,
        'xl' => 5,
    ];
}
```

### Responsive Widget Column Span

```php
protected int | string | array $columnSpan = [
    'md' => 2,
    'xl' => 3,
];
```

---

## Troubleshooting

### Issue: Layout Components Not Spanning Full Width

**Problem:** In v4, Grid/Section/Fieldset only consume one column by default.

**Solution:**
```php
Section::make()
    ->columnSpanFull()
```

Or configure globally:
```php
Section::configureUsing(fn (Section $section) => $section->columnSpanFull());
```

### Issue: Responsive Breakpoints Not Working

**Problem:** Layout doesn't adjust at expected screen sizes.

**Checklist:**
1. Verify breakpoint syntax: `'md' => 2`, not `md: 2`
2. Check parent container has grid configured
3. Ensure proper column spans defined
4. Test with browser dev tools to verify actual viewport size

### Issue: Container Breakpoints Not Applying

**Problem:** Container-based responsive layout not working.

**Solution:**
1. Enable grid container:
```php
Grid::make()->gridContainer()
```

2. Use `@` prefix for container breakpoints:
```php
->columns(['@md' => 3, '@xl' => 4])
```

3. Add fallback breakpoints for browser compatibility:
```php
->columns([
    '@md' => 3,
    '!@md' => 2,  // Fallback
])
```

### Issue: Column Order Not Changing

**Problem:** `columnOrder()` doesn't affect layout.

**Causes:**
- Missing breakpoint in parent grid configuration
- Conflicting CSS styles
- Not enough columns in grid

**Solution:**
```php
Grid::make()
    ->columns(['default' => 1, 'lg' => 3])  // Define columns first
    ->schema([
        TextInput::make('first')->columnOrder(['default' => 1, 'lg' => 3]),
        TextInput::make('second')->columnOrder(['default' => 2, 'lg' => 1]),
        TextInput::make('third')->columnOrder(['default' => 3, 'lg' => 2]),
    ])
```

### Issue: Inline Labels Not Displaying

**Problem:** Labels still appear above fields.

**Solutions:**

Check schema-level setting:
```php
$schema->inlineLabel()
```

Check section-level setting:
```php
Section::make()->inlineLabel()
```

Override for specific field:
```php
TextInput::make('name')->inlineLabel(false)
```

### Issue: Section Not Collapsible

**Problem:** Section doesn't collapse when clicked.

**Solution:**
```php
Section::make()
    ->collapsible()  // Must add this
    ->collapsed()    // Optional: start collapsed
```

### Issue: Dynamic Columns Not Updating

**Problem:** Closure for `columns()` not re-evaluating.

**Solution:** Add `->live()` to trigger field:
```php
Select::make('layout')
    ->live()
    ->options(['compact' => 'Compact', 'wide' => 'Wide']);

Grid::make()
    ->columns(fn (Get $get) => $get('layout') === 'wide' ? 4 : 2)
```

### Issue: Tabs Not Switching

**Problem:** Clicking tabs doesn't change active tab.

**Checklist:**
- Ensure each tab has unique label
- Check JavaScript console for errors
- Verify tabs are inside `Tabs::make()` component
- Test with minimal schema first

### Issue: Custom Component Not Rendering

**Problem:** Custom component shows blank or error.

**Checklist:**
1. Verify view path exists: `resources/views/filament/schemas/components/chart.blade.php`
2. Check view property matches path:
```php
protected string $view = 'filament.schemas.components.chart';
```
3. Ensure `make()` method returns instance:
```php
public static function make(): static
{
    return app(static::class);
}
```

### Performance: Large Forms Loading Slowly

**Optimizations:**

1. Use deferred loading for heavy sections:
```php
Section::make()
    ->defer()
```

2. Reduce unnecessary reactive fields (remove `->live()` if not needed)

3. Split into wizard steps:
```php
Wizard::make([
    Step::make('Basic')->schema([...]),
    Step::make('Advanced')->schema([...]),
])
```

4. Use tabs for related but independent sections:
```php
Tabs::make()->tabs([
    Tab::make('General')->schema([...]),
    Tab::make('Advanced')->schema([...]),
])
```

---

## Cross-References

### Related Topics

- **[FORMS.md](FORMS.md)** - Form components that work within schemas
- **[TABLES.md](TABLES.md)** - Table layout components (Grid, Split, Stack, Panel)
- **[INFOLISTS.md](INFOLISTS.md)** - Infolist entries with schema layouts
- **[ACTIONS.md](ACTIONS.md)** - Actions that can be embedded in sections/headers
- **[PANEL_CONFIGURATION.md](PANEL_CONFIGURATION.md)** - Global panel layout settings
- **[CODE_QUALITY.md](CODE_QUALITY.md)** - Patterns for organizing schema classes
- **[TESTING.md](TESTING.md)** - Testing schema components

### Component Integration

**Schemas work with:**
- Form components (TextInput, Select, FileUpload, etc.)
- Infolist entries (TextEntry, IconEntry, etc.)
- Table columns (when using layout components)
- Actions (in headers, footers, modals)
- Widgets (for dashboard layouts)

### Best Practices

1. **Separate Schema Classes** - Extract complex schemas into dedicated classes
2. **Use Global Configuration** - Set consistent defaults via `configureUsing()`
3. **Mobile-First Design** - Define base layout for mobile, enhance for desktop
4. **Semantic Grouping** - Use sections/fieldsets for related fields
5. **Progressive Enhancement** - Start simple, add complexity where needed
6. **Test Responsive Layouts** - Verify appearance at all breakpoints
7. **Minimize Nesting** - Keep schema depth reasonable for maintainability
8. **Document Complex Patterns** - Add comments for dynamic schemas

---

## FilamentPHP 4.x Documentation

- [Official Schemas Overview](https://filamentphp.com/docs/4.x/schemas/overview)
- [Grid Layouts](https://filamentphp.com/docs/4.x/schemas/layouts)
- [Sections](https://filamentphp.com/docs/4.x/schemas/sections)
- [Tabs](https://filamentphp.com/docs/4.x/schemas/tabs)
- [Wizards](https://filamentphp.com/docs/4.x/schemas/wizards)
- [Custom Components](https://filamentphp.com/docs/4.x/schemas/custom-components)
- [v4 Upgrade Guide](https://filamentphp.com/docs/4.x/upgrade-guide)

---

**Version:** 1.0.0  
**Last Updated:** January 18, 2026  
**FilamentPHP Version:** 4.x  
**Status:** Complete
