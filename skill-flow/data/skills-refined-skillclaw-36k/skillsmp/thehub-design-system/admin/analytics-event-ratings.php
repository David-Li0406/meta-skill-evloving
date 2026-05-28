<?php
/**
 * TheHUB Admin - Event Ratings Report
 * Shows aggregated event ratings for organizers and series admins
 * All data is anonymous - individual ratings are not shown
 */

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../includes/auth.php';
requireAdmin();

$pdo = hub_db();

$pageTitle = 'Event Ratings';
include __DIR__ . '/../includes/admin-header.php';

// Filters
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : date('Y');
$selectedSeries = isset($_GET['series']) ? (int)$_GET['series'] : 0;

// Get available years
$years = [];
try {
    $yearStmt = $pdo->query("SELECT DISTINCT YEAR(date) as y FROM events WHERE date IS NOT NULL ORDER BY y DESC");
    $years = $yearStmt->fetchAll(PDO::FETCH_COLUMN);
} catch (PDOException $e) {
    $years = [date('Y')];
}

// Get series for filter
$seriesList = [];
try {
    $seriesStmt = $pdo->query("SELECT id, name FROM series WHERE status = 'active' ORDER BY name");
    $seriesList = $seriesStmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {}

// Get event ratings summary
$eventRatings = [];
$totalResponses = 0;
$overallAvg = 0;

try {
    $sql = "
        SELECT
            e.id AS event_id,
            e.name AS event_name,
            e.date AS event_date,
            e.location,
            s.name AS series_name,
            COUNT(er.id) AS response_count,
            ROUND(AVG(er.overall_rating), 1) AS avg_rating,
            MIN(er.overall_rating) AS min_rating,
            MAX(er.overall_rating) AS max_rating
        FROM events e
        LEFT JOIN event_ratings er ON e.id = er.event_id
        LEFT JOIN series s ON e.series_id = s.id
        WHERE YEAR(e.date) = ?
    ";
    $params = [$selectedYear];

    if ($selectedSeries) {
        $sql .= " AND e.series_id = ?";
        $params[] = $selectedSeries;
    }

    $sql .= "
        GROUP BY e.id, e.name, e.date, e.location, s.name
        HAVING response_count > 0
        ORDER BY e.date DESC
    ";

    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $eventRatings = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Calculate totals
    foreach ($eventRatings as $er) {
        $totalResponses += $er['response_count'];
    }

    if ($totalResponses > 0) {
        $avgStmt = $pdo->prepare("
            SELECT ROUND(AVG(overall_rating), 1) FROM event_ratings er
            JOIN events e ON er.event_id = e.id
            WHERE YEAR(e.date) = ?
            " . ($selectedSeries ? " AND e.series_id = ?" : "")
        );
        $avgStmt->execute($selectedSeries ? [$selectedYear, $selectedSeries] : [$selectedYear]);
        $overallAvg = $avgStmt->fetchColumn() ?: 0;
    }
} catch (PDOException $e) {
    // Tables might not exist yet
}

// Get question averages if we have data
$questionAverages = [];
try {
    $qSql = "
        SELECT
            q.question_key,
            q.question_text,
            q.category,
            COUNT(a.id) AS response_count,
            ROUND(AVG(a.score), 1) AS avg_score
        FROM event_rating_questions q
        LEFT JOIN event_rating_answers a ON q.id = a.question_id
        LEFT JOIN event_ratings er ON a.rating_id = er.id
        LEFT JOIN events e ON er.event_id = e.id
        WHERE q.active = 1
          AND (e.id IS NULL OR YEAR(e.date) = ?)
    ";
    $qParams = [$selectedYear];

    if ($selectedSeries) {
        $qSql .= " AND (e.id IS NULL OR e.series_id = ?)";
        $qParams[] = $selectedSeries;
    }

    $qSql .= " GROUP BY q.id, q.question_key, q.question_text, q.category ORDER BY q.sort_order";

    $qStmt = $pdo->prepare($qSql);
    $qStmt->execute($qParams);
    $questionAverages = $qStmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {}
?>

<div class="admin-content">
    <div class="page-header">
        <h1><i data-lucide="star" class="page-icon"></i> <?= $pageTitle ?></h1>
        <p class="page-description">Aggregerade betyg fran deltagare (anonymiserade)</p>
    </div>

    <!-- Filters -->
    <div class="card mb-lg">
        <div class="card-body">
            <form method="GET" class="filter-row">
                <div class="form-group">
                    <label class="form-label">Ar</label>
                    <select name="year" class="form-select" onchange="this.form.submit()">
                        <?php foreach ($years as $y): ?>
                            <option value="<?= $y ?>" <?= $y == $selectedYear ? 'selected' : '' ?>><?= $y ?></option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Serie</label>
                    <select name="series" class="form-select" onchange="this.form.submit()">
                        <option value="0">Alla serier</option>
                        <?php foreach ($seriesList as $s): ?>
                            <option value="<?= $s['id'] ?>" <?= $s['id'] == $selectedSeries ? 'selected' : '' ?>>
                                <?= htmlspecialchars($s['name']) ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </form>
        </div>
    </div>

    <?php if (empty($eventRatings)): ?>
        <div class="alert alert-info">
            <i data-lucide="info"></i>
            Inga betyg har samlats in for denna period annu.
        </div>
    <?php else: ?>
        <!-- Summary Cards -->
        <div class="stats-grid mb-lg">
            <div class="stat-card">
                <div class="stat-icon"><i data-lucide="message-square"></i></div>
                <div class="stat-value"><?= $totalResponses ?></div>
                <div class="stat-label">Totalt antal svar</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i data-lucide="star"></i></div>
                <div class="stat-value"><?= $overallAvg ?></div>
                <div class="stat-label">Genomsnittligt betyg</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i data-lucide="calendar"></i></div>
                <div class="stat-value"><?= count($eventRatings) ?></div>
                <div class="stat-label">Events med betyg</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i data-lucide="users"></i></div>
                <div class="stat-value"><?= $totalResponses > 0 ? round($totalResponses / count($eventRatings), 1) : 0 ?></div>
                <div class="stat-label">Snitt svar/event</div>
            </div>
        </div>

        <!-- Question Averages -->
        <?php if (!empty($questionAverages) && $questionAverages[0]['response_count'] > 0): ?>
            <div class="card mb-lg">
                <div class="card-header">
                    <h2><i data-lucide="bar-chart-3"></i> Genomsnitt per fraga</h2>
                </div>
                <div class="card-body">
                    <div class="question-bars">
                        <?php foreach ($questionAverages as $q): ?>
                            <?php if ($q['response_count'] > 0): ?>
                                <div class="question-bar-row">
                                    <span class="question-bar-label"><?= htmlspecialchars($q['question_text']) ?></span>
                                    <div class="question-bar-container">
                                        <div class="question-bar" style="width: <?= ($q['avg_score'] / 10) * 100 ?>%"></div>
                                        <span class="question-bar-value"><?= $q['avg_score'] ?></span>
                                    </div>
                                </div>
                            <?php endif; ?>
                        <?php endforeach; ?>
                    </div>
                </div>
            </div>
        <?php endif; ?>

        <!-- Events Table -->
        <div class="card">
            <div class="card-header">
                <h2><i data-lucide="list"></i> Events</h2>
            </div>
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Event</th>
                            <th>Serie</th>
                            <th>Datum</th>
                            <th class="text-center">Svar</th>
                            <th class="text-center">Snitt</th>
                            <th class="text-center">Min</th>
                            <th class="text-center">Max</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($eventRatings as $er): ?>
                            <tr>
                                <td>
                                    <strong><?= htmlspecialchars($er['event_name']) ?></strong>
                                    <?php if ($er['location']): ?>
                                        <br><small class="text-muted"><?= htmlspecialchars($er['location']) ?></small>
                                    <?php endif; ?>
                                </td>
                                <td><?= htmlspecialchars($er['series_name'] ?? '-') ?></td>
                                <td><?= date('j M Y', strtotime($er['event_date'])) ?></td>
                                <td class="text-center"><?= $er['response_count'] ?></td>
                                <td class="text-center">
                                    <span class="rating-badge rating-<?= $er['avg_rating'] >= 7 ? 'good' : ($er['avg_rating'] >= 5 ? 'ok' : 'low') ?>">
                                        <?= $er['avg_rating'] ?>
                                    </span>
                                </td>
                                <td class="text-center text-muted"><?= $er['min_rating'] ?></td>
                                <td class="text-center text-muted"><?= $er['max_rating'] ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    <?php endif; ?>
</div>

<style>
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: var(--space-md);
}

.stat-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    text-align: center;
}

