<?php
/**
 * TheHUB - Rider Statistics & Achievements Rebuild System
 *
 * Kör denna funktion efter import av historiska resultat för att
 * räkna om all statistik och achievements från grunden.
 *
 * Användning:
 *   - Enskild åkare: rebuildRiderStats($pdo, $rider_id)
 *   - Alla åkare: rebuildAllRiderStats($pdo)
 *   - Via admin: /admin/rebuild-stats.php
 */

// ============================================
// CONFIGURATION
// ============================================

define('EXPERIENCE_LEVELS', [
    1 => ['name' => '1st Year', 'icon' => '⭐'],
    2 => ['name' => '2nd Year', 'icon' => '⭐'],
    3 => ['name' => 'Experienced', 'icon' => '⭐'],
    4 => ['name' => 'Expert', 'icon' => '🌟'],
    5 => ['name' => 'Veteran', 'icon' => '👑'],
    6 => ['name' => 'Legend', 'icon' => '🏆']  // Kräver 5+ säsonger OCH minst 1 serieseger
]);

define('HOT_STREAK_MINIMUM', 3); // Minst 3 raka topp-3 för achievement

// ============================================
// MAIN REBUILD FUNCTIONS
// ============================================

/**
 * Bygger om ALL statistik och achievements för EN åkare
 */
function rebuildRiderStats($pdo, $rider_id) {
    $stats = [
        'rider_id' => $rider_id,
        'started' => date('Y-m-d H:i:s'),
        'achievements_added' => 0,
        'errors' => []
    ];

    try {
        $pdo->beginTransaction();

        // 1. Rensa gamla achievements för denna åkare
        $stmt = $pdo->prepare("DELETE FROM rider_achievements WHERE rider_id = ?");
        $stmt->execute([$rider_id]);

        // 2. Hämta all resultathistorik
        $results = getRiderResultHistory($pdo, $rider_id);

        if (empty($results)) {
            $pdo->commit();
            $stats['message'] = 'Inga resultat hittades';
            $stats['success'] = true;
            return $stats;
        }

        // 3. Beräkna och spara achievements

        // Pallplatser
        $podiums = calculatePodiums($results);
        foreach ($podiums as $type => $count) {
            if ($count > 0) {
                insertAchievement($pdo, $rider_id, $type, $count);
                $stats['achievements_added']++;
            }
        }

        // Hot Streaks
        $hotStreak = calculateHotStreak($results);
        if ($hotStreak >= HOT_STREAK_MINIMUM) {
            insertAchievement($pdo, $rider_id, 'hot_streak', $hotStreak);
            $stats['achievements_added']++;
        }

        // Fullföljt per säsong
        $finishRates = calculateFinishRates($pdo, $rider_id);
        foreach ($finishRates as $year => $rate) {
            if ($rate == 100) {
                insertAchievement($pdo, $rider_id, 'finisher_100', '100%', null, $year);
                $stats['achievements_added']++;
            }
        }

        // Seriesegrar (historiska)
        $seriesWins = calculateSeriesChampionships($pdo, $rider_id);
        foreach ($seriesWins as $win) {
            insertAchievement($pdo, $rider_id, 'series_champion', $win['series_name'], $win['series_id'], $win['year']);
            $stats['achievements_added']++;
        }

        // Stage wins (snabbaste på SS)
        $stageWins = calculateStageWins($pdo, $rider_id);
        if ($stageWins > 0) {
            insertAchievement($pdo, $rider_id, 'stage_win', $stageWins);
            $stats['achievements_added']++;
        }

        // Multi-serie (topp-3 i flera serier samma säsong)
        $multiSeries = calculateMultiSeriesSeasons($pdo, $rider_id);
        foreach ($multiSeries as $year) {
            insertAchievement($pdo, $rider_id, 'multi_series', null, null, $year);
            $stats['achievements_added']++;
        }

        // Svensk Mästare (vunnit mästerskapstävling)
        $championships = calculateSwedishChampionships($pdo, $rider_id);
        foreach ($championships as $champ) {
            insertAchievement($pdo, $rider_id, 'swedish_champion', $champ['event_name'], null, $champ['year'], $champ['event_id']);
            $stats['achievements_added']++;
        }

        // 4. Uppdatera cached stats på rider-tabellen
        updateRiderCachedStats($pdo, $rider_id, $results);

        // 5. Uppdatera experience level
        updateExperienceLevel($pdo, $rider_id);

        $pdo->commit();
        $stats['success'] = true;
        $stats['completed'] = date('Y-m-d H:i:s');

    } catch (Exception $e) {
        $pdo->rollBack();
        $stats['success'] = false;
        $stats['errors'][] = $e->getMessage();
    }

    return $stats;
}

/**
 * Bygger om statistik för ALLA åkare
 * Använd med försiktighet - kan ta lång tid!
 */
