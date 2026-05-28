<?php
/**
 * Analytics Season Report
 *
 * 2-3 sidor A4 med säsongsöversikt, journey-data och insikter.
 * Optimerad för utskrift/PDF.
 *
 * @package TheHUB Admin
 */
require_once __DIR__ . '/../config.php';
require_admin();

require_once __DIR__ . '/../analytics/includes/KPICalculator.php';
require_once __DIR__ . '/../analytics/includes/ReportGenerator.php';

global $pdo;

// Välj år
$currentYear = (int)date('Y');
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : $currentYear - 1;

// Generera rapport
$generator = new ReportGenerator($pdo);
$report = $generator->generateSeasonReport($selectedYear);

// Hämta tillgängliga år
$years = [];
try {
    $stmt = $pdo->query("SELECT DISTINCT YEAR(date) as yr FROM events WHERE date IS NOT NULL ORDER BY yr DESC");
    $years = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {}

$page_title = $report['meta']['title'];
$hideNavigation = isset($_GET['print']);

if (!$hideNavigation) {
    include __DIR__ . '/components/unified-layout.php';
}
?>

<?php if ($hideNavigation): ?>
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <title><?= htmlspecialchars($page_title) ?></title>
    <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
<?php endif; ?>

<style>
/* A4 Print Styles */
@media print {
    body { margin: 0; padding: 0; }
    .no-print { display: none !important; }
    .report-page { page-break-after: always; }
    .report-page:last-child { page-break-after: avoid; }
}

.report-container {
    max-width: 210mm;
    margin: 0 auto;
    font-family: 'Manrope', sans-serif;
    color: #1a1a1a;
    background: white;
}

.report-page {
    padding: 15mm;
    min-height: 277mm;
    box-sizing: border-box;
    background: white;
    margin-bottom: var(--space-lg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

@media print {
    .report-page {
        border: none;
        margin: 0;
        border-radius: 0;
    }
}

.report-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 3px solid #37d4d6;
    padding-bottom: 10mm;
    margin-bottom: 10mm;
}

.report-title {
    font-family: 'Oswald', sans-serif;
    font-size: 28pt;
    font-weight: 600;
    color: #0b131e;
    margin: 0;
}

.report-subtitle {
    font-size: 11pt;
    color: #666;
    margin-top: 2mm;
}

.report-logo {
    font-family: 'Oswald', sans-serif;
    font-size: 14pt;
    color: #37d4d6;
}

/* KPI Grid */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 5mm;
    margin-bottom: 10mm;
}

.kpi-card {
    background: #f8f9fa;
    border-radius: 3mm;
    padding: 5mm;
    text-align: center;
}

.kpi-value {
    font-family: 'Oswald', sans-serif;
    font-size: 24pt;
    font-weight: 600;
    color: #0b131e;
}

.kpi-label {
    font-size: 9pt;
    color: #666;
    margin-top: 1mm;
}

.kpi-change {
    font-size: 9pt;
    margin-top: 2mm;
}

.kpi-change.positive { color: #10b981; }
.kpi-change.negative { color: #ef4444; }

/* Section headers */
.section-title {
    font-family: 'Oswald', sans-serif;
    font-size: 14pt;
    font-weight: 500;
    color: #0b131e;
    border-bottom: 1px solid #ddd;
    padding-bottom: 2mm;
    margin: 8mm 0 5mm 0;
}

/* Tables */
.report-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 9pt;
    margin-bottom: 5mm;
}

.report-table th {
    background: #f8f9fa;
    padding: 2mm 3mm;
    text-align: left;
    font-weight: 600;
    border-bottom: 1px solid #ddd;
}

.report-table td {
    padding: 2mm 3mm;
    border-bottom: 1px solid #eee;
}

.report-table tr:last-child td {
    border-bottom: none;
}

/* Funnel */
.funnel-container {
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    height: 50mm;
    margin: 5mm 0;
}

.funnel-bar {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 20%;
}

.funnel-fill {
    background: linear-gradient(180deg, #37d4d6 0%, #2bc4c6 100%);
    width: 100%;
    border-radius: 2mm 2mm 0 0;
    min-height: 5mm;
}

.funnel-label {
    font-size: 8pt;
    color: #666;
    margin-top: 2mm;
    text-align: center;
}

.funnel-value {
    font-family: 'Oswald', sans-serif;
    font-size: 12pt;
    font-weight: 500;
    margin-top: 1mm;
}

/* Recommendations */
.recommendation {
    background: #f8f9fa;
    border-left: 3px solid #37d4d6;
    padding: 3mm 4mm;
    margin-bottom: 3mm;
    font-size: 9pt;
}

.recommendation.high { border-color: #ef4444; }
.recommendation.medium { border-color: #fbbf24; }

.recommendation-title {
    font-weight: 600;
    margin-bottom: 1mm;
}

.recommendation-action {
    color: #666;
    font-style: italic;
}

/* Page footer */
.page-footer {
    position: absolute;
    bottom: 10mm;
    left: 15mm;
    right: 15mm;
    font-size: 8pt;
    color: #999;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #eee;
    padding-top: 2mm;
}

/* Controls */
.report-controls {
    display: flex;
    gap: var(--space-md);
    align-items: center;
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
}

@media print {
    .report-controls { display: none; }
}
</style>

<?php if (!$hideNavigation): ?>
<div class="report-controls no-print">
    <form method="get" style="display: flex; gap: var(--space-sm); align-items: center;">
        <label class="form-label" style="margin: 0;">År:</label>
        <select name="year" class="form-select" onchange="this.form.submit()" style="width: auto;">
            <?php foreach ($years as $yr): ?>
            <option value="<?= $yr ?>" <?= $yr == $selectedYear ? 'selected' : '' ?>><?= $yr ?></option>
            <?php endforeach; ?>
        </select>
    </form>
    <a href="?year=<?= $selectedYear ?>&print=1" target="_blank" class="btn-admin btn-admin-primary">
        <i data-lucide="printer"></i> Skriv ut / PDF
    </a>
</div>
<?php endif; ?>

<div class="report-container">

    <!-- SIDA 1: Säsongsöversikt -->
    <div class="report-page">
        <div class="report-header">
            <div>
                <h1 class="report-title"><?= htmlspecialchars($report['meta']['title']) ?></h1>
                <div class="report-subtitle">Genererad: <?= $report['meta']['generated_at'] ?></div>
            </div>
            <div class="report-logo">GravitySeries</div>
        </div>

        <div class="kpi-grid">
            <?php foreach ($report['overview']['kpis'] as $key => $kpi): ?>
            <div class="kpi-card">
                <div class="kpi-value"><?= number_format($kpi['value']) ?><?= $kpi['suffix'] ?? '' ?></div>
                <div class="kpi-label"><?= htmlspecialchars($kpi['label']) ?></div>
                <div class="kpi-change <?= $kpi['change'] >= 0 ? 'positive' : 'negative' ?>">
                    <?= $kpi['change'] >= 0 ? '+' : '' ?><?= $kpi['change'] ?>% vs <?= $selectedYear - 1 ?>
                </div>
            </div>
            <?php endforeach; ?>
        </div>

        <h2 class="section-title">Största event <?= $selectedYear ?></h2>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Event</th>
                    <th>Datum</th>
                    <th>Plats</th>
                    <th style="text-align: right;">Deltagare</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($report['overview']['top_events'] as $event): ?>
                <tr>
                    <td><?= htmlspecialchars($event['name']) ?></td>
                    <td><?= date('Y-m-d', strtotime($event['date'])) ?></td>
                    <td><?= htmlspecialchars($event['location'] ?? '-') ?></td>
                    <td style="text-align: right; font-weight: 600;"><?= number_format($event['participants']) ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>

        <h2 class="section-title">5-års utveckling</h2>
        <table class="report-table">
            <thead>
                <tr>
                    <th>År</th>
                    <th style="text-align: right;">Deltagare</th>
                    <th style="text-align: right;">Tillväxt</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach (array_slice($report['overview']['trend'], 0, 5) as $trend): ?>
                <tr>
                    <td><?= $trend['year'] ?></td>
                    <td style="text-align: right;"><?= number_format($trend['total_riders']) ?></td>
                    <td style="text-align: right;" class="<?= ($trend['growth_rate'] ?? 0) >= 0 ? 'positive' : 'negative' ?>">
                        <?= ($trend['growth_rate'] ?? 0) >= 0 ? '+' : '' ?><?= round($trend['growth_rate'] ?? 0, 1) ?>%
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <!-- SIDA 2: Rider Journey -->
    <div class="report-page">
        <div class="report-header">
            <div>
                <h1 class="report-title">Rider Journey</h1>
                <div class="report-subtitle">Kohort <?= $report['journey']['cohort_year'] ?> - Hur nya deltagare utvecklas över tid</div>
            </div>
        </div>

        <h2 class="section-title">Kohort-funnel: Retention över tid</h2>
        <?php if (!empty($report['journey']['funnel'])): ?>
        <div class="funnel-container">
            <?php
            $maxActive = max(array_column($report['journey']['funnel'], 'active')) ?: 1;
            foreach ($report['journey']['funnel'] as $step):
                $height = ($step['active'] / $maxActive) * 100;
            ?>
            <div class="funnel-bar">
                <div class="funnel-fill" style="height: <?= max($height, 10) ?>%;"></div>
                <div class="funnel-label">År <?= $step['year_offset'] ?> (<?= $step['calendar_year'] ?>)</div>
                <div class="funnel-value"><?= $step['retention_pct'] ?>%</div>
            </div>
            <?php endforeach; ?>
        </div>
        <?php else: ?>
        <p style="color: #666; font-style: italic;">Kohort-data saknas för detta år.</p>
        <?php endif; ?>

        <?php if (!empty($report['journey']['retention_by_starts'])): ?>
        <h2 class="section-title">Retention baserat på antal starter första året</h2>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Starter år 1</th>
                    <th style="text-align: right;">Antal</th>
                    <th style="text-align: right;">Kom tillbaka år 2</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($report['journey']['retention_by_starts'] as $row): ?>
                <tr>
                    <td><?= $row['start_bucket'] ?? $row['starts'] ?? '-' ?></td>
                    <td style="text-align: right;"><?= number_format($row['count'] ?? $row['riders'] ?? 0) ?></td>
                    <td style="text-align: right;"><?= round(($row['retention_rate'] ?? $row['returned_pct'] ?? 0) * 100, 1) ?>%</td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        <?php endif; ?>

        <?php if (!empty($report['journey']['top_clubs_retention'])): ?>
        <h2 class="section-title">Klubbar med bäst retention</h2>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Klubb</th>
                    <th style="text-align: right;">Retention</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($report['journey']['top_clubs_retention'] as $club): ?>
                <tr>
                    <td><?= htmlspecialchars($club['name']) ?></td>
                    <td style="text-align: right; font-weight: 600;"><?= $club['retention_pct'] ?>%</td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        <?php endif; ?>
    </div>

    <!-- SIDA 3: Insikter -->
    <div class="report-page">
        <div class="report-header">
            <div>
                <h1 class="report-title">Insikter & Rekommendationer</h1>
                <div class="report-subtitle">Baserat på <?= $selectedYear ?> års data</div>
            </div>
        </div>

        <?php if (!empty($report['insights']['rookie_events'])): ?>
        <h2 class="section-title">Event som lockar flest nya deltagare</h2>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Event</th>
                    <th style="text-align: right;">Rookies</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($report['insights']['rookie_events'] as $event): ?>
                <tr>
                    <td><?= htmlspecialchars($event['event_name'] ?? $event['name'] ?? '-') ?></td>
                    <td style="text-align: right; font-weight: 600;"><?= number_format($event['rookie_count'] ?? $event['rookies'] ?? 0) ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        <?php endif; ?>

        <?php if (!empty($report['insights']['rookie_clubs'])): ?>
        <h2 class="section-title">Klubbar som rekryterar flest nya</h2>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Klubb</th>
                    <th style="text-align: right;">Nya medlemmar</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach (array_slice($report['insights']['rookie_clubs'], 0, 5) as $club): ?>
                <tr>
                    <td><?= htmlspecialchars($club['club_name'] ?? $club['name'] ?? '-') ?></td>
                    <td style="text-align: right; font-weight: 600;"><?= number_format($club['rookie_count'] ?? $club['rookies'] ?? 0) ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        <?php endif; ?>

        <h2 class="section-title">Rekommendationer</h2>
        <?php foreach ($report['insights']['recommendations'] as $rec): ?>
        <div class="recommendation <?= $rec['priority'] ?>">
            <div class="recommendation-title"><?= htmlspecialchars($rec['area']) ?>: <?= htmlspecialchars($rec['insight']) ?></div>
            <div class="recommendation-action"><?= htmlspecialchars($rec['action']) ?></div>
        </div>
        <?php endforeach; ?>
    </div>

</div>

<?php if ($hideNavigation): ?>
<script>window.print();</script>
</body>
</html>
<?php else: ?>
<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
<?php endif; ?>
