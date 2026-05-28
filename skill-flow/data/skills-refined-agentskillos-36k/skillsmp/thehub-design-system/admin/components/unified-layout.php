<?php
/**
 * Admin Unified Layout - Uses same layout as public site
 *
 * Usage:
 *   $page_title = 'Dashboard';
 *   $breadcrumbs = [['label' => 'Admin'], ['label' => 'Dashboard']];
 *   $page_actions = '<a href="..." class="btn btn-primary">Action</a>'; // Optional
 *   include __DIR__ . '/components/unified-layout.php';
 *
 * The content should be placed in $admin_content variable before including this file.
 */

// Ensure we have the hub config
require_once __DIR__ . '/../../hub-config.php';
require_once __DIR__ . '/../../config.php';

// Ensure admin authentication
require_admin();

// Get theme
$theme = hub_get_theme();

// Get pending claims count for header notification
$pendingClaimsCount = 0;
try {
    global $pdo;
    if ($pdo) {
        $pendingClaimsCount = (int)$pdo->query("SELECT COUNT(*) FROM rider_claims WHERE status = 'pending'")->fetchColumn();
    }
} catch (Exception $e) {
    $pendingClaimsCount = 0;
}

// Create a mock pageInfo for the sidebar
$pageInfo = [
    'page' => 'admin',
    'section' => 'admin',
    'params' => []
];

