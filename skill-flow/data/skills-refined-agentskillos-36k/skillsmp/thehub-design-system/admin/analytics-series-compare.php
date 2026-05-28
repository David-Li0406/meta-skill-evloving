<?php
/**
 * Analytics Series Compare - Jämför Varumärken
 *
 * Välj valfritt antal varumärken per grupp (A, B, C) och jämför dem.
 * Varje grupp aggregerar alla valda varumärken.
 *
 * @package TheHUB Analytics
 * @version 2.0
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';

requireAnalyticsAccess();

global $pdo;

// Antal år att visa
$numYears = isset($_GET['years']) ? max(3, min(15, (int)$_GET['years'])) : 10;

// Hämta tillgängliga år
$availableYears = [];
try {
    $stmt = $pdo->query("SELECT DISTINCT season_year FROM series_participation ORDER BY season_year ASC");
    $availableYears = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {
    $error = $e->getMessage();
}

$yearsToShow = array_slice($availableYears, -$numYears);

// Hämta alla varumärken från series_brands
$allBrands = [];
try {
    $stmt = $pdo->query("
        SELECT
            sb.id,
            sb.name,
            sb.accent_color,
            sb.active,
            COUNT(DISTINCT s.id) as series_count
        FROM series_brands sb
        LEFT JOIN series s ON s.brand_id = sb.id
        GROUP BY sb.id
        ORDER BY sb.display_order ASC, sb.name ASC
    ");
    $allBrands = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    $error = "Kunde inte hämta varumärken: " . $e->getMessage();
}

// Parse valda varumärken per grupp (kommaseparerade IDs)
$groupA = isset($_GET['a']) ? array_filter(array_map('intval', explode(',', $_GET['a']))) : [];
$groupB = isset($_GET['b']) ? array_filter(array_map('intval', explode(',', $_GET['b']))) : [];
$groupC = isset($_GET['c']) ? array_filter(array_map('intval', explode(',', $_GET['c']))) : [];

// Gruppnamn baserade på valda varumärken
function getGroupName($brandIds, $allBrands) {
    if (empty($brandIds)) return '';
    $names = [];
    foreach ($brandIds as $id) {
        foreach ($allBrands as $b) {
            if ($b['id'] == $id) {
                $names[] = $b['name'];
                break;
            }
        }
    }
    if (count($names) <= 2) {
        return implode(' + ', $names);
    }
    return $names[0] . ' +' . (count($names) - 1);
}

/**
 * Hämta alla series_id för flera varumärken
 */
function getSeriesIdsForBrands($pdo, $brandIds) {
    if (empty($brandIds)) return [];
    $placeholders = implode(',', array_fill(0, count($brandIds), '?'));
    $stmt = $pdo->prepare("SELECT id FROM series WHERE brand_id IN ($placeholders)");
    $stmt->execute($brandIds);
    return $stmt->fetchAll(PDO::FETCH_COLUMN);
}

/**
 * Beräkna KPIs för en grupp av varumärken (aggregerat)
 */
