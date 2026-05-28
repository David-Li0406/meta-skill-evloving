<?php
/**
 * AJAX endpoint for rider series standings
 * Returns HTML for the series content section
 */

require_once __DIR__ . '/../hub-config.php';

$db = hub_db();
$riderId = intval($_GET['id'] ?? 0);
$selectedSeriesYear = intval($_GET['year'] ?? date('Y'));

if (!$riderId) {
    echo '<div class="series-empty-state"><p class="text-muted">Ogiltig förfrågan</p></div>';
    exit;
}

// Get series standings for the selected year
$seriesStandings = [];
try {
    $seriesStmt = $db->prepare("
        SELECT
            sr.cyclist_id, sr.series_id, sr.class_id, sr.ranking, sr.total_points,
            sr.events_count, sr.wins, sr.podiums, sr.trend,
            s.name as series_name, s.logo as series_logo, s.primary_color as series_color,
            cl.name as class_name, cl.display_name as class_display_name,
            (SELECT COUNT(*) FROM series_results WHERE series_id = sr.series_id AND class_id = sr.class_id AND year = sr.year) as total_riders
        FROM series_results sr
        JOIN series s ON sr.series_id = s.id
        LEFT JOIN classes cl ON sr.class_id = cl.id
        WHERE sr.cyclist_id = ? AND sr.year = ?
        ORDER BY s.sort_order, cl.sort_order
    ");
    $seriesStmt->execute([$riderId, $selectedSeriesYear]);
    $seriesStandings = $seriesStmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    // Ignore errors
}

if (!empty($seriesStandings)):
?>
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
</div>
<?php endif; ?>