// Auto-detect current admin page from URL for sidebar highlighting
if (!isset($current_admin_page)) {
    $scriptName = basename($_SERVER['SCRIPT_NAME'] ?? '', '.php');
    // PHP 5.x/7.x compatible - use array lookup instead of match()
    $pageMap = array(
        'promotor' => 'events',
        'event-edit' => 'events',
        'event-create' => 'events',
        'events' => 'events',
        'media' => 'media',
        'media-archive' => 'media',
        'sponsors' => 'sponsors',
        'sponsor-edit' => 'sponsors',
        'dashboard' => 'dashboard',
        'series' => 'series',
        'series-events' => 'series',
        'series-pricing' => 'series',
        'riders' => 'riders',
        'rider-edit' => 'riders',
        'clubs' => 'clubs',
        'club-edit' => 'clubs',
        'import' => 'import',
        'ranking' => 'ranking',
        'settings' => 'settings',
        'system-settings' => 'settings',
        'role-permissions' => 'settings'
    );
    $current_admin_page = isset($pageMap[$scriptName]) ? $pageMap[$scriptName] : $scriptName;
}
?>
<!DOCTYPE html>
<html lang="sv" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($page_title ?? 'Admin') ?> - TheHUB Admin</title>

    <!-- Force light theme - same as public site -->
    <script>
    (function() {
        // Always use light theme (dark mode disabled)
        document.documentElement.setAttribute('data-theme', 'light');
    })();
    </script>

    <!-- Favicon from branding.json -->
    <?php
    $faviconUrl = '/assets/favicon.svg';
    $faviconBrandingFile = __DIR__ . '/../../uploads/branding.json';
    if (file_exists($faviconBrandingFile)) {
        $faviconBranding = json_decode(file_get_contents($faviconBrandingFile), true);
        if (!empty($faviconBranding['logos']['favicon'])) {
            $faviconUrl = $faviconBranding['logos']['favicon'];
        }
    }
    $faviconExt = strtolower(pathinfo($faviconUrl, PATHINFO_EXTENSION));
    // PHP 5.x/7.x compatible - use array lookup instead of match()
    $faviconMimeMap = array(
        'svg' => 'image/svg+xml',
        'png' => 'image/png',
        'ico' => 'image/x-icon'
    );
    $faviconMime = isset($faviconMimeMap[$faviconExt]) ? $faviconMimeMap[$faviconExt] : 'image/png';
    ?>
    <link rel="icon" type="<?= $faviconMime ?>" href="<?= htmlspecialchars($faviconUrl) ?>">
    <link rel="icon" type="<?= $faviconMime ?>" sizes="32x32" href="<?= htmlspecialchars($faviconUrl) ?>">
    <link rel="apple-touch-icon" href="<?= htmlspecialchars($faviconUrl) ?>">
    <link rel="manifest" href="/admin/manifest.json">
    <meta name="theme-color" content="#0066CC">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="HUB Admin">

    <!-- V3 CSS -->
    <link rel="stylesheet" href="<?= hub_asset('css/reset.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/tokens.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/theme.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/layout.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/components.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/tables.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/utilities.css') ?>">
    <link rel="stylesheet" href="<?= hub_asset('css/grid.css') ?>">

    <!-- Admin Layout CSS - ONLY structure, NO color overrides -->
    <!-- Uses CSS variables from theme.css for all colors -->
    <!-- Original admin.css (3,784 lines) + admin-theme-fix.css (514 lines) -->
    <!-- Replaced with minimal layout-only.css (350 lines) -->
    <link rel="stylesheet" href="/admin/assets/css/admin-layout-only.css?v=<?= filemtime(__DIR__ . '/../assets/css/admin-layout-only.css') ?>">

    <!-- Admin Color Fix - Restores correct blue accent colors (#0066CC) -->
    <!-- Loads LAST to override any remaining cyan colors -->
    <link rel="stylesheet" href="/admin/assets/css/admin-color-fix.css?v=<?= filemtime(__DIR__ . '/../assets/css/admin-color-fix.css') ?>">

    <!-- Dynamic Branding CSS (from /uploads/branding.json) -->
    <?php
    $brandingFile = __DIR__ . '/../../uploads/branding.json';
    if (file_exists($brandingFile)) {
        $brandingData = json_decode(file_get_contents($brandingFile), true);
        if (is_array($brandingData)) {
            $cssOutput = '';
            $colorsCss = '';

            // Process custom colors from branding (use light theme colors for everything)
            if (!empty($brandingData['colors'])) {
                $colors = $brandingData['colors'];
                // Use light theme colors (or fall back to dark if light not set)
                $colorSource = $colors['light'] ?? $colors['dark'] ?? $colors;
                if (is_array($colorSource)) {
                    foreach ($colorSource as $cssVar => $value) {
                        if (strpos($cssVar, '--') === 0) {
                            $safeValue = htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
                            if (preg_match('/^(#[0-9A-Fa-f]{3,8}|rgba?\([^)]+\)|hsla?\([^)]+\)|[a-z]+)$/', $value)) {
                                $colorsCss .= $cssVar . ':' . $safeValue . ' !important;';
                            }
                        }
                    }
                }
            }

            // Process layout settings (content-max-width, sidebar-width, header-height)
            $layout = $brandingData['layout'] ?? null;
            if ($layout) {
                $contentMaxWidth = $layout['content_max_width'] ?? '1400';
                if ($contentMaxWidth === 'none') {
                    $cssOutput .= '--content-max-width:none;';
                } else {
                    $cssOutput .= '--content-max-width:' . intval($contentMaxWidth) . 'px;';
                }
                $sidebarWidth = intval($layout['sidebar_width'] ?? 72);
                $cssOutput .= '--sidebar-width:' . $sidebarWidth . 'px;';
                $headerHeight = intval($layout['header_height'] ?? 60);
                $cssOutput .= '--header-height:' . $headerHeight . 'px;';
            }

            // Process responsive layout settings
            $responsive = $brandingData['responsive'] ?? null;
            if ($responsive) {
                $desktopPadding = intval($responsive['desktop']['padding'] ?? 32);
                $desktopRadius = intval($responsive['desktop']['radius'] ?? 12);
                $cssOutput .= '--container-padding:' . $desktopPadding . 'px;';
                $cssOutput .= '--radius-sm:' . $desktopRadius . 'px;';
                $cssOutput .= '--radius-md:' . $desktopRadius . 'px;';
                $cssOutput .= '--radius-lg:' . $desktopRadius . 'px;';
            }

            // Process gradient settings
            $gradient = $brandingData['gradient'] ?? null;
            if ($gradient && !empty($gradient['enabled'])) {
                $angle = intval($gradient['angle'] ?? 135);
                $cssOutput .= '--gradient-angle:' . max(0, min(360, $angle)) . 'deg;';
                if (!empty($gradient['start']) && preg_match('/^#[0-9A-Fa-f]{6}$/', $gradient['start'])) {
                    $cssOutput .= '--gradient-start:' . htmlspecialchars($gradient['start'], ENT_QUOTES, 'UTF-8') . ';';
                }
                if (!empty($gradient['end']) && preg_match('/^#[0-9A-Fa-f]{6}$/', $gradient['end'])) {
                    $cssOutput .= '--gradient-end:' . htmlspecialchars($gradient['end'], ENT_QUOTES, 'UTF-8') . ';';
                }
            }

            // Output combined CSS
            if ($cssOutput || $colorsCss || $layout || $gradient) {
                echo '<style id="admin-branding">';
                if ($cssOutput) {
                    echo ':root{' . $cssOutput . '}';
                }
                if ($colorsCss) {
                    echo ':root{' . $colorsCss . '}';
                }
                echo '</style>';
            }
        }
    }
    ?>

    <!-- Prevent icon flash: hide data-lucide elements until JS replaces them -->
    <style>
        [data-lucide] {
            display: none !important;
        }
        /* Once lucide replaces them with SVG, they become visible */
        svg.lucide {
            display: inline-block !important;
        }
    </style>
</head>
<body>
    <a href="#main-content" class="skip-link">Hoppa till huvudinnehåll</a>

    <?php include HUB_ROOT . '/components/header.php'; ?>

    <div class="app-layout">
        <?php include HUB_ROOT . '/components/sidebar.php'; ?>

        <main id="main-content" class="main-content" role="main">
            <!-- Admin Submenu (automatic based on current page) -->
            <?php include __DIR__ . '/../../includes/components/admin-submenu.php'; ?>

            <!-- Page Header -->
            <div class="page-header admin-page-header">
                <h1 class="page-title"><?= htmlspecialchars($page_title ?? 'Admin') ?></h1>
                <?php if (isset($page_actions)): ?>
                    <div class="page-actions">
                        <?= $page_actions ?>
                    </div>
                <?php endif; ?>
            </div>

            <!-- Flash Messages -->
            <?php if (has_flash('success')): ?>
                <div class="alert alert-success">
                    <?= htmlspecialchars(get_flash('success')) ?>
                </div>
            <?php endif; ?>

            <?php if (has_flash('error')): ?>
                <div class="alert alert-error">
                    <?= htmlspecialchars(get_flash('error')) ?>
                </div>
            <?php endif; ?>

            <?php if (has_flash('warning')): ?>
                <div class="alert alert-warning">
                    <?= htmlspecialchars(get_flash('warning')) ?>
                </div>
            <?php endif; ?>

            <!-- Page Content -->
            <div class="page-content admin-content">