function getGroupKPIs($pdo, $brandIds, $year) {
    $seriesIds = getSeriesIdsForBrands($pdo, $brandIds);

    if (empty($seriesIds)) {
        return [
            'total_riders' => 0,
            'new_riders' => 0,
            'retained_riders' => 0,
            'retention_rate' => 0,
            'churn_rate' => 0,
            'growth_rate' => 0,
            'cross_participation' => 0,
            'average_age' => 0,
            'female_pct' => 0
        ];
    }

    $placeholders = implode(',', array_fill(0, count($seriesIds), '?'));

    // Totalt antal unika deltagare i gruppens serier detta år
    $stmt = $pdo->prepare("
        SELECT COUNT(DISTINCT rider_id)
        FROM series_participation
        WHERE series_id IN ($placeholders) AND season_year = ?
    ");
    $stmt->execute([...$seriesIds, $year]);
    $totalRiders = (int)$stmt->fetchColumn();

    // Nya riders (första året i NÅGON serie - använd riders.first_season)
    $stmt = $pdo->prepare("
        SELECT COUNT(DISTINCT sp.rider_id)
        FROM series_participation sp
        JOIN riders r ON sp.rider_id = r.id
        WHERE sp.series_id IN ($placeholders)
        AND sp.season_year = ?
        AND r.first_season = ?
    ");
    $stmt->execute([...$seriesIds, $year, $year]);
    $newRiders = (int)$stmt->fetchColumn();

    // Retained - deltog i gruppens serier både detta och förra året
    $stmt = $pdo->prepare("
        SELECT COUNT(DISTINCT sp1.rider_id)
        FROM series_participation sp1
        WHERE sp1.series_id IN ($placeholders)
        AND sp1.season_year = ?
        AND EXISTS (
            SELECT 1 FROM series_participation sp2
            WHERE sp2.rider_id = sp1.rider_id
            AND sp2.series_id IN ($placeholders)
            AND sp2.season_year = ?
        )
    ");
    $stmt->execute([...$seriesIds, $year, ...$seriesIds, $year - 1]);
    $retainedRiders = (int)$stmt->fetchColumn();

    // Förra årets deltagare (för retention rate)
    $stmt = $pdo->prepare("
        SELECT COUNT(DISTINCT rider_id)
        FROM series_participation
        WHERE series_id IN ($placeholders) AND season_year = ?
    ");
    $stmt->execute([...$seriesIds, $year - 1]);
    $prevYearRiders = (int)$stmt->fetchColumn();

    // Retention rate
    $retentionRate = $prevYearRiders > 0 ? round($retainedRiders / $prevYearRiders * 100, 1) : 0;

    // Churn rate
    $churnRate = 100 - $retentionRate;

    // Growth rate
    $growthRate = $prevYearRiders > 0 ? round(($totalRiders - $prevYearRiders) / $prevYearRiders * 100, 1) : 0;

    // Cross-participation (deltar även i serier UTANFÖR denna grupp)
    $brandPlaceholders = implode(',', array_fill(0, count($brandIds), '?'));
    $stmt = $pdo->prepare("
        SELECT COUNT(DISTINCT sp1.rider_id)
        FROM series_participation sp1
        WHERE sp1.series_id IN ($placeholders) AND sp1.season_year = ?
        AND EXISTS (
            SELECT 1 FROM series_participation sp2
            JOIN series s2 ON sp2.series_id = s2.id
            WHERE sp2.rider_id = sp1.rider_id
            AND sp2.season_year = sp1.season_year
            AND (s2.brand_id IS NULL OR s2.brand_id NOT IN ($brandPlaceholders))
        )
    ");
    $stmt->execute([...$seriesIds, $year, ...$brandIds]);
    $crossCount = (int)$stmt->fetchColumn();
    $crossParticipation = $totalRiders > 0 ? round($crossCount / $totalRiders * 100, 1) : 0;

    // Genomsnittsålder
    $stmt = $pdo->prepare("
        SELECT AVG(? - r.birth_year) as avg_age
        FROM riders r
        WHERE r.id IN (
            SELECT DISTINCT rider_id FROM series_participation
            WHERE series_id IN ($placeholders) AND season_year = ?
        )
        AND r.birth_year IS NOT NULL AND r.birth_year > 1900
    ");
    $stmt->execute([$year, ...$seriesIds, $year]);
    $avgAge = round((float)$stmt->fetchColumn(), 1);

    // Andel kvinnor
    $stmt = $pdo->prepare("
        SELECT
            SUM(CASE WHEN r.gender = 'F' THEN 1 ELSE 0 END) as female,
            COUNT(*) as total
        FROM riders r
        WHERE r.id IN (
            SELECT DISTINCT rider_id FROM series_participation
            WHERE series_id IN ($placeholders) AND season_year = ?
        )
        AND r.gender IN ('M', 'F')
    ");
    $stmt->execute([...$seriesIds, $year]);
    $genderRow = $stmt->fetch();
    $femalePct = $genderRow['total'] > 0 ? round($genderRow['female'] / $genderRow['total'] * 100, 1) : 0;

    return [
        'total_riders' => $totalRiders,
        'new_riders' => $newRiders,
        'retained_riders' => $retainedRiders,
        'retention_rate' => $retentionRate,
        'churn_rate' => $churnRate,
        'growth_rate' => $growthRate,
        'cross_participation' => $crossParticipation,
        'average_age' => $avgAge,
        'female_pct' => $femalePct
    ];
}

// Samla trenddata för valda grupper
$groupTrends = [];
$groupLabels = [];
$groupColors = ['#37d4d6', '#f97316', '#a855f7'];
$activeGroups = [];

try {
    // Grupp A
    if (!empty($groupA)) {
        $activeGroups[] = 0;
        $groupLabels[0] = getGroupName($groupA, $allBrands);
        $trends = [];
        foreach ($yearsToShow as $year) {
            $kpis = getGroupKPIs($pdo, $groupA, $year);
            $trends[] = array_merge(['year' => $year], $kpis);
        }
        $groupTrends[0] = $trends;
    }

    // Grupp B
    if (!empty($groupB)) {
        $activeGroups[] = 1;
        $groupLabels[1] = getGroupName($groupB, $allBrands);
        $trends = [];
        foreach ($yearsToShow as $year) {
            $kpis = getGroupKPIs($pdo, $groupB, $year);
            $trends[] = array_merge(['year' => $year], $kpis);
        }
        $groupTrends[1] = $trends;
    }

    // Grupp C
    if (!empty($groupC)) {
        $activeGroups[] = 2;
        $groupLabels[2] = getGroupName($groupC, $allBrands);
        $trends = [];
        foreach ($yearsToShow as $year) {
            $kpis = getGroupKPIs($pdo, $groupC, $year);
            $trends[] = array_merge(['year' => $year], $kpis);
        }
        $groupTrends[2] = $trends;
    }
} catch (Exception $e) {
    $error = "Fel vid datahämtning: " . $e->getMessage();
}

$hasData = !empty($activeGroups) && !empty($groupTrends);

// Page config
$page_title = 'Jämför Varumärken';
$breadcrumbs = [
    ['label' => 'Dashboard', 'url' => '/admin/dashboard.php'],
    ['label' => 'Analytics', 'url' => '/admin/analytics-dashboard.php'],
    ['label' => 'Jämför Varumärken']
];

$page_actions = '
<div class="btn-group">
    <a href="/admin/analytics-trends.php" class="btn-admin btn-admin-secondary">
        <i data-lucide="trending-up"></i> Trender (Totalt)
    </a>
</div>
';

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

<!-- Selection Panel -->
<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="layers"></i> Välj varumärken att jämföra</h3>
    </div>
    <div class="card-body">
        <?php if (empty($allBrands)): ?>
            <div class="alert alert-warning">
                <i data-lucide="alert-triangle"></i>
                Inga varumärken hittades. Skapa varumärken under <a href="/admin/series-brands.php">Serie-varumärken</a>.
            </div>
        <?php else: ?>
        <p class="text-muted mb-md">Välj ett eller flera varumärken per grupp. Varje grupp visas som en linje i graferna.</p>

        <form method="get" id="compareForm">
            <input type="hidden" name="years" value="<?= $numYears ?>">
            <input type="hidden" name="a" id="inputA" value="<?= htmlspecialchars($_GET['a'] ?? '') ?>">
            <input type="hidden" name="b" id="inputB" value="<?= htmlspecialchars($_GET['b'] ?? '') ?>">
            <input type="hidden" name="c" id="inputC" value="<?= htmlspecialchars($_GET['c'] ?? '') ?>">

            <div class="brand-groups">
                <!-- Grupp A -->
                <div class="brand-group" data-group="a">
                    <div class="group-header">
                        <span class="group-color" style="background: <?= $groupColors[0] ?>"></span>
                        <span class="group-label">Grupp A</span>
                        <span class="group-count"><?= count($groupA) ?> valda</span>
                    </div>
                    <div class="brand-checkboxes">
                        <?php foreach ($allBrands as $brand): ?>
                        <label class="brand-checkbox <?= in_array($brand['id'], $groupA) ? 'checked' : '' ?>">
                            <input type="checkbox" value="<?= $brand['id'] ?>" <?= in_array($brand['id'], $groupA) ? 'checked' : '' ?>>
                            <span class="brand-name"><?= htmlspecialchars($brand['name']) ?></span>
                        </label>
                        <?php endforeach; ?>
                    </div>
                </div>

                <!-- Grupp B -->
                <div class="brand-group" data-group="b">
                    <div class="group-header">
                        <span class="group-color" style="background: <?= $groupColors[1] ?>"></span>
                        <span class="group-label">Grupp B</span>
                        <span class="group-count"><?= count($groupB) ?> valda</span>
                    </div>
                    <div class="brand-checkboxes">
                        <?php foreach ($allBrands as $brand): ?>
                        <label class="brand-checkbox <?= in_array($brand['id'], $groupB) ? 'checked' : '' ?>">
                            <input type="checkbox" value="<?= $brand['id'] ?>" <?= in_array($brand['id'], $groupB) ? 'checked' : '' ?>>
                            <span class="brand-name"><?= htmlspecialchars($brand['name']) ?></span>
                        </label>
                        <?php endforeach; ?>
                    </div>
                </div>

                <!-- Grupp C -->
                <div class="brand-group" data-group="c">
                    <div class="group-header">
                        <span class="group-color" style="background: <?= $groupColors[2] ?>"></span>
                        <span class="group-label">Grupp C</span>
                        <span class="group-count"><?= count($groupC) ?> valda</span>
                    </div>
                    <div class="brand-checkboxes">
                        <?php foreach ($allBrands as $brand): ?>
                        <label class="brand-checkbox <?= in_array($brand['id'], $groupC) ? 'checked' : '' ?>">
                            <input type="checkbox" value="<?= $brand['id'] ?>" <?= in_array($brand['id'], $groupC) ? 'checked' : '' ?>>
                            <span class="brand-name"><?= htmlspecialchars($brand['name']) ?></span>
                        </label>
                        <?php endforeach; ?>
                    </div>
                </div>
            </div>

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">
                    <i data-lucide="refresh-cw"></i> Uppdatera jämförelse
                </button>
                <?php if ($hasData): ?>
                <a href="?years=<?= $numYears ?>" class="btn btn-secondary">
                    <i data-lucide="x"></i> Rensa val
                </a>
                <?php endif; ?>
            </div>
        </form>
        <?php endif; ?>
    </div>
</div>

<!-- Year Range Selector -->
<div class="filter-bar">
    <form method="get" class="filter-form">
        <input type="hidden" name="a" value="<?= htmlspecialchars($_GET['a'] ?? '') ?>">
        <input type="hidden" name="b" value="<?= htmlspecialchars($_GET['b'] ?? '') ?>">
        <input type="hidden" name="c" value="<?= htmlspecialchars($_GET['c'] ?? '') ?>">
        <div class="filter-group">
            <label class="filter-label">Antal år</label>
            <select name="years" class="form-select" onchange="this.form.submit()">
                <?php foreach ([5, 7, 10, 15] as $y): ?>
                    <option value="<?= $y ?>" <?= $y == $numYears ? 'selected' : '' ?>>
                        Senaste <?= $y ?> år
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
        <div class="filter-info">
            <span class="badge"><?= count($yearsToShow) ?> år data</span>
            <span class="text-muted"><?= min($yearsToShow) ?> - <?= max($yearsToShow) ?></span>
        </div>
    </form>
</div>

<?php if (isset($error)): ?>
<div class="alert alert-warning">
    <i data-lucide="alert-triangle"></i>
    <div>
        <strong>Fel vid datahämtning</strong><br>
        <small><?= htmlspecialchars($error) ?></small>
    </div>
</div>
<?php elseif (!$hasData): ?>
<div class="alert alert-info">
    <i data-lucide="info"></i>
    <div>
        <strong>Välj minst ett varumärke</strong><br>
        Kryssa i varumärken i minst en grupp ovan och klicka på "Uppdatera jämförelse".
    </div>
</div>
<?php else: ?>

<!-- Legend -->
<div class="chart-legend-bar">
    <?php foreach ($activeGroups as $idx): ?>
    <div class="legend-item">
        <span class="legend-color" style="background: <?= $groupColors[$idx] ?>"></span>
        <span class="legend-label"><?= htmlspecialchars($groupLabels[$idx]) ?></span>
    </div>
    <?php endforeach; ?>
</div>

<!-- DELTAGARTRENDER -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><i data-lucide="users"></i> Deltagarutveckling</h2>
        <span class="badge badge-primary"><?= count($yearsToShow) ?> säsonger</span>
    </div>
    <div class="admin-card-body">
        <div class="chart-container" style="height: 350px;">
            <canvas id="participantChart"></canvas>
        </div>
    </div>
</div>

<!-- RETENTION & GROWTH -->
<div class="grid grid-2 grid-gap-lg">
    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="refresh-cw"></i> Retention Rate</h2>
        </div>
        <div class="admin-card-body">
            <div class="chart-container" style="height: 280px;">
                <canvas id="retentionChart"></canvas>
            </div>
            <p class="chart-description">Andel riders som återkom från föregående säsong</p>
        </div>
    </div>

    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="trending-up"></i> Tillväxt</h2>
        </div>
        <div class="admin-card-body">
            <div class="chart-container" style="height: 280px;">
                <canvas id="growthChart"></canvas>
            </div>
            <p class="chart-description">Årlig procentuell förändring i deltagarantal</p>
        </div>
    </div>
</div>

<!-- CROSS-PARTICIPATION & NYA RIDERS -->
<div class="grid grid-2 grid-gap-lg">
    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="git-branch"></i> Cross-Participation</h2>
        </div>
        <div class="admin-card-body">
            <div class="chart-container" style="height: 280px;">
                <canvas id="crossParticipationChart"></canvas>
            </div>
            <p class="chart-description">Andel riders som även deltar i ANDRA varumärken</p>
        </div>
    </div>

    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="user-plus"></i> Nya Riders (Rekrytering)</h2>
        </div>
        <div class="admin-card-body">
            <div class="chart-container" style="height: 280px;">
                <canvas id="newRidersChart"></canvas>
            </div>
            <p class="chart-description">Antal helt nya deltagare per år</p>
        </div>
    </div>
</div>

<!-- DEMOGRAPHICS -->
<div class="grid grid-2 grid-gap-lg">
    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="users"></i> Könsfördelning</h2>
        </div>
        <div class="admin-card-body">
            <div class="chart-container" style="height: 280px;">
                <canvas id="genderChart"></canvas>
            </div>
            <p class="chart-description">Andel kvinnliga deltagare över tid</p>
        </div>
    </div>

    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="calendar"></i> Genomsnittsålder</h2>
        </div>
        <div class="admin-card-body">
            <div class="chart-container" style="height: 280px;">
                <canvas id="ageChart"></canvas>
            </div>
            <p class="chart-description">Genomsnittsålder för aktiva deltagare per säsong</p>
        </div>
    </div>
</div>

<!-- SAMMANFATTNINGSTABELLER -->
<?php foreach ($activeGroups as $idx): ?>
<div class="admin-card">
    <div class="admin-card-header">
        <h2>
            <span class="legend-color-inline" style="background: <?= $groupColors[$idx] ?>"></span>
            <?= htmlspecialchars($groupLabels[$idx]) ?>
        </h2>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <div class="admin-table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Säsong</th>
                        <th class="text-right">Totalt</th>
                        <th class="text-right">Nya</th>
                        <th class="text-right">Återvändare</th>
                        <th class="text-right">Retention</th>
                        <th class="text-right">Tillväxt</th>
                        <th class="text-right">Cross-Part.</th>
                        <th class="text-right">Snittålder</th>
                        <th class="text-right">Kvinnor</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_reverse($groupTrends[$idx]) as $row): ?>
                    <tr>
                        <td><strong><?= $row['year'] ?></strong></td>
                        <td class="text-right"><?= number_format($row['total_riders']) ?></td>
                        <td class="text-right"><?= number_format($row['new_riders']) ?></td>
                        <td class="text-right"><?= number_format($row['retained_riders']) ?></td>
                        <td class="text-right">
                            <span class="badge <?= $row['retention_rate'] >= 60 ? 'badge-success' : ($row['retention_rate'] >= 40 ? 'badge-warning' : 'badge-danger') ?>">
                                <?= $row['retention_rate'] ?>%
                            </span>
                        </td>
                        <td class="text-right">
                            <span class="trend-indicator <?= $row['growth_rate'] >= 0 ? 'positive' : 'negative' ?>">
                                <?= $row['growth_rate'] >= 0 ? '+' : '' ?><?= $row['growth_rate'] ?>%
                            </span>
                        </td>
                        <td class="text-right"><?= $row['cross_participation'] ?>%</td>
                        <td class="text-right"><?= $row['average_age'] ?> år</td>
                        <td class="text-right"><?= $row['female_pct'] ?>%</td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endforeach; ?>

<?php endif; ?>

<style>
/* Brand Groups */
.brand-groups {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-lg);
    margin-bottom: var(--space-lg);
}

.brand-group {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
}

.group-header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
    padding-bottom: var(--space-sm);
    border-bottom: 1px solid var(--color-border);
}

.group-color {
    width: 16px;
    height: 16px;
    border-radius: var(--radius-sm);
    flex-shrink: 0;
}

.group-label {
    font-weight: var(--weight-semibold);
    flex-grow: 1;
}

.group-count {
    font-size: var(--text-sm);
    color: var(--color-text-muted);
}

.brand-checkboxes {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
    max-height: 250px;
    overflow-y: auto;
}

.brand-checkbox {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: background 0.15s;
}

.brand-checkbox:hover {
    background: var(--color-bg-hover);
}

.brand-checkbox.checked {
    background: var(--color-accent-light);
}

.brand-checkbox input[type="checkbox"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
}

.brand-name {
    font-size: var(--text-sm);
}

.form-actions {
    display: flex;
    gap: var(--space-md);
    padding-top: var(--space-lg);
    border-top: 1px solid var(--color-border);
}

/* Legend Bar */
.chart-legend-bar {
    display: flex;
    justify-content: center;
    gap: var(--space-xl);
    margin-bottom: var(--space-lg);
    padding: var(--space-md);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.chart-legend-bar .legend-item {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    font-weight: var(--weight-semibold);
    font-size: var(--text-base);
}

.chart-legend-bar .legend-color {
    width: 20px;
    height: 20px;
    border-radius: var(--radius-sm);
}

.legend-color-inline {
    display: inline-block;
    width: 16px;
    height: 16px;
    border-radius: var(--radius-sm);
    margin-right: var(--space-sm);
    vertical-align: middle;
}

/* Filter Bar */
.filter-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-lg);
    margin-bottom: var(--space-xl);
    padding: var(--space-md);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.filter-form {
    display: flex;
    gap: var(--space-lg);
    align-items: center;
}

.filter-group {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
}

.filter-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    font-weight: var(--weight-medium);
}

.filter-info {
    display: flex;
    gap: var(--space-sm);
    align-items: center;
}

/* Chart Container */
.chart-container {
    position: relative;
    width: 100%;
}

.chart-description {
    margin: var(--space-md) 0 0;
    font-size: var(--text-sm);
    color: var(--color-text-muted);
    text-align: center;
}

/* Grid */
.grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}

.grid-gap-lg {
    gap: var(--space-lg);
}

/* Trend Indicator */
.trend-indicator {
    font-weight: var(--weight-semibold);
}

.trend-indicator.positive {
    color: var(--color-success);
}

.trend-indicator.negative {
    color: var(--color-error);
}

/* Badge variants */
.badge-success {
    background: rgba(34, 197, 94, 0.15);
    color: var(--color-success);
}

.badge-warning {
    background: rgba(251, 191, 36, 0.15);
    color: var(--color-warning);
}

.badge-danger {
    background: rgba(239, 68, 68, 0.15);
    color: var(--color-error);
}

.badge-primary {
    background: var(--color-accent-light);
    color: var(--color-accent);
}

/* Text utilities */
.text-right {
    text-align: right;
}

.text-muted {
    color: var(--color-text-muted);
    font-size: var(--text-sm);
}

.mb-lg {
    margin-bottom: var(--space-lg);
}

.mb-md {
    margin-bottom: var(--space-md);
}

/* Responsive */
@media (max-width: 1099px) {
    .brand-groups {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 899px) {
    .filter-bar {
        flex-direction: column;
        align-items: stretch;
    }

    .filter-form {
        flex-direction: column;
        align-items: stretch;
    }

    .grid-2 {
        grid-template-columns: 1fr;
    }

    .chart-legend-bar {
        flex-direction: column;
        align-items: center;
        gap: var(--space-sm);
    }
}

@media (max-width: 767px) {
    .filter-bar,
    .card,
    .chart-legend-bar {
        margin-left: calc(-1 * var(--container-padding, 16px));
        margin-right: calc(-1 * var(--container-padding, 16px));
        border-radius: 0;
        border-left: none;
        border-right: none;
    }

    .admin-table {
        font-size: var(--text-xs);
    }

    .admin-table th,
    .admin-table td {
        padding: var(--space-xs);
    }

    .form-actions {
        flex-direction: column;
    }
}
</style>

<script>
// Checkbox handler
document.addEventListener('DOMContentLoaded', function() {
    const groups = document.querySelectorAll('.brand-group');

    groups.forEach(group => {
        const groupKey = group.dataset.group;
        const checkboxes = group.querySelectorAll('input[type="checkbox"]');
        const countSpan = group.querySelector('.group-count');
        const hiddenInput = document.getElementById('input' + groupKey.toUpperCase());

        function updateGroup() {
            const selected = [];
            checkboxes.forEach(cb => {
                const label = cb.closest('.brand-checkbox');
                if (cb.checked) {
                    selected.push(cb.value);
                    label.classList.add('checked');
                } else {
                    label.classList.remove('checked');
                }
            });
            countSpan.textContent = selected.length + ' valda';
            hiddenInput.value = selected.join(',');
        }

        checkboxes.forEach(cb => {
            cb.addEventListener('change', updateGroup);
        });
    });
});
</script>

<?php if ($hasData): ?>
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Data från PHP
    const groupTrends = <?= json_encode($groupTrends) ?>;
    const groupLabels = <?= json_encode($groupLabels) ?>;
    const groupColors = <?= json_encode($groupColors) ?>;
    const activeGroups = <?= json_encode($activeGroups) ?>;

    // Hämta years från första aktiva gruppen
    const firstGroup = activeGroups[0];
    const years = groupTrends[firstGroup] ? groupTrends[firstGroup].map(d => d.year) : [];

    // Gemensamma chart-options
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            intersect: false,
            mode: 'index'
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: 'rgba(11, 19, 30, 0.9)',
                titleColor: '#f8f2f0',
                bodyColor: '#c7cfdd',
                borderColor: 'rgba(55, 212, 214, 0.3)',
                borderWidth: 1,
                padding: 12,
                displayColors: true,
                callbacks: {
                    title: function(items) {
                        return 'Säsong ' + items[0].label;
                    }
                }
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(55, 212, 214, 0.1)'
                },
                ticks: {
                    color: '#868fa2'
                }
            },
            y: {
                grid: {
                    color: 'rgba(55, 212, 214, 0.1)'
                },
                ticks: {
                    color: '#868fa2'
                }
            }
        }
    };

    // Skapa datasets för alla aktiva grupper
    function createDatasets(dataKey, suffix = '') {
        const datasets = [];
        activeGroups.forEach((idx) => {
            const data = groupTrends[idx];
            datasets.push({
                label: groupLabels[idx] + suffix,
                data: data.map(d => d[dataKey]),
                borderColor: groupColors[idx],
                backgroundColor: groupColors[idx] + '20',
                fill: false,
                tension: 0.3,
                borderWidth: 3,
                pointRadius: 4,
                pointHoverRadius: 6
            });
        });
        return datasets;
    }

    // 1. DELTAGARCHART
    new Chart(document.getElementById('participantChart'), {
        type: 'line',
        data: {
            labels: years,
            datasets: createDatasets('total_riders')
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toLocaleString() + ' riders';
                        }
                    }
                }
            }
        }
    });

    // 2. RETENTION CHART
    new Chart(document.getElementById('retentionChart'), {
        type: 'line',
        data: {
            labels: years,
            datasets: createDatasets('retention_rate')
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    min: 0,
                    max: 100,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: value => value + '%'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + '%';
                        }
                    }
                }
            }
        }
    });

    // 3. GROWTH CHART
    const growthDatasets = [];
    activeGroups.forEach((idx) => {
        const data = groupTrends[idx];
        growthDatasets.push({
            label: groupLabels[idx],
            data: data.map(d => d.growth_rate),
            backgroundColor: groupColors[idx] + '80',
            borderColor: groupColors[idx],
            borderWidth: 2,
            borderRadius: 4
        });
    });

    new Chart(document.getElementById('growthChart'), {
        type: 'bar',
        data: {
            labels: years,
            datasets: growthDatasets
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: value => value + '%'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            const val = context.parsed.y;
                            return context.dataset.label + ': ' + (val >= 0 ? '+' : '') + val + '%';
                        }
                    }
                }
            }
        }
    });

    // 4. CROSS-PARTICIPATION CHART
    new Chart(document.getElementById('crossParticipationChart'), {
        type: 'line',
        data: {
            labels: years,
            datasets: createDatasets('cross_participation')
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    min: 0,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: value => value + '%'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + '%';
                        }
                    }
                }
            }
        }
    });

    // 5. NEW RIDERS CHART
    new Chart(document.getElementById('newRidersChart'), {
        type: 'line',
        data: {
            labels: years,
            datasets: createDatasets('new_riders')
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toLocaleString() + ' nya';
                        }
                    }
                }
            }
        }
    });

    // 6. GENDER CHART
    new Chart(document.getElementById('genderChart'), {
        type: 'line',
        data: {
            labels: years,
            datasets: createDatasets('female_pct')
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    min: 0,
                    max: 50,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: value => value + '%'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + '% kvinnor';
                        }
                    }
                }
            }
        }
    });

    // 7. AGE CHART
    new Chart(document.getElementById('ageChart'), {
        type: 'line',
        data: {
            labels: years,
            datasets: createDatasets('average_age')
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: value => value + ' år'
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        ...commonOptions.plugins.tooltip.callbacks,
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(1) + ' år';
                        }
                    }
                }
            }
        }
    });
});
</script>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
