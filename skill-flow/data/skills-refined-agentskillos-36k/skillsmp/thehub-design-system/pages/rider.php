<?php
/**
 * V3 Single Rider Page - Redesigned Profile with Achievements & Series Standings
 */

// Define page type for sponsor placements
if (!defined('HUB_PAGE_TYPE')) {
    define('HUB_PAGE_TYPE', 'rider');
}

$db = hub_db();
$riderId = intval($pageInfo['params']['id'] ?? $_GET['id'] ?? 0);

// AJAX request for series content only
$isAjaxSeriesRequest = isset($_GET['ajax']) && $_GET['ajax'] === 'series';

// Check if current user is viewing their own profile
$currentUser = function_exists('hub_current_user') ? hub_current_user() : null;
$isOwnProfile = $currentUser && isset($currentUser['id']) && $currentUser['id'] == $riderId;

// Include rebuild functions for achievements
$rebuildPath = dirname(__DIR__) . '/includes/rebuild-rider-stats.php';
if (file_exists($rebuildPath)) {
    require_once $rebuildPath;
}

// Include new achievements system
$achievementsPath = dirname(__DIR__) . '/includes/achievements.php';
if (file_exists($achievementsPath)) {
    require_once $achievementsPath;
}

// Include ranking functions
$rankingFunctionsLoaded = false;
$rankingPaths = [
    dirname(__DIR__) . '/includes/ranking_functions.php',
    __DIR__ . '/../includes/ranking_functions.php',
];
foreach ($rankingPaths as $path) {
    if (file_exists($path)) {
        require_once $path;
        $rankingFunctionsLoaded = true;
        break;
    }
}

// Include avatar helper functions
$avatarHelperPath = dirname(__DIR__) . '/includes/get-avatar.php';
if (file_exists($avatarHelperPath)) {
    require_once $avatarHelperPath;
}

if (!$riderId) {
    header('Location: /riders');
    exit;
}

