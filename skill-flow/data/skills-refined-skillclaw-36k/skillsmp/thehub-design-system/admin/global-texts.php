<?php
/**
 * Global Texts Management - V3 Unified Design System
 * Manage default texts that can be used across events
 * Admin/Super Admin only - promotors do not have access
 */

require_once __DIR__ . '/../config.php';
require_admin();

// Promotors should not access this page
if (isRole('promotor')) {
    set_flash('error', 'Du har inte behörighet till denna sida');
    redirect('/admin/promotor.php');
}

$db = getDB();
$message = '';
$error = '';

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 if (!verify_csrf_token($_POST['csrf_token'] ?? '')) {
 $error = 'Ogiltig CSRF-token';
 } else {
 $action = $_POST['action'] ?? '';

 if ($action === 'update') {
 $id = (int)$_POST['id'];
 $content = trim($_POST['content'] ?? '');

 $db->update('global_texts', [
 'content' => $content
 ], 'id = ?', [$id]);

 $message = 'Text uppdaterad!';
 } elseif ($action === 'add') {
 $fieldKey = trim($_POST['field_key'] ?? '');
 $fieldName = trim($_POST['field_name'] ?? '');
 $fieldCategory = trim($_POST['field_category'] ?? 'general');
 $content = trim($_POST['content'] ?? '');

 if ($fieldKey && $fieldName) {
 $db->insert('global_texts', [
  'field_key' => $fieldKey,
  'field_name' => $fieldName,
  'field_category' => $fieldCategory,
  'content' => $content
 ]);
 $message = 'Ny global text skapad!';
 } else {
 $error = 'Fältnyckel och fältnamn krävs';
 }
 } elseif ($action === 'delete') {
 $id = (int)$_POST['id'];
 $db->query('DELETE FROM global_texts WHERE id = ?', [$id]);
 $message = 'Global text borttagen!';
 }
 }
}

// Get filter
$categoryFilter = $_GET['category'] ?? '';

// Build query
$where = [];
$params = [];

if ($categoryFilter) {
 $where[] = 'field_category = ?';
 $params[] = $categoryFilter;
}

$whereClause = !empty($where) ? 'WHERE ' . implode(' AND ', $where) : '';

