<?php
/**
 * Admin Layout med flikar
 * Inkludera detta på ALLA admin-sidor för fliknavigation
 *
 * Användning:
 *  require_once __DIR__ . '/../includes/admin-layout.php';
 *  // Efter <main>:
 *  render_admin_header('Sidtitel', $actions);
 *  // Före </main>:
 *  render_admin_footer();
 */

require_once __DIR__ . '/config/admin-tabs-config.php';
require_once __DIR__ . '/components/admin-tabs.php';

// Hämta nuvarande sida och grupp
$current_page = basename($_SERVER['PHP_SELF']);
$active_group = get_group_for_page($current_page);
$active_tab = $active_group ? get_active_tab($active_group, $current_page) : null;

/**
 * Rendera admin header med flikar
 *
 * @param string|null $title Sidtitel (om null, använder gruppens titel)
 * @param array $actions Knappar att visa i headern
 */
function render_admin_header($title = null, $actions = []) {
  // Note: Page title and tabs are now handled by unified-layout.php / admin-submenu.php
  // This function is kept for backward compatibility but only renders actions if provided
  if (!empty($actions)): ?>
  <div class="admin-page-header__actions mb-lg">
    <?php foreach ($actions as $action): ?>
      <a href="<?= htmlspecialchars($action['url']) ?>"
        class="btn <?= $action['class'] ?? 'btn--primary' ?>">
        <?php if (isset($action['icon'])): ?>
          <i data-lucide="<?= htmlspecialchars($action['icon']) ?>"></i>
        <?php endif; ?>
        <?= htmlspecialchars($action['label']) ?>
      </a>
    <?php endforeach; ?>
  </div>
  <?php endif;
}

/**
 * Stäng admin content
 * Note: Kept for backward compatibility, does nothing now
 */
function render_admin_footer() {
  // No-op - content wrapper is now handled by unified-layout.php
}

/**
 * Hämta aktiv grupp (för extern användning)
 *
 * @return string|null
 */
function get_current_admin_group() {
  global $active_group;
  return $active_group;
}

/**
 * Hämta aktiv flik (för extern användning)
 *
 * @return string|null
 */
function get_current_admin_tab() {
  global $active_tab;
  return $active_tab;
}
?>
