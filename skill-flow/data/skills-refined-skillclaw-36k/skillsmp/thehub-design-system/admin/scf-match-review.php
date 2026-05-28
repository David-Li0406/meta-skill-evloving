<?php
/**
 * SCF License Match Review
 *
 * Admin interface for reviewing and confirming/rejecting
 * potential UCI ID matches found by the SCF License sync.
 *
 * @package TheHUB Admin
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
require_once __DIR__ . '/../includes/SCFLicenseService.php';

// Get API key from environment
$apiKey = env('SCF_API_KEY', '');
$scfService = new SCFLicenseService($apiKey, $db);

// Get current admin user
$adminUser = get_admin_user();
$adminId = $adminUser['id'] ?? 0;

// Handle actions
$message = '';
$messageType = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    if (!check_csrf()) {
        $message = 'CSRF-validering misslyckades.';
        $messageType = 'danger';
    } else {
        $matchId = (int)($_POST['match_id'] ?? 0);

        switch ($_POST['action']) {
            case 'confirm':
                if ($matchId && $scfService->confirmMatch($matchId, $adminId)) {
                    $message = 'Matchning bekräftad! UCI ID har tilldelats deltagaren.';
                    $messageType = 'success';
                } else {
                    $message = 'Kunde inte bekräfta matchningen.';
                    $messageType = 'danger';
                }
                break;

            case 'reject':
                if ($matchId && $scfService->rejectMatch($matchId, $adminId)) {
                    $message = 'Matchning avvisad.';
                    $messageType = 'info';
                } else {
                    $message = 'Kunde inte avvisa matchningen.';
                    $messageType = 'danger';
                }
                break;

            case 'bulk_confirm':
                $matchIds = $_POST['match_ids'] ?? [];
                $confirmed = 0;
                foreach ($matchIds as $id) {
                    if ($scfService->confirmMatch((int)$id, $adminId)) {
                        $confirmed++;
                    }
                }
                $message = "$confirmed matchningar bekräftade.";
                $messageType = 'success';
                break;

            case 'bulk_reject':
                $matchIds = $_POST['match_ids'] ?? [];
                $rejected = 0;
                foreach ($matchIds as $id) {
                    if ($scfService->rejectMatch((int)$id, $adminId)) {
                        $rejected++;
                    }
                }
                $message = "$rejected matchningar avvisade.";
                $messageType = 'info';
                break;
        }
    }
}

// Get filters
$minScore = isset($_GET['min_score']) ? (float)$_GET['min_score'] : 0;
$limit = isset($_GET['limit']) ? min(200, max(10, (int)$_GET['limit'])) : 50;

// Get pending matches
$pendingMatches = $scfService->getPendingMatches($limit, $minScore);

// Count total pending
$totalPending = (int)$db->getValue("SELECT COUNT(*) FROM scf_match_candidates WHERE status = 'pending'");
$highConfidence = (int)$db->getValue("SELECT COUNT(*) FROM scf_match_candidates WHERE status = 'pending' AND match_score >= 90");

$page_title = 'Granska matchningar';
$breadcrumbs = [
    ['label' => 'System', 'url' => '/admin/tools.php'],
    ['label' => 'SCF Licenssynk', 'url' => '/admin/scf-sync-status.php'],
    ['label' => 'Granska matchningar']
];

$page_actions = '
<a href="/admin/scf-sync-status.php" class="btn btn-ghost">
    <i data-lucide="arrow-left"></i>
    Tillbaka
</a>';

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.match-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-md);
    overflow: hidden;
}
.match-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border-bottom: 1px solid var(--color-border);
    gap: var(--space-md);
    flex-wrap: wrap;
}
.match-score {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}
.score-badge {
    font-size: 1.25rem;
    font-weight: 700;
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-sm);
}
.score-badge.high { background: rgba(16, 185, 129, 0.15); color: var(--color-success); }
.score-badge.medium { background: rgba(217, 119, 6, 0.15); color: var(--color-warning); }
.score-badge.low { background: rgba(239, 68, 68, 0.15); color: var(--color-error); }

.match-body {
    display: grid;
    grid-template-columns: 1fr 60px 1fr;
    gap: var(--space-lg);
    padding: var(--space-md);
    align-items: start;
}
.match-source {
    padding: var(--space-md);
    background: var(--color-bg-hover);
    border-radius: var(--radius-sm);
}
.match-source h4 {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin: 0 0 var(--space-sm);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.match-source .name {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--space-sm);
}
.match-source .details {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}
.match-source .details p {
    margin: var(--space-2xs) 0;
}
.match-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-accent);
}

.match-actions {
    display: flex;
    gap: var(--space-sm);
    padding: var(--space-md);
    border-top: 1px solid var(--color-border);
    background: var(--color-bg-surface);
}
.match-actions .btn {
    flex: 1;
}

.bulk-actions {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
}
.bulk-actions .selection-info {
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
}

.filter-bar {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
}
.filter-bar .form-group {
    margin: 0;
}
.filter-bar label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-right: var(--space-xs);
}

.empty-state {
    text-align: center;
    padding: var(--space-3xl);
    color: var(--color-text-secondary);
}
.empty-state i {
    width: 48px;
    height: 48px;
    margin-bottom: var(--space-md);
    color: var(--color-accent);
}

@media (max-width: 767px) {
    .match-body {
        grid-template-columns: 1fr;
    }
    .match-arrow {
        transform: rotate(90deg);
        padding: var(--space-sm) 0;
    }
    .match-actions {
        flex-direction: column;
    }
}
</style>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?>">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<!-- Summary Stats -->
<div class="stat-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: var(--space-md); margin-bottom: var(--space-lg);">
    <div class="stat-card" style="background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-md); text-align: center;">
        <div style="font-size: 1.5rem; font-weight: 700; color: var(--color-accent);"><?= $totalPending ?></div>
        <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Att granska</div>
    </div>
    <div class="stat-card" style="background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-md); text-align: center;">
        <div style="font-size: 1.5rem; font-weight: 700; color: var(--color-success);"><?= $highConfidence ?></div>
        <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Hög konfidensgrad (90%+)</div>
    </div>
</div>

<!-- Filters -->
<form method="get" class="filter-bar">
    <div class="form-group">
        <label>Min. poäng:</label>
        <select name="min_score" class="form-select form-select-sm" onchange="this.form.submit()">
            <option value="0" <?= $minScore == 0 ? 'selected' : '' ?>>Alla</option>
            <option value="50" <?= $minScore == 50 ? 'selected' : '' ?>>50%+</option>
            <option value="75" <?= $minScore == 75 ? 'selected' : '' ?>>75%+</option>
            <option value="90" <?= $minScore == 90 ? 'selected' : '' ?>>90%+ (Hög)</option>
        </select>
    </div>
    <div class="form-group">
        <label>Visa:</label>
        <select name="limit" class="form-select form-select-sm" onchange="this.form.submit()">
            <option value="25" <?= $limit == 25 ? 'selected' : '' ?>>25</option>
            <option value="50" <?= $limit == 50 ? 'selected' : '' ?>>50</option>
            <option value="100" <?= $limit == 100 ? 'selected' : '' ?>>100</option>
            <option value="200" <?= $limit == 200 ? 'selected' : '' ?>>200</option>
        </select>
    </div>
</form>

<?php if (empty($pendingMatches)): ?>
<div class="empty-state">
    <i data-lucide="check-circle"></i>
    <h3>Inga matchningar att granska</h3>
    <p>Det finns inga väntande matchningar just nu. Kör matchningssökningen för att hitta nya.</p>
    <a href="/admin/scf-sync-status.php" class="btn btn-primary mt-md">
        Tillbaka till SCF Status
    </a>
</div>
<?php else: ?>

<!-- Bulk Actions -->
<form method="post" id="bulkForm">
    <?= csrf_field() ?>
    <div class="bulk-actions">
        <label class="form-check">
            <input type="checkbox" id="selectAll" onchange="toggleSelectAll(this)">
            <span>Markera alla</span>
        </label>
        <span class="selection-info">
            <span id="selectedCount">0</span> valda
        </span>
        <button type="submit" name="action" value="bulk_confirm" class="btn btn-success btn-sm" disabled id="bulkConfirmBtn">
            <i data-lucide="check"></i>
            Bekräfta valda
        </button>
        <button type="submit" name="action" value="bulk_reject" class="btn btn-danger btn-sm" disabled id="bulkRejectBtn">
            <i data-lucide="x"></i>
            Avvisa valda
        </button>
    </div>

    <!-- Match Cards -->
    <?php foreach ($pendingMatches as $match): ?>
    <?php
    $scoreClass = $match['match_score'] >= 90 ? 'high' : ($match['match_score'] >= 75 ? 'medium' : 'low');
    ?>
    <div class="match-card">
        <div class="match-header">
            <label class="form-check" style="margin: 0;">
                <input type="checkbox" name="match_ids[]" value="<?= $match['id'] ?>" class="match-checkbox" onchange="updateBulkButtons()">
            </label>
            <div class="match-score">
                <span class="score-badge <?= $scoreClass ?>"><?= number_format($match['match_score'], 0) ?>%</span>
                <span class="text-secondary text-sm"><?= htmlspecialchars($match['match_reason']) ?></span>
            </div>
            <a href="/rider/<?= $match['rider_id'] ?>" class="btn btn-ghost btn-sm" target="_blank">
                <i data-lucide="external-link"></i>
                Visa profil
            </a>
        </div>

        <div class="match-body">
            <!-- TheHUB Data -->
            <div class="match-source">
                <h4>TheHUB</h4>
                <div class="name"><?= htmlspecialchars($match['hub_firstname'] . ' ' . $match['hub_lastname']) ?></div>
                <div class="details">
                    <?php if ($match['hub_gender']): ?>
                    <p><strong>Kön:</strong> <?= $match['hub_gender'] === 'M' ? 'Man' : 'Kvinna' ?></p>
                    <?php endif; ?>
                    <?php if ($match['hub_birth_year']): ?>
                    <p><strong>Födelseår:</strong> <?= $match['hub_birth_year'] ?></p>
                    <?php endif; ?>
                    <p><strong>Rider ID:</strong> #<?= $match['rider_id'] ?></p>
                </div>
            </div>

            <!-- Arrow -->
            <div class="match-arrow">
                <i data-lucide="arrow-right" style="width: 32px; height: 32px;"></i>
            </div>

            <!-- SCF Data -->
            <div class="match-source" style="background: rgba(55, 212, 214, 0.1);">
                <h4>SCF License Portal</h4>
                <div class="name"><?= htmlspecialchars($match['scf_firstname'] . ' ' . $match['scf_lastname']) ?></div>
                <div class="details">
                    <p><strong>UCI ID:</strong> <code><?= htmlspecialchars($match['scf_uci_id']) ?></code></p>
                    <?php if ($match['scf_nationality']): ?>
                    <p><strong>Nationalitet:</strong> <?= htmlspecialchars($match['scf_nationality']) ?></p>
                    <?php endif; ?>
                    <?php if ($match['scf_club']): ?>
                    <p><strong>Klubb:</strong> <?= htmlspecialchars($match['scf_club']) ?></p>
                    <?php endif; ?>
                </div>
            </div>
        </div>

        <div class="match-actions">
            <button type="submit" name="action" value="confirm" class="btn btn-success" onclick="setMatchId(<?= $match['id'] ?>)">
                <i data-lucide="check"></i>
                Bekräfta
            </button>
            <button type="submit" name="action" value="reject" class="btn btn-danger" onclick="setMatchId(<?= $match['id'] ?>)">
                <i data-lucide="x"></i>
                Avvisa
            </button>
        </div>
    </div>
    <?php endforeach; ?>

    <input type="hidden" name="match_id" id="singleMatchId" value="">
</form>

<script>
function setMatchId(id) {
    document.getElementById('singleMatchId').value = id;
}

function toggleSelectAll(checkbox) {
    var checkboxes = document.querySelectorAll('.match-checkbox');
    checkboxes.forEach(function(cb) {
        cb.checked = checkbox.checked;
    });
    updateBulkButtons();
}

function updateBulkButtons() {
    var checkboxes = document.querySelectorAll('.match-checkbox:checked');
    var count = checkboxes.length;
    document.getElementById('selectedCount').textContent = count;
    document.getElementById('bulkConfirmBtn').disabled = count === 0;
    document.getElementById('bulkRejectBtn').disabled = count === 0;

    // Update select all checkbox
    var total = document.querySelectorAll('.match-checkbox').length;
    document.getElementById('selectAll').checked = count === total && total > 0;
}

// Refresh Lucide icons
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>

<?php endif; ?>
