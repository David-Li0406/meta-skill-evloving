<?php
/**
 * TheHUB Ranking System - Complete Implementation
 *
 * 24-month rolling ranking with:
 * - Field size weighting (more riders = higher value)
 * - Time decay (0-12mo = 100%, 13-24mo = 50%, 25+ = 0%)
 * - Event level multiplier (national = 100%, sportmotion = 50%)
 * - Both individual rider AND club rankings
 *
 * Club Ranking: Per event/class, best rider per club = 100%, second best = 50%, others = 0%
 */

// Valid disciplines
if (!defined('RANKING_DISCIPLINES')) {
    define('RANKING_DISCIPLINES', ['ENDURO', 'DH', 'GRAVITY']);
}

/**
 * Get default field size multipliers (1-15+)
 */
function getDefaultFieldMultipliers() {
    return [
        1 => 0.75, 2 => 0.77, 3 => 0.79, 4 => 0.81, 5 => 0.83,
        6 => 0.85, 7 => 0.86, 8 => 0.87, 9 => 0.88, 10 => 0.89,
        11 => 0.90, 12 => 0.91, 13 => 0.92, 14 => 0.93, 15 => 1.00
    ];
}

/**
 * Get default time decay settings
 */
function getDefaultTimeDecay() {
    return [
        'months_1_12' => 1.00,
        'months_13_24' => 0.50,
        'months_25_plus' => 0.00
    ];
}

/**
 * Get default event level multipliers
 */
function getDefaultEventLevelMultipliers() {
    return [
        'national' => 1.00,
        'sportmotion' => 0.50
    ];
}

/**
 * Get field multipliers from database
 */
function getRankingFieldMultipliers($db) {
    try {
        $result = $db->getRow("SELECT setting_value FROM ranking_settings WHERE setting_key = 'field_multipliers'");
        if ($result && $result['setting_value']) {
            $decoded = json_decode($result['setting_value'], true);
            if ($decoded) {
                // Convert string keys to int
                $multipliers = [];
                foreach ($decoded as $k => $v) {
                    $multipliers[(int)$k] = (float)$v;
                }
                return $multipliers;
            }
        }
    } catch (Exception $e) {
        // Fall through to default
    }
    return getDefaultFieldMultipliers();
}

/**
 * Get time decay settings from database
 */
function getRankingTimeDecay($db) {
    try {
        $result = $db->getRow("SELECT setting_value FROM ranking_settings WHERE setting_key = 'time_decay'");
        if ($result && $result['setting_value']) {
            $decoded = json_decode($result['setting_value'], true);
            if ($decoded) return $decoded;
        }
    } catch (Exception $e) {}
    return getDefaultTimeDecay();
}

/**
 * Get event level multipliers from database
 */
function getEventLevelMultipliers($db) {
    try {
        $result = $db->getRow("SELECT setting_value FROM ranking_settings WHERE setting_key = 'event_level_multipliers'");
        if ($result && $result['setting_value']) {
            $decoded = json_decode($result['setting_value'], true);
            if ($decoded) return $decoded;
        }
    } catch (Exception $e) {}
    return getDefaultEventLevelMultipliers();
}

/**
 * Save field multipliers to database
 */
