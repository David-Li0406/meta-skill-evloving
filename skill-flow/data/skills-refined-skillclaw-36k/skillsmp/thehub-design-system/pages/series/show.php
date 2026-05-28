<?php
/**
 * TheHUB V1.0 - Series Detail View
 * Shows series info, events, and standings (Individual + Club with 100%/50% rule)
 */

// Prevent direct access
if (!defined('HUB_ROOT')) {
    header('Location: /series');
    exit;
}

$pdo = hub_db();
$seriesId = $pageInfo['params']['id'] ?? 0;

if (!$seriesId) {
    include HUB_ROOT . '/pages/404.php';
    return;
}

// Fetch series details with brand logo fallback
$stmt = $pdo->prepare("
    SELECT s.*,
           COALESCE(s.logo, sb.logo) as logo,
           sb.name as brand_name,
           sb.accent_color as brand_accent_color
    FROM series s
    LEFT JOIN series_brands sb ON s.brand_id = sb.id
    WHERE s.id = ?
");
$stmt->execute([$seriesId]);
$series = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$series) {
    include HUB_ROOT . '/pages/404.php';
    return;
}

// Club championship only available for series from 2024 onwards
// Earlier data (2016-2023) is unreliable
$showClubChampionship = isset($series['year']) && (int)$series['year'] >= 2024;

// Check if series_events table exists
$useSeriesEvents = false;
try {
    $check = $pdo->query("SHOW TABLES LIKE 'series_events'");
    $useSeriesEvents = $check->rowCount() > 0;
} catch (Exception $e) {
    $useSeriesEvents = false;
}

// Check if series_results table has data for this series
$useSeriesResults = false;
try {
    $check = $pdo->prepare("SELECT COUNT(*) as cnt FROM series_results WHERE series_id = ?");
    $check->execute([$seriesId]);
    $row = $check->fetch(PDO::FETCH_ASSOC);
    $useSeriesResults = ($row && $row['cnt'] > 0);
} catch (Exception $e) {
    $useSeriesResults = false;
}

