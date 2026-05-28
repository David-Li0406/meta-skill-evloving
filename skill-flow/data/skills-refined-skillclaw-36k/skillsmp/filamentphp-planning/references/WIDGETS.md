# FilamentPHP 4.x Widgets Reference

## Table of Contents

1. [Overview](#overview)
2. [Widget Types](#widget-types)
3. [Stats Overview Widgets](#stats-overview-widgets)
4. [Chart Widgets](#chart-widgets)
5. [Table Widgets](#table-widgets)
6. [Custom Widgets](#custom-widgets)
7. [Widget Positioning and Layout](#widget-positioning-and-layout)
8. [Polling and Refresh](#polling-and-refresh)
9. [Dashboard Configuration](#dashboard-configuration)
10. [Dashboard Filters](#dashboard-filters)
11. [Resource Widgets](#resource-widgets)
12. [Widget-Page Interaction](#widget-page-interaction)
13. [Advanced Customization](#advanced-customization)
14. [Testing Widgets](#testing-widgets)
15. [Troubleshooting](#troubleshooting)
16. [Cross-References](#cross-references)

---

## Overview

FilamentPHP widgets are reusable components that display summary information, charts, tables, or custom content on dashboards and resource pages. Widgets provide a modular way to compose informational panels across your admin interface.

### When to Use Widgets

- **Dashboard metrics**: Display key performance indicators (KPIs)
- **Data visualization**: Show charts and graphs
- **Quick summaries**: Present recent activity or important records
- **Custom components**: Embed specialized UI elements
- **Resource insights**: Add context to resource list/edit pages

### Key Features

- Multiple widget types: stats, charts, tables, custom
- Automatic polling for real-time updates
- Responsive grid layout system
- Dashboard-wide filters
- Resource page integration
- Custom Livewire components
- Collapsible and customizable

---

## Widget Types

FilamentPHP provides four main widget types:

### 1. Stats Overview Widgets

Display numeric metrics with descriptions, icons, and charts:

```php
<?php

namespace App\Filament\Widgets;

use Filament\Widgets\StatsOverviewWidget as BaseWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class StatsOverview extends BaseWidget
{
    protected function getStats(): array
    {
        return [
            Stat::make('Unique views', '192.1k'),
            Stat::make('Bounce rate', '21%'),
            Stat::make('Average time on page', '3:12'),
        ];
    }
}
```

### 2. Chart Widgets

Display data visualization using Chart.js:

```php
<?php

namespace App\Filament\Widgets;

use Filament\Widgets\ChartWidget;

class BlogPostsChart extends ChartWidget
{
    protected ?string $heading = 'Blog Posts';

    protected function getData(): array
    {
        return [
            'datasets' => [
                [
                    'label' => 'Blog posts created',
                    'data' => [0, 10, 5, 2, 21, 32, 45, 74, 65, 45, 77, 89],
                ],
            ],
            'labels' => ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        ];
    }

    protected function getType(): string
    {
        return 'line';
    }
}
```

### 3. Table Widgets

Display tabular data on dashboards:

```bash
php artisan make:filament-widget LatestOrders --table
```

### 4. Custom Widgets

Create custom Livewire components:

```bash
php artisan make:filament-widget BlogPostsOverview
```

---

## Stats Overview Widgets

### Creating a Stats Widget

Generate with Artisan:

```bash
php artisan make:filament-widget StatsOverview --stats-overview
```

### Basic Stats

Create simple metric cards:

```php
<?php

namespace App\Filament\Widgets;

use Filament\Widgets\StatsOverviewWidget as BaseWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class StatsOverview extends BaseWidget
{
    protected function getStats(): array
    {
        return [
            Stat::make('Unique views', '192.1k'),
            Stat::make('Bounce rate', '21%'),
            Stat::make('Average time on page', '3:12'),
        ];
    }
}
```

### Adding Descriptions and Icons

Enhance stats with contextual information:

```php
use Filament\Widgets\StatsOverviewWidget\Stat;

protected function getStats(): array
{
    return [
        Stat::make('Unique views', '192.1k')
            ->description('32k increase')
            ->descriptionIcon('heroicon-m-arrow-trending-up'),
        Stat::make('Bounce rate', '21%')
            ->description('7% decrease')
            ->descriptionIcon('heroicon-m-arrow-trending-down'),
        Stat::make('Average time on page', '3:12')
            ->description('3% increase')
            ->descriptionIcon('heroicon-m-arrow-trending-up'),
    ];
}
```

### Controlling Icon Position

Position icons before or after description:

```php
use Filament\Support\Enums\IconPosition;
use Filament\Widgets\StatsOverviewWidget\Stat;

Stat::make('Unique views', '192.1k')
    ->description('32k increase')
    ->descriptionIcon('heroicon-m-arrow-trending-up', IconPosition::Before);
```

### Setting Stat Colors

Apply semantic colors to stats:

```php
use Filament\Widgets\StatsOverviewWidget\Stat;

protected function getStats(): array
{
    return [
        Stat::make('Unique views', '192.1k')
            ->description('32k increase')
            ->descriptionIcon('heroicon-m-arrow-trending-up')
            ->color('success'),
        Stat::make('Bounce rate', '21%')
            ->description('7% increase')
            ->descriptionIcon('heroicon-m-arrow-trending-down')
            ->color('danger'),
        Stat::make('Average time on page', '3:12')
            ->description('3% increase')
            ->descriptionIcon('heroicon-m-arrow-trending-up')
            ->color('success'),
    ];
}
```

Available colors: `success`, `warning`, `danger`, `info`, `gray`, `primary`

### Adding Charts to Stats

Visualize trends within stat cards:

```php
use Filament\Widgets\StatsOverviewWidget\Stat;

protected function getStats(): array
{
    return [
        Stat::make('Unique views', '192.1k')
            ->description('32k increase')
            ->descriptionIcon('heroicon-m-arrow-trending-up')
            ->chart([7, 2, 10, 3, 15, 4, 17])
            ->color('success'),
        // ...
    ];
}
```

The chart data is an array of numeric values visualized as a sparkline.

### Custom HTML Attributes for Stats

Add interactivity with Livewire directives:

```php
use Filament\Widgets\StatsOverviewWidget\Stat;

protected function getStats(): array
{
    return [
        Stat::make('Processed', '192.1k')
            ->color('success')
            ->extraAttributes([
                'class' => 'cursor-pointer',
                'wire:click' => "\$dispatch('setStatusFilter', { filter: 'processed' })",
            ]),
        // ...
    ];
}
```

This makes the stat clickable and dispatches a Livewire event.

---

## Chart Widgets

### Creating a Chart Widget

Generate with Artisan:

```bash
php artisan make:filament-widget BlogPostsChart --chart
```

### Basic Line Chart

```php
<?php

namespace App\Filament\Widgets;

use Filament\Widgets\ChartWidget;

class BlogPostsChart extends ChartWidget
{
    protected ?string $heading = 'Blog Posts';

    protected function getData(): array
    {
        return [
            'datasets' => [
                [
                    'label' => 'Blog posts created',
                    'data' => [0, 10, 5, 2, 21, 32, 45, 74, 65, 45, 77, 89],
                ],
            ],
            'labels' => ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        ];
    }

    protected function getType(): string
    {
        return 'line';
    }
}
```

Supported chart types: `line`, `bar`, `pie`, `doughnut`, `polarArea`, `radar`, `scatter`, `bubble`

### Adding Chart Description

Provide context below the heading:

```php
public function getDescription(): ?string
{
    return 'The number of blog posts published per month.';
}
```

### Customizing Chart Colors

Apply custom colors to datasets:

```php
protected function getData(): array
{
    return [
        'datasets' => [
            [
                'label' => 'Blog posts created',
                'data' => [0, 10, 5, 2, 21, 32, 45, 74, 65, 45, 77, 89],
                'backgroundColor' => '#36A2EB',
                'borderColor' => '#9BD0F5',
            ],
        ],
        'labels' => ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    ];
}
```

### Setting Predefined Chart Color

Use Filament's color system:

```php
protected string $color = 'info';
```

### Chart Filters

Add dropdown filters for dynamic data:

```php
protected function getFilters(): ?array
{
    return [
        'today' => 'Today',
        'week' => 'Last week',
        'month' => 'Last month',
        'year' => 'This year',
    ];
}
```

Set default filter:

```php
public ?string $filter = 'today';
```

Access filter in `getData()`:

```php
protected function getData(): array
{
    $activeFilter = $this->filter;

    // Query data based on $activeFilter...

    return [
        // ...
    ];
}
```

### Schema-Based Filters

Use form components for complex filters:

```php
use Filament\Forms\Components\DatePicker;
use Filament\Schemas\Schema;
use Filament\Widgets\ChartWidget\Concerns\HasFiltersSchema;

class BlogPostsChart extends ChartWidget
{
    use HasFiltersSchema;
    
    // ...
    
    public function filtersSchema(Schema $schema): Schema
    {
        return $schema->components([
            DatePicker::make('startDate')
                ->default(now()->subDays(30)),
            DatePicker::make('endDate')
                ->default(now()),
        ]);
    }
}
```

Access filter values:

```php
protected function getData(): array
{
    $startDate = $this->filters['startDate'] ?? null;
    $endDate = $this->filters['endDate'] ?? null;

    // Query data...

    return [
        // ...
    ];
}
```

**Note**: Filter values are live but unvalidated.

### Dynamic Data from Eloquent Models

Use the `flowframe/laravel-trend` package:

```bash
composer require flowframe/laravel-trend
```

```php
use Flowframe/Trend\Trend;
use Flowframe\Trend\TrendValue;

protected function getData(): array
{
    $data = Trend::model(BlogPost::class)
        ->between(
            start: now()->startOfYear(),
            end: now()->endOfYear(),
        )
        ->perMonth()
        ->count();

    return [
        'datasets' => [
            [
                'label' => 'Blog posts',
                'data' => $data->map(fn (TrendValue $value) => $value->aggregate),
            ],
        ],
        'labels' => $data->map(fn (TrendValue $value) => $value->date),
    ];
}
```

### Chart.js Options (Static)

Configure Chart.js via property:

```php
protected ?array $options = [
    'plugins' => [
        'legend' => [
            'display' => false,
        ],
    ],
];
```

### Chart.js Options (Dynamic)

Use method for conditional configuration:

```php
protected function getOptions(): array
{
    return [
        'plugins' => [
            'legend' => [
                'display' => false,
            ],
        ],
    ];
}
```

### Raw JavaScript in Options

Use `RawJs` for JavaScript callbacks:

```php
use Filament\Support\RawJs;

protected function getOptions(): RawJs
{
    return RawJs::make(<<<JS
        {
            scales: {
                y: {
                    ticks: {
                        callback: (value) => '€' + value,
                    },
                },
            },
        }
    JS);
}
```

### Setting Maximum Chart Height

Limit chart size:

```php
protected ?string $maxHeight = '300px';
```

### Collapsible Charts

Allow users to collapse charts:

```php
protected bool $isCollapsible = true;
```

### Chart.js Plugins

Install a plugin with NPM:

```bash
npm install chartjs-plugin-datalabels --save-dev
```

Create `resources/js/filament-chart-js-plugins.js`:

```javascript
import ChartDataLabels from 'chartjs-plugin-datalabels'

window.filamentChartJsPlugins ??= []
window.filamentChartJsPlugins.push(ChartDataLabels)
```

For global plugins:

```javascript
import ChartDataLabels from 'chartjs-plugin-datalabels'

window.filamentChartJsGlobalPlugins ??= []
window.filamentChartJsGlobalPlugins.push(ChartDataLabels)
```

Configure Vite (`vite.config.js`):

```javascript
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: [
                'resources/css/app.css',
                'resources/js/app.js',
                'resources/css/filament/admin/theme.css',
                'resources/js/filament-chart-js-plugins.js',
            ],
        }),
    ],
});
```

Register in service provider:

```php
use Filament\Support\Assets\Js;
use Filament\Support\Facades\FilamentAsset;
use Illuminate\Support\Facades\Vite;

FilamentAsset::register([
    Js::make('chart-js-plugins', Vite::asset('resources/js/filament-chart-js-plugins.js'))->module(),
]);
```

---

## Table Widgets

### Creating a Table Widget

Generate with Artisan:

```bash
php artisan make:filament-widget LatestOrders --table
```

Table widgets use the same table builder as resources, supporting all table features: columns, filters, actions, etc.

---

## Custom Widgets

### Creating a Custom Widget

Generate with Artisan:

```bash
php artisan make:filament-widget BlogPostsOverview
```

This creates a widget class and Blade view.

### Widget Class

```php
<?php

namespace App\Filament\Widgets;

use Filament\Widgets\Widget;

class BlogPostsOverview extends Widget
{
    protected static string $view = 'filament.widgets.blog-posts-overview';
}
```

### Widget View

Create `resources/views/filament/widgets/blog-posts-overview.blade.php`:

```blade
<x-filament-widgets::widget>
    <x-filament::section>
        <div>
            {{-- Widget content --}}
        </div>
    </x-filament::section>
</x-filament-widgets::widget>
```

You can use any Livewire features in the widget class and view.

---

## Widget Positioning and Layout

### Setting Widget Sort Order

Control display order:

```php
protected static ?int $sort = 2;
```

Widgets with lower sort numbers appear first.

### Setting Column Span (Fixed)

Make widget span multiple columns:

```php
protected int | string | array $columnSpan = 'full';
```

Or specify a number (1-12):

```php
protected int | string | array $columnSpan = 2;
```

### Setting Column Span (Responsive)

Different spans at different breakpoints:

```php
protected int | string | array $columnSpan = [
    'md' => 2,
    'xl' => 3,
];
```

### Configuring Dashboard Grid Columns (Fixed)

In your custom dashboard:

```php
public function getColumns(): int | array
{
    return 2;
}
```

### Configuring Dashboard Grid Columns (Responsive)

Different column counts at different breakpoints:

```php
public function getColumns(): int | array
{
    return [
        'md' => 4,
        'xl' => 5,
    ];
}
```

---

## Polling and Refresh

### Enabling Polling for Stats

Auto-refresh at intervals (default: 5 seconds):

```php
protected ?string $pollingInterval = '10s';
```

### Disabling Polling

Prevent automatic refresh:

```php
protected ?string $pollingInterval = null;
```

### Table Polling

Enable table content refresh:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->poll('10s');
}
```

---

## Dashboard Configuration

### Creating a Custom Dashboard

Extend the base dashboard:

```php
<?php

namespace App\Filament\Pages;

use Filament\Pages\Dashboard as BaseDashboard;

class Dashboard extends BaseDashboard
{
    // ...
}
```

### Manually Registering Custom Dashboard

If not auto-discovered:

```php
use App\Filament\Pages\Dashboard;
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->pages([
            Dashboard::class,
        ]);
}
```

### Removing Original Dashboard

Prevent conflicts:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->discoverPages(in: app_path('Filament/Pages'), for: 'App\\Filament\\Pages')
        ->pages([]);
}
```

### Customizing Dashboard Title

```php
protected static ?string $title = 'Finance dashboard';
```

### Setting Dashboard Route Path

```php
protected static string $routePath = 'finance';
```

This makes the dashboard accessible at `/admin/finance`.

### Setting Dashboard Navigation Sort

```php
protected static ?int $navigationSort = 15;
```

### Disabling Default Widgets

Remove Filament's default widgets:

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        // ...
        ->widgets([]);
}
```

### Customizing Widget Grid Columns

On resource pages:

```php
public function getHeaderWidgetsColumns(): int | array
{
    return 3;
}
```

Responsive:

```php
public function getHeaderWidgetsColumns(): int | array
{
    return [
        'md' => 4,
        'xl' => 5,
    ];
}
```

### Widget Headings and Descriptions

Override properties:

```php
protected ?string $heading = 'Analytics';

protected ?string $description = 'An overview of some analytics.';
```

Or use methods:

```php
protected function getHeading(): ?string
{
    return 'Analytics';
}

protected function getDescription(): ?string
{
    return 'An overview of some analytics.';
}
```

---

## Dashboard Filters

### Filters Form

Add dashboard-wide filtering:

```php
use Filament\Forms\Components\DatePicker;
use Filament\Pages\Dashboard as BaseDashboard;
use Filament\Pages\Dashboard\Concerns\HasFiltersForm;
use Filament\Schemas\Components\Section;
use Filament\Schemas\Schema;

class Dashboard extends BaseDashboard
{
    use HasFiltersForm;

    public function filtersForm(Schema $schema): Schema
    {
        return $schema
            ->components([
                Section::make()
                    ->schema([
                        DatePicker::make('startDate'),
                        DatePicker::make('endDate'),
                        // ...
                    ])
                    ->columns(3),
            ]);
    }
}
```

### Accessing Filter Values in Widgets

Use the `InteractsWithPageFilters` trait:

```php
use App\Models\BlogPost;
use Carbon\CarbonImmutable;
use Filament\Widgets\StatsOverviewWidget;
use Filament\Widgets\Concerns\InteractsWithPageFilters;
use Illuminate\Database\Eloquent\Builder;

class BlogPostsOverview extends StatsOverviewWidget
{
    use InteractsWithPageFilters;

    public function getStats(): array
    {
        $startDate = $this->pageFilters['startDate'] ?? null;
        $endDate = $this->pageFilters['endDate'] ?? null;

        return [
            StatsOverviewWidget\Stat::make(
                label: 'Total posts',
                value: BlogPost::query()
                    ->when($startDate, fn (Builder $query) => $query->whereDate('created_at', '>=', $startDate))
                    ->when($endDate, fn (Builder $query) => $query->whereDate('created_at', '<=', $endDate))
                    ->count(),
            ),
            // ...
        ];
    }
}
```

### Filter Action Modal

Replace form with modal for better performance:

```php
use Filament\Forms\Components\DatePicker;
use Filament\Pages\Dashboard as BaseDashboard;
use Filament\Pages\Dashboard\Actions\FilterAction;
use Filament\Pages\Dashboard\Concerns\HasFiltersAction;

class Dashboard extends BaseDashboard
{
    use HasFiltersAction;
    
    protected function getHeaderActions(): array
    {
        return [
            FilterAction::make()
                ->schema([
                    DatePicker::make('startDate'),
                    DatePicker::make('endDate'),
                    // ...
                ]),
        ];
    }
}
```

This defers widget reloads until "Apply" is clicked.

### Controlling Filter Persistence (Property)

Disable session persistence:

```php
use Filament\Pages\Dashboard as BaseDashboard;
use Filament\Pages\Dashboard\Concerns\HasFiltersForm;

class Dashboard extends BaseDashboard
{
    use HasFiltersForm;

    protected bool $persistsFiltersInSession = false;
}
```

### Controlling Filter Persistence (Method)

```php
use Filament\Pages\Dashboard as BaseDashboard;
use Filament\Pages\Dashboard\Concerns\HasFiltersForm;

class Dashboard extends BaseDashboard
{
    use HasFiltersForm;

    public function persistsFiltersInSession(): bool
    {
        return false;
    }
}
```

---

## Resource Widgets

### Creating a Resource Widget

Generate scoped to a resource:

```bash
php artisan make:filament-widget CustomerOverview --resource=CustomerResource
```

### Registering Resource Widgets

In the resource class:

```php
use App\Filament\Resources\Customers\Widgets\CustomerOverview;

public static function getWidgets(): array
{
    return [
        CustomerOverview::class,
    ];
}
```

### Displaying Widgets on Resource Pages

In the page class:

```php
<?php

namespace App\Filament\Resources\Customers\Pages;

use App\Filament\Resources\Customers\CustomerResource;

class ListCustomers extends ListRecords
{
    public static string $resource = CustomerResource::class;

    protected function getHeaderWidgets(): array
    {
        return [
            CustomerResource\Widgets\CustomerOverview::class,
        ];
    }
}
```

Also available: `getFooterWidgets()`

### Passing Data to Widgets

During registration:

```php
protected function getHeaderWidgets(): array
{
    return [
        CustomerResource\Widgets\CustomerOverview::make([
            'status' => 'active',
        ]),
    ];
}
```

In the widget:

```php
use Filament\Widgets\Widget;

class CustomerOverview extends Widget
{
    public string $status;

    // ...
}
```

From page using `getWidgetData()`:

```php
public function getWidgetData(): array
{
    return [
        'stats' => [
            'total' => 100,
        ],
    ];
}
```

Widget receives it automatically:

```php
public $stats = [];
```

---

## Widget-Page Interaction

### Accessing Current Record in Widgets

On Edit/View pages:

```php
use Illuminate\Database\Eloquent\Model;

public ?Model $record = null;
```

Filament automatically injects the current record.

### Accessing Table Data from Widgets

Enable in the List page:

```php
use Filament\Pages\Concerns\ExposesTableToWidgets;
use Filament\Resources\Pages\ListRecords;

class ListProducts extends ListRecords
{
    use ExposesTableToWidgets;

    // ...
}
```

In the widget:

```php
use App\Filament\Resources\Products\Pages\ListProducts;
use Filament\Widgets\Concerns\InteractsWithPageTable;
use Filament\Widgets\Widget;

class ProductStats extends Widget
{
    use InteractsWithPageTable;

    protected function getTablePage(): string
    {
        return ListProducts::class;
    }

    // ...
}
```

### Available Table Methods

```php
// Total count across all pages
$this->tableRecordsCount

// Current page records
$this->getPageTableRecords()

// Eloquent query builder
$this->getPageTableQuery()
```

Example usage:

```php
use Filament\Widgets\StatsOverviewWidget\Stat;

Stat::make('Total Products', $this->tableRecordsCount),

Stat::make('Total Products', $this->getPageTableRecords()->count()),

Stat::make('Total Products', $this->getPageTableQuery()->count()),
```

---

## Advanced Customization

### Conditional Widget Visibility

Control widget display:

```php
public static function canView(): bool
{
    return auth()->user()->isAdmin();
}
```

### Collapsible Widgets

Make widgets collapsible:

```php
protected bool $isCollapsible = true;
```

---

## Testing Widgets

### Verifying Package Installation

```bash
composer show filament/widgets
```

### Rendering Widgets in Blade

```php
<div>
    @livewire(\App\Livewire\Dashboard\PostsChart::class)
</div>
```

---

## Troubleshooting

### Widget Not Displaying

**Issue**: Widget doesn't appear on dashboard.

**Solutions**:
1. Ensure widget is registered in panel or resource
2. Check `canView()` doesn't return false
3. Verify namespace matches file location
4. Run `php artisan filament:upgrade` to regenerate cache
5. Check widget sort order isn't pushing it off-screen

### Polling Not Working

**Issue**: Widget doesn't auto-refresh.

**Solutions**:
1. Verify `$pollingInterval` is set correctly
2. Ensure Livewire is properly loaded
3. Check browser console for JavaScript errors
4. Test with a shorter interval (e.g., '5s')
5. Confirm `poll()` method syntax is correct

### Chart Not Rendering

**Issue**: Chart widget shows blank or errors.

**Solutions**:
1. Verify Chart.js is loaded (check browser network tab)
2. Ensure `getData()` returns proper structure
3. Check `getType()` returns valid chart type
4. Validate data array doesn't contain null values
5. Check browser console for Chart.js errors
6. Ensure `$maxHeight` isn't set too small

### Dashboard Filters Not Working

**Issue**: Filter values don't affect widget data.

**Solutions**:
1. Ensure widgets use `InteractsWithPageFilters` trait
2. Verify filter keys match what widgets expect
3. Check dashboard uses `HasFiltersForm` trait
4. Confirm `$this->pageFilters` is accessed correctly
5. Test with static filter values first
6. Remember filter data is unvalidated

### Widget Data Not Updating

**Issue**: Widget shows stale data after changes.

**Solutions**:
1. Enable polling if real-time updates needed
2. Dispatch browser events to refresh: `$this->dispatch('refresh-sidebar')`
3. Check if data is cached in widget properties
4. Verify Eloquent queries aren't cached
5. Clear application cache: `php artisan cache:clear`

### Custom Widget View Not Found

**Issue**: "View not found" error for custom widget.

**Solutions**:
1. Verify view path in `$view` property matches file location
2. Check view file is in `resources/views/` directory
3. Ensure namespace uses dot notation correctly
4. Run `php artisan view:clear`
5. Check for typos in view path

### Chart.js Plugin Not Loading

**Issue**: Chart.js plugin features don't work.

**Solutions**:
1. Verify NPM package is installed
2. Ensure Vite config includes plugin file
3. Check FilamentAsset registration in service provider
4. Run `npm run build` to compile assets
5. Clear browser cache and reload
6. Verify plugin syntax matches documentation

### Widget Layout Issues

**Issue**: Widgets overlapping or not responsive.

**Solutions**:
1. Check `$columnSpan` is set correctly
2. Verify dashboard `getColumns()` configuration
3. Test with `columnSpan = 'full'` first
4. Ensure responsive arrays use correct breakpoints
5. Check for conflicting CSS classes
6. Test on different screen sizes

### Resource Widget Not Accessing Data

**Issue**: Widget can't access table/record data.

**Solutions**:
1. Ensure page uses `ExposesTableToWidgets` trait
2. Verify widget uses `InteractsWithPageTable` trait
3. Check `getTablePage()` returns correct class
4. Confirm widget is registered on the correct page
5. Test with `dd($this->record)` to verify injection

---

## Cross-References

### Related FilamentPHP Topics

- **[TABLES.md](TABLES.md)**: Table widget implementation and features
- **[FORMS.md](FORMS.md)**: Form components for widget filters
- **[PANEL_CONFIGURATION.md](PANEL_CONFIGURATION.md)**: Panel-level widget configuration
- **[NOTIFICATIONS.md](NOTIFICATIONS.md)**: Widget interaction with notifications

### Prerequisites

- Understanding of Livewire components
- Familiarity with FilamentPHP panels and pages
- Basic knowledge of Chart.js (for chart widgets)
- Laravel Eloquent query building

### See Also

- [FilamentPHP Widgets Official Docs](https://filamentphp.com/docs/4.x/widgets)
- [Chart.js Documentation](https://www.chartjs.org/docs)
- [Laravel Trend Package](https://github.com/Flowframe/laravel-trend)
- [Livewire Documentation](https://livewire.laravel.com)

---

**Version**: FilamentPHP 4.x  
**Last Updated**: January 18, 2026  
**Total Examples**: 80+  
**Status**: Complete