// Fetch all global texts
$globalTexts = $db->getAll("
 SELECT * FROM global_texts
 {$whereClause}
 ORDER BY field_category, sort_order, field_name
", $params);

// Get all categories
$categories = $db->getAll("
 SELECT DISTINCT field_category
 FROM global_texts
 ORDER BY field_category
");

// Category labels
$categoryLabels = [
 'rules' => 'Regler & Säkerhet',
 'practical' => 'Praktisk Information',
 'facilities' => 'Faciliteter',
 'logistics' => 'Logistik',
 'contacts' => 'Kontakter',
 'media' => 'Media',
 'general' => 'Allmänt'
];

// Page config for unified layout
$page_title = 'Globala Texter';
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/settings'],
    ['label' => 'Texter']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

 <!-- Actions -->
 <div class="flex justify-between items-center mb-lg flex-wrap gap-md">
 <p class="text-secondary">
 Standardtexter som kan användas i events
 </p>
 <button type="button" class="btn btn--primary" onclick="showAddModal()">
 <i data-lucide="plus"></i>
 Ny Global Text
 </button>
 </div>

 <?php if ($message): ?>
 <div class="alert alert--success mb-lg">
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <?php if ($error): ?>
 <div class="alert alert-danger mb-lg">
 <?= h($error) ?>
 </div>
 <?php endif; ?>

 <!-- Category Filter -->
 <div class="gs-gs-category-tabs">
 <a href="?category=" class="gs-category-tab <?= !$categoryFilter ? 'active' : '' ?>">
 Alla
 </a>
 <?php foreach ($categories as $cat): ?>
 <a href="?category=<?= h($cat['field_category']) ?>"
  class="gs-category-tab <?= $categoryFilter === $cat['field_category'] ? 'active' : '' ?>">
  <?= h($categoryLabels[$cat['field_category']] ?? ucfirst($cat['field_category'])) ?>
 </a>
 <?php endforeach; ?>
 </div>

 <!-- Global Texts List -->
 <?php if (empty($globalTexts)): ?>
 <div class="card">
 <div class="card-body text-center">
  <i data-lucide="file-text" style="width: 48px; height: 48px; opacity: 0.3; margin: 0 auto 1rem;"></i>
  <p class="text-secondary">Inga globala texter hittades</p>
 </div>
 </div>
 <?php else: ?>
 <?php
 $currentCategory = '';
 foreach ($globalTexts as $text):
 if ($text['field_category'] !== $currentCategory):
  $currentCategory = $text['field_category'];
 ?>
 <h2 class="text-primary mb-md mt-lg">
  <i data-lucide="folder"></i>
  <?= h($categoryLabels[$currentCategory] ?? ucfirst($currentCategory)) ?>
 </h2>
 <?php endif; ?>

 <div class="card global-text-card">
 <div class="card-body">
  <form method="POST">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="update">
  <input type="hidden" name="id" value="<?= $text['id'] ?>">

  <div class="global-text-header">
  <div>
  <h3 class="gs-mb-xs"><?= h($text['field_name']) ?></h3>
  <div class="global-text-meta">
   <span class="badge badge-secondary badge-sm">
   <?= h($text['field_key']) ?>
   </span>
  </div>
  </div>
  <div class="flex gap-sm">
  <button type="submit" class="btn btn--primary btn--sm">
   <i data-lucide="save"></i>
   Spara
  </button>
  <button type="button"
   class="btn btn-danger btn--sm"
   onclick="deleteText(<?= $text['id'] ?>, '<?= h($text['field_name']) ?>')">
   <i data-lucide="trash-2"></i>
  </button>
  </div>
  </div>

  <div class="global-text-content">
  <textarea name="content"
   class="input global-text-textarea"
   placeholder="Ange standardtext..."><?= h($text['content']) ?></textarea>
  </div>
  </form>
 </div>
 </div>
 <?php endforeach; ?>
 <?php endif; ?>

<!-- Add Modal -->
<div id="addModal" class="gs-modal" class="hidden">
 <div class="gs-modal-overlay" onclick="closeAddModal()"></div>
 <div class="gs-modal-content" style="max-width: 500px;">
 <div class="gs-modal-header">
 <h2 class="gs-modal-title">
 <i data-lucide="plus"></i>
 Ny Global Text
 </h2>
 <button type="button" class="gs-modal-close" onclick="closeAddModal()">
 <i data-lucide="x"></i>
 </button>
 </div>
 <form method="POST">
 <?= csrf_field() ?>
 <input type="hidden" name="action" value="add">

 <div class="gs-modal-body">
 <div class="mb-md">
  <label class="label">Fältnyckel *</label>
  <input type="text" name="field_key" class="input" required
  placeholder="t.ex. my_custom_field">
  <small class="text-secondary">Unik nyckel (snake_case)</small>
 </div>

 <div class="mb-md">
  <label class="label">Fältnamn *</label>
  <input type="text" name="field_name" class="input" required
  placeholder="t.ex. Min Anpassade Text">
 </div>

 <div class="mb-md">
  <label class="label">Kategori</label>
  <select name="field_category" class="input">
  <option value="general">Allmänt</option>
  <option value="rules">Regler & Säkerhet</option>
  <option value="practical">Praktisk Information</option>
  <option value="facilities">Faciliteter</option>
  <option value="logistics">Logistik</option>
  <option value="contacts">Kontakter</option>
  <option value="media">Media</option>
  </select>
 </div>

 <div class="mb-md">
  <label class="label">Innehåll</label>
  <textarea name="content" class="input" rows="4"
  placeholder="Standardtext..."></textarea>
 </div>
 </div>

 <div class="gs-modal-footer">
 <button type="button" class="btn btn--secondary" onclick="closeAddModal()">
  Avbryt
 </button>
 <button type="submit" class="btn btn--primary">
  <i data-lucide="plus"></i>
  Skapa
 </button>
 </div>
 </form>
 </div>
</div>

<script>
function showAddModal() {
 document.getElementById('addModal').style.display = 'flex';
}

function closeAddModal() {
 document.getElementById('addModal').style.display = 'none';
}

function deleteText(id, name) {
 if (confirm('Är du säker på att du vill ta bort"' + name + '"?')) {
 const form = document.createElement('form');
 form.method = 'POST';
 form.innerHTML = `
 <?= csrf_field() ?>
 <input type="hidden" name="action" value="delete">
 <input type="hidden" name="id" value="${id}">
 `;
 document.body.appendChild(form);
 form.submit();
 }
}

// Close modal on escape
document.addEventListener('keydown', function(e) {
 if (e.key === 'Escape') {
 closeAddModal();
 }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
