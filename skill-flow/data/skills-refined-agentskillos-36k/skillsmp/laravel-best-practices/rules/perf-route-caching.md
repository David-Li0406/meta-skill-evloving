---
title: Run route:cache in Production
impact: HIGH
impactDescription: 2-5x faster route registration
tags: performance, caching, routes, production
---

## Run route:cache in Production

Route registration happens on every request. Caching compiles routes once for instant loading.

**Incorrect (routes parsed every request):**

```bash
# Production deployment without route caching
php artisan migrate --force
php artisan config:cache
# ❌ Missing route:cache - routes parsed on every request
```

**Correct (routes cached):**

```bash
# Production deployment with full caching
php artisan config:cache    # Cache configuration
php artisan route:cache     # Cache routes
php artisan view:cache      # Cache Blade templates
php artisan event:cache     # Cache event listeners
```

**Complete deployment script:**

```bash
#!/bin/bash
# deploy.sh

# Put app in maintenance mode
php artisan down

# Pull latest code
git pull origin main

# Install dependencies
composer install --no-dev --optimize-autoloader

# Run migrations
php artisan migrate --force

# Clear all caches first (important!)
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear

# Rebuild caches
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Restart queue workers
php artisan queue:restart

# Bring app back online
php artisan up
```

**When route caching won't work:**

```php
<?php

// ❌ Closures in routes - cannot be cached
Route::get('/test', function () {
    return 'Hello';
});

// ✓ Use controllers instead
Route::get('/test', [TestController::class, 'index']);
```

**Clear cache when routes change:**

```bash
# After modifying routes
php artisan route:clear
php artisan route:cache
```

**Check if routes are cached:**

```bash
# List cached file
ls -la bootstrap/cache/routes-v7.php

# Clear to disable caching (development)
php artisan route:clear
```

Reference: [Route Caching](https://laravel.com/docs/routing#route-caching)
