<?php
define('THEHUB_INIT', true);

// Centralized error handling - NEVER show errors in production
error_reporting(E_ALL);
ini_set('log_errors', '1');
ini_set('error_log', __DIR__ . '/logs/error.log');

function env($key, $default = null) {
    $value = getenv($key);
    if ($value === false) {
        // Check .env first, then .env.production as fallback
        $envFiles = [
            __DIR__ . '/.env',
            __DIR__ . '/.env.production'
        ];
        foreach ($envFiles as $envFile) {
            if (file_exists($envFile)) {
                $lines = file($envFile);
                foreach ($lines as $line) {
                    $line = trim($line);
                    // Skip comments and empty lines
                    if (empty($line) || strpos($line, '#') === 0) continue;
                    if (strpos($line, '=') !== false) {
                        list($k, $v) = explode('=', $line, 2);
                        if (trim($k) === $key) {
                            return trim($v);
                        }
                    }
                }
            }
        }
        return $default;
    }
    return $value;
}

define('ROOT_PATH', __DIR__);
define('INCLUDES_PATH', __DIR__ . '/includes');
define('UPLOADS_PATH', __DIR__ . '/uploads');
define('SITE_URL', env('SITE_URL', 'https://thehub.gravityseries.se'));

// Database configuration - MUST be set in .env file
define('DB_HOST', env('DB_HOST', 'localhost'));
define('DB_NAME', env('DB_NAME'));
define('DB_USER', env('DB_USER'));
define('DB_PASS', env('DB_PASS'));

// Check required database configuration
if (!DB_NAME || !DB_USER || !DB_PASS) {
    die('Database configuration missing. Please create a .env file with DB_NAME, DB_USER, and DB_PASS.');
}

define('APP_NAME', 'TheHUB');

// Admin credentials - MUST be set via environment variables in production
define('DEFAULT_ADMIN_USERNAME', env('ADMIN_USERNAME', 'admin'));
define('DEFAULT_ADMIN_PASSWORD_HASH', env('ADMIN_PASSWORD_HASH'));

// Security settings
define('CSRF_TOKEN_NAME', 'csrf_token');
define('MAX_UPLOAD_SIZE', 10 * 1024 * 1024); // 10MB
define('EVENTS_PER_PAGE', 20);
define('FORCE_HTTPS', env('FORCE_HTTPS', 'true'));

// Environment
define('APP_ENV', env('APP_ENV', 'production'));

// Force HTTPS in production
if (FORCE_HTTPS === 'true' && APP_ENV !== 'development') {
    if (!isset($_SERVER['HTTPS']) || $_SERVER['HTTPS'] !== 'on') {
        // Allow CLI and certain trusted proxies
        $behindProxy = isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https';
        if (!$behindProxy && php_sapi_name() !== 'cli') {
            $redirect = 'https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
            header('HTTP/1.1 301 Moved Permanently');
            header('Location: ' . $redirect);
            exit;
        }
    }
}

// Display errors only in development
if (APP_ENV === 'development') {
    ini_set('display_errors', '1');
} else {
    ini_set('display_errors', '0');
}

// Version info
define('APP_VERSION', '1.0');
define('APP_VERSION_NAME', 'Release');
define('APP_BUILD', '2026-01-23');
define('DEPLOYMENT_OFFSET', 591); // Total deployment count (update before each push if git not available on server)

try {
    $pdo = new PDO(
        'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4',
        DB_USER,
        DB_PASS,
        array(
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false
        )
    );
    $GLOBALS['pdo'] = $pdo;
} catch (PDOException $e) {
    die('Database connection failed');
}

if (session_status() === PHP_SESSION_NONE) {
    // Configure session with longer lifetime (7 days)
    session_set_cookie_params([
        'lifetime' => 604800, // 7 days
        'path' => '/',
        'domain' => '',
        'secure' => isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on',
        'httponly' => true,
        'samesite' => 'Lax'
    ]);
    session_name('thehub_session');
    session_start();
}

// Security headers (only for web requests, not CLI)
if (php_sapi_name() !== 'cli') {
    // Prevent MIME type sniffing
    header("X-Content-Type-Options: nosniff");

    // Prevent clickjacking
    header("X-Frame-Options: SAMEORIGIN");

    // Enable XSS filter in older browsers
    header("X-XSS-Protection: 1; mode=block");

    // Control referrer information
    header("Referrer-Policy: strict-origin-when-cross-origin");

    // Disable dangerous browser features
    header("Permissions-Policy: geolocation=(), microphone=(), camera=()");

    // HSTS - Force HTTPS for 1 year (only if HTTPS is enabled)
    if (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on') {
        header("Strict-Transport-Security: max-age=31536000; includeSubDomains");
    }

    // Content Security Policy - Allow Lucide icons from unpkg.com
    header("Content-Security-Policy: default-src 'self'; script-src 'self' https://unpkg.com 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:;");
}

date_default_timezone_set('Europe/Stockholm');

require_once __DIR__ . '/includes/helpers.php';
require_once __DIR__ . '/includes/auth.php';
?>
