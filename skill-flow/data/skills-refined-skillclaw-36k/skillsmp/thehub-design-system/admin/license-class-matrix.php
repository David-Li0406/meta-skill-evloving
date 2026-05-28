<?php
/**
 * License-Class Matrix Admin
 *
 * Visual matrix for managing which license types can register for which classes.
 * Three tabs for different event license classes: National, Sportmotion, Motion
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Available event license classes
$eventLicenseClasses = [
 'national' => ['name' => 'Nationellt', 'icon' => 'trophy', 'color' => 'warning', 'desc' => 'Nationella tävlingar med full rankingpoäng'],
 'sportmotion' => ['name' => 'Sportmotion', 'icon' => 'bike', 'color' => 'info', 'desc' => 'Sportmotion-event med 50% rankingpoäng'],
 'motion' => ['name' => 'Motion', 'icon' => 'heart', 'color' => 'success', 'desc' => 'Motion-event utan rankingpoäng']
];

// Current tab
$currentTab = $_GET['tab'] ?? 'national';
if (!array_key_exists($currentTab, $eventLicenseClasses)) {
 $currentTab = 'national';
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $action = $_POST['action'] ?? '';
 $saveTab = $_POST['event_license_class'] ?? 'national';

 if ($action === 'save_matrix' && array_key_exists($saveTab, $eventLicenseClasses)) {
 try {
  // Clear existing mappings for this event_license_class
  $db->query("DELETE FROM class_license_eligibility WHERE event_license_class = ?", [$saveTab]);

  // Insert new mappings
  $mappings = $_POST['mapping'] ?? [];
  $inserted = 0;

  foreach ($mappings as $classId => $licenseTypes) {
  foreach ($licenseTypes as $licenseCode => $value) {
   if ($value === '1') {
   $db->insert('class_license_eligibility', [
    'event_license_class' => $saveTab,
    'class_id' => (int)$classId,
    'license_type_code' => $licenseCode,
    'is_allowed' => 1
   ]);
   $inserted++;
   }
  }
  }

  $message ="Matris för '{$eventLicenseClasses[$saveTab]['name']}' sparad! $inserted kopplingar skapade.";
  $messageType = 'success';
  $currentTab = $saveTab; // Stay on same tab
 } catch (Exception $e) {
  $message = 'Fel: ' . $e->getMessage();
  $messageType = 'error';
 }
 }
}

// Get all license types from database (exclude Swe ID)
$licenseTypes = [];
try {
 $licenseTypes = $db->getAll("
 SELECT code, name, description, priority
 FROM license_types
 WHERE is_active = 1
   AND code NOT LIKE '%swe%'
   AND name NOT LIKE '%Swe ID%'
 ORDER BY priority DESC
");
} catch (Exception $e) {
 // Fallback to basic types if table doesn't exist
 $licenseTypes = [
 ['code' => 'engangslicens', 'name' => 'Engångslicens', 'description' => 'För enstaka tävlingar', 'priority' => 10],
 ['code' => 'motionslicens', 'name' => 'Motionslicens', 'description' => 'För motion/sportmotion', 'priority' => 20],
 ['code' => 'tavlingslicens', 'name' => 'Tävlingslicens', 'description' => 'Youth, Junior, Elite, Master etc', 'priority' => 100]
 ];
}

// Get all active classes
$classes = $db->getAll("
 SELECT id, name, display_name, gender, discipline
 FROM classes
 WHERE active = 1
 ORDER BY sort_order ASC, name ASC
");

// Get current mappings for the current tab
$currentMappings = [];
try {
 $mappings = $db->getAll(
 "SELECT class_id, license_type_code FROM class_license_eligibility WHERE event_license_class = ? AND is_allowed = 1",
 [$currentTab]
 );
 foreach ($mappings as $m) {
 $currentMappings[$m['class_id']][$m['license_type_code']] = true;
 }
} catch (Exception $e) {
 // Table might not exist yet or column missing - run migration 041
 $message = 'Kör migration 041 först för att uppdatera databasschemat.';
 $messageType = 'warning';
}

$page_title = 'Licens-Klass Matris';
$page_group = 'config';
include __DIR__ . '/components/unified-layout.php';
?>

 <!-- Messages -->
 <?php if ($message): ?>
  <div class="alert alert-<?= $messageType ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <!-- Event License Class Tabs -->
 <div class="admin-tabs">
  <?php foreach ($eventLicenseClasses as $key => $info): ?>
  <a href="?tab=<?= $key ?>" class="admin-tab <?= $currentTab === $key ? 'active' : '' ?>">
   <i data-lucide="<?= $info['icon'] ?>"></i>
   <?= h($info['name']) ?>
  </a>
  <?php endforeach; ?>
 </div>


 <?php if (empty($classes)): ?>
  <div class="card">
  <div class="card-body text-center gs-padding-xl">
   <i data-lucide="alert-triangle" class="gs-icon-48-empty"></i>
   <h3 class="mt-md">Inga klasser</h3>
   <p class="text-secondary">Skapa klasser först under Konfiguration → Klasser.</p>
  </div>
  </div>
 <?php else: ?>

 <style>
  .matrix-grid {
   display: grid;
   gap: 2px;
   background: var(--color-border);
   border-radius: var(--radius-md);
   overflow: hidden;
  }
  .matrix-header-row {
   display: contents;
  }
  .matrix-row {
   display: contents;
  }
  .matrix-cell {
   background: var(--color-bg-card);
   padding: var(--space-sm);
   display: flex;
   align-items: center;
   justify-content: center;
   min-height: 48px;
  }
  .matrix-cell-header {
   background: var(--color-bg-surface);
   font-weight: 600;
   font-size: 0.75rem;
   text-transform: uppercase;
   letter-spacing: 0.5px;
   color: var(--color-text-secondary);
   text-align: center;
   padding: var(--space-sm) var(--space-xs);
  }
  .matrix-cell-class {
   background: var(--color-bg-surface);
   justify-content: flex-start;
   font-weight: 500;
   gap: var(--space-xs);
   padding: var(--space-sm) var(--space-md);
  }
  .matrix-checkbox {
   width: 28px;
   height: 28px;
   cursor: pointer;
   accent-color: var(--color-accent);
   border-radius: var(--radius-sm);
  }
  .matrix-cell:has(.matrix-checkbox:checked) {
   background: rgba(55, 212, 214, 0.15);
  }
  .gender-badge {
   font-size: 0.7rem;
   padding: 2px 6px;
   border-radius: var(--radius-sm);
   font-weight: 600;
  }
  .gender-m { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }
  .gender-f { background: rgba(236, 72, 153, 0.2); color: #ec4899; }
  .gender-mix { background: rgba(156, 163, 175, 0.2); color: var(--color-text-muted); }
 </style>

 <div class="card">
  <div class="card-header" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: var(--space-sm);">
   <h2>
    <i data-lucide="grid-3x3"></i>
    <?= h($eventLicenseClasses[$currentTab]['name']) ?>
   </h2>
   <p class="text-secondary text-sm" style="margin: 0;"><?= h($eventLicenseClasses[$currentTab]['desc']) ?></p>
  </div>
  <div class="card-body">
   <form method="POST" id="matrixForm">
    <?= csrf_field() ?>
    <input type="hidden" name="action" value="save_matrix">
    <input type="hidden" name="event_license_class" value="<?= h($currentTab) ?>">


    <!-- Matrix Grid -->
    <div class="matrix-grid" style="grid-template-columns: minmax(160px, 1fr) repeat(<?= count($licenseTypes) ?>, minmax(70px, 100px));">
     <!-- Header Row -->
     <div class="matrix-header-row">
      <div class="matrix-cell matrix-cell-header" style="justify-content: flex-start;">Klass</div>
      <?php foreach ($licenseTypes as $license): ?>
       <div class="matrix-cell matrix-cell-header"><?= h($license['name']) ?></div>
      <?php endforeach; ?>
     </div>

     <!-- Class Rows -->
     <?php foreach ($classes as $class): ?>
      <div class="matrix-row">
       <div class="matrix-cell matrix-cell-class">
        <?= h($class['display_name'] ?: $class['name']) ?>
        <?php if ($class['gender'] === 'M'): ?>
         <span class="gender-badge gender-m">M</span>
        <?php elseif ($class['gender'] === 'K' || $class['gender'] === 'F'): ?>
         <span class="gender-badge gender-f">K</span>
        <?php else: ?>
         <span class="gender-badge gender-mix">Mix</span>
        <?php endif; ?>
       </div>
       <?php foreach ($licenseTypes as $license): ?>
        <div class="matrix-cell">
         <input type="hidden" name="mapping[<?= $class['id'] ?>][<?= h($license['code']) ?>]" value="0">
         <input type="checkbox"
          class="matrix-checkbox"
          name="mapping[<?= $class['id'] ?>][<?= h($license['code']) ?>]"
          value="1"
          data-license="<?= h($license['code']) ?>"
          <?= isset($currentMappings[$class['id']][$license['code']]) ? 'checked' : '' ?>>
        </div>
       <?php endforeach; ?>
      </div>
     <?php endforeach; ?>
    </div>

    <!-- Buttons -->
    <div style="margin-top: var(--space-lg); padding-top: var(--space-lg); border-top: 1px solid var(--color-border); display: flex; justify-content: space-between; align-items: center;">
     <button type="button" class="btn btn--secondary" onclick="clearAll()">
      <i data-lucide="x"></i>
      Rensa allt
     </button>
     <button type="submit" class="btn btn--primary">
      <i data-lucide="save"></i>
      Spara matris
     </button>
    </div>
   </form>

   <script>
   function clearAll() {
    if (confirm('Vill du verkligen rensa alla markeringar?')) {
     document.querySelectorAll('.matrix-checkbox').forEach(cb => cb.checked = false);
    }
   }
   </script>
  </div>
 </div>

 <?php endif; ?>



<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
