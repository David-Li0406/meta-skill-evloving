---
title: Use chunk() or cursor() for Large Datasets
impact: CRITICAL
impactDescription: Prevents memory exhaustion when processing many records
tags: eloquent, memory, chunking, cursor
---

## Use chunk() or cursor() for Large Datasets

Loading all records at once exhausts memory. Use chunk() or cursor() to process large datasets efficiently.

**Incorrect (memory exhaustion):**

```php
<?php

// ❌ Loads ALL users into memory at once
$users = User::all();

foreach ($users as $user) {
    $this->processUser($user);
}

// With 1M users, this crashes with memory exhausted
```

**Correct (chunking):**

```php
<?php

// ✓ Processes 1000 users at a time
User::chunk(1000, function ($users) {
    foreach ($users as $user) {
        $this->processUser($user);
    }
});

// Or with chunkById for safer pagination during updates
User::chunkById(1000, function ($users) {
    foreach ($users as $user) {
        $user->update(['processed' => true]);
    }
});
```

**Using lazy() for streaming:**

```php
<?php

// ✓ Uses PHP generators - minimal memory
foreach (User::lazy() as $user) {
    $this->processUser($user);
}

// With chunk size
foreach (User::lazy(1000) as $user) {
    $this->processUser($user);
}

// Can chain query methods
User::where('active', true)
    ->orderBy('id')
    ->lazy()
    ->each(fn ($user) => $this->processUser($user));
```

**Using cursor() for single-row streaming:**

```php
<?php

// ✓ Streams one row at a time from database
foreach (User::cursor() as $user) {
    $this->processUser($user);
}

// Note: cursor() keeps DB connection open longer
// Use lazy() for better connection management
```

**When to use each:**

```php
<?php

// chunk() - when you need to work with batches
// Good for: batch updates, bulk operations, progress tracking
User::chunk(500, function ($users, $page) {
    $this->processBatch($users);
    $this->updateProgress($page * 500);
});

// lazy() - when you need one-at-a-time processing
// Good for: exports, reports, transformations
$csv = User::lazy()->map(fn ($u) => $u->toArray());

// cursor() - when memory is extremely limited
// Good for: massive datasets, limited PHP memory
// Note: holds DB connection open
```

Reference: [Chunking Results](https://laravel.com/docs/eloquent#chunking-results)
