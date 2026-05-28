<?php
/**
 * Migration 014: Performance indexes for Journey Analysis
 * Adds indexes required for efficient cohort calculations
 */

// Get PDO connection
$pdo = $pdo ?? $GLOBALS['pdo'] ?? null;
if (!$pdo) {
    require_once __DIR__ . '/../../config.php';
    $pdo = $GLOBALS['pdo'] ?? null;
}

if (!$pdo) {
    echo "ERROR: No PDO connection available\n";
    return;
}

echo "=== Migration 014: Performance Indexes ===\n\n";

// Helper: check if index exists
$checkIndex = function(string $table, string $indexName) use ($pdo): bool {
    $stmt = $pdo->prepare("
        SELECT COUNT(*) FROM information_schema.STATISTICS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = ?
        AND INDEX_NAME = ?
    ");
    $stmt->execute([$table, $indexName]);
    return $stmt->fetchColumn() > 0;
};

// Helper: add index if not exists
$addIndex = function(string $table, string $indexName, string $columns) use ($pdo, $checkIndex): void {
    if ($checkIndex($table, $indexName)) {
        echo "Index '$indexName' finns redan - hoppar över\n";
        return;
    }
    try {
        $pdo->exec("CREATE INDEX $indexName ON $table ($columns)");
        echo "Skapade index '$indexName' på '$table'\n";
    } catch (PDOException $e) {
        echo "Fel: " . $e->getMessage() . "\n";
    }
};

// Create indexes
$addIndex('results', 'idx_results_cyclist', 'cyclist_id');
$addIndex('results', 'idx_results_event', 'event_id');
$addIndex('events', 'idx_events_date', 'date');
$addIndex('results', 'idx_results_cyclist_event', 'cyclist_id, event_id');

echo "\n=== Klar ===\n";