try {
    // Try to fetch rider with new profile fields first
    $rider = null;
    $hasNewColumns = true;

    try {
        $stmt = $db->prepare("
            SELECT
                r.id, r.firstname, r.lastname, r.birth_year, r.gender, r.nationality, r.email, r.password,
                r.license_number, r.license_type, r.license_year, r.license_valid_until, r.gravity_id, r.active,
                r.social_instagram, r.social_facebook, r.social_strava, r.social_youtube, r.social_tiktok,
                r.stats_total_starts, r.stats_total_finished, r.stats_total_wins, r.stats_total_podiums,
                r.first_season, r.experience_level, r.profile_image_url, r.avatar_url,
                c.id as club_id, c.name as club_name, c.city as club_city
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.id = ?
        ");
        $stmt->execute([$riderId]);
        $rider = $stmt->fetch(PDO::FETCH_ASSOC);

        // Try to fetch artist name columns separately (may not exist)
        try {
            $anonStmt = $db->prepare("SELECT is_anonymous, anonymous_source, merged_into_rider_id FROM riders WHERE id = ?");
            $anonStmt->execute([$riderId]);
            $anonData = $anonStmt->fetch(PDO::FETCH_ASSOC);
            if ($anonData && $rider) {
                $rider['is_anonymous'] = $anonData['is_anonymous'];
                $rider['anonymous_source'] = $anonData['anonymous_source'];
                $rider['merged_into_rider_id'] = $anonData['merged_into_rider_id'];
            }
        } catch (PDOException $e2) {
            // Columns don't exist - set defaults
            if ($rider) {
                $rider['is_anonymous'] = 0;
                $rider['anonymous_source'] = null;
                $rider['merged_into_rider_id'] = null;
            }
        }
    } catch (PDOException $e) {
        // New columns don't exist yet - use basic query
        $hasNewColumns = false;
    }

    // Fallback to basic query if new columns don't exist
    if (!$rider && !$hasNewColumns) {
        $stmt = $db->prepare("
            SELECT
                r.id, r.firstname, r.lastname, r.birth_year, r.gender, r.nationality, r.email, r.password,
                r.license_number, r.license_type, r.license_year, r.license_valid_until, r.gravity_id, r.active,
                c.id as club_id, c.name as club_name, c.city as club_city
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.id = ?
        ");
        $stmt->execute([$riderId]);
        $rider = $stmt->fetch(PDO::FETCH_ASSOC);

        // Set defaults for missing columns
        if ($rider) {
            $rider['social_instagram'] = null;
            $rider['social_facebook'] = null;
            $rider['social_strava'] = null;
            $rider['social_youtube'] = null;
            $rider['social_tiktok'] = null;
            $rider['stats_total_starts'] = 0;
            $rider['stats_total_finished'] = 0;
            $rider['stats_total_wins'] = 0;
            $rider['stats_total_podiums'] = 0;
            $rider['first_season'] = null;
            $rider['experience_level'] = 1;
            $rider['profile_image_url'] = null;
            $rider['avatar_url'] = null;
            $rider['is_anonymous'] = 0;
            $rider['anonymous_source'] = null;
            $rider['merged_into_rider_id'] = null;
        }
    }

    if (!$rider) {
        // Show rider-specific not found page
        http_response_code(404);
        ?>
        <div class="page-grid">
            <section class="card grid-full text-center p-lg">
                <div class="text-4xl mb-md"><i data-lucide="user-x"></i></div>
                <h1 class="text-2xl font-bold mb-sm">Åkare hittades inte</h1>
                <p class="text-secondary mb-lg">Åkare med ID <code class="code"><?= $riderId ?></code> finns inte i databasen.</p>
                <div class="flex justify-center gap-md">
                    <a href="/database" class="btn btn--primary">Sök åkare</a>
                    <a href="/riders" class="btn btn--secondary">Visa alla åkare</a>
                </div>
            </section>
        </div>
        <?php
        return;
    }

    // Always check rider_club_seasons for current year - this takes precedence over riders.club_id
    // because rider_club_seasons represents the actual club for each season
    $currentYear = (int)date('Y');

    // First try current year from rider_club_seasons
    $seasonClub = $db->prepare("
        SELECT rcs.club_id, c.name as club_name, c.city as club_city
        FROM rider_club_seasons rcs
        JOIN clubs c ON rcs.club_id = c.id
        WHERE rcs.rider_id = ? AND rcs.season_year = ?
        LIMIT 1
    ");
    $seasonClub->execute([$riderId, $currentYear]);
    $clubFromSeason = $seasonClub->fetch(PDO::FETCH_ASSOC);

    // If found in rider_club_seasons for current year, use that
    if ($clubFromSeason) {
        $rider['club_id'] = $clubFromSeason['club_id'];
        $rider['club_name'] = $clubFromSeason['club_name'];
        $rider['club_city'] = $clubFromSeason['club_city'];
    }
    // If no current year entry and no club from riders table, try latest year
    elseif (empty($rider['club_id'])) {
        $seasonClub = $db->prepare("
            SELECT rcs.club_id, c.name as club_name, c.city as club_city
            FROM rider_club_seasons rcs
            JOIN clubs c ON rcs.club_id = c.id
            WHERE rcs.rider_id = ?
            ORDER BY rcs.season_year DESC
            LIMIT 1
        ");
        $seasonClub->execute([$riderId]);
        $clubFromSeason = $seasonClub->fetch(PDO::FETCH_ASSOC);

        if ($clubFromSeason) {
            $rider['club_id'] = $clubFromSeason['club_id'];
            $rider['club_name'] = $clubFromSeason['club_name'];
            $rider['club_city'] = $clubFromSeason['club_city'];
        }
    }

    // Fetch club membership history
    $clubHistoryStmt = $db->prepare("
        SELECT rcs.season_year, rcs.club_id, c.name as club_name, rcs.locked,
               (SELECT COUNT(*) FROM results res
                JOIN events e ON res.event_id = e.id
                WHERE res.cyclist_id = ? AND YEAR(e.date) = rcs.season_year AND res.status != 'dns') as results_count
        FROM rider_club_seasons rcs
        JOIN clubs c ON rcs.club_id = c.id
        WHERE rcs.rider_id = ?
        ORDER BY rcs.season_year DESC
    ");
    $clubHistoryStmt->execute([$riderId, $riderId]);
    $clubHistory = $clubHistoryStmt->fetchAll(PDO::FETCH_ASSOC);

    // Fetch rider's results
    $stmt = $db->prepare("
        SELECT
            res.id, res.finish_time, res.status, res.points, res.position,
            res.event_id, res.class_id,
            e.id as event_id, e.name as event_name, e.date as event_date, e.location,
            s.id as series_id, s.name as series_name,
            sb.accent_color as series_color,
            cls.display_name as class_name,
            COALESCE(cls.awards_points, 1) as awards_podiums,
            CASE WHEN COALESCE(cls.awards_points, 1) = 0 THEN 1 ELSE 0 END as is_motion
        FROM results res
        JOIN events e ON res.event_id = e.id
        LEFT JOIN series s ON e.series_id = s.id
        LEFT JOIN series_brands sb ON s.brand_id = sb.id
        LEFT JOIN classes c ON res.class_id = c.id
        LEFT JOIN classes cls ON res.class_id = cls.id
        WHERE res.cyclist_id = ? AND res.status != 'dns'
        ORDER BY e.date DESC
    ");
    $stmt->execute([$riderId]);
    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Separate competitive and motion results
    $competitiveResults = array_filter($results, fn($r) => !$r['is_motion']);
    $motionResults = array_filter($results, fn($r) => $r['is_motion']);
    $hasCompetitiveResults = count($competitiveResults) > 0;

    // Motion stats (for highlight section)
    $motionStarts = count($motionResults);
    $motionFinished = count(array_filter($motionResults, fn($r) => $r['status'] === 'finished'));

    // Calculate stats from competitive results only (not motion)
    $totalStarts = count($competitiveResults);
    $finishedRaces = count(array_filter($competitiveResults, fn($r) => $r['status'] === 'finished'));
    $wins = count(array_filter($competitiveResults, fn($r) => $r['position'] == 1 && $r['status'] === 'finished'));
    $podiums = count(array_filter($competitiveResults, fn($r) => $r['position'] <= 3 && $r['status'] === 'finished'));

    // === TREND SECTION DATA ===

    // 1. Form curve - Last 10 races with positions and relative placement
    $finishedResults = array_filter($results, fn($r) => $r['status'] === 'finished' && $r['position'] > 0);
    $formResultsRaw = array_slice($finishedResults, 0, 10);
    $formResultsRaw = array_reverse($formResultsRaw); // Chronological order (oldest first)

    // Calculate relative position (position/total) for each race
    $formResults = [];
    $runningSum = 0;
    $runningCount = 0;

    foreach ($formResultsRaw as $idx => $fr) {
        // Get total participants in same class for this event
        $totalInClass = 1;
        try {
            $countStmt = $db->prepare("
                SELECT COUNT(*) as cnt
                FROM results
                WHERE event_id = ? AND class_id = ? AND status = 'finished'
            ");
            $countStmt->execute([$fr['event_id'], $fr['class_id']]);
            $countResult = $countStmt->fetch(PDO::FETCH_ASSOC);
            if ($countResult && $countResult['cnt'] > 0) {
                $totalInClass = $countResult['cnt'];
            }
        } catch (Exception $e) {}

        // Calculate relative position (lower is better, 0.0 = 1st, 1.0 = last)
        $relativePos = $totalInClass > 1 ? ($fr['position'] - 1) / ($totalInClass - 1) : 0;

        // Running average of position/total
        $runningSum += $fr['position'] / $totalInClass;
        $runningCount++;
        $runningAvg = $runningSum / $runningCount;

        $formResults[] = array_merge($fr, [
            'total_in_class' => $totalInClass,
            'relative_pos' => $relativePos,
            'running_avg' => $runningAvg
        ]);
    }

    // Calculate form trend (compare avg of first half vs second half)
    $formTrend = 'stable';
    if (count($formResults) >= 3) {
        $midPoint = (int)(count($formResults) / 2);
        $firstHalf = array_slice($formResults, 0, $midPoint);
        $secondHalf = array_slice($formResults, -$midPoint);

        $firstAvg = count($firstHalf) > 0 ? array_sum(array_column($firstHalf, 'position')) / count($firstHalf) : 0;
        $secondAvg = count($secondHalf) > 0 ? array_sum(array_column($secondHalf, 'position')) / count($secondHalf) : 0;

        // Lower position is better (1st > 2nd > 3rd)
        if ($secondAvg < $firstAvg - 1) {
            $formTrend = 'up'; // Improving (lower positions)
        } elseif ($secondAvg > $firstAvg + 1) {
            $formTrend = 'down'; // Declining (higher positions)
        }
    }

    // 2. Season Highlights calculation
    $highlights = [];

    // Win rate
    $winRate = $totalStarts > 0 ? round(($wins / $totalStarts) * 100) : 0;
    if ($winRate >= 10) {
        $highlights[] = [
            'icon' => 'trophy',
            'text' => $winRate . '% win rate',
            'type' => 'winrate'
        ];
    }

    // Podium streak (consecutive top-3 finishes)
    $currentStreak = 0;
    foreach ($results as $r) {
        if ($r['status'] === 'finished' && $r['position'] <= 3) {
            $currentStreak++;
        } else {
            break;
        }
    }
    if ($currentStreak >= 2) {
        $highlights[] = [
            'icon' => 'trending-up',
            'text' => $currentStreak . ' pallplatser i rad',
            'type' => 'streak',
            'active' => true
        ];
    }

    // Best result
    $bestResult = null;
    foreach ($finishedResults as $r) {
        if ($r['position'] == 1) {
            $bestResult = $r;
            break;
        }
    }
    if (!$bestResult && !empty($finishedResults)) {
        // Find lowest position
        $bestPos = PHP_INT_MAX;
        foreach ($finishedResults as $r) {
            if ($r['position'] < $bestPos) {
                $bestPos = $r['position'];
                $bestResult = $r;
            }
        }
    }
    if ($bestResult) {
        $posText = $bestResult['position'] == 1 ? '1:a' : ($bestResult['position'] == 2 ? '2:a' : ($bestResult['position'] == 3 ? '3:e' : $bestResult['position'] . ':e'));
        $highlights[] = [
            'icon' => 'star',
            'text' => 'Bästa: ' . $posText . ' ' . htmlspecialchars($bestResult['event_name']),
            'type' => 'best'
        ];
    }

    // Head-to-head statistics (riders beaten percentage)
    // Calculate from results: for each event, count riders with worse position
    $totalRidersBeaten = 0;
    $totalCompetitors = 0;
    foreach ($finishedResults as $r) {
        if (isset($r['event_id'])) {
            // Count riders in same event with worse position
            $eventStmt = $db->prepare("
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN position > ? THEN 1 ELSE 0 END) as beaten
                FROM results
                WHERE event_id = ? AND status = 'finished' AND cyclist_id != ?
            ");
            $eventStmt->execute([$r['position'], $r['event_id'], $riderId]);
            $eventStats = $eventStmt->fetch(PDO::FETCH_ASSOC);
            if ($eventStats) {
                $totalCompetitors += $eventStats['total'];
                $totalRidersBeaten += $eventStats['beaten'];
            }
        }
    }
    $h2hPercent = $totalCompetitors > 0 ? round(($totalRidersBeaten / $totalCompetitors) * 100) : 0;
    if ($h2hPercent >= 40 && $totalCompetitors >= 5) {
        $highlights[] = [
            'icon' => 'users',
            'text' => 'Slagit ' . $h2hPercent . '% av motståndare',
            'type' => 'h2h'
        ];
    }

    // Ensure we have at least some highlights
    if (empty($highlights) && $totalStarts > 0) {
        $highlights[] = [
            'icon' => 'bike',
            'text' => $totalStarts . ' starter denna säsong',
            'type' => 'starts'
        ];
    }

    // 3. Ranking history - Get historical positions from snapshots
    $rankingHistory = [];
    $rankingHistoryFull = []; // Full history for "Visa historik"
    $rankingHistory24m = [];  // Last 24 months for main chart
    if ($rankingFunctionsLoaded) {
        try {
            // Get ALL ranking snapshots
            $historyStmt = $db->prepare("
                SELECT
                    snapshot_date,
                    DATE_FORMAT(snapshot_date, '%Y-%m') as month,
                    DATE_FORMAT(snapshot_date, '%b') as month_short,
                    ranking_position,
                    total_ranking_points
                FROM ranking_snapshots
                WHERE rider_id = ? AND discipline = 'GRAVITY'
                ORDER BY snapshot_date ASC
            ");
            $historyStmt->execute([$riderId]);
            $allSnapshots = $historyStmt->fetchAll(PDO::FETCH_ASSOC);

            // Store full history for "Visa historik" section
            $rankingHistoryFull = $allSnapshots;

            // Filter to last 24 months for main chart (one point per month)
            // Use latest snapshot date as reference (not today's date)
            $latestSnapshotDate = !empty($allSnapshots) ? end($allSnapshots)['snapshot_date'] : date('Y-m-d');
            $cutoff24m = date('Y-m-d', strtotime($latestSnapshotDate . ' -24 months'));

            // First filter to 24 months, then group by month (take latest per month)
            $byMonth24m = [];
            foreach ($allSnapshots as $snap) {
                if ($snap['snapshot_date'] >= $cutoff24m) {
                    $byMonth24m[$snap['month']] = $snap;
                }
            }
            $rankingHistory24m = array_values($byMonth24m);

            // Group by month for compact display (take latest per month)
            $byMonth = [];
            foreach ($allSnapshots as $snap) {
                $byMonth[$snap['month']] = $snap;
            }
            $rankingHistory = array_values($byMonth);

            // Limit to last 6 entries for the compact view
            $rankingHistory = array_slice($rankingHistory, -6);
        } catch (Exception $e) {
            // Ignore errors
        }
    }

    // Calculate ranking change from start
    $rankingChange = 0;
    if (!empty($rankingHistory) && $rankingPosition) {
        $startPosition = $rankingHistory[0]['ranking_position'] ?? $rankingPosition;
        $rankingChange = $startPosition - $rankingPosition; // Positive = improved
    }

    // Calculate age
    $currentYear = date('Y');
    $age = ($rider['birth_year'] && $rider['birth_year'] > 0) ? ($currentYear - $rider['birth_year']) : null;

    // Get achievements
    $achievements = [];
    if (function_exists('getRiderAchievements')) {
        $achievements = getRiderAchievements($db, $riderId);
    }

    // Get detailed achievements (for modal display)
    $detailedAchievements = [];
    if (function_exists('getAllDetailedAchievements')) {
        $detailedAchievements = getAllDetailedAchievements($db, $riderId);
    }

    // Get social profiles
    $socialProfiles = [];
    if (function_exists('getRiderSocialProfiles')) {
        $socialProfiles = getRiderSocialProfiles($db, $riderId);
    }

    // Get available years for this rider (for series year selector)
    $yearsStmt = $db->prepare("
        SELECT DISTINCT YEAR(e.date) as year
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE r.cyclist_id = ? AND r.status = 'finished'
        ORDER BY year DESC
    ");
    $yearsStmt->execute([$riderId]);
    $availableYearsData = $yearsStmt->fetchAll(PDO::FETCH_ASSOC);
    $availableYears = array_column($availableYearsData, 'year');

    // Get selected year from URL parameter (default to current year)
    $selectedSeriesYear = isset($_GET['series_year']) ? intval($_GET['series_year']) : (int)date('Y');
    // Ensure year is valid
    if (!in_array($selectedSeriesYear, $availableYears) && !empty($availableYears)) {
        $selectedSeriesYear = $availableYears[0]; // Use most recent year
    }

    // Get series standings for selected year
    $seriesStandings = [];
    if (function_exists('getRiderSeriesStandings')) {
        $seriesStandings = getRiderSeriesStandings($db, $riderId, $selectedSeriesYear);
    }

    // Get ranking position
    $rankingPosition = null;
    $rankingPoints = 0;
    $rankingEvents = [];
    $parentDb = function_exists('getDB') ? getDB() : null;
    if ($rankingFunctionsLoaded && $parentDb && function_exists('getRiderRankingDetails')) {
        $riderRankingDetails = getRiderRankingDetails($parentDb, $riderId, 'GRAVITY');
        if ($riderRankingDetails) {
            $rankingPoints = $riderRankingDetails['total_ranking_points'] ?? 0;
            $rankingPosition = $riderRankingDetails['ranking_position'] ?? null;

            // Use events from ranking details (already has multipliers calculated)
            // Sort by weighted_points and take top results
            $allEvents = $riderRankingDetails['events'] ?? [];
            usort($allEvents, function($a, $b) {
                return ($b['weighted_points'] ?? 0) <=> ($a['weighted_points'] ?? 0);
            });
            $rankingEvents = array_slice($allEvents, 0, 10); // Top 10 events

            // Group events by month for modal display with dividers
            $rankingEventsByMonth = [];
            $swedishMonths = ['januari', 'februari', 'mars', 'april', 'maj', 'juni', 'juli', 'augusti', 'september', 'oktober', 'november', 'december'];

            // Sort all events by date (newest first) for modal display
            $allEventsSortedByDate = $allEvents;
            usort($allEventsSortedByDate, function($a, $b) {
                return strtotime($b['event_date'] ?? '2000-01-01') <=> strtotime($a['event_date'] ?? '2000-01-01');
            });

            foreach ($allEventsSortedByDate as $event) {
                $eventDate = strtotime($event['event_date'] ?? '2000-01-01');
                $monthKey = date('Y-m', $eventDate);
                if (!isset($rankingEventsByMonth[$monthKey])) {
                    $monthNum = (int)date('n', $eventDate) - 1;
                    $rankingEventsByMonth[$monthKey] = [
                        'month_label' => ucfirst($swedishMonths[$monthNum]) . ' ' . date('Y', $eventDate),
                        'events' => [],
                        'total_points' => 0,
                        'position_change' => null
                    ];
                }
                $rankingEventsByMonth[$monthKey]['events'][] = $event;
                $rankingEventsByMonth[$monthKey]['total_points'] += ($event['weighted_points'] ?? 0);
            }

            // Calculate position change per month from ranking history
            if (!empty($rankingHistoryFull)) {
                // Build map of month -> position at end of that month
                $positionByMonth = [];
                foreach ($rankingHistoryFull as $snap) {
                    $positionByMonth[$snap['month']] = (int)$snap['ranking_position'];
                }

                // Get sorted list of months
                $monthKeys = array_keys($positionByMonth);
                sort($monthKeys);

                // Calculate position change for each month (compared to previous month)
                for ($i = 0; $i < count($monthKeys); $i++) {
                    $month = $monthKeys[$i];
                    $currentPos = $positionByMonth[$month];

                    if ($i > 0) {
                        $prevMonth = $monthKeys[$i - 1];
                        $prevPos = $positionByMonth[$prevMonth];
                        // Positive change = improved (lower position number is better)
                        $change = $prevPos - $currentPos;

                        if (isset($rankingEventsByMonth[$month])) {
                            $rankingEventsByMonth[$month]['position_change'] = $change;
                        }
                    }
                }
            }
        }
    }

    // Experience level info
    $experienceLevel = $rider['experience_level'] ?? 1;
    $experienceInfo = [
        1 => ['name' => '1:a året', 'class' => 'level-1'],
        2 => ['name' => '2:a året', 'class' => 'level-2'],
        3 => ['name' => 'Erfaren', 'class' => 'level-3'],
        4 => ['name' => 'Expert', 'class' => 'level-4'],
        5 => ['name' => 'Veteran', 'class' => 'level-5'],
        6 => ['name' => 'Legend', 'class' => 'level-6']
    ];
    $expInfo = $experienceInfo[$experienceLevel] ?? $experienceInfo[1];

    // Profile image URL or initials fallback
    // Prefer avatar_url (from ImgBB), fallback to profile_image_url
    $profileImageUrl = $rider['avatar_url'] ?? $rider['profile_image_url'] ?? null;

    // Calculate initials for fallback
    $initials = function_exists('get_rider_initials')
        ? get_rider_initials($rider)
        : strtoupper(substr($rider['firstname'] ?? '', 0, 1) . substr($rider['lastname'] ?? '', 0, 1));

    // If no stored image, use UI Avatars fallback
    if (!$profileImageUrl) {
        if (function_exists('get_rider_avatar')) {
            $profileImageUrl = get_rider_avatar($rider, 200);
        } else {
            // Fallback: Generate UI Avatars URL directly
            $fullNameForAvatar = trim(($rider['firstname'] ?? '') . ' ' . ($rider['lastname'] ?? ''));
            if (empty($fullNameForAvatar)) $fullNameForAvatar = 'Rider';
            $profileImageUrl = 'https://ui-avatars.com/api/?name=' . urlencode($fullNameForAvatar) . '&size=200&background=61CE70&color=ffffff&bold=true&format=svg';
        }
    }

    // Check license status
    $hasLicense = !empty($rider['license_type']);
    $licenseActive = false;
    if ($hasLicense) {
        if (!empty($rider['license_year']) && $rider['license_year'] >= date('Y')) {
            $licenseActive = true;
        } elseif (!empty($rider['license_valid_until']) && $rider['license_valid_until'] !== '0000-00-00') {
            $licenseActive = strtotime($rider['license_valid_until']) >= strtotime('today');
        }
    }

    // Check Gravity ID status
    $hasGravityId = !empty($rider['gravity_id']);

    // Check if this profile can be claimed or needs activation
    // Available to ALL visitors - not just logged in users
    $canClaimProfile = false;      // Profile without email - can connect email
    $canActivateProfile = false;   // Profile with email but no password - can activate
    $hasPendingClaim = false;
    $isArtistName = false;         // Is this an artist name / anonymous profile?
    $canClaimArtistName = false;   // Can logged-in user claim this artist name?
    $hasPendingArtistClaim = false;

    // Check super admin status for admin-only features
    $isSuperAdmin = function_exists('hub_is_super_admin') && hub_is_super_admin();
    if (!$isSuperAdmin && isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true) {
        $isSuperAdmin = ($_SESSION['admin_role'] ?? '') === 'super_admin';
    }

    // Check if this is an artist name / anonymous profile
    // Either by is_anonymous flag or by criteria (only firstname, no lastname/birthyear/club)
    $isArtistName = !empty($rider['is_anonymous']);
    if (!$isArtistName) {
        // Fallback: detect by criteria if column doesn't exist
        $isArtistName = !empty($rider['firstname'])
            && (empty($rider['lastname']) || $rider['lastname'] === '')
            && (empty($rider['birth_year']) || $rider['birth_year'] === 0)
            && empty($rider['club_id'])
            && empty($rider['email']);
    }

    // If artist name, check for claiming options
    if ($isArtistName) {
        // Check for pending artist name claims
        try {
            $artistClaimCheck = $db->prepare("
                SELECT id FROM artist_name_claims
                WHERE anonymous_rider_id = ? AND status = 'pending'
            ");
            $artistClaimCheck->execute([$riderId]);
            $hasPendingArtistClaim = $artistClaimCheck->fetch() !== false;
        } catch (Exception $e) {
            // Table might not exist yet
        }

        // Logged-in users can claim if no pending claim
        if (!$hasPendingArtistClaim && $currentUser && !$isOwnProfile) {
            $canClaimArtistName = true;
        }
    }

    // Anyone can see claim/activate buttons - the process requires email verification
    if (empty($rider['email'])) {
        // No email - show "Connect email" option
        // Check if there's already a pending claim for this profile
        try {
            $claimCheck = $db->prepare("
                SELECT id FROM rider_claims
                WHERE target_rider_id = ? AND status = 'pending'
            ");
            $claimCheck->execute([$riderId]);
            $hasPendingClaim = $claimCheck->fetch() !== false;

            if (!$hasPendingClaim) {
                $canClaimProfile = true;
            }
        } catch (Exception $e) {
            // Table might not exist yet
            $canClaimProfile = true; // Allow testing even without table
        }
    } else {
        // Has email - show "Activate account" option (sends password reset)
        $canActivateProfile = empty($rider['password']);
    }

} catch (Exception $e) {
    $error = $e->getMessage();
    $rider = null;
}

if (!$rider) {
    // Show rider-specific error page
    http_response_code(404);
    ?>
    <div class="page-grid">
        <section class="card grid-full text-center p-lg">
            <div class="text-4xl mb-md">🚴‍♂️❓</div>
            <h1 class="text-2xl font-bold mb-sm">Åkare hittades inte</h1>
            <p class="text-secondary mb-lg">Åkare med ID <code class="code"><?= $riderId ?></code> finns inte i databasen.</p>
            <?php if (isset($error)): ?>
            <p class="text-sm text-error mb-md">Fel: <?= htmlspecialchars($error) ?></p>
            <?php endif; ?>
            <div class="flex justify-center gap-md">
                <a href="/database" class="btn btn--primary">Sök åkare</a>
                <a href="/riders" class="btn btn--secondary">Visa alla åkare</a>
            </div>
        </section>
    </div>
    <?php
    return;
}

$fullName = htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']);
$gidNumber = '';
if ($rider['gravity_id']) {
    $gidNumber = preg_replace('/^.*?-?(\d+)$/', '$1', $rider['gravity_id']);
    $gidNumber = ltrim($gidNumber, '0') ?: '0';
}

// Process achievements for display
$achievementCounts = ['gold' => 0, 'silver' => 0, 'bronze' => 0, 'hot_streak' => 0];
$isSeriesLeader = false;
$isSeriesChampion = false;
$isSwedishChampion = false;
$swedishChampionCount = 0;
$seriesChampionCount = 0;
$finisher100 = false;

foreach ($achievements as $ach) {
    switch ($ach['achievement_type']) {
        case 'gold': $achievementCounts['gold'] = (int)$ach['achievement_value']; break;
        case 'silver': $achievementCounts['silver'] = (int)$ach['achievement_value']; break;
        case 'bronze': $achievementCounts['bronze'] = (int)$ach['achievement_value']; break;
        case 'hot_streak': $achievementCounts['hot_streak'] = (int)$ach['achievement_value']; break;
        case 'series_leader': $isSeriesLeader = true; break;
        case 'series_champion':
            $isSeriesChampion = true;
            $seriesChampionCount++; // Count each series championship
            break;
        case 'swedish_champion':
            $isSwedishChampion = true;
            $swedishChampionCount++; // Count each SM title (value is event name, not count)
            break;
        case 'finisher_100': $finisher100 = true; break;
    }
}

// Calculate finish rate
$finishRate = $totalStarts > 0 ? round(($finishedRaces / $totalStarts) * 100) : 0;
?>

<link rel="stylesheet" href="/assets/css/pages/rider.css?v=<?= filemtime(__DIR__ . '/../assets/css/pages/rider.css') ?>">
<style>
/* Medal icons in form card */
.form-medal-icon {
    width: 24px;
    height: 24px;
}
.form-position-badge {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 600;
    background: var(--color-bg-sunken);
    border-radius: var(--radius-full);
    color: var(--color-text-secondary);
}
/* Slimmer cards on mobile */
@media (max-width: 599px) {
    .card {
        padding: var(--space-sm) !important;
    }
    .card-section-title-sm {
        font-size: 0.75rem;
        margin-bottom: var(--space-xs);
    }
    .form-avg-compact {
        margin-bottom: var(--space-xs);
    }
    .form-avg-number {
        font-size: 1.5rem;
    }
    .form-mini-chart {
        height: 60px;
        margin-bottom: var(--space-xs);
    }
    .form-last-5 {
        gap: var(--space-2xs);
    }
    .highlights-card {
        padding: var(--space-sm) var(--space-md);
    }
    .highlight-item {
        padding: var(--space-xs) var(--space-sm);
    }
}
</style>

<!-- Global Sponsor: Header Banner -->
<?= render_global_sponsors('rider', 'header_banner', '') ?>

<!-- Global Sponsor: Content Top -->
<?= render_global_sponsors('rider', 'content_top', '') ?>

<!-- New 2-Column Layout -->
<div class="rider-profile-layout">
    <!-- LEFT COLUMN: Ranking, Form, Series -->
    <div class="left-column">

        <!-- STATS CARD - Tabbed Ranking/Form -->
        <?php
        // Prepare ranking chart data for Chart.js - MAIN CHART shows only last 24 months
        $hasRankingChart = false;
        $rankingChartLabels = [];
        $rankingChartData = [];
        $swedishMonthsShort = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec'];

        // Use 24-month filtered data for main chart (needs at least 1 data point)
        if ($rankingPosition && !empty($rankingHistory24m) && count($rankingHistory24m) >= 1) {
            $hasRankingChart = true;
            foreach ($rankingHistory24m as $rh) {
                $monthNum = isset($rh['month']) ? (int)date('n', strtotime($rh['month'] . '-01')) - 1 : 0;
                $rankingChartLabels[] = ucfirst($swedishMonthsShort[$monthNum % 12] ?? '');
                $rankingChartData[] = (int)$rh['ranking_position'];
            }
        }

        // Prepare form chart data for Chart.js
        $hasFormChart = $hasCompetitiveResults && !empty($formResults);
        $formChartLabels = [];
        $formChartData = [];
        $bestPos = 0;
        $avgDisplay = '0.0';
        $numResults = 0;

        if ($hasFormChart) {
            $chartResults = array_slice($formResults, -10);
            $positions = array_column($chartResults, 'position');
            $bestPos = min($positions);
            $avgPlacement = count($positions) > 0 ? array_sum($positions) / count($positions) : 0;
            $avgDisplay = number_format($avgPlacement, 1);
            $numResults = count($chartResults);

            foreach ($chartResults as $fr) {
                $eventDate = strtotime($fr['event_date'] ?? 'now');
                // Show date like "23 jun" instead of just month
                $dayNum = date('j', $eventDate);
                $monthShort = $swedishMonthsShort[(int)date('n', $eventDate) - 1] ?? '';
                $formChartLabels[] = $dayNum . ' ' . $monthShort;
                $formChartData[] = (int)$fr['position'];
            }
        }

        // Show card if ranking, form data, or ranking history exists
        // Ranking history should always be visible even without current ranking
        $hasRankingHistory = !empty($rankingHistoryFull);
        if ($rankingPosition || $hasFormChart || $hasRankingHistory):
        ?>
        <div class="card stats-tabbed-card">
            <div class="stats-tabs">
                <?php if ($rankingPosition || $hasRankingHistory): ?>
                <button class="stats-tab active" data-tab="ranking-tab">
                    <i data-lucide="trending-up"></i>
                    <span>Ranking</span>
                </button>
                <?php endif; ?>
                <?php if ($hasFormChart): ?>
                <button class="stats-tab <?= !$rankingPosition && !$hasRankingHistory ? 'active' : '' ?>" data-tab="form-tab">
                    <i data-lucide="activity"></i>
                    <span>Form</span>
                </button>
                <?php endif; ?>
            </div>

            <?php if ($rankingPosition || $hasRankingHistory): ?>
            <div class="stats-tab-content active" id="ranking-tab">
                <?php if ($rankingPosition): ?>
                <!-- Has current ranking -->
                <div class="dashboard-chart-header">
                    <div class="dashboard-chart-stats">
                        <div class="dashboard-stat">
                            <span class="dashboard-stat-value dashboard-stat-value--red">#<?= $rankingPosition ?></span>
                            <span class="dashboard-stat-label">Position</span>
                        </div>
                        <div class="dashboard-stat">
                            <span class="dashboard-stat-value"><?= number_format($rankingPoints, 0) ?></span>
                            <span class="dashboard-stat-label">Poäng</span>
                        </div>
                    </div>
                </div>
                <?php if ($hasRankingChart): ?>
                <div class="dashboard-chart-body">
                    <canvas id="rankingChart"></canvas>
                </div>
                <?php else: ?>
                <div class="dashboard-chart-body dashboard-chart-placeholder">
                    <p class="text-muted text-center" style="padding: var(--space-lg);">
                        <i data-lucide="clock" style="width: 24px; height: 24px; margin-bottom: var(--space-xs); opacity: 0.5;"></i><br>
                        Historik genereras nästa ranking-uppdatering
                    </p>
                </div>
                <?php endif; ?>
                <div class="dashboard-chart-footer">
                    <button type="button" class="btn-calc-ranking-inline" onclick="openRankingModal()">
                        <i data-lucide="calculator"></i>
                        <span>Visa uträkning</span>
                    </button>
                    <?php if ($hasRankingHistory): ?>
                    <button type="button" class="btn-calc-ranking-inline" onclick="openHistoryModal()">
                        <i data-lucide="history"></i>
                        <span>Visa historik</span>
                    </button>
                    <?php endif; ?>
                </div>
                <?php else: ?>
                <!-- No current ranking, but has history - show history-focused view -->
                <?php
                // Get last known position from history
                $lastHistoryEntry = end($rankingHistoryFull);
                $lastKnownPosition = $lastHistoryEntry['ranking_position'] ?? null;
                $lastKnownDate = $lastHistoryEntry['snapshot_date'] ?? null;
                $bestHistoryPosition = !empty($rankingHistoryFull) ? min(array_column($rankingHistoryFull, 'ranking_position')) : null;
                ?>
                <div class="dashboard-chart-header">
                    <div class="dashboard-chart-stats">
                        <div class="dashboard-stat">
                            <span class="dashboard-stat-value" style="color: var(--color-text);">#<?= $lastKnownPosition ?? '-' ?></span>
                            <span class="dashboard-stat-label">Senaste</span>
                        </div>
                        <div class="dashboard-stat">
                            <span class="dashboard-stat-value dashboard-stat-value--green">#<?= $bestHistoryPosition ?? '-' ?></span>
                            <span class="dashboard-stat-label">Bästa</span>
                        </div>
                    </div>
                </div>
                <div class="dashboard-chart-body dashboard-chart-placeholder">
                    <p class="text-muted text-center" style="padding: var(--space-lg);">
                        <i data-lucide="history" style="width: 24px; height: 24px; margin-bottom: var(--space-xs); opacity: 0.5;"></i><br>
                        Ingen aktuell ranking<br>
                        <small>Senast rankad: <?= $lastKnownDate ? date('j M Y', strtotime($lastKnownDate)) : 'okänt' ?></small>
                    </p>
                </div>
                <div class="dashboard-chart-footer">
                    <button type="button" class="btn-calc-ranking-inline" onclick="openHistoryModal()">
                        <i data-lucide="history"></i>
                        <span>Visa historik</span>
                    </button>
                </div>
                <?php endif; ?>
            </div>
            <?php endif; ?>

            <?php if ($hasFormChart): ?>
            <div class="stats-tab-content <?= !$rankingPosition && !$hasRankingHistory ? 'active' : '' ?>" id="form-tab">
                <div class="dashboard-chart-header">
                    <div class="dashboard-chart-stats">
                        <div class="dashboard-stat">
                            <span class="dashboard-stat-value dashboard-stat-value--green">#<?= $bestPos ?></span>
                            <span class="dashboard-stat-label">Bästa</span>
                        </div>
                        <div class="dashboard-stat">
                            <span class="dashboard-stat-value"><?= $avgDisplay ?></span>
                            <span class="dashboard-stat-label">Snitt</span>
                        </div>
                    </div>
                </div>
                <div class="dashboard-chart-body">
                    <canvas id="formChart"></canvas>
                </div>
                <div class="dashboard-chart-footer">
                    <span><?= $numResults ?> tävlingar</span>
                </div>
            </div>
            <?php endif; ?>
        </div>
        <?php endif; ?>

        <!-- SERIES STANDINGS CARD - Now in left column -->
        <?php if (!empty($availableYears)): ?>
        <div class="card series-card">
            <div class="series-header">
                <h3 class="card-section-title"><i data-lucide="trophy"></i> Serieställning</h3>
            </div>

            <!-- Year Filter Links -->
            <?php if (count($availableYears) > 1): ?>
            <div class="series-year-tabs">
                <?php foreach ($availableYears as $year): ?>
                <a href="/rider/<?= $riderId ?>?series_year=<?= $year ?>"
                   class="year-tab <?= $year == $selectedSeriesYear ? 'active' : '' ?>">
                    <?= $year ?>
                </a>
                <?php endforeach; ?>
            </div>
            <?php else: ?>
            <div class="series-year-tabs">
                <span class="year-tab active"><?= $selectedSeriesYear ?></span>
            </div>
            <?php endif; ?>

            <div id="seriesContent">

            <?php if (!empty($seriesStandings)): ?>
            <!-- Series tabs -->
            <div class="series-tabs">
                <?php foreach ($seriesStandings as $idx => $standing): ?>
                <button class="series-tab-btn <?= $idx === 0 ? 'active' : '' ?>" data-target="series-<?= $idx ?>">
                    <span class="series-dot" style="background: <?= htmlspecialchars($standing['series_color'] ?? 'var(--color-accent)') ?>"></span>
                    <span><?= htmlspecialchars($standing['series_name']) ?></span>
                </button>
                <?php endforeach; ?>
            </div>

            <!-- Series content panels -->
            <?php foreach ($seriesStandings as $idx => $standing):
                // Get events for this series (filtered by year)
                $eventsStmt = $db->prepare("
                    SELECT r.position, r.points, r.status, e.id as event_id, e.name as event_name, e.date as event_date
                    FROM results r
                    JOIN events e ON r.event_id = e.id
                    WHERE r.cyclist_id = ? AND e.series_id = ? AND r.class_id = ? AND YEAR(e.date) = ?
                    ORDER BY e.date DESC
                ");
                $eventsStmt->execute([$riderId, $standing['series_id'], $standing['class_id'], $selectedSeriesYear]);
                $seriesEvents = $eventsStmt->fetchAll(PDO::FETCH_ASSOC);

                // Calculate progress percentage (inverted - lower rank is better)
                $rankPercent = max(5, min(100, 100 - (($standing['ranking'] - 1) / max(1, $standing['total_riders'] - 1)) * 100));
            ?>
            <div class="series-panel <?= $idx === 0 ? 'active' : '' ?>" id="series-<?= $idx ?>">

                <!-- Position Header -->
                <div class="series-position-header">
                    <div class="series-rank-display">
                        <span class="series-rank-number">#<?= $standing['ranking'] ?></span>
                        <span class="series-rank-text">av <?= $standing['total_riders'] ?> i <?= htmlspecialchars($standing['class_name'] ?? 'klassen') ?></span>
                    </div>
                    <?php if ($standing['trend'] != 0): ?>
                    <div class="series-trend <?= $standing['trend'] > 0 ? 'trend-up' : 'trend-down' ?>">
                        <i data-lucide="<?= $standing['trend'] > 0 ? 'trending-up' : 'trending-down' ?>"></i>
                        <span><?= $standing['trend'] > 0 ? '+' : '' ?><?= $standing['trend'] ?></span>
                    </div>
                    <?php endif; ?>
                </div>

                <!-- Progress Bar -->
                <div class="series-progress-bar">
                    <div class="progress-track">
                        <div class="progress-fill" style="width: <?= $rankPercent ?>%; background: <?= htmlspecialchars($standing['series_color'] ?? 'var(--color-accent)') ?>"></div>
                    </div>
                    <div class="progress-labels">
                        <span>#<?= $standing['total_riders'] ?></span>
                        <span>#1</span>
                    </div>
                </div>

                <!-- Stats Grid -->
                <div class="series-stats-grid">
                    <div class="series-stat-box">
                        <span class="stat-value"><?= number_format($standing['total_points'], 1) ?></span>
                        <span class="stat-label">Poäng</span>
                    </div>
                    <div class="series-stat-box">
                        <span class="stat-value"><?= $standing['events_count'] ?></span>
                        <span class="stat-label">Tävlingar</span>
                    </div>
                    <div class="series-stat-box">
                        <span class="stat-value"><?= $standing['wins'] ?></span>
                        <span class="stat-label">Vinster</span>
                    </div>
                    <div class="series-stat-box">
                        <span class="stat-value"><?= $standing['podiums'] ?></span>
                        <span class="stat-label">Pallplatser</span>
                    </div>
                </div>

                <!-- Events List -->
                <?php if (!empty($seriesEvents)): ?>
                <div class="series-events-list">
                    <h4 class="series-events-header">Tävlingar</h4>
                    <div class="series-events-compact">
                    <?php foreach ($seriesEvents as $event):
                        $pos = (int)$event['position'];
                        $seriesColor = $standing['series_color'] ?? 'var(--color-accent)';
                    ?>
                    <a href="/calendar/<?= $event['event_id'] ?>" class="result-row" style="--result-accent: <?= htmlspecialchars($seriesColor) ?>">
                        <span class="result-accent-bar"></span>
                        <span class="result-pos <?= $pos <= 3 ? 'p' . $pos : '' ?>">
                            <?php if ($pos === 1): ?>
                            <svg class="medal-icon-sm" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="#FFD700" stroke="#DAA520" stroke-width="2"/><text x="18" y="23" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">1</text></svg>
                            <?php elseif ($pos === 2): ?>
                            <svg class="medal-icon-sm" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="#C0C0C0" stroke="#A9A9A9" stroke-width="2"/><text x="18" y="23" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">2</text></svg>
                            <?php elseif ($pos === 3): ?>
                            <svg class="medal-icon-sm" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="#CD7F32" stroke="#8B4513" stroke-width="2"/><text x="18" y="23" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">3</text></svg>
                            <?php else: ?>
                            <?= $pos ?>
                            <?php endif; ?>
                        </span>
                        <span class="result-date"><?= date('j M', strtotime($event['event_date'])) ?></span>
                        <span class="result-details">
                            <span class="result-name"><?= htmlspecialchars($event['event_name']) ?></span>
                        </span>
                        <?php if ($event['status'] === 'finished' && $event['points'] > 0): ?>
                        <span class="result-points"><?= number_format($event['points'], 1) ?>p</span>
                        <?php elseif ($event['status'] !== 'finished'): ?>
                        <span class="result-status"><?= htmlspecialchars($event['status']) ?></span>
                        <?php endif; ?>
                    </a>
                    <?php endforeach; ?>
                    </div>
                </div>
                <?php endif; ?>

            </div>
            <?php endforeach; ?>
            <?php else: ?>
            <!-- No series standings for this year -->
            <div class="series-empty-state">
                <i data-lucide="calendar-x" class="icon-xl text-muted"></i>
                <p class="text-muted">Inga serieresultat för <?= $selectedSeriesYear ?>.</p>
                <?php if ($selectedSeriesYear != date('Y') && in_array((int)date('Y'), $availableYears)): ?>
                <a href="#" onclick="loadSeriesYear(<?= date('Y') ?>); return false;" class="btn btn-ghost btn-sm">Visa aktuellt år</a>
                <?php endif; ?>
            </div>
            <?php endif; ?>
            </div><!-- /#seriesContent -->
        </div>
        <?php endif; ?>

        <!-- RESULT HISTORY - in left column -->
        <div class="card history-card">
            <h3 class="card-section-title"><i data-lucide="history"></i> Resultathistorik</h3>
            <?php if (empty($results)): ?>
            <div class="empty-state-small">
                <i data-lucide="flag"></i>
                <p>Inga resultat registrerade</p>
            </div>
            <?php else: ?>
            <div class="results-list-compact">
                <?php
                $currentYear = null;
                foreach ($results as $result):
                    $resultYear = date('Y', strtotime($result['event_date']));
                    if ($resultYear !== $currentYear):
                        $currentYear = $resultYear;
                ?>
                <div class="year-divider">
                    <span class="year-label"><?= $currentYear ?></span>
                    <span class="year-line"></span>
                </div>
                <?php endif; ?>
                <a href="/event/<?= $result['event_id'] ?>" class="result-row" <?php if (!empty($result['series_color'])): ?>style="--result-accent: <?= htmlspecialchars($result['series_color']) ?>;"<?php endif; ?>>
                    <span class="result-accent-bar"></span>
                    <?php if ($result['is_motion']): ?>
                    <span class="result-pos motion">
                        <i data-lucide="check"></i>
                    </span>
                    <?php else: ?>
                    <span class="result-pos <?= $result['status'] === 'finished' && $result['position'] <= 3 ? 'p' . $result['position'] : '' ?>">
                        <?php if ($result['status'] !== 'finished'): ?>
                            <?= strtoupper(substr($result['status'], 0, 3)) ?>
                        <?php elseif ($result['position'] == 1): ?>
                            <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon-sm">
                        <?php elseif ($result['position'] == 2): ?>
                            <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon-sm">
                        <?php elseif ($result['position'] == 3): ?>
                            <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon-sm">
                        <?php else: ?>
                            #<?= $result['position'] ?>
                        <?php endif; ?>
                    </span>
                    <?php endif; ?>
                    <span class="result-date"><?= date('j M', strtotime($result['event_date'])) ?></span>
                    <span class="result-details">
                        <span class="result-name"><?php
                            if (!empty($result['series_name'])) {
                                echo htmlspecialchars($result['series_name']) . ' - ';
                            }
                            echo htmlspecialchars($result['event_name']);
                        ?></span>
                        <span class="result-meta"><?= htmlspecialchars($result['location'] ?? '') ?><?= !empty($result['location']) && !empty($result['class_name']) ? ' · ' : '' ?><?= htmlspecialchars($result['class_name'] ?? '') ?></span>
                    </span>
                </a>
                <?php endforeach; ?>
            </div>
            <?php endif; ?>
        </div>

    </div><!-- End left-column -->

    <!-- RIGHT COLUMN: Profile, Highlights, Achievements -->
    <div class="right-column">

        <!-- PROFILE CARD - Portrait Style -->
        <div class="card profile-card-v4">
            <!-- Square Photo or Initials -->
            <div class="profile-photo-hero <?= $profileImageUrl ? '' : 'initials-bg' ?>">
                <?php if ($profileImageUrl): ?>
                    <img src="<?= htmlspecialchars($profileImageUrl) ?>" alt="<?= $fullName ?>" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                    <div class="profile-initials-fallback" style="display: none;"><?= htmlspecialchars($initials) ?></div>
                <?php else: ?>
                    <div class="profile-initials"><?= htmlspecialchars($initials) ?></div>
                <?php endif; ?>
            </div>

            <!-- Info Section -->
            <div class="profile-info-centered">
                <h1 class="profile-name-hero">
                    <?= $fullName ?>
                    <?php
                    $nationality = $rider['nationality'] ?? 'SWE';
                    $countryCode = strtolower($nationality);
                    ?>
                    <img src="https://flagcdn.com/24x18/<?= $countryCode === 'swe' ? 'se' : ($countryCode === 'nor' ? 'no' : ($countryCode === 'den' ? 'dk' : ($countryCode === 'fin' ? 'fi' : $countryCode))) ?>.png"
                         alt="<?= $nationality ?>"
                         class="profile-flag"
                         onerror="this.style.display='none'">
                </h1>
                <?php if ($age): ?><span class="profile-subtitle"><?= $age ?> ar</span><?php endif; ?>
                <?php if ($rider['club_name']): ?>
                <a href="/club/<?= $rider['club_id'] ?>" class="profile-club-link-hero"><?= htmlspecialchars($rider['club_name']) ?></a>
                <?php endif; ?>
                <?php if ($rider['license_number']): ?>
                <span class="profile-uci-text">UCI: <?= htmlspecialchars($rider['license_number']) ?></span>
                <?php endif; ?>
            </div>

            <!-- Status Badges Row - License and/or Gravity ID -->
            <?php if ($hasLicense || $hasGravityId): ?>
            <div class="profile-badges-row">
                <?php if ($hasLicense): ?>
                <div class="profile-status-badge <?= $licenseActive ? 'badge-active' : 'badge-inactive' ?>">
                    <i data-lucide="award" class="badge-icon"></i>
                    <span class="badge-label">Licens</span>
                    <span class="badge-value"><?= $rider['license_year'] ?: '-' ?></span>
                </div>
                <?php endif; ?>
                <?php if ($hasGravityId): ?>
                <div class="profile-status-badge badge-gravity-id">
                    <i data-lucide="badge-check" class="badge-icon"></i>
                    <span class="badge-label">Gravity ID</span>
                    <span class="badge-value"><?= htmlspecialchars($rider['gravity_id']) ?></span>
                </div>
                <?php endif; ?>
            </div>
            <?php endif; ?>

            <!-- Social Media Icons - Colored when active -->
            <div class="profile-social-simple">
                <a href="<?= $socialProfiles['instagram']['url'] ?? '#' ?>" class="social-icon-simple social-instagram <?= empty($socialProfiles['instagram']) ? 'empty' : '' ?>" title="Instagram" <?= !empty($socialProfiles['instagram']) ? 'target="_blank"' : '' ?>>
                    <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                </a>
                <a href="<?= $socialProfiles['strava']['url'] ?? '#' ?>" class="social-icon-simple social-strava <?= empty($socialProfiles['strava']) ? 'empty' : '' ?>" title="Strava" <?= !empty($socialProfiles['strava']) ? 'target="_blank"' : '' ?>>
                    <svg viewBox="0 0 24 24"><path d="M15.387 17.944l-2.089-4.116h-3.065L15.387 24l5.15-10.172h-3.066m-7.008-5.599l2.836 5.598h4.172L10.463 0l-7 13.828h4.169"/></svg>
                </a>
                <a href="<?= $socialProfiles['facebook']['url'] ?? '#' ?>" class="social-icon-simple social-facebook <?= empty($socialProfiles['facebook']) ? 'empty' : '' ?>" title="Facebook" <?= !empty($socialProfiles['facebook']) ? 'target="_blank"' : '' ?>>
                    <svg viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                </a>
                <a href="<?= $socialProfiles['youtube']['url'] ?? '#' ?>" class="social-icon-simple social-youtube <?= empty($socialProfiles['youtube']) ? 'empty' : '' ?>" title="YouTube" <?= !empty($socialProfiles['youtube']) ? 'target="_blank"' : '' ?>>
                    <svg viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                </a>
                <a href="<?= $socialProfiles['tiktok']['url'] ?? '#' ?>" class="social-icon-simple social-tiktok <?= empty($socialProfiles['tiktok']) ? 'empty' : '' ?>" title="TikTok" <?= !empty($socialProfiles['tiktok']) ? 'target="_blank"' : '' ?>>
                    <svg viewBox="0 0 24 24"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
                </a>
            </div>

            <!-- Action Buttons -->
            <div class="profile-actions-row">
                <button type="button" class="btn-action-outline" onclick="shareProfile(<?= $riderId ?>)">
                    <i data-lucide="share-2"></i>
                    <span>Dela</span>
                </button>
                <?php if ($canClaimProfile): ?>
                <button type="button" class="btn-action-outline btn-claim-profile" onclick="openClaimModal()" title="Koppla e-postadress till denna profil">
                    <i data-lucide="mail-plus"></i>
                    <span>Koppla e-post</span>
                </button>
                <?php elseif ($canActivateProfile): ?>
                <button type="button" class="btn-action-outline btn-activate-profile" onclick="openActivateModal()" title="Skicka aktiveringslänk till <?= htmlspecialchars($rider['email']) ?>">
                    <i data-lucide="user-check"></i>
                    <span>Aktivera konto</span>
                </button>
                <?php elseif ($hasPendingClaim): ?>
                <button type="button" class="btn-action-outline btn-claim-pending" disabled>
                    <i data-lucide="clock"></i>
                    <span>Väntande förfrågan</span>
                </button>
                <?php endif; ?>

                <?php if ($isArtistName && $canClaimArtistName): ?>
                <button type="button" class="btn-action-outline btn-artist-claim" onclick="openArtistClaimModal()" title="Gor ansprak pa detta artistnamn">
                    <i data-lucide="link"></i>
                    <span>Mitt artistnamn</span>
                </button>
                <?php elseif ($isArtistName && !$currentUser): ?>
                <button type="button" class="btn-action-outline btn-artist-claim" onclick="openArtistActivateModal()" title="Aktivera denna profil">
                    <i data-lucide="user-plus"></i>
                    <span>Aktivera profil</span>
                </button>
                <?php elseif ($isArtistName && $hasPendingArtistClaim): ?>
                <button type="button" class="btn-action-outline btn-claim-pending" disabled>
                    <i data-lucide="clock"></i>
                    <span>Claim väntar</span>
                </button>
                <?php endif; ?>

                <?php if (function_exists('hub_is_admin') && hub_is_admin()): ?>
                <a href="/admin/rider-edit.php?id=<?= $riderId ?>" class="btn-action-outline">
                    <i data-lucide="pencil"></i>
                    <span>Redigera</span>
                </a>
                <?php endif; ?>
            </div>
        </div>

        <!-- CLUB HISTORY CARD -->
        <?php if (!empty($clubHistory)): ?>
        <div class="card club-history-card">
            <h3 class="card-section-title-sm"><i data-lucide="history"></i> Klubbtillhörighet</h3>
            <div class="club-history-list" id="clubHistoryList">
                <?php foreach ($clubHistory as $ch): ?>
                <div class="club-history-item" id="club-season-<?= $riderId ?>-<?= $ch['season_year'] ?>">
                    <span class="club-history-year"><?= $ch['season_year'] ?></span>
                    <a href="/club/<?= $ch['club_id'] ?>" class="club-history-name"><?= htmlspecialchars($ch['club_name']) ?></a>
                    <span class="club-history-meta">
                        <?= $ch['results_count'] ?> resultat
                        <?php if ($ch['locked']): ?>
                        <i data-lucide="lock" style="width: 12px; height: 12px; color: var(--color-warning);"></i>
                        <?php endif; ?>
                    </span>
                    <?php if ($isSuperAdmin): ?>
                    <button type="button" class="btn-delete-club-season" onclick="deleteClubSeason(<?= $riderId ?>, <?= $ch['season_year'] ?>)" title="Radera klubbtillhörighet">
                        <i data-lucide="trash-2"></i>
                    </button>
                    <?php endif; ?>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
        <style>
        .club-history-card { padding: var(--space-md); }
        .club-history-list { display: flex; flex-direction: column; gap: var(--space-xs); }
        .club-history-item {
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            padding: var(--space-xs) 0;
            border-bottom: 1px solid var(--color-border);
        }
        .club-history-item:last-child { border-bottom: none; }
        .club-history-year {
            font-weight: 600;
            font-size: 14px;
            min-width: 50px;
        }
        .club-history-name {
            flex: 1;
            color: var(--color-text);
            text-decoration: none;
        }
        .club-history-name:hover { color: var(--color-accent); }
        .club-history-meta {
            font-size: 12px;
            color: var(--color-text);
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .btn-delete-club-season {
            background: none;
            border: none;
            color: var(--color-danger);
            cursor: pointer;
            padding: 4px;
            opacity: 0.6;
            transition: opacity 0.2s;
        }
        .btn-delete-club-season:hover { opacity: 1; }
        .btn-delete-club-season i { width: 14px; height: 14px; }
        </style>
        <?php endif; ?>

        <!-- HIGHLIGHTS CARD -->
        <div class="card highlights-card">
            <h3 class="card-section-title-sm"><i data-lucide="star"></i> Highlights</h3>
            <?php if (!empty($highlights)): ?>
            <div class="highlights-list">
                <?php foreach ($highlights as $hl): ?>
                <div class="highlight-item">
                    <i data-lucide="<?= htmlspecialchars($hl['icon']) ?>"></i>
                    <span><?= $hl['text'] ?></span>
                </div>
                <?php endforeach; ?>
            </div>
            <?php endif; ?>
        </div>

        <!-- ACHIEVEMENTS CARD -->
        <div class="card achievements-card">
            <link rel="stylesheet" href="/assets/css/achievements.css?v=<?= file_exists(dirname(__DIR__) . '/assets/css/achievements.css') ? filemtime(dirname(__DIR__) . '/assets/css/achievements.css') : time() ?>">
            <?php
            $riderStats = [
                'gold' => $achievementCounts['gold'],
                'silver' => $achievementCounts['silver'],
                'bronze' => $achievementCounts['bronze'],
                'hot_streak' => $achievementCounts['hot_streak'],
                'series_completed' => $finisher100 ? 1 : 0,
                'is_serieledare' => $isSeriesLeader,
                'series_wins' => $seriesChampionCount,
                'sm_wins' => $swedishChampionCount,
                'seasons_active' => $experienceLevel,
                'has_series_win' => $isSeriesChampion,
                'first_season_year' => $rider['first_season'] ?? date('Y')
            ];

            if (function_exists('renderRiderAchievements')) {
                echo renderRiderAchievements($db, $riderId, $riderStats);
            }
            ?>
        </div>

        <!-- Achievement Details Modal -->
        <?php if (!empty($detailedAchievements)): ?>
        <div id="achievementModal" class="ranking-modal-overlay" style="display:none;">
            <div class="ranking-modal" style="max-height: calc(100vh - var(--header-height, 60px) - 40px); max-width: 500px;">
                <div class="ranking-modal-header">
                    <h3 id="achievementModalTitle">
                        <i data-lucide="award"></i>
                        <span></span>
                    </h3>
                    <button type="button" class="ranking-modal-close" onclick="closeAchievementModal()">
                        <i data-lucide="x"></i>
                    </button>
                </div>
                <div class="ranking-modal-body" id="achievementModalBody">
                    <!-- Content populated by JS -->
                </div>
                <div class="modal-close-footer">
                    <button type="button" onclick="closeAchievementModal()" class="modal-close-btn">
                        <i data-lucide="x"></i>
                        Stäng
                    </button>
                </div>
            </div>
        </div>

        <script>
        const detailedAchievements = <?= json_encode($detailedAchievements) ?>;

        // Format discipline name for display
        function formatDiscipline(discipline) {
            const labels = {
                'enduro': 'Enduro',
                'downhill': 'Downhill',
                'dh': 'Downhill',
                'xc': 'Cross Country',
                'cross-country': 'Cross Country',
                'xco': 'XCO',
                'xcc': 'XCC',
                'e-mtb': 'E-MTB',
                'emtb': 'E-MTB'
            };
            return labels[discipline?.toLowerCase()] || discipline || '';
        }

        function openAchievementModal(achievementType) {
            const data = detailedAchievements[achievementType];
            if (!data || !data.items || data.items.length === 0) return;

            const modal = document.getElementById('achievementModal');
            const titleSpan = document.querySelector('#achievementModalTitle span');
            const body = document.getElementById('achievementModalBody');

            titleSpan.textContent = data.label;

            let html = '<div class="achievement-details-list">';
            data.items.forEach(item => {
                const year = item.season_year || '';
                const eventName = item.event_name || item.achievement_value || '';
                const seriesName = item.series_name || item.series_short_name || '';
                const discipline = item.discipline || '';
                const className = item.class_name || '';
                const eventId = item.event_id;
                const eventDate = item.event_date ? new Date(item.event_date).toLocaleDateString('sv-SE', {day: 'numeric', month: 'short', year: 'numeric'}) : '';

                // For championships, show discipline (Enduro, DH, XC) if no series name
                const categoryLabel = seriesName || (discipline ? formatDiscipline(discipline) : '');

                html += '<div class="achievement-detail-item">';
                if (eventId) {
                    html += `<a href="/event/${eventId}" class="achievement-detail-link">`;
                }
                html += `<div class="achievement-detail-content">`;
                if (categoryLabel || className) {
                    html += `<span class="achievement-detail-series">${[categoryLabel, className].filter(Boolean).join(' · ')}</span>`;
                }
                html += `<span class="achievement-detail-name">${eventName}</span>`;
                html += `<span class="achievement-detail-year">${eventDate || year}</span>`;
                html += `</div>`;
                if (eventId) {
                    html += `<i data-lucide="chevron-right" class="achievement-detail-arrow"></i></a>`;
                }
                html += '</div>';
            });
            html += '</div>';

            body.innerHTML = html;
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';

            if (typeof lucide !== 'undefined') lucide.createIcons();
        }

        function closeAchievementModal() {
            const modal = document.getElementById('achievementModal');
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = '';
            }
        }

        document.getElementById('achievementModal')?.addEventListener('click', function(e) {
            if (e.target === this) closeAchievementModal();
        });

        // ESC key to close achievement modal
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                const achievementModal = document.getElementById('achievementModal');
                if (achievementModal && achievementModal.style.display === 'flex') {
                    closeAchievementModal();
                }
            }
        });

        // Add click handlers to badges with data
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.badge-item.clickable').forEach(badge => {
                badge.addEventListener('click', function() {
                    const type = this.dataset.achievement;
                    if (type && detailedAchievements[type]) {
                        openAchievementModal(type);
                    }
                });
            });
        });
        </script>

        <style>
        .achievement-details-list {
            display: flex;
            flex-direction: column;
            gap: var(--space-sm);
        }
        .achievement-detail-item {
            background: var(--color-bg-secondary);
            border-radius: var(--radius-sm);
            overflow: hidden;
        }
        .achievement-detail-link {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: var(--space-md);
            text-decoration: none;
            color: inherit;
            transition: background 0.2s;
        }
        .achievement-detail-link:hover {
            background: var(--color-bg-hover);
        }
        .achievement-detail-content {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .achievement-detail-item:not(:has(a)) .achievement-detail-content {
            padding: var(--space-md);
        }
        .achievement-detail-series {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--color-text-secondary);
        }
        .achievement-detail-name {
            font-weight: 600;
            color: var(--color-text-primary);
        }
        .achievement-detail-year {
            font-size: 0.85rem;
            color: var(--color-text-secondary);
        }
        .achievement-detail-arrow {
            width: 20px;
            height: 20px;
            color: var(--color-text-secondary);
        }
        </style>
        <?php endif; ?>

    </div><!-- End right-column -->

</div><!-- End rider-profile-layout -->

<script>
// Stats Tab Switching (Ranking/Form)
document.querySelectorAll('.stats-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.stats-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.stats-tab-content').forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        const targetId = tab.dataset.tab;
        document.getElementById(targetId)?.classList.add('active');
    });
});

// Series Tab Switching
document.querySelectorAll('.series-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.series-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        const targetId = tab.dataset.target;
        document.querySelectorAll('.series-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        document.getElementById(targetId).classList.add('active');
    });
});

