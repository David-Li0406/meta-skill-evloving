<?php
// CRITICAL: Enable errors FIRST before anything else
error_reporting(E_ALL);
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');

// Start output buffering to allow redirects from included pages (like login.php)
ob_start();

// Start session if not started
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

// Load config files
$hubConfigPath = __DIR__ . '/hub-config.php';
if (file_exists($hubConfigPath)) {
    require_once $hubConfigPath;
}

$routerPath = __DIR__ . '/router.php';
if (file_exists($routerPath)) {
    require_once $routerPath;
}

// Fallback for hub_get_theme
if (!function_exists('hub_get_theme')) {
    function hub_get_theme() {
        return 'dark';
    }
}

// Fallback for hub_is_ajax
if (!function_exists('hub_is_ajax')) {
    function hub_is_ajax() {
        return !empty($_SERVER['HTTP_X_REQUESTED_WITH']) &&
               strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest';
    }
}

// Fallback for hub_get_current_page
if (!function_exists('hub_get_current_page')) {
    function hub_get_current_page() {
        return [
            'page' => 'welcome',
            'section' => null,
            'params' => [],
            'file' => __DIR__ . '/pages/welcome.php'
        ];
    }
}

$pageInfo = hub_get_current_page();
$theme = hub_get_theme();

// AJAX request = return only content
if (hub_is_ajax()) {
    header('Content-Type: text/html; charset=utf-8');
    header('X-Page-Title: ' . ucfirst($pageInfo['page']) . ' – TheHUB');

    include __DIR__ . '/components/breadcrumb.php';

    if (file_exists($pageInfo['file'])) {
        include $pageInfo['file'];
    } else {
        include HUB_ROOT . '/pages/404.php';
    }
    exit;
}
?>
<!DOCTYPE html>
<html lang="sv">
<head>
    <?php include __DIR__ . '/components/head.php'; ?>
</head>
<body>
    <a href="#main-content" class="skip-link">Hoppa till huvudinnehåll</a>

    <?php include __DIR__ . '/components/header.php'; ?>

    <div class="app-layout">
        <?php include __DIR__ . '/components/sidebar.php'; ?>

        <main id="main-content" class="main-content" role="main" aria-live="polite" tabindex="-1">
            <?php include __DIR__ . '/components/breadcrumb.php'; ?>

            <div id="page-content" class="page-content">
                <?php
                if (file_exists($pageInfo['file'])) {
                    include $pageInfo['file'];
                } else {
                    include HUB_ROOT . '/pages/404.php';
                }
                ?>
            </div>
        </main>
    </div>

    <?php include __DIR__ . '/components/mobile-nav.php'; ?>
    <?php include __DIR__ . '/components/footer.php'; ?>
    <?php include __DIR__ . '/components/woocommerce-modal.php'; ?>

    <!-- Toast Container -->
    <div id="toast-container" class="toast-container"></div>

    <script src="<?= hub_asset('js/theme.js') ?>"></script>
    <script src="<?= hub_asset('js/router.js') ?>"></script>
    <script src="<?= hub_asset('js/app.js') ?>"></script>
    <script src="<?= hub_asset('js/search.js') ?>"></script>
    <script src="<?= hub_asset('js/registration.js') ?>"></script>
    <script src="<?= hub_asset('js/woocommerce.js') ?>"></script>
    <script src="<?= hub_asset('js/badge-system.js') ?>"></script>
    <script src="<?= hub_asset('js/pwa.js') ?>"></script>

    <!-- FOUC Prevention: Reveal content after CSS loaded -->
    <script>
        (function() {
            var main = document.querySelector('.main-content');
            if (main) {
                requestAnimationFrame(function() {
                    requestAnimationFrame(function() {
                        main.classList.add('css-ready');
                    });
                });
            }
        })();
    </script>

    <!-- Initialize Lucide icons -->
    <script>
        lucide.createIcons();
        // Re-initialize icons after AJAX page loads
        document.addEventListener('hub:contentloaded', () => lucide.createIcons());
    </script>
</body>
</html>
