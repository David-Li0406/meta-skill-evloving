<?php
/**
 * SCF Batch License Verification Tool
 *
 * Searches all UCI IDs in the database against SCF License Portal
 * and shows which riders match/don't match.
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$apiKey = env('SCF_API_KEY', '');
$year = (int)($_GET['year'] ?? date('Y'));

// Initialize SCF service
require_once __DIR__ . '/../includes/SCFLicenseService.php';
$scfService = null;
if ($apiKey) {
    $scfService = new SCFLicenseService($apiKey, $db);
}

$page_title = 'SCF Batch-verifiering';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'SCF Batch-verifiering']
];

// Get statistics
$stats = [
    'total_riders' => 0,
    'with_uci_id' => 0,
    'with_swe_id' => 0,
    'without_id' => 0,
    'verified_this_year' => 0,
    'not_verified' => 0
];

$stats['total_riders'] = (int)$db->getValue("SELECT COUNT(*) FROM riders");
$stats['with_uci_id'] = (int)$db->getValue("SELECT COUNT(*) FROM riders WHERE license_number IS NOT NULL AND license_number != '' AND license_number NOT LIKE 'SWE%'");
$stats['with_swe_id'] = (int)$db->getValue("SELECT COUNT(*) FROM riders WHERE license_number LIKE 'SWE%'");
$stats['without_id'] = (int)$db->getValue("SELECT COUNT(*) FROM riders WHERE license_number IS NULL OR license_number = ''");
$stats['verified_this_year'] = (int)$db->getValue("SELECT COUNT(*) FROM riders WHERE scf_license_year = ?", [$year]);
$stats['not_verified'] = $stats['with_uci_id'] - $stats['verified_this_year'];

// Handle actions
$message = '';
$messageType = 'info';
$results = [];
$progress = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $apiKey) {
    // Extend timeout for batch operations
    set_time_limit(300); // 5 minutes

    $csrfToken = $_POST['csrf_token'] ?? '';
    if (!verify_csrf_token($csrfToken)) {
        $message = 'CSRF-validering misslyckades.';
        $messageType = 'error';
    } else {
        $action = $_POST['action'] ?? '';

        if ($action === 'verify_batch') {
            // Verify a batch of riders
            $batchSize = min(50, max(1, (int)($_POST['batch_size'] ?? 20)));
            $offset = max(0, (int)($_POST['offset'] ?? 0));
            $onlyUnverified = isset($_POST['only_unverified']);

            // Get riders to verify
            $sql = "SELECT id, firstname, lastname, license_number, birth_year, gender,
                           club_id, scf_license_year, scf_license_verified_at
                    FROM riders
                    WHERE license_number IS NOT NULL
                    AND license_number != ''
                    AND license_number NOT LIKE 'SWE%'";

            if ($onlyUnverified) {
                $sql .= " AND (scf_license_year IS NULL OR scf_license_year != ?)";
            }

            $sql .= " ORDER BY id LIMIT ? OFFSET ?";

            $params = $onlyUnverified ? [$year, $batchSize, $offset] : [$batchSize, $offset];
            $riders = $db->getAll($sql, $params);

            if (empty($riders)) {
                $message = 'Inga fler cyklister att verifiera.';
                $messageType = 'info';
            } else {
                // Collect UCI IDs
                $uciIds = [];
                $ridersByUci = [];
                foreach ($riders as $rider) {
                    $uciId = preg_replace('/[^0-9]/', '', $rider['license_number']);
                    if (strlen($uciId) >= 8) {
                        $uciIds[] = $uciId;
                        $ridersByUci[$uciId] = $rider;
                    }
                }

                if (!empty($uciIds)) {
                    // Look up in SCF
                    $scfResults = $scfService->lookupByUciIds($uciIds, $year);

                    // Process results
                    $found = 0;
                    $notFound = 0;
                    $updated = 0;

                    foreach ($ridersByUci as $uciId => $rider) {
                        $normalizedUci = $scfService->normalizeUciId($uciId);
                        $licenseData = $scfResults[$normalizedUci] ?? $scfResults[$uciId] ?? null;

                        $result = [
                            'rider' => $rider,
                            'uci_id' => $uciId,
                            'found' => false,
                            'license_data' => null,
                            'synced' => false
                        ];

                        if ($licenseData) {
                            $found++;
                            $result['found'] = true;
                            $result['license_data'] = $licenseData;

                            // Auto-sync if found
                            if ($scfService->updateRiderLicense($rider['id'], $licenseData, $year)) {
                                $scfService->cacheLicense($licenseData, $year);
                                $result['synced'] = true;
                                $updated++;
                            }
                        } else {
                            $notFound++;
                        }

                        $results[] = $result;
                    }

                    $message = "Verifierade {$found} av " . count($uciIds) . " cyklister. {$updated} uppdaterade.";
                    if ($notFound > 0) {
                        $message .= " {$notFound} hittades inte i SCF.";
                    }
                    $messageType = $notFound > 0 ? 'warning' : 'success';

                    $progress = [
                        'offset' => $offset,
                        'batch_size' => $batchSize,
                        'processed' => count($riders),
                        'next_offset' => $offset + $batchSize
                    ];
                }
            }
        }

        if ($action === 'verify_single') {
            // Verify a single rider
            $riderId = (int)($_POST['rider_id'] ?? 0);
            $rider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$riderId]);

            if ($rider && !empty($rider['license_number'])) {
                $uciId = preg_replace('/[^0-9]/', '', $rider['license_number']);
                $scfResults = $scfService->lookupByUciIds([$uciId], $year);

                $normalizedUci = $scfService->normalizeUciId($uciId);
                $licenseData = $scfResults[$normalizedUci] ?? $scfResults[$uciId] ?? null;

                if ($licenseData) {
                    if ($scfService->updateRiderLicense($riderId, $licenseData, $year)) {
                        $scfService->cacheLicense($licenseData, $year);
                        $message = "Cyklist \"{$rider['firstname']} {$rider['lastname']}\" verifierad och uppdaterad!";
                        $messageType = 'success';
                    }
                } else {
                    $message = "Cyklist \"{$rider['firstname']} {$rider['lastname']}\" hittades inte i SCF.";
                    $messageType = 'warning';
                }
            }
        }
    }
}

// Get sample of unverified riders for preview
$unverifiedRiders = $db->getAll("
    SELECT r.id, r.firstname, r.lastname, r.license_number, r.birth_year, r.gender,
           c.name as club_name, r.scf_license_year, r.scf_license_verified_at
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE r.license_number IS NOT NULL
    AND r.license_number != ''
    AND r.license_number NOT LIKE 'SWE%'
    AND (r.scf_license_year IS NULL OR r.scf_license_year != ?)
    ORDER BY r.lastname, r.firstname
    LIMIT 100
", [$year]);

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}

.stat-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    text-align: center;
}

.stat-value {
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--color-accent);
}

.stat-label {
    font-size: var(--text-sm);
    color: var(--color-text-muted);
}

.stat-card.success .stat-value { color: var(--color-success); }
.stat-card.warning .stat-value { color: var(--color-warning); }
.stat-card.error .stat-value { color: var(--color-error); }

.result-row {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-sm) var(--space-md);
    border-bottom: 1px solid var(--color-border);
}

.result-row:last-child { border-bottom: none; }

.result-row.found { background: rgba(16, 185, 129, 0.05); }
.result-row.not-found { background: rgba(239, 68, 68, 0.05); }

.result-name { flex: 1; font-weight: 500; }
.result-uci { font-family: monospace; font-size: var(--text-sm); }
.result-status { flex-shrink: 0; }

.progress-bar {
    background: var(--color-bg-hover);
    border-radius: var(--radius-full);
    height: 8px;
    overflow: hidden;
    margin-top: var(--space-sm);
}

.progress-fill {
    background: var(--color-accent);
    height: 100%;
    transition: width 0.3s ease;
}
</style>

<?php if (!$apiKey): ?>
<div class="alert alert-danger">
    API-nyckel saknas. Lagg till <code>SCF_API_KEY=din_nyckel</code> i <code>.env</code>-filen.
</div>
<?php else: ?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?>">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<!-- Statistics -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value"><?= number_format($stats['total_riders']) ?></div>
        <div class="stat-label">Totalt cyklister</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= number_format($stats['with_uci_id']) ?></div>
        <div class="stat-label">Med UCI ID</div>
    </div>
    <div class="stat-card warning">
        <div class="stat-value"><?= number_format($stats['with_swe_id']) ?></div>
        <div class="stat-label">Med SWE-ID</div>
    </div>
    <div class="stat-card error">
        <div class="stat-value"><?= number_format($stats['without_id']) ?></div>
        <div class="stat-label">Utan ID</div>
    </div>
    <div class="stat-card success">
        <div class="stat-value"><?= number_format($stats['verified_this_year']) ?></div>
        <div class="stat-label">Verifierade <?= $year ?></div>
    </div>
    <div class="stat-card error">
        <div class="stat-value"><?= number_format($stats['not_verified']) ?></div>
        <div class="stat-label">Ej verifierade</div>
    </div>
</div>

<!-- Batch Verification Form -->
<div class="card">
    <div class="card-header">
        <h3>Batch-verifiering mot SCF</h3>
    </div>
    <div class="card-body">
        <p class="text-secondary" style="margin-bottom: var(--space-md);">
            Soker igenom cyklister med UCI ID mot SCF License Portal och uppdaterar deras licensdata.
        </p>

        <form method="post" id="batchForm">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="verify_batch">
            <input type="hidden" name="auto_continue" id="autoContinueInput" value="0">

            <div style="display: flex; gap: var(--space-md); flex-wrap: wrap; align-items: end;">
                <div class="form-group" style="margin: 0;">
                    <label class="form-label">Batch-storlek</label>
                    <select name="batch_size" id="batchSize" class="form-select" style="width: 100px;">
                        <option value="5">5</option>
                        <option value="10" selected>10</option>
                        <option value="20">20</option>
                        <option value="50">50</option>
                    </select>
                </div>

                <div class="form-group" style="margin: 0;">
                    <label class="form-label">Starta fran</label>
                    <input type="number" name="offset" id="offsetInput" class="form-input" style="width: 100px;" value="<?= $progress['next_offset'] ?? 0 ?>">
                </div>

                <div class="form-group" style="margin: 0;">
                    <label class="admin-checkbox-label">
                        <input type="checkbox" name="only_unverified" id="onlyUnverified" checked>
                        <span>Endast overifierade</span>
                    </label>
                </div>

                <button type="submit" class="btn btn-primary">
                    <i data-lucide="search"></i> Verifiera batch
                </button>

                <button type="button" id="verifyAllBtn" class="btn btn-success" onclick="startAutoVerify()">
                    <i data-lucide="zap"></i> Verifiera ALLA
                </button>

                <button type="button" id="stopBtn" class="btn btn-danger" style="display: none;" onclick="stopAutoVerify()">
                    <i data-lucide="square"></i> Stoppa
                </button>
            </div>
        </form>

        <?php if ($stats['not_verified'] > 0): ?>
        <div class="progress-bar" style="margin-top: var(--space-md);">
            <div class="progress-fill" id="progressFill" style="width: <?= round($stats['verified_this_year'] / $stats['with_uci_id'] * 100) ?>%;"></div>
        </div>
        <p class="text-secondary text-sm" style="margin-top: var(--space-xs);" id="progressText">
            <?= round($stats['verified_this_year'] / $stats['with_uci_id'] * 100, 1) ?>% verifierade
            (<span id="verifiedCount"><?= $stats['verified_this_year'] ?></span> av <?= $stats['with_uci_id'] ?>)
        </p>
        <?php endif; ?>

        <div id="autoStatus" style="display: none; margin-top: var(--space-md); padding: var(--space-md); background: var(--color-bg-hover); border-radius: var(--radius-md);">
            <div style="display: flex; align-items: center; gap: var(--space-sm);">
                <div class="spinner" style="width: 20px; height: 20px; border: 2px solid var(--color-border); border-top-color: var(--color-accent); border-radius: 50%; animation: spin 1s linear infinite;"></div>
                <span id="autoStatusText">Forbereder...</span>
            </div>
        </div>
    </div>
</div>

<style>
@keyframes spin {
    to { transform: rotate(360deg); }
}
</style>

<script>
let isRunning = false;
let totalToVerify = <?= $stats['not_verified'] ?>;
let totalWithUci = <?= $stats['with_uci_id'] ?>;
let currentVerified = <?= $stats['verified_this_year'] ?>;

function startAutoVerify() {
    if (isRunning) return;
    isRunning = true;

    document.getElementById('verifyAllBtn').style.display = 'none';
    document.getElementById('stopBtn').style.display = 'inline-flex';
    document.getElementById('autoStatus').style.display = 'block';
    document.getElementById('autoContinueInput').value = '1';
    document.getElementById('offsetInput').value = '0';

    runNextBatch();
}

function stopAutoVerify() {
    isRunning = false;
    document.getElementById('verifyAllBtn').style.display = 'inline-flex';
    document.getElementById('stopBtn').style.display = 'none';
    document.getElementById('autoStatus').style.display = 'none';
    document.getElementById('autoContinueInput').value = '0';
}

function updateStatus(text) {
    document.getElementById('autoStatusText').textContent = text;
}

function updateProgress(verified, total) {
    const pct = Math.round(verified / total * 100);
    document.getElementById('progressFill').style.width = pct + '%';
    document.getElementById('progressText').innerHTML = pct + '% verifierade (<span id="verifiedCount">' + verified + '</span> av ' + total + ')';
}

let retryCount = 0;
const MAX_RETRIES = 2;

async function runNextBatch() {
    if (!isRunning) return;

    const form = document.getElementById('batchForm');
    const formData = new FormData(form);
    const currentOffset = formData.get('offset');

    updateStatus('Verifierar batch fran position ' + currentOffset + '...');

    // Create abort controller with 120 second timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 120000);

    try {
        const response = await fetch(window.location.href, {
            method: 'POST',
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error('Server returnerade ' + response.status);
        }

        const html = await response.text();

        // Reset retry count on success
        retryCount = 0;

        // Parse the response to get progress info
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');

        // Check for error message in response
        const errorAlert = doc.querySelector('.alert-danger');
        if (errorAlert) {
            console.error('Server error:', errorAlert.textContent);
            updateStatus('Server-fel: ' + errorAlert.textContent.trim());
            // Continue anyway with next batch
        }

        // Check if there are results (meaning more to process)
        const resultRows = doc.querySelectorAll('.result-row');

        // Update stats from response
        const newVerifiedEl = doc.querySelector('.stat-card.success .stat-value');
        if (newVerifiedEl) {
            currentVerified = parseInt(newVerifiedEl.textContent.replace(/[^0-9]/g, ''));
            updateProgress(currentVerified, totalWithUci);
        }

        // Get new offset from response
        const newOffsetInput = doc.querySelector('[name="offset"]');
        const nextOffset = newOffsetInput ? parseInt(newOffsetInput.value) : 0;

        // Check remaining count
        const newNotVerifiedEl = doc.querySelectorAll('.stat-card.error .stat-value');
        let remaining = 0;
        if (newNotVerifiedEl.length >= 2) {
            remaining = parseInt(newNotVerifiedEl[1].textContent.replace(/[^0-9]/g, ''));
        }

        if (resultRows.length > 0 && isRunning && remaining > 0) {
            // More results, continue
            document.getElementById('offsetInput').value = nextOffset;
            const batchSize = parseInt(document.getElementById('batchSize').value);
            updateStatus('Klar med batch (' + resultRows.length + ' st). Fortsatter om 2 sek... (' + remaining + ' kvar)');

            // Delay to not overload API
            setTimeout(runNextBatch, 2000);
        } else {
            // No more results
            stopAutoVerify();
            updateStatus('Klart! Alla cyklister har verifierats.');
            alert('Verifiering klar! Alla cyklister med UCI ID har kontrollerats mot SCF.');
            location.reload();
        }
    } catch (error) {
        clearTimeout(timeoutId);
        console.error('Error:', error);

        if (error.name === 'AbortError') {
            updateStatus('Timeout - forsoker igen...');
        } else {
            updateStatus('Fel: ' + error.message);
        }

        // Retry logic
        retryCount++;
        if (retryCount <= MAX_RETRIES && isRunning) {
            updateStatus('Fel uppstod. Forsoker igen (' + retryCount + '/' + MAX_RETRIES + ')...');
            setTimeout(runNextBatch, 3000);
        } else {
            updateStatus('Avbrot efter ' + MAX_RETRIES + ' misslyckade forsok.');
            stopAutoVerify();
        }
    }
}
</script>

<!-- Results from current batch -->
<?php if (!empty($results)): ?>
<div class="card">
    <div class="card-header">
        <h3>Resultat fran batch</h3>
    </div>
    <div class="card-body p-0">
        <?php foreach ($results as $r): ?>
        <div class="result-row <?= $r['found'] ? 'found' : 'not-found' ?>">
            <div class="result-name">
                <a href="/rider/<?= $r['rider']['id'] ?>" class="color-accent">
                    <?= htmlspecialchars($r['rider']['firstname'] . ' ' . $r['rider']['lastname']) ?>
                </a>
            </div>
            <div class="result-uci"><?= htmlspecialchars($r['uci_id']) ?></div>
            <div class="result-status">
                <?php if ($r['found']): ?>
                    <span class="badge badge-success">
                        <i data-lucide="check" style="width: 14px; height: 14px;"></i>
                        Hittad
                        <?php if ($r['synced']): ?> & synkad<?php endif; ?>
                    </span>
                    <?php if (!empty($r['license_data']['license_type'])): ?>
                        <span class="badge"><?= htmlspecialchars($r['license_data']['license_type']) ?></span>
                    <?php endif; ?>
                    <?php if (!empty($r['license_data']['license_category'])): ?>
                        <span class="badge badge-info"><?= htmlspecialchars($r['license_data']['license_category']) ?></span>
                    <?php endif; ?>
                <?php else: ?>
                    <span class="badge badge-danger">
                        <i data-lucide="x" style="width: 14px; height: 14px;"></i>
                        Ej hittad
                    </span>
                <?php endif; ?>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</div>
<?php endif; ?>

<!-- Unverified riders preview -->
<?php if (!empty($unverifiedRiders)): ?>
<div class="card">
    <div class="card-header">
        <h3>Overifierade cyklister (<?= count($unverifiedRiders) ?> av <?= $stats['not_verified'] ?>)</h3>
    </div>
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>UCI ID</th>
                        <th>Fodelsear</th>
                        <th>Klubb</th>
                        <th>Senast verifierad</th>
                        <th>Atgard</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($unverifiedRiders as $rider): ?>
                    <tr>
                        <td>
                            <a href="/rider/<?= $rider['id'] ?>" class="color-accent">
                                <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                            </a>
                        </td>
                        <td><code><?= htmlspecialchars($rider['license_number']) ?></code></td>
                        <td><?= $rider['birth_year'] ?: '-' ?></td>
                        <td><?= htmlspecialchars($rider['club_name'] ?? '-') ?></td>
                        <td>
                            <?php if ($rider['scf_license_verified_at']): ?>
                                <?= date('Y-m-d', strtotime($rider['scf_license_verified_at'])) ?>
                                (<?= $rider['scf_license_year'] ?>)
                            <?php else: ?>
                                <span class="text-muted">Aldrig</span>
                            <?php endif; ?>
                        </td>
                        <td>
                            <form method="post" style="display: inline;">
                                <?= csrf_field() ?>
                                <input type="hidden" name="action" value="verify_single">
                                <input type="hidden" name="rider_id" value="<?= $rider['id'] ?>">
                                <button type="submit" class="btn btn-sm btn-secondary" title="Verifiera">
                                    <i data-lucide="refresh-cw" style="width: 14px; height: 14px;"></i>
                                </button>
                            </form>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<?php endif; ?>

<script>
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
