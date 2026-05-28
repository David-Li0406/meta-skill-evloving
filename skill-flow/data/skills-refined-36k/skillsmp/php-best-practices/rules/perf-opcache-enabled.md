---
title: Enable and Configure OPcache
impact: HIGH
impactDescription: 2-3x performance improvement by caching compiled bytecode
tags: performance, opcache, caching, bytecode
---

## Enable and Configure OPcache

PHP recompiles scripts on every request by default. OPcache stores compiled bytecode in shared memory, dramatically improving performance.

**Incorrect (OPcache disabled or misconfigured):**

```ini
; OPcache disabled - every request recompiles
opcache.enable=0

; Or insufficient memory
opcache.memory_consumption=32
opcache.max_accelerated_files=2000

; Revalidating too often
opcache.revalidate_freq=0
```

**Correct (production OPcache configuration):**

```ini
; php.ini production settings

; Enable OPcache
opcache.enable=1
opcache.enable_cli=1

; Memory settings (adjust based on your codebase)
opcache.memory_consumption=256
opcache.interned_strings_buffer=64
opcache.max_accelerated_files=20000

; Production: never check for file changes
; Deploy with opcache_reset() or php-fpm reload
opcache.validate_timestamps=0

; Development only: check files periodically
; opcache.validate_timestamps=1
; opcache.revalidate_freq=2

; Performance optimizations
opcache.save_comments=1
opcache.fast_shutdown=1

; JIT compilation (PHP 8+)
opcache.jit_buffer_size=100M
opcache.jit=1255
```

**Deployment script to clear cache:**

```php
<?php
// deploy.php - call after deployment
if (function_exists('opcache_reset')) {
    opcache_reset();
    echo "OPcache cleared\n";
}

// Or reload PHP-FPM
// sudo systemctl reload php-fpm
```

**Check OPcache status:**

```php
<?php
$status = opcache_get_status();
$config = opcache_get_configuration();

echo "Memory used: " . round($status['memory_usage']['used_memory'] / 1024 / 1024) . "MB\n";
echo "Hit rate: " . round($status['opcache_statistics']['opcache_hit_rate'], 2) . "%\n";
echo "Cached files: " . $status['opcache_statistics']['num_cached_scripts'] . "\n";
```

Reference: [PHP OPcache](https://www.php.net/manual/en/book.opcache.php)
