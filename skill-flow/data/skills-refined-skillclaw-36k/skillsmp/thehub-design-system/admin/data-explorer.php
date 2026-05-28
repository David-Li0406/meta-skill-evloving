<?php
require_once __DIR__ . '/../config.php';
require_admin();

// Only superadmin can access this page
$current_admin = get_current_admin();
if (!$current_admin || $current_admin['role'] !== 'superadmin') {
 header('HTTP/1.1 403 Forbidden');
 echo '<h1>403 - Åtkomst nekad</h1><p>Endast superadmin har tillgång till denna sida.</p>';
 exit;
}

$db = getDB();

// Get list of all tables
$tables = $db->getAll("SHOW TABLES");
$tableNames = array_map(function($t) {
 return array_values($t)[0];
}, $tables);

// Selected table
$selectedTable = $_GET['table'] ?? null;
$tableData = [];
$columns = [];
$totalRows = 0;
$page = max(1, (int)($_GET['page'] ?? 1));
$perPage = 50;
$search = $_GET['search'] ?? '';

if ($selectedTable && in_array($selectedTable, $tableNames)) {
 // Get column info
 $columns = $db->getAll("DESCRIBE `$selectedTable`");

 // Count total rows
 $countResult = $db->getRow("SELECT COUNT(*) as count FROM `$selectedTable`");
 $totalRows = $countResult['count'];

 // Build query with search
 $offset = ($page - 1) * $perPage;

 if ($search) {
  // Search in all columns
  $searchConditions = [];
  foreach ($columns as $col) {
   $searchConditions[] = "`{$col['Field']}` LIKE ?";
  }
  $whereClause = implode(' OR ', $searchConditions);
  $searchParams = array_fill(0, count($columns), "%$search%");

  $tableData = $db->getAll(
   "SELECT * FROM `$selectedTable` WHERE $whereClause LIMIT $perPage OFFSET $offset",
   $searchParams
  );

  // Update count for search
  $countResult = $db->getRow(
   "SELECT COUNT(*) as count FROM `$selectedTable` WHERE $whereClause",
   $searchParams
  );
  $totalRows = $countResult['count'];
 } else {
  $tableData = $db->getAll("SELECT * FROM `$selectedTable` LIMIT $perPage OFFSET $offset");
 }
}

$totalPages = ceil($totalRows / $perPage);

// Page config for unified layout
$page_title = 'Data Explorer';
$breadcrumbs = [
  ['label' => 'System'],
  ['label' => 'Data Explorer']
];

include __DIR__ . '/components/unified-layout.php';
?>

<div class="admin-card mb-lg">
 <div class="admin-card-header">
  <h2>
   <i data-lucide="database"></i>
   Databastabeller
  </h2>
 </div>
 <div class="admin-card-body">
  <div style="display: flex; flex-wrap: wrap; gap: var(--space-sm);">
   <?php foreach ($tableNames as $table): ?>
    <a href="?table=<?= urlencode($table) ?>"
      class="btn-admin <?= $selectedTable === $table ? 'btn-admin-primary' : 'btn-admin-secondary' ?>"
      style="font-size: var(--text-sm);">
     <?= h($table) ?>
    </a>
   <?php endforeach; ?>
  </div>
 </div>
</div>

<?php if ($selectedTable): ?>
<div class="admin-card">
 <div class="admin-card-header">
  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: var(--space-md);">
   <h2>
    <i data-lucide="table"></i>
    <?= h($selectedTable) ?>
    <span style="font-weight: normal; font-size: var(--text-sm); color: var(--color-text-secondary);">
     (<?= number_format($totalRows) ?> rader)
    </span>
   </h2>

   <form method="GET" style="display: flex; gap: var(--space-sm);">
    <input type="hidden" name="table" value="<?= h($selectedTable) ?>">
    <input type="text"
        name="search"
        value="<?= h($search) ?>"
        class="admin-form-input"
        placeholder="Sök..."
        style="width: 200px;">
    <button type="submit" class="btn-admin btn-admin-secondary">
     <i data-lucide="search"></i>
    </button>
    <?php if ($search): ?>
     <a href="?table=<?= urlencode($selectedTable) ?>" class="btn-admin btn-admin-ghost">
      <i data-lucide="x"></i>
     </a>
    <?php endif; ?>
   </form>
  </div>
 </div>
 <div class="admin-card-body">
  <!-- Column Info -->
  <details class="mb-lg">
   <summary style="cursor: pointer; font-weight: 600; color: var(--color-text-secondary);">
    <i data-lucide="columns"></i>
    Kolumner (<?= count($columns) ?>)
   </summary>
   <div style="margin-top: var(--space-md); display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: var(--space-sm);">
    <?php foreach ($columns as $col): ?>
     <div style="padding: var(--space-sm); background: var(--color-bg-muted); border-radius: var(--radius-sm); font-size: var(--text-sm);">
      <strong><?= h($col['Field']) ?></strong>
      <span class="text-secondary"><?= h($col['Type']) ?></span>
      <?php if ($col['Key'] === 'PRI'): ?>
       <span class="badge badge-primary" style="font-size: 10px;">PK</span>
      <?php endif; ?>
     </div>
    <?php endforeach; ?>
   </div>
  </details>

  <!-- Data Table -->
  <?php if (count($tableData) > 0): ?>
   <div class="table-responsive">
    <table class="table">
     <thead>
      <tr>
       <?php foreach ($columns as $col): ?>
        <th style="white-space: nowrap;"><?= h($col['Field']) ?></th>
       <?php endforeach; ?>
      </tr>
     </thead>
     <tbody>
      <?php foreach ($tableData as $row): ?>
       <tr>
        <?php foreach ($columns as $col): ?>
         <td style="max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
          <?php
          $value = $row[$col['Field']] ?? '';
          if (strlen($value) > 100) {
           echo '<span title="' . h($value) . '">' . h(substr($value, 0, 100)) . '...</span>';
          } else {
           echo h($value);
          }
          ?>
         </td>
        <?php endforeach; ?>
       </tr>
      <?php endforeach; ?>
     </tbody>
    </table>
   </div>

   <!-- Pagination -->
   <?php if ($totalPages > 1): ?>
    <div style="margin-top: var(--space-lg); display: flex; justify-content: center; gap: var(--space-sm);">
     <?php if ($page > 1): ?>
      <a href="?table=<?= urlencode($selectedTable) ?>&page=<?= $page - 1 ?><?= $search ? '&search=' . urlencode($search) : '' ?>"
        class="btn-admin btn-admin-secondary">
       <i data-lucide="chevron-left"></i>
       Föregående
      </a>
     <?php endif; ?>

     <span style="padding: var(--space-sm) var(--space-md); color: var(--color-text-secondary);">
      Sida <?= $page ?> av <?= $totalPages ?>
     </span>

     <?php if ($page < $totalPages): ?>
      <a href="?table=<?= urlencode($selectedTable) ?>&page=<?= $page + 1 ?><?= $search ? '&search=' . urlencode($search) : '' ?>"
        class="btn-admin btn-admin-secondary">
       Nästa
       <i data-lucide="chevron-right"></i>
      </a>
     <?php endif; ?>
    </div>
   <?php endif; ?>

  <?php else: ?>
   <div style="text-align: center; padding: var(--space-2xl); color: var(--color-text-secondary);">
    <i data-lucide="inbox" style="width: 48px; height: 48px; margin-bottom: var(--space-md);"></i>
    <p>Ingen data hittades<?= $search ? ' för sökningen "' . h($search) . '"' : '' ?></p>
   </div>
  <?php endif; ?>
 </div>
</div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
