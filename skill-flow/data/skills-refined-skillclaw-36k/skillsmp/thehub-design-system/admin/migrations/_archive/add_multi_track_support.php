<?php
/**
 * Migration: Add Multi-Track Support
 *
 * Adds columns to event_tracks for:
 * - route_type: Type of route (elite, sport, etc.)
 * - route_label: Display label for the route
 * - is_primary: Flag for primary/default track
 * - display_order: Sort order for tracks
 * - color: Track color for map display
 *
 * @since 2025-12-10
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration: Multi-Track Support</title>";
echo "<style>
    body { font-family: system-ui, sans-serif; padding: 20px; background: #f5f5f5; max-width: 800px; margin: 0 auto; }
    .success { color: #059669; }
    .error { color: #dc2626; }
    .info { color: #0284c7; }
    .box { background: white; padding: 20px; border-radius: 8px; margin: 15px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    h1 { color: #171717; }
    pre { background: #1a1a1a; color: #e5e5e5; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 12px; }
    code { background: #e5e5e5; padding: 2px 6px; border-radius: 4px; }
</style>";
echo "</head><body>";
echo "<h1>Migration: Multi-Track Support</h1>";
echo "<p>Lägger till stöd för flera GPX-banor per event med etiketter och färger.</p>";

$columnsAdded = 0;
$errors = [];

try {
    // Check if table exists first
    $tableExists = $db->getAll("SHOW TABLES LIKE 'event_tracks'");
    if (empty($tableExists)) {
        echo "<div class='box' style='background: #fef3c7; border-left: 4px solid #f59e0b;'>";
        echo "<h2 style='color: #b45309;'>⚠️ Tabell saknas</h2>";
        echo "<p>Tabellen <code>event_tracks</code> finns inte. Kör först migrationen <strong>add_event_map_system.php</strong></p>";
        echo "</div>";
        echo "<p><a href='/admin/migrations/migration-browser.php'>← Tillbaka till Migration Browser</a></p>";
        echo "</body></html>";
        exit;
    }

    // Get existing columns
    $existingColumns = [];
    $columnsResult = $db->getAll("SHOW COLUMNS FROM event_tracks");
    foreach ($columnsResult as $col) {
        $existingColumns[] = $col['Field'];
    }

    // =========================================
    // COLUMN 1: route_type
    // =========================================
    echo "<div class='box'>";
    echo "<h3>1. route_type</h3>";
    echo "<p>Typ av bana (t.ex. 'elite', 'sport', 'junior')</p>";

    if (!in_array('route_type', $existingColumns)) {
        $db->query("ALTER TABLE event_tracks ADD COLUMN route_type VARCHAR(50) NULL AFTER name");
        echo "<p class='success'>✓ Lade till kolumn route_type</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn route_type finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // COLUMN 2: route_label
    // =========================================
    echo "<div class='box'>";
    echo "<h3>2. route_label</h3>";
    echo "<p>Visningsnamn för banan (t.ex. 'Elite 45km')</p>";

    if (!in_array('route_label', $existingColumns)) {
        $db->query("ALTER TABLE event_tracks ADD COLUMN route_label VARCHAR(100) NULL AFTER route_type");
        echo "<p class='success'>✓ Lade till kolumn route_label</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn route_label finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // COLUMN 3: is_primary
    // =========================================
    echo "<div class='box'>";
    echo "<h3>3. is_primary</h3>";
    echo "<p>Flagga för primär/huvudbana (visas först)</p>";

    if (!in_array('is_primary', $existingColumns)) {
        $db->query("ALTER TABLE event_tracks ADD COLUMN is_primary TINYINT(1) DEFAULT 0 AFTER route_label");
        echo "<p class='success'>✓ Lade till kolumn is_primary</p>";
        $columnsAdded++;

        // Set existing tracks as primary
        $db->query("UPDATE event_tracks SET is_primary = 1 WHERE id IN (
            SELECT id FROM (
                SELECT MIN(id) as id FROM event_tracks GROUP BY event_id
            ) as first_tracks
        )");
        echo "<p class='info'>ℹ Satte befintliga banor som primära</p>";
    } else {
        echo "<p class='info'>ℹ Kolumn is_primary finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // COLUMN 4: display_order
    // =========================================
    echo "<div class='box'>";
    echo "<h3>4. display_order</h3>";
    echo "<p>Sorteringsordning för banor</p>";

    if (!in_array('display_order', $existingColumns)) {
        $db->query("ALTER TABLE event_tracks ADD COLUMN display_order INT DEFAULT 0 AFTER is_primary");
        echo "<p class='success'>✓ Lade till kolumn display_order</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn display_order finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // COLUMN 5: color
    // =========================================
    echo "<div class='box'>";
    echo "<h3>5. color</h3>";
    echo "<p>Färg för banan på kartan (hex-kod)</p>";

    if (!in_array('color', $existingColumns)) {
        $db->query("ALTER TABLE event_tracks ADD COLUMN color VARCHAR(7) DEFAULT '#3B82F6' AFTER display_order");
        echo "<p class='success'>✓ Lade till kolumn color</p>";
        $columnsAdded++;
    } else {
        echo "<p class='info'>ℹ Kolumn color finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // INDEX
    // =========================================
    echo "<div class='box'>";
    echo "<h3>6. Index för sortering</h3>";

    $indexExists = $db->getAll("SHOW INDEX FROM event_tracks WHERE Key_name = 'idx_event_tracks_order'");
    if (empty($indexExists)) {
        $db->query("ALTER TABLE event_tracks ADD INDEX idx_event_tracks_order (event_id, display_order)");
        echo "<p class='success'>✓ Skapade index idx_event_tracks_order</p>";
    } else {
        echo "<p class='info'>ℹ Index idx_event_tracks_order finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // SUMMARY
    // =========================================
    echo "<div class='box' style='background: #d1fae5; border-left: 4px solid #059669;'>";
    echo "<h2 class='success'>✅ Migration klar!</h2>";

    if ($columnsAdded > 0) {
        echo "<p><strong>{$columnsAdded} kolumner lades till.</strong></p>";
    } else {
        echo "<p>Alla kolumner fanns redan.</p>";
    }

    echo "<h4>Nya funktioner:</h4>";
    echo "<ul>";
    echo "<li><strong>Flera banor per event</strong> - Ladda upp olika GPX-filer för Elite, Sport, etc.</li>";
    echo "<li><strong>Etiketter</strong> - Visa tydliga namn i dropdown-menyer</li>";
    echo "<li><strong>Färgkodning</strong> - Varje bana får sin egen färg på kartan</li>";
    echo "<li><strong>Primär bana</strong> - En bana visas som standard</li>";
    echo "</ul>";

    echo "<h4>Tillgängliga färger:</h4>";
    echo "<div style='display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px;'>";
    $colors = [
        '#3B82F6' => 'Blå',
        '#61CE70' => 'Grön',
        '#EF4444' => 'Röd',
        '#F59E0B' => 'Orange',
        '#8B5CF6' => 'Lila',
        '#EC4899' => 'Rosa',
        '#14B8A6' => 'Teal',
        '#6B7280' => 'Grå'
    ];
    foreach ($colors as $hex => $name) {
        echo "<span style='display: inline-flex; align-items: center; gap: 5px; padding: 4px 10px; background: #f5f5f5; border-radius: 20px;'>";
        echo "<span style='width: 14px; height: 14px; background: {$hex}; border-radius: 3px;'></span>";
        echo $name;
        echo "</span>";
    }
    echo "</div>";
    echo "</div>";

    echo "<p style='margin-top: 20px;'>";
    echo "<a href='/admin/migrations/migration-browser.php' style='color: #004a98;'>← Tillbaka till Migration Browser</a>";
    echo " | ";
    echo "<a href='/admin/event-map.php' style='color: #004a98;'>Testa karthantering →</a>";
    echo "</p>";

} catch (Exception $e) {
    echo "<div class='box' style='background: #fee2e2; border-left: 4px solid #dc2626;'>";
    echo "<h2 class='error'>✗ Migration misslyckades!</h2>";
    echo "<p class='error'>Fel: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
    echo "</div>";
}

echo "</body></html>";
