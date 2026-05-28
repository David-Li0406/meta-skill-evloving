<?php
/**
 * Standardized Layout Header for TheHUB
 *
 * Usage:
 *   $pageTitle = 'Dashboard';
 *   $pageType = 'admin'; // or 'public'
 *   include __DIR__ . '/../includes/layout-header.php';
 *
 * Variables:
 *   - $pageTitle (required): The page title
 *   - $pageType (required): 'admin' or 'public'
 *   - $bodyClass (optional): Additional body classes
 */

// ============================================================================
// SECURITY HEADERS
// ============================================================================
// Prevent page from being displayed in an iframe (clickjacking protection)
header("X-Frame-Options: DENY");

// Prevent MIME type sniffing
header("X-Content-Type-Options: nosniff");

// Control referrer information
header("Referrer-Policy: no-referrer-when-downgrade");

// Permissions policy (disable unnecessary features)
header("Permissions-Policy: geolocation=(), microphone=(), camera=()");

// XSS Protection (for older browsers)
header("X-XSS-Protection: 1; mode=block");

// Strict Transport Security (HSTS) - only when using HTTPS
if (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on') {
    header("Strict-Transport-Security: max-age=31536000; includeSubDomains");
}

// Content Security Policy (allow self + unpkg.com for Lucide icons)
$csp = implode('; ', [
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline' https://unpkg.com",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "font-src 'self' data:",
    "connect-src 'self'",
    "frame-ancestors 'none'"
]);
header("Content-Security-Policy: {$csp}");

// ============================================================================
// PAGE SETUP
// ============================================================================
// Validate required variables
if (!isset($pageTitle)) {
    $pageTitle = 'TheHUB';
}

if (!isset($pageType)) {
    $pageType = 'public';
}

// ============================================================================
// AUTOMATIC PAGE TYPE DETECTION
// ============================================================================
// Detect event pages automatically based on URL pattern /event/{ID}
$requestUri = $_SERVER['REQUEST_URI'] ?? '';
$isEventPage = preg_match('#^/event/\d+#', $requestUri) === 1;
$isAdminPage = strpos($requestUri, '/admin') === 0;

// Build body classes array
$bodyClasses = [];

// Page type class
if ($pageType === 'admin' || $isAdminPage) {
    $bodyClasses[] = 'admin-page';
    $bodyClasses[] = 'is-admin';
} else {
    $bodyClasses[] = 'public-page';
    $bodyClasses[] = 'is-public';
}

// Event page isolation - automatic detection (NO manual override allowed)
if ($isEventPage) {
    $bodyClasses[] = 'event-page';
}

// Add any custom body classes
if (isset($bodyClass) && !empty($bodyClass)) {
    $bodyClasses[] = $bodyClass;
}

// Determine title suffix and final body class string
$titleSuffix = ($pageType === 'admin') ? ' - TheHUB Admin' : ' - TheHUB';
$bodyClass = implode(' ', array_unique($bodyClasses));

