<?php
/**
 * TheHUB Sidebar Navigation
 * Uses Lucide-style SVG icons
 * Includes admin navigation for admin users
 */

// Ensure hub-config is loaded
if (!defined('HUB_ROOT')) {
    $hubConfig = __DIR__ . '/../hub-config.php';
    if (file_exists($hubConfig)) {
        require_once $hubConfig;
    } else {
        // Fallback definition
        define('HUB_ROOT', dirname(__DIR__));
    }
}

require_once __DIR__ . '/icons.php';
require_once __DIR__ . '/../includes/auth.php';

$currentPage = $pageInfo['page'] ?? 'dashboard';
$currentSection = $pageInfo['section'] ?? '';
// Check roles properly - use hasRole for hierarchical check
// promotor = role 2, admin = role 3, super_admin = role 4
$isPromotorOnly = function_exists('isRole') && isRole('promotor') && !(function_exists('hasRole') && hasRole('admin'));
// isAdminUser must be admin or super_admin, NOT just logged in
$isAdminUser = function_exists('hasRole') && hasRole('admin');
// Promotors should see their limited admin menu, not full admin
$isAdminSection = strpos($_SERVER['REQUEST_URI'], '/admin') === 0;

// Fallback for hub_is_nav_active if not defined
if (!function_exists('hub_is_nav_active')) {
    function hub_is_nav_active($navId, $currentPage) {
        return $navId === $currentPage;
    }
}

// Fallback nav items if HUB_NAV not defined
$sidebarNav = defined('HUB_NAV') ? HUB_NAV : [
    ['id' => 'calendar', 'label' => 'Kalender', 'icon' => 'calendar', 'url' => '/calendar', 'aria' => 'Kalender'],
    ['id' => 'results', 'label' => 'Resultat', 'icon' => 'flag', 'url' => '/results', 'aria' => 'Resultat'],
    ['id' => 'series', 'label' => 'Serier', 'icon' => 'trophy', 'url' => '/series', 'aria' => 'Serier'],
    ['id' => 'database', 'label' => 'Databas', 'icon' => 'search', 'url' => '/database', 'aria' => 'Databas'],
    ['id' => 'ranking', 'label' => 'Ranking', 'icon' => 'trending-up', 'url' => '/ranking', 'aria' => 'Ranking'],
];

// Load admin tabs config to get navigation from single source of truth
require_once __DIR__ . '/../includes/config/admin-tabs-config.php';

// Get pending claims count for notification badge (only in admin section)
$pendingClaimsCount = 0;
if ($isAdminSection && $isAdminUser) {
    try {
        global $pdo;
        if ($pdo) {
            $pendingClaimsCount = (int)$pdo->query("SELECT COUNT(*) FROM rider_claims WHERE status = 'pending'")->fetchColumn();
        }
    } catch (Exception $e) {
        $pendingClaimsCount = 0;
    }
}

// Build admin navigation from config - show only main groups
$dashboardItem = [
    'id' => 'admin-dashboard',
    'label' => 'Dashboard',
    'icon' => 'layout-dashboard',
    'url' => '/admin/dashboard',
    'aria' => 'Admin Dashboard'
];

// Add badge to Dashboard if there are pending claims
if ($pendingClaimsCount > 0) {
    $dashboardItem['badge'] = $pendingClaimsCount;
    $dashboardItem['badgeType'] = 'alert';
}

$adminNav = [$dashboardItem];

// Add main groups from ADMIN_TABS config
foreach ($ADMIN_TABS as $groupId => $group) {
    // Skip super_admin_only groups for non-super admins
    if (isset($group['super_admin_only']) && $group['super_admin_only']) {
        // Special case: Analytics group - also allow users with statistics permission
        if ($groupId === 'analytics') {
            if (!function_exists('hasAnalyticsAccess') || !hasAnalyticsAccess()) {
                continue;
            }
        } else {
            // Default: require super_admin role
            if (!function_exists('hasRole') || !hasRole('super_admin')) {
                continue;
            }
        }
    }

    // Get first tab's URL as the group URL
    $firstTabUrl = $group['tabs'][0]['url'] ?? '/admin/';

    $navItem = [
        'id' => 'admin-' . $groupId,
        'label' => $group['title'],
        'icon' => $group['icon'],
        'url' => $firstTabUrl,
        'aria' => $group['title'],
        'pages' => get_pages_in_group($groupId) // All pages in this group
    ];

    $adminNav[] = $navItem;
}

