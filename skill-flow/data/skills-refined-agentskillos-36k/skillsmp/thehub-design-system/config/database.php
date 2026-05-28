<?php
/**
 * Database Configuration
 *
 * IMPORTANT: This file is configured for LOCAL DEVELOPMENT
 * For production (InfinityFree), use the credentials from .env file
 */

// Check if we're using environment-based config
if (function_exists('env')) {
    $host = env('DB_HOST');
    $name = env('DB_NAME');
    $user = env('DB_USER');
    $pass = env('DB_PASS');

    // If env vars are set and NOT placeholder values, use them
    if ($host && $name && $user &&
        !str_contains($host, 'REPLACE_WITH') &&
        !str_contains($name, 'REPLACE_WITH') &&
        !str_contains($user, 'REPLACE_WITH')) {

        define('DB_HOST', $host);
        define('DB_NAME', $name);
        define('DB_USER', $user);
        define('DB_PASS', $pass);
        define('DB_CHARSET', env('DB_CHARSET', 'utf8mb4'));
        define('DB_ERROR_DISPLAY', env('APP_DEBUG', 'false') === 'true');

        error_log("✅ Database config loaded from .env file");
        error_log("   Host: " . DB_HOST);
        error_log("   Database: " . DB_NAME);
        error_log("   User: " . DB_USER);
        return;
    }
}

// Fallback to local development settings
// CHANGE THESE for your local MySQL setup
define('DB_HOST', 'localhost');
define('DB_NAME', 'thehub');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_CHARSET', 'utf8mb4');
define('DB_ERROR_DISPLAY', true);

error_log("⚠️  Database config using LOCAL DEVELOPMENT defaults");
error_log("   Host: " . DB_HOST);
error_log("   Database: " . DB_NAME);
error_log("   User: " . DB_USER);
error_log("   ⚠️  For production, create .env file with real credentials!");