// Share Profile Function
function shareProfile(riderId) {
    const shareUrl = window.location.origin + '/rider/' + riderId;
    const imageUrl = window.location.origin + '/api/share-image.php?rider_id=' + riderId;

    // Check if Web Share API is available
    if (navigator.share) {
        navigator.share({
            title: document.title,
            text: 'Kolla in min GravitySeries-profil!',
            url: shareUrl
        }).catch(() => {});
    } else {
        // Show modal with share options
        showShareModal(shareUrl, imageUrl, riderId);
    }
}

function showShareModal(shareUrl, imageUrl, riderId) {
    // Create modal
    const modal = document.createElement('div');
    modal.className = 'share-modal-overlay';
    modal.innerHTML = `
        <div class="share-modal">
            <div class="share-modal-header">
                <h3>Dela profil</h3>
                <button class="share-modal-close" onclick="this.closest('.share-modal-overlay').remove()">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            </div>
            <div class="share-modal-body">
                <div class="share-preview">
                    <img src="${imageUrl}" alt="Dela bild" loading="lazy">
                </div>
                <div class="share-options">
                    <a href="${imageUrl}" download="gravityseries-stats.png" class="share-option">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="7 10 12 15 17 10"/>
                            <line x1="12" y1="15" x2="12" y2="3"/>
                        </svg>
                        Ladda ner bild
                    </a>
                    <button onclick="copyToClipboard('${shareUrl}')" class="share-option">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                        </svg>
                        Kopiera länk
                    </button>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    // Close on overlay click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.remove();
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show success feedback
        const btn = event.target.closest('.share-option');
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Kopierat!';
        setTimeout(() => { btn.innerHTML = originalHtml; }, 2000);
    });
}

// Ranking Modal Functions
function openRankingModal() {
    const modal = document.getElementById('rankingModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeRankingModal() {
    const modal = document.getElementById('rankingModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Close modal on overlay click
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('rankingModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeRankingModal();
            }
        });
    }
});

// Close modal on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeRankingModal();
    }
});

// Series Tabs Switching
document.addEventListener('DOMContentLoaded', function() {
    const seriesTabs = document.querySelectorAll('.series-tab-btn');
    seriesTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');

            // Remove active class from all tabs and panels
            document.querySelectorAll('.series-tab-btn').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.series-panel').forEach(p => p.classList.remove('active'));

            // Add active class to clicked tab and corresponding panel
            this.classList.add('active');
            const targetPanel = document.getElementById(targetId);
            if (targetPanel) {
                targetPanel.classList.add('active');
            }
        });
    });
});
</script>

<?php if ($rankingPosition): ?>
<!-- Ranking Calculation Modal -->
<div id="rankingModal" class="ranking-modal-overlay">
    <div class="ranking-modal" style="max-height: calc(100vh - var(--header-height, 60px) - 40px);">
        <div class="ranking-modal-header">
            <h3>
                <i data-lucide="calculator"></i>
                Rankinguträkning
            </h3>
            <button type="button" class="ranking-modal-close" onclick="closeRankingModal()">
                <i data-lucide="x"></i>
            </button>
        </div>
        <div class="ranking-modal-body">
            <div class="ranking-modal-summary">
                <span class="summary-label">Total poäng</span>
                <span class="summary-value"><?= number_format($rankingPoints, 1) ?> p</span>
            </div>

            <div class="modal-formula-hint">
                <i data-lucide="info"></i>
                Formel: Baspoäng × Fältfaktor × Eventtypfaktor × Tidsfaktor
            </div>

            <div class="modal-events-list">
                <?php if (!empty($rankingEventsByMonth)): ?>
                <?php foreach ($rankingEventsByMonth as $monthKey => $monthData): ?>
                <div class="modal-month-divider">
                    <span class="modal-month-label"><?= htmlspecialchars($monthData['month_label']) ?></span>
                    <?php if ($monthData['position_change'] !== null): ?>
                    <span class="modal-month-change <?= $monthData['position_change'] > 0 ? 'positive' : ($monthData['position_change'] < 0 ? 'negative' : '') ?>">
                        <?= $monthData['position_change'] > 0 ? '+' : '' ?><?= $monthData['position_change'] ?> plac
                    </span>
                    <?php endif; ?>
                </div>
                <?php foreach ($monthData['events'] as $event): ?>
                <div class="modal-event-item">
                    <div class="modal-event-row">
                        <div class="modal-event-info">
                            <span class="modal-event-name"><?= htmlspecialchars($event['event_name'] ?? 'Event') ?></span>
                            <span class="modal-event-date"><?= date('j M Y', strtotime($event['event_date'])) ?></span>
                        </div>
                        <span class="modal-event-points">+<?= number_format($event['weighted_points'] ?? 0, 0) ?></span>
                    </div>
                    <div class="modal-calc-row">
                        <span class="modal-calc-item">
                            <span class="modal-calc-label">Bas:</span>
                            <span class="modal-calc-value"><?= number_format($event['original_points'] ?? 0, 0) ?></span>
                        </span>
                        <span class="modal-calc-op">×</span>
                        <span class="modal-calc-item">
                            <span class="modal-calc-label">Fält:</span>
                            <span class="modal-calc-value <?= ($event['field_multiplier'] ?? 1) < 1 ? 'dim' : '' ?>"><?= number_format(($event['field_multiplier'] ?? 1) * 100, 0) ?>%</span>
                        </span>
                        <span class="modal-calc-op">×</span>
                        <span class="modal-calc-item">
                            <span class="modal-calc-label">Typ:</span>
                            <span class="modal-calc-value <?= ($event['event_level_multiplier'] ?? 1) < 1 ? 'dim' : '' ?>"><?= number_format(($event['event_level_multiplier'] ?? 1) * 100, 0) ?>%</span>
                        </span>
                        <span class="modal-calc-op">×</span>
                        <span class="modal-calc-item">
                            <span class="modal-calc-label">Tid:</span>
                            <span class="modal-calc-value <?= ($event['time_multiplier'] ?? 1) < 1 ? 'dim' : '' ?>"><?= number_format(($event['time_multiplier'] ?? 1) * 100, 0) ?>%</span>
                        </span>
                    </div>
                </div>
                <?php endforeach; ?>
                <?php endforeach; ?>
                <?php elseif (!empty($rankingEvents)): ?>
                <?php foreach ($rankingEvents as $event): ?>
                <div class="modal-event-item">
                    <div class="modal-event-row">
                        <div class="modal-event-info">
                            <span class="modal-event-name"><?= htmlspecialchars($event['event_name'] ?? 'Event') ?></span>
                            <span class="modal-event-date"><?= date('j M Y', strtotime($event['event_date'])) ?></span>
                        </div>
                        <span class="modal-event-points">+<?= number_format($event['weighted_points'] ?? 0, 0) ?></span>
                    </div>
                </div>
                <?php endforeach; ?>
                <?php else: ?>
                <div class="modal-empty-state">
                    <i data-lucide="info"></i>
                    <p>Inga tävlingar hittades för beräkning ännu.</p>
                    <p class="modal-empty-hint">Rankingpoäng baseras på dina resultat i Gravity-tävlingar.</p>
                </div>
                <?php endif; ?>
            </div>

            <!-- Close button at bottom for better mobile UX -->
            <div class="modal-close-footer">
                <button type="button" onclick="closeRankingModal()" class="modal-close-btn">
                    <i data-lucide="x"></i>
                    Stäng
                </button>
            </div>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Ranking History Modal - Outside rankingPosition block so it shows for history-only riders -->
<?php if (!empty($rankingHistoryFull)): ?>
<div id="historyModal" class="ranking-modal-overlay">
    <div class="ranking-modal" style="max-height: calc(100vh - var(--header-height, 60px) - 40px); max-width: 800px;">
        <div class="ranking-modal-header">
            <h3>
                <i data-lucide="history"></i>
                Rankinghistorik
            </h3>
            <button type="button" class="ranking-modal-close" onclick="closeHistoryModal()">
                <i data-lucide="x"></i>
            </button>
        </div>
        <div class="ranking-modal-body">
            <?php
            // Prepare full history data for the modal chart
            $historyLabels = [];
            $historyData = [];
            $historyPoints = [];
            foreach ($rankingHistoryFull as $rh) {
                $date = strtotime($rh['snapshot_date'] ?? $rh['month'] . '-01');
                $historyLabels[] = date('M Y', $date);
                $historyData[] = (int)$rh['ranking_position'];
                $historyPoints[] = (float)($rh['total_ranking_points'] ?? 0);
            }

            // Find best and worst positions
            $bestHistoryPos = !empty($historyData) ? min($historyData) : 0;
            $worstHistoryPos = !empty($historyData) ? max($historyData) : 0;
            $firstPos = $historyData[0] ?? 0;
            $lastPos = end($historyData) ?: 0;
            $improvement = $firstPos - $lastPos;

            // Get the display position (current or last known)
            $displayPosition = $rankingPosition ?: $lastPos;
            $positionLabel = $rankingPosition ? 'Nuvarande position' : 'Senaste position';
            ?>

            <div class="ranking-modal-summary">
                <span class="summary-label"><?= $positionLabel ?></span>
                <span class="summary-value">#<?= $displayPosition ?></span>
            </div>

            <div class="history-stats-row">
                <div class="history-stat">
                    <span class="history-stat-value text-success">#<?= $bestHistoryPos ?></span>
                    <span class="history-stat-label">Bästa</span>
                </div>
                <div class="history-stat">
                    <span class="history-stat-value">#<?= $worstHistoryPos ?></span>
                    <span class="history-stat-label">Sämsta</span>
                </div>
                <div class="history-stat">
                    <span class="history-stat-value <?= $improvement > 0 ? 'text-success' : ($improvement < 0 ? 'text-danger' : '') ?>">
                        <?= $improvement > 0 ? '+' : '' ?><?= $improvement ?>
                    </span>
                    <span class="history-stat-label">Utveckling</span>
                </div>
                <div class="history-stat">
                    <span class="history-stat-value"><?= count($historyData) ?></span>
                    <span class="history-stat-label">Datapunkter</span>
                </div>
            </div>

            <div class="history-chart-container" style="height: 300px; margin: var(--space-lg) 0;">
                <canvas id="historyChart"></canvas>
            </div>

            <div class="modal-close-footer">
                <button type="button" onclick="closeHistoryModal()" class="modal-close-btn">
                    <i data-lucide="x"></i>
                    Stäng
                </button>
            </div>
        </div>
    </div>
</div>

<script>
const historyChartLabels = <?= json_encode($historyLabels) ?>;
const historyChartData = <?= json_encode($historyData) ?>;
const historyChartPoints = <?= json_encode($historyPoints) ?>;
let historyChartInstance = null;

function openHistoryModal() {
    const modal = document.getElementById('historyModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';

        // Initialize chart after modal is visible
        setTimeout(() => {
            initHistoryChart();
        }, 100);

        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
}

function closeHistoryModal() {
    const modal = document.getElementById('historyModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function initHistoryChart() {
    const ctx = document.getElementById('historyChart');
    if (!ctx || historyChartInstance) return;

    historyChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: historyChartLabels,
            datasets: [{
                label: 'Ranking',
                data: historyChartData,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3,
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const idx = context.dataIndex;
                            const points = historyChartPoints[idx] || 0;
                            return ['Position: #' + context.raw, 'Poäng: ' + points.toFixed(0)];
                        }
                    }
                }
            },
            scales: {
                y: {
                    reverse: true,
                    min: 1,
                    title: { display: true, text: 'Position' },
                    ticks: { stepSize: 1 }
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45,
                        autoSkip: true,
                        maxTicksLimit: 12
                    }
                }
            }
        }
    });
}

// Close on overlay click
document.getElementById('historyModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeHistoryModal();
});

// ESC key to close history modal
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const historyModal = document.getElementById('historyModal');
        if (historyModal && historyModal.style.display === 'flex') {
            closeHistoryModal();
        }
    }
});
</script>

<style>
.history-stats-row {
    display: flex;
    justify-content: space-around;
    padding: var(--space-md);
    background: var(--color-bg-secondary);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-md);
}
.history-stat {
    text-align: center;
}
.history-stat-value {
    display: block;
    font-size: 1.5rem;
    font-weight: 700;
}
.history-stat-label {
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    text-transform: uppercase;
}
.history-chart-container {
    position: relative;
}
</style>
<?php endif; ?>

<?php if ($canClaimProfile): ?>
<!-- Profile Claim Modal (Super Admin) -->
<div id="claimModal" class="claim-modal-overlay">
    <div class="claim-modal">
        <div class="claim-modal-header">
            <h3>
                <i data-lucide="user-plus"></i>
                Koppla e-post till profil
            </h3>
            <button type="button" class="claim-modal-close" onclick="closeClaimModal()">
                <i data-lucide="x"></i>
            </button>
        </div>
        <form id="claimForm" class="claim-modal-body">
            <div class="claim-info-box claim-info-admin">
                <i data-lucide="clock"></i>
                <p><strong>Kräver godkännande:</strong> Förfrågan skickas till admin för granskning. Efter godkännande kopplas e-posten och en aktiveringslänk skickas.</p>
            </div>

            <div class="claim-profile-card claim-profile-target">
                <span class="claim-profile-label">Profil utan e-post</span>
                <span class="claim-profile-name"><?= $fullName ?></span>
                <span class="claim-profile-meta"><?= count($results) ?> resultat</span>
            </div>

            <div class="claim-form-group">
                <label for="claimEmail">E-postadress att koppla <span class="required">*</span></label>
                <input type="email" id="claimEmail" name="email" class="claim-input" required placeholder="namn@example.com">
            </div>

            <div class="claim-form-group">
                <label for="claimPhone">Telefonnummer <span class="required">*</span></label>
                <input type="tel" id="claimPhone" name="phone" class="claim-input" required placeholder="070-123 45 67">
                <span class="claim-field-hint">Obligatoriskt för verifiering</span>
            </div>

            <div class="claim-form-divider">
                <span>Sociala medier (för verifiering)</span>
            </div>

            <div class="claim-social-grid">
                <div class="claim-form-group">
                    <label for="claimInstagram">
                        <i data-lucide="instagram"></i>
                        Instagram
                    </label>
                    <input type="text" id="claimInstagram" name="instagram" class="claim-input" placeholder="@användarnamn">
                </div>

                <div class="claim-form-group">
                    <label for="claimFacebook">
                        <i data-lucide="facebook"></i>
                        Facebook
                    </label>
                    <input type="text" id="claimFacebook" name="facebook" class="claim-input" placeholder="Profilnamn eller URL">
                </div>
            </div>

            <div class="claim-form-group">
                <label for="claimReason">Anteckning (valfritt)</label>
                <textarea id="claimReason" name="reason" rows="2" class="claim-textarea" placeholder="T.ex. verifierad via telefon..."></textarea>
            </div>

            <input type="hidden" name="target_rider_id" value="<?= $riderId ?>">

            <!-- GDPR Consent -->
            <div class="claim-consent-group">
                <label class="claim-consent-label">
                    <input type="checkbox" id="claimConsent" name="gdpr_consent" value="1" required>
                    <span class="claim-consent-checkmark"></span>
                    <span class="claim-consent-text">
                        Jag godkänner att mina uppgifter sparas och behandlas enligt
                        <a href="/integritetspolicy" target="_blank">integritetspolicyn</a>.
                        Uppgifterna används endast för att verifiera min identitet och hantera mitt konto.
                    </span>
                </label>
            </div>

            <div class="claim-form-actions">
                <button type="button" class="btn-secondary" onclick="closeClaimModal()">Avbryt</button>
                <button type="submit" class="btn-primary">
                    <i data-lucide="send"></i>
                    Skicka förfrågan
                </button>
            </div>
        </form>
        <div id="claimSuccess" class="claim-success" style="display: none;">
            <i data-lucide="clock"></i>
            <h4>Förfrågan skickad!</h4>
            <p>En admin kommer att granska och godkänna förfrågan. Aktiveringslänk skickas därefter.</p>
            <button type="button" class="btn-primary" onclick="closeClaimModal();">Stäng</button>
        </div>
    </div>
</div>
<?php endif; ?>

<?php if ($isArtistName): ?>
<!-- Artist Name Claim Modal (Logged-in Users) -->
<div id="artistClaimModal" class="claim-modal-overlay">
    <div class="claim-modal">
        <div class="claim-modal-header">
            <h3>
                <i data-lucide="link"></i>
                Koppla artistnamn till din profil
            </h3>
            <button type="button" class="claim-modal-close" onclick="closeArtistClaimModal()">
                <i data-lucide="x"></i>
            </button>
        </div>
        <form id="artistClaimForm" class="claim-modal-body">
            <div class="claim-info-box claim-info-admin">
                <i data-lucide="info"></i>
                <p><strong>Hur fungerar det?</strong> Om detta artistnamn ar ditt, kan du koppla det till din profil. Dina gamla resultat fran artistnamnet sammanfogas med dina nuvarande resultat efter admin-granskning.</p>
            </div>

            <div class="claim-profile-card claim-profile-target">
                <span class="claim-profile-label">Artistnamn</span>
                <span class="claim-profile-name"><?= htmlspecialchars($rider['firstname']) ?></span>
                <span class="claim-profile-meta"><?= count($results) ?> resultat</span>
            </div>

            <?php if ($currentUser): ?>
            <div class="claim-profile-card" style="background: var(--color-accent-light); border-color: var(--color-accent);">
                <span class="claim-profile-label">Kopplas till din profil</span>
                <span class="claim-profile-name"><?= htmlspecialchars($currentUser['firstname'] . ' ' . $currentUser['lastname']) ?></span>
            </div>
            <?php endif; ?>

            <div class="claim-form-group">
                <label for="artistEvidence">Motivering <span class="required">*</span></label>
                <textarea id="artistEvidence" name="evidence" rows="3" class="claim-textarea" required placeholder="Forklara varfor detta artistnamn ar ditt, t.ex. 'Tavlade under detta namn 2015-2017 i XYZ-serien'"></textarea>
            </div>

            <input type="hidden" name="anonymous_rider_id" value="<?= $riderId ?>">
            <input type="hidden" name="claiming_rider_id" value="<?= $currentUser['id'] ?? '' ?>">
            <input type="hidden" name="action" value="claim">

            <!-- GDPR Consent -->
            <div class="claim-consent-group">
                <label class="claim-consent-label">
                    <input type="checkbox" id="artistClaimConsent" name="gdpr_consent" value="1" required>
                    <span class="claim-consent-checkmark"></span>
                    <span class="claim-consent-text">
                        Jag intygar att detta artistnamn ar mitt och godkanner att resultaten sammanfogas med min profil.
                    </span>
                </label>
            </div>

            <div class="claim-form-actions">
                <button type="button" class="btn-secondary" onclick="closeArtistClaimModal()">Avbryt</button>
                <button type="submit" class="btn-primary">
                    <i data-lucide="send"></i>
                    Skicka forfragan
                </button>
            </div>
        </form>
        <div id="artistClaimSuccess" class="claim-success" style="display: none;">
            <i data-lucide="check-circle"></i>
            <h4>Forfragan skickad!</h4>
            <p>En admin kommer granska din forfragan. Nar den godkanns sammanfogas dina resultat automatiskt.</p>
            <button type="button" class="btn-primary" onclick="closeArtistClaimModal();">Stang</button>
        </div>
    </div>
</div>

<!-- Artist Name Activate Modal (Non-logged-in Users) -->
<div id="artistActivateModal" class="claim-modal-overlay">
    <div class="claim-modal">
        <div class="claim-modal-header">
            <h3>
                <i data-lucide="user-plus"></i>
                Aktivera artistnamn-profil
            </h3>
            <button type="button" class="claim-modal-close" onclick="closeArtistActivateModal()">
                <i data-lucide="x"></i>
            </button>
        </div>
        <form id="artistActivateForm" class="claim-modal-body">
            <div class="claim-info-box claim-info-admin">
                <i data-lucide="info"></i>
                <p><strong>Aktivera din profil:</strong> Om detta artistnamn ar ditt, fyll i dina uppgifter for att aktivera profilen. En admin granskar forfragan innan aktiveringen genomfors.</p>
            </div>

            <div class="claim-profile-card claim-profile-target">
                <span class="claim-profile-label">Artistnamn</span>
                <span class="claim-profile-name"><?= htmlspecialchars($rider['firstname']) ?></span>
                <span class="claim-profile-meta"><?= count($results) ?> resultat bevaras</span>
            </div>

            <div class="claim-form-group">
                <label for="activateEmail">E-postadress <span class="required">*</span></label>
                <input type="email" id="activateEmail" name="email" class="claim-input" required placeholder="din@email.se">
            </div>

            <div class="claim-form-divider">
                <span>Dina uppgifter</span>
            </div>

            <div class="claim-social-grid">
                <div class="claim-form-group">
                    <label for="activateFirstname">Fornamn</label>
                    <input type="text" id="activateFirstname" name="firstname" class="claim-input" value="<?= htmlspecialchars($rider['firstname']) ?>">
                </div>
                <div class="claim-form-group">
                    <label for="activateLastname">Efternamn <span class="required">*</span></label>
                    <input type="text" id="activateLastname" name="lastname" class="claim-input" required placeholder="Efternamn">
                </div>
            </div>

            <div class="claim-social-grid">
                <div class="claim-form-group">
                    <label for="activateBirthYear">Fodelsear</label>
                    <input type="number" id="activateBirthYear" name="birth_year" class="claim-input" min="1940" max="<?= date('Y') - 5 ?>" placeholder="t.ex. 1990">
                </div>
                <div class="claim-form-group">
                    <label for="activatePhone">Telefon</label>
                    <input type="tel" id="activatePhone" name="phone" class="claim-input" placeholder="070-123 45 67">
                </div>
            </div>

            <input type="hidden" name="anonymous_rider_id" value="<?= $riderId ?>">
            <input type="hidden" name="action" value="activate">

            <!-- GDPR Consent -->
            <div class="claim-consent-group">
                <label class="claim-consent-label">
                    <input type="checkbox" id="activateConsent" name="gdpr_consent" value="1" required>
                    <span class="claim-consent-checkmark"></span>
                    <span class="claim-consent-text">
                        Jag intygar att detta artistnamn ar mitt och godkanner att mina uppgifter sparas enligt
                        <a href="/integritetspolicy" target="_blank">integritetspolicyn</a>.
                    </span>
                </label>
            </div>

            <div class="claim-form-actions">
                <button type="button" class="btn-secondary" onclick="closeArtistActivateModal()">Avbryt</button>
                <button type="submit" class="btn-primary">
                    <i data-lucide="send"></i>
                    Skicka forfragan
                </button>
            </div>
        </form>
        <div id="artistActivateSuccess" class="claim-success" style="display: none;">
            <i data-lucide="check-circle"></i>
            <h4>Forfragan skickad!</h4>
            <p>En admin kommer granska din forfragan. Du far ett mail nar profilen ar aktiverad.</p>
            <button type="button" class="btn-primary" onclick="closeArtistActivateModal();">Stang</button>
        </div>
    </div>
</div>

<script>
// Artist Name Claim Modal Functions
function openArtistClaimModal() {
    document.getElementById('artistClaimModal')?.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeArtistClaimModal() {
    document.getElementById('artistClaimModal')?.classList.remove('active');
    document.body.style.overflow = '';
}

function openArtistActivateModal() {
    document.getElementById('artistActivateModal')?.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeArtistActivateModal() {
    document.getElementById('artistActivateModal')?.classList.remove('active');
    document.body.style.overflow = '';
}

// Handle Artist Claim Form Submission
document.getElementById('artistClaimForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;

    submitBtn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Skickar...';
    submitBtn.disabled = true;

    try {
        const formData = new FormData(form);
        const response = await fetch('/api/artist-name-claim.php', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            form.style.display = 'none';
            document.getElementById('artistClaimSuccess').style.display = 'block';
        } else {
            alert(result.error || 'Ett fel uppstod. Forsok igen.');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    } catch (err) {
        alert('Ett fel uppstod. Forsok igen.');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }

    lucide.createIcons();
});

// Handle Artist Activate Form Submission
document.getElementById('artistActivateForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;

    submitBtn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Skickar...';
    submitBtn.disabled = true;

    try {
        const formData = new FormData(form);
        const response = await fetch('/api/artist-name-claim.php', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            form.style.display = 'none';
            document.getElementById('artistActivateSuccess').style.display = 'block';
        } else {
            alert(result.error || 'Ett fel uppstod. Forsok igen.');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    } catch (err) {
        alert('Ett fel uppstod. Forsok igen.');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }

    lucide.createIcons();
});

// Close modals on overlay click
document.getElementById('artistClaimModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeArtistClaimModal();
});
document.getElementById('artistActivateModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeArtistActivateModal();
});
</script>
<?php endif; ?>

<!-- Modal CSS - Always loaded for both claim and activate modals -->
<style>
.claim-modal-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.7);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    z-index: 200;
    justify-content: center;
    align-items: center;
    padding: var(--space-md);
}
.claim-modal-overlay.active {
    display: flex;
}
.claim-modal {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    max-width: 520px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: var(--shadow-lg);
}
.claim-modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
    background: var(--color-bg-secondary);
}
.claim-modal-header h3 {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin: 0;
    font-size: var(--text-lg);
    color: var(--color-text);
}
.claim-modal-header h3 i {
    color: var(--color-accent);
}
.claim-modal-close {
    background: none;
    border: none;
    padding: var(--space-xs);
    cursor: pointer;
    color: var(--color-text-secondary);
    border-radius: var(--radius-sm);
}
.claim-modal-close:hover {
    background: var(--color-bg-secondary);
    color: var(--color-text);
}
.claim-modal-body {
    padding: var(--space-lg);
}
.claim-info-box {
    display: flex;
    gap: var(--space-sm);
    padding: var(--space-md);
    background: rgba(97, 206, 112, 0.1);
    border: 1px solid var(--color-success);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-lg);
}
.claim-info-box.claim-info-admin i {
    flex-shrink: 0;
    width: 20px;
    height: 20px;
    color: var(--color-success);
}
.claim-info-box p {
    margin: 0;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}
.claim-info-box p strong {
    color: var(--color-text);
}
.claim-profile-card {
    padding: var(--space-md);
    background: var(--color-bg-secondary);
    border-radius: var(--radius-md);
    text-align: center;
    margin-bottom: var(--space-lg);
}
.claim-profile-target {
    border: 2px solid var(--color-accent);
}
.claim-profile-label {
    display: block;
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
    margin-bottom: var(--space-xs);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.claim-profile-name {
    display: block;
    font-weight: 600;
    font-size: var(--text-lg);
    color: var(--color-text);
}
.claim-profile-meta {
    display: block;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-top: 2px;
}
.claim-form-group {
    margin-bottom: var(--space-md);
}
.claim-form-group label {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    font-size: var(--text-sm);
    font-weight: 500;
    margin-bottom: var(--space-xs);
    color: var(--color-text);
}
.claim-form-group label i {
    width: 16px;
    height: 16px;
    color: var(--color-text-secondary);
}
.claim-form-group label .required {
    color: var(--color-danger);
}
.claim-input,
.claim-textarea {
    width: 100%;
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    font-family: inherit;
    font-size: var(--text-sm);
    color: var(--color-text);
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.claim-input:focus,
.claim-textarea:focus {
    outline: none;
    border-color: var(--color-accent);
    box-shadow: 0 0 0 3px rgba(97, 206, 112, 0.15);
}
.claim-input::placeholder,
.claim-textarea::placeholder {
    color: var(--color-text-muted);
}
.claim-textarea {
    resize: vertical;
    min-height: 60px;
}
.claim-field-hint {
    display: block;
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
    margin-top: var(--space-2xs);
}
.claim-form-divider {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    margin: var(--space-lg) 0;
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
}
.claim-form-divider::before,
.claim-form-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--color-border);
}
.claim-social-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-md);
}
.claim-form-actions {
    display: flex;
    gap: var(--space-sm);
    justify-content: flex-end;
    margin-top: var(--space-lg);
    padding-top: var(--space-lg);
    border-top: 1px solid var(--color-border);
}
.claim-form-actions .btn-secondary {
    padding: var(--space-sm) var(--space-md);
    background: transparent;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    cursor: pointer;
    color: var(--color-text-secondary);
    transition: all 0.15s ease;
}
.claim-form-actions .btn-secondary:hover {
    background: var(--color-bg-secondary);
    border-color: var(--color-text-muted);
}
.claim-form-actions .btn-primary {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-lg);
    background: var(--color-accent);
    color: #111;
    border: none;
    border-radius: var(--radius-sm);
    cursor: pointer;
    font-weight: 600;
    transition: all 0.15s ease;
}
.claim-form-actions .btn-primary:hover {
    background: #7dd88a;
    transform: translateY(-1px);
}
.claim-success {
    padding: var(--space-xl);
    text-align: center;
}
.claim-success i {
    width: 48px;
    height: 48px;
    color: var(--color-success);
    margin-bottom: var(--space-md);
}
.claim-success h4 {
    margin: 0 0 var(--space-sm);
    color: #fff;
}
.claim-success p {
    color: var(--color-text-secondary);
    margin-bottom: var(--space-lg);
}
.btn-claim-profile {
    border-color: var(--color-accent) !important;
    color: var(--color-accent) !important;
}
.btn-claim-pending {
    opacity: 0.6;
    cursor: not-allowed !important;
}
/* GDPR Consent Checkbox */
.claim-consent-group {
    margin: var(--space-lg) 0;
    padding: var(--space-md);
    background: var(--color-bg-secondary);
    border-radius: var(--radius-md);
    border: 1px solid var(--color-border);
}
.claim-consent-label {
    display: flex;
    align-items: flex-start;
    gap: var(--space-sm);
    cursor: pointer;
    font-size: var(--text-sm);
    line-height: 1.5;
}
.claim-consent-label input[type="checkbox"] {
    position: absolute;
    opacity: 0;
    cursor: pointer;
}
.claim-consent-checkmark {
    flex-shrink: 0;
    width: 20px;
    height: 20px;
    background: var(--color-bg-card);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s ease;
    margin-top: 2px;
}
.claim-consent-checkmark::after {
    content: '';
    width: 6px;
    height: 10px;
    border: solid transparent;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
    margin-bottom: 2px;
}
.claim-consent-label input:checked ~ .claim-consent-checkmark {
    background: var(--color-accent);
    border-color: var(--color-accent);
}
.claim-consent-label input:checked ~ .claim-consent-checkmark::after {
    border-color: #111;
}
.claim-consent-label input:focus ~ .claim-consent-checkmark {
    box-shadow: 0 0 0 3px rgba(97, 206, 112, 0.2);
}
.claim-consent-text {
    color: var(--color-text-secondary);
}
.claim-consent-text a {
    color: var(--color-accent);
    text-decoration: underline;
}
.claim-consent-text a:hover {
    color: #7dd88a;
}
/* Mobile Modal - Between header and bottom nav */
@media (max-width: 767px) {
    .claim-modal-overlay {
        top: calc(var(--header-height, 60px) + env(safe-area-inset-top, 0px));
        bottom: calc(var(--mobile-nav-height, 95px) + env(safe-area-inset-bottom, 0px));
        padding: 0;
        overflow: hidden;
        align-items: stretch;
    }
    .claim-modal {
        max-width: 100%;
        max-height: 100%;
        height: 100%;
        border-radius: 0;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        border: none;
    }
    .claim-modal-header {
        flex-shrink: 0;
        background: var(--color-bg-card);
        border-radius: 0;
    }
    .claim-modal-header h3 {
        font-size: 1rem;
    }
    .claim-modal-close {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--color-bg-secondary);
        border-radius: var(--radius-full);
    }
    .claim-modal-close i {
        width: 20px;
        height: 20px;
    }
    .claim-modal-body {
        flex: 1;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
        padding: var(--space-md);
        min-height: 0;
    }
    .claim-social-grid {
        grid-template-columns: 1fr;
    }
}
</style>

<?php if ($canClaimProfile): ?>
<script>
function openClaimModal() {
    document.getElementById('claimModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeClaimModal() {
    document.getElementById('claimModal').classList.remove('active');
    document.body.style.overflow = '';
}

document.getElementById('claimForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalHtml = submitBtn.innerHTML;

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i data-lucide="loader-2" class="animate-spin"></i> Skickar...';

    try {
        const formData = new FormData(form);
        const response = await fetch('/api/rider-claim.php', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            form.style.display = 'none';
            document.getElementById('claimSuccess').style.display = 'block';
            if (typeof lucide !== 'undefined') lucide.createIcons();
        } else {
            alert(result.error || 'Ett fel uppstod');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalHtml;
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    } catch (error) {
        alert('Ett fel uppstod vid anslutning till servern');
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalHtml;
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
});

// Close modal on overlay click
document.getElementById('claimModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeClaimModal();
});
</script>
<?php endif; ?>

<!-- Activation Modal JavaScript - Always loaded -->
<script>
// Activation modal functions - loaded unconditionally to ensure onclick handlers work
function openActivateModal() {
    // Create modal dynamically (like shareProfile does)
    const modal = document.createElement('div');
    modal.id = 'activateModal';
    modal.className = 'claim-modal-overlay active';
    modal.innerHTML = `
        <div class="claim-modal">
            <div class="claim-modal-header">
                <h3>
                    <i data-lucide="user-check"></i>
                    Aktivera konto
                </h3>
                <button type="button" class="claim-modal-close" onclick="closeActivateModal()">
                    <i data-lucide="x"></i>
                </button>
            </div>
            <div class="claim-modal-body">
                <div class="claim-info-box claim-info-admin">
                    <i data-lucide="mail"></i>
                    <p>En aktiveringslänk skickas till profilens e-postadress så att kontot kan aktiveras med ett lösenord.</p>
                </div>

                <div class="claim-profile-card claim-profile-target">
                    <span class="claim-profile-label">Profil att aktivera</span>
                    <span class="claim-profile-name"><?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?></span>
                    <span class="claim-profile-meta"><?= count($results) ?> resultat</span>
                </div>

                <div class="claim-form-group">
                    <label>
                        <i data-lucide="mail"></i>
                        E-postadress
                    </label>
                    <input type="email" class="claim-input" value="<?= htmlspecialchars($rider['email']) ?>" readonly style="background: var(--color-bg-secondary);">
                    <span class="claim-field-hint">Ett mail med lösenordslänk skickas hit</span>
                </div>

                <div class="claim-form-actions">
                    <button type="button" class="btn-secondary" onclick="closeActivateModal()">Avbryt</button>
                    <button type="button" class="btn-primary" onclick="sendActivationEmail(<?= $riderId ?>)">
                        <i data-lucide="send"></i>
                        Skicka aktiveringslänk
                    </button>
                </div>
            </div>
            <div id="activateSuccess" class="claim-success" style="display: none;">
                <i data-lucide="check-circle"></i>
                <h4>Aktiveringslänk skickad!</h4>
                <p>Användaren får ett mail med länk för att sätta lösenord.</p>
                <button type="button" class="btn-primary" onclick="closeActivateModal();">Stäng</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
    
    // Re-init lucide icons
    if (typeof lucide !== 'undefined') lucide.createIcons();
    
    // Close on overlay click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeActivateModal();
    });
}

