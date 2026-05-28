<?php
/**
 * Analytics Export Center
 *
 * Centraliserad exporthantering for alla analytics-rapporter.
 * Visar exporthistorik, rate limits, och genererar nya exporter.
 *
 * @package TheHUB Admin
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
requireAnalyticsAccess();

require_once __DIR__ . '/../analytics/includes/AnalyticsEngine.php';
require_once __DIR__ . '/../analytics/includes/ExportLogger.php';
require_once __DIR__ . '/../analytics/includes/KPICalculator.php';
require_once __DIR__ . '/../analytics/includes/AnalyticsConfig.php';
require_once __DIR__ . '/../analytics/includes/SVGChartRenderer.php';
require_once __DIR__ . '/../analytics/includes/PdfExportBuilder.php';

global $pdo;

$engine = new AnalyticsEngine($pdo);
$logger = new ExportLogger($pdo);
$kpi = new KPICalculator($pdo);

// Hamta tillgangliga ar
$years = [];
try {
    $years = $pdo->query("
        SELECT DISTINCT season_year
        FROM rider_yearly_stats
        ORDER BY season_year DESC
    ")->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {
    // Table might not exist yet
}

$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : ($years[0] ?? date('Y'));

// Hamta export statistik
$exportStats = ['total_exports' => 0, 'total_rows' => 0, 'reproducibility_rate' => 0];
$myExports = [];
$rateLimitStatus = ['can_export' => true, 'hourly' => ['current' => 0, 'limit' => 100], 'daily' => ['current' => 0, 'limit' => 1000]];
$latestSnapshot = null;
$pngSupport = ['can_convert' => false];
$pdfStatus = ['available' => false, 'version' => ''];
$recalcStatus = ['pending' => 0];
$rateLimitSource = 'config';

try {
    $exportStats = $logger->getExportStats('month');
    $userId = $_SESSION['user_id'] ?? 1;
    $myExports = $logger->getUserExports($userId, 20);
    $userRole = $_SESSION['role'] ?? null;
    $rateLimitStatus = $logger->getRateLimitStatus($userId, null, $userRole);
    $latestSnapshot = $engine->getLatestSnapshot();
    $pngSupport = SVGChartRenderer::getPngSupportInfo();
    $pdfStatus = PdfExportBuilder::getPdfEngineStatus();
    $recalcStatus = $engine->getRecalcQueueStatus();
    $rateLimitSource = $logger->getRateLimitSource();
} catch (Exception $e) {
    // Components might not be fully set up
}

// Page config
$page_title = 'Export Center';
$breadcrumbs = [
    ['label' => 'Dashboard', 'url' => '/admin/dashboard.php'],
    ['label' => 'Analytics', 'url' => '/admin/analytics-dashboard.php'],
    ['label' => 'Export Center']
];

$page_actions = '';

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Status Overview -->
<div class="grid grid-cols-4 gap-md mb-lg">
        <div class="stat-card">
            <div class="stat-value"><?= number_format($exportStats['total_exports'] ?? 0) ?></div>
            <div class="stat-label">Exporter (30 dagar)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value"><?= number_format($exportStats['total_rows'] ?? 0) ?></div>
            <div class="stat-label">Rader exporterade</div>
        </div>
        <div class="stat-card">
            <div class="stat-value"><?= ($exportStats['reproducibility_rate'] ?? 0) ?>%</div>
            <div class="stat-label">Reproducerbara</div>
        </div>
        <div class="stat-card">
            <div class="stat-value"><?= $latestSnapshot ? '#' . $latestSnapshot['id'] : '-' ?></div>
            <div class="stat-label">Aktiv Snapshot</div>
        </div>
    </div>

    <!-- Rate Limit Warning -->
    <?php if (!$rateLimitStatus['can_export']): ?>
    <div class="alert alert-warning mb-lg">
        <i data-lucide="alert-triangle"></i>
        <strong>Rate limit nadd!</strong> Du har exporterat for mycket data. Vanligen innan du kan exportera igen.
        <br>Timme: <?= $rateLimitStatus['hourly']['current'] ?>/<?= $rateLimitStatus['hourly']['limit'] ?>,
        Dag: <?= $rateLimitStatus['daily']['current'] ?>/<?= $rateLimitStatus['daily']['limit'] ?>
    </div>
    <?php endif; ?>

    <div class="grid grid-cols-2 gap-lg">
        <!-- Left Column: Export Types -->
        <div>
            <!-- Quick Exports -->
            <div class="card mb-lg">
                <div class="card-header">
                    <h3><i data-lucide="zap"></i> Snabbexporter</h3>
                </div>
                <div class="card-body">
                    <form method="get" class="filter-row mb-md">
                        <div class="form-group">
                            <label class="form-label">Sasong</label>
                            <select name="year" class="form-select" onchange="this.form.submit()">
                                <?php foreach ($years as $y): ?>
                                    <option value="<?= $y ?>" <?= $y == $selectedYear ? 'selected' : '' ?>><?= $y ?></option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                    </form>

                    <div class="export-buttons">
                        <button type="button" class="btn btn-secondary" onclick="exportData('retention')" <?= !$rateLimitStatus['can_export'] ? 'disabled' : '' ?>>
                            <i data-lucide="repeat"></i> Retention Report
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="exportData('at_risk')" <?= !$rateLimitStatus['can_export'] ? 'disabled' : '' ?>>
                            <i data-lucide="alert-circle"></i> At-Risk Riders
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="exportData('cohort')" <?= !$rateLimitStatus['can_export'] ? 'disabled' : '' ?>>
                            <i data-lucide="users"></i> Cohort Analysis
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="exportData('winback')" <?= !$rateLimitStatus['can_export'] ? 'disabled' : '' ?>>
                            <i data-lucide="user-plus"></i> Winback Candidates
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="exportData('club_stats')" <?= !$rateLimitStatus['can_export'] ? 'disabled' : '' ?>>
                            <i data-lucide="building"></i> Club Statistics
                        </button>
                    </div>
                </div>
            </div>

            <!-- PDF Reports -->
            <div class="card mb-lg">
                <div class="card-header">
                    <h3><i data-lucide="file-text"></i> PDF-rapporter</h3>
                </div>
                <div class="card-body">
                    <?php if (!$pdfStatus['available']): ?>
                    <div class="alert alert-danger mb-md">
                        <i data-lucide="alert-octagon"></i>
                        <strong>PDF ENGINE MISSING (CRITICAL)</strong><br>
                        TCPDF ar obligatorisk for PDF-export i v3.0.2. Installera via:<br>
                        <code>composer require tecnickcom/tcpdf</code>
                    </div>
                    <?php else: ?>
                    <p class="text-muted mb-md">
                        PDF-rapporter inkluderar alltid "Definitions & Provenance" box for fullstandig reproducerbarhet.
                        <br><small>Motor: TCPDF <?= $pdfStatus['version'] ?></small>
                    </p>
                    <?php endif; ?>
                    <div class="export-buttons">
                        <button type="button" class="btn btn-primary" onclick="generatePdf('season_summary')"
                                <?= (!$rateLimitStatus['can_export'] || !$pdfStatus['available']) ? 'disabled' : '' ?>>
                            <i data-lucide="file-text"></i> Sasongsammanfattning
                        </button>
                        <button type="button" class="btn btn-primary" onclick="generatePdf('retention_report')"
                                <?= (!$rateLimitStatus['can_export'] || !$pdfStatus['available']) ? 'disabled' : '' ?>>
                            <i data-lucide="trending-up"></i> Retentionsrapport
                        </button>
                    </div>
                </div>
            </div>

            <!-- System Status -->
            <div class="card">
                <div class="card-header">
                    <h3><i data-lucide="cpu"></i> Systemstatus</h3>
                </div>
                <div class="card-body">
                    <table class="table table-compact">
                        <tr>
                            <td>Platform Version</td>
                            <td><span class="badge badge-success"><?= AnalyticsConfig::PLATFORM_VERSION ?></span></td>
                        </tr>
                        <tr>
                            <td>Calculation Version</td>
                            <td><?= AnalyticsConfig::CALCULATION_VERSION ?></td>
                        </tr>
                        <tr>
                            <td><strong>PDF ENGINE</strong></td>
                            <td>
                                <?php if ($pdfStatus['available']): ?>
                                    <span class="badge badge-success">OK</span>
                                    <small class="text-muted">(TCPDF <?= $pdfStatus['version'] ?>)</small>
                                <?php else: ?>
                                    <span class="badge badge-danger">MISSING (CRITICAL)</span>
                                    <br><small class="text-warning">PDF-export blockerad! Installera TCPDF.</small>
                                <?php endif; ?>
                            </td>
                        </tr>
                        <tr>
                            <td>PNG Export</td>
                            <td>
                                <?php if ($pngSupport['can_convert']): ?>
                                    <span class="badge badge-success">Tillganglig</span>
                                <?php else: ?>
                                    <span class="badge badge-warning">SVG Fallback</span>
                                <?php endif; ?>
                            </td>
                        </tr>
                        <tr>
                            <td>Rate Limit Source</td>
                            <td>
                                <?php if ($rateLimitSource === 'database'): ?>
                                    <span class="badge badge-success">Database</span>
                                <?php else: ?>
                                    <span class="badge badge-warning">Config (fallback)</span>
                                <?php endif; ?>
                            </td>
                        </tr>
                        <tr>
                            <td>Recalc Queue</td>
                            <td>
                                <?php if ($recalcStatus['pending'] > 0): ?>
                                    <span class="badge badge-warning"><?= $recalcStatus['pending'] ?> pending</span>
                                <?php else: ?>
                                    <span class="badge badge-success">Tom</span>
                                <?php endif; ?>
                            </td>
                        </tr>
                        <tr>
                            <td>Senaste Snapshot</td>
                            <td>
                                <?php if ($latestSnapshot): ?>
                                    #<?= $latestSnapshot['id'] ?> (<?= date('Y-m-d H:i', strtotime($latestSnapshot['created_at'])) ?>)
                                <?php else: ?>
                                    <span class="text-muted">Ingen</span>
                                <?php endif; ?>
                            </td>
                        </tr>
                    </table>

                    <button type="button" class="btn btn-ghost mt-md" onclick="createSnapshot()">
                        <i data-lucide="camera"></i> Skapa ny Snapshot
                    </button>
                </div>
            </div>
        </div>

        <!-- Right Column: Export History -->
        <div>
            <div class="card">
                <div class="card-header">
                    <h3><i data-lucide="history"></i> Mina exporter</h3>
                </div>
                <div class="card-body">
                    <?php if (empty($myExports)): ?>
                        <p class="text-muted">Inga exporter annu.</p>
                    <?php else: ?>
                        <div class="table-responsive">
                            <table class="table table-compact">
                                <thead>
                                    <tr>
                                        <th>Typ</th>
                                        <th>Datum</th>
                                        <th>Rader</th>
                                        <th>Snapshot</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($myExports as $export): ?>
                                    <tr>
                                        <td>
                                            <span class="badge badge-secondary"><?= htmlspecialchars($export['export_type']) ?></span>
                                            <?php if ($export['contains_pii']): ?>
                                                <i data-lucide="shield-alert" class="text-warning" title="Innehaller PII"></i>
                                            <?php endif; ?>
                                        </td>
                                        <td><?= date('Y-m-d H:i', strtotime($export['exported_at'])) ?></td>
                                        <td><?= number_format($export['row_count']) ?></td>
                                        <td>
                                            <?php if ($export['snapshot_id']): ?>
                                                <span class="badge badge-success">#<?= $export['snapshot_id'] ?></span>
                                            <?php else: ?>
                                                <span class="badge badge-warning">-</span>
                                            <?php endif; ?>
                                        </td>
                                        <td>
                                            <button class="btn btn-ghost btn-sm" onclick="viewManifest(<?= $export['id'] ?>)" title="Visa manifest">
                                                <i data-lucide="file-search"></i>
                                            </button>
                                        </td>
                                    </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                    <?php endif; ?>
                </div>
            </div>

            <!-- Rate Limits -->
            <div class="card mt-lg">
                <div class="card-header">
                    <h3><i data-lucide="gauge"></i> Rate Limits</h3>
                </div>
                <div class="card-body">
                    <div class="rate-limit-bar">
                        <label>Timme</label>
                        <div class="progress-bar-container">
                            <div class="progress-bar <?= $rateLimitStatus['hourly']['current'] >= $rateLimitStatus['hourly']['limit'] ? 'danger' : 'success' ?>"
                                 style="width: <?= min(100, ($rateLimitStatus['hourly']['current'] / $rateLimitStatus['hourly']['limit']) * 100) ?>%"></div>
                        </div>
                        <span><?= $rateLimitStatus['hourly']['current'] ?>/<?= $rateLimitStatus['hourly']['limit'] ?></span>
                    </div>
                    <div class="rate-limit-bar mt-md">
                        <label>Dag</label>
                        <div class="progress-bar-container">
                            <div class="progress-bar <?= $rateLimitStatus['daily']['current'] >= $rateLimitStatus['daily']['limit'] ? 'danger' : 'success' ?>"
                                 style="width: <?= min(100, ($rateLimitStatus['daily']['current'] / $rateLimitStatus['daily']['limit']) * 100) ?>%"></div>
                        </div>
                        <span><?= $rateLimitStatus['daily']['current'] ?>/<?= $rateLimitStatus['daily']['limit'] ?></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Manifest Modal -->
<div id="manifestModal" class="modal" style="display: none;">
    <div class="modal-content">
        <div class="modal-header">
            <h3>Export Manifest</h3>
            <button class="btn btn-ghost" onclick="closeModal()">&times;</button>
        </div>
        <div class="modal-body">
            <pre id="manifestContent"></pre>
        </div>
    </div>
</div>

<style>
.grid {
    display: grid;
}
.grid-cols-2 {
    grid-template-columns: repeat(2, 1fr);
}
.grid-cols-4 {
    grid-template-columns: repeat(4, 1fr);
}
.gap-md {
    gap: var(--space-md);
}
.gap-lg {
    gap: var(--space-lg);
}

.stat-card {
    background: var(--color-bg-surface);
    padding: var(--space-md);
    border-radius: var(--radius-md);
    text-align: center;
    border: 1px solid var(--color-border);
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

.export-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-sm);
}
.export-buttons .btn {
    flex: 1 1 calc(50% - var(--space-sm));
    min-width: 140px;
}

.progress-bar-container {
    flex: 1;
    height: 8px;
    background: var(--color-bg-surface);
    border-radius: var(--radius-full);
    overflow: hidden;
    margin: 0 var(--space-sm);
}
.progress-bar {
    height: 100%;
    border-radius: var(--radius-full);
    transition: width 0.3s ease;
}
.progress-bar.success { background: var(--color-success); }
.progress-bar.danger { background: var(--color-error); }

.rate-limit-bar {
    display: flex;
    align-items: center;
}
.rate-limit-bar label {
    width: 60px;
    color: var(--color-text-secondary);
}
.rate-limit-bar span {
    width: 80px;
    text-align: right;
    font-size: 0.85rem;
    color: var(--color-text-muted);
}

.table-compact td, .table-compact th {
    padding: var(--space-xs) var(--space-sm);
}

.modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}
.modal-content {
    background: var(--color-bg-card);
    border-radius: var(--radius-lg);
    max-width: 600px;
    width: 90%;
    max-height: 80vh;
    overflow: hidden;
    border: 1px solid var(--color-border);
}
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-md);
    border-bottom: 1px solid var(--color-border);
}
.modal-body {
    padding: var(--space-md);
    overflow-y: auto;
    max-height: calc(80vh - 60px);
}
.modal-body pre {
    white-space: pre-wrap;
    font-size: 0.85rem;
    color: var(--color-text-secondary);
}

@media (max-width: 767px) {
    .grid-cols-2, .grid-cols-4 {
        grid-template-columns: 1fr;
    }
    .export-buttons .btn {
        flex: 1 1 100%;
    }
    .card {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
    }
    .stat-card {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
    }
    .alert {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
    }
}
</style>

<script>
const selectedYear = <?= $selectedYear ?>;

async function exportData(type) {
    try {
        const response = await fetch(`/api/analytics/export.php?type=${type}&year=${selectedYear}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${type}_${selectedYear}.csv`;
            a.click();
            window.URL.revokeObjectURL(url);
            location.reload(); // Refresh to show new export in history
        } else {
            const error = await response.json();
            alert('Exportfel: ' + (error.error || 'Okant fel'));
        }
    } catch (err) {
        alert('Exportfel: ' + err.message);
    }
}

async function generatePdf(type) {
    alert('PDF-generering kommer snart! Typ: ' + type);
    // TODO: Implement PDF generation endpoint
}

async function createSnapshot() {
    try {
        const response = await fetch('/api/analytics/create-snapshot.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const result = await response.json();
        if (result.success) {
            alert('Snapshot #' + result.snapshot_id + ' skapad!');
            location.reload();
        } else {
            alert('Fel: ' + (result.error || 'Okant fel'));
        }
    } catch (err) {
        alert('Fel vid skapande av snapshot: ' + err.message);
    }
}

async function viewManifest(exportId) {
    try {
        const response = await fetch(`/api/analytics/get-manifest.php?id=${exportId}`);
        const result = await response.json();

        if (result.success) {
            document.getElementById('manifestContent').textContent = JSON.stringify(result.manifest, null, 2);
            document.getElementById('manifestModal').style.display = 'flex';
        } else {
            alert('Kunde inte hamta manifest');
        }
    } catch (err) {
        alert('Fel: ' + err.message);
    }
}

function closeModal() {
    document.getElementById('manifestModal').style.display = 'none';
}

// Close modal on outside click
document.getElementById('manifestModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeModal();
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
