# Global Search - FilamentPHP 4.x Reference

## Table of Contents
1. [Overview](#overview)
2. [Basic Global Search Configuration](#basic-global-search-configuration)
3. [Searchable Attributes](#searchable-attributes)
4. [Search Result Customization](#search-result-customization)
5. [Eager Loading & Performance](#eager-loading--performance)
6. [Global Search Positioning](#global-search-positioning)
7. [Keyboard Shortcuts & Debouncing](#keyboard-shortcuts--debouncing)
8. [Table Search](#table-search)
9. [Advanced Search Patterns](#advanced-search-patterns)
10. [Search Optimization](#search-optimization)
11. [Scout Integration](#scout-integration)
12. [Troubleshooting](#troubleshooting)
13. [Cross-References](#cross-references)

---

## Overview

**Purpose**: Global search allows users to quickly find records across all resources in a FilamentPHP panel. It provides a unified search interface accessible from the sidebar or topbar.

**Key Concepts**:
- **recordTitleAttribute**: Defines which model attribute to display as the search result title
- **Searchable Attributes**: Model fields indexed for search queries
- **Result Customization**: Control how search results appear (title, URL, details, actions)
- **Performance**: Eager loading, debouncing, and query optimization
- **Positioning**: Sidebar, topbar, or disabled

**Common Use Cases**:
- Quick navigation to specific records across resources
- Finding users, orders, products without navigating to list pages
- Searching related data (e.g., posts by author name)
- Custom search logic for complex queries

---

## Basic Global Search Configuration

### Enable Global Search on Resource

```php
// app/Filament/Resources/PostResource.php
namespace App\Filament\Resources;

use Filament\Resources\Resource;

class PostResource extends Resource
{
    protected static ?string $model = Post::class;
    
    // Set which attribute to use as the title in search results
    protected static ?string $recordTitleAttribute = 'title';
    
    // Optional: Set the navigation label
    protected static ?string $navigationLabel = 'Posts';
    
    // Optional: Set the navigation icon
    protected static ?string $navigationIcon = 'heroicon-o-document-text';
}
```

**Key Points**:
- `$recordTitleAttribute` enables global search for the resource
- The attribute value is displayed as the main text in search results
- If not set, global search won't index this resource

### Multiple Word Attributes

```php
// app/Filament/Resources/CustomerResource.php
class CustomerResource extends Resource
{
    protected static ?string $model = Customer::class;
    
    // Use a computed attribute for full name
    protected static ?string $recordTitleAttribute = 'full_name';
}

// app/Models/Customer.php
class Customer extends Model
{
    protected $appends = ['full_name'];
    
    public function getFullNameAttribute(): string
    {
        return "{$this->first_name} {$this->last_name}";
    }
}
```

### Disable Global Search

```php
// To completely disable global search for a resource
class InternalLogResource extends Resource
{
    protected static ?string $model = InternalLog::class;
    
    // Don't set $recordTitleAttribute - global search will be disabled
    
    // Or explicitly set to null
    protected static ?string $recordTitleAttribute = null;
}
```

---

## Searchable Attributes

### Define Searchable Attributes

```php
// app/Filament/Resources/PostResource.php
class PostResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'title';
    
    public static function getGloballySearchableAttributes(): array
    {
        return [
            'title',
            'slug',
            'content',
        ];
    }
}
```

**Key Points**:
- Returns array of model attributes to search
- All attributes searched using SQL `LIKE` queries
- Case-insensitive by default

### Search Relationship Attributes

```php
// Search across relationships using dot notation
class PostResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'title';
    
    public static function getGloballySearchableAttributes(): array
    {
        return [
            'title',
            'slug',
            'author.name',           // Search by author name
            'category.name',         // Search by category name
            'tags.name',             // Search by tag names
            'company.department.name', // Nested relationships
        ];
    }
}
```

**Relationship Requirements**:
- Relationships must be defined on the model
- Use dot notation for nested relationships
- Eager load relationships to avoid N+1 queries (see below)

### Computed Attributes

```php
class CustomerResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'full_name';
    
    public static function getGloballySearchableAttributes(): array
    {
        return [
            'first_name',
            'last_name',
            'email',
            'phone',
            'company.name',
        ];
    }
}

// Model accessor
class Customer extends Model
{
    public function getFullNameAttribute(): string
    {
        return trim("{$this->first_name} {$this->last_name}");
    }
}
```

### Search Multiple Fields Together

```php
// Search across multiple text fields
class ProductResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'name';
    
    public static function getGloballySearchableAttributes(): array
    {
        return [
            'name',
            'sku',
            'description',
            'brand.name',
            'category.name',
            'supplier.company_name',
        ];
    }
}
```

---

## Search Result Customization

### Customize Result Title

```php
// app/Filament/Resources/PostResource.php
class PostResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'title';
    
    public static function getGlobalSearchResultTitle(Model $record): string
    {
        // Simple title
        return $record->title;
        
        // Or add extra context
        return "{$record->title} ({$record->status})";
        
        // Or format with HTML (use HtmlString)
        return new HtmlString(
            "<strong>{$record->title}</strong> <span class='text-gray-500'>#{$record->id}</span>"
        );
    }
}
```

### Customize Result URL

```php
class PostResource extends Resource
{
    public static function getGlobalSearchResultUrl(Model $record): string
    {
        // Default: goes to resource view page
        return static::getUrl('view', ['record' => $record]);
        
        // Or go directly to edit page
        return static::getUrl('edit', ['record' => $record]);
        
        // Or custom URL
        return route('posts.preview', ['post' => $record->slug]);
    }
}
```

### Add Result Details

```php
class PostResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'title';
    
    public static function getGlobalSearchResultDetails(Model $record): array
    {
        return [
            'Author' => $record->author->name,
            'Category' => $record->category->name,
            'Published' => $record->published_at?->format('M d, Y'),
        ];
    }
}
```

**Result**:
```
My Blog Post Title
Author: John Doe
Category: Technology
Published: Jan 15, 2024
```

### Advanced Result Details

```php
class OrderResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'number';
    
    public static function getGlobalSearchResultDetails(Model $record): array
    {
        $details = [
            'Customer' => $record->customer->full_name,
            'Total' => 'EGP ' . number_format($record->total, 2),
            'Status' => ucfirst($record->status),
        ];
        
        if ($record->shipped_at) {
            $details['Shipped'] = $record->shipped_at->format('M d, Y');
        }
        
        return $details;
    }
}
```

### Add Result Actions

```php
use Filament\GlobalSearch\Actions\Action;

class PostResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'title';
    
    public static function getGlobalSearchResultActions(Model $record): array
    {
        return [
            Action::make('view')
                ->label('View')
                ->icon('heroicon-o-eye')
                ->url(static::getUrl('view', ['record' => $record])),
                
            Action::make('edit')
                ->label('Edit')
                ->icon('heroicon-o-pencil')
                ->url(static::getUrl('edit', ['record' => $record])),
                
            Action::make('preview')
                ->label('Preview')
                ->icon('heroicon-o-globe-alt')
                ->url(route('posts.show', $record))
                ->openUrlInNewTab(),
        ];
    }
}
```

---

## Eager Loading & Performance

### Basic Eager Loading

```php
// app/Filament/Resources/PostResource.php
class PostResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'title';
    
    public static function getGloballySearchableAttributes(): array
    {
        return [
            'title',
            'author.name',
            'category.name',
        ];
    }
    
    // Eager load relationships to prevent N+1 queries
    public static function getGlobalSearchEloquentQuery(): Builder
    {
        return parent::getGlobalSearchEloquentQuery()
            ->with(['author', 'category']);
    }
}
```

**Why This Matters**:
- Without eager loading: 1 query + N queries for each result's relationships
- With eager loading: 2-3 queries total (much faster)

### Advanced Eager Loading

```php
class OrderResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'number';
    
    public static function getGloballySearchableAttributes(): array
    {
        return [
            'number',
            'customer.name',
            'customer.email',
            'items.product.name',
        ];
    }
    
    public static function getGlobalSearchEloquentQuery(): Builder
    {
        return parent::getGlobalSearchEloquentQuery()
            ->with([
                'customer',
                'items.product',
                'shippingAddress',
            ])
            ->withCount('items');
    }
}
```

### Selective Column Loading

```php
class ProductResource extends Resource
{
    public static function getGlobalSearchEloquentQuery(): Builder
    {
        return parent::getGlobalSearchEloquentQuery()
            ->select([
                'id',
                'name',
                'sku',
                'price',
                'category_id',
                'brand_id',
            ])
            ->with([
                'category:id,name',
                'brand:id,name',
            ]);
    }
}
```

### Add Scopes

```php
class PostResource extends Resource
{
    public static function getGlobalSearchEloquentQuery(): Builder
    {
        return parent::getGlobalSearchEloquentQuery()
            ->with(['author', 'category'])
            ->published()  // Only search published posts
            ->latest();
    }
}

// Model scope
class Post extends Model
{
    public function scopePublished(Builder $query): Builder
    {
        return $query->where('status', 'published')
            ->whereNotNull('published_at')
            ->where('published_at', '<=', now());
    }
}
```

---

## Global Search Positioning

### Configure Panel Search Position

```php
// app/Providers/Filament/AdminPanelProvider.php
use Filament\Panel;
use Filament\Support\Enums\GlobalSearchPosition;

public function panel(Panel $panel): Panel
{
    return $panel
        ->id('admin')
        ->path('admin')
        
        // Position in sidebar (default)
        ->globalSearch(position: GlobalSearchPosition::Sidebar)
        
        // Or position in topbar
        // ->globalSearch(position: GlobalSearchPosition::Topbar)
        
        // Or disable global search entirely
        // ->globalSearch(false)
        
        ->pages([
            Dashboard::class,
        ])
        ->resources([
            PostResource::class,
        ]);
}
```

### Topbar Position

```php
// Use topbar for more prominent search
public function panel(Panel $panel): Panel
{
    return $panel
        ->id('admin')
        ->path('admin')
        ->globalSearch(position: GlobalSearchPosition::Topbar)
        ->globalSearchKeyBindings(['command+k', 'ctrl+k'])  // Add keyboard shortcuts
        ->pages([
            Dashboard::class,
        ]);
}
```

### Conditional Search Position

```php
public function panel(Panel $panel): Panel
{
    $searchPosition = auth()->user()?->prefers_topbar_search 
        ? GlobalSearchPosition::Topbar 
        : GlobalSearchPosition::Sidebar;
        
    return $panel
        ->id('admin')
        ->globalSearch(position: $searchPosition);
}
```

---

## Keyboard Shortcuts & Debouncing

### Configure Keyboard Shortcuts

```php
// app/Providers/Filament/AdminPanelProvider.php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->id('admin')
        ->path('admin')
        
        // Set keyboard shortcuts to open global search
        ->globalSearchKeyBindings(['command+k', 'ctrl+k'])
        
        // Or use different shortcuts
        // ->globalSearchKeyBindings(['command+/', 'ctrl+/'])
        // ->globalSearchKeyBindings(['command+p', 'ctrl+p'])
        
        ->resources([
            PostResource::class,
        ]);
}
```

**User Experience**:
- User presses `Cmd+K` (Mac) or `Ctrl+K` (Windows/Linux)
- Global search modal opens immediately
- User can start typing without clicking

### Configure Debouncing

```php
public function panel(Panel $panel): Panel
{
    return $panel
        ->id('admin')
        ->path('admin')
        
        // Wait 750ms after user stops typing before searching
        ->globalSearchDebounce('750ms')
        
        // Or use different delays
        // ->globalSearchDebounce('500ms')  // Faster, more requests
        // ->globalSearchDebounce('1000ms') // Slower, fewer requests
        
        ->globalSearchKeyBindings(['command+k', 'ctrl+k']);
}
```

**Why Debouncing Matters**:
- Without debouncing: Search runs on every keystroke (inefficient)
- With 750ms debounce: Search only runs after user pauses typing
- Reduces server load and improves UX

### Complete Configuration

```php
use Filament\Support\Enums\GlobalSearchPosition;

public function panel(Panel $panel): Panel
{
    return $panel
        ->id('admin')
        ->path('admin')
        ->globalSearch(position: GlobalSearchPosition::Topbar)
        ->globalSearchKeyBindings(['command+k', 'ctrl+k'])
        ->globalSearchDebounce('750ms')
        ->resources([
            PostResource::class,
            ProductResource::class,
            OrderResource::class,
        ]);
}
```

---

## Table Search

### Enable Table Column Search

```php
// app/Filament/Resources/PostResource.php
use Filament\Tables;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            Tables\Columns\TextColumn::make('title')
                ->searchable(),  // Enable search for this column
                
            Tables\Columns\TextColumn::make('author.name')
                ->searchable(),  // Search by relationship
                
            Tables\Columns\TextColumn::make('status')
                ->badge(),
                
            Tables\Columns\TextColumn::make('published_at')
                ->date(),
        ])
        ->filters([
            // ...
        ]);
}
```

### Search Multiple Columns

```php
public static function table(Table $table): Table
{
    return $table
        ->columns([
            Tables\Columns\TextColumn::make('name')
                ->searchable(),
                
            Tables\Columns\TextColumn::make('email')
                ->searchable(),
                
            Tables\Columns\TextColumn::make('phone')
                ->searchable(),
        ])
        
        // Search box will search all searchable columns
        ->defaultSort('name');
}
```

### Search with Query Modification

```php
use Illuminate\Database\Eloquent\Builder;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            Tables\Columns\TextColumn::make('title')
                ->searchable(query: function (Builder $query, string $search): Builder {
                    return $query->where(function (Builder $query) use ($search) {
                        $query->where('title', 'like', "%{$search}%")
                            ->orWhere('slug', 'like', "%{$search}%");
                    });
                }),
                
            Tables\Columns\TextColumn::make('author.name')
                ->searchable(),
        ]);
}
```

### Individual Column Search

```php
public static function table(Table $table): Table
{
    return $table
        ->columns([
            Tables\Columns\TextColumn::make('title')
                ->searchable(isIndividual: true),  // Separate search field
                
            Tables\Columns\TextColumn::make('author.name')
                ->searchable(isIndividual: true),
                
            Tables\Columns\TextColumn::make('status')
                ->searchable(isIndividual: true),
        ])
        
        // Each column gets its own search box in the table header
        ->persistSearchInSession();
}
```

### Search Across Relationships

```php
public static function table(Table $table): Table
{
    return $table
        ->columns([
            Tables\Columns\TextColumn::make('number')
                ->searchable(),
                
            Tables\Columns\TextColumn::make('customer.name')
                ->searchable(query: function (Builder $query, string $search): Builder {
                    return $query->whereHas('customer', function (Builder $query) use ($search) {
                        $query->where('name', 'like', "%{$search}%")
                            ->orWhere('email', 'like', "%{$search}%");
                    });
                }),
                
            Tables\Columns\TextColumn::make('total')
                ->money('EGP'),
        ]);
}
```

### Persist Search in Session

```php
public static function table(Table $table): Table
{
    return $table
        ->columns([
            Tables\Columns\TextColumn::make('name')
                ->searchable(),
            Tables\Columns\TextColumn::make('email')
                ->searchable(),
        ])
        
        // Remember search query when navigating away and back
        ->persistSearchInSession()
        
        // Also persist filters
        ->persistFiltersInSession();
}
```

---

## Advanced Search Patterns

### Custom Search Query Logic

```php
class ProductResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'name';
    
    public static function getGloballySearchableAttributes(): array
    {
        return ['name', 'sku', 'description'];
    }
    
    public static function getGlobalSearchEloquentQuery(): Builder
    {
        return parent::getGlobalSearchEloquentQuery()
            ->with(['category', 'brand'])
            
            // Only search active products
            ->where('status', 'active')
            
            // Only products in stock
            ->where('stock_quantity', '>', 0)
            
            // Order by relevance (exact matches first)
            ->orderByRaw("CASE WHEN name = ? THEN 0 ELSE 1 END", [request('search')]);
    }
}
```

### Multi-Tenant Search Scoping

```php
class PostResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'title';
    
    public static function getGlobalSearchEloquentQuery(): Builder
    {
        $query = parent::getGlobalSearchEloquentQuery()
            ->with(['author', 'category']);
            
        // Scope to current tenant
        if (Filament::getTenant()) {
            $query->whereBelongsTo(Filament::getTenant());
        }
        
        return $query;
    }
}
```

### Search Across Multiple Models

```php
// Create a custom global search provider
use Filament\GlobalSearch\GlobalSearchResults;
use Filament\GlobalSearch\Contracts\GlobalSearchProvider;

class CustomGlobalSearchProvider implements GlobalSearchProvider
{
    public function getResults(string $query): ?GlobalSearchResults
    {
        $results = new GlobalSearchResults();
        
        // Search posts
        $posts = Post::where('title', 'like', "%{$query}%")
            ->orWhere('content', 'like', "%{$query}%")
            ->limit(5)
            ->get();
            
        foreach ($posts as $post) {
            $results->category('Posts')->add(
                title: $post->title,
                url: PostResource::getUrl('view', ['record' => $post]),
                details: ['Author' => $post->author->name],
            );
        }
        
        // Search products
        $products = Product::where('name', 'like', "%{$query}%")
            ->orWhere('sku', 'like', "%{$query}%")
            ->limit(5)
            ->get();
            
        foreach ($products as $product) {
            $results->category('Products')->add(
                title: $product->name,
                url: ProductResource::getUrl('view', ['record' => $product]),
                details: ['SKU' => $product->sku, 'Price' => 'EGP ' . $product->price],
            );
        }
        
        return $results;
    }
}
```

### Search External API

```php
class CustomerResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'name';
    
    public static function getGlobalSearchResults(string $search): ?Collection
    {
        // Search local database
        $localResults = static::getModel()::query()
            ->where('name', 'like', "%{$search}%")
            ->orWhere('email', 'like', "%{$search}%")
            ->limit(10)
            ->get();
            
        // Also search external CRM API
        $externalResults = Http::get('https://crm.example.com/api/customers/search', [
            'query' => $search,
        ])->json();
        
        // Merge results
        return $localResults->concat(
            collect($externalResults)->map(fn ($customer) => new Customer([
                'id' => $customer['id'],
                'name' => $customer['name'],
                'email' => $customer['email'],
                'source' => 'external',
            ]))
        );
    }
}
```

---

## Search Optimization

### Limit Search Results

```php
class PostResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'title';
    
    // Limit to 10 results maximum
    protected static int $globalSearchResultsLimit = 10;
    
    public static function getGlobalSearchEloquentQuery(): Builder
    {
        return parent::getGlobalSearchEloquentQuery()
            ->with(['author', 'category'])
            ->limit(static::$globalSearchResultsLimit);
    }
}
```

### Database Indexing

```php
// Create database migration for search performance
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('posts', function (Blueprint $table) {
            // Add indexes for searchable columns
            $table->index('title');
            $table->index('slug');
            
            // Composite index for multi-column searches
            $table->index(['status', 'published_at']);
            
            // Full-text index for content search (MySQL 5.6+)
            $table->fullText(['title', 'content']);
        });
        
        Schema::table('customers', function (Blueprint $table) {
            $table->index('name');
            $table->index('email');
            $table->index(['first_name', 'last_name']);
        });
    }
    
    public function down(): void
    {
        Schema::table('posts', function (Blueprint $table) {
            $table->dropIndex(['title']);
            $table->dropIndex(['slug']);
            $table->dropIndex(['status', 'published_at']);
            $table->dropFullText(['title', 'content']);
        });
        
        Schema::table('customers', function (Blueprint $table) {
            $table->dropIndex(['name']);
            $table->dropIndex(['email']);
            $table->dropIndex(['first_name', 'last_name']);
        });
    }
};
```

### Full-Text Search

```php
class PostResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'title';
    
    public static function getGloballySearchableAttributes(): array
    {
        return ['title', 'content'];
    }
    
    public static function getGlobalSearchEloquentQuery(): Builder
    {
        $search = request('search');
        
        return parent::getGlobalSearchEloquentQuery()
            ->with(['author', 'category'])
            
            // Use full-text search when available (MySQL 5.6+)
            ->when(
                $search && config('database.default') === 'mysql',
                fn (Builder $query) => $query->whereFullText(['title', 'content'], $search),
                fn (Builder $query) => $query->where(function (Builder $q) use ($search) {
                    $q->where('title', 'like', "%{$search}%")
                        ->orWhere('content', 'like', "%{$search}%");
                })
            );
    }
}
```

### Cache Search Results

```php
use Illuminate\Support\Facades\Cache;

class ProductResource extends Resource
{
    public static function getGlobalSearchResults(string $search): ?Collection
    {
        $cacheKey = "global_search_products_{$search}";
        
        return Cache::remember($cacheKey, now()->addMinutes(5), function () use ($search) {
            return static::getModel()::query()
                ->where('name', 'like', "%{$search}%")
                ->orWhere('sku', 'like', "%{$search}%")
                ->with(['category', 'brand'])
                ->limit(20)
                ->get();
        });
    }
}
```

---

## Scout Integration

### Install Laravel Scout

```bash
cd e:\AI_rewirte\larament; composer require laravel/scout
cd e:\AI_rewirte\larament; php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

### Configure Model for Scout

```php
// app/Models/Post.php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;
    
    // Define searchable data
    public function toSearchableArray(): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'content' => $this->content,
            'author' => $this->author->name,
            'category' => $this->category->name,
        ];
    }
    
    // Optional: Conditional indexing
    public function shouldBeSearchable(): bool
    {
        return $this->status === 'published';
    }
}
```

### Use Scout in Resource

```php
class PostResource extends Resource
{
    protected static ?string $recordTitleAttribute = 'title';
    
    public static function getGlobalSearchEloquentQuery(): Builder
    {
        $search = request('search');
        
        // Use Scout for search
        if ($search) {
            $ids = Post::search($search)
                ->take(50)
                ->keys();
                
            return Post::query()
                ->whereIn('id', $ids)
                ->with(['author', 'category']);
        }
        
        return parent::getGlobalSearchEloquentQuery()
            ->with(['author', 'category']);
    }
}
```

### Advanced Scout Configuration

```php
// config/scout.php
return [
    'driver' => env('SCOUT_DRIVER', 'meilisearch'),
    
    'meilisearch' => [
        'host' => env('MEILISEARCH_HOST', 'http://localhost:7700'),
        'key' => env('MEILISEARCH_KEY', null),
        'index-settings' => [
            Post::class => [
                'filterableAttributes' => ['status', 'author_id'],
                'sortableAttributes' => ['published_at'],
            ],
        ],
    ],
];

// Resource with Scout filters
class PostResource extends Resource
{
    public static function getGlobalSearchEloquentQuery(): Builder
    {
        $search = request('search');
        
        if ($search) {
            $ids = Post::search($search)
                ->where('status', 'published')  // Scout filter
                ->orderBy('published_at', 'desc')  // Scout sort
                ->take(50)
                ->keys();
                
            return Post::query()
                ->whereIn('id', $ids)
                ->with(['author', 'category'])
                ->orderByRaw('FIELD(id, ' . $ids->implode(',') . ')');  // Maintain Scout order
        }
        
        return parent::getGlobalSearchEloquentQuery()
            ->with(['author', 'category']);
    }
}
```

---

## Troubleshooting

### Global Search Not Appearing

**Problem**: Global search doesn't show in panel

**Solutions**:
1. Check `$recordTitleAttribute` is set:
   ```php
   protected static ?string $recordTitleAttribute = 'title';
   ```

2. Verify resource is registered:
   ```php
   // AdminPanelProvider
   ->resources([
       PostResource::class,  // Must be registered
   ])
   ```

3. Check global search isn't disabled:
   ```php
   // Should NOT have this:
   // ->globalSearch(false)
   ```

### No Search Results

**Problem**: Search returns no results even with matching data

**Solutions**:
1. Check searchable attributes are correct:
   ```php
   public static function getGloballySearchableAttributes(): array
   {
       return [
           'title',  // Must match actual column name
           'slug',
       ];
   }
   ```

2. Verify query scopes aren't too restrictive:
   ```php
   public static function getGlobalSearchEloquentQuery(): Builder
   {
       return parent::getGlobalSearchEloquentQuery()
           ->with(['author'])
           // ->published()  // Remove if too restrictive
           ;
   }
   ```

3. Check for tenant scoping issues:
   ```php
   // Make sure tenant is set correctly
   dd(Filament::getTenant());
   ```

### Slow Search Performance

**Problem**: Search takes several seconds

**Solutions**:
1. Add database indexes:
   ```php
   Schema::table('posts', function (Blueprint $table) {
       $table->index('title');
       $table->index('status');
   });
   ```

2. Eager load relationships:
   ```php
   public static function getGlobalSearchEloquentQuery(): Builder
   {
       return parent::getGlobalSearchEloquentQuery()
           ->with(['author', 'category'])  // Prevent N+1
           ->select(['id', 'title', 'author_id', 'category_id']);  // Limit columns
   }
   ```

3. Limit results:
   ```php
   protected static int $globalSearchResultsLimit = 10;
   ```

4. Use Scout for large datasets:
   ```php
   // See Scout Integration section
   ```

### Relationship Search Not Working

**Problem**: Searching by relationship attributes returns no results

**Solutions**:
1. Verify relationship exists:
   ```php
   // In Post model
   public function author()
   {
       return $this->belongsTo(User::class, 'author_id');
   }
   ```

2. Eager load the relationship:
   ```php
   public static function getGlobalSearchEloquentQuery(): Builder
   {
       return parent::getGlobalSearchEloquentQuery()
           ->with(['author']);  // Must eager load
   }
   ```

3. Use correct dot notation:
   ```php
   public static function getGloballySearchableAttributes(): array
   {
       return [
           'title',
           'author.name',  // Correct
           // 'author_name',  // Wrong
       ];
   }
   ```

### Search Results Missing Details

**Problem**: Result details not showing

**Solutions**:
1. Check method signature:
   ```php
   public static function getGlobalSearchResultDetails(Model $record): array
   {
       return [
           'Author' => $record->author->name,
       ];
   }
   ```

2. Ensure relationships are loaded:
   ```php
   public static function getGlobalSearchEloquentQuery(): Builder
   {
       return parent::getGlobalSearchEloquentQuery()
           ->with(['author']);  // Required for details
   }
   ```

3. Check for null values:
   ```php
   public static function getGlobalSearchResultDetails(Model $record): array
   {
       return array_filter([
           'Author' => $record->author?->name,  // Use null-safe operator
           'Published' => $record->published_at?->format('M d, Y'),
       ]);
   }
   ```

---

## Cross-References

### Related Documentation
- [RESOURCES.md](RESOURCES.md) - Resource configuration and `$recordTitleAttribute`
- [TABLES.md](TABLES.md) - Table column search and filters
- [PANEL_CONFIGURATION.md](PANEL_CONFIGURATION.md) - Global search positioning and keyboard shortcuts
- [CODE_QUALITY.md](CODE_QUALITY.md) - Performance optimization and N+1 query prevention

### External Resources
- [FilamentPHP Global Search Docs](https://filamentphp.com/docs/4.x/panels/global-search)
- [Laravel Scout Documentation](https://laravel.com/docs/11.x/scout)
- [Meilisearch Documentation](https://www.meilisearch.com/docs)
- [MySQL Full-Text Search](https://dev.mysql.com/doc/refman/8.0/en/fulltext-search.html)

### Common Patterns
- **Quick Navigation**: Enable global search for all major resources
- **Relationship Search**: Search across related data (author.name, category.name)
- **Performance**: Always eager load relationships + add database indexes
- **Multi-Tenant**: Scope search queries to current tenant
- **Arabic Search**: Use full-text indexes for better Arabic text support

---

**Last Updated**: January 2024  
**FilamentPHP Version**: 4.x  
**Larament Project**: Laravel + FilamentPHP + React/Inertia
