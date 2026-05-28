<?php
/**
 * Test DB - Check database connection and tables
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Page config
$page_title = 'Testa DB';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'Testa DB']
];

include __DIR__ . '/components/unified-layout.php';
?>

<div class="card">
    <div class="card-header">
        <h3>Series table columns</h3>
    </div>
    <div class="card-body">
        <pre><?php
        $cols = $db->query("DESCRIBE series")->fetchAll(PDO::FETCH_ASSOC);
        foreach ($cols as $col) {
            echo htmlspecialchars($col['Field'] . " - " . $col['Type']) . "\n";
        }
        ?></pre>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
