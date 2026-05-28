<?php
/**
 * Backfill Ranking Snapshots
 *
 * Genererar ranking-snapshots för varje event-datum de senaste 24 månaderna.
 * Detta ger en punkt per event i ranking-grafen.
 *
 * Kör via CLI: php tools/backfill-ranking-snapshots.php
 */

// Only run from CLI
if (php_sapi_name() !== 'cli') {
    die("This script must be run from the command line.\n");
}

// Set working directory
chdir(__DIR__ . '/..');

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';

echo "=== Backfill Ranking Snapshots ===\n\n";

try {
    $db = getDB();

    // Get all unique event dates from last 24 months
    $cutoff = date('Y-m-d', strtotime('-24 months'));

    echo "Hämtar alla event-datum från $cutoff...\n";

    $eventDates = $db->getAll("
        SELECT DISTINCT DATE(e.date) as event_date
        FROM events e
        JOIN results r ON r.event_id = e.id
        WHERE e.date >= ?
          AND e.discipline IN ('ENDURO', 'DH')
          AND r.status = 'finished'
        ORDER BY e.date ASC
    ", [$cutoff]);

    echo "Hittade " . count($eventDates) . " unika event-datum.\n\n";

    if (empty($eventDates)) {
        echo "Inga events hittades.\n";
        exit(0);
    }

    // For each event date, calculate and save snapshots
    $totalSnapshots = 0;

    foreach ($eventDates as $idx => $row) {
        $eventDate = $row['event_date'];
        $progress = ($idx + 1) . "/" . count($eventDates);

        echo "[$progress] Beräknar ranking för $eventDate... ";

        // Calculate ranking data AS OF this date
        $riderData = calculateRankingDataAsOf($db, 'GRAVITY', $eventDate);

        if (empty($riderData)) {
            echo "inga riders.\n";
            continue;
        }

        // Delete existing snapshots for this date (if re-running)
        $db->query("DELETE FROM ranking_snapshots WHERE discipline = 'GRAVITY' AND snapshot_date = ?", [$eventDate]);

        // Insert snapshots
        $count = 0;
        foreach ($riderData as $rider) {
            $db->query("INSERT INTO ranking_snapshots
                (rider_id, discipline, snapshot_date, total_ranking_points,
                 points_last_12_months, points_months_13_24, events_count,
                 ranking_position, previous_position, position_change)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)", [
                $rider['rider_id'],
                'GRAVITY',
                $eventDate,
                $rider['total_ranking_points'],
                $rider['points_12'],
                $rider['points_13_24'],
                $rider['events_count'],
                $rider['ranking_position']
            ]);
            $count++;
        }

        echo "$count riders.\n";
        $totalSnapshots += $count;
    }

    echo "\n=== Klart! ===\n";
    echo "Totalt skapade snapshots: $totalSnapshots\n";

} catch (Exception $e) {
    echo "FEL: " . $e->getMessage() . "\n";
    echo $e->getTraceAsString() . "\n";
    exit(1);
}

/**
 * Calculate ranking data as of a specific date
 * This simulates what the ranking would have been on that date
 */
function calculateRankingDataAsOf($db, $discipline, $asOfDate) {
    // Calculate cutoffs based on the as-of date
    $cutoff12 = date('Y-m-d', strtotime($asOfDate . ' -12 months'));
    $cutoff24 = date('Y-m-d', strtotime($asOfDate . ' -24 months'));

    // Get events up to this date
    $events = $db->getAll("
        SELECT
            e.id as event_id,
            e.name as event_name,
            e.date as event_date,
            e.discipline,
            e.event_level,
            e.location
        FROM events e
        WHERE e.date <= ?
          AND e.date >= ?
          AND e.discipline IN ('ENDURO', 'DH')
        ORDER BY e.date DESC
    ", [$asOfDate, $cutoff24]);

    if (empty($events)) {
        return [];
    }

    // Calculate points for each rider
    $riderPoints = [];

    foreach ($events as $event) {
        // Get field size for this event
        $fieldSize = $db->getRow("
            SELECT COUNT(DISTINCT cyclist_id) as cnt
            FROM results
            WHERE event_id = ? AND status = 'finished'
        ", [$event['event_id']]);
        $participantCount = $fieldSize['cnt'] ?? 0;

        // Get results for this event
        $results = $db->getAll("
            SELECT
                r.cyclist_id as rider_id,
                r.position,
                r.points as original_points
            FROM results r
            WHERE r.event_id = ? AND r.status = 'finished' AND r.position > 0
        ", [$event['event_id']]);

        foreach ($results as $result) {
            $riderId = $result['rider_id'];

            if (!isset($riderPoints[$riderId])) {
                $riderPoints[$riderId] = [
                    'rider_id' => $riderId,
                    'points_12' => 0,
                    'points_13_24' => 0,
                    'events_count' => 0
                ];
            }

            // Calculate weighted points
            $basePoints = $result['original_points'] ?? 0;

            // Field size multiplier
            $fieldMultiplier = calculateFieldMultiplier($participantCount);

            // Event level multiplier
            $levelMultiplier = getEventLevelMultiplier($event['event_level'] ?? 'local');

            // Time decay - based on whether event is in last 12 months or 13-24 months
            $eventDateObj = strtotime($event['event_date']);
            $cutoff12Obj = strtotime($cutoff12);

            $weightedPoints = $basePoints * $fieldMultiplier * $levelMultiplier;

            if ($eventDateObj >= $cutoff12Obj) {
                // Last 12 months - full points
                $riderPoints[$riderId]['points_12'] += $weightedPoints;
            } else {
                // 13-24 months - 50% decay
                $riderPoints[$riderId]['points_13_24'] += $weightedPoints * 0.5;
            }

            $riderPoints[$riderId]['events_count']++;
        }
    }

    // Calculate total points and rank
    $rankings = [];
    foreach ($riderPoints as $riderId => $data) {
        $totalPoints = $data['points_12'] + $data['points_13_24'];

        if ($totalPoints > 0) {
            $rankings[] = [
                'rider_id' => $riderId,
                'total_ranking_points' => $totalPoints,
                'points_12' => $data['points_12'],
                'points_13_24' => $data['points_13_24'],
                'events_count' => $data['events_count'],
                'ranking_position' => 0
            ];
        }
    }

    // Sort by total points (descending)
    usort($rankings, function($a, $b) {
        return $b['total_ranking_points'] <=> $a['total_ranking_points'];
    });

    // Assign positions
    foreach ($rankings as $idx => &$rider) {
        $rider['ranking_position'] = $idx + 1;
    }

    return $rankings;
}

/**
 * Calculate field size multiplier
 */
function calculateFieldMultiplier($participantCount) {
    if ($participantCount >= 50) return 1.0;
    if ($participantCount >= 40) return 0.95;
    if ($participantCount >= 30) return 0.90;
    if ($participantCount >= 20) return 0.85;
    if ($participantCount >= 15) return 0.80;
    if ($participantCount >= 10) return 0.75;
    if ($participantCount >= 5) return 0.60;
    return 0.50;
}

/**
 * Get event level multiplier
 */
function getEventLevelMultiplier($eventLevel) {
    $multipliers = [
        'world_cup' => 1.5,
        'world_series' => 1.4,
        'ews' => 1.3,
        'national_championship' => 1.25,
        'sm' => 1.25,
        'national' => 1.1,
        'regional' => 1.0,
        'local' => 0.9
    ];

    return $multipliers[strtolower($eventLevel)] ?? 1.0;
}
