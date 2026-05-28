<?php
/**
 * Admin Tabs Component
 * Återanvändbar flik-navigation för admin-sidor
 *
 * Mobile-first, orientation-aware design:
 * - Portrait mobil: Vertikala knappar (full bredd)
 * - Landscape mobil: Horisontell rad med wrap
 * - Tablet/Desktop: Horisontell rad
 *
 * @param array $tabs Array med flikar: ['id' => '', 'label' => '', 'icon' => '', 'url' => '']
 * @param string $active_tab ID för aktiv flik
 * @param array $options Valfria inställningar:
 *  - 'compact' => true för scrollbar variant (5+ flikar)
 *  - 'class' => extra CSS-klasser
 */
function render_admin_tabs($tabs, $active_tab, $options = []) {
  $base_class = 'admin-tabs';
  $extra_classes = [];

  // Lägg till compact-klass om många flikar
  if (count($tabs) >= 5 || !empty($options['compact'])) {
    $extra_classes[] = 'admin-tabs--compact';
  }

  // Lägg till few-klass om få flikar (för tablet 2-kolumn)
  if (count($tabs) <= 3) {
    $extra_classes[] = 'admin-tabs--few';
  }

  // Lägg till custom klasser
  if (!empty($options['class'])) {
    $extra_classes[] = $options['class'];
  }

  $class_string = $base_class . (count($extra_classes) > 0 ? ' ' . implode(' ', $extra_classes) : '');
  ?>
  <nav class="<?= htmlspecialchars($class_string) ?>" role="tablist" aria-label="Navigeringsflikar">
    <?php foreach ($tabs as $index => $tab):
      $is_active = $tab['id'] === $active_tab;
      $tab_classes = $base_class . '__tab';
      if ($is_active) {
        $tab_classes .= ' ' . $base_class . '__tab--active';
      }
    ?>
      <a href="<?= htmlspecialchars($tab['url']) ?>"
        class="<?= $tab_classes ?>"
        role="tab"
        id="tab-<?= htmlspecialchars($tab['id']) ?>"
        aria-selected="<?= $is_active ? 'true' : 'false' ?>"
        <?= isset($tab['badge']) ? 'data-badge="' . htmlspecialchars($tab['badge']) . '"' : '' ?>>
        <?php if (isset($tab['icon'])): ?>
          <i data-lucide="<?= htmlspecialchars($tab['icon']) ?>" aria-hidden="true"></i>
        <?php endif; ?>
        <span><?= htmlspecialchars($tab['label']) ?></span>
      </a>
    <?php endforeach; ?>
  </nav>
  <?php
}

/**
 * Rendera sidhuvud med titel och actions
 * Mobile-first: Vertikal stack på mobil, horisontell på desktop
 *
 * @param string $title Sidtitel
 * @param array $actions Array med knappar: ['label' => '', 'url' => '', 'icon' => '', 'class' => '']
 */
function render_admin_page_header($title, $actions = []) {
  ?>
  <header class="admin-page-header">
    <h1 class="admin-page-header__title"><?= htmlspecialchars($title) ?></h1>
    <?php if (!empty($actions)): ?>
    <div class="admin-page-header__actions">
      <?php foreach ($actions as $action):
        $btn_class = 'btn ' . ($action['class'] ?? 'btn--primary');
      ?>
        <a href="<?= htmlspecialchars($action['url']) ?>"
          class="<?= htmlspecialchars($btn_class) ?>">
          <?php if (isset($action['icon'])): ?>
            <i data-lucide="<?= htmlspecialchars($action['icon']) ?>" aria-hidden="true"></i>
          <?php endif; ?>
          <span><?= htmlspecialchars($action['label']) ?></span>
        </a>
      <?php endforeach; ?>
    </div>
    <?php endif; ?>
  </header>
  <?php
}
?>
