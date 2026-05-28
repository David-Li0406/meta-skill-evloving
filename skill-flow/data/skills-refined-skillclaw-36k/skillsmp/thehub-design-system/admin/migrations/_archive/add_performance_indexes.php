<?php
/**
 * Performance Indexes Migration
 * Adds database indexes for better query performance
 *
 * Run this migration once to add all performance-critical indexes
 */

// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

// Use global $pdo from config.php
global $pdo;

// Check database connection
if (!$pdo) {
    $page_title = 'Databasfel';
    $breadcrumbs = [
        ['label' => 'Verktyg', 'url' => '/admin/tools'],
        ['label' => 'Prestandaindex']
    ];
    include __DIR__ . '/../components/unified-layout.php';
    echo '<div class="alert alert-danger">Kunde inte ansluta till databasen. Kontrollera databasinställningarna.</div>';
    include __DIR__ . '/../components/unified-layout-footer.php';
    exit;
}

$results = [];

// List of indexes to add
$indexes = [
    // Results table - most queried
    [
        'table' => 'results',
        'name' => 'idx_results_event_cyclist',
        'columns' => 'event_id, cyclist_id',
        'description' => 'Faster lookups for results by event and rider'
    ],
    [
        'table' => 'results',
        'name' => 'idx_results_class',
        'columns' => 'class_id',
        'description' => 'Faster class-based filtering'
    ],
    [
        'table' => 'results',
        'name' => 'idx_results_event_class',
        'columns' => 'event_id, class_id',
        'description' => 'Faster event results by class'
    ],

    // Series tables
    [
        'table' => 'series_events',
        'name' => 'idx_series_events_composite',
        'columns' => 'series_id, event_id',
        'description' => 'Faster series event lookups'
    ],
    [
        'table' => 'series_results',
        'name' => 'idx_series_results_composite',
        'columns' => 'series_id, event_id, cyclist_id, class_id',
        'description' => 'Faster series results lookups (N+1 fix)'
    ],
    [
        'table' => 'series_results',
        'name' => 'idx_series_results_cyclist',
        'columns' => 'cyclist_id',
        'description' => 'Faster rider series history'
    ],

    // Riders table
    [
        'table' => 'riders',
        'name' => 'idx_riders_license',
        'columns' => 'license_number',
        'description' => 'Faster license lookups'
    ],
    [
        'table' => 'riders',
        'name' => 'idx_riders_club',
        'columns' => 'club_id',
        'description' => 'Faster club member lists'
    ],
    [
        'table' => 'riders',
        'name' => 'idx_riders_names',
        'columns' => 'lastname, firstname',
        'description' => 'Faster name searches'
    ],

    // Events table
    [
        'table' => 'events',
        'name' => 'idx_events_date',
        'columns' => 'date',
        'description' => 'Faster date-based event queries'
    ],
    [
        'table' => 'events',
        'name' => 'idx_events_series',
        'columns' => 'series_id',
        'description' => 'Faster series event lists'
    ],

    // Classes table
    [
        'table' => 'classes',
        'name' => 'idx_classes_active_sort',
        'columns' => 'active, sort_order',
        'description' => 'Faster active class lists'
    ],

    // Point scale values
    [
        'table' => 'point_scale_values',
        'name' => 'idx_psv_scale_position',
        'columns' => 'scale_id, position',
        'description' => 'Faster point lookups'
    ]
];

// Helper function to check if index exists
function indexExists($pdo, $table, $indexName) {
    try {
        $stmt = $pdo->prepare("SHOW INDEX FROM `$table` WHERE Key_name = ?");
        $stmt->execute([$indexName]);
        return $stmt->fetch() !== false;
    } catch (PDOException $e) {
        return false;
    }
}

// Helper function to check if table exists
function tableExists($pdo, $table) {
    try {
        $stmt = $pdo->prepare("SHOW TABLES LIKE ?");
        $stmt->execute([$table]);
        return $stmt->fetch() !== false;
    } catch (PDOException $e) {
        return false;
    }
}

// Process each index
foreach ($indexes as $index) {
    $table = $index['table'];
    $name = $index['name'];
    $columns = $index['columns'];
    $desc = $index['description'];

    // Check if table exists
    if (!tableExists($pdo, $table)) {
        $results[] = [
            'status' => 'skipped',
            'index' => $name,
            'table' => $table,
            'message' => "Table '$table' does not exist"
        ];
        continue;
    }

    // Check if index already exists
    if (indexExists($pdo, $table, $name)) {
        $results[] = [
            'status' => 'exists',
            'index' => $name,
            'table' => $table,
            'message' => "Index already exists"
        ];
        continue;
    }

    // Create the index
    try {
        $sql = "ALTER TABLE `$table` ADD INDEX `$name` ($columns)";
        $pdo->exec($sql);
        $results[] = [
            'status' => 'created',
            'index' => $name,
            'table' => $table,
            'message' => $desc
        ];
    } catch (PDOException $e) {
        $results[] = [
            'status' => 'error',
            'index' => $name,
            'table' => $table,
            'message' => $e->getMessage()
        ];
    }
}

// Page output
$page_title = 'Lägg till prestandaindex';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Prestandaindex']
];

include __DIR__ . '/../components/unified-layout.php';
?>

<div class="card">
    <div class="card-header">
        <h2>
            <i data-lucide="database"></i>
            Databasindex för prestanda
        </h2>
    </div>
    <div class="card-body">
        <p style="margin-bottom: var(--space-lg); color: var(--color-text-secondary);">
            Denna migrering lägger till optimeringsindex för att förbättra databasprestanda.
            Index snabbar upp sökningar och JOINs avsevärt.
        </p>

        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Tabell</th>
                        <th>Index</th>
                        <th>Beskrivning</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($results as $result): ?>
                    <tr>
                        <td>
                            <?php if ($result['status'] === 'created'): ?>
                                <span class="badge badge-success">Skapad</span>
                            <?php elseif ($result['status'] === 'exists'): ?>
                                <span class="badge badge-secondary">Finns redan</span>
                            <?php elseif ($result['status'] === 'skipped'): ?>
                                <span class="badge badge-warning">Hoppades över</span>
                            <?php else: ?>
                                <span class="badge badge-danger">Fel</span>
                            <?php endif; ?>
                        </td>
                        <td><code><?= htmlspecialchars($result['table']) ?></code></td>
                        <td><code><?= htmlspecialchars($result['index']) ?></code></td>
                        <td><?= htmlspecialchars($result['message']) ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>

        <?php
        $created = count(array_filter($results, fn($r) => $r['status'] === 'created'));
        $exists = count(array_filter($results, fn($r) => $r['status'] === 'exists'));
        $errors = count(array_filter($results, fn($r) => $r['status'] === 'error'));
        ?>

        <div style="margin-top: var(--space-lg); padding: var(--space-md); background: var(--color-bg-muted); border-radius: var(--radius-md);">
            <strong>Sammanfattning:</strong>
            <?= $created ?> skapade,
            <?= $exists ?> fanns redan,
            <?= $errors ?> fel
        </div>
    </div>
</div>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