.stat-icon {
    width: 40px;
    height: 40px;
    margin: 0 auto var(--space-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-accent-light);
    border-radius: var(--radius-md);
    color: var(--color-accent);
}

.stat-icon i {
    width: 20px;
    height: 20px;
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-text-primary);
}

.stat-label {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
}

.question-bars {
    display: flex;
    flex-direction: column;
    gap: var(--space-md);
}

.question-bar-row {
    display: flex;
    align-items: center;
    gap: var(--space-md);
}

.question-bar-label {
    min-width: 250px;
    font-size: 0.875rem;
    color: var(--color-text-secondary);
}

.question-bar-container {
    flex: 1;
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.question-bar {
    height: 24px;
    background: linear-gradient(90deg, var(--color-accent), var(--color-accent-hover));
    border-radius: var(--radius-sm);
    min-width: 20px;
}

.question-bar-value {
    min-width: 30px;
    font-weight: 600;
    color: var(--color-accent);
}

.rating-badge {
    display: inline-block;
    padding: var(--space-2xs) var(--space-sm);
    border-radius: var(--radius-full);
    font-weight: 600;
    font-size: 0.875rem;
}

.rating-good {
    background: rgba(16, 185, 129, 0.15);
    color: var(--color-success);
}

.rating-ok {
    background: rgba(251, 191, 36, 0.15);
    color: var(--color-warning);
}

.rating-low {
    background: rgba(239, 68, 68, 0.15);
    color: var(--color-error);
}

.filter-row {
    display: flex;
    gap: var(--space-md);
    flex-wrap: wrap;
}

.filter-row .form-group {
    margin: 0;
    min-width: 150px;
}

@media (max-width: 768px) {
    .question-bar-row {
        flex-direction: column;
        align-items: flex-start;
    }

    .question-bar-label {
        min-width: auto;
    }

    .question-bar-container {
        width: 100%;
    }
}
</style>

<?php include __DIR__ . '/../includes/admin-footer.php'; ?>
