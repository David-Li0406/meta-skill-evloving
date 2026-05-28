<?php
/**
 * Debug: Test duplicate finder queries
 */
ini_set('display_errors', '1');
error_reporting(E_ALL);

require_once __DIR__ . '/../../config.php';
require_admin();

header('Content-Type: text/plain; charset=utf-8');

echo "=== DUPLICATE FINDER DEBUG ===\n\n";

// Test 1: Database connection
echo "1. DATABASE CONNECTION:\n";
echo str_repeat("-", 50) . "\n";
try {
    $db = getDB();
    echo "   getDB() OK\n";
    $pdo = $db->getPdo();
    echo "   getPdo() OK\n";
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
    exit;
}

// Test 2: Count riders
echo "\n2. ANTAL RIDERS:\n";
echo str_repeat("-", 50) . "\n";
try {
    $count = $db->getValue("SELECT COUNT(*) FROM riders");
    echo "   Totalt: {$count} riders\n";
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// Test 3: Find exact name duplicates
echo "\n3. EXAKTA NAMNDUPLICATES:\n";
echo str_repeat("-", 50) . "\n";
try {
    $duplicates = $db->getAll("
        SELECT firstname, lastname, COUNT(*) as cnt
        FROM riders
        WHERE firstname IS NOT NULL AND lastname IS NOT NULL
        GROUP BY LOWER(firstname), LOWER(lastname)
        HAVING cnt > 1
        ORDER BY cnt DESC
        LIMIT 20
    ");

    if (empty($duplicates)) {
        echo "   INGA HITTADES!\n";
    } else {
        echo "   Hittade " . count($duplicates) . " grupper:\n";
        foreach ($duplicates as $d) {
            echo "   - {$d['firstname']} {$d['lastname']}: {$d['cnt']} st\n";
        }
    }
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// Test 4: Show some sample riders
echo "\n4. SAMPLE RIDERS (första 10):\n";
echo str_repeat("-", 50) . "\n";
try {
    $riders = $db->getAll("
        SELECT id, firstname, lastname, birth_year, license_number
        FROM riders
        ORDER BY id DESC
        LIMIT 10
    ");
    foreach ($riders as $r) {
        echo "   ID {$r['id']}: {$r['firstname']} {$r['lastname']} ({$r['birth_year']}) - {$r['license_number']}\n";
    }
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// Test 5: Check for NULL names
echo "\n5. RIDERS MED NULL NAMN:\n";
echo str_repeat("-", 50) . "\n";
try {
    $nullFirst = $db->getValue("SELECT COUNT(*) FROM riders WHERE firstname IS NULL");
    $nullLast = $db->getValue("SELECT COUNT(*) FROM riders WHERE lastname IS NULL");
    $emptyFirst = $db->getValue("SELECT COUNT(*) FROM riders WHERE firstname = ''");
    $emptyLast = $db->getValue("SELECT COUNT(*) FROM riders WHERE lastname = ''");

    echo "   NULL firstname: {$nullFirst}\n";
    echo "   NULL lastname: {$nullLast}\n";
    echo "   Empty firstname: {$emptyFirst}\n";
    echo "   Empty lastname: {$emptyLast}\n";
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// Test 6: Check ignored duplicates file
echo "\n6. IGNORERADE DUBBLETTER:\n";
echo str_repeat("-", 50) . "\n";
$ignoredFile = __DIR__ . '/../../uploads/ignored_rider_duplicates.json';
if (file_exists($ignoredFile)) {
    $ignored = json_decode(file_get_contents($ignoredFile), true);
    $count = is_array($ignored) ? count($ignored) : 0;
    echo "   Fil finns: {$ignoredFile}\n";
    echo "   Antal ignorerade par: {$count}\n";
    if ($count > 0 && $count <= 20) {
        echo "   Par: " . implode(', ', $ignored) . "\n";
    }
} else {
    echo "   Fil finns INTE (inga ignorerade)\n";
}

// Test 7: SOUNDEX test
echo "\n7. SOUNDEX TEST (liknande förnamn, samma efternamn):\n";
echo str_repeat("-", 50) . "\n";
try {
    $soundex = $db->getAll("
        SELECT lastname, SOUNDEX(firstname) as fname_sound, COUNT(*) as cnt,
               GROUP_CONCAT(DISTINCT firstname SEPARATOR ', ') as firstnames
        FROM riders
        WHERE firstname IS NOT NULL AND lastname IS NOT NULL
        GROUP BY LOWER(lastname), SOUNDEX(firstname)
        HAVING cnt > 1 AND COUNT(DISTINCT LOWER(firstname)) > 1
        ORDER BY cnt DESC
        LIMIT 10
    ");

    if (empty($soundex)) {
        echo "   INGA HITTADES!\n";
    } else {
        foreach ($soundex as $s) {
            echo "   - {$s['lastname']}: {$s['firstnames']} ({$s['cnt']} st)\n";
        }
    }
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// Test 8: Check if rider_merge_map exists
echo "\n8. RIDER_MERGE_MAP:\n";
echo str_repeat("-", 50) . "\n";
try {
    $count = $db->getValue("SELECT COUNT(*) FROM rider_merge_map");
    echo "   Antal merges: {$count}\n";
} catch (Exception $e) {
    echo "   Tabell finns inte eller FEL: " . $e->getMessage() . "\n";
}

echo "\n=== SLUT ===\n";
