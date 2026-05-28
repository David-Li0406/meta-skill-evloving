<?php
/**
 * TheHUB Bottom Navigation
 * Uses SVG icons (Lucide-style)
 */

// Ensure hub-config is loaded (may already be loaded by parent)
if (!defined('HUB_ROOT')) {
    $hubConfig = __DIR__ . '/../hub-config.php';
    if (file_exists($hubConfig)) {
        require_once $hubConfig;
    }
}

require_once __DIR__ . '/icons.php';

$currentPage = $pageInfo['page'] ?? 'dashboard';
$isLoggedIn = function_exists('hub_is_logged_in') ? hub_is_logged_in() : false;
$isPromotorOnly = function_exists('isRole') && isRole('promotor');

// Fallback for hub_is_nav_active if not defined
if (!function_exists('hub_is_nav_active')) {
    function hub_is_nav_active($navId, $currentPage) {
        return $navId === $currentPage;
    }
}

// Icon mapping for nav items
$navIcons = [
    'calendar' => 'calendar',
    'results' => 'flag',
    'series' => 'trophy',
    'news' => 'newspaper',
    'database' => 'search',
    'ranking' => 'trending-up',
    'profile' => 'user',
];

// Fallback nav items if HUB_NAV not defined
$hubNav = defined('HUB_NAV') ? HUB_NAV : [
    ['id' => 'calendar', 'label' => 'Kalender', 'url' => '/calendar', 'aria' => 'Kalender'],
    ['id' => 'results', 'label' => 'Resultat', 'url' => '/results', 'aria' => 'Resultat'],
    ['id' => 'series', 'label' => 'Serier', 'url' => '/series', 'aria' => 'Serier'],
    ['id' => 'database', 'label' => 'Databas', 'url' => '/database', 'aria' => 'Databas'],
    ['id' => 'ranking', 'label' => 'Ranking', 'url' => '/ranking', 'aria' => 'Ranking'],
];

// Admin link is NOT added here - it's accessed via profile menu in header
?>
<nav class="mobile-nav" role="navigation" aria-label="Huvudnavigering">
  <div class="mobile-nav-inner">
    <?php foreach ($hubNav as $item): ?>
      <?php
      $isActive = hub_is_nav_active($item['id'], $currentPage);
      $iconName = $navIcons[$item['id']] ?? 'info';
      ?>
      <a href="<?= htmlspecialchars($item['url']) ?>"
         class="mobile-nav-link<?= $isActive ? ' active' : '' ?>"
         data-nav="<?= htmlspecialchars($item['id']) ?>"
         <?= $isActive ? 'aria-current="page"' : '' ?>
         aria-label="<?= htmlspecialchars($item['aria']) ?>">
        <span class="mobile-nav-icon" aria-hidden="true"><?= hub_icon($iconName) ?></span>
        <span class="mobile-nav-label"><?= htmlspecialchars($item['label']) ?></span>
      </a>
    <?php endforeach; ?>
  </div>
</nav>
