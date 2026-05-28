<?php
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

// Initialize message variables
$message = '';
$messageType = 'info';

// Load current settings
$settingsFile = __DIR__ . '/../config/public_settings.php';
$currentSettings = require $settingsFile;

// Load sponsor settings from database
$sponsorPublicEnabled = false;
$hideEmptyForAdmin = false;
try {
    $sponsorSetting = $db->getRow("SELECT setting_value FROM sponsor_settings WHERE setting_key = 'public_enabled'");
    $sponsorPublicEnabled = ($sponsorSetting && $sponsorSetting['setting_value'] == '1');

    $hideEmptySetting = $db->getRow("SELECT setting_value FROM sponsor_settings WHERE setting_key = 'hide_empty_for_admin'");
    $hideEmptyForAdmin = ($hideEmptySetting && $hideEmptySetting['setting_value'] == '1');
} catch (Exception $e) {
    // Table might not exist yet
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $action = $_POST['action'] ?? '';

 if ($action === 'save_sponsor_visibility') {
     $enabled = isset($_POST['sponsor_public_enabled']) ? 1 : 0;
     $hideEmpty = isset($_POST['hide_empty_for_admin']) ? 1 : 0;
     try {
         // Save public_enabled setting
         $exists = $db->getRow("SELECT id FROM sponsor_settings WHERE setting_key = 'public_enabled'");
         if ($exists) {
             $db->query("UPDATE sponsor_settings SET setting_value = ? WHERE setting_key = 'public_enabled'", [$enabled]);
         } else {
             $db->query("INSERT INTO sponsor_settings (setting_key, setting_value) VALUES ('public_enabled', ?)", [$enabled]);
         }
         $sponsorPublicEnabled = ($enabled == 1);

         // Save hide_empty_for_admin setting
         $existsHideEmpty = $db->getRow("SELECT id FROM sponsor_settings WHERE setting_key = 'hide_empty_for_admin'");
         if ($existsHideEmpty) {
             $db->query("UPDATE sponsor_settings SET setting_value = ? WHERE setting_key = 'hide_empty_for_admin'", [$hideEmpty]);
         } else {
             $db->query("INSERT INTO sponsor_settings (setting_key, setting_value) VALUES ('hide_empty_for_admin', ?)", [$hideEmpty]);
         }
         $hideEmptyForAdmin = ($hideEmpty == 1);

         $message = 'Sponsorinställningar sparade!';
         $messageType = 'success';
     } catch (Exception $e) {
         $message = 'Kunde inte spara inställning: ' . $e->getMessage();
         $messageType = 'error';
     }
 } elseif ($action === 'save_settings') {
 $public_riders_display = $_POST['public_riders_display'] ?? 'with_results';
 $min_results_to_show = intval($_POST['min_results_to_show'] ?? 1);

 // Validate
 if (!in_array($public_riders_display, ['all', 'with_results'])) {
  $message = 'Ogiltigt värde för visningsläge';
  $messageType = 'error';
 } elseif ($min_results_to_show < 1) {
  $message = 'Minsta antal resultat måste vara minst 1';
  $messageType = 'error';
 } else {
  // Create new settings array
  $newSettings = [
  'public_riders_display' => $public_riders_display,
  'min_results_to_show' => $min_results_to_show,
  ];

  // Generate PHP code for the settings file
  $phpCode ="<?php\n";
  $phpCode .="/**\n";
  $phpCode .=" * Public Display Settings\n";
  $phpCode .=" * Configure what data is visible on the public website\n";
  $phpCode .=" */\n\n";
  $phpCode .="return [\n";
  $phpCode .=" // Show all riders publicly or only those with results\n";
  $phpCode .=" // Options: 'all' or 'with_results'\n";
  $phpCode .=" 'public_riders_display' => '{$newSettings['public_riders_display']}',\n\n";
  $phpCode .=" // Minimum number of results required to show rider (when 'with_results' is selected)\n";
  $phpCode .=" 'min_results_to_show' => {$newSettings['min_results_to_show']},\n";
  $phpCode .="];\n";

  // Write to file
  if (file_put_contents($settingsFile, $phpCode) !== false) {
  $currentSettings = $newSettings;
  $message = 'Inställningar sparade!';
  $messageType = 'success';
  } else {
  $message = 'Kunde inte spara inställningar. Kontrollera filrättigheter.';
  $messageType = 'error';
  }
 }
 }
}