function rebuildAllRiderStats($pdo, $progressCallback = null) {
    $startTime = microtime(true);

    // Hämta alla åkare som har minst ett resultat OCH finns i riders-tabellen
    // Detta förhindrar att achievements skapas för ogiltiga rider_ids
    $stmt = $pdo->query("
        SELECT DISTINCT res.cyclist_id as rider_id
        FROM results res
        INNER JOIN riders r ON res.cyclist_id = r.id
        WHERE res.cyclist_id IS NOT NULL
        ORDER BY res.cyclist_id
    ");
    $riderIds = $stmt->fetchAll(PDO::FETCH_COLUMN);

    $totalRiders = count($riderIds);
    $processed = 0;
    $failed = 0;
    $results = [];

    foreach ($riderIds as $riderId) {
        $result = rebuildRiderStats($pdo, $riderId);

        if (!isset($result['success']) || !$result['success']) {
            $failed++;
        }

        $processed++;
        $results[$riderId] = $result;

        // Progress callback för UI-uppdatering
        if ($progressCallback && is_callable($progressCallback)) {
            $progressCallback($processed, $totalRiders, $riderId, $result);
        }
    }

    // Uppdatera aktiva serieledare
    updateCurrentSeriesLeaders($pdo);

    $endTime = microtime(true);

    return [
        'total_riders' => $totalRiders,
        'processed' => $processed,
        'failed' => $failed,
        'duration_seconds' => round($endTime - $startTime, 2),
        'details' => $results
    ];
}

// ============================================
// DATA RETRIEVAL
// ============================================

/**
 * Hämtar komplett resultathistorik för en åkare
 */
function getRiderResultHistory($pdo, $rider_id) {
    $stmt = $pdo->prepare("
        SELECT
            r.id as result_id,
            r.position,
            r.finish_time as time,
            r.points,
            r.status,
            CASE WHEN r.status = 'dnf' THEN 1 ELSE 0 END as dnf,
            CASE WHEN r.status = 'dns' THEN 1 ELSE 0 END as dns,
            CASE WHEN r.status = 'dsq' THEN 1 ELSE 0 END as dsq,
            e.id as event_id,
            e.name as event_name,
            e.date as event_date,
            YEAR(e.date) as season_year,
            s.id as series_id,
            s.name as series_name,
            c.id as class_id,
            c.display_name as class_name
        FROM results r
        JOIN events e ON r.event_id = e.id
        LEFT JOIN series s ON e.series_id = s.id
        LEFT JOIN classes c ON r.class_id = c.id
        WHERE r.cyclist_id = ?
        ORDER BY e.date ASC
    ");
    $stmt->execute([$rider_id]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Hämtar achievements för en åkare
 */
function getRiderAchievements($pdo, $rider_id) {
    $stmt = $pdo->prepare("
        SELECT * FROM rider_achievements
        WHERE rider_id = ?
        ORDER BY earned_at DESC
    ");
    $stmt->execute([$rider_id]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Hämtar sociala profiler med formaterade URLs
 */
function getRiderSocialProfiles($pdo, $rider_id) {
    $stmt = $pdo->prepare("
        SELECT
            social_instagram,
            social_facebook,
            social_strava,
            social_youtube,
            social_tiktok
        FROM riders WHERE id = ?
    ");
    $stmt->execute([$rider_id]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$row) return [];

    $profiles = [];

    if (!empty($row['social_instagram'])) {
        $ig = $row['social_instagram'];
        $profiles['instagram'] = [
            'username' => $ig,
            'url' => strpos($ig, 'http') === 0 ? $ig : 'https://instagram.com/' . ltrim($ig, '@')
        ];
    }

    if (!empty($row['social_strava'])) {
        $strava = $row['social_strava'];
        $profiles['strava'] = [
            'id' => $strava,
            'url' => strpos($strava, 'http') === 0 ? $strava : 'https://strava.com/athletes/' . $strava
        ];
    }

    if (!empty($row['social_facebook'])) {
        $fb = $row['social_facebook'];
        $profiles['facebook'] = [
            'id' => $fb,
            'url' => strpos($fb, 'http') === 0 ? $fb : 'https://facebook.com/' . $fb
        ];
    }

    if (!empty($row['social_youtube'])) {
        $yt = $row['social_youtube'];
        if (strpos($yt, 'http') === 0) {
            $url = $yt;
        } elseif (strpos($yt, '@') === 0) {
            $url = 'https://youtube.com/' . $yt;
        } else {
            $url = 'https://youtube.com/@' . $yt;
        }
        $profiles['youtube'] = [
            'id' => $yt,
            'url' => $url
        ];
    }

    if (!empty($row['social_tiktok'])) {
        $tt = $row['social_tiktok'];
        $profiles['tiktok'] = [
            'username' => $tt,
            'url' => strpos($tt, 'http') === 0 ? $tt : 'https://tiktok.com/@' . ltrim($tt, '@')
        ];
    }

    return $profiles;
}

/**
 * Hämtar serieställningar med trend
 */
function getRiderSeriesStandings($pdo, $rider_id, $year = null) {
    $year = $year ?? date('Y');

    // First get the series and their count_best_results setting
    // Exclude motion classes (awards_points = 0 or name contains 'motion')
    // Join series_brands to get the accent color
    $stmt = $pdo->prepare("
        SELECT DISTINCT
            s.id as series_id,
            s.name as series_name,
            s.count_best_results,
            r.class_id,
            c.display_name as class_name,
            sb.accent_color as series_color
        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN series s ON e.series_id = s.id
        LEFT JOIN series_brands sb ON s.brand_id = sb.id
        JOIN classes c ON r.class_id = c.id
        WHERE r.cyclist_id = ? AND YEAR(e.date) = ? AND r.status = 'finished'
          AND COALESCE(c.awards_points, 1) = 1
    ");
    $stmt->execute([$rider_id, $year]);
    $seriesClasses = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $standings = [];
    foreach ($seriesClasses as $sc) {
        // Get all points for this rider in this series/class
        $pStmt = $pdo->prepare("
            SELECT r.points, r.position, e.id as event_id
            FROM results r
            JOIN events e ON r.event_id = e.id
            WHERE r.cyclist_id = ? AND e.series_id = ? AND r.class_id = ?
                  AND YEAR(e.date) = ? AND r.status = 'finished'
            ORDER BY r.points DESC
        ");
        $pStmt->execute([$rider_id, $sc['series_id'], $sc['class_id'], $year]);
        $results = $pStmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($results)) continue;

        // Calculate counted points based on count_best_results
        $countBest = $sc['count_best_results'];
        $allPoints = array_column($results, 'points');

        if ($countBest && count($allPoints) > $countBest) {
            // Sort descending and take best X
            rsort($allPoints);
            $countedPoints = array_sum(array_slice($allPoints, 0, $countBest));
        } else {
            $countedPoints = array_sum($allPoints);
        }

        $wins = count(array_filter($results, fn($r) => $r['position'] == 1));
        $podiums = count(array_filter($results, fn($r) => $r['position'] <= 3));

        $standings[] = [
            'series_id' => $sc['series_id'],
            'series_name' => $sc['series_name'],
            'class_id' => $sc['class_id'],
            'class_name' => $sc['class_name'],
            'count_best_results' => $countBest,
            'total_points' => $countedPoints,
            'events_count' => count($results),
            'wins' => $wins,
            'podiums' => $podiums,
            'series_color' => $sc['series_color'] ?? null
        ];
    }

    // Sort by total_points
    usort($standings, fn($a, $b) => $b['total_points'] - $a['total_points']);

    // Lägg till ranking och trend för varje serie
    foreach ($standings as &$standing) {
        $standing['ranking'] = getSeriesRanking($pdo, $standing['series_id'], $rider_id, $standing['class_id'], $year, $standing['count_best_results']);
        $standing['trend'] = calculateTrend($pdo, $standing['series_id'], $rider_id, $standing['class_id'], $year);
        $standing['total_riders'] = getTotalRidersInClass($pdo, $standing['series_id'], $standing['class_id'], $year);
        $standing['gap_to_podium'] = calculateGapToPodium($pdo, $standing['series_id'], $rider_id, $standing['class_id'], $year, $standing['count_best_results']);
        $standing['results'] = getSeriesResults($pdo, $standing['series_id'], $rider_id, $year);
        // Use brand color from database, fallback to name-based color
        if (empty($standing['series_color'])) {
            $standing['series_color'] = getSeriesColor($standing['series_name']);
        }
    }

    return $standings;
}

/**
 * Hämtar ranking position i serie (med count_best_results)
 */
function getSeriesRanking($pdo, $series_id, $rider_id, $class_id, $year, $countBest = null) {
    // Get all riders in this series/class
    $stmt = $pdo->prepare("
        SELECT DISTINCT r.cyclist_id
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE e.series_id = ? AND r.class_id = ? AND YEAR(e.date) = ? AND r.status = 'finished'
    ");
    $stmt->execute([$series_id, $class_id, $year]);
    $riders = $stmt->fetchAll(PDO::FETCH_COLUMN);

    // Calculate counted points for each rider
    $riderPoints = [];
    foreach ($riders as $rid) {
        $pStmt = $pdo->prepare("
            SELECT r.points
            FROM results r
            JOIN events e ON r.event_id = e.id
            WHERE r.cyclist_id = ? AND e.series_id = ? AND r.class_id = ?
                  AND YEAR(e.date) = ? AND r.status = 'finished'
            ORDER BY r.points DESC
        ");
        $pStmt->execute([$rid, $series_id, $class_id, $year]);
        $points = $pStmt->fetchAll(PDO::FETCH_COLUMN);

        if ($countBest && count($points) > $countBest) {
            $total = array_sum(array_slice($points, 0, $countBest));
        } else {
            $total = array_sum($points);
        }
        $riderPoints[$rid] = $total;
    }

    // Sort by points descending
    arsort($riderPoints);

    // Find rider's position
    $position = 1;
    foreach ($riderPoints as $rid => $pts) {
        if ($rid == $rider_id) {
            return $position;
        }
        $position++;
    }
    return null;
}

/**
 * Hämtar totalt antal åkare i klass/serie
 */
function getTotalRidersInClass($pdo, $series_id, $class_id, $year) {
    $stmt = $pdo->prepare("
        SELECT COUNT(DISTINCT r.cyclist_id) as total
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE e.series_id = ? AND r.class_id = ? AND YEAR(e.date) = ? AND r.status = 'finished'
    ");
    $stmt->execute([$series_id, $class_id, $year]);
    return $stmt->fetchColumn() ?: 0;
}

/**
 * Beräknar poängdifferens till pallplats (med count_best_results)
 */
function calculateGapToPodium($pdo, $series_id, $rider_id, $class_id, $year, $countBest = null) {
    // Get all riders in this series/class
    $stmt = $pdo->prepare("
        SELECT DISTINCT r.cyclist_id
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE e.series_id = ? AND r.class_id = ? AND YEAR(e.date) = ? AND r.status = 'finished'
    ");
    $stmt->execute([$series_id, $class_id, $year]);
    $riders = $stmt->fetchAll(PDO::FETCH_COLUMN);

    // Calculate counted points for each rider
    $riderPointsMap = [];
    foreach ($riders as $rid) {
        $pStmt = $pdo->prepare("
            SELECT r.points
            FROM results r
            JOIN events e ON r.event_id = e.id
            WHERE r.cyclist_id = ? AND e.series_id = ? AND r.class_id = ?
                  AND YEAR(e.date) = ? AND r.status = 'finished'
            ORDER BY r.points DESC
        ");
        $pStmt->execute([$rid, $series_id, $class_id, $year]);
        $points = $pStmt->fetchAll(PDO::FETCH_COLUMN);

        if ($countBest && count($points) > $countBest) {
            $total = array_sum(array_slice($points, 0, $countBest));
        } else {
            $total = array_sum($points);
        }
        $riderPointsMap[$rid] = $total;
    }

    // Sort by points descending
    arsort($riderPointsMap);
    $sortedRiders = array_keys($riderPointsMap);

    if (count($sortedRiders) < 3) {
        return null; // Not enough riders
    }

    $riderPoints = $riderPointsMap[$rider_id] ?? 0;

    // Find rider's position
    $position = array_search($rider_id, $sortedRiders);
    if ($position === false) {
        return null;
    }

    if ($position == 0) {
        // Leader - show gap to second place
        return $riderPoints - $riderPointsMap[$sortedRiders[1]];
    } elseif ($position <= 2) {
        // In podium - show gap to previous position
        return $riderPointsMap[$sortedRiders[$position - 1]] - $riderPoints;
    } else {
        // Not in podium - show gap to third place
        return $riderPointsMap[$sortedRiders[2]] - $riderPoints;
    }
}

// ============================================
// ACHIEVEMENT CALCULATIONS
// ============================================

/**
 * Räknar pallplatser
 */
function calculatePodiums($results) {
    $podiums = ['gold' => 0, 'silver' => 0, 'bronze' => 0];

    foreach ($results as $r) {
        if ($r['status'] !== 'finished') continue;

        switch ($r['position']) {
            case 1: $podiums['gold']++; break;
            case 2: $podiums['silver']++; break;
            case 3: $podiums['bronze']++; break;
        }
    }

    return $podiums;
}

/**
 * Beräknar längsta hot streak (raka topp-3 placeringar)
 */
function calculateHotStreak($results) {
    $currentStreak = 0;
    $maxStreak = 0;

    // Sortera efter datum (bör redan vara sorterat)
    usort($results, fn($a, $b) => strtotime($a['event_date']) - strtotime($b['event_date']));

    foreach ($results as $r) {
        // Hoppa över DNS (ingår inte i streak-beräkning)
        if ($r['status'] === 'dns') continue;

        // DNF/DSQ bryter streak
        if ($r['status'] !== 'finished') {
            $maxStreak = max($maxStreak, $currentStreak);
            $currentStreak = 0;
            continue;
        }

        if ($r['position'] <= 3) {
            $currentStreak++;
        } else {
            $maxStreak = max($maxStreak, $currentStreak);
            $currentStreak = 0;
        }
    }

    return max($maxStreak, $currentStreak);
}

/**
 * Beräknar fullföljt-procent per säsong
 */
function calculateFinishRates($pdo, $rider_id) {
    $stmt = $pdo->prepare("
        SELECT
            YEAR(e.date) as season_year,
            COUNT(*) as total_starts,
            SUM(CASE WHEN r.status = 'finished' THEN 1 ELSE 0 END) as finished
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE r.cyclist_id = ?
        GROUP BY YEAR(e.date)
    ");
    $stmt->execute([$rider_id]);
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $rates = [];
    foreach ($rows as $row) {
        if ($row['total_starts'] > 0) {
            $rates[$row['season_year']] = round(($row['finished'] / $row['total_starts']) * 100);
        }
    }

    return $rates;
}

/**
 * Hittar seriesegrar (seriemästare för avslutade serier)
 *
 * Kvalificerar som avslutad serie:
 * 1. Serier markerade som 'completed' (manuell - administatör markerar när alla resultat är inne)
 * 2. Serier från tidigare år (bakåtkompatibilitet)
 *
 * OBS: end_date används INTE längre automatiskt - serien måste markeras som completed
 * för att undvika felaktig mästarskap om resultat saknas.
 *
 * @param bool $debug Enable debug output (default false)
 */
function calculateSeriesChampionships($pdo, $rider_id, $debug = false) {
    $currentYear = (int)date('Y');
    $debugLog = [];
    $MIN_RACES_FOR_CHAMPIONSHIP = 2; // Minimum races required to be eligible

    // Check if series_events junction table exists
    $stmt = $pdo->query("SHOW TABLES LIKE 'series_events'");
    $useSeriesEvents = $stmt->fetch() !== false;
    if ($debug) $debugLog[] = "useSeriesEvents: " . ($useSeriesEvents ? 'JA' : 'NEJ');
    if ($debug) $debugLog[] = "Minimikrav: {$MIN_RACES_FOR_CHAMPIONSHIP} starter";

    // Get series info including count_best_results
    $seriesInfo = [];
    $seriesStmt = $pdo->query("SELECT id, name, year, status, end_date, count_best_results FROM series");
    while ($s = $seriesStmt->fetch(PDO::FETCH_ASSOC)) {
        $seriesInfo[(int)$s['id']] = $s;
    }
    if ($debug) $debugLog[] = "Antal serier: " . count($seriesInfo);

    // Get all series/class combinations where rider has results
    if ($useSeriesEvents) {
        $stmt = $pdo->prepare("
            SELECT DISTINCT s.id as series_id, r.class_id
            FROM results r
            JOIN events e ON r.event_id = e.id
            JOIN series_events se ON se.event_id = e.id
            JOIN series s ON se.series_id = s.id
            WHERE r.cyclist_id = ? AND r.status = 'finished'
        ");
    } else {
        $stmt = $pdo->prepare("
            SELECT DISTINCT s.id as series_id, r.class_id
            FROM results r
            JOIN events e ON r.event_id = e.id
            JOIN series s ON e.series_id = s.id
            WHERE r.cyclist_id = ? AND r.status = 'finished'
        ");
    }
    $stmt->execute([$rider_id]);
    $riderSeriesClasses = $stmt->fetchAll(PDO::FETCH_ASSOC);
    if ($debug) $debugLog[] = "Åkarens serie/klass-kombinationer: " . count($riderSeriesClasses);

    $championships = [];

    foreach ($riderSeriesClasses as $sc) {
        $seriesId = (int)$sc['series_id'];
        $classId = (int)$sc['class_id'];
        $series = $seriesInfo[$seriesId] ?? null;

        if (!$series) {
            if ($debug) $debugLog[] = "  - Serie {$seriesId} saknas!";
            continue;
        }

        $effectiveYear = (int)($series['year'] ?? $currentYear);
        $isCompleted = ($series['status'] ?? '') === 'completed';
        $isPastYear = $effectiveYear < $currentYear;
        $countBest = $series['count_best_results'] ? (int)$series['count_best_results'] : null;

        if ($debug) {
            $debugLog[] = "  Serie {$seriesId} ({$series['name']}): completed=" . ($isCompleted?'J':'N') . ", pastYear=" . ($isPastYear?'J':'N') . ", countBest=" . ($countBest ?? 'alla');
        }

        // Only qualifying series (completed OR past year)
        if (!$isCompleted && !$isPastYear) {
            if ($debug) $debugLog[] = "    -> Ej kvalificerad";
            continue;
        }

        // Get ALL riders' individual race results in this series/class
        if ($useSeriesEvents) {
            $allResultsStmt = $pdo->prepare("
                SELECT r.cyclist_id, r.points
                FROM results r
                JOIN events e ON r.event_id = e.id
                JOIN series_events se ON se.event_id = e.id
                WHERE se.series_id = ? AND r.class_id = ? AND r.status = 'finished'
                ORDER BY r.cyclist_id, r.points DESC
            ");
        } else {
            $allResultsStmt = $pdo->prepare("
                SELECT r.cyclist_id, r.points
                FROM results r
                JOIN events e ON r.event_id = e.id
                WHERE e.series_id = ? AND r.class_id = ? AND r.status = 'finished'
                ORDER BY r.cyclist_id, r.points DESC
            ");
        }
        $allResultsStmt->execute([$seriesId, $classId]);
        $allResults = $allResultsStmt->fetchAll(PDO::FETCH_ASSOC);

        // Group by rider and calculate counted points (best X of Y)
        $riderTotals = [];
        $currentRiderId = null;
        $currentPoints = [];

        foreach ($allResults as $row) {
            if ($row['cyclist_id'] !== $currentRiderId) {
                if ($currentRiderId !== null) {
                    // Only include riders with minimum races
                    if (count($currentPoints) >= $MIN_RACES_FOR_CHAMPIONSHIP) {
                        usort($currentPoints, function($a, $b) { return $b - $a; });
                        $counted = $countBest ? array_slice($currentPoints, 0, $countBest) : $currentPoints;
                        $riderTotals[$currentRiderId] = [
                            'counted' => array_sum($counted),
                            'race_count' => count($currentPoints)
                        ];
                    }
                }
                $currentRiderId = $row['cyclist_id'];
                $currentPoints = [];
            }
            $currentPoints[] = (int)$row['points'];
        }
        // Don't forget last rider
        if ($currentRiderId !== null && count($currentPoints) >= $MIN_RACES_FOR_CHAMPIONSHIP) {
            usort($currentPoints, function($a, $b) { return $b - $a; });
            $counted = $countBest ? array_slice($currentPoints, 0, $countBest) : $currentPoints;
            $riderTotals[$currentRiderId] = [
                'counted' => array_sum($counted),
                'race_count' => count($currentPoints)
            ];
        }

        if (empty($riderTotals)) {
            if ($debug) $debugLog[] = "    -> Inga med minst {$MIN_RACES_FOR_CHAMPIONSHIP} starter";
            continue;
        }

        // Find max counted points among eligible riders
        $maxCounted = max(array_column($riderTotals, 'counted'));

        // Check if this rider is the champion
        $riderData = $riderTotals[$rider_id] ?? null;

        if ($debug) {
            $riderCounted = $riderData ? $riderData['counted'] : 0;
            $riderRaces = $riderData ? $riderData['race_count'] : 0;
            $eligible = $riderData ? 'JA' : 'NEJ (för få starter)';
            $debugLog[] = "    -> Åkare: {$riderCounted}p ({$riderRaces} starter), Max: {$maxCounted}p, Kvalificerad: {$eligible}";
        }

        if ($riderData && $riderData['counted'] == $maxCounted && $maxCounted > 0) {
            $championships[] = [
                'series_id' => $seriesId,
                'series_name' => $series['name'],
                'year' => $effectiveYear
            ];
            if ($debug) $debugLog[] = "    -> MÄSTARE!";
        }
    }

    if ($debug) {
        $debugLog[] = "Returnerar " . count($championships) . " mästarskap";
        return ['championships' => $championships, 'debug' => $debugLog];
    }

    return $championships;
}

/**
 * Räknar stage wins (snabbaste tid på en SS/etapp)
 */
function calculateStageWins($pdo, $rider_id) {
    // Stage wins are not tracked separately in this database
    // Return 0 for now - can be extended later
    return 0;
}

/**
 * Hittar säsonger där åkaren hade topp-3 i flera serier
 */
function calculateMultiSeriesSeasons($pdo, $rider_id) {
    $stmt = $pdo->prepare("
        SELECT YEAR(e.date) as season_year, COUNT(DISTINCT s.id) as series_count
        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN series s ON e.series_id = s.id
        WHERE r.cyclist_id = ?
          AND r.position <= 3
          AND r.status = 'finished'
        GROUP BY YEAR(e.date)
        HAVING series_count >= 2
    ");
    $stmt->execute([$rider_id]);

    return $stmt->fetchAll(PDO::FETCH_COLUMN);
}

/**
 * Hittar Svensk Mästare-titlar (vunnit event markerat som mästerskap)
 * Filtrerar på klasser som har is_championship_class = 1
 */
function calculateSwedishChampionships($pdo, $rider_id) {
    $stmt = $pdo->prepare("
        SELECT
            e.id as event_id,
            e.name as event_name,
            YEAR(e.date) as year,
            r.class_id,
            c.name as class_name
        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN classes c ON r.class_id = c.id
        WHERE r.cyclist_id = ?
          AND r.position = 1
          AND r.status = 'finished'
          AND e.is_championship = 1
          AND COALESCE(c.is_championship_class, 0) = 1
        ORDER BY e.date DESC
    ");
    $stmt->execute([$rider_id]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Beräknar trend (positionsförändring efter senaste event)
 * Returns: positive number = improved, negative = declined, 0 = no change
 */
function calculateTrend($pdo, $series_id, $rider_id, $class_id, $year) {
    // Hämta senaste två events
    $stmt = $pdo->prepare("
        SELECT e.id, e.date
        FROM events e
        WHERE e.series_id = ? AND YEAR(e.date) = ?
        ORDER BY e.date DESC
        LIMIT 2
    ");
    $stmt->execute([$series_id, $year]);
    $events = $stmt->fetchAll(PDO::FETCH_ASSOC);

    if (count($events) < 2) {
        return 0;
    }

    // Get standings before latest event
    $latestEventId = $events[0]['id'];

    // Calculate ranking after previous event (excluding latest)
    $stmt = $pdo->prepare("
        SELECT r.cyclist_id, SUM(r.points) as total_points
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE e.series_id = ? AND r.class_id = ? AND YEAR(e.date) = ?
          AND e.id != ? AND r.status = 'finished'
        GROUP BY r.cyclist_id
        ORDER BY total_points DESC
    ");
    $stmt->execute([$series_id, $class_id, $year, $latestEventId]);
    $previousStandings = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $previousPosition = null;
    $pos = 1;
    foreach ($previousStandings as $r) {
        if ($r['cyclist_id'] == $rider_id) {
            $previousPosition = $pos;
            break;
        }
        $pos++;
    }

    // Get current ranking
    $currentPosition = getSeriesRanking($pdo, $series_id, $rider_id, $class_id, $year);

    if ($previousPosition === null || $currentPosition === null) {
        return 0;
    }

    // Positive = improved (moved up in ranking), negative = declined
    return $previousPosition - $currentPosition;
}

/**
 * Hämtar resultat för en specifik serie
 */
function getSeriesResults($pdo, $series_id, $rider_id, $year) {
    $stmt = $pdo->prepare("
        SELECT
            e.id as event_id,
            r.position,
            r.finish_time as time,
            r.points,
            r.status,
            e.name as event_name,
            e.date as event_date,
            c.display_name as class_name
        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN classes c ON r.class_id = c.id
        WHERE r.cyclist_id = ?
          AND e.series_id = ?
          AND YEAR(e.date) = ?
          AND r.status != 'dns'
        ORDER BY e.date DESC
    ");
    $stmt->execute([$rider_id, $series_id, $year]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// ============================================
// UPDATE FUNCTIONS
// ============================================

/**
 * Sparar achievement till databasen
 */
function insertAchievement($pdo, $rider_id, $type, $value = null, $series_id = null, $year = null, $event_id = null) {
    $stmt = $pdo->prepare("
        INSERT INTO rider_achievements
            (rider_id, achievement_type, achievement_value, series_id, season_year, event_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ");
    $stmt->execute([$rider_id, $type, $value, $series_id, $year, $event_id]);
}

/**
 * Uppdaterar cachade stats på rider-tabellen för snabb hämtning
 */
function updateRiderCachedStats($pdo, $rider_id, $results) {
    $totalStarts = count($results);
    $finished = 0;
    $wins = 0;
    $podiums = 0;
    $totalPoints = 0;

    foreach ($results as $r) {
        if ($r['status'] === 'finished') {
            $finished++;
            $totalPoints += $r['points'] ?? 0;

            if ($r['position'] == 1) $wins++;
            if ($r['position'] <= 3) $podiums++;
        }
    }

    $stmt = $pdo->prepare("
        UPDATE riders SET
            stats_total_starts = ?,
            stats_total_finished = ?,
            stats_total_wins = ?,
            stats_total_podiums = ?,
            stats_total_points = ?,
            stats_updated_at = NOW()
        WHERE id = ?
    ");
    $stmt->execute([$totalStarts, $finished, $wins, $podiums, $totalPoints, $rider_id]);
}

/**
 * Beräknar och uppdaterar experience level
 * Baserat på antal UNIKA säsonger med resultat (inte kalenderår sedan start)
 * Legend (6) kräver: 5+ säsonger OCH minst 1 serieseger
 */
function updateExperienceLevel($pdo, $rider_id) {
    // Räkna antal unika säsonger med resultat (inte bara kalenderår sedan start)
    $stmt = $pdo->prepare("
        SELECT
            MIN(YEAR(e.date)) as first_season,
            COUNT(DISTINCT YEAR(e.date)) as seasons_with_results
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE r.cyclist_id = ?
    ");
    $stmt->execute([$rider_id]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    $firstSeason = $row['first_season'] ?? null;
    $seasonsWithResults = (int)($row['seasons_with_results'] ?? 0);

    if (!$firstSeason || $seasonsWithResults === 0) return;

    // Experience baserat på FAKTISKA säsonger med resultat
    $experienceLevel = min($seasonsWithResults, 5);

    // Kolla om Legend-status (kräver 5+ säsonger OCH serieseger)
    if ($seasonsWithResults >= 5) {
        $stmt = $pdo->prepare("
            SELECT COUNT(*) FROM rider_achievements
            WHERE rider_id = ? AND achievement_type = 'series_champion'
        ");
        $stmt->execute([$rider_id]);
        $seriesWins = (int)$stmt->fetchColumn();

        if ($seriesWins > 0) {
            $experienceLevel = 6; // Legend!
        }
    }

    $stmt = $pdo->prepare("
        UPDATE riders SET
            first_season = ?,
            experience_level = ?
        WHERE id = ?
    ");
    $stmt->execute([$firstSeason, $experienceLevel, $rider_id]);
}

/**
 * Uppdaterar aktiva serieledare (för pågående säsonger)
 * Kräver minst 2 genomförda tävlingar för att vara serieledare
 */
function updateCurrentSeriesLeaders($pdo) {
    $currentYear = date('Y');
    $minEventsForLeader = 2; // Minst 2 tävlingar krävs

    // Rensa gamla serieledare-achievements för innevarande år
    $stmt = $pdo->prepare("
        DELETE FROM rider_achievements
        WHERE achievement_type = 'series_leader'
          AND season_year = ?
    ");
    $stmt->execute([$currentYear]);

    // Hitta nuvarande ledare per serie och klass
    $stmt = $pdo->prepare("
        SELECT DISTINCT e.series_id, r.class_id
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE YEAR(e.date) = ? AND e.series_id IS NOT NULL
    ");
    $stmt->execute([$currentYear]);
    $seriesClasses = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($seriesClasses as $sc) {
        // Kolla hur många events som genomförts i denna serie/klass
        $stmt = $pdo->prepare("
            SELECT COUNT(DISTINCT e.id) as event_count
            FROM events e
            JOIN results r ON r.event_id = e.id
            WHERE e.series_id = ? AND r.class_id = ? AND YEAR(e.date) = ?
        ");
        $stmt->execute([$sc['series_id'], $sc['class_id'], $currentYear]);
        $eventCount = (int)$stmt->fetchColumn();

        // Skippa om färre än 2 events genomförts
        if ($eventCount < $minEventsForLeader) {
            continue;
        }

        // Find leader for this series/class
        $stmt = $pdo->prepare("
            SELECT r.cyclist_id, SUM(r.points) as total_points
            FROM results r
            JOIN events e ON r.event_id = e.id
            WHERE e.series_id = ? AND r.class_id = ? AND YEAR(e.date) = ? AND r.status = 'finished'
            GROUP BY r.cyclist_id
            ORDER BY total_points DESC
            LIMIT 1
        ");
        $stmt->execute([$sc['series_id'], $sc['class_id'], $currentYear]);
        $leader = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($leader && $leader['total_points'] > 0) {
            insertAchievement(
                $pdo,
                $leader['cyclist_id'],
                'series_leader',
                null,
                $sc['series_id'],
                $currentYear
            );
        }
    }
}

/**
 * Experience level helper
 */
function getExperienceLevelInfo($level) {
    $levels = [
        1 => ['name' => '1st Year', 'icon' => '⭐', 'next' => '2nd Year'],
        2 => ['name' => '2nd Year', 'icon' => '⭐', 'next' => 'Experienced'],
        3 => ['name' => 'Experienced', 'icon' => '⭐', 'next' => 'Expert'],
        4 => ['name' => 'Expert', 'icon' => '🌟', 'next' => 'Veteran'],
        5 => ['name' => 'Veteran', 'icon' => '👑', 'next' => 'Legend (kräver serieseger)'],
        6 => ['name' => 'Legend', 'icon' => '🏆', 'next' => null]
    ];
    return $levels[$level] ?? $levels[1];
}

/**
 * Get series color based on name
 */
function getSeriesColor($seriesName) {
    $name = strtolower($seriesName ?? '');

    // GravitySeries colors from CLAUDE.md
    if (strpos($name, 'gravityseries') !== false || strpos($name, 'gravity series') !== false) {
        return '#61CE70'; // --color-gs-green
    }
    if (strpos($name, 'ges') !== false || strpos($name, 'gravity enduro') !== false) {
        return '#EF761F'; // --color-ges-orange
    }
    if (strpos($name, 'ggs') !== false || strpos($name, 'gravity gravel') !== false) {
        return '#8A9A5B'; // --color-ggs-green
    }
    if (strpos($name, 'blue') !== false) {
        return '#004a98'; // --color-gs-blue
    }

    // Default accent color
    return '#61CE70';
}

/**
 * Bygger om statistik för alla åkare i ett specifikt event
 * Anropas automatiskt efter resultatimport
 */
function rebuildEventRiderStats($pdo, $eventId) {
    // Hämta alla åkare som har resultat i detta event
    $stmt = $pdo->prepare("
        SELECT DISTINCT cyclist_id as rider_id
        FROM results
        WHERE event_id = ? AND cyclist_id IS NOT NULL
    ");
    $stmt->execute([$eventId]);
    $riderIds = $stmt->fetchAll(PDO::FETCH_COLUMN);

    if (empty($riderIds)) {
        return [
            'event_id' => $eventId,
            'processed' => 0,
            'failed' => 0,
            'message' => 'Inga åkare hittades för detta event'
        ];
    }

    $startTime = microtime(true);
    $processed = 0;
    $failed = 0;

    foreach ($riderIds as $riderId) {
        $result = rebuildRiderStats($pdo, $riderId);

        if (!isset($result['success']) || !$result['success']) {
            $failed++;
        }
        $processed++;
    }

    // Uppdatera serieledare om eventet tillhör en serie
    $eventInfo = $pdo->prepare("SELECT series_id FROM events WHERE id = ?");
    $eventInfo->execute([$eventId]);
    $seriesId = $eventInfo->fetchColumn();

    if ($seriesId) {
        updateCurrentSeriesLeaders($pdo);
    }

    $endTime = microtime(true);

    return [
        'event_id' => $eventId,
        'processed' => $processed,
        'failed' => $failed,
        'duration_seconds' => round($endTime - $startTime, 2)
    ];
}

/**
 * Sanitize social media handles
 */
function sanitizeSocialHandle($value, $platform) {
    if (empty($value)) return null;

    $value = trim($value);

    switch ($platform) {
        case 'instagram':
        case 'tiktok':
            // Remove @ prefix if present
            return ltrim($value, '@');

        case 'strava':
            // Extract athlete ID from URL if full URL provided
            if (preg_match('/strava\.com\/athletes\/(\d+)/', $value, $matches)) {
                return $matches[1];
            }
            // If just numbers, return as-is
            if (is_numeric($value)) {
                return $value;
            }
            return $value;

        case 'facebook':
            // If full URL, extract path
            if (preg_match('/facebook\.com\/(.+?)(?:\/|$|\?)/', $value, $matches)) {
                return $matches[1];
            }
            return $value;

        case 'youtube':
            // Handle @username or channel ID
            if (preg_match('/youtube\.com\/@(.+?)(?:\/|$|\?)/', $value, $matches)) {
                return '@' . $matches[1];
            }
            if (preg_match('/youtube\.com\/channel\/(.+?)(?:\/|$|\?)/', $value, $matches)) {
                return $matches[1];
            }
            // If starts with @, keep it
            if (strpos($value, '@') === 0) {
                return $value;
            }
            return $value;
    }

    return $value;
}