function saveFieldMultipliers($db, $multipliers) {
    $json = json_encode($multipliers);
    $db->query("INSERT INTO ranking_settings (setting_key, setting_value, description)
                VALUES ('field_multipliers', ?, 'Fältstorlek-multiplikatorer')
                ON DUPLICATE KEY UPDATE setting_value = ?", [$json, $json]);
}

/**
 * Save time decay to database
 */
function saveTimeDecay($db, $timeDecay) {
    $json = json_encode($timeDecay);
    $db->query("INSERT INTO ranking_settings (setting_key, setting_value, description)
                VALUES ('time_decay', ?, 'Tidsviktning')
                ON DUPLICATE KEY UPDATE setting_value = ?", [$json, $json]);
}

/**
 * Save event level multipliers to database
 */
function saveEventLevelMultipliers($db, $eventLevel) {
    $json = json_encode($eventLevel);
    $db->query("INSERT INTO ranking_settings (setting_key, setting_value, description)
                VALUES ('event_level_multipliers', ?, 'Eventtyp-multiplikatorer')
                ON DUPLICATE KEY UPDATE setting_value = ?", [$json, $json]);
}

/**
 * Get field multiplier for specific field size
 */
function getFieldMultiplier($fieldSize, $multipliers) {
    $fieldSize = max(1, (int)$fieldSize);
    if ($fieldSize >= 15) return $multipliers[15] ?? 1.00;
    return $multipliers[$fieldSize] ?? 0.75;
}

/**
 * Check if ranking tables exist
 */
function rankingTablesExist($db) {
    try {
        $tables = $db->getAll("SHOW TABLES LIKE 'ranking_snapshots'");
        return !empty($tables);
    } catch (Exception $e) {
        return false;
    }
}

/**
 * Get discipline display name
 */
function getDisciplineDisplayName($discipline) {
    $names = [
        'ENDURO' => 'Enduro',
        'DH' => 'Downhill',
        'GRAVITY' => 'Gravity'
    ];
    return $names[$discipline] ?? $discipline;
}

/**
 * Get the ranking reference date - first day of month AFTER the latest event
 *
 * IMPORTANT: This now returns the SAME date for all disciplines to ensure
 * consistent time decay calculations. Previously, each discipline had its own
 * reference date which caused GRAVITY (ENDURO+DH) to show different points
 * than the sum of ENDURO and DH rankings.
 *
 * The reference date is: first day of the month after the latest event with results
 * This ensures a consistent 24-month rolling window.
 */
function getLatestEventDateWithResults($db, $discipline = 'GRAVITY') {
    // ALWAYS use the latest event across ALL disciplines (ENDURO + DH)
    // This ensures consistent time decay calculations regardless of which
    // discipline ranking we're calculating
    $result = $db->getRow("
        SELECT MAX(e.date) as latest_date
        FROM events e
        JOIN results r ON r.event_id = e.id
        WHERE r.status = 'finished'
        AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0)
        AND e.discipline IN ('ENDURO', 'DH')
    ");

    $latestDate = $result['latest_date'] ?? date('Y-m-d');

    // Calculate first day of the month AFTER the latest event
    // This is the reference point for time decay calculations
    $firstOfNextMonth = date('Y-m-01', strtotime($latestDate . ' +1 month'));

    return $firstOfNextMonth;
}

/**
 * Calculate ranking data on-the-fly from results
 * Returns array of riders with their ranking points
 *
 * IMPORTANT: Ranking is calculated relative to the latest event with results,
 * NOT relative to today's date. This ensures correct time decay even when
 * viewing historical data.
 */
function calculateRankingData($db, $discipline = 'GRAVITY', $debug = false) {
    // Use latest event date as reference instead of today
    $referenceDate = getLatestEventDateWithResults($db, $discipline);
    $cutoffDate = date('Y-m-d', strtotime($referenceDate . ' -24 months'));

    $fieldMultipliers = getRankingFieldMultipliers($db);
    $eventLevelMultipliers = getEventLevelMultipliers($db);
    $timeDecay = getRankingTimeDecay($db);

    // Build discipline filter
    $disciplineFilter = '';
    $params = [$cutoffDate];

    if ($discipline === 'GRAVITY') {
        $disciplineFilter = "AND e.discipline IN ('ENDURO', 'DH')";
    } elseif ($discipline) {
        $disciplineFilter = 'AND e.discipline = ?';
        $params[] = $discipline;
    }

    // Get all qualifying results
    $results = $db->getAll("
        SELECT
            r.cyclist_id as rider_id,
            r.event_id,
            r.class_id,
            COALESCE(
                CASE
                    WHEN COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0
                    THEN COALESCE(r.run_1_points, 0) + COALESCE(r.run_2_points, 0)
                    ELSE r.points
                END,
                r.points
            ) as original_points,
            e.date as event_date,
            e.discipline,
            COALESCE(e.event_level, 'national') as event_level
        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN classes cl ON r.class_id = cl.id
        WHERE r.status = 'finished'
        AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0)
        AND e.date >= ?
        {$disciplineFilter}
        AND COALESCE(cl.series_eligible, 1) = 1
        AND COALESCE(cl.awards_points, 1) = 1
    ", $params);

    if (empty($results)) return [];

    // Calculate field sizes per event/class
    $fieldSizes = [];
    foreach ($results as $result) {
        $key = $result['event_id'] . '_' . $result['class_id'];
        $fieldSizes[$key] = ($fieldSizes[$key] ?? 0) + 1;
    }

    // Get rider info
    $riderIds = array_values(array_unique(array_column($results, 'rider_id')));
    $riderInfo = [];
    if (!empty($riderIds)) {
        $placeholders = implode(',', array_fill(0, count($riderIds), '?'));
        $riders = $db->getAll("
            SELECT r.id, r.firstname, r.lastname, r.club_id, c.name as club_name
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.id IN ($placeholders)
        ", $riderIds);
        foreach ($riders as $rider) {
            $riderInfo[$rider['id']] = $rider;
        }
    }

    // Calculate points per rider
    $riderData = [];
    $refDateObj = new DateTime($referenceDate);

    foreach ($results as $result) {
        $riderId = $result['rider_id'];
        $key = $result['event_id'] . '_' . $result['class_id'];
        $fieldSize = $fieldSizes[$key] ?? 1;

        // Calculate multipliers
        $fieldMult = getFieldMultiplier($fieldSize, $fieldMultipliers);
        $eventLevelMult = $eventLevelMultipliers[$result['event_level']] ?? 1.00;

        // Time decay relative to latest event date (not today)
        $eventDate = new DateTime($result['event_date']);
        $monthsDiff = ($refDateObj->format('Y') - $eventDate->format('Y')) * 12 +
                      ($refDateObj->format('n') - $eventDate->format('n'));

        if ($monthsDiff < 12) {
            $timeMult = $timeDecay['months_1_12'];
        } elseif ($monthsDiff < 24) {
            $timeMult = $timeDecay['months_13_24'];
        } else {
            $timeMult = $timeDecay['months_25_plus'];
        }

        // Calculate ranking points
        $basePoints = (float)$result['original_points'];
        $rankingPoints = $basePoints * $fieldMult * $eventLevelMult;
        $weightedPoints = $rankingPoints * $timeMult;

        // Aggregate per rider
        if (!isset($riderData[$riderId])) {
            $info = $riderInfo[$riderId] ?? [];
            $riderData[$riderId] = [
                'rider_id' => $riderId,
                'firstname' => $info['firstname'] ?? '',
                'lastname' => $info['lastname'] ?? '',
                'club_id' => $info['club_id'] ?? null,
                'club_name' => $info['club_name'] ?? '',
                'total_ranking_points' => 0,
                'points_12' => 0,
                'points_13_24' => 0,
                'events_count' => 0
            ];
        }

        $riderData[$riderId]['total_ranking_points'] += $weightedPoints;
        $riderData[$riderId]['events_count']++;

        if ($monthsDiff < 12) {
            $riderData[$riderId]['points_12'] += $rankingPoints;
        } else {
            $riderData[$riderId]['points_13_24'] += $rankingPoints;
        }
    }

    // Sort by total points
    usort($riderData, function($a, $b) {
        return $b['total_ranking_points'] <=> $a['total_ranking_points'];
    });

    // Add ranking positions
    $position = 1;
    $prevPoints = null;
    $actualPosition = 1;

    foreach ($riderData as &$rider) {
        if ($prevPoints !== null && $rider['total_ranking_points'] < $prevPoints) {
            $position = $actualPosition;
        }
        $rider['ranking_position'] = $position;
        $prevPoints = $rider['total_ranking_points'];
        $actualPosition++;
    }

    return array_values($riderData);
}

/**
 * Calculate ranking data as of a specific date (for backfill/historical snapshots)
 * Same logic as calculateRankingData() but calculates relative to asOfDate instead of today
 */
function calculateRankingDataAsOf($db, $discipline = 'GRAVITY', $asOfDate = null) {
    if (!$asOfDate) {
        $asOfDate = date('Y-m-d');
    }

    $cutoffDate = date('Y-m-d', strtotime($asOfDate . ' -24 months'));

    $fieldMultipliers = getRankingFieldMultipliers($db);
    $eventLevelMultipliers = getEventLevelMultipliers($db);
    $timeDecay = getRankingTimeDecay($db);

    // Build discipline filter
    $disciplineFilter = '';
    $params = [$asOfDate, $cutoffDate];

    if ($discipline === 'GRAVITY') {
        $disciplineFilter = "AND e.discipline IN ('ENDURO', 'DH')";
    } elseif ($discipline) {
        $disciplineFilter = 'AND e.discipline = ?';
        $params[] = $discipline;
    }

    // Get all qualifying results up to asOfDate
    $results = $db->getAll("
        SELECT
            r.cyclist_id as rider_id,
            r.event_id,
            r.class_id,
            COALESCE(
                CASE
                    WHEN COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0
                    THEN COALESCE(r.run_1_points, 0) + COALESCE(r.run_2_points, 0)
                    ELSE r.points
                END,
                r.points
            ) as original_points,
            e.date as event_date,
            e.discipline,
            COALESCE(e.event_level, 'national') as event_level
        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN classes cl ON r.class_id = cl.id
        WHERE r.status = 'finished'
        AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0)
        AND e.date <= ?
        AND e.date >= ?
        {$disciplineFilter}
        AND COALESCE(cl.series_eligible, 1) = 1
        AND COALESCE(cl.awards_points, 1) = 1
    ", $params);

    if (empty($results)) return [];

    // Calculate field sizes per event/class
    $fieldSizes = [];
    foreach ($results as $result) {
        $key = $result['event_id'] . '_' . $result['class_id'];
        $fieldSizes[$key] = ($fieldSizes[$key] ?? 0) + 1;
    }

    // Calculate points per rider
    $riderData = [];
    $referenceDate = new DateTime($asOfDate);

    foreach ($results as $result) {
        $riderId = $result['rider_id'];
        $key = $result['event_id'] . '_' . $result['class_id'];
        $fieldSize = $fieldSizes[$key] ?? 1;

        // Calculate multipliers
        $fieldMult = getFieldMultiplier($fieldSize, $fieldMultipliers);
        $eventLevelMult = $eventLevelMultipliers[$result['event_level']] ?? 1.00;

        // Time decay relative to asOfDate
        $eventDate = new DateTime($result['event_date']);
        $monthsDiff = ($referenceDate->format('Y') - $eventDate->format('Y')) * 12 +
                      ($referenceDate->format('n') - $eventDate->format('n'));

        if ($monthsDiff < 12) {
            $timeMult = $timeDecay['months_1_12'];
        } elseif ($monthsDiff < 24) {
            $timeMult = $timeDecay['months_13_24'];
        } else {
            $timeMult = $timeDecay['months_25_plus'];
        }

        // Calculate ranking points
        $basePoints = (float)$result['original_points'];
        $rankingPoints = $basePoints * $fieldMult * $eventLevelMult;
        $weightedPoints = $rankingPoints * $timeMult;

        // Aggregate per rider
        if (!isset($riderData[$riderId])) {
            $riderData[$riderId] = [
                'rider_id' => $riderId,
                'total_ranking_points' => 0,
                'points_12' => 0,
                'points_13_24' => 0,
                'events_count' => 0
            ];
        }

        $riderData[$riderId]['total_ranking_points'] += $weightedPoints;
        $riderData[$riderId]['events_count']++;

        if ($monthsDiff < 12) {
            $riderData[$riderId]['points_12'] += $rankingPoints;
        } else {
            $riderData[$riderId]['points_13_24'] += $rankingPoints;
        }
    }

    // Sort by total points
    usort($riderData, function($a, $b) {
        return $b['total_ranking_points'] <=> $a['total_ranking_points'];
    });

    // Add ranking positions
    $position = 1;
    $prevPoints = null;
    $actualPosition = 1;

    foreach ($riderData as &$rider) {
        if ($prevPoints !== null && $rider['total_ranking_points'] < $prevPoints) {
            $position = $actualPosition;
        }
        $rider['ranking_position'] = $position;
        $prevPoints = $rider['total_ranking_points'];
        $actualPosition++;
    }

    return array_values($riderData);
}

/**
 * Calculate CLUB ranking data - GLOBAL 24-month rolling
 *
 * Per event/class: Best rider per club = 100%, second best = 50%, others = 0%
 * Same time decay as individual ranking (0-12mo = 100%, 13-24mo = 50%)
 * Same field size weighting
 */
function calculateClubRankingData($db, $discipline = 'GRAVITY', $debug = false) {
    // Use latest event date as reference instead of today
    $referenceDate = getLatestEventDateWithResults($db, $discipline);
    $cutoffDate = date('Y-m-d', strtotime($referenceDate . ' -24 months'));

    $fieldMultipliers = getRankingFieldMultipliers($db);
    $eventLevelMultipliers = getEventLevelMultipliers($db);
    $timeDecay = getRankingTimeDecay($db);

    // Build discipline filter
    $disciplineFilter = '';
    $params = [$cutoffDate];

    if ($discipline === 'GRAVITY') {
        $disciplineFilter = "AND e.discipline IN ('ENDURO', 'DH')";
    } elseif ($discipline) {
        $disciplineFilter = 'AND e.discipline = ?';
        $params[] = $discipline;
    }

    // Get all qualifying results with club info, sorted by points for club position calculation
    // Priority for club assignment:
    // 1. r.club_id (explicitly set in results table)
    // 2. rider_club_seasons for the event year (historical club membership)
    // 3. rd.club_id (rider's current club as last fallback)
    $results = $db->getAll("
        SELECT
            r.cyclist_id as rider_id,
            r.event_id,
            r.class_id,
            COALESCE(r.club_id, rcs.club_id, rd.club_id) as club_id,
            COALESCE(c1.name, c2.name, c3.name) as club_name,
            COALESCE(
                CASE
                    WHEN COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0
                    THEN COALESCE(r.run_1_points, 0) + COALESCE(r.run_2_points, 0)
                    ELSE r.points
                END,
                r.points
            ) as original_points,
            e.date as event_date,
            e.discipline,
            COALESCE(e.event_level, 'national') as event_level
        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN classes cl ON r.class_id = cl.id
        JOIN riders rd ON r.cyclist_id = rd.id
        LEFT JOIN rider_club_seasons rcs ON rcs.rider_id = rd.id AND rcs.season_year = YEAR(e.date)
        LEFT JOIN clubs c1 ON r.club_id = c1.id
        LEFT JOIN clubs c2 ON rcs.club_id = c2.id
        LEFT JOIN clubs c3 ON rd.club_id = c3.id
        WHERE r.status = 'finished'
        AND COALESCE(r.club_id, rcs.club_id, rd.club_id) IS NOT NULL
        AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0)
        AND e.date >= ?
        {$disciplineFilter}
        AND COALESCE(cl.series_eligible, 1) = 1
        AND COALESCE(cl.awards_points, 1) = 1
        ORDER BY e.id, cl.id, COALESCE(r.club_id, rcs.club_id, rd.club_id), original_points DESC
    ", $params);

    if (empty($results)) return [];

    // Calculate field sizes per event/class
    $fieldSizes = [];
    foreach ($results as $result) {
        $key = $result['event_id'] . '_' . $result['class_id'];
        $fieldSizes[$key] = ($fieldSizes[$key] ?? 0) + 1;
    }

    $refDateObj = new DateTime($referenceDate);
    $clubData = [];

    // Group results by event/class/club to determine 1st and 2nd best
    $eventClassClub = [];
    foreach ($results as $result) {
        $key = $result['event_id'] . '_' . $result['class_id'] . '_' . $result['club_id'];
        if (!isset($eventClassClub[$key])) {
            $eventClassClub[$key] = [];
        }
        $eventClassClub[$key][] = $result;
    }

    // Process each event/class/club group
    foreach ($eventClassClub as $key => $riders) {
        // Riders are already sorted by points DESC from query
        $rank = 1;
        foreach ($riders as $rider) {
            // Only 1st (100%) and 2nd (50%) count
            if ($rank > 2) break;

            $clubId = $rider['club_id'];
            $fieldKey = $rider['event_id'] . '_' . $rider['class_id'];
            $fieldSize = $fieldSizes[$fieldKey] ?? 1;

            // Calculate multipliers
            $fieldMult = getFieldMultiplier($fieldSize, $fieldMultipliers);
            $eventLevelMult = $eventLevelMultipliers[$rider['event_level']] ?? 1.00;

            // Club position multiplier: 1st = 100%, 2nd = 50%
            $clubPositionMult = ($rank === 1) ? 1.00 : 0.50;

            // Time decay relative to latest event date (not today)
            $eventDate = new DateTime($rider['event_date']);
            $monthsDiff = ($refDateObj->format('Y') - $eventDate->format('Y')) * 12 +
                          ($refDateObj->format('n') - $eventDate->format('n'));

            if ($monthsDiff < 12) {
                $timeMult = $timeDecay['months_1_12'];
            } elseif ($monthsDiff < 24) {
                $timeMult = $timeDecay['months_13_24'];
            } else {
                $timeMult = $timeDecay['months_25_plus'];
            }

            // Calculate ranking points for this rider's contribution to club
            $basePoints = (float)$rider['original_points'];
            $rankingPoints = $basePoints * $fieldMult * $eventLevelMult * $clubPositionMult;
            $weightedPoints = $rankingPoints * $timeMult;

            // Aggregate to club
            if (!isset($clubData[$clubId])) {
                $clubData[$clubId] = [
                    'club_id' => $clubId,
                    'club_name' => $rider['club_name'],
                    'total_ranking_points' => 0,
                    'points_12' => 0,
                    'points_13_24' => 0,
                    'riders_count' => 0,
                    'events_count' => 0,
                    'scoring_riders' => [] // Track unique riders who scored
                ];
            }

            $clubData[$clubId]['total_ranking_points'] += $weightedPoints;
            $clubData[$clubId]['events_count']++;

            if ($monthsDiff < 12) {
                $clubData[$clubId]['points_12'] += $rankingPoints;
            } else {
                $clubData[$clubId]['points_13_24'] += $rankingPoints;
            }

            // Track unique scoring riders
            if (!in_array($rider['rider_id'], $clubData[$clubId]['scoring_riders'])) {
                $clubData[$clubId]['scoring_riders'][] = $rider['rider_id'];
            }

            $rank++;
        }
    }

    // Convert scoring_riders array to count
    foreach ($clubData as &$club) {
        $club['riders_count'] = count($club['scoring_riders']);
        unset($club['scoring_riders']);
    }

    // Sort by total points
    usort($clubData, function($a, $b) {
        return $b['total_ranking_points'] <=> $a['total_ranking_points'];
    });

    // Add ranking positions
    $position = 1;
    $prevPoints = null;
    $actualPosition = 1;

    foreach ($clubData as &$club) {
        if ($prevPoints !== null && $club['total_ranking_points'] < $prevPoints) {
            $position = $actualPosition;
        }
        $club['ranking_position'] = $position;
        $prevPoints = $club['total_ranking_points'];
        $actualPosition++;
    }

    return array_values($clubData);
}

/**
 * Calculate CLUB ranking data as of a specific date (for backfill/historical snapshots)
 * Same logic as calculateClubRankingData() but calculates relative to asOfDate instead of today
 */
function calculateClubRankingDataAsOf($db, $discipline = 'GRAVITY', $asOfDate = null) {
    if (!$asOfDate) {
        $asOfDate = date('Y-m-d');
    }

    $cutoffDate = date('Y-m-d', strtotime($asOfDate . ' -24 months'));

    $fieldMultipliers = getRankingFieldMultipliers($db);
    $eventLevelMultipliers = getEventLevelMultipliers($db);
    $timeDecay = getRankingTimeDecay($db);

    // Build discipline filter
    $disciplineFilter = '';
    $params = [$asOfDate, $cutoffDate];

    if ($discipline === 'GRAVITY') {
        $disciplineFilter = "AND e.discipline IN ('ENDURO', 'DH')";
    } elseif ($discipline) {
        $disciplineFilter = 'AND e.discipline = ?';
        $params[] = $discipline;
    }

    // Get all qualifying results with club info up to asOfDate
    // Priority for club assignment:
    // 1. r.club_id (explicitly set in results table)
    // 2. rider_club_seasons for the event year (historical club membership)
    // 3. rd.club_id (rider's current club as last fallback)
    $results = $db->getAll("
        SELECT
            r.cyclist_id as rider_id,
            r.event_id,
            r.class_id,
            COALESCE(r.club_id, rcs.club_id, rd.club_id) as club_id,
            COALESCE(c1.name, c2.name, c3.name) as club_name,
            COALESCE(
                CASE
                    WHEN COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0
                    THEN COALESCE(r.run_1_points, 0) + COALESCE(r.run_2_points, 0)
                    ELSE r.points
                END,
                r.points
            ) as original_points,
            e.date as event_date,
            e.discipline,
            COALESCE(e.event_level, 'national') as event_level
        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN classes cl ON r.class_id = cl.id
        JOIN riders rd ON r.cyclist_id = rd.id
        LEFT JOIN rider_club_seasons rcs ON rcs.rider_id = rd.id AND rcs.season_year = YEAR(e.date)
        LEFT JOIN clubs c1 ON r.club_id = c1.id
        LEFT JOIN clubs c2 ON rcs.club_id = c2.id
        LEFT JOIN clubs c3 ON rd.club_id = c3.id
        WHERE r.status = 'finished'
        AND COALESCE(r.club_id, rcs.club_id, rd.club_id) IS NOT NULL
        AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0)
        AND e.date <= ?
        AND e.date >= ?
        {$disciplineFilter}
        AND COALESCE(cl.series_eligible, 1) = 1
        AND COALESCE(cl.awards_points, 1) = 1
        ORDER BY e.id, cl.id, COALESCE(r.club_id, rcs.club_id, rd.club_id), original_points DESC
    ", $params);

    if (empty($results)) return [];

    // Calculate field sizes per event/class
    $fieldSizes = [];
    foreach ($results as $result) {
        $key = $result['event_id'] . '_' . $result['class_id'];
        $fieldSizes[$key] = ($fieldSizes[$key] ?? 0) + 1;
    }

    $referenceDate = new DateTime($asOfDate);
    $clubData = [];

    // Group results by event/class/club to determine 1st and 2nd best
    $eventClassClub = [];
    foreach ($results as $result) {
        $key = $result['event_id'] . '_' . $result['class_id'] . '_' . $result['club_id'];
        if (!isset($eventClassClub[$key])) {
            $eventClassClub[$key] = [];
        }
        $eventClassClub[$key][] = $result;
    }

    // Process each event/class/club group
    foreach ($eventClassClub as $key => $riders) {
        $rank = 1;
        foreach ($riders as $rider) {
            if ($rank > 2) break;

            $clubId = $rider['club_id'];
            $fieldKey = $rider['event_id'] . '_' . $rider['class_id'];
            $fieldSize = $fieldSizes[$fieldKey] ?? 1;

            $fieldMult = getFieldMultiplier($fieldSize, $fieldMultipliers);
            $eventLevelMult = $eventLevelMultipliers[$rider['event_level']] ?? 1.00;
            $clubPositionMult = ($rank === 1) ? 1.00 : 0.50;

            // Time decay relative to asOfDate
            $eventDate = new DateTime($rider['event_date']);
            $monthsDiff = ($referenceDate->format('Y') - $eventDate->format('Y')) * 12 +
                          ($referenceDate->format('n') - $eventDate->format('n'));

            if ($monthsDiff < 12) {
                $timeMult = $timeDecay['months_1_12'];
            } elseif ($monthsDiff < 24) {
                $timeMult = $timeDecay['months_13_24'];
            } else {
                $timeMult = $timeDecay['months_25_plus'];
            }

            $basePoints = (float)$rider['original_points'];
            $rankingPoints = $basePoints * $fieldMult * $eventLevelMult * $clubPositionMult;
            $weightedPoints = $rankingPoints * $timeMult;

            if (!isset($clubData[$clubId])) {
                $clubData[$clubId] = [
                    'club_id' => $clubId,
                    'club_name' => $rider['club_name'],
                    'total_ranking_points' => 0,
                    'points_12' => 0,
                    'points_13_24' => 0,
                    'riders_count' => 0,
                    'events_count' => 0,
                    'scoring_riders' => []
                ];
            }

            $clubData[$clubId]['total_ranking_points'] += $weightedPoints;
            $clubData[$clubId]['events_count']++;

            if ($monthsDiff < 12) {
                $clubData[$clubId]['points_12'] += $rankingPoints;
            } else {
                $clubData[$clubId]['points_13_24'] += $rankingPoints;
            }

            if (!in_array($rider['rider_id'], $clubData[$clubId]['scoring_riders'])) {
                $clubData[$clubId]['scoring_riders'][] = $rider['rider_id'];
            }

            $rank++;
        }
    }

    // Convert scoring_riders array to count
    foreach ($clubData as &$club) {
        $club['riders_count'] = count($club['scoring_riders']);
        unset($club['scoring_riders']);
    }

    // Sort by total points
    usort($clubData, function($a, $b) {
        return $b['total_ranking_points'] <=> $a['total_ranking_points'];
    });

    // Add ranking positions
    $position = 1;
    $prevPoints = null;
    $actualPosition = 1;

    foreach ($clubData as &$club) {
        if ($prevPoints !== null && $club['total_ranking_points'] < $prevPoints) {
            $position = $actualPosition;
        }
        $club['ranking_position'] = $position;
        $prevPoints = $club['total_ranking_points'];
        $actualPosition++;
    }

    return array_values($clubData);
}

/**
 * Save ranking snapshots for a specific discipline
 */
function saveRankingSnapshots($db, $discipline, $debug = false) {
    // Use latest event date as snapshot date (not today)
    $snapshotDate = getLatestEventDateWithResults($db, $discipline);

    // Get previous snapshot for position changes
    $previousSnapshot = $db->getAll("
        SELECT rider_id, ranking_position FROM ranking_snapshots
        WHERE discipline = ? AND snapshot_date = (
            SELECT MAX(snapshot_date) FROM ranking_snapshots
            WHERE discipline = ? AND snapshot_date < ?
        )
    ", [$discipline, $discipline, $snapshotDate]);

    $previousPositions = [];
    foreach ($previousSnapshot as $row) {
        $previousPositions[$row['rider_id']] = $row['ranking_position'];
    }

    // Calculate current ranking
    $riderData = calculateRankingData($db, $discipline, $debug);

    // Delete old snapshot for today (if re-running)
    $db->query("DELETE FROM ranking_snapshots WHERE discipline = ? AND snapshot_date = ?",
               [$discipline, $snapshotDate]);

    $count = 0;
    foreach ($riderData as $rider) {
        $prevPos = $previousPositions[$rider['rider_id']] ?? null;
        $posChange = $prevPos !== null ? ($prevPos - $rider['ranking_position']) : null;

        $db->query("INSERT INTO ranking_snapshots
            (rider_id, discipline, snapshot_date, total_ranking_points,
             points_last_12_months, points_months_13_24, events_count,
             ranking_position, previous_position, position_change)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            $rider['rider_id'],
            $discipline,
            $snapshotDate,
            $rider['total_ranking_points'],
            $rider['points_12'],
            $rider['points_13_24'],
            $rider['events_count'],
            $rider['ranking_position'],
            $prevPos,
            $posChange
        ]);
        $count++;
    }

    return $count;
}

/**
 * Save CLUB ranking snapshots for a specific discipline
 */
function saveClubRankingSnapshots($db, $discipline, $debug = false) {
    // Use latest event date as snapshot date (not today)
    $snapshotDate = getLatestEventDateWithResults($db, $discipline);

    // Get previous snapshot
    $previousSnapshot = $db->getAll("
        SELECT club_id, ranking_position FROM club_ranking_snapshots
        WHERE discipline = ? AND snapshot_date = (
            SELECT MAX(snapshot_date) FROM club_ranking_snapshots
            WHERE discipline = ? AND snapshot_date < ?
        )
    ", [$discipline, $discipline, $snapshotDate]);

    $previousPositions = [];
    foreach ($previousSnapshot as $row) {
        $previousPositions[$row['club_id']] = $row['ranking_position'];
    }

    // Calculate current club ranking
    $clubData = calculateClubRankingData($db, $discipline, $debug);

    // Delete old snapshot for today
    $db->query("DELETE FROM club_ranking_snapshots WHERE discipline = ? AND snapshot_date = ?",
               [$discipline, $snapshotDate]);

    $count = 0;
    foreach ($clubData as $club) {
        $prevPos = $previousPositions[$club['club_id']] ?? null;
        $posChange = $prevPos !== null ? ($prevPos - $club['ranking_position']) : null;

        $db->query("INSERT INTO club_ranking_snapshots
            (club_id, discipline, snapshot_date, total_ranking_points,
             points_last_12_months, points_months_13_24, riders_count, events_count,
             ranking_position, previous_position, position_change)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            $club['club_id'],
            $discipline,
            $snapshotDate,
            $club['total_ranking_points'],
            $club['points_12'],
            $club['points_13_24'],
            $club['riders_count'],
            $club['events_count'],
            $club['ranking_position'],
            $prevPos,
            $posChange
        ]);
        $count++;
    }

    return $count;
}

/**
 * Run full ranking update for all disciplines
 * Updates both rider and club rankings
 */
function runFullRankingUpdate($db, $debug = false) {
    $startTime = microtime(true);
    $stats = [
        'enduro' => ['riders' => 0, 'clubs' => 0],
        'dh' => ['riders' => 0, 'clubs' => 0],
        'gravity' => ['riders' => 0, 'clubs' => 0],
        'monthly_snapshots' => 0
    ];

    foreach (['ENDURO', 'DH', 'GRAVITY'] as $discipline) {
        $key = strtolower($discipline);

        if ($debug) echo "<p>Calculating $discipline riders...</p>";
        $stats[$key]['riders'] = saveRankingSnapshots($db, $discipline, $debug);

        if ($debug) echo "<p>Calculating $discipline clubs...</p>";
        $stats[$key]['clubs'] = saveClubRankingSnapshots($db, $discipline, $debug);
    }

    // Also create monthly snapshots going back 24 months
    if ($debug) echo "<p>Creating monthly historical snapshots...</p>";
    $stats['monthly_snapshots'] = createMonthlyRankingSnapshots($db, $debug);

    $stats['total_time'] = round(microtime(true) - $startTime, 2);

    // Save last calculation info
    $db->query("INSERT INTO ranking_settings (setting_key, setting_value, description)
                VALUES ('last_calculation', ?, 'Senaste beräkning')
                ON DUPLICATE KEY UPDATE setting_value = ?", [
        json_encode(['date' => date('Y-m-d H:i:s'), 'stats' => $stats]),
        json_encode(['date' => date('Y-m-d H:i:s'), 'stats' => $stats])
    ]);

    return $stats;
}

/**
 * Create monthly ranking snapshots going back 24 months from latest event
 * This provides historical data for ranking charts
 */
function createMonthlyRankingSnapshots($db, $debug = false) {
    $snapshotCount = 0;

    // Get the latest event date as our reference point
    $latestEventDate = getLatestEventDateWithResults($db, 'GRAVITY');

    // Generate list of 1st of each month going back 24 months
    $refDate = new DateTime($latestEventDate);
    $monthlyDates = [];

    // Start from the 1st of the current month of the latest event
    $currentMonth = new DateTime($refDate->format('Y-m-01'));

    for ($i = 0; $i < 24; $i++) {
        $monthlyDates[] = $currentMonth->format('Y-m-d');
        $currentMonth->modify('-1 month');
    }

    foreach ($monthlyDates as $snapshotDate) {
        // Check if we have any events with results before this date
        $hasData = $db->getRow("
            SELECT 1 FROM events e
            JOIN results r ON r.event_id = e.id
            WHERE e.date <= ? AND r.status = 'finished'
            AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0)
            LIMIT 1
        ", [$snapshotDate]);

        if (!$hasData) {
            continue; // Skip months without any data
        }

        // Check if snapshot already exists for this date
        $existing = $db->getRow("
            SELECT 1 FROM ranking_snapshots
            WHERE discipline = 'GRAVITY' AND snapshot_date = ?
            LIMIT 1
        ", [$snapshotDate]);

        if ($existing) {
            continue; // Don't overwrite existing snapshots
        }

        if ($debug) echo "<p>Creating snapshot for {$snapshotDate}...</p>";

        // Calculate ranking as of this date
        $riderData = calculateRankingDataAsOf($db, 'GRAVITY', $snapshotDate);

        // Get previous snapshot for position changes
        $previousSnapshot = $db->getAll("
            SELECT rider_id, ranking_position FROM ranking_snapshots
            WHERE discipline = 'GRAVITY' AND snapshot_date = (
                SELECT MAX(snapshot_date) FROM ranking_snapshots
                WHERE discipline = 'GRAVITY' AND snapshot_date < ?
            )
        ", [$snapshotDate]);

        $previousPositions = [];
        foreach ($previousSnapshot as $prev) {
            $previousPositions[$prev['rider_id']] = $prev['ranking_position'];
        }

        // Insert rider snapshots
        foreach ($riderData as $rider) {
            $prevPos = $previousPositions[$rider['rider_id']] ?? null;
            $posChange = $prevPos !== null ? ($prevPos - $rider['ranking_position']) : null;

            $db->query("INSERT INTO ranking_snapshots
                (rider_id, discipline, snapshot_date, total_ranking_points,
                 points_last_12_months, points_months_13_24, events_count,
                 ranking_position, previous_position, position_change)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
                $rider['rider_id'],
                'GRAVITY',
                $snapshotDate,
                $rider['total_ranking_points'],
                $rider['points_12'],
                $rider['points_13_24'],
                $rider['events_count'],
                $rider['ranking_position'],
                $prevPos,
                $posChange
            ]);
            $snapshotCount++;
        }

        // Also calculate club ranking
        $clubData = calculateClubRankingDataAsOf($db, 'GRAVITY', $snapshotDate);

        // Check if club snapshot exists
        $existingClub = $db->getRow("
            SELECT 1 FROM club_ranking_snapshots
            WHERE discipline = 'GRAVITY' AND snapshot_date = ?
            LIMIT 1
        ", [$snapshotDate]);

        if (!$existingClub) {
            $previousClubSnapshot = $db->getAll("
                SELECT club_id, ranking_position FROM club_ranking_snapshots
                WHERE discipline = 'GRAVITY' AND snapshot_date = (
                    SELECT MAX(snapshot_date) FROM club_ranking_snapshots
                    WHERE discipline = 'GRAVITY' AND snapshot_date < ?
                )
            ", [$snapshotDate]);

            $previousClubPositions = [];
            foreach ($previousClubSnapshot as $prev) {
                $previousClubPositions[$prev['club_id']] = $prev['ranking_position'];
            }

            foreach ($clubData as $club) {
                $prevPos = $previousClubPositions[$club['club_id']] ?? null;
                $posChange = $prevPos !== null ? ($prevPos - $club['ranking_position']) : null;

                $db->query("INSERT INTO club_ranking_snapshots
                    (club_id, discipline, snapshot_date, total_ranking_points,
                     points_last_12_months, points_months_13_24, riders_count, events_count,
                     ranking_position, previous_position, position_change)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
                    $club['club_id'],
                    'GRAVITY',
                    $snapshotDate,
                    $club['total_ranking_points'],
                    $club['points_12'],
                    $club['points_13_24'],
                    $club['riders_count'],
                    $club['events_count'],
                    $club['ranking_position'],
                    $prevPos,
                    $posChange
                ]);
            }
        }
    }

    return $snapshotCount;
}

/**
 * Get current rider ranking from snapshots (with pagination)
 */
function getCurrentRanking($db, $discipline = 'GRAVITY', $limit = 50, $offset = 0) {
    // Get latest snapshot date
    $latest = $db->getRow("SELECT MAX(snapshot_date) as snapshot_date FROM ranking_snapshots WHERE discipline = ?", [$discipline]);
    $snapshotDate = $latest['snapshot_date'] ?? null;

    if (!$snapshotDate) {
        // Fall back to live calculation
        $data = calculateRankingData($db, $discipline);
        return [
            'riders' => array_slice($data, $offset, $limit),
            'total' => count($data),
            'snapshot_date' => null,
            'discipline' => $discipline
        ];
    }

    // Get total count
    $countResult = $db->getRow("SELECT COUNT(*) as cnt FROM ranking_snapshots WHERE discipline = ? AND snapshot_date = ?",
                               [$discipline, $snapshotDate]);
    $total = $countResult['cnt'] ?? 0;

    // Get paginated results
    // Uses COALESCE to fallback to rider_club_seasons if riders.club_id is NULL
    $riders = $db->getAll("
        SELECT
            rs.*,
            r.firstname,
            r.lastname,
            COALESCE(r.club_id, rcs_latest.club_id) as club_id,
            COALESCE(c.name, c_season.name) as club_name
        FROM ranking_snapshots rs
        JOIN riders r ON rs.rider_id = r.id
        LEFT JOIN clubs c ON r.club_id = c.id
        LEFT JOIN (
            SELECT rider_id, club_id
            FROM rider_club_seasons
            WHERE (rider_id, season_year) IN (
                SELECT rider_id, MAX(season_year)
                FROM rider_club_seasons
                GROUP BY rider_id
            )
        ) rcs_latest ON rcs_latest.rider_id = r.id AND r.club_id IS NULL
        LEFT JOIN clubs c_season ON rcs_latest.club_id = c_season.id
        WHERE rs.discipline = ? AND rs.snapshot_date = ?
        ORDER BY rs.ranking_position ASC
        LIMIT ? OFFSET ?
    ", [$discipline, $snapshotDate, $limit, $offset]);

    return [
        'riders' => $riders,
        'total' => $total,
        'snapshot_date' => $snapshotDate,
        'discipline' => $discipline
    ];
}

/**
 * Get current CLUB ranking from snapshots (with pagination)
 */
function getCurrentClubRanking($db, $discipline = 'GRAVITY', $limit = 50, $offset = 0) {
    // Get latest snapshot date
    $latest = $db->getRow("SELECT MAX(snapshot_date) as snapshot_date FROM club_ranking_snapshots WHERE discipline = ?", [$discipline]);
    $snapshotDate = $latest['snapshot_date'] ?? null;

    if (!$snapshotDate) {
        // Fall back to live calculation
        $data = calculateClubRankingData($db, $discipline);
        return [
            'clubs' => array_slice($data, $offset, $limit),
            'total' => count($data),
            'snapshot_date' => null,
            'discipline' => $discipline
        ];
    }

    // Get total count
    $countResult = $db->getRow("SELECT COUNT(*) as cnt FROM club_ranking_snapshots WHERE discipline = ? AND snapshot_date = ?",
                               [$discipline, $snapshotDate]);
    $total = $countResult['cnt'] ?? 0;

    // Get paginated results
    $clubs = $db->getAll("
        SELECT
            crs.*,
            c.name as club_name,
            c.short_name,
            c.city,
            c.region,
            c.logo
        FROM club_ranking_snapshots crs
        JOIN clubs c ON crs.club_id = c.id
        WHERE crs.discipline = ? AND crs.snapshot_date = ?
        ORDER BY crs.ranking_position ASC
        LIMIT ? OFFSET ?
    ", [$discipline, $snapshotDate, $limit, $offset]);

    return [
        'clubs' => $clubs,
        'total' => $total,
        'snapshot_date' => $snapshotDate,
        'discipline' => $discipline
    ];
}

/**
 * Get ranking statistics per discipline
 */
function getRankingStats($db) {
    $stats = [];

    foreach (['ENDURO', 'DH', 'GRAVITY'] as $discipline) {
        $riderCount = $db->getRow("
            SELECT COUNT(*) as cnt FROM ranking_snapshots
            WHERE discipline = ? AND snapshot_date = (
                SELECT MAX(snapshot_date) FROM ranking_snapshots WHERE discipline = ?
            )
        ", [$discipline, $discipline]);

        $clubCount = $db->getRow("
            SELECT COUNT(*) as cnt FROM club_ranking_snapshots
            WHERE discipline = ? AND snapshot_date = (
                SELECT MAX(snapshot_date) FROM club_ranking_snapshots WHERE discipline = ?
            )
        ", [$discipline, $discipline]);

        // Count unique events in last 24 months from latest event
        $latestDate = getLatestEventDateWithResults($db, $discipline);
        $cutoff = date('Y-m-d', strtotime($latestDate . ' -24 months'));
        $discFilter = $discipline === 'GRAVITY' ? "IN ('ENDURO', 'DH')" : "= '$discipline'";
        $eventCount = $db->getRow("SELECT COUNT(DISTINCT id) as cnt FROM events WHERE discipline $discFilter AND date >= ?", [$cutoff]);

        $stats[$discipline] = [
            'riders' => $riderCount['cnt'] ?? 0,
            'clubs' => $clubCount['cnt'] ?? 0,
            'events' => $eventCount['cnt'] ?? 0
        ];
    }

    return $stats;
}

/**
 * Get last calculation info
 */
function getLastRankingCalculation($db) {
    try {
        $result = $db->getRow("SELECT setting_value FROM ranking_settings WHERE setting_key = 'last_calculation'");
        if ($result && $result['setting_value']) {
            return json_decode($result['setting_value'], true) ?: ['date' => null, 'stats' => []];
        }
    } catch (Exception $e) {}
    return ['date' => null, 'stats' => []];
}

/**
 * Calculate single rider ranking
 */
function calculateSingleRiderRanking($db, $riderId, $discipline = 'GRAVITY') {
    $data = calculateRankingData($db, $discipline);
    foreach ($data as $rider) {
        if ($rider['rider_id'] == $riderId) {
            return $rider;
        }
    }
    return null;
}

/**
 * Get single club ranking
 */
function getSingleClubRanking($db, $clubId, $discipline = 'GRAVITY') {
    $data = calculateClubRankingData($db, $discipline);
    foreach ($data as $club) {
        if ($club['club_id'] == $clubId) {
            return $club;
        }
    }
    return null;
}

/**
 * Get detailed ranking breakdown for a rider
 */
function getRiderRankingDetails($db, $riderId, $discipline = 'GRAVITY') {
    // Get rider info
    $rider = $db->getRow("
        SELECT r.*, c.name as club_name
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.id = ?
    ", [$riderId]);

    if (!$rider) {
        return null;
    }

    // Get current ranking from snapshot if available
    $latestSnapshot = $db->getRow("
        SELECT MAX(snapshot_date) as snapshot_date FROM ranking_snapshots WHERE discipline = ?
    ", [$discipline]);

    $ranking = null;
    if ($latestSnapshot && $latestSnapshot['snapshot_date']) {
        $ranking = $db->getRow("
            SELECT * FROM ranking_snapshots
            WHERE rider_id = ? AND discipline = ? AND snapshot_date = ?
        ", [$riderId, $discipline, $latestSnapshot['snapshot_date']]);
    }

    // Get event breakdown - use latest event date as reference
    $referenceDate = getLatestEventDateWithResults($db, $discipline);
    $cutoffDate = date('Y-m-d', strtotime($referenceDate . ' -24 months'));
    $disciplineFilter = $discipline === 'GRAVITY' ? "AND e.discipline IN ('ENDURO', 'DH')" : "AND e.discipline = ?";
    $params = [$riderId, $cutoffDate];
    if ($discipline !== 'GRAVITY') {
        $params[] = $discipline;
    }

    $events = $db->getAll("
        SELECT
            r.event_id,
            r.class_id,
            e.discipline,
            COALESCE(
                CASE
                    WHEN COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0
                    THEN COALESCE(r.run_1_points, 0) + COALESCE(r.run_2_points, 0)
                    ELSE r.points
                END,
                r.points
            ) as original_points,
            e.date as event_date,
            e.name as event_name,
            e.location,
            e.event_level,
            cl.name as class_name,
            cl.display_name as class_display_name,
            (SELECT COUNT(*) FROM results r2 WHERE r2.event_id = r.event_id AND r2.class_id = r.class_id AND r2.status = 'finished') as field_size
        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN classes cl ON r.class_id = cl.id
        WHERE r.cyclist_id = ?
        AND e.date >= ?
        {$disciplineFilter}
        AND r.status = 'finished'
        AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0)
        AND COALESCE(cl.series_eligible, 1) = 1
        AND COALESCE(cl.awards_points, 1) = 1
        ORDER BY e.date DESC
    ", $params);

    // Get multipliers
    $fieldMultipliers = getRankingFieldMultipliers($db);
    $timeDecay = getRankingTimeDecay($db);
    $eventLevelMultipliers = getEventLevelMultipliers($db);

    // Calculate weighted points for each event
    $totalRankingPoints = 0;
    foreach ($events as &$event) {
        $fieldSize = (int)($event['field_size'] ?? 1);
        $fieldMult = $fieldMultipliers[min($fieldSize, 15)] ?? 1.00;

        $eventLevel = $event['event_level'] ?? 'national';
        $eventLevelMult = ($eventLevel === 'sportmotion')
            ? ($eventLevelMultipliers['sportmotion'] ?? 0.50)
            : ($eventLevelMultipliers['national'] ?? 1.00);

        // Time decay relative to latest event date (not today)
        $eventDate = $event['event_date'] ?? date('Y-m-d');
        $monthsAgo = (int)((strtotime($referenceDate) - strtotime($eventDate)) / (30.44 * 24 * 3600));
        if ($monthsAgo <= 12) {
            $timeMult = $timeDecay['months_1_12'] ?? 1.00;
        } elseif ($monthsAgo <= 24) {
            $timeMult = $timeDecay['months_13_24'] ?? 0.50;
        } else {
            $timeMult = $timeDecay['months_25_plus'] ?? 0.00;
        }

        $basePoints = (float)($event['original_points'] ?? 0);
        $weightedPoints = $basePoints * $fieldMult * $eventLevelMult * $timeMult;

        $event['field_multiplier'] = $fieldMult;
        $event['event_level_multiplier'] = $eventLevelMult;
        $event['time_multiplier'] = $timeMult;
        $event['weighted_points'] = $weightedPoints;
        $event['class_name'] = $event['class_display_name'] ?: $event['class_name'];

        $totalRankingPoints += $weightedPoints;
    }
    unset($event);

    return [
        'rider' => $rider,
        'ranking' => $ranking,
        'events' => $events,
        'discipline' => $discipline,
        'total_ranking_points' => $totalRankingPoints,
        'ranking_position' => $ranking['ranking_position'] ?? null
    ];
}

/**
 * Get ranking history for a rider (all snapshots over time)
 * Returns up to $limit snapshots ordered by date ascending (oldest first)
 */
function getRiderRankingHistory($db, $riderId, $discipline = 'GRAVITY', $limit = 50) {
    // Get all snapshots for this rider, ordered by date (oldest first)
    $history = $db->getAll("
        SELECT
            snapshot_date,
            ranking_position,
            total_ranking_points,
            points_last_12_months,
            points_months_13_24,
            events_count,
            position_change
        FROM ranking_snapshots
        WHERE rider_id = ? AND discipline = ?
        ORDER BY snapshot_date ASC
        LIMIT ?
    ", [$riderId, $discipline, $limit]);

    return $history;
}
