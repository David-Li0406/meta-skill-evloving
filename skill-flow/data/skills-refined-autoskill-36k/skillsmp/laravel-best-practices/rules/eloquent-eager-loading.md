---
title: Use with() to Prevent N+1 Queries
impact: CRITICAL
impactDescription: 10-100x query reduction for related data
tags: eloquent, n+1, eager-loading, performance
---

## Use with() to Prevent N+1 Queries

Lazy loading relationships inside loops causes N+1 queries. Eager load relationships upfront with with().

**Incorrect (N+1 queries):**

```php
<?php

// Controller
public function index()
{
    $posts = Post::all(); // 1 query

    return view('posts.index', compact('posts'));
}

// View - posts/index.blade.php
@foreach($posts as $post)
    <h2>{{ $post->title }}</h2>
    <p>By: {{ $post->author->name }}</p>  {{-- +1 query each --}}
    <span>{{ $post->category->name }}</span> {{-- +1 query each --}}
@endforeach

// 100 posts = 1 + 100 + 100 = 201 queries! 😱
```

**Correct (eager loading):**

```php
<?php

// Controller
public function index()
{
    $posts = Post::with(['author', 'category'])->get(); // 3 queries total

    return view('posts.index', compact('posts'));
}

// View - same code, but only 3 queries regardless of post count ✓
@foreach($posts as $post)
    <h2>{{ $post->title }}</h2>
    <p>By: {{ $post->author->name }}</p>
    <span>{{ $post->category->name }}</span>
@endforeach
```

**Nested eager loading:**

```php
<?php

// Load nested relationships
$posts = Post::with([
    'author.profile',           // Author and their profile
    'comments.user',            // Comments and their users
    'tags',                     // Tags
])->get();

// Constrained eager loading
$posts = Post::with([
    'comments' => function ($query) {
        $query->where('approved', true)
              ->orderBy('created_at', 'desc')
              ->limit(5);
    }
])->get();
```

**Prevent lazy loading in development:**

```php
<?php

// app/Providers/AppServiceProvider.php
public function boot()
{
    Model::preventLazyLoading(! app()->isProduction());
}

// Now lazy loading throws an exception in dev/staging
// Helps catch N+1 issues before production
```

**Load missing relationships:**

```php
<?php

// When you already have models but need more relations
$posts->load('author');         // Load single relation
$posts->loadMissing('author');  // Only if not already loaded
```

Reference: [Eager Loading](https://laravel.com/docs/eloquent-relationships#eager-loading)
