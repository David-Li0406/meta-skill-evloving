<?php
/**
 * Debug & System Tools
 * Administrative tools for system maintenance and debugging
 */

require_once __DIR__ . '/../config.php';
require_admin();
require_once __DIR__ . '/../includes/admin-layout.php';

$db = getDB();
$current_admin = get_current_admin();

// Admin tools organized by workflow
$debugTools = [
 'import' => [
 'title' => '1. Import & License',
 'icon' => 'upload',
 'items' => [
 ['name' => 'Berika CSV med License', 'url' => '/admin/enrich-uci-id.php', 'desc' => 'Fyll i saknade license numbers innan import'],
 ['name' => 'Sök License Number', 'url' => '/admin/search-uci-id.php', 'desc' => 'Slå upp enskilda license numbers'],
 ]
 ],
 'duplicates' => [
 'title' => '2. Dublettrensning',
 'icon' => 'git-merge',
 'items' => [
 ['name' => 'Auto-slå ihop UCI/SWE', 'url' => '/admin/auto-merge-uci-swe.php', 'desc' => 'Automatisk sammanslagning av UCI-ID och SWE-ID'],
 ['name' => 'Auto-slå ihop klubbar', 'url' => '/admin/auto-merge-clubs.php', 'desc' => 'Automatisk sammanslagning av klubbdubbletter'],
 ['name' => 'Manuell dublettrensning', 'url' => '/admin/cleanup-duplicates.php', 'desc' => 'Hantera ryttardubbletter manuellt + normalisera namn'],
 ['name' => 'Manuell klubbrensning', 'url' => '/admin/cleanup-clubs.php', 'desc' => 'Hantera klubbdubbletter manuellt'],
 ]
 ],
 'points' => [
 'title' => '3. Poäng & Resultat',
 'icon' => 'award',
 'items' => [
 ['name' => 'Poängmallar', 'url' => '/admin/point-scales.php', 'desc' => 'Skapa och hantera poängmallar'],
 ['name' => 'Omräkna Resultat', 'url' => '/admin/recalculate-results.php', 'desc' => 'Tilldela poängmall och omräkna poäng'],
 ['name' => 'Rensa Eventresultat', 'url' => '/admin/clear-event-results.php', 'desc' => 'Ta bort resultat för specifikt event'],
 ['name' => 'Flytta Klassresultat', 'url' => '/admin/move-class-results.php', 'desc' => 'Flytta resultat mellan klasser'],
 ['name' => 'Omtilldela Klasser', 'url' => '/admin/reassign-classes.php', 'desc' => 'Korrigera klassplaceringar baserat på kön/ålder'],
 ]
 ],
 'database' => [
 'title' => '4. Databas',
 'icon' => 'database',
 'items' => [
 ['name' => 'Kör Migrationer', 'url' => '/admin/migrate.php', 'desc' => 'Kör databasmigrationer'],
 ]
 ],
 'system' => [
 'title' => '5. System',
 'icon' => 'settings',
 'items' => [
 ['name' => 'Kontrollera filer', 'url' => '/admin/check-files.php', 'desc' => 'Verifiera att systemfiler finns'],
 ]
 ]
];

$pageTitle = 'Debug & Verktyg';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <?php render_admin_header('Debug & Verktyg', 'settings'); ?>

 <div class="alert alert--info mb-lg">
 <i data-lucide="info"></i>
 Debug- och testverktyg för systemadministration. Använd med försiktighet.
 </div>

 <?php foreach ($debugTools as $category): ?>
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="<?= $category['icon'] ?>"></i>
  <?= h($category['title']) ?>
 </h2>
 </div>
 <div class="card-body">
 <?php foreach ($category['items'] as $tool): ?>
 <div class="gs-debug-tool-item flex items-center justify-between">
  <div>
  <strong><?= h($tool['name']) ?></strong>
  <div class="text-sm text-secondary"><?= h($tool['desc']) ?></div>
  </div>
  <a href="<?= h($tool['url']) ?>" class="btn btn--sm btn--secondary" target="_blank">
  <i data-lucide="external-link"></i>
  Öppna
  </a>
 </div>
 <?php endforeach; ?>
 </div>
 </div>
 <?php endforeach; ?>

 <?php render_admin_footer(); ?>
 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