// Get theme from user profile or default to dark
$userTheme = 'dark';
$isLoggedIn = isset($_SESSION['rider_id']) && $_SESSION['rider_id'] > 0;
if ($isLoggedIn && function_exists('get_current_rider')) {
    try {
        $currentUser = get_current_rider();
        if (isset($currentUser['theme_preference'])) {
            $userTheme = $currentUser['theme_preference'];
        }
    } catch (Exception $e) {
        // Use default
    }
}
// Force light theme for now (dark theme disabled)
$userTheme = 'light';
?>
<!DOCTYPE html>
<html lang="sv" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title><?= h($pageTitle) ?><?= $titleSuffix ?></title>

    <!-- Force light theme - dark mode disabled for now -->
    <script>
    (function() {
        // Always use light theme
        document.documentElement.setAttribute('data-theme', 'light');
    })();
    window.HUB = window.HUB || {};
    window.HUB.isLoggedIn = <?= $isLoggedIn ? 'true' : 'false' ?>;
    </script>

    <!-- CRITICAL CSS - Moved to critical-inline.css for maintainability -->

    <!-- Google Fonts - Required for typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cabin+Condensed:wght@400;500;600;700&family=Manrope:wght@300;400;500;600;700&family=Oswald:wght@400;500;600;700&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">

    <!-- CRITICAL: Inline CSS extracted to file for maintainability -->
    <!-- MUST load FIRST to prevent FOUC and ensure sidebar visibility -->
    <link rel="stylesheet" href="/assets/css/critical-inline.css?v=<?= filemtime(__DIR__ . '/../assets/css/critical-inline.css') ?>">

    <!-- Design System CSS -->
    <!-- 1. CSS Reset -->
    <link rel="stylesheet" href="/assets/css/reset.css?v=<?= filemtime(__DIR__ . '/../assets/css/reset.css') ?>">

    <!-- 2. Design Tokens -->
    <link rel="stylesheet" href="/assets/css/tokens.css?v=<?= filemtime(__DIR__ . '/../assets/css/tokens.css') ?>">

    <!-- 3. Theme Variables (Light/Dark/Auto Support) -->
    <link rel="stylesheet" href="/assets/css/theme.css?v=<?= filemtime(__DIR__ . '/../assets/css/theme.css') ?>">
    
    <!-- 3.5. Branding Overrides (from uploads/branding.json) - MUST come after theme.css -->
    <?= generateBrandingCSS() ?>

    <!-- 4. Layout System -->
    <link rel="stylesheet" href="/assets/css/layout.css?v=<?= filemtime(__DIR__ . '/../assets/css/layout.css') ?>">

    <!-- 5. UI Components -->
    <link rel="stylesheet" href="/assets/css/components.css?v=<?= filemtime(__DIR__ . '/../assets/css/components.css') ?>">

    <!-- 6. Table Styles -->
    <link rel="stylesheet" href="/assets/css/tables.css?v=<?= filemtime(__DIR__ . '/../assets/css/tables.css') ?>">

    <!-- 7. Utility Classes -->
    <link rel="stylesheet" href="/assets/css/utilities.css?v=<?= filemtime(__DIR__ . '/../assets/css/utilities.css') ?>">

    <!-- 8. Grid System -->
    <link rel="stylesheet" href="/assets/css/grid.css?v=<?= filemtime(__DIR__ . '/../assets/css/grid.css') ?>">

    <!-- 9. PWA Support -->
    <link rel="stylesheet" href="/assets/css/pwa.css?v=<?= filemtime(__DIR__ . '/../assets/css/pwa.css') ?>">

    <!-- 9. GS Compatibility Layer (maps old gs-* classes to V1.0) -->
    <link rel="stylesheet" href="/assets/css/compatibility.css?v=<?= filemtime(__DIR__ . '/../assets/css/compatibility.css') ?>">

    <!-- 10. Global Sponsors & Blog System -->
    <link rel="stylesheet" href="/assets/css/sponsors-blog.css?v=<?= filemtime(__DIR__ . '/../assets/css/sponsors-blog.css') ?>">

    <!-- ============================================================================
         PAGE-SPECIFIC CSS - Dynamic loading based on current page
         Automatically loads CSS for current page from /assets/css/pages/
         Symlinks are supported transparently (e.g., login.css → auth.css)
         ============================================================================ -->
    <?php
    // Get current page slug from filename
    $pageSlug = basename($_SERVER['PHP_SELF'], '.php');
    $requestUri = $_SERVER['REQUEST_URI'] ?? '';

    // Special handling for event pages (URL pattern: /event/123, /event/abc)
    if (preg_match('#^/event/[^/]+#', $requestUri)) {
        $pageSlug = 'event';
    }

    // Special handling for calendar event pages
    if (preg_match('#^/calendar/event/[^/]+#', $requestUri)) {
        $pageSlug = 'calendar-event';
    }

    // Map special pages to their CSS files
    $pageStyleMap = [
        'index'              => 'welcome',
        'calendar'           => 'calendar-index',
        'event'              => 'calendar-event',
        'results'            => 'results-index',
        'profile'            => 'profile-index',
        'login'              => 'auth',
        'register'           => 'auth',
        'forgot-password'    => 'auth',
        'reset-password'     => 'auth',
        'activate-account'   => 'auth',
        // Add more mappings as needed
    ];

    // Determine which CSS file to load
    $pageStyle = $pageStyleMap[$pageSlug] ?? $pageSlug;
    $cssPath = __DIR__ . "/../assets/css/pages/{$pageStyle}.css";

    // Check if page-specific CSS exists (follows symlinks automatically)
    if (file_exists($cssPath)) {
        $version = filemtime($cssPath);
        echo "    <link rel=\"stylesheet\" href=\"/assets/css/pages/{$pageStyle}.css?v={$version}\">\n";
    }
    ?>

    <!-- PWA Support -->
    <link rel="manifest" href="/manifest.php">
    <meta name="theme-color" content="#004A98">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="TheHUB">
    <!-- Favicon (from branding or default) -->
    <?php
    $brandingFavicon = getBranding('logos.favicon');
    $faviconUrl = $brandingFavicon ?: '/assets/favicon.svg';

    // Detect favicon MIME type from extension
    $faviconExt = strtolower(pathinfo($faviconUrl, PATHINFO_EXTENSION));
    // PHP 5.x/7.x compatible - use array lookup instead of match()
    $faviconMimeMap = array(
        'svg' => 'image/svg+xml',
        'png' => 'image/png',
        'jpg' => 'image/jpeg',
        'jpeg' => 'image/jpeg',
        'ico' => 'image/x-icon',
        'gif' => 'image/gif',
        'webp' => 'image/webp'
    );
    $faviconMime = isset($faviconMimeMap[$faviconExt]) ? $faviconMimeMap[$faviconExt] : 'image/png';

    // Use branding favicon for apple-touch-icon - use favicon URL regardless of format
    // iOS modern Safari supports SVG, older versions will use manifest icons
    $appleTouchIcon = $faviconUrl;
    ?>
    <link rel="apple-touch-icon" href="<?= h($appleTouchIcon) ?>">
    <link rel="icon" type="<?= $faviconMime ?>" href="<?= h($faviconUrl) ?>">
    <link rel="icon" type="<?= $faviconMime ?>" sizes="32x32" href="<?= h($faviconUrl) ?>">

</head>
<body class="<?= $bodyClass ?>">
    <!-- Hamburger (hidden on desktop via inline CSS) -->
    <button class="mobile-menu-toggle" onclick="toggleMenu()" aria-label="Toggle menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/>
        </svg>
    </button>

    <!-- Navigation - use same sidebar component for consistency -->
    <?php include __DIR__ . '/../components/sidebar.php'; ?>

    <!-- Overlay (hidden on desktop via inline CSS) -->
    <div class="sidebar-overlay" onclick="closeMenu()"></div>

    <!-- Admin Submenu (automatic based on current page) -->
    <?php
    if ($pageType === 'admin') {
        include __DIR__ . '/components/admin-submenu.php';
    }
    ?>
