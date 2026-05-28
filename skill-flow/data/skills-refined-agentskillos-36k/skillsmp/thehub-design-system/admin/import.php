<?php
/**
 * Admin Import - V3 Unified Design System
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();
$message = '';
$messageType = 'success';

// Current tab
$tab = $_GET['tab'] ?? 'import';

// Load import history helper functions for history tab
if ($tab === 'history') {
 require_once __DIR__ . '/../includes/import-history.php';
}

// Handle file upload (import tab)
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['import_file'])) {
 checkCsrf();
 $importType = $_POST['import_type'] ?? '';
 $file = $_FILES['import_file'];

 $validation = validateFileUpload($file, ['text/csv', 'text/plain', 'application/csv', 'application/vnd.ms-excel']);

 if (!$validation['valid']) {
 $message = $validation['error'];
 $messageType = 'error';
 } else {
 // Move uploaded file
 $uploadDir = UPLOADS_PATH;
 if (!is_dir($uploadDir)) {
  mkdir($uploadDir, 0755, true);
 }

 $filename = time() . '_' . basename($file['name']);
 $filepath = $uploadDir . '/' . $filename;

 if (move_uploaded_file($file['tmp_name'], $filepath)) {
  // Import file based on type
  if ($importType === 'cyclists') {
  require_once __DIR__ . '/../imports/import_cyclists.php';
  $importer = new CyclistImporter();

  ob_start();
  $success = $importer->import($filepath);
  $output = ob_get_clean();

  $stats = $importer->getStats();

  if ($success) {
   $message ="Import klar! {$stats['success']} av {$stats['total']} rader importerade.";
   $messageType = 'success';
  } else {
   $message ="Import misslyckades. Kontrollera filformatet.";
   $messageType = 'error';
  }
  } elseif ($importType === 'results') {
  require_once __DIR__ . '/../imports/import_results.php';
  $importer = new ResultImporter();

  ob_start();
  $success = $importer->import($filepath);
  $output = ob_get_clean();

  $stats = $importer->getStats();

  if ($success) {
   $message ="Import klar! {$stats['success']} resultat importerade.";
   $messageType = 'success';
  } else {
   $message ="Import misslyckades. Kontrollera filformatet.";
   $messageType = 'error';
  }
  }

  // Clean up uploaded file
  @unlink($filepath);
 } else {
  $message ="Kunde inte ladda upp filen.";
  $messageType = 'error';
 }
 }

 if ($message) {
 set_flash($messageType, $message);
 redirect('/admin/import.php');
 }
}

// Handle rollback/delete actions (history tab)
if ($_SERVER['REQUEST_METHOD'] === 'POST' && $tab === 'history') {
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

// Handle filters for history tab
$type = $_GET['type'] ?? '';

// Get import history for history tab
$imports = [];
if ($tab === 'history') {
 $imports = getImportHistory($db, 100, $type ?: null);
}

// Page config for unified layout
$page_title = 'Import & Data';
$breadcrumbs = [
    ['label' => 'Import']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Messages -->
 <?php if ($message): ?>
  <div class="alert alert--<?= $messageType ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <?php if ($tab === 'import'): ?>
  <!-- Import Options Grid -->
  <div class="admin-import-grid mb-xl">
   <!-- Deltagare -->
   <div class="admin-import-section" style="border-left: 3px solid var(--color-success);">
    <div class="admin-import-section-header">
     <div class="admin-import-section-icon" style="background: rgba(34, 197, 94, 0.1); color: var(--color-success);">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
     </div>
     <div class="admin-import-section-content">
      <h3 class="admin-import-section-title">Deltagare</h3>
      <p class="admin-import-section-description">Importera cyklister med klubb och licens.</p>
     </div>
    </div>
    <div class="admin-import-section-actions">
     <a href="/admin/download-templates.php?template=riders" class="btn-admin btn-admin-secondary btn-admin-sm" title="Ladda ner mall">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      <span>Mall</span>
     </a>
     <a href="/admin/import-riders.php" class="btn-admin btn-admin-success btn-admin-sm" title="Importera">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      <span>Import</span>
     </a>
    </div>
   </div>

   <!-- Resultat -->
   <div class="admin-import-section" style="border-left: 3px solid var(--color-accent);">
    <div class="admin-import-section-header">
     <div class="admin-import-section-icon" style="background: rgba(245, 158, 11, 0.1); color: var(--color-accent);">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
     </div>
     <div class="admin-import-section-content">
      <h3 class="admin-import-section-title">Resultat</h3>
      <p class="admin-import-section-description">Enduro (SS1-SS15) eller DH (Run1/Run2).</p>
     </div>
    </div>
    <div class="admin-import-section-actions">
     <a href="/admin/import-results.php?template=enduro" class="btn-admin btn-admin-secondary btn-admin-sm" title="Ladda ner mall">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      <span>Mall</span>
     </a>
     <a href="/admin/import-results.php" class="btn-admin btn-admin-warning btn-admin-sm" title="Importera">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      <span>Import</span>
     </a>
    </div>
   </div>

   <!-- Bulk Resultat -->
   <div class="admin-import-section" style="border-left: 3px solid var(--color-success);">
    <div class="admin-import-section-header">
     <div class="admin-import-section-icon" style="background: rgba(97, 206, 112, 0.1); color: var(--color-success);">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 16v6"/><path d="M12 21v-6"/><path d="M8 17v4"/><path d="M4 21h16"/><path d="M4 3h16"/><path d="M16 3v6"/><path d="M12 3v6"/><path d="M8 3v6"/></svg>
     </div>
     <div class="admin-import-section-content">
      <h3 class="admin-import-section-title">Bulk-import Resultat</h3>
      <p class="admin-import-section-description">Importera 100+ CSV-filer i ett svep.</p>
     </div>
    </div>
    <div class="admin-import-section-actions">
     <a href="/admin/import-bulk-results.php" class="btn-admin btn-admin-success btn-admin-sm" title="Bulk-import">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      <span>Bulk</span>
     </a>
    </div>
   </div>

   <!-- Dual Slalom Slutresultat -->
   <div class="admin-import-section" style="border-left: 3px solid #9333ea;">
    <div class="admin-import-section-header">
     <div class="admin-import-section-icon" style="background: rgba(147, 51, 234, 0.1); color: #9333ea;">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>
     </div>
     <div class="admin-import-section-content">
      <h3 class="admin-import-section-title">Dual Slalom Resultat</h3>
      <p class="admin-import-section-description">Elimineringsresultat med tävlings- och kvalpoängsklass.</p>
     </div>
    </div>
    <div class="admin-import-section-actions">
     <a href="/admin/import-results.php?tab=dual_slalom" class="btn-admin btn-admin-sm" style="background: linear-gradient(135deg, #9333ea 0%, #6366f1 100%); color: white;" title="Importera">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      <span>Import</span>
     </a>
    </div>
   </div>

   <!-- Events -->
   <div class="admin-import-section" style="border-left: 3px solid var(--color-info);">
    <div class="admin-import-section-header">
     <div class="admin-import-section-icon" style="background: rgba(59, 130, 246, 0.1); color: var(--color-info);">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
     </div>
     <div class="admin-import-section-content">
      <h3 class="admin-import-section-title">Events</h3>
      <p class="admin-import-section-description">Events med datum, plats och arrangör.</p>
     </div>
    </div>
    <div class="admin-import-section-actions">
     <a href="/admin/import-events.php?template=1" class="btn-admin btn-admin-secondary btn-admin-sm" title="Ladda ner mall">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      <span>Mall</span>
     </a>
     <a href="/admin/import-events.php" class="btn-admin btn-admin-info btn-admin-sm" title="Importera">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      <span>Import</span>
     </a>
    </div>
   </div>

   <!-- Poängmallar -->
   <div class="admin-import-section" style="border-left: 3px solid var(--color-accent);">
    <div class="admin-import-section-header">
     <div class="admin-import-section-icon" style="background: rgba(245, 158, 11, 0.1); color: var(--color-accent);">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
     </div>
     <div class="admin-import-section-content">
      <h3 class="admin-import-section-title">Poängmallar</h3>
      <p class="admin-import-section-description">Poängskala för serier och tävlingar.</p>
     </div>
    </div>
    <div class="admin-import-section-actions">
     <a href="/templates/poangmall-standard.csv" class="btn-admin btn-admin-secondary btn-admin-sm" download title="Ladda ner mall">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      <span>Mall</span>
     </a>
     <a href="/admin/point-scales.php" class="btn-admin btn-admin-primary btn-admin-sm" title="Hantera">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
      <span>Hantera</span>
     </a>
    </div>
   </div>

   <!-- Gravity ID -->
   <div class="admin-import-section" style="border-left: 3px solid #764ba2;">
    <div class="admin-import-section-header">
     <div class="admin-import-section-icon" style="background: rgba(118, 75, 162, 0.1); color: #764ba2;">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><polyline points="17 11 19 13 23 9"/></svg>
     </div>
     <div class="admin-import-section-content">
      <h3 class="admin-import-section-title">Gravity ID</h3>
      <p class="admin-import-section-description">Medlemsrabatter vid eventanmälan.</p>
     </div>
    </div>
    <div class="admin-import-section-actions">
     <a href="/admin/import-gravity-id.php?template=1" class="btn-admin btn-admin-secondary btn-admin-sm" title="Ladda ner mall">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      <span>Mall</span>
     </a>
     <a href="/admin/import-gravity-id.php" class="btn-admin btn-admin-sm" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;" title="Importera">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      <span>Import</span>
     </a>
    </div>
   </div>
  </div>

  <!-- Import Tools -->
  <h3 class="mb-md flex items-center gap-sm text-base">
   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 18px; height: 18px;"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
   Verktyg
  </h3>
  <div class="admin-import-grid mb-xl">
   <!-- Berika Ryttardata -->
   <div class="admin-import-section" style="border-left: 3px solid var(--color-success);">
    <div class="admin-import-section-header">
     <div class="admin-import-section-icon" style="background: rgba(34, 197, 94, 0.1); color: var(--color-success);">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
     </div>
     <div class="admin-import-section-content">
      <h3 class="admin-import-section-title">Berika Data</h3>
      <p class="admin-import-section-description">Uppdatera SWE ID-ryttare med saknad data.</p>
     </div>
    </div>
    <div class="admin-import-section-actions">
     <a href="/admin/enrich-riders.php" class="btn-admin btn-admin-success btn-admin-sm" title="Berika data">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      <span>Kör</span>
     </a>
    </div>
   </div>

   <!-- Kontrollera License Numbers -->
   <div class="admin-import-section" style="border-left: 3px solid var(--color-accent);">
    <div class="admin-import-section-header">
     <div class="admin-import-section-icon" style="background: rgba(245, 158, 11, 0.1); color: var(--color-accent);">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>
     </div>
     <div class="admin-import-section-content">
      <h3 class="admin-import-section-title">Licensnummer</h3>
      <p class="admin-import-section-description">Konvertera ogiltiga ID till SWE ID.</p>
     </div>
    </div>
    <div class="admin-import-section-actions">
     <a href="/admin/check-license-numbers.php" class="btn-admin btn-admin-warning btn-admin-sm" title="Kontrollera">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <span>Kolla</span>
     </a>
    </div>
   </div>

   <!-- Hitta Dubbletter -->
   <div class="admin-import-section" style="border-left: 3px solid var(--color-error);">
    <div class="admin-import-section-header">
     <div class="admin-import-section-icon" style="background: rgba(239, 68, 68, 0.1); color: var(--color-error);">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
     </div>
     <div class="admin-import-section-content">
      <h3 class="admin-import-section-title">Dubbletter</h3>
      <p class="admin-import-section-description">Fuzzy name matching för att hitta kopior.</p>
     </div>
    </div>
    <div class="admin-import-section-actions">
     <a href="/admin/find-duplicates.php" class="btn-admin btn-admin-danger btn-admin-sm" title="Hitta dubbletter">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M6 21V9a9 9 0 0 0 9 9"/></svg>
      <span>Hitta</span>
     </a>
    </div>
   </div>
  </div>

  <!-- Format Guide -->
  <div class="admin-card">
   <div class="admin-card-header">
    <h2 class="flex items-center gap-sm">
     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
     Format-guide
    </h2>
   </div>
  <div class="card-body">
   <div class="grid grid-cols-1 md-grid-cols-2 gap-md">
   <details class="gs-details">
    <summary class="text-sm">Deltagare-kolumner</summary>
    <ul class="text-xs mt-sm" style="list-style: disc; padding-left: 1.5rem;">
    <li><strong>first_name, last_name</strong> (required)</li>
    <li><strong>birth_year</strong> eller <strong>personnummer</strong></li>
    <li>uci_id, swe_id, club_name, gender</li>
    <li>license_type, license_category, discipline</li>
    </ul>
   </details>

   <details class="gs-details">
    <summary class="text-sm">Resultat-kolumner</summary>
    <ul class="text-xs mt-sm" style="list-style: disc; padding-left: 1.5rem;">
    <li><strong>Category, FirstName, LastName</strong> (required)</li>
    <li>PlaceByCategory, Bib no, Club, UCI-ID</li>
    <li>NetTime, Status (FIN/DNF/DNS/DQ)</li>
    <li>SS1-SS15 (Enduro) eller Run1/Run2 (DH)</li>
    </ul>
   </details>

   <details class="gs-details">
    <summary class="text-sm">Event-kolumner</summary>
    <ul class="text-xs mt-sm" style="list-style: disc; padding-left: 1.5rem;">
    <li><strong>Namn, Datum</strong> (required)</li>
    <li>Advent ID, Plats, Bana, Disciplin</li>
    <li>Distans, Höjdmeter, Arrangör</li>
    <li>Webbplats, Anmälningsfrist, Kontakt</li>
    </ul>
   </details>

   <details class="gs-details">
    <summary class="text-sm">Poängmall-kolumner</summary>
    <ul class="text-xs mt-sm" style="list-style: disc; padding-left: 1.5rem;">
    <li><strong>Position, Poäng</strong> (standard)</li>
    <li><strong>Position, Kval, Final</strong> (DH)</li>
    <li>Använd semikolon (;) som separator</li>
    </ul>
   </details>
   </div>

   <div class="alert alert--info mt-md">
   <strong>Tips:</strong> Alla importer stöder svenska och engelska kolumnnamn. Spara som CSV (UTF-8) för bästa resultat.
   </div>
  </div>
  </div>

 <?php else: ?>
  <!-- History Tab -->

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
   <input type="hidden" name="tab" value="history">
   <div>
    <label for="type" class="label">
    <i data-lucide="filter"></i>
    Importtyp
    </label>
    <select id="type" name="type" class="input" style="max-width: 200px;">
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
    <a href="?tab=history" class="btn btn--secondary">
    Rensa
    </a>
   <?php endif; ?>
   </form>
  </div>
  </div>

  <!-- Stats -->
  <div class="grid grid-stats grid-gap-md mb-lg">
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
      <span class="text-secondary gs-font-monospace">
      <?= date('Y-m-d H:i', strtotime($import['imported_at'])) ?>
      </span>
      <br>
      <span class="text-xs text-secondary">
      av <?= h($import['imported_by']) ?>
      </span>
     </td>
     <td>
      <span class="badge badge--primary">
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
      'failed' => ['badge' => 'error', 'icon' => 'x-circle', 'text' => 'Misslyckad'],
      'rolled_back' => ['badge' => 'warning', 'icon' => 'rotate-ccw', 'text' => 'Återställd']
      ];
      $statusInfo = $statusMap[$import['status']] ?? ['badge' => 'secondary', 'icon' => 'help-circle', 'text' => $import['status']];
      ?>
      <span class="badge badge--<?= $statusInfo['badge'] ?>">
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

 <?php endif; ?>

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