// Check if current admin page is active - using pages array from config
function isAdminPageActive($item, $requestUri) {
    // Get current page name from URI
    $currentPage = basename(parse_url($requestUri, PHP_URL_PATH));

    // If item has pages array, check if current page is in it
    if (isset($item['pages']) && is_array($item['pages'])) {
        return in_array($currentPage, $item['pages']);
    }

    // Fallback: check by URL prefix
    $groupId = str_replace('admin-', '', $item['id']);
    return strpos($requestUri, '/admin/' . $groupId) !== false;
}
?>
<aside class="sidebar" role="navigation" aria-label="Huvudnavigering">
  <nav class="sidebar-nav">
    <?php if ($isAdminSection && $isAdminUser): ?>
      <!-- Admin Navigation -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Admin</div>
        <?php foreach ($adminNav as $item): ?>
          <?php $isActive = isAdminPageActive($item, $_SERVER['REQUEST_URI']); ?>
          <?php $hasBadge = isset($item['badge']) && $item['badge'] > 0; ?>
          <a href="<?= htmlspecialchars($item['url']) ?>"
             class="sidebar-link<?= $isActive ? ' is-active' : '' ?><?= $hasBadge ? ' has-badge' : '' ?>"
             data-nav="<?= htmlspecialchars($item['id']) ?>"
             data-tooltip="<?= htmlspecialchars($item['label']) ?>"
             <?= $isActive ? 'aria-current="page"' : '' ?>
             aria-label="<?= htmlspecialchars($item['aria']) ?>">
            <span class="sidebar-icon" aria-hidden="true">
              <?= hub_icon($item['icon'], 'sidebar-icon-svg') ?>
              <?php if ($hasBadge): ?>
                <span class="sidebar-badge sidebar-badge--<?= $item['badgeType'] ?? 'default' ?>"><?= $item['badge'] ?></span>
              <?php endif; ?>
            </span>
            <span class="sidebar-label"><?= htmlspecialchars($item['label']) ?></span>
          </a>
        <?php endforeach; ?>
      </div>

      <!-- Divider -->
      <div class="sidebar-divider"></div>

      <!-- Back to Public Site -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Publik</div>
    <?php elseif ($isAdminSection && $isPromotorOnly): ?>
      <!-- Promotor Navigation -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Promotor</div>
        <?php
        $currentPath = $_SERVER['REQUEST_URI'];
        $promotorNav = [
            ['id' => 'events', 'label' => 'Tävlingar', 'icon' => 'calendar', 'url' => '/admin/promotor.php', 'match' => '/admin/promotor.php'],
            ['id' => 'series', 'label' => 'Serier', 'icon' => 'medal', 'url' => '/admin/promotor-series.php', 'match' => '/admin/promotor-series'],
            ['id' => 'media', 'label' => 'Media', 'icon' => 'image', 'url' => '/admin/sponsors.php', 'match' => '/admin/sponsor'],
            ['id' => 'onsite', 'label' => 'Direktanmälan', 'icon' => 'user-plus', 'url' => '/admin/onsite-registration.php', 'match' => '/admin/onsite'],
        ];
        foreach ($promotorNav as $item):
            $isActive = strpos($currentPath, $item['match']) !== false;
        ?>
          <a href="<?= htmlspecialchars($item['url']) ?>"
             class="sidebar-link<?= $isActive ? ' is-active' : '' ?>"
             data-nav="<?= htmlspecialchars($item['id']) ?>"
             data-tooltip="<?= htmlspecialchars($item['label']) ?>"
             <?= $isActive ? 'aria-current="page"' : '' ?>
             aria-label="<?= htmlspecialchars($item['label']) ?>">
            <span class="sidebar-icon" aria-hidden="true">
              <?= hub_icon($item['icon'], 'sidebar-icon-svg') ?>
            </span>
            <span class="sidebar-label"><?= htmlspecialchars($item['label']) ?></span>
          </a>
        <?php endforeach; ?>
      </div>

      <!-- Divider -->
      <div class="sidebar-divider"></div>

      <!-- Back to Public Site -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Publik</div>
    <?php endif; ?>

    <!-- Public Navigation -->
    <?php foreach ($sidebarNav as $item): ?>
      <?php $isActive = !$isAdminSection && hub_is_nav_active($item['id'], $currentPage); ?>
      <a href="<?= htmlspecialchars($item['url']) ?>"
         class="sidebar-link<?= $isActive ? ' is-active' : '' ?>"
         data-nav="<?= htmlspecialchars($item['id']) ?>"
         data-tooltip="<?= htmlspecialchars($item['label']) ?>"
         <?= $isActive ? 'aria-current="page"' : '' ?>
         aria-label="<?= htmlspecialchars($item['aria']) ?>">
        <span class="sidebar-icon" aria-hidden="true"><?= hub_icon($item['icon'], 'sidebar-icon-svg') ?></span>
        <span class="sidebar-label"><?= htmlspecialchars($item['label']) ?></span>
      </a>
    <?php endforeach; ?>

    <?php if ($isAdminSection && ($isAdminUser || $isPromotorOnly)): ?>
      </div>
    <?php endif; ?>

    <?php if (!$isAdminSection && $isAdminUser): ?>
      <!-- Admin Link for non-admin pages -->
      <div class="sidebar-divider"></div>
      <a href="/admin/dashboard"
         class="sidebar-link sidebar-link--admin"
         data-nav="admin"
         data-tooltip="Admin"
         aria-label="Gå till admin">
        <span class="sidebar-icon" aria-hidden="true"><?= hub_icon('settings', 'sidebar-icon-svg') ?></span>
        <span class="sidebar-label">Admin</span>
      </a>
    <?php elseif (!$isAdminSection && $isPromotorOnly): ?>
      <!-- Promotor Admin Link -->
      <div class="sidebar-divider"></div>
      <a href="/admin/promotor.php"
         class="sidebar-link sidebar-link--admin"
         data-nav="promotor-admin"
         data-tooltip="Mina tävlingar"
         aria-label="Hantera mina tävlingar">
        <span class="sidebar-icon" aria-hidden="true"><?= hub_icon('settings', 'sidebar-icon-svg') ?></span>
        <span class="sidebar-label">Admin</span>
      </a>
    <?php endif; ?>
  </nav>
</aside>
<!-- Sidebar CSS is in assets/css/layout.css -->
