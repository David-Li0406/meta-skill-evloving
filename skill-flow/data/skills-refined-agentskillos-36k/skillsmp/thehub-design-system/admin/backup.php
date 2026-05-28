<?php
/**
 * Database Backup Tool - Superadmin Only
 * Creates and downloads SQL backup of the database
 */

require_once __DIR__ . '/../config.php';
require_admin();

// Only superadmin can access this
if (!hasRole('super_admin')) {
    header('Location: /admin?error=access_denied');
    exit;
}

$db = getDB();

// Handle download request
if (isset($_GET['download'])) {
    $tables = $db->getAll("SHOW TABLES");
    $tableKey = 'Tables_in_' . DB_NAME;

    // Set headers for download
    $filename = 'thehub_backup_' . date('Y-m-d_His') . '.sql';
    header('Content-Type: application/sql');
    header('Content-Disposition: attachment; filename="' . $filename . '"');
    header('Cache-Control: no-cache, no-store, must-revalidate');

    // Output SQL header
    echo "-- TheHUB Database Backup\n";
    echo "-- Generated: " . date('Y-m-d H:i:s') . "\n";
    echo "-- Database: " . DB_NAME . "\n\n";
    echo "SET FOREIGN_KEY_CHECKS=0;\n";
    echo "SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO';\n\n";

    foreach ($tables as $tableRow) {
        $table = $tableRow[$tableKey];

        // Get CREATE TABLE statement
        $createTable = $db->getRow("SHOW CREATE TABLE `$table`");
        $createKey = 'Create Table';

        echo "-- --------------------------------------------------------\n";
        echo "-- Table: $table\n";
        echo "-- --------------------------------------------------------\n\n";
        echo "DROP TABLE IF EXISTS `$table`;\n";
        echo $createTable[$createKey] . ";\n\n";

        // Get table data
        $rows = $db->getAll("SELECT * FROM `$table`");

        if (!empty($rows)) {
            $columns = array_keys($rows[0]);
            $columnList = '`' . implode('`, `', $columns) . '`';

            echo "INSERT INTO `$table` ($columnList) VALUES\n";

            $valueRows = [];
            foreach ($rows as $row) {
                $values = [];
                foreach ($row as $value) {
                    if ($value === null) {
                        $values[] = 'NULL';
                    } else {
                        $values[] = "'" . addslashes($value) . "'";
                    }
                }
                $valueRows[] = '(' . implode(', ', $values) . ')';
            }

            // Output in chunks to avoid memory issues
            $chunks = array_chunk($valueRows, 100);
            foreach ($chunks as $i => $chunk) {
                if ($i > 0) {
                    echo ",\n";
                }
                echo implode(",\n", $chunk);
            }
            echo ";\n\n";
        }
    }

    echo "SET FOREIGN_KEY_CHECKS=1;\n";
    exit;
}

// Page config for unified layout
$page_title = 'Databas Backup';
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/settings'],
    ['label' => 'Backup']
];

include __DIR__ . '/components/unified-layout.php';

// Get database stats
$stats = [
    ['label' => 'Deltagare', 'count' => $db->getRow("SELECT COUNT(*) as c FROM riders")['c']],
    ['label' => 'Klubbar', 'count' => $db->getRow("SELECT COUNT(*) as c FROM clubs")['c']],
    ['label' => 'Events', 'count' => $db->getRow("SELECT COUNT(*) as c FROM events")['c']],
    ['label' => 'Resultat', 'count' => $db->getRow("SELECT COUNT(*) as c FROM results")['c']],
    ['label' => 'Serier', 'count' => $db->getRow("SELECT COUNT(*) as c FROM series")['c']],
    ['label' => 'Serieresultat', 'count' => $db->getRow("SELECT COUNT(*) as c FROM series_results")['c']],
];

// Estimate backup size (rough)
$sizeResult = $db->getRow("
    SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb
    FROM information_schema.tables
    WHERE table_schema = '" . DB_NAME . "'
");
$estimatedSize = $sizeResult['size_mb'] ?? '?';
?>

<div class="card">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="database"></i>
            Databas Backup
        </h2>
    </div>
    <div class="card-body">
        <div class="alert alert-warning mb-lg">
            <i data-lucide="alert-triangle"></i>
            <div>
                <strong>Viktigt:</strong> Backup innehåller ALL data inklusive känslig information.
                Förvara filen säkert och radera den när den inte längre behövs.
            </div>
        </div>

        <h3 class="mb-md">Databasinnehåll</h3>
        <div class="gs-info-grid mb-lg">
            <?php foreach ($stats as $stat): ?>
            <div class="gs-info-item">
                <div class="gs-info-label"><?= $stat['label'] ?></div>
                <div class="gs-info-value"><?= number_format($stat['count']) ?></div>
            </div>
            <?php endforeach; ?>
        </div>

        <div class="gs-info-grid mb-lg">
            <div class="gs-info-item">
                <div class="gs-info-label">Uppskattad storlek</div>
                <div class="gs-info-value"><?= $estimatedSize ?> MB</div>
            </div>
            <div class="gs-info-item">
                <div class="gs-info-label">Databas</div>
                <div class="gs-info-value"><?= h(DB_NAME) ?></div>
            </div>
        </div>

        <a href="?download=1" class="btn btn-primary btn-lg">
            <i data-lucide="download"></i>
            Ladda ner backup (.sql)
        </a>
    </div>
</div>

<div class="card mt-lg">
    <div class="card-header">
        <h3>
            <i data-lucide="info"></i>
            Återställning
        </h3>
    </div>
    <div class="card-body">
        <p class="text-muted mb-md">
            För att återställa en backup, använd phpMyAdmin eller kommandoraden:
        </p>
        <pre class="code-block">mysql -u [användarnamn] -p <?= h(DB_NAME) ?> &lt; backup_fil.sql</pre>
    </div>
</div>

<style>
.code-block {
    background: var(--color-secondary);
    color: var(--color-star);
    padding: var(--space-md);
    border-radius: var(--radius-sm);
    font-family: monospace;
    font-size: 0.9rem;
    overflow-x: auto;
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
