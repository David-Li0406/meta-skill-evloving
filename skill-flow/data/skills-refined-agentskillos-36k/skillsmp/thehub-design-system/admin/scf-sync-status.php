<?php
/**
 * SCF License Sync Status
 *
 * Dashboard for monitoring SCF License Portal integration
 * Shows sync statistics, recent operations, and license verification status.
 *
 * @package TheHUB Admin
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
require_once __DIR__ . '/../includes/SCFLicenseService.php';

// Get API key from environment
$apiKey = env('SCF_API_KEY', '');
$scfEnabled = !empty($apiKey);

// Initialize service if API key is available
$scfService = null;
$stats = [];
$recentSyncs = [];

if ($scfEnabled) {
    $scfService = new SCFLicenseService($apiKey, $db);
    $currentYear = (int)date('Y');
    $stats = $scfService->getSyncStats($currentYear);
    $recentSyncs = $scfService->getRecentSyncs(10);
}

// Get general rider statistics
// license_number contains either:
// - Real UCI ID: 11 digits like 10012345678 (NOT starting with "SWE")
// - Generated SWE-ID: like SWE2510001 (for riders without real UCI ID)
$riderStats = [
    'total_riders' => (int)$db->getValue("SELECT COUNT(*) FROM riders"),
    'with_uci_id' => (int)$db->getValue("SELECT COUNT(*) FROM riders WHERE license_number IS NOT NULL AND license_number != '' AND license_number NOT LIKE 'SWE%'"),
    'without_uci_id' => (int)$db->getValue("SELECT COUNT(*) FROM riders WHERE license_number IS NULL OR license_number = '' OR license_number LIKE 'SWE%'"),
    'verified_this_year' => (int)$db->getValue("SELECT COUNT(*) FROM riders WHERE scf_license_year = ?", [(int)date('Y')]),
    'pending_matches' => (int)$db->getValue("SELECT COUNT(*) FROM scf_match_candidates WHERE status = 'pending'")
];

// Handle manual sync trigger
$message = '';
$messageType = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    $csrfToken = $_POST['csrf_token'] ?? '';
    if (!verify_csrf_token($csrfToken)) {
        $message = 'CSRF-validering misslyckades.';
        $messageType = 'danger';
    } else {
        switch ($_POST['action']) {
            case 'trigger_sync':
                if (!$scfEnabled) {
                    $message = 'SCF API är inte konfigurerat. Lägg till SCF_API_KEY i .env-filen.';
                    $messageType = 'danger';
                    break;
                }

                $year = (int)date('Y');
                $batchSize = 50; // Process 50 riders at a time for web request

                try {
                    // Count how many need syncing
                    $totalToSync = $scfService->countRidersToSync($year, true);

                    if ($totalToSync === 0) {
                        $message = 'Alla deltagare med UCI ID är redan verifierade för ' . $year . '.';
                        $messageType = 'success';
                        break;
                    }

                    // Get a batch of riders to sync
                    $riders = $scfService->getRidersToSync($year, $batchSize, 0, true);

                    if (empty($riders)) {
                        $message = 'Inga deltagare att synkronisera.';
                        $messageType = 'info';
                        break;
                    }

                    // Start sync log
                    $scfService->startSync('manual_batch', $year, count($riders));

                    // Sync the batch
                    $result = $scfService->syncRiderBatch($riders, $year);

                    // Complete sync
                    $scfService->completeSync('completed');

                    // Refresh stats
                    $riderStats['verified_this_year'] = (int)$db->getValue(
                        "SELECT COUNT(*) FROM riders WHERE scf_license_year = ?",
                        [$year]
                    );

                    $message = sprintf(
                        'Synkronisering klar! Bearbetade: %d, Hittade licenser: %d, Uppdaterade: %d, Fel: %d. Totalt kvar: %d',
                        $result['processed'],
                        $result['found'],
                        $result['updated'],
                        $result['errors'],
                        $totalToSync - $result['processed']
                    );
                    $messageType = $result['errors'] > 0 ? 'warning' : 'success';

                } catch (Exception $e) {
                    $scfService->completeSync('failed', $e->getMessage());
                    $message = 'Synkronisering misslyckades: ' . $e->getMessage();
                    $messageType = 'danger';
                    error_log('SCF Sync error: ' . $e->getMessage());
                }
                break;
        }
    }
}

$page_title = 'SCF Licenssynk';
$breadcrumbs = [
    ['label' => 'System', 'url' => '/admin/tools.php'],
    ['label' => 'SCF Licenssynk']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
}
.stat-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    text-align: center;
}
.stat-card .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-accent);
    line-height: 1.2;
}
.stat-card .stat-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-top: var(--space-xs);
}
.stat-card.warning .stat-value { color: var(--color-warning); }
.stat-card.success .stat-value { color: var(--color-success); }
.stat-card.danger .stat-value { color: var(--color-error); }

.progress-bar-container {
    width: 100%;
    height: 24px;
    background: var(--color-bg-hover);
    border-radius: var(--radius-sm);
    overflow: hidden;
    margin: var(--space-md) 0;
}
.progress-bar {
    height: 100%;
    background: var(--color-accent);
    transition: width 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-bg-page);
    font-size: var(--text-sm);
    font-weight: 600;
}

.sync-log-table {
    width: 100%;
    font-size: var(--text-sm);
}
.sync-log-table th {
    text-align: left;
    padding: var(--space-sm);
    border-bottom: 2px solid var(--color-border);
    color: var(--color-text-secondary);
    font-weight: 600;
}
.sync-log-table td {
    padding: var(--space-sm);
    border-bottom: 1px solid var(--color-border);
}
.sync-status {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-2xs) var(--space-sm);
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
    font-weight: 600;
}
.sync-status.completed { background: rgba(16, 185, 129, 0.15); color: var(--color-success); }
.sync-status.running { background: rgba(59, 130, 246, 0.15); color: var(--color-info); }
.sync-status.failed { background: rgba(239, 68, 68, 0.15); color: var(--color-error); }

.action-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-sm);
    margin-top: var(--space-lg);
}

.info-box {
    background: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-bottom: var(--space-lg);
}
.info-box.warning {
    background: rgba(217, 119, 6, 0.1);
    border-color: rgba(217, 119, 6, 0.3);
}

@media (max-width: 767px) {
    .stat-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: var(--space-sm);
    }
    .stat-card {
        padding: var(--space-md);
    }
    .stat-card .stat-value {
        font-size: 1.5rem;
    }
}
</style>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?>">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<?php if (!$scfEnabled): ?>
<div class="info-box warning">
    <strong>SCF API ej konfigurerat</strong><br>
    Lägg till <code>SCF_API_KEY</code> i din <code>.env</code>-fil för att aktivera licenssynkronisering med Svenska Cykelförbundet.
</div>
<?php endif; ?>

<!-- Statistics Overview -->
<div class="stat-grid">
    <div class="stat-card">
        <div class="stat-value"><?= number_format($riderStats['total_riders']) ?></div>
        <div class="stat-label">Totalt deltagare</div>
    </div>
    <div class="stat-card success">
        <div class="stat-value"><?= number_format($riderStats['with_uci_id']) ?></div>
        <div class="stat-label">Med UCI ID</div>
    </div>
    <div class="stat-card warning">
        <div class="stat-value"><?= number_format($riderStats['without_uci_id']) ?></div>
        <div class="stat-label">Utan UCI ID</div>
    </div>
    <div class="stat-card <?= $riderStats['verified_this_year'] > 0 ? 'success' : '' ?>">
        <div class="stat-value"><?= number_format($riderStats['verified_this_year']) ?></div>
        <div class="stat-label">Verifierade <?= date('Y') ?></div>
    </div>
    <div class="stat-card <?= $riderStats['pending_matches'] > 0 ? 'warning' : '' ?>">
        <div class="stat-value"><?= number_format($riderStats['pending_matches']) ?></div>
        <div class="stat-label">Matchningar att granska</div>
    </div>
</div>

<!-- License Verification Progress -->
<?php if ($riderStats['with_uci_id'] > 0): ?>
<div class="card">
    <div class="card-header">
        <h3>Licensverifiering <?= date('Y') ?></h3>
    </div>
    <div class="card-body">
        <?php
        $verificationPercent = round(($riderStats['verified_this_year'] / $riderStats['with_uci_id']) * 100, 1);
        ?>
        <div class="progress-bar-container">
            <div class="progress-bar" style="width: <?= min(100, $verificationPercent) ?>%">
                <?= $verificationPercent ?>%
            </div>
        </div>
        <p class="text-secondary text-sm">
            <?= number_format($riderStats['verified_this_year']) ?> av <?= number_format($riderStats['with_uci_id']) ?> deltagare med UCI ID har verifierats mot SCF <?= date('Y') ?>.
        </p>
    </div>
</div>
<?php endif; ?>

<!-- Quick Actions -->
<div class="card">
    <div class="card-header">
        <h3>Snabbåtgärder</h3>
    </div>
    <div class="card-body">
        <div class="action-buttons">
            <a href="/admin/scf-match-review.php" class="btn btn-primary">
                <i data-lucide="user-check"></i>
                Granska matchningar
                <?php if ($riderStats['pending_matches'] > 0): ?>
                <span class="badge badge-warning"><?= $riderStats['pending_matches'] ?></span>
                <?php endif; ?>
            </a>
            <?php if ($scfEnabled): ?>
            <form method="post" style="display: inline;">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="trigger_sync">
                <button type="submit" class="btn btn-secondary">
                    <i data-lucide="refresh-cw"></i>
                    Starta synkronisering
                </button>
            </form>
            <?php endif; ?>
            <a href="/admin/riders.php?filter=no_uci" class="btn btn-ghost">
                <i data-lucide="search"></i>
                Visa deltagare utan UCI ID
            </a>
        </div>
    </div>
</div>

<!-- Recent Sync Operations -->
<?php if (!empty($recentSyncs)): ?>
<div class="card">
    <div class="card-header">
        <h3>Senaste synkroniseringar</h3>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="sync-log-table">
                <thead>
                    <tr>
                        <th>Tid</th>
                        <th>Typ</th>
                        <th>År</th>
                        <th>Status</th>
                        <th>Bearbetade</th>
                        <th>Hittade</th>
                        <th>Uppdaterade</th>
                        <th>Fel</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($recentSyncs as $sync): ?>
                    <tr>
                        <td>
                            <?= date('Y-m-d H:i', strtotime($sync['started_at'])) ?>
                            <?php if ($sync['completed_at']): ?>
                            <br><span class="text-secondary text-xs">
                                <?php
                                $duration = strtotime($sync['completed_at']) - strtotime($sync['started_at']);
                                echo $duration < 60 ? "{$duration}s" : round($duration / 60, 1) . 'min';
                                ?>
                            </span>
                            <?php endif; ?>
                        </td>
                        <td><?= htmlspecialchars($sync['sync_type']) ?></td>
                        <td><?= $sync['year'] ?></td>
                        <td>
                            <span class="sync-status <?= $sync['status'] ?>">
                                <?php
                                $statusLabels = [
                                    'completed' => 'Klar',
                                    'running' => 'Pågår',
                                    'failed' => 'Misslyckad',
                                    'cancelled' => 'Avbruten'
                                ];
                                echo $statusLabels[$sync['status']] ?? $sync['status'];
                                ?>
                            </span>
                        </td>
                        <td><?= number_format($sync['processed']) ?> / <?= number_format($sync['total_riders']) ?></td>
                        <td><?= number_format($sync['found']) ?></td>
                        <td><?= number_format($sync['updated']) ?></td>
                        <td><?= $sync['errors'] > 0 ? '<span class="text-danger">' . $sync['errors'] . '</span>' : '0' ?></td>
                    </tr>
                    <?php if ($sync['error_message']): ?>
                    <tr>
                        <td colspan="8" class="text-danger text-sm" style="padding-left: var(--space-xl);">
                            <i data-lucide="alert-circle" style="width: 14px; height: 14px;"></i>
                            <?= htmlspecialchars(substr($sync['error_message'], 0, 200)) ?>
                        </td>
                    </tr>
                    <?php endif; ?>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Configuration Info -->
<div class="card">
    <div class="card-header">
        <h3>Konfiguration</h3>
    </div>
    <div class="card-body">
        <table class="table">
            <tr>
                <td><strong>API Status</strong></td>
                <td>
                    <?php if ($scfEnabled): ?>
                    <span class="badge badge-success">Aktiverad</span>
                    <?php else: ?>
                    <span class="badge badge-danger">Ej konfigurerad</span>
                    <?php endif; ?>
                </td>
            </tr>
            <tr>
                <td><strong>API Endpoint</strong></td>
                <td><code>https://licens.scf.se/api/1.0</code></td>
            </tr>
            <tr>
                <td><strong>Max per batch</strong></td>
                <td>25 UCI IDs</td>
            </tr>
            <tr>
                <td><strong>Rate limit</strong></td>
                <td>600ms mellan requests</td>
            </tr>
        </table>

        <h4 class="mt-lg">Cron-kommandon</h4>
        <p class="text-secondary text-sm">Lägg till i crontab för automatisk synkronisering:</p>
        <pre style="background: var(--color-bg-hover); padding: var(--space-md); border-radius: var(--radius-sm); font-size: var(--text-xs); overflow-x: auto;"># Daglig licensverifiering kl 03:00
0 3 * * * cd <?= ROOT_PATH ?>/cron && php sync_scf_licenses.php --year=<?= date('Y') ?> >> /var/log/scf-sync.log 2>&1

# Veckovis matchningssökning söndag kl 04:00
0 4 * * 0 cd <?= ROOT_PATH ?>/cron && php find_scf_matches.php --limit=500 >> /var/log/scf-match.log 2>&1</pre>
    </div>
</div>

<script>
// Refresh Lucide icons
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>
