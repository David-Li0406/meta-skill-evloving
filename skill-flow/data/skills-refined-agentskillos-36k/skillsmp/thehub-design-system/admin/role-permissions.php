<?php
/**
 * Role Permissions Management - V3 Unified Design System
 * Edit what each role can access
 * Only accessible by super_admin
 */
require_once __DIR__ . '/../config.php';
require_admin();

// Only super_admin can access this page
if (!hasRole('super_admin')) {
 http_response_code(403);
 die('Access denied: Only super administrators can manage role permissions.');
}

$db = getDB();

$message = '';
$messageType = 'info';

// Get all permissions
$permissions = $db->getAll("SELECT * FROM permissions ORDER BY category, name");

// Group permissions by category
$permissionsByCategory = [];
foreach ($permissions as $perm) {
 $cat = $perm['category'] ?: 'other';
 if (!isset($permissionsByCategory[$cat])) {
 $permissionsByCategory[$cat] = [];
 }
 $permissionsByCategory[$cat][] = $perm;
}

// Get current role permissions
$rolePermissions = [];
$roles = ['super_admin', 'admin', 'promotor', 'rider'];
foreach ($roles as $role) {
 $perms = $db->getAll("
 SELECT p.id FROM permissions p
 JOIN role_permissions rp ON p.id = rp.permission_id
 WHERE rp.role = ?
", [$role]);
 $rolePermissions[$role] = array_column($perms, 'id');
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $action = $_POST['action'] ?? '';

 if ($action === 'update_permissions') {
 try {
 // Update each role's permissions (except super_admin which always has all)
 foreach (['admin', 'promotor', 'rider'] as $role) {
 $selectedPerms = $_POST['permissions'][$role] ?? [];

 // Delete existing permissions for this role
 $db->delete('role_permissions', 'role = ?', [$role]);

 // Insert new permissions
 foreach ($selectedPerms as $permId) {
  $db->insert('role_permissions', [
  'role' => $role,
  'permission_id' => (int)$permId
  ]);
 }

 // Refresh role permissions
 $perms = $db->getAll("
  SELECT p.id FROM permissions p
  JOIN role_permissions rp ON p.id = rp.permission_id
  WHERE rp.role = ?
 ", [$role]);
 $rolePermissions[$role] = array_column($perms, 'id');
 }

 $message = 'Behörigheter uppdaterade!';
 $messageType = 'success';
 } catch (Exception $e) {
 $message = 'Kunde inte uppdatera behörigheter: ' . $e->getMessage();
 $messageType = 'error';
 }
 }
}

// Category labels
$categoryLabels = [
 'system' => 'System',
 'events' => 'Events',
 'series' => 'Serier',
 'riders' => 'Deltagare',
 'clubs' => 'Klubbar',
 'import' => 'Import',
 'export' => 'Export',
 'other' => 'Övrigt'
];

// Role labels
$roleLabels = [
 'super_admin' => 'Super Admin',
 'admin' => 'Admin',
 'promotor' => 'Promotor',
 'rider' => 'Rider'
];

$roleColors = [
 'super_admin' => 'error',
 'admin' => 'warning',
 'promotor' => 'primary',
 'rider' => 'success'
];

// Page config for unified layout
$page_title = 'Rollbehörigheter';
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/settings'],
    ['label' => 'Roller']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Message -->
 <?php if ($message): ?>
 <div class="alert alert-<?= h($messageType) ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Info -->
 <div class="alert alert--info mb-lg">
 <i data-lucide="info"></i>
 <div>
 <strong>Super Admin</strong> har alltid alla behörigheter och kan inte begränsas.
 Ändra behörigheter för Admin, Promotor och Rider nedan.
 </div>
 </div>

 <form method="POST">
 <?= csrf_field() ?>
 <input type="hidden" name="action" value="update_permissions">

 <?php foreach ($permissionsByCategory as $category => $perms): ?>
 <div class="card mb-lg">
 <div class="card-header">
  <h2 class=""><?= h($categoryLabels[$category] ?? ucfirst($category)) ?></h2>
 </div>
 <div class="card-body gs-p-0">
  <div class="table-container">
  <table class="table">
  <thead>
  <tr>
   <th style="width: 40%;">Behörighet</th>
   <?php foreach ($roles as $role): ?>
   <th class="text-center" style="width: 15%;">
   <span class="badge badge-<?= $roleColors[$role] ?>"><?= $roleLabels[$role] ?></span>
   </th>
   <?php endforeach; ?>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($perms as $perm): ?>
  <tr>
   <td>
   <div class="font-medium"><?= h($perm['name']) ?></div>
   <?php if ($perm['description']): ?>
   <div class="text-xs text-secondary"><?= h($perm['description']) ?></div>
   <?php endif; ?>
   </td>
   <?php foreach ($roles as $role): ?>
   <td class="text-center">
   <?php if ($role === 'super_admin'): ?>
   <input type="checkbox" checked disabled class="checkbox-input">
   <?php else: ?>
   <input
    type="checkbox"
    name="permissions[<?= $role ?>][]"
    value="<?= $perm['id'] ?>"
    <?= in_array($perm['id'], $rolePermissions[$role]) ? 'checked' : '' ?>
    class="checkbox-input"
   >
   <?php endif; ?>
   </td>
   <?php endforeach; ?>
  </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>
 </div>
 </div>
 <?php endforeach; ?>

 <div class="card">
 <div class="card-body">
  <div class="flex justify-between items-center">
  <div class="text-secondary">
  <i data-lucide="info" class="icon-sm"></i>
  Ändringar träder i kraft direkt vid nästa sidladdning för användare
  </div>
  <button type="submit" class="btn btn--primary">
  <i data-lucide="save"></i>
  Spara behörigheter
  </button>
  </div>
 </div>
 </div>
 </form>

 <!-- Quick Actions -->
 <div class="card mt-lg">
 <div class="card-header">
 <h2 class="">Snabbåtgärder</h2>
 </div>
 <div class="card-body">
 <div class="flex gap-md flex-wrap">
  <button type="button" onclick="selectAllForRole('admin')" class="btn btn--secondary btn--sm">
  Alla till Admin
  </button>
  <button type="button" onclick="clearAllForRole('promotor')" class="btn btn--secondary btn--sm">
  Rensa Promotor
  </button>
  <button type="button" onclick="clearAllForRole('rider')" class="btn btn--secondary btn--sm">
  Rensa Rider
  </button>
 </div>
 </div>
 </div>
 </div>

<style>
.checkbox-input {
 width: 18px;
 height: 18px;
 cursor: pointer;
}
.checkbox-input:disabled {
 cursor: not-allowed;
 opacity: 0.7;
}
</style>

<script>
function selectAllForRole(role) {
 document.querySelectorAll(`input[name="permissions[${role}][]"]`).forEach(cb => {
 cb.checked = true;
 });
}

function clearAllForRole(role) {
 document.querySelectorAll(`input[name="permissions[${role}][]"]`).forEach(cb => {
 cb.checked = false;
 });
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
