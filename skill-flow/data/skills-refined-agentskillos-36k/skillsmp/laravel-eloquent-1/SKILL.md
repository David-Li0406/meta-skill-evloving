---
name: laravel-eloquent
description: Design efficient Eloquent relationships with proper eager loading, scopes, and query optimization. Use this when working with models, relationships, or database queries.
allowed-tools: Bash,Read,Write,Edit,Glob,Grep
---

# Eloquent Relationships & Loading

Build efficient, maintainable Eloquent models with proper relationships and query optimization.

## Relationship Definition

### Always Use Return Types

```php
use Illuminate\Database\Eloquent\Relations\{HasMany, BelongsTo, BelongsToMany};

class Post extends Model
{
    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class)
            ->withTimestamps()
            ->withPivot('order');
    }

    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }

    public function latestComment(): HasOne
    {
        return $this->hasOne(Comment::class)->latestOfMany();
    }
}
```

### Relationship Types

**One-to-One:**
```php
// User has one Profile
public function profile(): HasOne
{
    return $this->hasOne(Profile::class);
}

// Profile belongs to User
public function user(): BelongsTo
{
    return $this->belongsTo(User::class);
}
```

**One-to-Many:**
```php
// User has many Posts
public function posts(): HasMany
{
    return $this->hasMany(Post::class);
}

// Post belongs to User
public function author(): BelongsTo
{
    return $this->belongsTo(User::class, 'user_id');
}
```

**Many-to-Many:**
```php
// Post belongs to many Tags
public function tags(): BelongsToMany
{
    return $this->belongsToMany(Tag::class)
        ->withTimestamps()
        ->withPivot('order', 'featured');
}

// Tag belongs to many Posts
public function posts(): BelongsToMany
{
    return $this->belongsToMany(Post::class)
        ->withTimestamps();
}
```

**Polymorphic:**
```php
// Comment can belong to Post or Video
public function commentable(): MorphTo
{
    return $this->morphTo();
}

// Post has many Comments (polymorphic)
public function comments(): MorphMany
{
    return $this->morphMany(Comment::class, 'commentable');
}
```

## Eager Loading (Prevent N+1)

### Basic Eager Loading

```php
// ❌ BAD: N+1 queries (1 + N queries)
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->author->name; // Separate query for each post!
}

// ✅ GOOD: 2 queries total
$posts = Post::with('author')->get();
foreach ($posts as $post) {
    echo $post->author->name; // Uses eager-loaded data
}
```

### Multiple Relationships

```php
// Load multiple relationships
$posts = Post::with(['author', 'tags', 'comments'])->get();

// Nested relationships
$posts = Post::with(['author.profile', 'comments.user'])->get();
```

### Conditional Eager Loading

```php
// Only load published posts
$users = User::with([
    'posts' => fn($query) => $query->where('published', true)->latest()
])->get();

// Limit eager-loaded records (Laravel 11+)
$users = User::with([
    'posts' => fn($query) => $query->latest()->limit(5)
])->get();
```

### Aggregate Loading

```php
// Count relationships
$posts = Post::withCount('comments')->get();
// Accessed via: $post->comments_count

// Sum/Average/Max/Min
$users = User::withSum('orders', 'total')
    ->withAvg('reviews', 'rating')
    ->withMax('posts', 'created_at')
    ->get();

// Accessed via: $user->orders_sum_total, $user->reviews_avg_rating
```

### Lazy Eager Loading

```php
// Already loaded posts, now need authors
$posts = Post::all();

if ($needAuthors) {
    $posts->load('author');
}

// Conditional loading
$posts->load([
    'comments' => fn($q) => $q->where('approved', true)
]);
```

## Querying Relationships

### Has/WhereHas

```php
// Get posts that have at least one comment
$posts = Post::has('comments')->get();

// Get posts with more than 5 comments
$posts = Post::has('comments', '>', 5)->get();

// Get posts with approved comments
$posts = Post::whereHas('comments', function ($query) {
    $query->where('approved', true);
})->get();

// Get posts without comments
$posts = Post::doesntHave('comments')->get();
```

### Relationship Queries

```php
// Query relationship as a subquery
$users = User::select(['id', 'name'])
    ->addSelect([
        'latest_post_title' => Post::select('title')
            ->whereColumn('user_id', 'users.id')
            ->latest()
            ->limit(1)
    ])
    ->get();
```

## Relationship Manipulation

### Attach/Detach (Many-to-Many)

```php
// Attach tags to post
$post->tags()->attach([1, 2, 3]);

// Attach with pivot data
$post->tags()->attach(1, ['order' => 1, 'featured' => true]);

// Detach specific tags
$post->tags()->detach([1, 2]);

// Detach all tags
$post->tags()->detach();
```

### Sync (Many-to-Many)

```php
// Replace all tags (atomic operation)
$post->tags()->sync([1, 2, 3]);

// Sync with pivot data
$post->tags()->sync([
    1 => ['order' => 1],
    2 => ['order' => 2],
]);

// Sync without detaching (only add new)
$post->tags()->syncWithoutDetaching([4, 5]);
```