function closeActivateModal() {
    const modal = document.getElementById('activateModal');
    if (modal) {
        modal.remove();
        document.body.style.overflow = '';
    }
}

async function sendActivationEmail(riderId) {
    const btn = event.target.closest('button');
    const originalHtml = btn.innerHTML;

    btn.disabled = true;
    btn.innerHTML = '<i data-lucide="loader-2" class="animate-spin"></i> Skickar...';
    if (typeof lucide !== 'undefined') lucide.createIcons();

    try {
        const response = await fetch('/api/rider-activate.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify({ rider_id: riderId })
        });

        const result = await response.json();

        if (result.success) {
            document.querySelector('#activateModal .claim-modal-body').style.display = 'none';
            document.getElementById('activateSuccess').style.display = 'block';
            if (typeof lucide !== 'undefined') lucide.createIcons();
        } else {
            alert(result.error || 'Ett fel uppstod');
            btn.disabled = false;
            btn.innerHTML = originalHtml;
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    } catch (error) {
        alert('Ett fel uppstod vid anslutning till servern');
        btn.disabled = false;
        btn.innerHTML = originalHtml;
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
}

</script>

<!-- Chart.js Initialization -->
<?php if ($hasRankingChart || $hasFormChart): ?>
<script>
(function() {
    function initCharts() {
        if (typeof Chart === 'undefined') {
            console.error('Chart.js not loaded');
            return;
        }

        <?php if ($hasRankingChart): ?>
        // Ranking Chart (red theme)
        const rankingCtx = document.getElementById('rankingChart');
        if (rankingCtx) {
            const ctx = rankingCtx.getContext('2d');
            const rankingGradient = ctx.createLinearGradient(0, 0, 0, 280);
            rankingGradient.addColorStop(0, 'rgba(239, 68, 68, 0.25)');
            rankingGradient.addColorStop(1, 'rgba(239, 68, 68, 0.02)');

            new Chart(rankingCtx, {
                type: 'line',
                data: {
                    labels: <?= json_encode($rankingChartLabels) ?>,
                    datasets: [{
                        data: <?= json_encode($rankingChartData) ?>,
                        borderColor: '#ef4444',
                        backgroundColor: rankingGradient,
                        fill: 'start',
                        tension: 0.4,
                        borderWidth: 2,
                        pointRadius: 3,
                        pointHoverRadius: 5,
                        pointBackgroundColor: '#fff',
                        pointBorderColor: '#ef4444',
                        pointBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { intersect: false, mode: 'index' },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleFont: { size: 10 },
                            bodyFont: { size: 11, weight: 'bold' },
                            padding: 6,
                            cornerRadius: 4,
                            displayColors: false,
                            callbacks: {
                                title: function(items) { return items[0].label; },
                                label: function(item) { return '#' + item.raw; }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { font: { size: 9 }, color: '#6b7280', maxRotation: 0 }
                        },
                        y: {
                            reverse: true,
                            beginAtZero: false,
                            grid: { color: '#f0f0f0' },
                            ticks: { font: { size: 9 }, color: '#6b7280' }
                        }
                    }
                }
            });
        }
        <?php endif; ?>

        <?php if ($hasFormChart): ?>
        // Form Chart (green theme)
        const formCtx = document.getElementById('formChart');
        if (formCtx) {
            const ctx = formCtx.getContext('2d');
            const formGradient = ctx.createLinearGradient(0, 0, 0, 280);
            formGradient.addColorStop(0, 'rgba(97, 206, 112, 0.25)');
            formGradient.addColorStop(1, 'rgba(97, 206, 112, 0.02)');

            new Chart(formCtx, {
                type: 'line',
                data: {
                    labels: <?= json_encode($formChartLabels) ?>,
                    datasets: [{
                        data: <?= json_encode($formChartData) ?>,
                        borderColor: '#61CE70',
                        backgroundColor: formGradient,
                        fill: 'start',
                        tension: 0.4,
                        borderWidth: 2,
                        pointRadius: 3,
                        pointHoverRadius: 5,
                        pointBackgroundColor: '#fff',
                        pointBorderColor: '#61CE70',
                        pointBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { intersect: false, mode: 'index' },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleFont: { size: 10 },
                            bodyFont: { size: 11, weight: 'bold' },
                            padding: 6,
                            cornerRadius: 4,
                            displayColors: false,
                            callbacks: {
                                title: function(items) { return items[0].label; },
                                label: function(item) { return '#' + item.raw; }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { font: { size: 9 }, color: '#6b7280', maxRotation: 0 }
                        },
                        y: {
                            reverse: true,
                            beginAtZero: false,
                            grid: { color: '#f0f0f0' },
                            ticks: { font: { size: 9 }, color: '#6b7280' }
                        }
                    }
                }
            });
        }
        <?php endif; ?>
    }

    // Chart.js is now loaded before this script runs
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCharts);
    } else {
        initCharts();
    }
})();
</script>
<?php endif; ?>

<!-- Series Year AJAX Loading -->
<script>
function loadSeriesYear(year) {
    const container = document.getElementById('seriesContent');
    const select = document.getElementById('seriesYearSelect');
    if (!container) {
        console.error('Series container not found');
        return;
    }

    // Update select value
    if (select) select.value = year;

    // Show loading state
    container.innerHTML = '<div class="series-loading"><i data-lucide="loader-2" class="spin"></i> Laddar...</div>';

    // Fetch new content
    const url = '/api/rider-series.php?id=<?= $riderId ?>&year=' + year;
    console.log('Fetching series:', url);

    fetch(url)
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            return response.text();
        })
        .then(html => {
            console.log('Received HTML length:', html.length);
            container.innerHTML = html;
            // Re-init Lucide icons
            if (typeof lucide !== 'undefined') lucide.createIcons();
            // Re-init series tabs
            initSeriesTabs();
        })
        .catch(err => {
            console.error('Series load error:', err);
            container.innerHTML = '<div class="series-empty-state"><p class="text-muted">Kunde inte ladda seriedata</p></div>';
        });
}

