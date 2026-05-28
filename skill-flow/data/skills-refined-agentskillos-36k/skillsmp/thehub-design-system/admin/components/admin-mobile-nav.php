<?php
/**
 * TheHUB Admin Mobile Navigation
 * Horizontally scrollable bottom nav for admin pages
 *
 * NOTE: Primary navigation is defined in /includes/config/admin-tabs-config.php
 * and rendered via /components/sidebar.php
 *
 * This mobile nav should be kept in sync with admin-tabs-config.php
 * (admin-sidebar.php has been deprecated - 2026-01-12)
 *
 * Role-based access:
 * - promotor: Dashboard, Tävlingar, Serier
 * - admin/super_admin: + Ekonomi, Konfiguration, Databas, Import, System
 */
require_once __DIR__ . '/../../hub-config.php';
require_once __DIR__ . '/../../components/icons.php';
require_once __DIR__ . '/../../includes/auth.php';

// Get current user's role for filtering
$currentAdminRole = $_SESSION['admin_role'] ?? 'admin';
$isPromotor = ($currentAdminRole === 'promotor');
$roleHierarchy = ['promotor' => 1, 'admin' => 2, 'super_admin' => 3];
$userRoleLevel = $roleHierarchy[$currentAdminRole] ?? 0;

// Check analytics access
$hasAnalytics = function_exists('hasAnalyticsAccess') && hasAnalyticsAccess();

// Admin navigation - should match /includes/config/admin-tabs-config.php
// Promotors get different URLs than admins
$adminNav = [];

if ($isPromotor) {
    // PROMOTOR navigation - specific pages for promotors
    $adminNav = [
        ['id' => 'dashboard', 'label' => 'Tävlingar', 'icon' => 'calendar', 'url' => '/admin/promotor.php'],
        ['id' => 'series', 'label' => 'Serier', 'icon' => 'trophy', 'url' => '/admin/promotor-series.php'],
        ['id' => 'media', 'label' => 'Media', 'icon' => 'image', 'url' => '/admin/sponsors.php'],
        ['id' => 'onsite', 'label' => 'Direktanmälan', 'icon' => 'user-plus', 'url' => '/admin/onsite-registration.php'],
    ];
} else {
    // ADMIN navigation - full admin access
    $adminNav = [
        ['id' => 'dashboard', 'label' => 'Dashboard', 'icon' => 'layout-dashboard', 'url' => '/admin/dashboard.php'],
        ['id' => 'events', 'label' => 'Tävlingar', 'icon' => 'calendar', 'url' => '/admin/events.php'],
        ['id' => 'series', 'label' => 'Serier', 'icon' => 'trophy', 'url' => '/admin/series.php'],
        ['id' => 'ekonomi', 'label' => 'Ekonomi', 'icon' => 'wallet', 'url' => '/admin/ekonomi.php'],
        ['id' => 'config', 'label' => 'Konfig', 'icon' => 'sliders', 'url' => '/admin/classes.php'],
        ['id' => 'riders', 'label' => 'Databas', 'icon' => 'users', 'url' => '/admin/riders.php'],
        ['id' => 'import', 'label' => 'Import', 'icon' => 'upload', 'url' => '/admin/import.php'],
    ];

    // Analytics for super_admin or statistics permission
    if ($hasAnalytics) {
        $adminNav[] = ['id' => 'analytics', 'label' => 'Analytics', 'icon' => 'bar-chart-3', 'url' => '/admin/analytics-dashboard.php'];
    }

    // System only for super_admin
    if ($currentAdminRole === 'super_admin') {
        $adminNav[] = ['id' => 'settings', 'label' => 'System', 'icon' => 'settings', 'url' => '/admin/users.php'];
    }
}

// Determine active page from URL
$requestUri = $_SERVER['REQUEST_URI'] ?? '';
$currentPath = parse_url($requestUri, PHP_URL_PATH);

function isAdminNavActive($item, $currentPath) {
    $itemPath = parse_url($item['url'], PHP_URL_PATH);

    // Dashboard special case
    if ($item['id'] === 'dashboard') {
        return $currentPath === '/admin/dashboard' ||
               $currentPath === '/admin/promotor' ||
               $currentPath === '/admin/' ||
               $currentPath === '/admin';
    }

    // Analytics special case - match all analytics pages
    if ($item['id'] === 'analytics') {
        return strpos($currentPath, '/admin/analytics') === 0;
    }

    // Check if current path starts with this item's path
    return strpos($currentPath, $itemPath) === 0;
}
?>
<nav class="admin-mobile-nav" role="navigation" aria-label="Admin navigering">
    <div class="admin-mobile-nav-inner">
        <?php foreach ($adminNav as $item): ?>
            <?php $isActive = isAdminNavActive($item, $currentPath); ?>
            <a href="<?= htmlspecialchars($item['url']) ?>"
               class="admin-mobile-nav-link<?= $isActive ? ' active' : '' ?>"
               <?= $isActive ? 'aria-current="page"' : '' ?>>
                <span class="admin-mobile-nav-icon"><?= hub_icon($item['icon']) ?></span>
                <span class="admin-mobile-nav-label"><?= htmlspecialchars($item['label']) ?></span>
            </a>
        <?php endforeach; ?>
    </div>
</nav>
