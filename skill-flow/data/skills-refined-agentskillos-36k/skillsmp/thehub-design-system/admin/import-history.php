<?php
/**
 * Import History - V3 Unified Design System
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

// Load import history helper functions
require_once __DIR__ . '/../includes/import-history.php';


// Initialize message variables
$message = '';
$messageType = 'info';

// Handle rollback request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $action = $_POST['action'] ?? '';

 if ($action === 'rollback') {
 $importId = intval($_POST['import_id']);
 $result = rollbackImport($db, $importId, $current_admin['username'] ?? 'admin');

 $message = $result['message'];
 $messageType = $result['success'] ? 'success' : 'error';
 } elseif ($action === 'delete') {
 $importId = intval($_POST['import_id']);
 $result = deleteImportHistory($db, $importId);

 $message = $result['message'];
 $messageType = $result['success'] ? 'success' : 'error';
 }
}

// Handle filters
$type = $_GET['type'] ?? '';

// Get import history
$imports = getImportHistory($db, 100, $type ?: null);

// Page config for unified layout
$page_title = 'Import Historik';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import'],
    ['label' => 'Historik']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

  <!-- Messages -->
  <?php if ($message): ?>
  <div class="alert alert-<?= $messageType ?> mb-lg">
   <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
   <?= h($message) ?>
  </div>
  <?php endif; ?>

  <!-- Info Alert -->
  <div class="alert alert--info mb-lg">
  <i data-lucide="info"></i>
  <div>
   <strong>Import History & Rollback</strong><br>
   Här kan du se alla imports som gjorts i systemet och vid behov återställa (rollback) en import.
   Rollback raderar alla poster som skapades och återställer uppdaterade poster till sina tidigare värden.
  </div>
  </div>

  <!-- Filters -->
  <div class="card mb-lg">
  <div class="card-body">
   <form method="GET" class="flex gap-md gs-items-end">
   <div>
    <label for="type" class="label">
    <i data-lucide="filter"></i>
    Importtyp
    </label>
    <select id="type" name="type" class="input" class="gs-max-w-200">
    <option value="">Alla</option>
    <option value="uci" <?= $type === 'uci' ? 'selected' : '' ?>>UCI Import</option>
    <option value="riders" <?= $type === 'riders' ? 'selected' : '' ?>>Riders</option>
    <option value="results" <?= $type === 'results' ? 'selected' : '' ?>>Results</option>
    <option value="events" <?= $type === 'events' ? 'selected' : '' ?>>Events</option>
    <option value="clubs" <?= $type === 'clubs' ? 'selected' : '' ?>>Clubs</option>
    </select>
   </div>
   <button type="submit" class="btn btn--primary">
    <i data-lucide="filter"></i>
    Filtrera
   </button>
   <?php if ($type): ?>
    <a href="/admin/import-history.php" class="btn btn--secondary">
    Rensa
    </a>
   <?php endif; ?>
   </form>
  </div>
  </div>

  <!-- Stats -->
  <div class="grid grid-cols-2 gs-md-grid-cols-4 gap-lg mb-lg">
  <div class="stat-card">
   <i data-lucide="database" class="icon-lg text-primary mb-md"></i>
   <div class="stat-number"><?= count($imports) ?></div>
   <div class="stat-label">Totalt imports</div>
  </div>
  <div class="stat-card">
   <i data-lucide="check-circle" class="icon-lg text-success mb-md"></i>
   <div class="stat-number">
   <?= count(array_filter($imports, fn($i) => $i['status'] === 'completed')) ?>
   </div>
   <div class="stat-label">Lyckade</div>
  </div>
  <div class="stat-card">
   <i data-lucide="rotate-ccw" class="icon-lg text-warning mb-md"></i>
   <div class="stat-number">
   <?= count(array_filter($imports, fn($i) => $i['status'] === 'rolled_back')) ?>
   </div>
   <div class="stat-label">Återställda</div>
  </div>
  <div class="stat-card">
   <i data-lucide="file-text" class="icon-lg text-accent mb-md"></i>
   <div class="stat-number">
   <?= array_sum(array_column($imports, 'total_records')) ?>
   </div>
   <div class="stat-label">Totalt poster</div>
  </div>
  </div>

  <!-- Import History Table -->
  <?php if (empty($imports)): ?>
  <div class="card">
   <div class="card-body text-center py-xl">
   <i data-lucide="database" class="gs-icon-64-secondary"></i>
   <p class="text-secondary">Ingen importhistorik ännu</p>
   </div>
  </div>
  <?php else: ?>
  <div class="card">
   <div class="table-responsive">
   <table class="table">
    <thead>
    <tr>
     <th>
     <i data-lucide="calendar"></i>
     Datum & Tid
     </th>
     <th>
     <i data-lucide="tag"></i>
     Typ
     </th>
     <th>
     <i data-lucide="file"></i>
     Fil
     </th>
     <th class="text-center">
     <i data-lucide="hash"></i>
     Poster
     </th>
     <th class="text-center">
     <i data-lucide="check"></i>
     Lyckade
     </th>
     <th class="text-center">
     <i data-lucide="edit"></i>
     Uppdaterade
     </th>
     <th class="text-center">
     <i data-lucide="x"></i>
     Misslyckade
     </th>
     <th>
     <i data-lucide="activity"></i>
     Status
     </th>
     <th class="table-col-w150-right">Åtgärder</th>
    </tr>
    </thead>
    <tbody>
    <?php foreach ($imports as $import): ?>
     <tr>
     <td>
      <span class="text-secondary" class="gs-font-monospace">
      <?= date('Y-m-d H:i', strtotime($import['imported_at'])) ?>
      </span>
      <br>
      <span class="text-xs text-secondary">
      av <?= h($import['imported_by']) ?>
      </span>
     </td>
     <td>
      <span class="badge badge-primary">
      <i data-lucide="<?= getImportIcon($import['import_type']) ?>"></i>
      <?= h(ucfirst($import['import_type'])) ?>
      </span>
     </td>
     <td>
      <strong><?= h($import['filename']) ?></strong>
      <?php if ($import['file_size']): ?>
      <br>
      <span class="text-xs text-secondary">
       <?= formatFileSize($import['file_size']) ?>
      </span>
      <?php endif; ?>
     </td>
     <td class="text-center">
      <strong><?= $import['total_records'] ?></strong>
     </td>
     <td class="text-center">
      <span class="text-success">
      <strong><?= $import['success_count'] ?></strong>
      </span>
     </td>
     <td class="text-center">
      <span class="text-primary">
      <?= $import['updated_count'] ?>
      </span>
     </td>
     <td class="text-center">
      <?php if ($import['failed_count'] > 0): ?>
      <span class="text-error">
       <strong><?= $import['failed_count'] ?></strong>
      </span>
      <?php else: ?>
      <span class="text-secondary">0</span>
      <?php endif; ?>
     </td>
     <td>
      <?php
      $statusMap = [
      'completed' => ['badge' => 'success', 'icon' => 'check-circle', 'text' => 'Lyckad'],
      'failed' => ['badge' => 'danger', 'icon' => 'x-circle', 'text' => 'Misslyckad'],
      'rolled_back' => ['badge' => 'warning', 'icon' => 'rotate-ccw', 'text' => 'Återställd']
      ];
      $statusInfo = $statusMap[$import['status']] ?? ['badge' => 'secondary', 'icon' => 'help-circle', 'text' => $import['status']];
      ?>
      <span class="badge badge-<?= $statusInfo['badge'] ?>">
      <i data-lucide="<?= $statusInfo['icon'] ?>"></i>
      <?= $statusInfo['text'] ?>
      </span>
      <?php if ($import['status'] === 'rolled_back'): ?>
      <br>
      <span class="text-xs text-secondary">
       <?= date('Y-m-d H:i', strtotime($import['rolled_back_at'])) ?>
      </span>
      <?php endif; ?>
     </td>
     <td class="text-right">
      <div class="flex gap-sm gs-justify-end">
      <?php if ($import['status'] === 'completed'): ?>
       <button
       type="button"
       class="btn btn--sm btn--secondary btn-warning"
       onclick="rollbackImport(<?= $import['id'] ?>, '<?= addslashes(h($import['filename'])) ?>', <?= $import['success_count'] + $import['updated_count'] ?>)"
       title="Återställ import"
       >
       <i data-lucide="rotate-ccw"></i>
       Rollback
       </button>
      <?php endif; ?>
      <?php if ($import['error_summary']): ?>
       <button
       type="button"
       class="btn btn--sm btn--secondary"
       onclick="showErrors(<?= $import['id'] ?>, <?= htmlspecialchars(json_encode($import['error_summary']), ENT_QUOTES) ?>)"
       title="Visa fel"
       >
       <i data-lucide="alert-circle"></i>
       </button>
      <?php endif; ?>
      <button
       type="button"
       class="btn btn--sm btn--secondary btn-danger"
       onclick="deleteImport(<?= $import['id'] ?>, '<?= addslashes(h($import['filename'])) ?>')"
       title="Radera från historik"
      >
       <i data-lucide="trash-2"></i>
      </button>
      </div>
     </td>
     </tr>
    <?php endforeach; ?>
    </tbody>
   </table>
   </div>
  </div>
  <?php endif; ?>
 </div>

 <script>
  // Rollback import with confirmation
  function rollbackImport(id, filename, affectedRecords) {
  if (!confirm(`VARNING! Vill du verkligen återställa importen"${filename}"?\n\nDetta kommer att:\n- Radera ${affectedRecords} skapade poster\n- Återställa uppdaterade poster till tidigare värden\n\nDenna åtgärd kan INTE ångras!`)) {
   return;
  }

  // Create form and submit
  const form = document.createElement('form');
  form.method = 'POST';
  form.innerHTML = `
   <?= csrf_field() ?>
   <input type="hidden" name="action" value="rollback">
   <input type="hidden" name="import_id" value="${id}">
  `;
  document.body.appendChild(form);
  form.submit();
  }

  // Show error details
  function showErrors(id, errorSummary) {
  alert('Fel från import:\n\n' + errorSummary);
  }

  // Delete import from history
  function deleteImport(id, filename) {
  if (!confirm(`Vill du radera"${filename}" från importhistoriken?\n\nOBS: Detta raderar bara historikposten, inte de importerade posterna.`)) {
   return;
  }

  // Create form and submit
  const form = document.createElement('form');
  form.method = 'POST';
  form.innerHTML = `
   <?= csrf_field() ?>
   <input type="hidden" name="action" value="delete">
   <input type="hidden" name="import_id" value="${id}">
  `;
  document.body.appendChild(form);
  form.submit();
  }
 </script>
 </div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>

<?php
// Helper function for import type icons
function getImportIcon($type) {
 $icons = [
 'uci' => 'file-badge',
 'riders' => 'users',
 'results' => 'trophy',
 'events' => 'calendar',
 'clubs' => 'building',
 'other' => 'file'
 ];
 return $icons[$type] ?? 'file';
}

// Helper function for file size formatting
function formatFileSize($bytes) {
 if ($bytes >= 1073741824) {
 return number_format($bytes / 1073741824, 2) . ' GB';
 } elseif ($bytes >= 1048576) {
 return number_format($bytes / 1048576, 2) . ' MB';
 } elseif ($bytes >= 1024) {
 return number_format($bytes / 1024, 2) . ' KB';
 } else {
 return $bytes . ' bytes';
 }
}
?>
