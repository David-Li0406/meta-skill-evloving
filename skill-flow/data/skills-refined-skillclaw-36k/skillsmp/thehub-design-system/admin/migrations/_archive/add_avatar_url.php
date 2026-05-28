<?php
/**
 * Migration: Add avatar_url column to riders table
 *
 * This migration adds support for ImgBB-hosted profile pictures.
 * The avatar_url column stores the external image URL.
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Add Avatar URL Migration</title>";
echo "<style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 40px; background: #f5f5f5; max-width: 800px; margin: 0 auto; }
    .card { background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
    h1 { color: #171717; margin-bottom: 8px; }
    h2 { color: #323539; font-size: 18px; margin-top: 24px; }
    .success { color: #16a34a; background: #f0fdf4; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #16a34a; }
    .error { color: #dc2626; background: #fef2f2; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #dc2626; }
    .info { color: #2563eb; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #2563eb; }
    .warning { color: #d97706; background: #fffbeb; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #d97706; }
    code { background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
    pre { background: #1f2937; color: #f9fafb; padding: 16px; border-radius: 8px; overflow-x: auto; }
    .btn { display: inline-block; padding: 12px 24px; background: #61CE70; color: #fff; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 16px; }
    .btn:hover { background: #4eb85d; }
    .btn-secondary { background: #6b7280; }
</style>";
echo "</head><body>";

echo "<div class='card'>";
echo "<h1>Migration: Avatar URL</h1>";
echo "<p style='color: #6b7280;'>Lägger till <code>avatar_url</code> kolumn för profilbilder via ImgBB</p>";
echo "</div>";

try {
    require_once __DIR__ . '/../../config.php';

    // Check admin authentication
    if (function_exists('require_admin')) {
        require_admin();
    } elseif (function_exists('requireAdmin')) {
        requireAdmin();
    }

    $db = function_exists('getDB') ? getDB() : null;
    if (!$db && isset($GLOBALS['pdo'])) {
        $pdo = $GLOBALS['pdo'];
    } else {
        $pdo = $db->getPdo();
    }

    echo "<div class='card'>";
    echo "<h2>Steg 1: Kontrollera om kolumnen redan finns</h2>";

    // Check if column exists
    $stmt = $pdo->query("SHOW COLUMNS FROM riders LIKE 'avatar_url'");
    $columnExists = $stmt->rowCount() > 0;

    if ($columnExists) {
        echo "<p class='info'>Kolumnen <code>avatar_url</code> finns redan i tabellen <code>riders</code>. Ingen ändring behövs.</p>";
    } else {
        echo "<p class='warning'>Kolumnen <code>avatar_url</code> finns inte. Skapar den nu...</p>";

        echo "<h2>Steg 2: Lägg till avatar_url kolumn</h2>";

        try {
            // Add avatar_url column after email
            $pdo->exec("ALTER TABLE riders ADD COLUMN avatar_url VARCHAR(500) DEFAULT NULL AFTER email");
            echo "<p class='success'>✓ Kolumnen <code>avatar_url</code> har lagts till!</p>";

            // Try to add index
            echo "<h2>Steg 3: Lägg till index (valfritt)</h2>";
            try {
                $pdo->exec("ALTER TABLE riders ADD INDEX idx_avatar_url (avatar_url(255))");
                echo "<p class='success'>✓ Index har lagts till för snabbare sökningar.</p>";
            } catch (PDOException $e) {
                echo "<p class='info'>Index kunde inte läggas till (kan redan finnas): " . htmlspecialchars($e->getMessage()) . "</p>";
            }

        } catch (PDOException $e) {
            echo "<p class='error'>✗ Fel vid skapande av kolumn: " . htmlspecialchars($e->getMessage()) . "</p>";
        }
    }

    // Verify the column
    echo "<h2>Verifiering</h2>";
    $stmt = $pdo->query("SHOW COLUMNS FROM riders LIKE 'avatar_url'");
    if ($stmt->rowCount() > 0) {
        $column = $stmt->fetch(PDO::FETCH_ASSOC);
        echo "<p class='success'>✓ Kolumnen finns nu i databasen!</p>";
        echo "<pre>" . json_encode($column, JSON_PRETTY_PRINT) . "</pre>";
    } else {
        echo "<p class='error'>✗ Kolumnen kunde inte verifieras.</p>";
    }

    // Show next steps
    echo "<h2>Nästa steg</h2>";
    echo "<ol style='line-height: 2;'>";
    echo "<li>Konfigurera ImgBB API-nyckel i <code>/config/imgbb.php</code></li>";
    echo "<li>Testa uppladdning på <code>/test-avatar-upload.php</code></li>";
    echo "<li>Användare kan nu ladda upp profilbilder via <strong>Redigera profil</strong></li>";
    echo "</ol>";

    echo "<a href='/admin/' class='btn'>Tillbaka till Admin</a>";
    echo " <a href='/profile/edit' class='btn btn-secondary'>Testa profilredigering</a>";
    echo "</div>";

} catch (Exception $e) {
    echo "<div class='card'>";
    echo "<p class='error'>✗ Ett fel uppstod: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
    echo "</div>";
}

echo "</body></html>";
