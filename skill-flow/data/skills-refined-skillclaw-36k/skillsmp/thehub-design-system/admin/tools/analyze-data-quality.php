<?php
/**
 * Data Quality Analysis Tool
 * Identifies problematic data in the results and riders tables
 */

require_once __DIR__ . '/../../config.php';
require_once __DIR__ . '/../../hub-config.php';
// Note: getDB() is provided by helpers.php which is included via config.php

header('Content-Type: text/html; charset=utf-8');

// Start session if not started
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Only allow super admin or check for CLI
$isCLI = php_sapi_name() === 'cli';
if (!$isCLI) {
    $isSuperAdmin = (function_exists('hub_is_super_admin') && hub_is_super_admin())
                    || (isset($_SESSION['admin_role']) && $_SESSION['admin_role'] === 'super_admin');
    if (!$isSuperAdmin) {
        die('Access denied - Super admin required');
    }
}

$db = getDB();

echo "<html><head><title>Data Quality Analysis</title>";
echo "<style>
body { font-family: system-ui, sans-serif; padding: 20px; max-width: 1400px; margin: 0 auto; }
h1, h2, h3 { color: #171717; }
.problem { background: #fef2f2; border: 1px solid #ef4444; padding: 15px; margin: 10px 0; border-radius: 8px; }
.warning { background: #fffbeb; border: 1px solid #f59e0b; padding: 15px; margin: 10px 0; border-radius: 8px; }
.info { background: #eff6ff; border: 1px solid #3b82f6; padding: 15px; margin: 10px 0; border-radius: 8px; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; }
th, td { border: 1px solid #e5e7eb; padding: 8px; text-align: left; font-size: 13px; }
th { background: #f9fafb; }
tr:hover { background: #f3f4f6; }
.count { font-weight: bold; color: #ef4444; }
a { color: #2563eb; }
</style></head><body>";

echo "<h1>Data Quality Analysis</h1>";
echo "<p>Analyserar databas efter problem...</p>";

// ============================================================================
// 1. CLUBS THAT LOOK LIKE TIMES
// ============================================================================
echo "<h2>1. Klubbar som ser ut som tider/sträcktider</h2>";

$timePatternClubs = $db->getAll("
    SELECT c.id, c.name, c.city, COUNT(r.id) as rider_count
    FROM clubs c
    LEFT JOIN riders r ON r.club_id = c.id
    WHERE c.name REGEXP '^[0-9]{1,2}:[0-9]{2}:[0-9]{2}'
       OR c.name REGEXP '^[0-9]{1,2}:[0-9]{2}\.[0-9]+'
       OR c.name REGEXP '^[0-9]+\.[0-9]+\.[0-9]+'
       OR c.name REGEXP '^\+[0-9]{10,}'
       OR c.name REGEXP '^[0-9]{10,}'
       OR c.name LIKE '%:%:%'
    GROUP BY c.id
    ORDER BY c.name
");

if ($timePatternClubs) {
    echo "<div class='problem'>";
    echo "<p><span class='count'>" . count($timePatternClubs) . "</span> klubbar ser ut som tider:</p>";
    echo "<table><tr><th>ID</th><th>Namn</th><th>Stad</th><th>Antal åkare</th><th>Åtgärd</th></tr>";
    foreach ($timePatternClubs as $club) {
        echo "<tr>";
        echo "<td>{$club['id']}</td>";
        echo "<td><strong>{$club['name']}</strong></td>";
        echo "<td>{$club['city']}</td>";
        echo "<td>{$club['rider_count']}</td>";
        echo "<td><a href='/admin/clubs.php?edit={$club['id']}'>Redigera</a></td>";
        echo "</tr>";
    }
    echo "</table></div>";
} else {
    echo "<div class='info'>Inga klubbar med tidsmönster hittades.</div>";
}

// ============================================================================
// 2. RESULTS WITH PHONE NUMBERS OR GARBAGE IN BIB/TIME FIELDS
// ============================================================================
echo "<h2>2. Resultat med telefonnummer/skräpdata i fält</h2>";

// Check bib_number for phone numbers or other garbage
$garbageInFields = $db->getAll("
    SELECT r.id, r.event_id, r.cyclist_id, r.position, r.bib_number, r.finish_time, r.points, r.notes,
           e.name as event_name, e.date as event_date,
           CONCAT(ri.firstname, ' ', ri.lastname) as rider_name
    FROM results r
    JOIN events e ON r.event_id = e.id
    JOIN riders ri ON r.cyclist_id = ri.id
    WHERE r.bib_number REGEXP '^\\\+[0-9]{10,}'
       OR r.bib_number REGEXP '^[0-9]{10,}'
       OR r.notes REGEXP '^\\\+[0-9]{10,}'
       OR LENGTH(r.bib_number) > 10
    ORDER BY e.date DESC, r.position
    LIMIT 100
");

if ($garbageInFields) {
    echo "<div class='problem'>";
    echo "<p><span class='count'>" . count($garbageInFields) . "</span> resultat med misstänkt data i bib_number/notes:</p>";
    echo "<table><tr><th>Event</th><th>Datum</th><th>Åkare</th><th>Pos</th><th>Bib</th><th>Tid</th><th>Notes</th></tr>";
    foreach ($garbageInFields as $row) {
        echo "<tr>";
        echo "<td><a href='/event/{$row['event_id']}'>{$row['event_name']}</a></td>";
        echo "<td>{$row['event_date']}</td>";
        echo "<td><a href='/rider/{$row['cyclist_id']}'>{$row['rider_name']}</a></td>";
        echo "<td>{$row['position']}</td>";
        echo "<td><strong>" . htmlspecialchars(substr($row['bib_number'] ?? '', 0, 20)) . "</strong></td>";
        echo "<td>{$row['finish_time']}</td>";
        echo "<td>" . htmlspecialchars(substr($row['notes'] ?? '', 0, 30)) . "</td>";
        echo "</tr>";
    }
    echo "</table></div>";
} else {
    echo "<div class='info'>Inga telefonnummer/skräpdata i bib_number/notes.</div>";
}

// ============================================================================
// 3. RESULTS WITH SUSPICIOUS FINISH TIMES
// ============================================================================
echo "<h2>3. Resultat med misstänkta tider</h2>";

// Check for finish_time values that seem wrong
$suspiciousTimes = $db->getAll("
    SELECT r.id, r.event_id, r.cyclist_id, r.position, r.finish_time, r.points,
           e.name as event_name, e.date as event_date,
           CONCAT(ri.firstname, ' ', ri.lastname) as rider_name
    FROM results r
    JOIN events e ON r.event_id = e.id
    JOIN riders ri ON r.cyclist_id = ri.id
    WHERE r.finish_time IS NOT NULL
      AND (
          TIME_TO_SEC(r.finish_time) > 86400  -- Over 24 hours
          OR TIME_TO_SEC(r.finish_time) < 60   -- Under 1 minute (suspicious for most events)
      )
    ORDER BY e.date DESC, r.position
    LIMIT 100
");

if ($suspiciousTimes) {
    echo "<div class='warning'>";
    echo "<p><span class='count'>" . count($suspiciousTimes) . "</span> resultat med misstänkta tider (visas max 100):</p>";
    echo "<table><tr><th>Event</th><th>Datum</th><th>Åkare</th><th>Pos</th><th>Tid</th><th>Poäng</th></tr>";
    foreach ($suspiciousTimes as $row) {
        echo "<tr>";
        echo "<td><a href='/event/{$row['event_id']}'>{$row['event_name']}</a></td>";
        echo "<td>{$row['event_date']}</td>";
        echo "<td><a href='/rider/{$row['cyclist_id']}'>{$row['rider_name']}</a></td>";
        echo "<td>{$row['position']}</td>";
        echo "<td><strong>{$row['finish_time']}</strong></td>";
        echo "<td>{$row['points']}</td>";
        echo "</tr>";
    }
    echo "</table></div>";
} else {
    echo "<div class='info'>Inga misstänkta tider i finish_time hittades.</div>";
}

// ============================================================================
// 4. CHECK FOR SS (STAGE) TIME ISSUES
// ============================================================================
echo "<h2>4. Stage-tider (SS1-SS15) med problem</h2>";

// First check if SS columns exist
$hasSSColumns = false;
try {
    $columns = $db->getAll("SHOW COLUMNS FROM results LIKE 'ss%'");
    $hasSSColumns = count($columns) > 0;
} catch (Exception $e) {
    $hasSSColumns = false;
}

if ($hasSSColumns) {
    // Look for SS times that look like phone numbers or other garbage
    $suspiciousSS = $db->getAll("
        SELECT r.id, r.event_id, r.cyclist_id, r.position,
               r.ss1, r.ss2, r.ss3,
               e.name as event_name, e.date as event_date,
               CONCAT(ri.firstname, ' ', ri.lastname) as rider_name
        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN riders ri ON r.cyclist_id = ri.id
        WHERE (
            r.ss1 REGEXP '^[0-9]{10,}' OR r.ss1 REGEXP '^\+[0-9]'
            OR r.ss2 REGEXP '^[0-9]{10,}' OR r.ss2 REGEXP '^\+[0-9]'
            OR r.ss3 REGEXP '^[0-9]{10,}' OR r.ss3 REGEXP '^\+[0-9]'
            OR CAST(r.ss1 AS UNSIGNED) > 100000000
            OR CAST(r.ss2 AS UNSIGNED) > 100000000
        )
        ORDER BY e.date DESC
        LIMIT 100
    ");

    if ($suspiciousSS) {
        echo "<div class='problem'>";
        echo "<p><span class='count'>" . count($suspiciousSS) . "</span> resultat med misstänkta SS-tider:</p>";
        echo "<table><tr><th>Event</th><th>Datum</th><th>Åkare</th><th>Pos</th><th>SS1</th><th>SS2</th><th>SS3</th></tr>";
        foreach ($suspiciousSS as $row) {
            echo "<tr>";
            echo "<td><a href='/event/{$row['event_id']}'>{$row['event_name']}</a></td>";
            echo "<td>{$row['event_date']}</td>";
            echo "<td><a href='/rider/{$row['cyclist_id']}'>{$row['rider_name']}</a></td>";
            echo "<td>{$row['position']}</td>";
            echo "<td><strong>{$row['ss1']}</strong></td>";
            echo "<td><strong>{$row['ss2']}</strong></td>";
            echo "<td><strong>{$row['ss3']}</strong></td>";
            echo "</tr>";
        }
        echo "</table></div>";
    } else {
        echo "<div class='info'>Inga misstänkta SS-tider hittades.</div>";
    }
} else {
    echo "<div class='info'>SS-kolumner finns inte i results-tabellen.</div>";
}

// ============================================================================
// 4. RIDERS WITH SUSPICIOUS CLUB NAMES (direct text instead of club_id)
// ============================================================================
echo "<h2>5. Åkare med misstänkta klubbkopplingar</h2>";

// Check if there's a club_name or similar field that might have bad data
$ridersWithBadClubs = $db->getAll("
    SELECT r.id, r.firstname, r.lastname, r.club_id, c.name as club_name
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE c.name REGEXP '^[0-9]{1,2}:[0-9]{2}'
       OR c.name REGEXP '^\+[0-9]{10,}'
       OR c.name REGEXP '^[0-9]{10,}'
    ORDER BY r.lastname, r.firstname
    LIMIT 100
");

if ($ridersWithBadClubs) {
    echo "<div class='problem'>";
    echo "<p><span class='count'>" . count($ridersWithBadClubs) . "</span> åkare kopplade till misstänkta klubbar:</p>";
    echo "<table><tr><th>ID</th><th>Namn</th><th>Klubb ID</th><th>Klubbnamn</th><th>Åtgärd</th></tr>";
    foreach ($ridersWithBadClubs as $row) {
        echo "<tr>";
        echo "<td>{$row['id']}</td>";
        echo "<td><a href='/rider/{$row['id']}'>{$row['firstname']} {$row['lastname']}</a></td>";
        echo "<td>{$row['club_id']}</td>";
        echo "<td><strong>{$row['club_name']}</strong></td>";
        echo "<td><a href='/admin/riders.php?edit={$row['id']}'>Redigera</a></td>";
        echo "</tr>";
    }
    echo "</table></div>";
} else {
    echo "<div class='info'>Inga åkare med misstänkta klubbkopplingar.</div>";
}

// ============================================================================
// 5. EVENTS WITH POSITION/POINTS MISMATCH
// ============================================================================
echo "<h2>6. Event med positioner/poäng som inte stämmer</h2>";

$mismatchEvents = $db->getAll("
    SELECT e.id, e.name, e.date,
           COUNT(r.id) as result_count,
           MAX(r.position) as max_position,
           MIN(r.position) as min_position,
           MAX(r.points) as max_points,
           SUM(CASE WHEN r.position = 1 AND r.points < 100 THEN 1 ELSE 0 END) as winners_with_low_points,
           SUM(CASE WHEN r.position > 100 AND r.points > 400 THEN 1 ELSE 0 END) as high_pos_high_points
    FROM events e
    JOIN results r ON r.event_id = e.id
    WHERE r.status = 'finished'
    GROUP BY e.id
    HAVING winners_with_low_points > 0 OR high_pos_high_points > 0
    ORDER BY e.date DESC
    LIMIT 50
");

if ($mismatchEvents) {
    echo "<div class='warning'>";
    echo "<p><span class='count'>" . count($mismatchEvents) . "</span> event med misstänkt position/poäng-förhållande:</p>";
    echo "<table><tr><th>Event</th><th>Datum</th><th>Resultat</th><th>Pos (min-max)</th><th>Max poäng</th><th>Problem</th></tr>";
    foreach ($mismatchEvents as $row) {
        $problems = [];
        if ($row['winners_with_low_points'] > 0) $problems[] = "Vinnare med <100p";
        if ($row['high_pos_high_points'] > 0) $problems[] = "Pos>100 med >400p";
        echo "<tr>";
        echo "<td><a href='/event/{$row['id']}'>{$row['name']}</a></td>";
        echo "<td>{$row['date']}</td>";
        echo "<td>{$row['result_count']}</td>";
        echo "<td>{$row['min_position']} - {$row['max_position']}</td>";
        echo "<td>{$row['max_points']}</td>";
        echo "<td>" . implode(', ', $problems) . "</td>";
        echo "</tr>";
    }
    echo "</table></div>";
} else {
    echo "<div class='info'>Inga uppenbara position/poäng-problem hittades.</div>";
}

// ============================================================================
// 6. DUPLICATE RIDERS (potential bad imports)
// ============================================================================
echo "<h2>7. Potentiella dubbletter av åkare</h2>";

$duplicates = $db->getAll("
    SELECT firstname, lastname, birth_year, COUNT(*) as count,
           GROUP_CONCAT(id ORDER BY id SEPARATOR ', ') as ids
    FROM riders
    GROUP BY LOWER(firstname), LOWER(lastname), birth_year
    HAVING count > 1
    ORDER BY count DESC, lastname, firstname
    LIMIT 50
");

if ($duplicates) {
    echo "<div class='warning'>";
    echo "<p><span class='count'>" . count($duplicates) . "</span> potentiella dubbletter hittades:</p>";
    echo "<table><tr><th>Namn</th><th>Födelseår</th><th>Antal</th><th>IDs</th></tr>";
    foreach ($duplicates as $row) {
        echo "<tr>";
        echo "<td>{$row['firstname']} {$row['lastname']}</td>";
        echo "<td>{$row['birth_year']}</td>";
        echo "<td><strong>{$row['count']}</strong></td>";
        echo "<td>{$row['ids']}</td>";
        echo "</tr>";
    }
    echo "</table></div>";
} else {
    echo "<div class='info'>Inga dubbletter hittades.</div>";
}

// ============================================================================
// 7. EVENTS BY YEAR - Overview
// ============================================================================
echo "<h2>8. Resultatöversikt per år</h2>";

$yearStats = $db->getAll("
    SELECT YEAR(e.date) as year,
           COUNT(DISTINCT e.id) as event_count,
           COUNT(r.id) as result_count,
           AVG(r.points) as avg_points,
           MAX(r.points) as max_points
    FROM events e
    LEFT JOIN results r ON r.event_id = e.id
    GROUP BY YEAR(e.date)
    ORDER BY year DESC
");

echo "<div class='info'>";
echo "<table><tr><th>År</th><th>Event</th><th>Resultat</th><th>Snittpoäng</th><th>Max poäng</th></tr>";
foreach ($yearStats as $row) {
    echo "<tr>";
    echo "<td><strong>{$row['year']}</strong></td>";
    echo "<td>{$row['event_count']}</td>";
    echo "<td>{$row['result_count']}</td>";
    echo "<td>" . round($row['avg_points'] ?? 0, 1) . "</td>";
    echo "<td>{$row['max_points']}</td>";
    echo "</tr>";
}
echo "</table></div>";

// ============================================================================
// 8. SPECIFIC CHECK: Niklas Selin / Åre 2017
// ============================================================================
echo "<h2>9. Specifik kontroll: Enduro Åre-event</h2>";

$areEvents = $db->getAll("
    SELECT e.id, e.name, e.date, e.discipline,
           COUNT(r.id) as result_count
    FROM events e
    LEFT JOIN results r ON r.event_id = e.id
    WHERE e.name LIKE '%Åre%' OR e.name LIKE '%Are%'
    GROUP BY e.id
    ORDER BY e.date DESC
");

if ($areEvents) {
    echo "<div class='info'>";
    echo "<p>Åre-event hittade:</p>";
    echo "<table><tr><th>ID</th><th>Event</th><th>Datum</th><th>Disciplin</th><th>Resultat</th><th>Åtgärd</th></tr>";
    foreach ($areEvents as $row) {
        echo "<tr>";
        echo "<td>{$row['id']}</td>";
        echo "<td>{$row['name']}</td>";
        echo "<td>{$row['date']}</td>";
        echo "<td>{$row['discipline']}</td>";
        echo "<td>{$row['result_count']}</td>";
        echo "<td><a href='/admin/results.php?event_id={$row['id']}'>Visa resultat</a> | <a href='/event/{$row['id']}'>Publik sida</a></td>";
        echo "</tr>";
    }
    echo "</table></div>";
}

echo "<hr><p><em>Analys klar: " . date('Y-m-d H:i:s') . "</em></p>";
echo "</body></html>";
