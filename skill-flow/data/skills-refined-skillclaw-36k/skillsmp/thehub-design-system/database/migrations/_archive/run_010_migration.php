<?php
/**
 * Run Migration 010: Categories to Classes
 *
 * This script:
 * 1. Runs the SQL migration
 * 2. Recalculates class positions for all affected events
 * 3. Recalculates class points for all affected events
 * 4. Generates a summary report
 */

require_once __DIR__ . '/../../config.php';
require_once __DIR__ . '/../../includes/class-calculations.php';

$db = getDB();

echo "===========================================\n";
echo "Migration 010: Categories → Classes\n";
echo "===========================================\n\n";

// Step 1: Run SQL migration
echo "Step 1: Running SQL migration...\n";
try {
    $sql = file_get_contents(__DIR__ . '/010_migrate_categories_to_classes.sql');

    // Split into individual statements
    $statements = array_filter(
        array_map('trim', explode(';', $sql)),
        function($stmt) {
            return !empty($stmt) &&
                   !preg_match('/^\s*--/', $stmt) &&
                   !preg_match('/^\s*SELECT/', $stmt); // Skip SELECT statements for now
        }
    );

    foreach ($statements as $statement) {
        if (!empty($statement)) {
            $db->query($statement);
        }
    }

    echo "✅ SQL migration completed successfully\n\n";
} catch (Exception $e) {
    echo "❌ Error running SQL migration: " . $e->getMessage() . "\n";
    exit(1);
}

// Step 2: Get all events that need recalculation
echo "Step 2: Finding events to recalculate...\n";
$eventsToRecalculate = $db->getAll("
    SELECT DISTINCT e.id, e.name, e.date
    FROM results r
    INNER JOIN events e ON r.event_id = e.id
    WHERE r.class_id IS NOT NULL
    ORDER BY e.date DESC
");

echo "Found " . count($eventsToRecalculate) . " events to recalculate\n\n";

// Step 3: Enable classes for all these events
echo "Step 3: Enabling classes for events...\n";
foreach ($eventsToRecalculate as $event) {
    $db->update('events', ['enable_classes' => 1], 'id = ?', [$event['id']]);
}
echo "✅ Enabled classes for " . count($eventsToRecalculate) . " events\n\n";

// Step 4: Recalculate class positions
echo "Step 4: Recalculating class positions...\n";
$totalUpdated = 0;
$errors = [];

foreach ($eventsToRecalculate as $event) {
    echo "  Processing: {$event['name']} ({$event['date']})... ";

    try {
        $stats = recalculateClassPositions($db, $event['id']);
        $totalUpdated += $stats['updated'];

        if (!empty($stats['errors'])) {
            $errors = array_merge($errors, $stats['errors']);
            echo "⚠️  {$stats['updated']} updated (with errors)\n";
        } else {
            echo "✅ {$stats['updated']} updated\n";
        }
    } catch (Exception $e) {
        echo "❌ Error: " . $e->getMessage() . "\n";
        $errors[] = "Event {$event['id']}: " . $e->getMessage();
    }
}

echo "\n✅ Class positions recalculated: {$totalUpdated} results\n";
if (!empty($errors)) {
    echo "⚠️  Errors encountered: " . count($errors) . "\n";
}
echo "\n";

// Step 5: Recalculate class points
echo "Step 5: Recalculating class points...\n";
$totalPointsUpdated = 0;

foreach ($eventsToRecalculate as $event) {
    echo "  Processing: {$event['name']}... ";

    try {
        $stats = recalculateClassPoints($db, $event['id']);
        $totalPointsUpdated += $stats['updated'];

        if (!empty($stats['errors'])) {
            echo "⚠️  {$stats['updated']} updated (with errors)\n";
        } else {
            echo "✅ {$stats['updated']} points calculated\n";
        }
    } catch (Exception $e) {
        echo "❌ Error: " . $e->getMessage() . "\n";
    }
}

echo "\n✅ Class points calculated: {$totalPointsUpdated} results\n\n";

// Step 6: Generate summary report
echo "===========================================\n";
echo "Migration Summary Report\n";
echo "===========================================\n\n";

// Count migrated results
$migratedCount = $db->getRow("
    SELECT COUNT(*) as count
    FROM results
    WHERE category_id IS NOT NULL AND class_id IS NOT NULL
");

echo "Results migrated: {$migratedCount['count']}\n";

// Count by class
$classCounts = $db->getAll("
    SELECT
        cls.name,
        cls.display_name,
        COUNT(*) as count
    FROM results r
    INNER JOIN classes cls ON r.class_id = cls.id
    WHERE r.category_id IS NOT NULL
    GROUP BY cls.id, cls.name, cls.display_name
    ORDER BY count DESC
    LIMIT 10
");

echo "\nTop 10 Classes:\n";
foreach ($classCounts as $classCount) {
    echo sprintf("  %-20s %-40s %5d results\n",
        $classCount['name'],
        $classCount['display_name'],
        $classCount['count']
    );
}

// Results without class assignment
$unmigrated = $db->getRow("
    SELECT COUNT(*) as count
    FROM results
    WHERE category_id IS NOT NULL AND class_id IS NULL
");

if ($unmigrated['count'] > 0) {
    echo "\n⚠️  Warning: {$unmigrated['count']} results could not be migrated\n";
    echo "   These need manual review.\n";
}

// Events affected
echo "\nEvents affected: " . count($eventsToRecalculate) . "\n";

echo "\n===========================================\n";
echo "Migration completed successfully!\n";
echo "===========================================\n\n";

echo "Next steps:\n";
echo "1. Review the migration log: SELECT * FROM category_class_migration_log\n";
echo "2. Test the application thoroughly\n";
echo "3. Update series to enable classes if needed\n";
echo "4. Once confirmed working, you can deprecate the category_id column\n\n";

// Save report to file
$report = ob_get_contents();
file_put_contents(
    __DIR__ . '/010_migration_report_' . date('Y-m-d_His') . '.txt',
    $report
);

echo "Report saved to: " . __DIR__ . "/010_migration_report_" . date('Y-m-d_His') . ".txt\n";
