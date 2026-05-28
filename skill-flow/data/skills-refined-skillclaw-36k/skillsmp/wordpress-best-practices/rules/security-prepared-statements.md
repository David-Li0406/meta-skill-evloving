---
title: Use $wpdb->prepare() for All Queries
impact: CRITICAL
impactDescription: Prevents SQL injection attacks
tags: security, sql-injection, wpdb, database
---

## Use $wpdb->prepare() for All Queries

Direct variable interpolation in SQL enables injection attacks. Always use $wpdb->prepare() for queries with user data.

**Incorrect (SQL injection vulnerable):**

```php
<?php
global $wpdb;

// ❌ Direct interpolation - SQL injection vulnerability
$results = $wpdb->get_results(
    "SELECT * FROM {$wpdb->posts} WHERE post_author = $user_id"
);

// ❌ String concatenation
$results = $wpdb->get_results(
    "SELECT * FROM {$wpdb->postmeta} WHERE meta_key = '" . $key . "'"
);

// ❌ User input in LIKE
$results = $wpdb->get_results(
    "SELECT * FROM {$wpdb->posts} WHERE post_title LIKE '%{$search}%'"
);
```

**Correct (prepared statements):**

```php
<?php
global $wpdb;

// ✓ Integer placeholder
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_author = %d",
        $user_id
    )
);

// ✓ String placeholder
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->postmeta} WHERE meta_key = %s",
        $key
    )
);

// ✓ LIKE with proper escaping
$search_escaped = $wpdb->esc_like($search);
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_title LIKE %s",
        '%' . $search_escaped . '%'
    )
);

// ✓ Multiple placeholders
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts}
         WHERE post_type = %s
         AND post_status = %s
         AND post_author = %d",
        $post_type,
        $post_status,
        $user_id
    )
);
```

**Placeholder reference:**

```php
<?php
// %s - String (quoted and escaped)
// %d - Integer (signed)
// %f - Float
// %i - Identifier (table/column name, backtick-quoted)

// Insert example
$wpdb->insert(
    $wpdb->posts,
    [
        'post_title' => $title,
        'post_content' => $content,
        'post_author' => $user_id,
    ],
    ['%s', '%s', '%d'] // Format array
);

// Update example
$wpdb->update(
    $wpdb->posts,
    ['post_title' => $new_title],  // Data
    ['ID' => $post_id],             // Where
    ['%s'],                         // Data format
    ['%d']                          // Where format
);
```

Reference: [Class Reference wpdb](https://developer.wordpress.org/reference/classes/wpdb/)