function initSeriesTabs() {
    document.querySelectorAll('.series-tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const target = this.dataset.target;
            // Update tabs
            document.querySelectorAll('.series-tab-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            // Update panels
            document.querySelectorAll('.series-panel').forEach(p => p.classList.remove('active'));
            const panel = document.getElementById(target);
            if (panel) panel.classList.add('active');
        });
    });
}
// Init on page load
document.addEventListener('DOMContentLoaded', initSeriesTabs);
</script>

<!-- Global Sponsor: Content Bottom -->
<?= render_global_sponsors('rider', 'content_bottom', 'Tack till våra partners') ?>

<!-- Delete Club Season (superadmin) -->
<?php if ($isSuperAdmin): ?>
<script>
function deleteClubSeason(riderId, year) {
    if (!confirm('Radera klubbtillhörighet för ' + year + '?\n\nDetta tar bort kopplingen mellan åkaren och klubben för detta år.')) {
        return;
    }

    fetch('/api/delete-club-season.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rider_id: riderId, year: year })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            const row = document.getElementById('club-season-' + riderId + '-' + year);
            if (row) {
                row.style.opacity = '0';
                setTimeout(() => row.remove(), 200);
            }
        } else {
            alert('Fel: ' + (data.error || 'Kunde inte radera'));
        }
    })
    .catch(err => alert('Fel: ' + err.message));
}
</script>
<?php endif; ?>
