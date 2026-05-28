<?php
/**
 * Migration: Add profile fields for registration auto-fill
 *
 * Adds phone, emergency contact, and UCI ID fields to riders table
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Add Profile Fields Migration</title>";
echo "<style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 40px; background: #f5f5f5; max-width: 800px; margin: 0 auto; }
    .card { background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
    h1 { color: #171717; margin-bottom: 8px; }
    h2 { color: #323539; font-size: 18px; margin-top: 24px; }
    .success { color: #16a34a; background: #f0fdf4; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #16a34a; margin: 8px 0; }
    .error { color: #dc2626; background: #fef2f2; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #dc2626; margin: 8px 0; }
    .info { color: #2563eb; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #2563eb; margin: 8px 0; }
    code { background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
    .btn { display: inline-block; padding: 12px 24px; background: #61CE70; color: #fff; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 16px; }
</style>";
echo "</head><body>";

echo "<div class='card'>";
echo "<h1>Migration: Profilfält för anmälan</h1>";
echo "<p style='color: #6b7280;'>Lägger till telefon, nödkontakt och UCI ID för auto-ifyllning vid anmälan</p>";
echo "</div>";

try {
    require_once __DIR__ . '/../../config.php';

    // Check admin authentication
    if (function_exists('require_admin')) {
        require_admin();
    } elseif (function_exists('requireAdmin')) {
        requireAdmin();
    }

    $pdo = $GLOBALS['pdo'] ?? null;
    if (!$pdo) {
        throw new Exception('Database connection not available');
    }

    echo "<div class='card'>";

    // Define columns to add
    $columns = [
        'phone' => "VARCHAR(50) DEFAULT NULL COMMENT 'Telefonnummer'",
        'uci_id' => "VARCHAR(50) DEFAULT NULL COMMENT 'UCI ID'",
        'ice_name' => "VARCHAR(255) DEFAULT NULL COMMENT 'Nödkontakt namn (In Case of Emergency)'",
        'ice_phone' => "VARCHAR(50) DEFAULT NULL COMMENT 'Nödkontakt telefon'"
    ];

    foreach ($columns as $columnName => $columnDef) {
        echo "<h2>Kolumn: <code>{$columnName}</code></h2>";

        // Check if column exists
        $stmt = $pdo->query("SHOW COLUMNS FROM riders LIKE '{$columnName}'");
        $exists = $stmt->rowCount() > 0;

        if ($exists) {
            echo "<p class='info'>Kolumnen <code>{$columnName}</code> finns redan.</p>";
        } else {
            try {
                $pdo->exec("ALTER TABLE riders ADD COLUMN {$columnName} {$columnDef}");
                echo "<p class='success'>✓ Kolumnen <code>{$columnName}</code> har lagts till!</p>";
            } catch (PDOException $e) {
                echo "<p class='error'>✗ Kunde inte lägga till <code>{$columnName}</code>: " . htmlspecialchars($e->getMessage()) . "</p>";
            }
        }
    }

    // Verify all columns
    echo "<h2>Verifiering</h2>";
    $allGood = true;
    foreach (array_keys($columns) as $col) {
        $stmt = $pdo->query("SHOW COLUMNS FROM riders LIKE '{$col}'");
        if ($stmt->rowCount() > 0) {
            echo "<p class='success'>✓ <code>{$col}</code> finns</p>";
        } else {
            echo "<p class='error'>✗ <code>{$col}</code> saknas</p>";
            $allGood = false;
        }
    }

    if ($allGood) {
        echo "<h2 style='color: #16a34a;'>✅ Migrering klar!</h2>";
        echo "<p>Alla kolumner har lagts till. Användare kan nu fylla i dessa fält via profilredigering.</p>";
    }

    echo "<a href='/admin/' class='btn'>Tillbaka till Admin</a>";
    echo " <a href='/profile/edit' class='btn' style='background: #6b7280;'>Testa profilredigering</a>";
    echo "</div>";

} catch (Exception $e) {
    echo "<div class='card'>";
    echo "<p class='error'>✗ Ett fel uppstod: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "</div>";
}

echo "</body></html>";