// Check if this series uses DH-style points (run_1_points + run_2_points)
$isDHSeries = false;
try {
    $dhCheck = $pdo->prepare("
        SELECT COUNT(*) as cnt FROM series_results
        WHERE series_id = ? AND (COALESCE(run_1_points, 0) > 0 OR COALESCE(run_2_points, 0) > 0)
    ");
    $dhCheck->execute([$seriesId]);
    $dhRow = $dhCheck->fetch(PDO::FETCH_ASSOC);
    $isDHSeries = ($dhRow && $dhRow['cnt'] > 0);
} catch (Exception $e) {
    $isDHSeries = false;
}

// Get events in series
if ($useSeriesEvents) {
    $stmt = $pdo->prepare("
        SELECT e.*, v.name as venue_name, v.city as venue_city,
               COUNT(DISTINCT r.cyclist_id) as result_count
        FROM series_events se
        JOIN events e ON se.event_id = e.id
        LEFT JOIN venues v ON e.venue_id = v.id
        LEFT JOIN results r ON e.id = r.event_id
        WHERE se.series_id = ?
        GROUP BY e.id
        ORDER BY e.date ASC
    ");
} else {
    $stmt = $pdo->prepare("
        SELECT e.*, v.name as venue_name, v.city as venue_city,
               COUNT(DISTINCT r.cyclist_id) as result_count
        FROM events e
        LEFT JOIN venues v ON e.venue_id = v.id
        LEFT JOIN results r ON e.id = r.event_id
        WHERE e.series_id = ?
        GROUP BY e.id
        ORDER BY e.date ASC
    ");
}
$stmt->execute([$seriesId]);
$events = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Get classes with results in this series (only point-awarding classes)
if ($useSeriesEvents) {
    $stmt = $pdo->prepare("
        SELECT DISTINCT c.id, c.name, c.display_name, c.sort_order,
               COUNT(DISTINCT r.cyclist_id) as rider_count
        FROM classes c
        JOIN results r ON c.id = r.class_id
        JOIN series_events se ON r.event_id = se.event_id
        WHERE se.series_id = ?
          AND COALESCE(c.series_eligible, 1) = 1
          AND COALESCE(c.awards_points, 1) = 1
        GROUP BY c.id
        ORDER BY c.sort_order ASC
    ");
    $stmt->execute([$seriesId]);
    $classes = $stmt->fetchAll(PDO::FETCH_ASSOC);
} else {
    $stmt = $pdo->prepare("
        SELECT DISTINCT c.id, c.name, c.display_name, c.sort_order,
               COUNT(DISTINCT r.cyclist_id) as rider_count
        FROM classes c
        JOIN results r ON c.id = r.class_id
        JOIN events e ON r.event_id = e.id
        WHERE e.series_id = ?
          AND COALESCE(c.series_eligible, 1) = 1
          AND COALESCE(c.awards_points, 1) = 1
        GROUP BY c.id
        ORDER BY c.sort_order ASC
    ");
    $stmt->execute([$seriesId]);
    $classes = $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// Selected class filter
$selectedClass = $_GET['class'] ?? 'all';
$searchName = $_GET['search'] ?? '';
$countBest = $series['count_best_results'] ?? null;

// Build standings with per-event points (like V2)
$standingsByClass = [];
$eventIds = array_column($events, 'id');

if (!empty($eventIds)) {
    // Get all riders who have results in this series (point-awarding classes only)
    $placeholders = implode(',', array_fill(0, count($eventIds), '?'));

    $sql = "
        SELECT DISTINCT
            ri.id as rider_id,
            ri.firstname,
            ri.lastname,
            COALESCE(rcs.club_id, ri.club_id) as club_id,
            COALESCE(rcs_club.name, c.name) as club_name,
            cls.id as class_id,
            cls.name as class_name,
            cls.display_name as class_display_name,
            cls.sort_order as class_sort_order
        FROM riders ri
        LEFT JOIN rider_club_seasons rcs ON ri.id = rcs.rider_id AND rcs.season_year = ?
        LEFT JOIN clubs rcs_club ON rcs.club_id = rcs_club.id
        LEFT JOIN clubs c ON ri.club_id = c.id
        JOIN results r ON ri.id = r.cyclist_id
        LEFT JOIN classes cls ON r.class_id = cls.id
        WHERE r.event_id IN ({$placeholders})
          AND COALESCE(cls.series_eligible, 1) = 1
          AND COALESCE(cls.awards_points, 1) = 1
    ";
    $seriesYear = $series['year'] ?? (int)date('Y');
    $params = array_merge([$seriesYear], $eventIds);

    if ($selectedClass !== 'all') {
        $sql .= " AND r.class_id = ?";
        $params[] = $selectedClass;
    }

    if ($searchName) {
        $sql .= " AND (ri.firstname LIKE ? OR ri.lastname LIKE ?)";
        $params[] = "%{$searchName}%";
        $params[] = "%{$searchName}%";
    }

    $sql .= " ORDER BY cls.sort_order ASC, ri.lastname, ri.firstname";

    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $riders = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // For each rider, get their points from each event
    foreach ($riders as $rider) {
        $riderData = [
            'rider_id' => $rider['rider_id'],
            'firstname' => $rider['firstname'],
            'lastname' => $rider['lastname'],
            'club_id' => $rider['club_id'],
            'club_name' => $rider['club_name'],
            'class_id' => $rider['class_id'],
            'event_points' => [],
            'event_run1' => [],   // DH Kval points
            'event_run2' => [],   // DH Race points
            'excluded_events' => [],
            'total_points' => 0
        ];

        // Get points for each event
        $allPoints = [];
        foreach ($events as $event) {
            if ($useSeriesResults) {
                $pStmt = $pdo->prepare("
                    SELECT points, run_1_points, run_2_points FROM series_results
                    WHERE series_id = ? AND cyclist_id = ? AND event_id = ? AND class_id = ?
                    LIMIT 1
                ");
                $pStmt->execute([$seriesId, $rider['rider_id'], $event['id'], $rider['class_id']]);
            } else {
                $pStmt = $pdo->prepare("
                    SELECT points, 0 as run_1_points, 0 as run_2_points FROM results
                    WHERE cyclist_id = ? AND event_id = ? AND class_id = ?
                    LIMIT 1
                ");
                $pStmt->execute([$rider['rider_id'], $event['id'], $rider['class_id']]);
            }
            $result = $pStmt->fetch(PDO::FETCH_ASSOC);
            $points = $result ? (int)$result['points'] : 0;
            $run1 = $result ? (int)($result['run_1_points'] ?? 0) : 0;
            $run2 = $result ? (int)($result['run_2_points'] ?? 0) : 0;
            $riderData['event_points'][$event['id']] = $points;
            $riderData['event_run1'][$event['id']] = $run1;
            $riderData['event_run2'][$event['id']] = $run2;
            if ($points > 0) {
                $allPoints[] = ['event_id' => $event['id'], 'points' => $points];
            }
        }

        // Apply count_best_results rule
        if ($countBest && count($allPoints) > $countBest) {
            usort($allPoints, function($a, $b) {
                return $b['points'] - $a['points'];
            });
            for ($i = $countBest; $i < count($allPoints); $i++) {
                $riderData['excluded_events'][$allPoints[$i]['event_id']] = true;
            }
            for ($i = 0; $i < $countBest; $i++) {
                $riderData['total_points'] += $allPoints[$i]['points'];
            }
        } else {
            foreach ($allPoints as $p) {
                $riderData['total_points'] += $p['points'];
            }
        }

        // Only include riders with points
        if ($riderData['total_points'] > 0) {
            $classKey = $rider['class_display_name'] ?? $rider['class_name'] ?? 'Okand';
            if (!isset($standingsByClass[$classKey])) {
                $standingsByClass[$classKey] = [
                    'class_id' => $rider['class_id'],
                    'sort_order' => $rider['class_sort_order'],
                    'riders' => []
                ];
            }
            $standingsByClass[$classKey]['riders'][] = $riderData;
        }
    }

    // Sort riders within each class by total points
    foreach ($standingsByClass as &$classData) {
        usort($classData['riders'], function($a, $b) {
            return $b['total_points'] - $a['total_points'];
        });
    }
    unset($classData);

    // Sort classes by sort_order
    uasort($standingsByClass, function($a, $b) {
        return ($a['sort_order'] ?? 999) - ($b['sort_order'] ?? 999);
    });
}

// ============================================================================
// CLUB STANDINGS with 100%/50% rule
// Best rider per club/class/event = 100%, second best = 50%, others = 0%
// Only calculated for series from 2024 onwards
// ============================================================================
$clubStandings = [];
$clubRiderContributions = [];

if (!$showClubChampionship) {
    // Skip club standings calculation for series before 2024
    goto skip_club_standings;
}

foreach ($events as $event) {
    $eventId = $event['id'];

    // Get all results for this event with series points, grouped by club and class
    // Use rider_club_seasons for accurate year-based club membership
    if ($useSeriesResults) {
        $stmt = $pdo->prepare("
            SELECT
                sr.cyclist_id,
                sr.class_id,
                sr.points,
                rd.firstname,
                rd.lastname,
                COALESCE(rcs.club_id, rd.club_id) as club_id,
                COALESCE(rcs_club.name, c.name) as club_name,
                COALESCE(rcs_club.city, c.city) as club_city,
                cls.name as class_name,
                cls.display_name as class_display_name
            FROM series_results sr
            JOIN riders rd ON sr.cyclist_id = rd.id
            LEFT JOIN rider_club_seasons rcs ON rd.id = rcs.rider_id AND rcs.season_year = ?
            LEFT JOIN clubs rcs_club ON rcs.club_id = rcs_club.id
            LEFT JOIN clubs c ON rd.club_id = c.id
            LEFT JOIN classes cls ON sr.class_id = cls.id
            WHERE sr.series_id = ? AND sr.event_id = ?
            AND COALESCE(rcs.club_id, rd.club_id) IS NOT NULL
            AND sr.points > 0
            AND COALESCE(cls.series_eligible, 1) = 1
            AND COALESCE(cls.awards_points, 1) = 1
            ORDER BY COALESCE(rcs.club_id, rd.club_id), sr.class_id, sr.points DESC
        ");
        $stmt->execute([$seriesYear, $seriesId, $eventId]);
    } else {
        $stmt = $pdo->prepare("
            SELECT
                r.cyclist_id,
                r.class_id,
                r.points,
                rd.firstname,
                rd.lastname,
                COALESCE(rcs.club_id, rd.club_id) as club_id,
                COALESCE(rcs_club.name, c.name) as club_name,
                COALESCE(rcs_club.city, c.city) as club_city,
                cls.name as class_name,
                cls.display_name as class_display_name
            FROM results r
            JOIN riders rd ON r.cyclist_id = rd.id
            LEFT JOIN rider_club_seasons rcs ON rd.id = rcs.rider_id AND rcs.season_year = ?
            LEFT JOIN clubs rcs_club ON rcs.club_id = rcs_club.id
            LEFT JOIN clubs c ON rd.club_id = c.id
            LEFT JOIN classes cls ON r.class_id = cls.id
            WHERE r.event_id = ?
            AND r.status = 'finished'
            AND COALESCE(rcs.club_id, rd.club_id) IS NOT NULL
            AND r.points > 0
            AND COALESCE(cls.series_eligible, 1) = 1
            AND COALESCE(cls.awards_points, 1) = 1
            ORDER BY COALESCE(rcs.club_id, rd.club_id), r.class_id, r.points DESC
        ");
        $stmt->execute([$seriesYear, $eventId]);
    }
    $eventResults = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Group by club and class
    $clubClassResults = [];
    foreach ($eventResults as $result) {
        $key = $result['club_id'] . '_' . $result['class_id'];
        if (!isset($clubClassResults[$key])) {
            $clubClassResults[$key] = [];
        }
        $clubClassResults[$key][] = $result;
    }

    // Apply 100%/50% rule for each club/class combo
    foreach ($clubClassResults as $clubRiders) {
        $rank = 1;
        foreach ($clubRiders as $rider) {
            $clubId = $rider['club_id'];
            $clubName = $rider['club_name'];
            $originalPoints = (float)$rider['points'];
            $clubPoints = 0;

            if ($rank === 1) {
                $clubPoints = $originalPoints;
            } elseif ($rank === 2) {
                $clubPoints = round($originalPoints * 0.5, 0);
            }

            // Initialize club if not exists
            if (!isset($clubStandings[$clubId])) {
                $clubStandings[$clubId] = [
                    'club_id' => $clubId,
                    'club_name' => $clubName,
                    'club_city' => $rider['club_city'] ?? '',
                    'riders' => [],
                    'total_points' => 0,
                    'event_points' => [],
                    'rider_count' => 0,
                    'best_event_points' => 0,
                    'events_with_points' => 0
                ];
                foreach ($events as $e) {
                    $clubStandings[$clubId]['event_points'][$e['id']] = 0;
                }
            }

            // Add club points for this event
            $clubStandings[$clubId]['event_points'][$eventId] += $clubPoints;
            $clubStandings[$clubId]['total_points'] += $clubPoints;

            // Track rider contribution
            $riderId = $rider['cyclist_id'];
            $riderKey = $clubId . '_' . $riderId;
            if (!isset($clubRiderContributions[$riderKey])) {
                $clubRiderContributions[$riderKey] = [
                    'rider_id' => $riderId,
                    'club_id' => $clubId,
                    'name' => $rider['firstname'] . ' ' . $rider['lastname'],
                    'class_name' => $rider['class_display_name'] ?? $rider['class_name'],
                    'total_club_points' => 0
                ];
            }
            $clubRiderContributions[$riderKey]['total_club_points'] += $clubPoints;

            $rank++;
        }
    }
}

// Add riders to their clubs
foreach ($clubRiderContributions as $riderData) {
    $clubId = $riderData['club_id'];
    if (isset($clubStandings[$clubId])) {
        $clubStandings[$clubId]['riders'][] = [
            'rider_id' => $riderData['rider_id'],
            'name' => $riderData['name'],
            'class_name' => $riderData['class_name'],
            'points' => $riderData['total_club_points']
        ];
        $clubStandings[$clubId]['rider_count']++;
    }
}

// Calculate best_event_points and events_with_points for each club
foreach ($clubStandings as $clubId => &$club) {
    $maxEventPoints = 0;
    $eventsWithPoints = 0;
    foreach ($club['event_points'] as $pts) {
        if ($pts > $maxEventPoints) {
            $maxEventPoints = $pts;
        }
        if ($pts > 0) {
            $eventsWithPoints++;
        }
    }
    $club['best_event_points'] = $maxEventPoints;
    $club['events_with_points'] = $eventsWithPoints;
}
unset($club);

// Sort clubs by total points
uasort($clubStandings, function($a, $b) {
    return $b['total_points'] - $a['total_points'];
});

// Sort riders within each club by points
foreach ($clubStandings as &$club) {
    usort($club['riders'], function($a, $b) {
        return $b['points'] - $a['points'];
    });
}
unset($club);

skip_club_standings:
?>

<div class="page-header">
    <nav class="breadcrumb">
        <a href="/series">Serier</a>
        <span class="breadcrumb-sep">></span>
        <span><?= htmlspecialchars($series['name']) ?></span>
    </nav>
</div>

<div class="series-detail">
    <!-- Series Header -->
    <div class="series-hero">
        <div class="series-hero-logo">
            <?php if ($series['logo']): ?>
                <img src="<?= htmlspecialchars($series['logo']) ?>" alt="<?= htmlspecialchars($series['name']) ?>">
            <?php else: ?>
                <span class="series-logo-placeholder"><i data-lucide="trophy" class="icon-xl"></i></span>
            <?php endif; ?>
        </div>
        <div class="series-hero-info">
            <h1 class="series-title"><?= htmlspecialchars($series['name']) ?></h1>
            <?php if ($series['description']): ?>
                <p class="series-description"><?= htmlspecialchars($series['description']) ?></p>
            <?php endif; ?>
            <div class="series-meta">
                <span><?= count($events) ?> tavlingar</span>
                <?php if ($countBest): ?>
                <span>Raknar <?= $countBest ?> basta resultat</span>
                <?php endif; ?>
            </div>
        </div>
    </div>

    <?php
    // Show warning for unverified historical series (2024 and older)
    $showHistoricalWarning = isset($series['year']) && (int)$series['year'] <= 2024 && empty($series['historical_data_verified']);
    if ($showHistoricalWarning):
    ?>
    <div class="series-historical-warning">
        <i data-lucide="alert-triangle"></i>
        <span>Serietabellerna för äldre serier är under arbete. Dessa kräver en del manuellt arbete för att bli korrekta och arbete pågår.</span>
    </div>
    <?php endif; ?>

    <!-- Navigation Row: Toggle + Events Dropdown -->
    <div class="series-nav-row">
        <!-- Toggle Buttons: Individual / Clubs -->
        <div class="standings-toggle">
            <button class="standings-toggle-btn active" data-tab="individual" onclick="switchTab('individual')">
                <i data-lucide="user"></i>
                <span>Individuellt</span>
            </button>
            <?php if ($showClubChampionship): ?>
            <button class="standings-toggle-btn" data-tab="club" onclick="switchTab('club')">
                <i data-lucide="shield"></i>
                <span>Klubbmastarskap</span>
            </button>
            <?php endif; ?>
        </div>

        <!-- Collapsible Events Section -->
        <details class="events-dropdown">
            <summary class="events-dropdown-header">
                <span><i data-lucide="calendar" class="events-dropdown-icon"></i> Tavlingar i serien</span>
                <span class="events-count"><?= count($events) ?> st</span>
                <span class="dropdown-arrow">▾</span>
            </summary>
            <div class="events-dropdown-content">
                <?php if (empty($events)): ?>
                    <p class="text-muted">Inga tavlingar i serien annu.</p>
                <?php else: ?>
                    <?php foreach ($events as $i => $event):
                        $eventDate = strtotime($event['date']);
                        $hasResults = $eventDate < time() && $event['result_count'] > 0;
                    ?>
                    <a href="/event/<?= $event['id'] ?>" class="event-dropdown-item">
                        <span class="event-num">#<?= $i + 1 ?></span>
                        <span class="event-date"><?= date('j M', $eventDate) ?></span>
                        <span class="event-name"><?= htmlspecialchars($event['name']) ?></span>
                        <?php if (!empty($event['is_championship'])): ?>
                        <span class="event-sm-badge event-sm-badge--small" title="Svenska Mästerskap">SM</span>
                        <?php endif; ?>
                        <span class="event-results"><?= $hasResults ? $event['result_count'] . ' resultat' : 'Kommande' ?></span>
                    </a>
                    <?php endforeach; ?>
                <?php endif; ?>
            </div>
        </details>
    </div>

    <!-- Individual Standings Section -->
    <div id="individual-standings">
        <?php
        // Calculate individual stats
        $totalIndividualRiders = 0;
        foreach ($standingsByClass as $classData) {
            $totalIndividualRiders += count($classData['riders']);
        }
        ?>

        <!-- Summary Stats Cards -->
        <div class="stats-grid stats-grid--3 mb-md">
            <div class="stat-card">
                <div class="stat-value"><?= count($classes) ?></div>
                <div class="stat-label">Klasser</div>
            </div>
            <div class="stat-card">
                <div class="stat-value"><?= $totalIndividualRiders ?></div>
                <div class="stat-label">Deltagare</div>
            </div>
            <div class="stat-card">
                <div class="stat-value"><?= count($events) ?></div>
                <div class="stat-label">Events</div>
            </div>
        </div>

        <!-- Filters -->
        <form method="get" class="filter-bar">
            <div class="filter-group">
                <label class="filter-label">Klass</label>
                <select name="class" id="class-filter" class="filter-select" onchange="this.form.submit()">
                    <option value="all" <?= $selectedClass === 'all' ? 'selected' : '' ?>>Alla klasser</option>
                    <?php foreach ($classes as $cls): ?>
                        <option value="<?= $cls['id'] ?>" <?= $selectedClass == $cls['id'] ? 'selected' : '' ?>>
                            <?= htmlspecialchars($cls['display_name'] ?? $cls['name']) ?> (<?= $cls['rider_count'] ?>)
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div class="filter-group filter-search-group">
                <label class="filter-label">Sök namn</label>
                <input type="search" name="search" id="name-search" class="filter-select" value="<?= htmlspecialchars($searchName) ?>" placeholder="Skriv namn...">
            </div>
            <button type="submit" class="btn btn--primary filter-btn">Sök</button>
        </form>

        <!-- Individual Standings -->
        <div class="card">
            <h2 class="card-title">Individuell stallning</h2>
            <?php if ($countBest): ?>
                <p class="text-muted standings-note">Raknar <?= $countBest ?> basta resultat</p>
            <?php endif; ?>

            <?php if (empty($standingsByClass)): ?>
                <p class="text-muted text-center">Ingen stallning annu.</p>
            <?php else: ?>
                <?php foreach ($standingsByClass as $className => $classData): ?>
                <div class="standings-class">
                    <h3 class="standings-class-title"><?= htmlspecialchars($className) ?> <span class="rider-count">(<?= count($classData['riders']) ?>)</span></h3>
                    <div class="table-responsive">
                        <table class="table standings-table">
                            <thead>
                                <tr>
                                    <th class="col-pos">#</th>
                                    <th class="col-name">Namn</th>
                                    <th class="col-club">Klubb</th>
                                    <?php $eventNum = 1; foreach ($events as $event): ?>
                                        <?php if ($isDHSeries): ?>
                                        <th class="col-event col-event-dh" title="<?= htmlspecialchars($event['name']) ?> - Kval">
                                            <div class="th-dh">#<?= $eventNum ?></div>
                                            <div class="th-dh-type">Kval</div>
                                        </th>
                                        <th class="col-event col-event-dh" title="<?= htmlspecialchars($event['name']) ?> - Race">
                                            <div class="th-dh">#<?= $eventNum ?></div>
                                            <div class="th-dh-type">Race</div>
                                        </th>
                                        <?php else: ?>
                                        <th class="col-event" title="<?= htmlspecialchars($event['name']) ?>">#<?= $eventNum ?></th>
                                        <?php endif; ?>
                                    <?php $eventNum++; endforeach; ?>
                                    <th class="col-total">Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($classData['riders'] as $pos => $row): ?>
                                <tr>
                                    <td class="col-pos">
                                        <?php if ($pos == 0): ?>
                                            <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon">
                                        <?php elseif ($pos == 1): ?>
                                            <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon">
                                        <?php elseif ($pos == 2): ?>
                                            <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon">
                                        <?php else: ?>
                                            <?= $pos + 1 ?>
                                        <?php endif; ?>
                                    </td>
                                    <td class="col-name">
                                        <a href="/rider/<?= $row['rider_id'] ?>">
                                            <?= htmlspecialchars($row['firstname'] . ' ' . $row['lastname']) ?>
                                        </a>
                                    </td>
                                    <td class="col-club"><?= htmlspecialchars($row['club_name'] ?? '-') ?></td>
                                    <?php foreach ($events as $event):
                                        $pts = $row['event_points'][$event['id']] ?? 0;
                                        $run1 = $row['event_run1'][$event['id']] ?? 0;
                                        $run2 = $row['event_run2'][$event['id']] ?? 0;
                                        $isExcluded = isset($row['excluded_events'][$event['id']]);
                                    ?>
                                        <?php if ($isDHSeries): ?>
                                        <!-- DH: Kval column -->
                                        <td class="col-event col-event-dh">
                                            <?= $run1 > 0 ? $run1 : '<span class="no-points">-</span>' ?>
                                        </td>
                                        <!-- DH: Race column -->
                                        <td class="col-event col-event-dh">
                                            <?= $run2 > 0 ? $run2 : '<span class="no-points">-</span>' ?>
                                        </td>
                                        <?php else: ?>
                                        <td class="col-event <?= $isExcluded ? 'excluded' : '' ?>">
                                            <?php if ($pts > 0): ?>
                                                <?php if ($isExcluded): ?>
                                                    <span class="points-excluded" title="Raknas ej"><?= $pts ?></span>
                                                <?php else: ?>
                                                    <?= $pts ?>
                                                <?php endif; ?>
                                            <?php else: ?>
                                                <span class="no-points">-</span>
                                            <?php endif; ?>
                                        </td>
                                        <?php endif; ?>
                                    <?php endforeach; ?>
                                    <td class="col-total"><strong><?= $row['total_points'] ?></strong></td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                </div>
                <?php endforeach; ?>
            <?php endif; ?>
        </div>
    </div>

    <?php if ($showClubChampionship): ?>
    <!-- Club Standings Section (Admin Style) -->
    <div id="club-standings" style="display: none;">
        <?php
        // Calculate summary stats
        $clubTotalParticipants = array_sum(array_column($clubStandings, 'rider_count'));
        $clubCount = count($clubStandings);
        $eventCount = count($events);
        ?>

        <!-- Summary Stats Cards -->
        <div class="stats-grid stats-grid--3 mb-md">
            <div class="stat-card">
                <div class="stat-value"><?= $clubCount ?></div>
                <div class="stat-label">Klubbar</div>
            </div>
            <div class="stat-card">
                <div class="stat-value"><?= $clubTotalParticipants ?></div>
                <div class="stat-label">Deltagare</div>
            </div>
            <div class="stat-card">
                <div class="stat-value"><?= $eventCount ?></div>
                <div class="stat-label">Events</div>
            </div>
        </div>

        <!-- Club Standings Table -->
        <div class="card">
            <div class="card-header">
                <h2 class="card-title"><i data-lucide="list-ordered" class="card-title-icon"></i> Klubbranking - <?= htmlspecialchars($series['name']) ?></h2>
            </div>

            <?php if (empty($clubStandings)): ?>
                <div class="empty-state">
                    <div class="empty-state-icon"><i data-lucide="shield"></i></div>
                    <p>Inga klubbresultat annu.</p>
                </div>
            <?php else: ?>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th style="width: 60px;">Rank</th>
                                <th>Klubb</th>
                                <th class="text-right">Poang</th>
                                <th class="text-right table-col-hide-portrait">Deltagare</th>
                                <th class="text-right table-col-hide-portrait">Events</th>
                                <th class="text-right table-col-hide-portrait">Basta event</th>
                                <th style="width: 50px;"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php $clubPos = 0; foreach ($clubStandings as $club): $clubPos++; ?>
                            <tr>
                                <td>
                                    <?php if ($clubPos == 1): ?>
                                        <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon">
                                    <?php elseif ($clubPos == 2): ?>
                                        <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon">
                                    <?php elseif ($clubPos == 3): ?>
                                        <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon">
                                    <?php else: ?>
                                        <?= $clubPos ?>
                                    <?php endif; ?>
                                </td>
                                <td><a href="/club/<?= $club['club_id'] ?>" class="text-link"><strong><?= htmlspecialchars($club['club_name']) ?></strong></a></td>
                                <td class="text-right"><strong><?= number_format($club['total_points']) ?></strong></td>
                                <td class="text-right table-col-hide-portrait"><?= $club['rider_count'] ?></td>
                                <td class="text-right table-col-hide-portrait"><?= $club['events_with_points'] ?></td>
                                <td class="text-right table-col-hide-portrait"><?= number_format($club['best_event_points']) ?></td>
                                <td>
                                    <button class="btn-icon" onclick="showClubDetail(<?= $club['club_id'] ?>)" title="Visa detaljer">
                                        <i data-lucide="eye"></i>
                                    </button>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            <?php endif; ?>
        </div>

        <!-- Info Card -->
        <div class="card mt-md">
            <div class="card-body">
                <p class="text-muted text-sm" style="margin: 0;">
                    <i data-lucide="info" style="width: 14px; height: 14px; vertical-align: middle;"></i>
                    Basta akare per klubb/klass far 100%, nast basta 50%, ovriga 0%.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- Club Detail Modal -->
<div id="club-detail-modal" class="modal" style="display: none;">
    <div class="modal-backdrop" onclick="closeClubDetail()"></div>
    <div class="modal-content">
        <div class="modal-header">
            <h3 id="club-detail-title">Klubbdetaljer</h3>
            <button class="btn-icon" onclick="closeClubDetail()"><i data-lucide="x"></i></button>
        </div>
        <div class="modal-body" id="club-detail-body">
            <!-- Content loaded dynamically -->
        </div>
    </div>
</div>

<!-- Store club data for modal -->
<script type="application/json" id="club-data">
<?= json_encode(array_values($clubStandings), JSON_UNESCAPED_UNICODE) ?>
</script>
<script type="application/json" id="events-data">
<?= json_encode($events, JSON_UNESCAPED_UNICODE) ?>
</script>
<?php endif; // $showClubChampionship ?>

<script>
function switchTab(tab) {
    document.querySelectorAll('.standings-toggle-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });
    const individualEl = document.getElementById('individual-standings');
    const clubEl = document.getElementById('club-standings');
    if (individualEl) individualEl.style.display = tab === 'individual' ? '' : 'none';
    if (clubEl) clubEl.style.display = tab === 'club' ? '' : 'none';
    // Re-initialize Lucide icons for the newly visible section
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Club detail modal functions (only if club championship is enabled)
const clubDataEl = document.getElementById('club-data');
const eventsDataEl = document.getElementById('events-data');
const clubData = clubDataEl ? JSON.parse(clubDataEl.textContent) : [];
const eventsData = eventsDataEl ? JSON.parse(eventsDataEl.textContent) : [];

function showClubDetail(clubId) {
    if (!clubData.length) return;
    const club = clubData.find(c => c.club_id === clubId);
    if (!club) return;

    document.getElementById('club-detail-title').textContent = club.club_name;

    // Build event breakdown table
    let eventRows = '';
    eventsData.forEach((event, idx) => {
        const pts = club.event_points[event.id] || 0;
        const eventDate = event.date ? new Date(event.date).toLocaleDateString('sv-SE', {day: 'numeric', month: 'short'}) : '-';
        eventRows += `<tr>
            <td>#${idx + 1}</td>
            <td>${event.name}</td>
            <td>${eventDate}</td>
            <td class="text-right"><strong>${pts > 0 ? pts.toLocaleString() : '-'}</strong></td>
        </tr>`;
    });

    // Build riders list
    let riderRows = '';
    club.riders.forEach(rider => {
        riderRows += `<tr>
            <td><a href="/rider/${rider.rider_id}">${rider.name}</a></td>
            <td class="text-muted">${rider.class_name}</td>
            <td class="text-right"><strong>${rider.points.toLocaleString()} p</strong></td>
        </tr>`;
    });

    const html = `
        <div class="modal-stats">
            <div class="modal-stat">
                <div class="modal-stat-value">${club.total_points.toLocaleString()}</div>
                <div class="modal-stat-label">Totalt</div>
            </div>
            <div class="modal-stat">
                <div class="modal-stat-value">${club.rider_count}</div>
                <div class="modal-stat-label">Akare</div>
            </div>
            <div class="modal-stat">
                <div class="modal-stat-value">${club.events_with_points}</div>
                <div class="modal-stat-label">Events</div>
            </div>
            <div class="modal-stat">
                <div class="modal-stat-value">${club.best_event_points.toLocaleString()}</div>
                <div class="modal-stat-label">Basta</div>
            </div>
        </div>

        <h4 style="margin: 16px 0 8px;">Poang per event</h4>
        <div class="table-responsive">
            <table class="table table--sm">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Event</th>
                        <th>Datum</th>
                        <th class="text-right">Poang</th>
                    </tr>
                </thead>
                <tbody>${eventRows}</tbody>
            </table>
        </div>

        <h4 style="margin: 16px 0 8px;">Akare (${club.rider_count} st)</h4>
        <div class="table-responsive">
            <table class="table table--sm">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>Klass</th>
                        <th class="text-right">Poang</th>
                    </tr>
                </thead>
                <tbody>${riderRows}</tbody>
            </table>
        </div>
    `;

    document.getElementById('club-detail-body').innerHTML = html;
    document.getElementById('club-detail-modal').style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeClubDetail() {
    document.getElementById('club-detail-modal').style.display = 'none';
    document.body.style.overflow = '';
}

// Close modal on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeClubDetail();
    }
});
</script>

<style>
/* DH Series - two-row header for Kval/Race */
.th-dh {
    font-weight: 600;
    font-size: 0.85rem;
}
.th-dh-type {
    font-weight: 400;
    font-size: 0.7rem;
    color: var(--color-text-secondary, #666);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.col-event-dh {
    min-width: 45px;
    text-align: center;
    padding: 4px 6px !important;
}

/* Series Navigation Row - Toggle + Dropdown side by side on desktop */
.series-nav-row {
    display: flex;
    flex-direction: column;
    gap: var(--space-md);
    margin-bottom: var(--space-md);
}
@media (min-width: 768px) {
    .series-nav-row {
        flex-direction: row;
        align-items: stretch;
    }
    .series-nav-row .standings-toggle {
        flex: 1;
        margin-bottom: 0;
    }
    .series-nav-row .events-dropdown {
        flex: 1;
    }
}

/* Override events-dropdown to match toggle buttons */
.series-nav-row .events-dropdown {
    background: white;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    margin-bottom: 0;
}
.series-nav-row .events-dropdown-header {
    padding: var(--space-sm) var(--space-md);
    font-size: 0.875rem;
    background: white;
}
.series-nav-row .events-dropdown-header:hover {
    background: #f5f5f5;
}
.series-nav-row .events-dropdown[open] {
    box-shadow: none;
}

/* Standings Toggle (50/50 buttons within toggle container) */
.standings-toggle {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-sm);
}
.standings-toggle-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-md);
    background: #ffffff;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    font-size: 0.875rem;
    font-weight: 600;
    color: #171717;
    cursor: pointer;
    transition: all 0.15s ease;
    opacity: 1;
}
.standings-toggle-btn i {
    width: 18px;
    height: 18px;
    color: inherit;
}
.standings-toggle-btn:hover {
    background: #f5f5f5;
    border-color: #323539;
}
.standings-toggle-btn.active {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: #ffffff;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-sm);
}
.stats-grid--3 {
    grid-template-columns: repeat(3, 1fr);
}
.stat-card {
    background: white;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: var(--space-sm) var(--space-md);
    text-align: center;
}
.stat-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--color-primary);
    line-height: 1.2;
}
.stat-label {
    font-size: 0.75rem;
    color: var(--color-text);
}

/* Button Icon */
.btn-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-star);
    color: var(--color-text);
    cursor: pointer;
    transition: all 0.15s ease;
}
.btn-icon:hover {
    background: var(--color-star-fade);
    color: var(--color-primary);
    border-color: var(--color-primary);
}
.btn-icon i {
    width: 16px;
    height: 16px;
}

/* Modal Styles */
.modal {
    position: fixed;
    inset: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-md);
}
.modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
}
.modal-content {
    position: relative;
    background: white;
    border-radius: var(--radius-lg);
    width: 100%;
    max-width: 600px;
    max-height: 90vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: var(--shadow-lg);
}
.modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}
.modal-header h3 {
    margin: 0;
    font-size: 1.125rem;
}
.modal-body {
    padding: var(--space-lg);
    overflow-y: auto;
}
.modal-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
}
.modal-stat {
    text-align: center;
    padding: var(--space-sm);
    background: #f5f5f5;
    border-radius: var(--radius-sm);
}
.modal-stat-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--color-primary);
}
.modal-stat-label {
    font-size: 0.75rem;
    color: var(--color-text);
}

/* Mobile Fullscreen Modal */
@media (max-width: 767px) {
    .modal {
        padding: 0;
    }
    .modal-content {
        max-width: 100%;
        max-height: 100%;
        height: 100%;
        border-radius: 0;
    }
    .modal-header {
        position: sticky;
        top: 0;
        background: white;
        z-index: 10;
        padding: var(--space-md);
        border-bottom: 1px solid var(--color-border);
    }
    .modal-header h3 {
        font-size: 1rem;
    }
    .modal-header .btn-icon {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--color-bg-secondary);
        border-radius: var(--radius-full);
    }
    .modal-body {
        flex: 1;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
        padding: var(--space-md);
    }
    .modal-stats {
        grid-template-columns: repeat(2, 1fr);
    }
}
.table--sm {
    font-size: 0.875rem;
}
.table--sm th, .table--sm td {
    padding: var(--space-xs) var(--space-sm);
}
</style>

<!-- CSS loaded from /assets/css/pages/series-show.css -->
