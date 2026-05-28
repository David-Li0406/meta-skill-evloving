<?php
/**
 * Migration 051: Populate series_brands using PHP (MySQL 5.7 compatible)
 *
 * This script populates the series_brands table and links series to brands
 * using PHP regex instead of MySQL REGEXP_REPLACE for compatibility.
 *
 * Run this if migration 050 didn't populate the data (MySQL < 8.0)
 */

// Get database connection - support multiple contexts
if (function_exists('getDB')) {
    $pdo = getDB();
} elseif (isset($GLOBALS['pdo'])) {
    $pdo = $GLOBALS['pdo'];
} else {
    // Direct execution
    require_once dirname(__DIR__, 2) . '/config/database.php';
    global $pdo;
}

if (!$pdo) {
    die("No database connection available\n");
}

echo "Populating series_brands table...\n";

// Get all series
$series = $pdo->query("
    SELECT id, name, logo, gradient_start, gradient_end, accent_color
    FROM series
    WHERE name IS NOT NULL AND name != ''
    ORDER BY year DESC, name ASC
")->fetchAll(PDO::FETCH_ASSOC);

echo "Found " . count($series) . " series\n";

// Extract unique brand names using PHP regex
$brands = [];
foreach ($series as $s) {
    // Remove trailing 4-digit year from name
    $brandName = trim(preg_replace('/\s*\d{4}$/', '', $s['name']));
    if (empty($brandName)) {
        continue;
    }

    // Only store first occurrence (keeps most recent series styling)
    if (!isset($brands[$brandName])) {
        $brands[$brandName] = [
            'name' => $brandName,
            'slug' => strtolower(str_replace(' ', '-', $brandName)),
            'logo' => $s['logo'],
            'gradient_start' => $s['gradient_start'] ?: '#004A98',
            'gradient_end' => $s['gradient_end'] ?: '#002a5c',
            'accent_color' => $s['accent_color'] ?: '#61CE70'
        ];
    }
}

echo "Found " . count($brands) . " unique brands\n";

// Insert brands
$insertStmt = $pdo->prepare("
    INSERT INTO series_brands (name, slug, logo, gradient_start, gradient_end, accent_color, active)
    VALUES (?, ?, ?, ?, ?, ?, 1)
    ON DUPLICATE KEY UPDATE
        logo = COALESCE(VALUES(logo), logo),
        gradient_start = VALUES(gradient_start),
        gradient_end = VALUES(gradient_end),
        accent_color = VALUES(accent_color)
");

$brandIds = [];
foreach ($brands as $brand) {
    try {
        $insertStmt->execute([
            $brand['name'],
            $brand['slug'],
            $brand['logo'],
            $brand['gradient_start'],
            $brand['gradient_end'],
            $brand['accent_color']
        ]);
        echo "  + Added/updated brand: {$brand['name']}\n";
    } catch (PDOException $e) {
        echo "  ! Error adding brand {$brand['name']}: " . $e->getMessage() . "\n";
    }
}

// Get all brand IDs by name
$brandRows = $pdo->query("SELECT id, name FROM series_brands")->fetchAll(PDO::FETCH_ASSOC);
foreach ($brandRows as $b) {
    $brandIds[$b['name']] = $b['id'];
}

// Update series to link to their brands
$updateStmt = $pdo->prepare("UPDATE series SET brand_id = ? WHERE id = ?");
$linked = 0;
foreach ($series as $s) {
    $brandName = trim(preg_replace('/\s*\d{4}$/', '', $s['name']));
    if (isset($brandIds[$brandName])) {
        $updateStmt->execute([$brandIds[$brandName], $s['id']]);
        $linked++;
    }
}

echo "\nLinked $linked series to their brands\n";
echo "Done!\n";
