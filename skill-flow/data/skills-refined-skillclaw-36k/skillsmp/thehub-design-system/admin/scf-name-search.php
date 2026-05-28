<?php
/**
 * SCF Name Search Tool
 *
 * Searches for riders without UCI ID in SCF using name and birth year.
 * Creates match candidates for manual review.
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

$page_title = 'SCF Namnsok';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'SCF Namnsok']
];

// Get statistics
$stats = [
    'without_uci' => 0,
    'with_swe_id' => 0,
    'pending_matches' => 0,
    'confirmed_matches' => 0
];

$stats['without_uci'] = (int)$db->getValue("SELECT COUNT(*) FROM riders WHERE license_number IS NULL OR license_number = '' OR license_number LIKE 'SWE%'");
$stats['with_swe_id'] = (int)$db->getValue("SELECT COUNT(*) FROM riders WHERE license_number LIKE 'SWE%'");
$stats['pending_matches'] = (int)$db->getValue("SELECT COUNT(*) FROM scf_match_candidates WHERE status = 'pending'");
$stats['confirmed_matches'] = (int)$db->getValue("SELECT COUNT(*) FROM scf_match_candidates WHERE status = 'confirmed'");

// Handle actions
$message = '';
$messageType = 'info';
$searchResults = [];
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

        if ($action === 'search_single') {
            // Search for a single rider
            $riderId = (int)($_POST['rider_id'] ?? 0);
            $rider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$riderId]);

            if ($rider) {
                $firstname = $rider['firstname'];
                $lastname = $rider['lastname'];
                $gender = $rider['gender'] ?: 'M';
                $birthYear = $rider['birth_year'];

                // Build birthdate if we have year
                $birthdate = null;
                if ($birthYear) {
                    $birthdate = $birthYear . '-01-01';
                }

                // Call SCF API
                $apiResults = $scfService->lookupByName($firstname, $lastname, $gender, $birthdate, $year);

                if (!empty($apiResults)) {
                    // Store as match candidates
                    foreach ($apiResults as $scfData) {
                        $matchScore = calculateMatchScore($rider, $scfData);

                        $db->query("
                            INSERT INTO scf_match_candidates
                            (rider_id, hub_firstname, hub_lastname, hub_gender, hub_birth_year,
                             scf_uci_id, scf_firstname, scf_lastname, scf_club, scf_nationality,
                             match_score, match_reason, status)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
                            ON DUPLICATE KEY UPDATE
                                scf_firstname = VALUES(scf_firstname),
                                scf_lastname = VALUES(scf_lastname),
                                scf_club = VALUES(scf_club),
                                match_score = VALUES(match_score),
                                match_reason = VALUES(match_reason)
                        ", [
                            $riderId,
                            $rider['firstname'],
                            $rider['lastname'],
                            $rider['gender'],
                            $rider['birth_year'],
                            $scfData['uci_id'] ?? null,
                            $scfData['firstname'] ?? null,
                            $scfData['lastname'] ?? null,
                            $scfData['club_name'] ?? null,
                            $scfData['nationality'] ?? null,
                            $matchScore['score'],
                            $matchScore['reason']
                        ]);

                        $searchResults[] = [
                            'rider' => $rider,
                            'scf' => $scfData,
                            'score' => $matchScore
                        ];
                    }

                    $message = "Hittade " . count($apiResults) . " potentiella matchningar for \"{$firstname} {$lastname}\".";
                    $messageType = 'success';
                } else {
                    $message = "Ingen matchning hittades for \"{$firstname} {$lastname}\" i SCF.";
                    $messageType = 'warning';
                }
            }
        }

        if ($action === 'search_batch') {
            // Search for a batch of riders without UCI ID
            $batchSize = min(20, max(1, (int)($_POST['batch_size'] ?? 10)));
            $offset = max(0, (int)($_POST['offset'] ?? 0));

            // Get riders without UCI ID
            $riders = $db->getAll("
                SELECT r.*, c.name as club_name
                FROM riders r
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE (r.license_number IS NULL OR r.license_number = '' OR r.license_number LIKE 'SWE%')
                AND r.firstname IS NOT NULL AND r.firstname != ''
                AND r.lastname IS NOT NULL AND r.lastname != ''
                AND NOT EXISTS (
                    SELECT 1 FROM scf_match_candidates mc
                    WHERE mc.rider_id = r.id AND mc.status != 'rejected'
                )
                ORDER BY r.id
                LIMIT ? OFFSET ?
            ", [$batchSize, $offset]);

            $found = 0;
            $notFound = 0;

            foreach ($riders as $rider) {
                $gender = $rider['gender'] ?: 'M';
                $birthdate = $rider['birth_year'] ? $rider['birth_year'] . '-01-01' : null;

                // Rate limiting - wait between API calls
                $scfService->rateLimit();

                $apiResults = $scfService->lookupByName(
                    $rider['firstname'],
                    $rider['lastname'],
                    $gender,
                    $birthdate,
                    $year
                );

                if (!empty($apiResults)) {
                    $found++;
                    foreach ($apiResults as $scfData) {
                        $matchScore = calculateMatchScore($rider, $scfData);

                        $db->query("
                            INSERT INTO scf_match_candidates
                            (rider_id, hub_firstname, hub_lastname, hub_gender, hub_birth_year,
                             scf_uci_id, scf_firstname, scf_lastname, scf_club, scf_nationality,
                             match_score, match_reason, status)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
                            ON DUPLICATE KEY UPDATE
                                scf_firstname = VALUES(scf_firstname),
                                scf_lastname = VALUES(scf_lastname),
                                scf_club = VALUES(scf_club),
                                match_score = VALUES(match_score),
                                match_reason = VALUES(match_reason)
                        ", [
                            $rider['id'],
                            $rider['firstname'],
                            $rider['lastname'],
                            $rider['gender'],
                            $rider['birth_year'],
                            $scfData['uci_id'] ?? null,
                            $scfData['firstname'] ?? null,
                            $scfData['lastname'] ?? null,
                            $scfData['club_name'] ?? null,
                            $scfData['nationality'] ?? null,
                            $matchScore['score'],
                            $matchScore['reason']
                        ]);
                    }
                } else {
                    $notFound++;
                }
            }

            $message = "Sokade " . count($riders) . " cyklister. Hittade matchningar for $found, $notFound utan matchning.";
            $messageType = $found > 0 ? 'success' : 'warning';

            // Track progress for auto-continue
            $progress = [
                'processed' => count($riders),
                'found' => $found,
                'not_found' => $notFound,
                'next_offset' => $offset + $batchSize,
                'has_more' => count($riders) >= $batchSize
            ];
        }

        if ($action === 'confirm_match') {
            // Confirm a match and update rider
            $matchId = (int)($_POST['match_id'] ?? 0);
            $match = $db->getRow("SELECT * FROM scf_match_candidates WHERE id = ?", [$matchId]);

            if ($match && !empty($match['scf_uci_id'])) {
                // Update rider with UCI ID
                $db->query("
                    UPDATE riders
                    SET license_number = ?,
                        updated_at = NOW()
                    WHERE id = ?
                ", [$match['scf_uci_id'], $match['rider_id']]);

                // Mark match as confirmed
                $db->query("
                    UPDATE scf_match_candidates
                    SET status = 'confirmed',
                        reviewed_by = ?,
                        reviewed_at = NOW()
                    WHERE id = ?
                ", [getCurrentUserId(), $matchId]);

                // Now verify the rider's license
                $uciIds = [$match['scf_uci_id']];
                $scfResults = $scfService->lookupByUciIds($uciIds, $year);
                $licenseData = reset($scfResults);

                if ($licenseData) {
                    $scfService->updateRiderLicense($match['rider_id'], $licenseData, $year);
                    $scfService->cacheLicense($licenseData, $year);
                }

                $message = "Matchning bekraftad! Cyklist uppdaterad med UCI ID {$match['scf_uci_id']}.";
                $messageType = 'success';
            }
        }

        if ($action === 'reject_match') {
            $matchId = (int)($_POST['match_id'] ?? 0);
            $db->query("
                UPDATE scf_match_candidates
                SET status = 'rejected',
                    reviewed_by = ?,
                    reviewed_at = NOW()
                WHERE id = ?
            ", [getCurrentUserId(), $matchId]);

            $message = "Matchning avvisad.";
            $messageType = 'info';
        }
    }
}

// Helper function to calculate match score
function calculateMatchScore($rider, $scfData) {
    $score = 0;
    $reasons = [];

    // Name match
    $hubFirstname = mb_strtolower(trim($rider['firstname'] ?? ''));
    $hubLastname = mb_strtolower(trim($rider['lastname'] ?? ''));
    $scfFirstname = mb_strtolower(trim($scfData['firstname'] ?? ''));
    $scfLastname = mb_strtolower(trim($scfData['lastname'] ?? ''));

    if ($hubFirstname === $scfFirstname) {
        $score += 30;
        $reasons[] = "Exakt fornamn (+30)";
    } elseif (similar_text($hubFirstname, $scfFirstname) / max(strlen($hubFirstname), strlen($scfFirstname)) > 0.8) {
        $score += 20;
        $reasons[] = "Liknande fornamn (+20)";
    }

    if ($hubLastname === $scfLastname) {
        $score += 30;
        $reasons[] = "Exakt efternamn (+30)";
    } elseif (similar_text($hubLastname, $scfLastname) / max(strlen($hubLastname), strlen($scfLastname)) > 0.8) {
        $score += 20;
        $reasons[] = "Liknande efternamn (+20)";
    }

    // Birth year match
    if (!empty($rider['birth_year']) && !empty($scfData['birth_year'])) {
        if ($rider['birth_year'] == $scfData['birth_year']) {
            $score += 25;
            $reasons[] = "Samma fodelsear (+25)";
        } elseif (abs($rider['birth_year'] - $scfData['birth_year']) <= 1) {
            $score += 10;
            $reasons[] = "Fodelsear +/-1 ar (+10)";
        }
    }

    // Gender match
    if (!empty($rider['gender']) && !empty($scfData['gender'])) {
        if (strtoupper($rider['gender']) === strtoupper($scfData['gender'])) {
            $score += 10;
            $reasons[] = "Samma kon (+10)";
        }
    }

    // Has license (bonus)
    if (!empty($scfData['license_type'])) {
        $score += 5;
        $reasons[] = "Har licens (+5)";
    }

    return [
        'score' => min(100, $score),
        'reason' => implode(', ', $reasons)
    ];
}

// Get pending match candidates
$pendingMatches = $db->getAll("
    SELECT mc.*, r.firstname as rider_firstname, r.lastname as rider_lastname,
           r.birth_year as rider_birth_year, r.gender as rider_gender,
           c.name as rider_club
    FROM scf_match_candidates mc
    JOIN riders r ON mc.rider_id = r.id
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE mc.status = 'pending'
    ORDER BY mc.match_score DESC, mc.created_at DESC
    LIMIT 50
");

// Get riders without UCI ID for searching
$ridersWithoutUci = $db->getAll("
    SELECT r.id, r.firstname, r.lastname, r.birth_year, r.gender,
           r.license_number, c.name as club_name
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE (r.license_number IS NULL OR r.license_number = '' OR r.license_number LIKE 'SWE%')
    AND r.firstname IS NOT NULL AND r.firstname != ''
    AND r.lastname IS NOT NULL AND r.lastname != ''
    AND NOT EXISTS (
        SELECT 1 FROM scf_match_candidates mc
        WHERE mc.rider_id = r.id AND mc.status != 'rejected'
    )
    ORDER BY r.lastname, r.firstname
    LIMIT 100
");

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

.stat-card.warning .stat-value { color: var(--color-warning); }
.stat-card.success .stat-value { color: var(--color-success); }

.match-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-bottom: var(--space-md);
}

.match-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-sm);
}

.match-score {
    font-size: var(--text-lg);
    font-weight: 700;
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-sm);
}

.match-score.high { background: var(--color-success); color: white; }
.match-score.medium { background: var(--color-warning); color: white; }
.match-score.low { background: var(--color-error); color: white; }

.match-comparison {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: var(--space-md);
    align-items: center;
}

.match-side { padding: var(--space-sm); }
.match-side.hub { background: var(--color-bg-hover); border-radius: var(--radius-sm); }
.match-side.scf { background: rgba(16, 185, 129, 0.1); border-radius: var(--radius-sm); }

.match-arrow {
    color: var(--color-text-muted);
    font-size: var(--text-xl);
}

.match-name { font-weight: 600; font-size: var(--text-base); }
.match-details { font-size: var(--text-sm); color: var(--color-text-secondary); }

.match-actions {
    display: flex;
    gap: var(--space-sm);
    margin-top: var(--space-md);
    padding-top: var(--space-md);
    border-top: 1px solid var(--color-border);
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
    <div class="stat-card warning">
        <div class="stat-value"><?= number_format($stats['without_uci']) ?></div>
        <div class="stat-label">Utan UCI ID</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= number_format($stats['with_swe_id']) ?></div>
        <div class="stat-label">Med SWE-ID</div>
    </div>
    <div class="stat-card warning">
        <div class="stat-value"><?= number_format($stats['pending_matches']) ?></div>
        <div class="stat-label">Vantande matchningar</div>
    </div>
    <div class="stat-card success">
        <div class="stat-value"><?= number_format($stats['confirmed_matches']) ?></div>
        <div class="stat-label">Bekraftade</div>
    </div>
</div>

<!-- Batch Search -->
<div class="card">
    <div class="card-header">
        <h3>Batch-sok i SCF</h3>
    </div>
    <div class="card-body">
        <p class="text-secondary" style="margin-bottom: var(--space-md);">
            Soker efter cyklister utan UCI ID (inklusive SWE-ID) i SCF baserat pa namn och fodelsear.
            Namnsok gar langsamt (en per request) - ca 10 cyklister tar ~6 sekunder.
        </p>

        <form method="post" id="batchForm">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="search_batch">
            <input type="hidden" name="offset" id="offsetInput" value="<?= $progress['next_offset'] ?? 0 ?>">

            <div style="display: flex; gap: var(--space-md); flex-wrap: wrap; align-items: end;">
                <div class="form-group" style="margin: 0;">
                    <label class="form-label">Antal per batch</label>
                    <select name="batch_size" id="batchSize" class="form-select" style="width: 100px;">
                        <option value="5">5</option>
                        <option value="10" selected>10</option>
                        <option value="20">20</option>
                    </select>
                </div>

                <button type="submit" class="btn btn-primary">
                    <i data-lucide="search"></i> Sok batch
                </button>

                <button type="button" id="searchAllBtn" class="btn btn-success" onclick="startAutoSearch()">
                    <i data-lucide="zap"></i> Sok ALLA
                </button>

                <button type="button" id="stopBtn" class="btn btn-danger" style="display: none;" onclick="stopAutoSearch()">
                    <i data-lucide="square"></i> Stoppa
                </button>
            </div>
        </form>

        <?php if ($stats['without_uci'] > 0): ?>
        <div class="progress-bar" style="margin-top: var(--space-md);">
            <div class="progress-fill" id="progressFill" style="width: 0%;"></div>
        </div>
        <p class="text-secondary text-sm" style="margin-top: var(--space-xs);" id="progressText">
            <?= number_format($stats['without_uci']) ?> cyklister utan UCI ID att soka
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
.progress-bar {
    background: var(--color-bg-hover);
    border-radius: var(--radius-full);
    height: 8px;
    overflow: hidden;
}
.progress-fill {
    background: var(--color-accent);
    height: 100%;
    transition: width 0.3s ease;
}
</style>

<script>
let isRunning = false;
let totalToSearch = <?= $stats['without_uci'] - $stats['pending_matches'] ?>;
let totalFound = 0;
let totalProcessed = 0;
let retryCount = 0;
const MAX_RETRIES = 2;

function startAutoSearch() {
    if (isRunning) return;
    isRunning = true;
    totalFound = 0;
    totalProcessed = 0;

    document.getElementById('searchAllBtn').style.display = 'none';
    document.getElementById('stopBtn').style.display = 'inline-flex';
    document.getElementById('autoStatus').style.display = 'block';
    document.getElementById('offsetInput').value = '0';

    runNextBatch();
}

function stopAutoSearch() {
    isRunning = false;
    document.getElementById('searchAllBtn').style.display = 'inline-flex';
    document.getElementById('stopBtn').style.display = 'none';
    document.getElementById('autoStatus').style.display = 'none';
}

function updateStatus(text) {
    document.getElementById('autoStatusText').textContent = text;
}

function updateProgress(processed, total) {
    const pct = total > 0 ? Math.round(processed / total * 100) : 0;
    document.getElementById('progressFill').style.width = pct + '%';
    document.getElementById('progressText').textContent = processed + ' av ' + total + ' sokta (' + pct + '%)';
}

async function runNextBatch() {
    if (!isRunning) return;

    const form = document.getElementById('batchForm');
    const formData = new FormData(form);

    updateStatus('Soker batch fran position ' + formData.get('offset') + '...');

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
        retryCount = 0;

        // Parse the response
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');

        // Check for alert message
        const alertEl = doc.querySelector('.alert-success, .alert-warning');
        if (alertEl) {
            console.log('Batch result:', alertEl.textContent);
        }

        // Get new offset from response
        const newOffsetInput = doc.querySelector('[name="offset"]');
        const nextOffset = newOffsetInput ? parseInt(newOffsetInput.value) : 0;

        // Check remaining count from stats
        const statsCards = doc.querySelectorAll('.stat-card .stat-value');
        let remaining = 0;
        if (statsCards.length >= 1) {
            remaining = parseInt(statsCards[0].textContent.replace(/[^0-9]/g, ''));
        }

        // Check if we got results (processed riders)
        const tableRows = doc.querySelectorAll('.table tbody tr');
        const hasMore = tableRows.length > 0 || remaining > 0;

        totalProcessed += parseInt(document.getElementById('batchSize').value);
        updateProgress(totalProcessed, totalToSearch);

        if (hasMore && isRunning && nextOffset > 0) {
            document.getElementById('offsetInput').value = nextOffset;
            updateStatus('Klar med batch. Fortsatter om 2 sek... (' + remaining + ' cyklister kvar)');
            setTimeout(runNextBatch, 2000);
        } else {
            stopAutoSearch();
            updateStatus('Klart! Alla cyklister har sokts.');
            alert('Sokning klar! Ga igenom "Vantande matchningar" for att bekrafta.');
            location.reload();
        }
    } catch (error) {
        clearTimeout(timeoutId);
        console.error('Error:', error);

        retryCount++;
        if (retryCount <= MAX_RETRIES && isRunning) {
            updateStatus('Fel uppstod. Forsoker igen (' + retryCount + '/' + MAX_RETRIES + ')...');
            setTimeout(runNextBatch, 3000);
        } else {
            updateStatus('Avbrot efter ' + MAX_RETRIES + ' misslyckade forsok.');
            stopAutoSearch();
        }
    }
}
</script>

<!-- Pending Matches -->
<?php if (!empty($pendingMatches)): ?>
<div class="card">
    <div class="card-header">
        <h3>Vantande matchningar (<?= count($pendingMatches) ?>)</h3>
    </div>
    <div class="card-body">
        <?php foreach ($pendingMatches as $match): ?>
        <div class="match-card">
            <div class="match-header">
                <div>
                    <strong>Match #<?= $match['id'] ?></strong>
                    <span class="text-secondary text-sm">
                        Skapad <?= date('Y-m-d H:i', strtotime($match['created_at'])) ?>
                    </span>
                </div>
                <div class="match-score <?= $match['match_score'] >= 70 ? 'high' : ($match['match_score'] >= 40 ? 'medium' : 'low') ?>">
                    <?= $match['match_score'] ?>%
                </div>
            </div>

            <div class="match-comparison">
                <div class="match-side hub">
                    <div class="match-name"><?= htmlspecialchars($match['hub_firstname'] . ' ' . $match['hub_lastname']) ?></div>
                    <div class="match-details">
                        <?php if ($match['rider_birth_year']): ?>Fodd <?= $match['rider_birth_year'] ?><?php endif; ?>
                        <?php if ($match['rider_gender']): ?> &middot; <?= $match['rider_gender'] === 'M' ? 'Man' : 'Kvinna' ?><?php endif; ?>
                        <?php if ($match['rider_club']): ?><br><?= htmlspecialchars($match['rider_club']) ?><?php endif; ?>
                    </div>
                </div>

                <div class="match-arrow">
                    <i data-lucide="arrow-right"></i>
                </div>

                <div class="match-side scf">
                    <div class="match-name"><?= htmlspecialchars($match['scf_firstname'] . ' ' . $match['scf_lastname']) ?></div>
                    <div class="match-details">
                        UCI: <code><?= htmlspecialchars($match['scf_uci_id']) ?></code>
                        <?php if ($match['scf_nationality']): ?> &middot; <?= htmlspecialchars($match['scf_nationality']) ?><?php endif; ?>
                        <?php if ($match['scf_club']): ?><br><?= htmlspecialchars($match['scf_club']) ?><?php endif; ?>
                    </div>
                </div>
            </div>

            <div class="text-secondary text-sm" style="margin-top: var(--space-sm);">
                <?= htmlspecialchars($match['match_reason']) ?>
            </div>

            <div class="match-actions">
                <form method="post" style="display: inline;">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="confirm_match">
                    <input type="hidden" name="match_id" value="<?= $match['id'] ?>">
                    <button type="submit" class="btn btn-primary" onclick="return confirm('Bekrafta matchning och uppdatera cyklisten med UCI ID?')">
                        <i data-lucide="check"></i> Bekrafta
                    </button>
                </form>
                <form method="post" style="display: inline;">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="reject_match">
                    <input type="hidden" name="match_id" value="<?= $match['id'] ?>">
                    <button type="submit" class="btn btn-danger">
                        <i data-lucide="x"></i> Avvisa
                    </button>
                </form>
                <a href="/rider/<?= $match['rider_id'] ?>" class="btn btn-secondary" target="_blank">
                    <i data-lucide="external-link"></i> Visa profil
                </a>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</div>
<?php endif; ?>

<!-- Riders without UCI ID -->
<?php if (!empty($ridersWithoutUci)): ?>
<div class="card">
    <div class="card-header">
        <h3>Cyklister utan UCI ID (<?= count($ridersWithoutUci) ?>)</h3>
    </div>
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>Nuvarande ID</th>
                        <th>Fodelsear</th>
                        <th>Kon</th>
                        <th>Klubb</th>
                        <th>Atgard</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($ridersWithoutUci as $rider): ?>
                    <tr>
                        <td>
                            <a href="/rider/<?= $rider['id'] ?>" class="color-accent">
                                <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                            </a>
                        </td>
                        <td>
                            <?php if ($rider['license_number']): ?>
                                <code class="text-warning"><?= htmlspecialchars($rider['license_number']) ?></code>
                            <?php else: ?>
                                <span class="text-muted">-</span>
                            <?php endif; ?>
                        </td>
                        <td><?= $rider['birth_year'] ?: '-' ?></td>
                        <td><?= $rider['gender'] ?: '-' ?></td>
                        <td><?= htmlspecialchars($rider['club_name'] ?? '-') ?></td>
                        <td>
                            <form method="post" style="display: inline;">
                                <?= csrf_field() ?>
                                <input type="hidden" name="action" value="search_single">
                                <input type="hidden" name="rider_id" value="<?= $rider['id'] ?>">
                                <button type="submit" class="btn btn-sm btn-secondary" title="Sok i SCF">
                                    <i data-lucide="search" style="width: 14px; height: 14px;"></i>
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
