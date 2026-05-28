<?php
/**
 * Migration: Add all profile columns to riders table
 *
 * This migration adds all columns needed for complete profile editing:
 * - Social profiles (Instagram, Strava, Facebook, YouTube, TikTok)
 * - Contact info (phone, email)
 * - Emergency contact (ICE)
 * - Profile image (avatar_url)
 * - Additional fields (uci_id, birth_year)
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Lägg till profilkolumner</title>";
echo "<style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 40px; background: #f5f5f5; max-width: 900px; margin: 0 auto; }
    .card { background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
    h1 { color: #171717; margin-bottom: 8px; }
    h2 { color: #323539; font-size: 18px; margin-top: 24px; margin-bottom: 12px; }
    .success { color: #16a34a; background: #f0fdf4; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #16a34a; margin: 8px 0; }
    .error { color: #dc2626; background: #fef2f2; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #dc2626; margin: 8px 0; }
    .info { color: #2563eb; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #2563eb; margin: 8px 0; }
    .warning { color: #d97706; background: #fffbeb; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #d97706; margin: 8px 0; }
    code { background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
    .btn { display: inline-block; padding: 12px 24px; background: #61CE70; color: #fff; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 16px; margin-right: 8px; }
    .btn:hover { background: #4eb85d; }
    .btn-secondary { background: #6b7280; }
    .btn-secondary:hover { background: #4b5563; }
    table { width: 100%; border-collapse: collapse; margin: 16px 0; }
    th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid #e5e7eb; }
    th { background: #f9fafb; font-weight: 600; }
    .status-exists { color: #16a34a; }
    .status-added { color: #2563eb; }
    .status-failed { color: #dc2626; }
</style>";
echo "</head><body>";

echo "<div class='card'>";
echo "<h1>Migration: Profilkolumner</h1>";
echo "<p style='color: #6b7280;'>Lägger till alla kolumner som behövs för komplett profilredigering</p>";
echo "</div>";

try {
    require_once __DIR__ . '/../../config.php';

    // Check admin authentication
    if (function_exists('require_admin')) {
        require_admin();
    } elseif (function_exists('requireAdmin')) {
        requireAdmin();
    }

    // Get database connection - try multiple methods
    $pdo = null;

    // Method 1: getDB() returns Database object with getPdo()
    if (function_exists('getDB')) {
        $db = getDB();
        if ($db && method_exists($db, 'getPdo')) {
            $pdo = $db->getPdo();
        }
    }

    // Method 2: Global $pdo variable
    if (!$pdo && isset($GLOBALS['pdo'])) {
        $pdo = $GLOBALS['pdo'];
    }

    // Method 3: hub_db() function
    if (!$pdo && function_exists('hub_db')) {
        $pdo = hub_db();
    }

    if (!$pdo) {
        throw new Exception('Kunde inte ansluta till databasen. Kontrollera att config.php är korrekt konfigurerad.');
    }

    echo "<div class='card'>";

    // Define all columns to add
    $columns = [
        // Social profiles
        'social_instagram' => [
            'definition' => "VARCHAR(100) DEFAULT NULL COMMENT 'Instagram användarnamn'",
            'group' => 'Sociala profiler'
        ],
        'social_strava' => [
            'definition' => "VARCHAR(100) DEFAULT NULL COMMENT 'Strava profil'",
            'group' => 'Sociala profiler'
        ],
        'social_facebook' => [
            'definition' => "VARCHAR(255) DEFAULT NULL COMMENT 'Facebook profil'",
            'group' => 'Sociala profiler'
        ],
        'social_youtube' => [
            'definition' => "VARCHAR(100) DEFAULT NULL COMMENT 'YouTube kanal'",
            'group' => 'Sociala profiler'
        ],
        'social_tiktok' => [
            'definition' => "VARCHAR(100) DEFAULT NULL COMMENT 'TikTok användarnamn'",
            'group' => 'Sociala profiler'
        ],

        // Contact info
        'phone' => [
            'definition' => "VARCHAR(50) DEFAULT NULL COMMENT 'Telefonnummer'",
            'group' => 'Kontaktuppgifter'
        ],

        // Emergency contact (ICE)
        'ice_name' => [
            'definition' => "VARCHAR(255) DEFAULT NULL COMMENT 'Nödkontakt namn (In Case of Emergency)'",
            'group' => 'Nödkontakt'
        ],
        'ice_phone' => [
            'definition' => "VARCHAR(50) DEFAULT NULL COMMENT 'Nödkontakt telefon'",
            'group' => 'Nödkontakt'
        ],

        // Profile image
        'avatar_url' => [
            'definition' => "VARCHAR(500) DEFAULT NULL COMMENT 'Profilbild URL (ImgBB)'",
            'group' => 'Profilbild'
        ],
        'profile_image_url' => [
            'definition' => "VARCHAR(500) DEFAULT NULL COMMENT 'Profilbild URL (alternativ)'",
            'group' => 'Profilbild'
        ],

        // Additional fields
        'uci_id' => [
            'definition' => "VARCHAR(50) DEFAULT NULL COMMENT 'UCI ID'",
            'group' => 'Övrigt'
        ],
    ];

    // Get existing columns
    $existingColumns = [];
    $stmt = $pdo->query("SHOW COLUMNS FROM riders");
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        $existingColumns[] = $row['Field'];
    }

    // Group columns by category
    $groups = [];
    foreach ($columns as $name => $info) {
        $groups[$info['group']][$name] = $info;
    }

    $added = 0;
    $skipped = 0;
    $failed = 0;
    $results = [];

    foreach ($groups as $groupName => $groupColumns) {
        echo "<h2>{$groupName}</h2>";
        echo "<table>";
        echo "<tr><th>Kolumn</th><th>Typ</th><th>Status</th></tr>";

        foreach ($groupColumns as $colName => $colInfo) {
            $exists = in_array($colName, $existingColumns);

            if ($exists) {
                echo "<tr>";
                echo "<td><code>{$colName}</code></td>";
                echo "<td><code>" . htmlspecialchars(explode(' ', $colInfo['definition'])[0]) . "</code></td>";
                echo "<td class='status-exists'>Finns redan</td>";
                echo "</tr>";
                $skipped++;
                $results[$colName] = 'exists';
            } else {
                try {
                    $sql = "ALTER TABLE riders ADD COLUMN {$colName} {$colInfo['definition']}";
                    $pdo->exec($sql);
                    echo "<tr>";
                    echo "<td><code>{$colName}</code></td>";
                    echo "<td><code>" . htmlspecialchars(explode(' ', $colInfo['definition'])[0]) . "</code></td>";
                    echo "<td class='status-added'>Tillagd</td>";
                    echo "</tr>";
                    $added++;
                    $results[$colName] = 'added';
                } catch (PDOException $e) {
                    echo "<tr>";
                    echo "<td><code>{$colName}</code></td>";
                    echo "<td><code>" . htmlspecialchars(explode(' ', $colInfo['definition'])[0]) . "</code></td>";
                    echo "<td class='status-failed'>Misslyckades: " . htmlspecialchars($e->getMessage()) . "</td>";
                    echo "</tr>";
                    $failed++;
                    $results[$colName] = 'failed';
                }
            }
        }

        echo "</table>";
    }

    echo "</div>";

    // Summary
    echo "<div class='card'>";
    echo "<h2>Sammanfattning</h2>";

    if ($added > 0) {
        echo "<p class='success'>✓ {$added} kolumn(er) har lagts till</p>";
    }
    if ($skipped > 0) {
        echo "<p class='info'>{$skipped} kolumn(er) fanns redan</p>";
    }
    if ($failed > 0) {
        echo "<p class='error'>✗ {$failed} kolumn(er) kunde inte läggas till</p>";
    }

    if ($failed === 0) {
        echo "<h2 style='color: #16a34a; margin-top: 24px;'>Migrering klar!</h2>";
        echo "<p>Alla nödvändiga kolumner finns nu i databasen. Profilredigering bör fungera korrekt.</p>";
    } else {
        echo "<p class='warning'>Vissa kolumner kunde inte läggas till. Kontrollera felmeddelandena ovan.</p>";
    }

    echo "<div style='margin-top: 24px;'>";
    echo "<a href='/admin/' class='btn'>Tillbaka till Admin</a>";
    echo "<a href='/profile/edit' class='btn btn-secondary' target='_blank'>Testa profilredigering</a>";
    echo "<a href='/admin/settings-imgbb.php' class='btn btn-secondary'>ImgBB-inställningar</a>";
    echo "</div>";

    echo "</div>";

    // Verification
    echo "<div class='card'>";
    echo "<h2>Verifiering</h2>";
    echo "<p>Alla kolumner i <code>riders</code>-tabellen:</p>";

    $stmt = $pdo->query("SHOW COLUMNS FROM riders");
    $allCols = $stmt->fetchAll(PDO::FETCH_ASSOC);

    echo "<table>";
    echo "<tr><th>Kolumn</th><th>Typ</th><th>Null</th><th>Default</th></tr>";
    foreach ($allCols as $col) {
        $highlight = isset($results[$col['Field']]) ? ' style="background: #f0fdf4;"' : '';
        echo "<tr{$highlight}>";
        echo "<td><code>{$col['Field']}</code></td>";
        echo "<td><code>{$col['Type']}</code></td>";
        echo "<td>{$col['Null']}</td>";
        echo "<td>" . ($col['Default'] ?? '<em>NULL</em>') . "</td>";
        echo "</tr>";
    }
    echo "</table>";
    echo "</div>";

} catch (Exception $e) {
    echo "<div class='card'>";
    echo "<p class='error'>✗ Ett fel uppstod: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "</div>";
}

echo "</body></html>";