// Get statistics
$total_riders = $db->getRow("SELECT COUNT(*) as count FROM riders WHERE active = 1")['count'] ?? 0;
$riders_with_results = $db->getRow("
 SELECT COUNT(DISTINCT c.id) as count
 FROM riders c
 INNER JOIN results r ON c.id = r.cyclist_id
 WHERE c.active = 1
")['count'] ?? 0;
$riders_without_results = $total_riders - $riders_with_results;

$page_title = 'Publika Inställningar';
$page_group = 'config';
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Messages -->
<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'info') ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Statistics -->
<div class="admin-stats-grid mb-lg">
    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-info-light); color: var(--color-info);">
            <i data-lucide="users"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $total_riders ?></div>
            <div class="admin-stat-label">Totalt aktiva deltagare</div>
        </div>
    </div>
    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-success-light); color: var(--color-success);">
            <i data-lucide="trophy"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $riders_with_results ?></div>
            <div class="admin-stat-label">Med resultat</div>
        </div>
    </div>
    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-bg-tertiary); color: var(--color-text-secondary);">
            <i data-lucide="user-x"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $riders_without_results ?></div>
            <div class="admin-stat-label">Utan resultat</div>
        </div>
    </div>
</div>

 <!-- Settings Form -->
 <div class="card">
  <div class="card-header">
  <h2 class="">
   <i data-lucide="eye"></i>
   Synlighet för Deltagare
  </h2>
  </div>
  <form method="POST" class="card-body">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="save_settings">

  <div class="mb-lg">
   <p class="text-secondary mb-md">
   Välj vilka deltagare som ska visas på den publika deltagarsidan (<code>/riders.php</code>).
   </p>

   <div class="alert alert--info mb-md">
   <i data-lucide="info"></i>
   <strong>Nuvarande inställning:</strong>
   <?php if ($currentSettings['public_riders_display'] === 'all'): ?>
    Visar alla <?= $total_riders ?> aktiva deltagare
   <?php else: ?>
    Visar bara deltagare med resultat (<?= $riders_with_results ?> deltagare)
   <?php endif; ?>
   </div>
  </div>

  <!-- Display Mode -->
  <div class="mb-lg">
   <label class="label mb-sm">
   <i data-lucide="users"></i>
   Visningsläge
   </label>

   <div class="flex flex-col gap-md">
   <label class="gs-radio-card <?= $currentSettings['public_riders_display'] === 'with_results' ? 'active' : '' ?>">
    <input
    type="radio"
    name="public_riders_display"
    value="with_results"
    class="gs-radio"
    <?= $currentSettings['public_riders_display'] === 'with_results' ? 'checked' : '' ?>
    >
    <div class="gs-radio-card-content">
    <div class="gs-radio-card-title">
     <i data-lucide="trophy"></i>
     Endast deltagare med resultat
    </div>
    <div class="gs-radio-card-description">
     Visar bara de <?= $riders_with_results ?> deltagare som har tävlat och har minst ett resultat registrerat.
     <strong>Rekommenderat för offentlig visning.</strong>
    </div>
    </div>
   </label>

   <label class="gs-radio-card <?= $currentSettings['public_riders_display'] === 'all' ? 'active' : '' ?>">
    <input
    type="radio"
    name="public_riders_display"
    value="all"
    class="gs-radio"
    <?= $currentSettings['public_riders_display'] === 'all' ? 'checked' : '' ?>
    >
    <div class="gs-radio-card-content">
    <div class="gs-radio-card-title">
     <i data-lucide="users"></i>
     Alla aktiva deltagare
    </div>
    <div class="gs-radio-card-description">
     Visar alla <?= $total_riders ?> aktiva deltagare, även de utan resultat.
     Inkluderar <?= $riders_without_results ?> deltagare som inte har några registrerade resultat än.
    </div>
    </div>
   </label>
   </div>
  </div>

  <!-- Minimum Results (shown only when 'with_results' is selected) -->
  <div class="mb-lg <?= $currentSettings['public_riders_display'] === 'with_results' ? '' : 'hidden' ?>" id="minResultsSection">
   <label for="min_results_to_show" class="label">
   <i data-lucide="hash"></i>
   Minsta antal resultat
   </label>
   <input
   type="number"
   id="min_results_to_show"
   name="min_results_to_show"
   class="input gs-max-w-200"
   min="1"
   value="<?= $currentSettings['min_results_to_show'] ?>"
   >
   <small class="text-muted">
   Deltagare måste ha minst detta antal registrerade resultat för att visas.
   </small>
  </div>

  <!-- Save Button -->
  <div class="flex gs-justify-end gap-md gs-pt-md border-top">
   <a href="/admin/dashboard.php" class="btn btn--secondary">
   <i data-lucide="x"></i>
   Avbryt
   </a>
   <button type="submit" class="btn btn--primary">
   <i data-lucide="save"></i>
   Spara Inställningar
   </button>
  </div>
  </form>
 </div>

 <!-- Preview -->
 <div class="card mt-lg">
  <div class="card-header">
  <h2 class="">
   <i data-lucide="external-link"></i>
   Förhandsgranskning
  </h2>
  </div>
  <div class="card-body">
  <p class="text-secondary mb-md">
   Se hur den publika deltagarsidan ser ut med nuvarande inställningar.
  </p>
  <a href="/riders.php" target="_blank" class="btn btn--secondary">
   <i data-lucide="eye"></i>
   Öppna Publika Deltagarsidan
  </a>
  </div>
 </div>

 <!-- Sponsor/Ad Visibility Settings -->
 <div class="card mt-lg">
  <div class="card-header">
   <h2 class="">
    <i data-lucide="megaphone"></i>
    Synlighet för Sponsorer &amp; Reklam
   </h2>
  </div>
  <form method="POST" class="card-body">
   <?= csrf_field() ?>
   <input type="hidden" name="action" value="save_sponsor_visibility">

   <div class="mb-lg">
    <p class="text-secondary mb-md">
     Styr om sponsorbanners och reklamplatser ska visas för alla besökare eller endast för administratörer.
     Detta påverkar alla sidor där sponsorplatser har aktiverats (startsidan, resultat, ranking, serier, databas, kalender).
    </p>

    <div class="alert alert--<?= $sponsorPublicEnabled ? 'success' : 'warning' ?> mb-md">
     <i data-lucide="<?= $sponsorPublicEnabled ? 'eye' : 'eye-off' ?>"></i>
     <strong>Nuvarande status:</strong>
     <?php if ($sponsorPublicEnabled): ?>
      Sponsorer och reklam är <strong>synliga för alla besökare</strong>
     <?php else: ?>
      Sponsorer och reklam är <strong>endast synliga för administratörer</strong> (testläge)
     <?php endif; ?>
    </div>
   </div>

   <div class="mb-lg">
    <label class="gs-toggle-label">
     <input
      type="checkbox"
      name="sponsor_public_enabled"
      class="gs-toggle"
      <?= $sponsorPublicEnabled ? 'checked' : '' ?>
     >
     <span class="gs-toggle-slider"></span>
     <span class="gs-toggle-text">Visa sponsorer för alla besökare</span>
    </label>
    <small class="text-muted d-block mt-xs">
     När denna är avstängd visas sponsorplatser endast för inloggade administratörer (för testning och förhandsvisning).
    </small>
   </div>

   <div class="mb-lg">
    <label class="gs-toggle-label">
     <input
      type="checkbox"
      name="hide_empty_for_admin"
      class="gs-toggle"
      <?= $hideEmptyForAdmin ? 'checked' : '' ?>
     >
     <span class="gs-toggle-slider"></span>
     <span class="gs-toggle-text">Dölj tomma sponsorplatser för admin</span>
    </label>
    <small class="text-muted d-block mt-xs">
     När denna är aktiverad visas endast sponsorplatser som har en logotyp uppladdad. Tomma platser döljs även för administratörer.
    </small>
   </div>

   <div class="flex gs-justify-end gap-md gs-pt-md border-top">
    <button type="submit" class="btn btn--primary">
     <i data-lucide="save"></i>
     Spara Synlighet
    </button>
   </div>
  </form>
 </div>

 <!-- Sponsor Management Link -->
 <div class="card mt-lg">
  <div class="card-header">
   <h2 class="">
    <i data-lucide="settings"></i>
    Hantera Sponsorer
   </h2>
  </div>
  <div class="card-body">
   <p class="text-secondary mb-md">
    Lägg till, redigera och hantera sponsorplaceringar och reklambanners.
   </p>
   <a href="/admin/sponsor-placements.php" class="btn btn--secondary">
    <i data-lucide="megaphone"></i>
    Öppna Sponsorhantering
   </a>
  </div>
 </div>
</div>


<script>
// Show/hide minimum results section based on selected display mode
document.addEventListener('DOMContentLoaded', function() {
 const radios = document.querySelectorAll('input[name="public_riders_display"]');
 const minResultsSection = document.getElementById('minResultsSection');

 radios.forEach(radio => {
 radio.addEventListener('change', function() {
  if (this.value === 'with_results') {
  minResultsSection.style.display = 'block';
  } else {
  minResultsSection.style.display = 'none';
  }

  // Update active class on radio cards
  document.querySelectorAll('.gs-radio-card').forEach(card => {
  card.classList.remove('active');
  });
  this.closest('.gs-radio-card').classList.add('active');
 });
 });
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
