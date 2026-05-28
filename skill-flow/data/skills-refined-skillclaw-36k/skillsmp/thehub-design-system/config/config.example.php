<?php
/**
 * Application Configuration Example
 * Copy this file to config.php and customize
 */

// Application settings
define('APP_NAME', 'TheHUB');
define('APP_URL', 'https://yourdomain.se');

// Paths
define('ROOT_PATH', dirname(__DIR__));
define('UPLOAD_PATH', ROOT_PATH . '/uploads');

// Admin settings
define('ADMIN_EMAIL', 'admin@yourdomain.se');
define('ADMIN_PASSWORD_HASH', ''); // Use password_hash() to generate

// Session settings
define('SESSION_NAME', 'thehub_session');
define('SESSION_LIFETIME', 3600 * 24); // 24 hours

// Import settings
define('MAX_UPLOAD_SIZE', 10 * 1024 * 1024); // 10MB
define('ALLOWED_EXTENSIONS', ['xlsx', 'xls', 'csv']);

// Display settings
define('RESULTS_PER_PAGE', 50);
define('EVENTS_PER_PAGE', 20);

// Timezone
date_default_timezone_set('Europe/Stockholm');
