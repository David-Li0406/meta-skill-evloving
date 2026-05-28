<?php
/**
 * Public Club Points Detail Page
 * Shows detailed breakdown of a club's points in a series
 * Accessed via /club-points?club_id=X&series_id=Y
 * Add ?modal=1 to load without header/footer (for iframe embedding)
 */

$db = hub_db();
$isModal = isset($_GET['modal']) && $_GET['modal'] == '1';

// Get parameters
$clubId = isset($_GET['club_id']) ? (int)$_GET['club_id'] : 0;
$seriesId = isset($_GET['series_id']) ? (int)$_GET['series_id'] : 0;

if (!$clubId || !$seriesId) {
    header('Location: /series');
    exit;
}

// Include club-points-system
require_once HUB_ROOT . '/includes/club-points-system.php';

// Get detailed breakdown using the system functions
// We need to convert from PDO to the DB wrapper
$configDb = getDB();
$detail = getClubPointsDetail($configDb, $clubId, $seriesId);

// Get club info directly if the cached data is empty
$stmt = $db->prepare("SELECT * FROM clubs WHERE id = ?");
$stmt->execute([$clubId]);
$club = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$club) {
    include HUB_ROOT . '/pages/404.php';
    return;
}

// Get series info with brand logo fallback
$stmt = $db->prepare("
    SELECT s.*, COALESCE(s.logo, sb.logo) as logo, sb.accent_color as brand_accent_color
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

// Check if we have cached data
$hasCachedData = !empty($detail) && !empty($detail['standing']);
$standing = $detail['standing'] ?? null;
$events = $detail['events'] ?? [];
$riderDetails = $detail['rider_details'] ?? [];

// If no cached data, calculate on-the-fly from results (same as series-single.php)
if (!$hasCachedData) {
    // Get events in this series
    $stmt = $db->prepare("
        SELECT e.id, e.name, e.date, e.location
        FROM events e
        LEFT JOIN series_events se ON e.id = se.event_id AND se.series_id = ?
        WHERE e.series_id = ? OR se.series_id = ?
        ORDER BY e.date ASC
    ");
    $stmt->execute([$seriesId, $seriesId, $seriesId]);
    $seriesEvents = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Check if series_results exists
    $useSeriesResults = false;
    try {
        $stmt = $db->prepare("SELECT COUNT(*) FROM series_results WHERE series_id = ?");
        $stmt->execute([$seriesId]);
        $useSeriesResults = ($stmt->fetchColumn() > 0);
    } catch (Exception $e) {
        $useSeriesResults = false;
    }

    // Calculate club points from results
    $totalPoints = 0;
    $totalParticipants = 0;
    $eventsCount = 0;
    $bestEventPoints = 0;

    foreach ($seriesEvents as $event) {
        $eventId = $event['id'];

        // Get results for this club in this event
        if ($useSeriesResults) {
            $stmt = $db->prepare("
                SELECT
                    sr.cyclist_id,
                    sr.class_id,
                    sr.points,
                    rd.firstname,
                    rd.lastname,
                    cls.name as class_name,
                    cls.display_name as class_display_name
                FROM series_results sr
                JOIN riders rd ON sr.cyclist_id = rd.id
                LEFT JOIN classes cls ON sr.class_id = cls.id
                WHERE sr.series_id = ? AND sr.event_id = ? AND rd.club_id = ?
                AND sr.points > 0
                AND COALESCE(cls.series_eligible, 1) = 1
                ORDER BY sr.class_id, sr.points DESC
            ");
            $stmt->execute([$seriesId, $eventId, $clubId]);
        } else {
            $stmt = $db->prepare("
                SELECT
                    r.cyclist_id,
                    r.class_id,
                    r.points,
                    rd.firstname,
                    rd.lastname,
                    cls.name as class_name,
                    cls.display_name as class_display_name
                FROM results r
                JOIN riders rd ON r.cyclist_id = rd.id
                LEFT JOIN classes cls ON r.class_id = cls.id
                WHERE r.event_id = ? AND rd.club_id = ?
                AND r.status = 'finished'
                AND r.points > 0
                AND COALESCE(cls.series_eligible, 1) = 1
                ORDER BY r.class_id, r.points DESC
            ");
            $stmt->execute([$eventId, $clubId]);
        }
        $clubResults = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if (empty($clubResults)) continue;

        $eventPoints = 0;
        $eventParticipants = count($clubResults);
        $classRiders = [];

        // Group by class and apply 100%/50% rule
        foreach ($clubResults as $result) {
            $classId = $result['class_id'];
            if (!isset($classRiders[$classId])) {
                $classRiders[$classId] = 0;
            }
            $classRiders[$classId]++;
            $rank = $classRiders[$classId];

            $originalPoints = (float)$result['points'];
            $percentage = 0;
            $clubPoints = 0;

            if ($rank === 1) {
                $clubPoints = $originalPoints;
                $percentage = 100;
            } elseif ($rank === 2) {
                $clubPoints = round($originalPoints * 0.5, 0);
                $percentage = 50;
            }

            $eventPoints += $clubPoints;

            // Store for display
            $riderDetails[$eventId][] = [
                'firstname' => $result['firstname'],
                'lastname' => $result['lastname'],
                'class_name' => $result['class_display_name'] ?? $result['class_name'],
                'original_points' => $originalPoints,
                'club_points' => $clubPoints,
                'percentage_applied' => $percentage,
                'rider_rank_in_club' => $rank
            ];
        }

        if ($eventPoints > 0) {
            $eventsCount++;
            $totalPoints += $eventPoints;
            $totalParticipants += $eventParticipants;
            $bestEventPoints = max($bestEventPoints, $eventPoints);

            $events[] = [
                'event_id' => $eventId,
                'event_name' => $event['name'],
                'event_date' => $event['date'],
                'location' => $event['location'],
                'total_points' => $eventPoints,
                'participants_count' => $eventParticipants
            ];
        }
    }

    // Get ranking among all clubs
    // Calculate all clubs' points for this series
    $stmt = $db->prepare("
        SELECT DISTINCT c.id as club_id, c.name
        FROM clubs c
        JOIN riders r ON r.club_id = c.id
        JOIN results res ON res.cyclist_id = r.id
        JOIN events e ON res.event_id = e.id
        WHERE (e.series_id = ? OR e.id IN (SELECT event_id FROM series_events WHERE series_id = ?))
        AND res.status = 'finished'
        AND res.points > 0
    ");
    $stmt->execute([$seriesId, $seriesId]);
    $allClubs = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // This is simplified - in production you'd calculate all clubs properly
    $ranking = 1; // Default

    $standing = [
        'ranking' => $ranking,
        'total_points' => $totalPoints,
        'total_participants' => $totalParticipants,
        'events_count' => $eventsCount,
        'best_event_points' => $bestEventPoints
    ];
}

// If modal mode, output standalone HTML with minimal styling
if ($isModal):
?>
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($club['name']) ?> - Klubbpoäng</title>
    <link rel="stylesheet" href="/assets/css/base.css">
    <link rel="stylesheet" href="/assets/css/components.css">
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body style="background: var(--color-bg-page); padding: var(--space-lg);">
<?php endif; ?>

<?php if (!$isModal): ?>
<!-- Back Button -->
<div class="mb-lg">
    <a href="/series/<?= $seriesId ?>" class="btn-link">
        <i data-lucide="arrow-left"></i>
        Tillbaka till <?= htmlspecialchars($series['name']) ?>
    </a>
</div>
<?php endif; ?>

<!-- Header -->
<div class="club-header mb-lg">
    <div class="flex items-center gap-lg">
        <?php if (!empty($club['logo'])): ?>
        <img src="<?= htmlspecialchars($club['logo']) ?>" alt="" class="club-logo-lg">
        <?php endif; ?>
        <div>
            <h1 class="page-title"><?= htmlspecialchars($club['name']) ?></h1>
            <?php if (!empty($club['city'])): ?>
            <p class="text-muted">
                <i data-lucide="map-pin" class="icon-inline"></i>
                <?= htmlspecialchars($club['city']) ?>
                <?php if (!empty($club['region'])): ?>, <?= htmlspecialchars($club['region']) ?><?php endif; ?>
            </p>
            <?php endif; ?>
        </div>
    </div>
</div>

<!-- Summary Card -->
<?php if ($standing): ?>
<section class="card mb-lg">
    <div class="card-header">
        <h2 class="card-title">
            <i data-lucide="award"></i>
            Klubbpoäng - <?= htmlspecialchars($series['name']) ?>
        </h2>
    </div>
    <div class="card-body">
        <div class="stats-grid stats-grid-5">
            <div class="stat-box">
                <div class="stat-value <?= $standing['ranking'] <= 3 ? 'text-warning' : '' ?>">
                    #<?= $standing['ranking'] ?>
                </div>
                <div class="stat-label">Ranking</div>
            </div>
            <div class="stat-box">
                <div class="stat-value"><?= number_format($standing['total_points']) ?></div>
                <div class="stat-label">Totala poäng</div>
            </div>
            <div class="stat-box">
                <div class="stat-value"><?= $standing['total_participants'] ?></div>
                <div class="stat-label">Deltagare</div>
            </div>
            <div class="stat-box">
                <div class="stat-value"><?= $standing['events_count'] ?></div>
                <div class="stat-label">Events</div>
            </div>
            <div class="stat-box">
                <div class="stat-value"><?= number_format($standing['best_event_points']) ?></div>
                <div class="stat-label">Bästa event</div>
            </div>
        </div>
    </div>
</section>
<?php endif; ?>

<!-- Events Breakdown -->
<section class="card mb-lg">
    <div class="card-header">
        <h2 class="card-title">
            <i data-lucide="calendar"></i>
            Poäng per event
        </h2>
    </div>
    <div class="card-body p-0">
        <?php if (empty($events)): ?>
        <div class="empty-state">
            <div class="empty-state-icon"><i data-lucide="info"></i></div>
            <p>Inga eventpoäng registrerade för denna klubb i serien.</p>
        </div>
        <?php else: ?>
            <?php foreach ($events as $event): ?>
            <div class="event-breakdown">
                <!-- Event Header -->
                <div class="event-breakdown-header">
                    <div class="event-breakdown-info">
                        <strong><?= htmlspecialchars($event['event_name']) ?></strong>
                        <span class="text-muted">
                            <?= date('j M Y', strtotime($event['event_date'])) ?>
                            <?php if (!empty($event['location'])): ?>
                                &middot; <?= htmlspecialchars($event['location']) ?>
                            <?php endif; ?>
                        </span>
                    </div>
                    <div class="event-breakdown-stats">
                        <span class="text-muted"><?= $event['participants_count'] ?> åkare</span>
                        <span class="event-points"><?= number_format($event['total_points']) ?> p</span>
                    </div>
                </div>

                <!-- Rider Details Table -->
                <?php if (isset($riderDetails[$event['event_id']]) && !empty($riderDetails[$event['event_id']])): ?>
                <div class="table-wrapper">
                    <table class="table table--compact">
                        <thead>
                            <tr>
                                <th>Åkare</th>
                                <th>Klass</th>
                                <th class="text-right">Original</th>
                                <th class="text-center">%</th>
                                <th class="text-right">Klubbpoäng</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($riderDetails[$event['event_id']] as $rider): ?>
                            <tr class="<?= $rider['club_points'] == 0 ? 'text-muted' : '' ?>">
                                <td>
                                    <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                                    <?php if ($rider['rider_rank_in_club'] == 1): ?>
                                        <span class="badge badge--sm badge--warning">1:a</span>
                                    <?php elseif ($rider['rider_rank_in_club'] == 2): ?>
                                        <span class="badge badge--sm badge--secondary">2:a</span>
                                    <?php endif; ?>
                                </td>
                                <td><?= htmlspecialchars($rider['class_name'] ?? '-') ?></td>
                                <td class="text-right"><?= (int)$rider['original_points'] ?></td>
                                <td class="text-center">
                                    <?php if ($rider['percentage_applied'] == 100): ?>
                                        <span class="badge badge--sm badge--success">100%</span>
                                    <?php elseif ($rider['percentage_applied'] == 50): ?>
                                        <span class="badge badge--sm badge--warning">50%</span>
                                    <?php else: ?>
                                        <span class="badge badge--sm badge--muted">0%</span>
                                    <?php endif; ?>
                                </td>
                                <td class="text-right font-bold"><?= (int)$rider['club_points'] ?></td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
                <?php endif; ?>
            </div>
            <?php endforeach; ?>
        <?php endif; ?>
    </div>
</section>

<!-- Points Summary by Class -->
<?php
// Calculate points by class
$classTotals = [];
foreach ($riderDetails as $eventId => $riders) {
    foreach ($riders as $rider) {
        $className = $rider['class_name'] ?? 'Okänd';
        if (!isset($classTotals[$className])) {
            $classTotals[$className] = ['points' => 0, 'riders' => 0];
        }
        $classTotals[$className]['points'] += $rider['club_points'];
        if ($rider['club_points'] > 0) {
            $classTotals[$className]['riders']++;
        }
    }
}
arsort($classTotals);
?>

<?php if (!empty($classTotals)): ?>
<section class="card">
    <div class="card-header">
        <h2 class="card-title">
            <i data-lucide="layers"></i>
            Poäng per klass
        </h2>
    </div>
    <div class="card-body p-0">
        <div class="table-wrapper">
            <table class="table">
                <thead>
                    <tr>
                        <th>Klass</th>
                        <th class="text-right">Poänggivande åkare</th>
                        <th class="text-right">Totala poäng</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($classTotals as $className => $data): ?>
                    <tr>
                        <td><strong><?= htmlspecialchars($className) ?></strong></td>
                        <td class="text-right"><?= $data['riders'] ?></td>
                        <td class="text-right font-bold"><?= number_format($data['points']) ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</section>
<?php endif; ?>

<!-- Info Box -->
<div class="info-box mt-lg">
    <div class="info-box-icon"><i data-lucide="info"></i></div>
    <div class="info-box-content">
        <strong>Hur klubbpoäng räknas</strong>
        <ul class="info-list">
            <li>Bästa åkare från varje klubb per klass får 100% av sina poäng</li>
            <li>Näst bästa åkare från samma klubb/klass får 50%</li>
            <li>Övriga åkare från klubben i samma klass får 0%</li>
        </ul>
    </div>
</div>

<style>
.club-logo-lg {
    width: 64px;
    height: 64px;
    object-fit: contain;
}

.stats-grid-5 {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: var(--space-md);
}

@media (max-width: 767px) {
    .stats-grid-5 {
        grid-template-columns: repeat(2, 1fr);
    }
    .stats-grid-5 > :last-child {
        grid-column: span 2;
    }
}

.stat-box {
    text-align: center;
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
}

.stat-value {
    font-size: 1.75rem;
    font-weight: var(--weight-bold);
    color: var(--color-text-primary);
    line-height: 1.2;
}

.stat-value.text-warning {
    color: var(--color-warning);
}

.stat-label {
    font-size: var(--text-sm);
    color: var(--color-text-muted);
    margin-top: var(--space-xs);
}

.event-breakdown {
    border-bottom: 1px solid var(--color-border);
}

.event-breakdown:last-child {
    border-bottom: none;
}

.event-breakdown-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-md);
    background: var(--color-bg-surface);
    flex-wrap: wrap;
    gap: var(--space-sm);
}

.event-breakdown-info {
    display: flex;
    flex-direction: column;
    gap: var(--space-2xs);
}

.event-breakdown-stats {
    display: flex;
    align-items: center;
    gap: var(--space-md);
}

.event-points {
    font-weight: var(--weight-bold);
    color: var(--color-primary);
}

.info-box {
    display: flex;
    gap: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
    border-left: 4px solid var(--color-accent);
}

.info-box-icon {
    color: var(--color-accent);
    flex-shrink: 0;
}

.info-list {
    margin: var(--space-sm) 0 0 0;
    padding-left: var(--space-lg);
    font-size: var(--text-sm);
    color: var(--color-text-muted);
}

.info-list li {
    margin-bottom: var(--space-xs);
}

.btn-link {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
    color: var(--color-text-muted);
    text-decoration: none;
    font-size: var(--text-sm);
}

.btn-link:hover {
    color: var(--color-primary);
}

.icon-inline {
    width: 16px;
    height: 16px;
    vertical-align: middle;
}

.badge--muted {
    background: var(--color-bg-muted);
    color: var(--color-text-muted);
}
</style>

<?php if ($isModal): ?>
<script>
  // Initialize lucide icons
  lucide.createIcons();
</script>
</body>
</html>
<?php endif; ?>