### Create/Update Through Relationships

```php
// Create related model
$post = Post::find(1);
$comment = $post->comments()->create([
    'body' => 'Great post!',
    'user_id' => auth()->id(),
]);

// Update related models
$post->comments()->update(['approved' => true]);

// Delete related models
$post->comments()->delete();
```

## Scopes

### Local Scopes

```php
class Post extends Model
{
    public function scopePublished(Builder $query): void
    {
        $query->where('published', true);
    }

    public function scopePopular(Builder $query): void
    {
        $query->where('views', '>', 1000);
    }

    public function scopeByAuthor(Builder $query, User $author): void
    {
        $query->where('user_id', $author->id);
    }
}

// Usage
$posts = Post::published()->popular()->get();
$posts = Post::byAuthor($user)->latest()->get();
```

### Global Scopes

```php
namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\{Builder, Model, Scope};

class PublishedScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('published', true);
    }
}

// Apply to model
class Post extends Model
{
    protected static function booted(): void
    {
        static::addGlobalScope(new PublishedScope);
    }
}

// Remove global scope when needed
$allPosts = Post::withoutGlobalScope(PublishedScope::class)->get();
```

## Performance Patterns

### Chunking Large Datasets

```php
// Process large datasets efficiently
Post::chunk(200, function ($posts) {
    foreach ($posts as $post) {
        // Process each post
    }
});

// Lazy loading (memory efficient)
Post::lazy()->each(function ($post) {
    // Process each post
});

// Lazy with chunk size
Post::lazy(200)->each(function ($post) {
    // Process each post
});
```

### Select Specific Columns

```php
// Only load needed columns
$posts = Post::select(['id', 'title', 'created_at'])
    ->with(['author' => fn($q) => $q->select(['id', 'name'])])
    ->get();
```

### Raw Expressions

```php
use Illuminate\Support\Facades\DB;

// Use raw expressions when needed
$users = User::select([
    'users.*',
    DB::raw('(SELECT COUNT(*) FROM posts WHERE posts.user_id = users.id) as post_count')
])->get();
```

## Testing Relationships

### Factory Relationships

```php
// Create post with author
$post = Post::factory()
    ->for(User::factory())
    ->create();

// Create post with tags
$post = Post::factory()
    ->hasAttached(Tag::factory()->count(3))
    ->create();

// Create user with posts
$user = User::factory()
    ->has(Post::factory()->count(5))
    ->create();

// Complex relationships
$user = User::factory()
    ->has(
        Post::factory()
            ->count(3)
            ->hasAttached(Tag::factory()->count(2))
    )
    ->create();
```

### Testing Queries

```php
test('eager loads author to prevent N+1', function () {
    User::factory()->has(Post::factory()->count(10))->create();

    DB::enableQueryLog();

    $posts = Post::with('author')->get();

    // Should be 2 queries: posts + authors
    expect(DB::getQueryLog())->toHaveCount(2);
});

test('scopes filter correctly', function () {
    Post::factory()->create(['published' => true]);
    Post::factory()->create(['published' => false]);

    $posts = Post::published()->get();

    expect($posts)->toHaveCount(1);
    expect($posts->first()->published)->toBeTrue();
});
```

## Common Patterns

### Polymorphic Comments

```php
// models/Concerns/HasComments.php
trait HasComments
{
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

// Use in models
class Post extends Model
{
    use HasComments;
}

class Video extends Model
{
    use HasComments;
}

// Query
$post->comments()->create(['body' => 'Great!']);
$video->comments()->create(['body' => 'Awesome!']);
```

### Through Relationships

```php
// Country -> Users -> Posts
class Country extends Model
{
    public function posts(): HasManyThrough
    {
        return $this->hasManyThrough(Post::class, User::class);
    }
}

// Usage
$country = Country::find(1);
$posts = $country->posts; // All posts by users in this country
```

## Output Checklist

After working with Eloquent relationships:

- ✅ **Return types defined** on all relationship methods
- ✅ **Eager loading** prevents N+1 queries
- ✅ **Relationships tested** in factories and feature tests
- ✅ **Scopes** for common query patterns
- ✅ **Proper pluralization** (singular for belongsTo, plural for hasMany)
- ✅ **Performance verified** using Laravel Debugbar or tinker

## Important Reminders

- **ALWAYS** define explicit return types on relationships
- **ALWAYS** use eager loading (`with()`) to prevent N+1 queries
- **ALWAYS** test relationship queries for performance
- **NEVER** query relationships in loops without eager loading
- **NEVER** add dark mode support (light mode only)
- **NEVER** customize Flux UI component colors, typography, or borders (only padding/margins)
- **USE** `withCount()` for counting instead of `->count()` in views
- **CHECK** Laravel Debugbar for query counts during development
- **PREFER** relationship methods over manual joins
