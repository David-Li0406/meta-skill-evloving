<?php
/**
 * Analytics Data Quality Panel
 *
 * Visar datakvalitetsmatningar for att identifiera problem med:
 * - Saknade fodelseår
 * - Saknade klubbar
 * - Saknade klasser
 * - Saknade regioner
 * - Potentiella dubbletter
 *
 * @package TheHUB Admin
 */

require_once __DIR__ . '/../config.php';
require_admin();

require_once __DIR__ . '/../analytics/includes/KPICalculator.php';
require_once __DIR__ . '/../analytics/includes/AnalyticsConfig.php';

$pageTitle = 'Datakvalitet';
include __DIR__ . '/../includes/admin-header.php';

$pdo = hub_db();
$kpi = new KPICalculator($pdo);

// Hamta tillgangliga ar
$years = $pdo->query("
    SELECT DISTINCT season_year
    FROM rider_yearly_stats
    ORDER BY season_year DESC
")->fetchAll(PDO::FETCH_COLUMN);

$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : ($years[0] ?? date('Y'));

// Hamta datakvalitetsmetrics
$metrics = $kpi->getDataQualityMetrics($selectedYear);

// Hamta historik
$historyStmt = $pdo->prepare("
    SELECT *
    FROM data_quality_metrics
    WHERE season_year = ?
    ORDER BY measured_at DESC
    LIMIT 10
");
$historyStmt->execute([$selectedYear]);
$history = $historyStmt->fetchAll(PDO::FETCH_ASSOC);

// Thresholds fran config
$thresholds = AnalyticsConfig::DATA_QUALITY_THRESHOLDS;
?>

<div class="admin-content">
    <div class="page-header">
        <h1><i data-lucide="shield-check"></i> <?= $pageTitle ?></h1>
        <p class="text-muted">Analysera och forbattra datakvaliteten i analytics-plattformen</p>
    </div>

    <!-- Filter -->
    <div class="card mb-lg">
        <div class="card-body">
            <form method="get" class="filter-row">
                <div class="form-group">
                    <label class="form-label">Sasong</label>
                    <select name="year" class="form-select" onchange="this.form.submit()">
                        <?php foreach ($years as $y): ?>
                            <option value="<?= $y ?>" <?= $y == $selectedYear ? 'selected' : '' ?>><?= $y ?></option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <div class="form-group">
                    <button type="button" class="btn btn-secondary" onclick="saveMetrics()">
                        <i data-lucide="save"></i> Spara matning
                    </button>
                </div>
            </form>
        </div>
    </div>

    <?php if (isset($metrics['error'])): ?>
        <div class="alert alert-warning"><?= htmlspecialchars($metrics['error']) ?></div>
    <?php else: ?>

    <!-- Overall Status -->
    <div class="card mb-lg">
        <div class="card-header">
            <h3>
                <i data-lucide="activity"></i>
                Overall Status:
                <?php
                $statusClass = match($metrics['quality_status']) {
                    'good' => 'badge-success',
                    'warning' => 'badge-warning',
                    'critical' => 'badge-danger',
                    default => 'badge-secondary'
                };
                $statusText = match($metrics['quality_status']) {
                    'good' => 'Bra',
                    'warning' => 'Varning',
                    'critical' => 'Kritisk',
                    default => 'Okand'
                };
                ?>
                <span class="badge <?= $statusClass ?>"><?= $statusText ?></span>
            </h3>
        </div>
        <div class="card-body">
            <div class="grid grid-cols-4 gap-md">
                <div class="stat-card">
                    <div class="stat-value"><?= number_format($metrics['total_riders']) ?></div>
                    <div class="stat-label">Totalt riders</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value"><?= $metrics['potential_duplicates'] ?></div>
                    <div class="stat-label">Potentiella dubbletter</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value"><?= $metrics['merged_riders'] ?></div>
                    <div class="stat-label">Sammanslagna riders</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value"><?= date('Y-m-d H:i', strtotime($metrics['measured_at'])) ?></div>
                    <div class="stat-label">Senast matt</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Coverage Metrics -->
    <div class="card mb-lg">
        <div class="card-header">
            <h3><i data-lucide="pie-chart"></i> Datatackning</h3>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Falt</th>
                            <th>Tackning</th>
                            <th>Tröskel</th>
                            <th>Status</th>
                            <th>Saknas</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        $coverageFields = [
                            'birth_year_coverage' => ['label' => 'Fodelseår', 'threshold' => $thresholds['birth_year_coverage'] * 100, 'missing' => 'riders_missing_birth_year'],
                            'club_coverage' => ['label' => 'Klubb', 'threshold' => $thresholds['club_coverage'] * 100, 'missing' => 'riders_missing_club'],
                            'gender_coverage' => ['label' => 'Kon', 'threshold' => 50, 'missing' => 'riders_missing_gender'],
                            'class_coverage' => ['label' => 'Klass (resultat)', 'threshold' => ($thresholds['class_coverage'] ?? 0.7) * 100, 'missing' => 'results_missing_class'],
                            'event_date_coverage' => ['label' => 'Event-datum', 'threshold' => $thresholds['event_date_coverage'] * 100, 'missing' => null],
                        ];

                        foreach ($coverageFields as $key => $field):
                            $value = $metrics[$key] ?? 0;
                            $threshold = $field['threshold'];
                            $isBelowThreshold = $value < $threshold;
                            $statusClass = $isBelowThreshold ? 'badge-danger' : 'badge-success';
                            $statusText = $isBelowThreshold ? 'Under tröskel' : 'OK';
                            $missing = $field['missing'] ? ($metrics[$field['missing']] ?? 0) : '-';
                        ?>
                        <tr>
                            <td><strong><?= $field['label'] ?></strong></td>
                            <td>
                                <div class="progress-bar-container">
                                    <div class="progress-bar <?= $isBelowThreshold ? 'warning' : 'success' ?>"
                                         style="width: <?= min($value, 100) ?>%"></div>
                                </div>
                                <span><?= $value ?>%</span>
                            </td>
                            <td><?= $threshold ?>%</td>
                            <td><span class="badge <?= $statusClass ?>"><?= $statusText ?></span></td>
                            <td><?= is_numeric($missing) ? number_format($missing) : $missing ?></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Recommendations -->
    <div class="card mb-lg">
        <div class="card-header">
            <h3><i data-lucide="lightbulb"></i> Rekommendationer</h3>
        </div>
        <div class="card-body">
            <ul class="recommendations-list">
                <?php if ($metrics['birth_year_coverage'] < $thresholds['birth_year_coverage'] * 100): ?>
                <li class="recommendation warning">
                    <i data-lucide="alert-triangle"></i>
                    <div>
                        <strong>Lat fodelseår-tackning (<?= $metrics['birth_year_coverage'] ?>%)</strong>
                        <p>At-Risk berakningar som anvander alder kan bli opålitliga.
                           Overväg att importera fodelseår fran licenssystemet.</p>
                    </div>
                </li>
                <?php endif; ?>

                <?php if ($metrics['club_coverage'] < $thresholds['club_coverage'] * 100): ?>
                <li class="recommendation warning">
                    <i data-lucide="alert-triangle"></i>
                    <div>
                        <strong>Lat klubb-tackning (<?= $metrics['club_coverage'] ?>%)</strong>
                        <p>Klubbstatistik och geografisk analys blir ofullstandig.
                           Matchning mot SCF-registret kan forbattra detta.</p>
                    </div>
                </li>
                <?php endif; ?>

                <?php if ($metrics['potential_duplicates'] > 0): ?>
                <li class="recommendation info">
                    <i data-lucide="users"></i>
                    <div>
                        <strong><?= $metrics['potential_duplicates'] ?> potentiella dubbletter hittade</strong>
                        <p>Anvand <a href="riders-merge.php">Rider Merge-verktyget</a> for att granska
                           och sla ihop dubbletter.</p>
                    </div>
                </li>
                <?php endif; ?>

                <?php if ($metrics['quality_status'] === 'good'): ?>
                <li class="recommendation success">
                    <i data-lucide="check-circle"></i>
                    <div>
                        <strong>Datakvaliteten ar god!</strong>
                        <p>Alla viktiga falt har tillracklig tackning for tillforlitliga analyser.</p>
                    </div>
                </li>
                <?php endif; ?>
            </ul>
        </div>
    </div>

    <!-- History -->
    <?php if (!empty($history)): ?>
    <div class="card">
        <div class="card-header">
            <h3><i data-lucide="history"></i> Matningshistorik</h3>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Datum</th>
                            <th>Fodelseår</th>
                            <th>Klubb</th>
                            <th>Kon</th>
                            <th>Klass</th>
                            <th>Dubbletter</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($history as $h): ?>
                        <tr>
                            <td><?= date('Y-m-d H:i', strtotime($h['measured_at'])) ?></td>
                            <td><?= $h['birth_year_coverage'] ?>%</td>
                            <td><?= $h['club_coverage'] ?>%</td>
                            <td><?= $h['gender_coverage'] ?>%</td>
                            <td><?= $h['class_coverage'] ?>%</td>
                            <td><?= $h['potential_duplicates'] ?></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <?php endif; ?>
</div>

<style>
.stat-card {
    background: var(--color-bg-surface);
    padding: var(--space-md);
    border-radius: var(--radius-md);
    text-align: center;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-accent);
}

.stat-label {
    font-size: 0.85rem;
    color: var(--color-text-muted);
    margin-top: var(--space-xs);
}

.progress-bar-container {
    width: 100px;
    height: 8px;
    background: var(--color-bg-surface);
    border-radius: var(--radius-full);
    overflow: hidden;
    display: inline-block;
    margin-right: var(--space-sm);
}

.progress-bar {
    height: 100%;
    border-radius: var(--radius-full);
}

.progress-bar.success {
    background: var(--color-success);
}

.progress-bar.warning {
    background: var(--color-warning);
}

.recommendations-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.recommendation {
    display: flex;
    align-items: flex-start;
    gap: var(--space-md);
    padding: var(--space-md);
    margin-bottom: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
    border-left: 4px solid var(--color-border);
}

.recommendation.warning {
    border-left-color: var(--color-warning);
}

.recommendation.info {
    border-left-color: var(--color-info);
}

.recommendation.success {
    border-left-color: var(--color-success);
}

.recommendation i {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    color: var(--color-text-muted);
}

.recommendation.warning i {
    color: var(--color-warning);
}

.recommendation.info i {
    color: var(--color-info);
}

.recommendation.success i {
    color: var(--color-success);
}

.recommendation strong {
    display: block;
    margin-bottom: var(--space-xs);
}

.recommendation p {
    margin: 0;
    color: var(--color-text-secondary);
    font-size: 0.9rem;
}

.grid {
    display: grid;
}

.grid-cols-4 {
    grid-template-columns: repeat(4, 1fr);
}

.gap-md {
    gap: var(--space-md);
}

@media (max-width: 768px) {
    .grid-cols-4 {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>

<script>
function saveMetrics() {
    const year = document.querySelector('select[name="year"]').value;

    fetch(`/api/analytics/save-quality-metrics.php?year=${year}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert('Matning sparad!');
            location.reload();
        } else {
            alert('Fel: ' + (data.error || 'Okant fel'));
        }
    })
    .catch(err => {
        alert('Fel vid sparning: ' + err.message);
    });
}
</script>

<?php include __DIR__ . '/../includes/admin-footer.php'; ?>
