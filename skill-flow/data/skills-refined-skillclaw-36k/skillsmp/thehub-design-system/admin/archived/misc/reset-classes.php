<?php
/**
 * Reset Classes Script
 * Deletes all existing classes and creates the new standard class set
 *
 * IMPORTANT: Run this only once to set up the initial classes!
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';
$stats = ['deleted' => 0, 'created' => 0, 'errors' => []];

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['confirm_reset'])) {
 checkCsrf();

 try {
 // Start transaction
 $db->query("START TRANSACTION");

 // Delete all existing classes (only if they have no results)
 $existingClasses = $db->getAll("SELECT id, name, display_name FROM classes");

 foreach ($existingClasses as $class) {
  $resultCount = $db->getOne(
  "SELECT COUNT(*) FROM results WHERE class_id = ?",
  [$class['id']]
  );

  if ($resultCount > 0) {
  // Set results' class_id to NULL instead of deleting the class
  $db->query(
  "UPDATE results SET class_id = NULL WHERE class_id = ?",
   [$class['id']]
  );
  error_log("Unlinked {$resultCount} results from class: {$class['display_name']}");
  }

  // Now delete the class
  $db->delete('classes', 'id = ?', [$class['id']]);
  $stats['deleted']++;
 }

 // Create new classes
 $newClasses = [
  ['name' => 'DE', 'display_name' => 'Damer Elit', 'gender' => 'F', 'sort_order' => 10],
  ['name' => 'F15-16', 'display_name' => 'Flickor 15-16', 'gender' => 'F', 'min_age' => 15, 'max_age' => 16, 'sort_order' => 20],
  ['name' => 'DJ', 'display_name' => 'Damer Junior', 'gender' => 'F', 'min_age' => 17, 'max_age' => 18, 'sort_order' => 30],
  ['name' => 'HE', 'display_name' => 'Herrar Elit', 'gender' => 'M', 'sort_order' => 40],
  ['name' => 'H45', 'display_name' => 'Master Herrar 45+', 'gender' => 'M', 'min_age' => 45, 'sort_order' => 50],
  ['name' => 'MK', 'display_name' => 'Motion Kids / Nybörjare', 'sort_order' => 60],
  ['name' => 'MM', 'display_name' => 'Motion Mellan', 'sort_order' => 70],
  ['name' => 'F13-14', 'display_name' => 'Flickor 13-14', 'gender' => 'F', 'min_age' => 13, 'max_age' => 14, 'sort_order' => 80],
  ['name' => 'SML', 'display_name' => 'Sportmotion Lång', 'sort_order' => 90],
  ['name' => 'SMEB', 'display_name' => 'MTB E-Bike Sportmotion', 'sort_order' => 100],
  ['name' => 'P15-16', 'display_name' => 'Pojkar 15-16', 'gender' => 'M', 'min_age' => 15, 'max_age' => 16, 'sort_order' => 110],
  ['name' => 'HJ', 'display_name' => 'Herrar Junior', 'gender' => 'M', 'min_age' => 17, 'max_age' => 18, 'sort_order' => 120],
  ['name' => 'P13-14', 'display_name' => 'Pojkar 13-14', 'gender' => 'M', 'min_age' => 13, 'max_age' => 14, 'sort_order' => 130],
  ['name' => 'D35', 'display_name' => 'Master Damer 35+', 'gender' => 'F', 'min_age' => 35, 'sort_order' => 140],
  ['name' => 'H35', 'display_name' => 'Master Herrar 35+', 'gender' => 'M', 'min_age' => 35, 'max_age' => 44, 'sort_order' => 150],
  ['name' => 'H19', 'display_name' => 'Herrar 19', 'gender' => 'M', 'min_age' => 19, 'max_age' => 19, 'sort_order' => 160],
  ['name' => 'D19', 'display_name' => 'Damer 19', 'gender' => 'F', 'min_age' => 19, 'max_age' => 19, 'sort_order' => 170],
 ];

 foreach ($newClasses as $classData) {
  // Set defaults
  if (!isset($classData['discipline'])) $classData['discipline'] = '';
  if (!isset($classData['gender'])) $classData['gender'] = '';
  if (!isset($classData['min_age'])) $classData['min_age'] = null;
  if (!isset($classData['max_age'])) $classData['max_age'] = null;
  $classData['active'] = 1;

  $db->insert('classes', $classData);
  $stats['created']++;
 }

 // Commit transaction
 $db->query("COMMIT");

 $message ="Klasser återställda! {$stats['deleted']} raderade, {$stats['created']} skapade.";
 $messageType = 'success';

 } catch (Exception $e) {
 $db->query("ROLLBACK");
 $message = 'Fel vid återställning: ' . $e->getMessage();
 $messageType = 'error';
 $stats['errors'][] = $e->getMessage();
 }
}

$pageTitle = 'Återställ Klasser';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <!-- Header -->
 <div class="flex items-center justify-between mb-lg">
  <div>
  <h1 class="text-primary">
   <i data-lucide="refresh-cw"></i>
   Återställ Klasser
  </h1>
  <p class="text-secondary mt-sm">
   Radera alla befintliga klasser och skapa standarduppsättningen
  </p>
  </div>
  <a href="/admin/classes.php" class="btn btn--secondary">
  <i data-lucide="arrow-left"></i>
  Tillbaka
  </a>
 </div>

 <!-- Message -->
 <?php if ($message): ?>
  <div class="alert alert-<?= h($messageType) ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <!-- Stats -->
 <?php if ($stats['deleted'] > 0 || $stats['created'] > 0): ?>
  <div class="card mb-lg">
  <div class="card-header">
   <h2 class="">Statistik</h2>
  </div>
  <div class="card-body">
   <div class="grid grid-cols-2 gap-md">
   <div>
    <div class="text-sm text-secondary">Raderade klasser</div>
    <div class="text-error"><?= $stats['deleted'] ?></div>
   </div>
   <div>
    <div class="text-sm text-secondary">Skapade klasser</div>
    <div class="text-success"><?= $stats['created'] ?></div>
   </div>
   </div>
  </div>
  </div>
 <?php endif; ?>

 <!-- Warning Card -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="text-error">
   <i data-lucide="alert-triangle"></i>
   VARNING - Läs detta först!
  </h2>
  </div>
  <div class="card-body">
  <p class="text-error mb-md">
   <strong>Detta script kommer att:</strong>
  </p>
  <ul class="text-secondary" class="gs-list-ml-lg-lh-1-8">
   <li>Radera ALLA befintliga klasser i databasen</li>
   <li>Koppla bort alla resultat från deras klasser (class_id sätts till NULL)</li>
   <li>Skapa 17 nya standardklasser</li>
  </ul>
  <p class="text-error mt-md">
   <strong>Resultat som redan är importerade kommer INTE att tilldelas till de nya klasserna automatiskt.</strong>
   Du måste re-importera dina resultat eller manuellt tilldela klasser.
  </p>
  </div>
 </div>

 <!-- New Classes Preview -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="">
   <i data-lucide="list"></i>
   Nya klasser som kommer skapas (17 st)
  </h2>
  </div>
  <div class="card-body">
  <div class="table-responsive">
   <table class="table">
   <thead>
    <tr>
    <th>Namn</th>
    <th>Visningsnamn</th>
    <th>Kön</th>
    <th>Ålder</th>
    <th>Sortering</th>
    </tr>
   </thead>
   <tbody>
    <tr><td>DE</td><td>Damer Elit</td><td>Dam</td><td>-</td><td>10</td></tr>
    <tr><td>F15-16</td><td>Flickor 15-16</td><td>Dam</td><td>15-16</td><td>20</td></tr>
    <tr><td>DJ</td><td>Damer Junior</td><td>Dam</td><td>17-18</td><td>30</td></tr>
    <tr><td>HE</td><td>Herrar Elit</td><td>Herr</td><td>-</td><td>40</td></tr>
    <tr><td>H45</td><td>Master Herrar 45+</td><td>Herr</td><td>45+</td><td>50</td></tr>
    <tr><td>MK</td><td>Motion Kids / Nybörjare</td><td>Alla</td><td>-</td><td>60</td></tr>
    <tr><td>MM</td><td>Motion Mellan</td><td>Alla</td><td>-</td><td>70</td></tr>
    <tr><td>F13-14</td><td>Flickor 13-14</td><td>Dam</td><td>13-14</td><td>80</td></tr>
    <tr><td>SML</td><td>Sportmotion Lång</td><td>Alla</td><td>-</td><td>90</td></tr>
    <tr><td>SMEB</td><td>MTB E-Bike Sportmotion</td><td>Alla</td><td>-</td><td>100</td></tr>
    <tr><td>P15-16</td><td>Pojkar 15-16</td><td>Herr</td><td>15-16</td><td>110</td></tr>
    <tr><td>HJ</td><td>Herrar Junior</td><td>Herr</td><td>17-18</td><td>120</td></tr>
    <tr><td>P13-14</td><td>Pojkar 13-14</td><td>Herr</td><td>13-14</td><td>130</td></tr>
    <tr><td>D35</td><td>Master Damer 35+</td><td>Dam</td><td>35+</td><td>140</td></tr>
    <tr><td>H35</td><td>Master Herrar 35+</td><td>Herr</td><td>35-44</td><td>150</td></tr>
    <tr><td>H19</td><td>Herrar 19</td><td>Herr</td><td>19</td><td>160</td></tr>
    <tr><td>D19</td><td>Damer 19</td><td>Dam</td><td>19</td><td>170</td></tr>
   </tbody>
   </table>
  </div>
  </div>
 </div>

 <!-- Confirm Form -->
 <div class="card">
  <div class="card-body">
  <form method="POST" onsubmit="return confirm('Är du ABSOLUT säker på att du vill radera alla klasser och skapa nya? Detta går inte att ångra!');">
   <?= csrf_field() ?>

   <div class="form-group">
   <label class="checkbox-label">
    <input type="checkbox" required>
    <span>Jag förstår att detta kommer radera alla befintliga klasser</span>
   </label>
   </div>

   <div class="form-group">
   <label class="checkbox-label">
    <input type="checkbox" required>
    <span>Jag förstår att befintliga resultat kommer kopplas bort från sina klasser</span>
   </label>
   </div>

   <div class="flex gap-md mt-lg">
   <button type="submit" name="confirm_reset" class="btn btn-danger">
    <i data-lucide="refresh-cw"></i>
    Återställ Klasser
   </button>
   <a href="/admin/classes.php" class="btn btn--secondary">
    <i data-lucide="x"></i>
    Avbryt
   </a>
   </div>
  </form>
  </div>
 </div>
 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
