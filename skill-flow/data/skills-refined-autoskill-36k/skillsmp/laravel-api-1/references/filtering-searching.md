# Filtering & Searching

Advanced query patterns for filtering, searching, and sorting API results.

## Basic Filtering & Search

```php
public function index(Request $request): JsonResponse
{
    $query = Post::query()->with('author');

    // Filter by published status
    if ($request->has('published')) {
        $query->where('published', $request->boolean('published'));
    }

    // Search
    if ($request->filled('search')) {
        $query->where('title', 'like', "%{$request->search}%");
    }

    // Sort
    $sortField = $request->input('sort', 'created_at');
    $sortDirection = $request->input('direction', 'desc');
    $query->orderBy($sortField, $sortDirection);

    $posts = $query->paginate($request->input('per_page', 20));

    return PostResource::collection($posts)->response();
}
```

## Multi-Field Search

```php
if ($request->filled('search')) {
    $search = $request->search;
    $query->where(function ($q) use ($search) {
        $q->where('title', 'like', "%{$search}%")
          ->orWhere('content', 'like', "%{$search}%")
          ->orWhere('slug', 'like', "%{$search}%");
    });
}
```

## Date Range Filtering

```php
if ($request->filled(['start_date', 'end_date'])) {
    $query->whereBetween('created_at', [
        $request->start_date,
        $request->end_date,
    ]);
}
```

## Relationship Filtering

```php
// Filter posts by author name
if ($request->filled('author')) {
    $query->whereHas('author', function ($q) use ($request) {
        $q->where('name', 'like', "%{$request->author}%");
    });
}

// Filter posts by category slug
if ($request->filled('category')) {
    $query->whereHas('category', function ($q) use ($request) {
        $q->where('slug', $request->category);
    });
}
```

## Advanced Sorting

```php
// Allow sorting by relationship field
$allowedSorts = ['created_at', 'title', 'author_name'];
$sortField = $request->input('sort', 'created_at');

if (!in_array($sortField, $allowedSorts)) {
    $sortField = 'created_at';
}

if ($sortField === 'author_name') {
    $query->join('users', 'posts.user_id', '=', 'users.id')
          ->orderBy('users.name', $request->input('direction', 'asc'))
          ->select('posts.*');
} else {
    $query->orderBy($sortField, $request->input('direction', 'desc'));
}
```
