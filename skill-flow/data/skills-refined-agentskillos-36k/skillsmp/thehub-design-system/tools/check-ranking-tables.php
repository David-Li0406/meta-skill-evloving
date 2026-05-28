<?php
/**
 * Simple Database Table Check
 * This script checks if ranking tables exist and displays any errors
 */

// Force display all errors
error_reporting(E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

echo "<h1>Database Table Check</h1>";
echo "<pre>";

try {
    // Load config
    echo "1. Loading config...\n";
    require_once __DIR__ . '/../config.php';
    echo "   ✅ Config loaded\n\n";

    // Get database connection
    echo "2. Connecting to database...\n";
    $db = getDB();
    echo "   ✅ Database connected\n\n";

    // Check if ranking_points table exists
    echo "3. Checking ranking_points table...\n";
    try {
        $result = $db->getRow("SELECT COUNT(*) as cnt FROM ranking_points");
        echo "   ✅ ranking_points table exists with {$result['cnt']} rows\n\n";
    } catch (Exception $e) {
        echo "   ❌ ranking_points table ERROR: " . $e->getMessage() . "\n\n";
    }

    // Check if ranking_snapshots table exists
    echo "4. Checking ranking_snapshots table...\n";
    try {
        $result = $db->getRow("SELECT COUNT(*) as cnt FROM ranking_snapshots");
        echo "   ✅ ranking_snapshots table exists with {$result['cnt']} rows\n\n";
    } catch (Exception $e) {
        echo "   ❌ ranking_snapshots table ERROR: " . $e->getMessage() . "\n\n";
    }

    // Check if club_ranking_snapshots table exists
    echo "5. Checking club_ranking_snapshots table...\n";
    try {
        $result = $db->getRow("SELECT COUNT(*) as cnt FROM club_ranking_snapshots");
        echo "   ✅ club_ranking_snapshots table exists with {$result['cnt']} rows\n\n";
    } catch (Exception $e) {
        echo "   ❌ club_ranking_snapshots table ERROR: " . $e->getMessage() . "\n\n";
    }

    // Check if ranking_functions.php can be loaded
    echo "6. Loading ranking_functions.php...\n";
    require_once __DIR__ . '/../includes/ranking_functions.php';
    echo "   ✅ ranking_functions.php loaded\n\n";

    // Check if key functions exist
    echo "7. Checking if key functions exist...\n";
    if (function_exists('calculateAllRankingPoints')) {
        echo "   ✅ calculateAllRankingPoints() exists\n";
    } else {
        echo "   ❌ calculateAllRankingPoints() NOT FOUND\n";
    }

    if (function_exists('createRankingSnapshot')) {
        echo "   ✅ createRankingSnapshot() exists\n";
    } else {
        echo "   ❌ createRankingSnapshot() NOT FOUND\n";
    }

    if (function_exists('createClubRankingSnapshot')) {
        echo "   ✅ createClubRankingSnapshot() exists\n";
    } else {
        echo "   ❌ createClubRankingSnapshot() NOT FOUND\n";
    }
    echo "\n";

    // Check migrations table
    echo "8. Checking which migrations have been run...\n";
    try {
        // Try different possible column names
        $migrations = $db->getAll("SELECT * FROM migrations ORDER BY id DESC LIMIT 10");
        if (!empty($migrations)) {
            echo "   Recent migrations:\n";
            foreach ($migrations as $m) {
                // Handle different column name formats
                $fileName = $m['migration_file'] ?? $m['file'] ?? $m['name'] ?? 'Unknown';
                $execTime = $m['executed_at'] ?? $m['created_at'] ?? $m['run_at'] ?? 'Unknown';
                echo "   - {$fileName} at {$execTime}\n";
            }
        } else {
            echo "   ℹ️  No migrations recorded yet\n";
        }
    } catch (Exception $e) {
        echo "   ℹ️  Could not read migrations table: " . $e->getMessage() . "\n";
        echo "   (This is not critical - migrations may use a different tracking system)\n";
    }
    echo "\n";

    echo "9. Summary:\n";
    echo "   All basic checks completed. If you see this message, the basic\n";
    echo "   system is working. Check above for any ❌ errors.\n\n";

    echo "   If tables are missing, run the migrations at:\n";
    echo "   /admin/migrate.php\n\n";

} catch (Exception $e) {
    echo "\n❌ FATAL ERROR:\n";
    echo "Message: " . $e->getMessage() . "\n";
    echo "File: " . $e->getFile() . "\n";
    echo "Line: " . $e->getLine() . "\n\n";
    echo "Stack trace:\n";
    echo $e->getTraceAsString() . "\n";
}

echo "</pre>";
echo "<p><a href='/admin/migrate.php'>Go to Migrations</a> | <a href='/admin/ranking.php'>Go to Ranking Admin</a></p>";
?>
