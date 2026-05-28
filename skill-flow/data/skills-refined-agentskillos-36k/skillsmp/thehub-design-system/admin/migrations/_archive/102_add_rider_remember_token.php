<?php
/**
 * Migration 102: Add Remember Token to Riders
 *
 * Adds remember_token columns for "kom ihåg mig" (remember me) functionality.
 *
 * @since 2026-01-10
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration 102: Rider Remember Token</title>";
echo "<style>
    body { font-family: system-ui, sans-serif; padding: 20px; background: #0b131e; color: #f8f2f0; max-width: 900px; margin: 0 auto; }
    .success { color: #10b981; }
    .error { color: #ef4444; }
    .info { color: #38bdf8; }
    .box { background: #0e1621; padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid rgba(55, 212, 214, 0.2); }
    h1 { color: #37d4d6; }
    h3 { color: #f8f2f0; margin-top: 0; }
    .btn { display: inline-block; padding: 10px 20px; background: #37d4d6; color: #0b131e; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 20px; }
</style>";
echo "</head><body>";
echo "<h1>Migration 102: Rider Remember Token</h1>";

$columnsAdded = 0;

/**
 * Helper: Check if column exists
 */
function columnExists($db, $table, $column) {
    $result = $db->getAll("SHOW COLUMNS FROM `{$table}` LIKE '{$column}'");
    return !empty($result);
}

/**
 * Helper: Check if index exists
 */
function indexExists($db, $table, $index) {
    $result = $db->getAll("SHOW INDEX FROM `{$table}` WHERE Key_name = '{$index}'");
    return !empty($result);
}

try {
    echo "<div class='box'>";
    echo "<h3>Lägg till remember_token-kolumner i riders</h3>";

    // remember_token
    if (!columnExists($db, 'riders', 'remember_token')) {
        $db->query("ALTER TABLE riders ADD COLUMN remember_token VARCHAR(64) NULL");
        echo "<p class='success'>✓ Lade till kolumn remember_token</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn remember_token finns redan</p>";
    }

    // remember_token_expires
    if (!columnExists($db, 'riders', 'remember_token_expires')) {
        $db->query("ALTER TABLE riders ADD COLUMN remember_token_expires DATETIME NULL");
        echo "<p class='success'>✓ Lade till kolumn remember_token_expires</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn remember_token_expires finns redan</p>";
    }

    // Index
    if (!indexExists($db, 'riders', 'idx_remember_token')) {
        $db->query("ALTER TABLE riders ADD INDEX idx_remember_token (remember_token)");
        echo "<p class='success'>✓ Lade till index idx_remember_token</p>";
    } else {
        echo "<p class='info'>ℹ Index idx_remember_token finns redan</p>";
    }

    echo "</div>";

    // Summary
    echo "<div class='box'>";
    echo "<h3>Sammanfattning</h3>";
    echo "<p class='success'>✓ {$columnsAdded} kolumner tillagda</p>";
    echo "<p class='info'>'Kom ihåg mig'-funktionen är nu aktiverad!</p>";
    echo "</div>";

} catch (Exception $e) {
    echo "<div class='box'>";
    echo "<p class='error'>✗ Fel vid migration: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "</div>";
}

echo "<a href='/admin/' class='btn'>Tillbaka till Admin</a>";
echo "</body></html>";
