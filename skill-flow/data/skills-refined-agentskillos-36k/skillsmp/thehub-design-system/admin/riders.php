<?php
/**
 * Admin Riders - V3 Design System
 */
require_once __DIR__ . '/../config.php';
require_admin();

global $pdo;
$db = getDB();

// Message variables
$message = '';
$messageType = 'info';

// Handle POST actions (merge)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'merge') {
        $keepId = intval($_POST['keep_id'] ?? 0);
        $mergeIds = $_POST['merge_ids'] ?? [];

        // Ensure mergeIds is array of integers
        $mergeIds = array_map('intval', (array)$mergeIds);
        $mergeIds = array_filter($mergeIds, fn($id) => $id > 0 && $id !== $keepId);

        if ($keepId && !empty($mergeIds)) {
            try {
                // Get rider names for message
                $keepRider = $db->getRow("SELECT firstname, lastname FROM riders WHERE id = ?", [$keepId]);
                if (!$keepRider) {
                    throw new Exception('Måldeltagaren hittades inte');
                }
                $keepName = $keepRider['firstname'] . ' ' . $keepRider['lastname'];

                $mergedNames = [];
                foreach ($mergeIds as $mergeId) {
                    $mergeRider = $db->getRow("SELECT firstname, lastname FROM riders WHERE id = ?", [$mergeId]);
                    if ($mergeRider) {
                        $mergedNames[] = $mergeRider['firstname'] . ' ' . $mergeRider['lastname'];
                    }
                }

                if (empty($mergedNames)) {
                    throw new Exception('Inga deltagare att slå samman hittades');
                }

                $pdo = $db->getPdo();
                $pdo->beginTransaction();

                foreach ($mergeIds as $removeId) {
                    // Move results
                    $stmt = $pdo->prepare("UPDATE results SET cyclist_id = ? WHERE cyclist_id = ?");
                    $stmt->execute([$keepId, $removeId]);

                    // Move series_results
                    $stmt = $pdo->prepare("UPDATE series_results SET cyclist_id = ? WHERE cyclist_id = ?");
                    $stmt->execute([$keepId, $removeId]);

                    // Move elimination_qualifying
                    try {
                        $stmt = $pdo->prepare("UPDATE elimination_qualifying SET rider_id = ? WHERE rider_id = ?");
                        $stmt->execute([$keepId, $removeId]);
                    } catch (Exception $e) { /* Table might not exist */ }

                    // Move elimination_brackets (all rider fields)
                    try {
                        $pdo->prepare("UPDATE elimination_brackets SET rider_1_id = ? WHERE rider_1_id = ?")->execute([$keepId, $removeId]);
                        $pdo->prepare("UPDATE elimination_brackets SET rider_2_id = ? WHERE rider_2_id = ?")->execute([$keepId, $removeId]);
                        $pdo->prepare("UPDATE elimination_brackets SET winner_id = ? WHERE winner_id = ?")->execute([$keepId, $removeId]);
                        $pdo->prepare("UPDATE elimination_brackets SET loser_id = ? WHERE loser_id = ?")->execute([$keepId, $removeId]);
                    } catch (Exception $e) { /* Table might not exist */ }

                    // Move elimination_results
                    try {
                        $pdo->prepare("UPDATE elimination_results SET rider_id = ? WHERE rider_id = ?")->execute([$keepId, $removeId]);
                    } catch (Exception $e) { /* Table might not exist */ }

                    // Move event_registrations (delete duplicates first)
                    try {
                        $pdo->prepare("DELETE er1 FROM event_registrations er1 INNER JOIN event_registrations er2 ON er1.event_id = er2.event_id WHERE er1.rider_id = ? AND er2.rider_id = ?")->execute([$removeId, $keepId]);
                        $pdo->prepare("UPDATE event_registrations SET rider_id = ? WHERE rider_id = ?")->execute([$keepId, $removeId]);
                    } catch (Exception $e) { /* Table might not exist */ }

                    // Move event_tickets
                    try {
                        $pdo->prepare("DELETE et1 FROM event_tickets et1 INNER JOIN event_tickets et2 ON et1.event_id = et2.event_id WHERE et1.rider_id = ? AND et2.rider_id = ?")->execute([$removeId, $keepId]);
                        $pdo->prepare("UPDATE event_tickets SET rider_id = ? WHERE rider_id = ?")->execute([$keepId, $removeId]);
                    } catch (Exception $e) { /* Table might not exist */ }

                    // Move club_rider_points
                    try {
                        $pdo->prepare("UPDATE club_rider_points SET rider_id = ? WHERE rider_id = ?")->execute([$keepId, $removeId]);
                    } catch (Exception $e) { /* Table might not exist */ }

                    // Move event_refund_requests
                    try {
                        $pdo->prepare("UPDATE event_refund_requests SET rider_id = ? WHERE rider_id = ?")->execute([$keepId, $removeId]);
                    } catch (Exception $e) { /* Table might not exist */ }

                    // Move rider_claims
                    try {
                        $pdo->prepare("UPDATE rider_claims SET claimed_rider_id = ? WHERE claimed_rider_id = ?")->execute([$keepId, $removeId]);
                        $pdo->prepare("UPDATE rider_claims SET requesting_rider_id = ? WHERE requesting_rider_id = ?")->execute([$keepId, $removeId]);
                    } catch (Exception $e) { /* Table might not exist */ }

                    // Record merge in rider_merge_map (to prevent recreating merged riders on import)
                    try {
                        $mergedRiderInfo = $db->getRow("SELECT firstname, lastname, license_number FROM riders WHERE id = ?", [$removeId]);
                        if ($mergedRiderInfo) {
                            $pdo->prepare("
                                INSERT INTO rider_merge_map (canonical_rider_id, merged_rider_id, merged_firstname, merged_lastname, merged_license_number, reason, status)
                                VALUES (?, ?, ?, ?, ?, 'manual_merge', 'approved')
                                ON DUPLICATE KEY UPDATE canonical_rider_id = VALUES(canonical_rider_id), merged_firstname = VALUES(merged_firstname), merged_lastname = VALUES(merged_lastname), merged_license_number = VALUES(merged_license_number)
                            ")->execute([$keepId, $removeId, $mergedRiderInfo['firstname'], $mergedRiderInfo['lastname'], $mergedRiderInfo['license_number']]);
                        }
                    } catch (Exception $e) { /* Table might not exist yet */ }

                    // Delete the merged rider
                    $pdo->prepare("DELETE FROM riders WHERE id = ?")->execute([$removeId]);
                }

                $pdo->commit();

                $count = count($mergedNames);
                if ($count === 1) {
                    $message = "Deltagaren \"{$mergedNames[0]}\" har slagits samman med \"$keepName\"";
                } else {
                    $message = "$count deltagare har slagits samman med \"$keepName\": " . implode(', ', $mergedNames);
                }
                $messageType = 'success';
            } catch (Exception $e) {
                if (isset($pdo) && $pdo->inTransaction()) {
                    $pdo->rollBack();
                }
                $message = 'Fel vid sammanslagning: ' . $e->getMessage();
                $messageType = 'error';
            }
        } else {
            $message = 'Välj minst två deltagare att slå samman';
            $messageType = 'error';
        }
    }
}

// Handle search and filters
$search = $_GET['search'] ?? '';
$club_id = isset($_GET['club_id']) && is_numeric($_GET['club_id']) ? intval($_GET['club_id']) : null;
$nationality = isset($_GET['nationality']) && strlen($_GET['nationality']) >= 2 && strlen($_GET['nationality']) <= 3 ? strtoupper($_GET['nationality']) : null;
$onlyWithResults = isset($_GET['with_results']) && $_GET['with_results'] == '1';
$onlySweId = isset($_GET['swe_only']) && $_GET['swe_only'] == '1';
$onlyActivated = isset($_GET['activated']) && $_GET['activated'] == '1';
$onlyLicensed2026 = isset($_GET['licensed_2026']) && $_GET['licensed_2026'] == '1';
$hasEmail = isset($_GET['has_email']) ? $_GET['has_email'] : null; // null = all, '1' = with email, '0' = without email

// Handle sorting
$sortBy = $_GET['sort'] ?? 'name';
$sortOrder = $_GET['order'] ?? 'asc';

// Validate sort parameters
$allowedSorts = ['name', 'year', 'club', 'license', 'results', 'nationality'];
$allowedOrders = ['asc', 'desc'];
if (!in_array($sortBy, $allowedSorts)) $sortBy = 'name';
if (!in_array($sortOrder, $allowedOrders)) $sortOrder = 'asc';

// Build ORDER BY clause
$orderBy = '';
if ($sortBy === 'name') {
    $orderBy = $sortOrder === 'asc' ? 'c.lastname ASC, c.firstname ASC' : 'c.lastname DESC, c.firstname DESC';
} elseif ($sortBy === 'year') {
    $orderBy = $sortOrder === 'asc' ? 'c.birth_year ASC' : 'c.birth_year DESC';
} elseif ($sortBy === 'club') {
    $orderBy = $sortOrder === 'asc' ? 'cl.name ASC, c.lastname ASC' : 'cl.name DESC, c.lastname ASC';
} elseif ($sortBy === 'license') {
    $orderBy = $sortOrder === 'asc' ? 'c.license_number ASC' : 'c.license_number DESC';
} elseif ($sortBy === 'results') {
    $orderBy = $sortOrder === 'asc' ? 'result_count ASC, c.lastname ASC' : 'result_count DESC, c.lastname ASC';
} elseif ($sortBy === 'nationality') {
    $orderBy = $sortOrder === 'asc' ? 'c.nationality ASC, c.lastname ASC' : 'c.nationality DESC, c.lastname ASC';
}

// Build query filters
$where = [];
$params = [];

if ($search) {
    $where[] = "(CONCAT(c.firstname, ' ', c.lastname) LIKE ? OR c.license_number LIKE ?)";
    $params[] = "%$search%";
    $params[] = "%$search%";
}

if ($club_id) {
    $where[] = "c.club_id = ?";
    $params[] = $club_id;
}

if ($nationality) {
    $where[] = "c.nationality = ?";
    $params[] = $nationality;
}

if ($onlyWithResults) {
    $where[] = "EXISTS (SELECT 1 FROM results r WHERE r.cyclist_id = c.id)";
}

if ($onlySweId) {
    $where[] = "c.license_number LIKE 'SWE%'";
}

if ($onlyActivated) {
    $where[] = "c.password IS NOT NULL AND c.password != ''";
}

if ($onlyLicensed2026) {
    $currentYear = (int)date('Y');
    $where[] = "(c.scf_license_year = $currentYear OR c.license_year = $currentYear)";
}

if ($hasEmail === '1') {
    $where[] = "c.email IS NOT NULL AND c.email != ''";
} elseif ($hasEmail === '0') {
    $where[] = "(c.email IS NULL OR c.email = '')";
}

$whereClause = $where ? 'WHERE ' . implode(' AND ', $where) : '';

// Check if scf_license_year column exists
$hasScfColumn = false;
try {
    $columns = $db->getAll("SHOW COLUMNS FROM riders LIKE 'scf_license_year'");
    $hasScfColumn = !empty($columns);
} catch (Exception $e) {}

$scfSelect = $hasScfColumn ? "c.scf_license_year," : "NULL as scf_license_year,";

$sql = "SELECT
    c.id, c.firstname, c.lastname, c.birth_year, c.gender, c.nationality,
    c.license_number, c.license_type, c.license_category, c.license_valid_until, c.discipline, c.active,
    {$scfSelect}
    COALESCE(cl.name, cl_season.name) as club_name,
    COALESCE(cl.id, rcs_latest.club_id) as club_id,
    (SELECT COUNT(*) FROM results r WHERE r.cyclist_id = c.id) as result_count
FROM riders c
LEFT JOIN clubs cl ON c.club_id = cl.id
LEFT JOIN (
    SELECT rider_id, club_id
    FROM rider_club_seasons rcs1
    WHERE season_year = (SELECT MAX(season_year) FROM rider_club_seasons rcs2 WHERE rcs2.rider_id = rcs1.rider_id)
) rcs_latest ON rcs_latest.rider_id = c.id AND c.club_id IS NULL
LEFT JOIN clubs cl_season ON rcs_latest.club_id = cl_season.id
$whereClause
ORDER BY {$orderBy}
LIMIT 1000";

$riders = $db->getAll($sql, $params);

// Get selected club info if filtering
$selectedClub = null;
if ($club_id) {
    $selectedClub = $db->getRow("SELECT * FROM clubs WHERE id = ?", [$club_id]);
}

// Get distinct nationalities for filter dropdown
$nationalities = $db->getAll("SELECT DISTINCT nationality, COUNT(*) as count FROM riders WHERE nationality IS NOT NULL AND nationality != '' GROUP BY nationality ORDER BY count DESC, nationality ASC");

// Common nationality names for display
$nationalityNames = [
    'SWE' => 'Sverige',
    'NOR' => 'Norge',
    'DEN' => 'Danmark',
    'FIN' => 'Finland',
    'GBR' => 'Storbritannien',
    'GER' => 'Tyskland',
    'FRA' => 'Frankrike',
    'ITA' => 'Italien',
    'ESP' => 'Spanien',
    'USA' => 'USA',
    'CAN' => 'Kanada',
    'AUS' => 'Australien',
    'NZL' => 'Nya Zeeland',
    'AUT' => 'Österrike',
    'SUI' => 'Schweiz',
    'BEL' => 'Belgien',
    'NED' => 'Nederländerna',
    'POL' => 'Polen',
    'CZE' => 'Tjeckien',
];

// Helper function for age calculation (use existing if available)
if (!function_exists('calculateAge')) {
    function calculateAge($birthYear) {
        if (!$birthYear) return null;
        return date('Y') - $birthYear;
    }
}

// Page config
$page_title = 'Deltagare';
$breadcrumbs = [
    ['label' => 'Deltagare']
];

// Get pending claims count for notification badge
$pendingClaimsCount = 0;
try {
    $claimsResult = $db->getRow("SELECT COUNT(*) as cnt FROM rider_claims WHERE status = 'pending'");
    $pendingClaimsCount = (int)($claimsResult['cnt'] ?? 0);
} catch (Exception $e) {
    // Table might not exist
}

$claimsButton = '';
if ($pendingClaimsCount > 0) {
    $claimsButton = '<a href="/admin/rider-claims" class="btn-admin btn-admin-warning" style="position: relative;">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><polyline points="16 11 18 13 22 9"/></svg>
    Väntande förfrågningar
    <span style="position: absolute; top: -6px; right: -6px; background: #ef4444; color: white; font-size: 11px; font-weight: 600; padding: 2px 6px; border-radius: 10px;">' . $pendingClaimsCount . '</span>
</a> ';
} else {
    $claimsButton = '<a href="/admin/rider-claims" class="btn-admin btn-admin-secondary">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><polyline points="16 11 18 13 22 9"/></svg>
    Profilförfrågningar
</a> ';
}

$page_actions = $claimsButton . '<a href="/admin/import/riders" class="btn-admin btn-admin-primary">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
    Importera
</a>';

// Build sort URL helper
function buildSortUrl($field, $currentSort, $currentOrder, $search, $club_id, $nationality, $onlyWithResults, $onlySweId, $onlyActivated, $onlyLicensed2026, $hasEmail) {
    $newOrder = ($currentSort === $field && $currentOrder === 'asc') ? 'desc' : 'asc';
    $url = "?sort=$field&order=$newOrder";
    if ($search) $url .= '&search=' . urlencode($search);
    if ($club_id) $url .= '&club_id=' . $club_id;
    if ($nationality) $url .= '&nationality=' . urlencode($nationality);
    if ($onlyWithResults) $url .= '&with_results=1';
    if ($onlySweId) $url .= '&swe_only=1';
    if ($onlyActivated) $url .= '&activated=1';
    if ($onlyLicensed2026) $url .= '&licensed_2026=1';
    if ($hasEmail !== null) $url .= '&has_email=' . $hasEmail;
    return $url;
}

// Include unified layout (uses same layout as public site)
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
    <div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'info') ?>">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <?php if ($messageType === 'success'): ?>
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
            <?php elseif ($messageType === 'error'): ?>
                <circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>
            <?php else: ?>
                <circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/><line x1="12" x2="12.01" y1="8" y2="8"/>
            <?php endif; ?>
        </svg>
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<?php if ($selectedClub): ?>
    <div class="alert alert-info">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/><line x1="12" x2="12.01" y1="8" y2="8"/></svg>
        <span>Visar deltagare från <strong><?= htmlspecialchars($selectedClub['name']) ?></strong></span>
        <a href="/admin/riders" class="btn-admin btn-admin-sm btn-admin-secondary ml-auto">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
            Rensa filter
        </a>
    </div>
<?php endif; ?>

<!-- Search and Filter -->
<div class="admin-card">
    <div class="admin-card-body">
        <form method="GET" id="searchForm" class="admin-form-row items-end">
            <?php if ($club_id): ?>
                <input type="hidden" name="club_id" value="<?= $club_id ?>">
            <?php endif; ?>

            <div class="admin-form-group flex-1 mb-0">
                <label for="searchInput" class="admin-form-label">Sök</label>
                <input
                    type="text"
                    name="search"
                    id="searchInput"
                    class="admin-form-input"
                    placeholder="Sök efter namn eller licensnummer..."
                    value="<?= htmlspecialchars($search) ?>"
                    autocomplete="off"
                >
            </div>

            <div class="admin-form-group mb-0 min-w-140">
                <label class="admin-form-label">Nationalitet</label>
                <select name="nationality" class="admin-form-select" onchange="this.form.submit()">
                    <option value="">Alla länder</option>
                    <?php foreach ($nationalities as $nat): ?>
                    <option value="<?= h($nat['nationality']) ?>" <?= $nationality === $nat['nationality'] ? 'selected' : '' ?>>
                        <?= h($nationalityNames[$nat['nationality']] ?? $nat['nationality']) ?> (<?= $nat['count'] ?>)
                    </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="admin-form-group mb-0">
                <label class="admin-checkbox-label">
                    <input type="checkbox" name="with_results" value="1" <?= $onlyWithResults ? 'checked' : '' ?> onchange="this.form.submit()">
                    <span>Endast med resultat</span>
                </label>
            </div>

            <div class="admin-form-group mb-0">
                <label class="admin-checkbox-label">
                    <input type="checkbox" name="swe_only" value="1" <?= $onlySweId ? 'checked' : '' ?> onchange="this.form.submit()">
                    <span>Endast SWE-ID</span>
                </label>
            </div>

            <div class="admin-form-group mb-0">
                <label class="admin-checkbox-label">
                    <input type="checkbox" name="activated" value="1" <?= $onlyActivated ? 'checked' : '' ?> onchange="this.form.submit()">
                    <span>Aktiverade konton</span>
                </label>
            </div>

            <div class="admin-form-group mb-0">
                <label class="admin-checkbox-label">
                    <input type="checkbox" name="licensed_2026" value="1" <?= $onlyLicensed2026 ? 'checked' : '' ?> onchange="this.form.submit()">
                    <span>Aktiv licens (<?= date('Y') ?>)</span>
                </label>
            </div>

            <div class="admin-form-group mb-0 min-w-140">
                <label class="admin-form-label">E-post</label>
                <select name="has_email" class="admin-form-select" onchange="this.form.submit()">
                    <option value="">Alla</option>
                    <option value="1" <?= $hasEmail === '1' ? 'selected' : '' ?>>Med e-post</option>
                    <option value="0" <?= $hasEmail === '0' ? 'selected' : '' ?>>Utan e-post</option>
                </select>
            </div>

            <?php if ($search || $nationality || $onlyWithResults || $onlySweId || $onlyActivated || $onlyLicensed2026 || $hasEmail !== null): ?>
                <a href="/admin/riders<?= $club_id ? '?club_id=' . $club_id : '' ?>" class="btn-admin btn-admin-sm btn-admin-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                    Rensa
                </a>
            <?php endif; ?>
        </form>
    </div>
</div>

<!-- Riders Table -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><?= count($riders) ?> deltagare</h2>
    </div>
    <div class="admin-card-body p-0">
        <?php if (empty($riders)): ?>
            <div class="admin-empty-state">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                <h3>Inga deltagare hittades</h3>
                <p>Prova att ändra sökning eller filter.</p>
            </div>
        <?php else: ?>
            <!-- Merge toolbar (hidden until 2+ selected) -->
            <div id="mergeToolbar" style="display: none; padding: var(--space-md); background: var(--color-accent-light); border-bottom: 1px solid var(--color-border);">
                <form method="POST" id="mergeForm" style="display: flex; align-items: center; gap: var(--space-md); flex-wrap: wrap;">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="merge">
                    <input type="hidden" name="keep_id" id="keepId">
                    <div id="mergeIdsContainer"></div>
                    <span><strong id="selectedCount">0</strong> deltagare valda</span>
                    <div style="flex: 1; display: flex; align-items: center; gap: var(--space-sm);">
                        <label style="white-space: nowrap;">Behåll:</label>
                        <select id="keepSelect" class="form-select form-select-sm" style="min-width: 250px;"></select>
                    </div>
                    <span id="mergePreview" style="color: var(--color-text-secondary); font-size: 0.9em;"></span>
                    <button type="submit" class="btn btn--primary btn-sm">
                        <i data-lucide="git-merge"></i> Slå samman
                    </button>
                    <button type="button" class="btn btn--secondary btn-sm" onclick="clearRiderSelection()">Avbryt</button>
                </form>
            </div>

            <div class="admin-table-container">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th style="width: 40px;"><input type="checkbox" id="selectAllRiders" title="Markera alla"></th>
                            <th>
                                <a href="<?= buildSortUrl('name', $sortBy, $sortOrder, $search, $club_id, $nationality, $onlyWithResults, $onlySweId, $onlyActivated, $onlyLicensed2026, $hasEmail) ?>" class="admin-sortable">
                                    Namn
                                    <?php if ($sortBy === 'name'): ?>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs">
                                            <?php if ($sortOrder === 'asc'): ?>
                                                <path d="m18 15-6-6-6 6"/>
                                            <?php else: ?>
                                                <path d="m6 9 6 6 6-6"/>
                                            <?php endif; ?>
                                        </svg>
                                    <?php endif; ?>
                                </a>
                            </th>
                            <th>
                                <a href="<?= buildSortUrl('nationality', $sortBy, $sortOrder, $search, $club_id, $nationality, $onlyWithResults, $onlySweId, $onlyActivated, $onlyLicensed2026, $hasEmail) ?>" class="admin-sortable">
                                    Land
                                    <?php if ($sortBy === 'nationality'): ?>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs">
                                            <?php if ($sortOrder === 'asc'): ?>
                                                <path d="m18 15-6-6-6 6"/>
                                            <?php else: ?>
                                                <path d="m6 9 6 6 6-6"/>
                                            <?php endif; ?>
                                        </svg>
                                    <?php endif; ?>
                                </a>
                            </th>
                            <th>
                                <a href="<?= buildSortUrl('year', $sortBy, $sortOrder, $search, $club_id, $nationality, $onlyWithResults, $onlySweId, $onlyActivated, $onlyLicensed2026, $hasEmail) ?>" class="admin-sortable">
                                    År
                                    <?php if ($sortBy === 'year'): ?>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs">
                                            <?php if ($sortOrder === 'asc'): ?>
                                                <path d="m18 15-6-6-6 6"/>
                                            <?php else: ?>
                                                <path d="m6 9 6 6 6-6"/>
                                            <?php endif; ?>
                                        </svg>
                                    <?php endif; ?>
                                </a>
                            </th>
                            <th>
                                <a href="<?= buildSortUrl('club', $sortBy, $sortOrder, $search, $club_id, $nationality, $onlyWithResults, $onlySweId, $onlyActivated, $onlyLicensed2026, $hasEmail) ?>" class="admin-sortable">
                                    Klubb
                                    <?php if ($sortBy === 'club'): ?>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs">
                                            <?php if ($sortOrder === 'asc'): ?>
                                                <path d="m18 15-6-6-6 6"/>
                                            <?php else: ?>
                                                <path d="m6 9 6 6 6-6"/>
                                            <?php endif; ?>
                                        </svg>
                                    <?php endif; ?>
                                </a>
                            </th>
                            <th>
                                <a href="<?= buildSortUrl('license', $sortBy, $sortOrder, $search, $club_id, $nationality, $onlyWithResults, $onlySweId, $onlyActivated, $onlyLicensed2026, $hasEmail) ?>" class="admin-sortable">
                                    Licensnummer
                                    <?php if ($sortBy === 'license'): ?>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs">
                                            <?php if ($sortOrder === 'asc'): ?>
                                                <path d="m18 15-6-6-6 6"/>
                                            <?php else: ?>
                                                <path d="m6 9 6 6 6-6"/>
                                            <?php endif; ?>
                                        </svg>
                                    <?php endif; ?>
                                </a>
                            </th>
                            <th>
                                <a href="<?= buildSortUrl('results', $sortBy, $sortOrder, $search, $club_id, $nationality, $onlyWithResults, $onlySweId, $onlyActivated, $onlyLicensed2026, $hasEmail) ?>" class="admin-sortable">
                                    Resultat
                                    <?php if ($sortBy === 'results'): ?>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs">
                                            <?php if ($sortOrder === 'asc'): ?>
                                                <path d="m18 15-6-6-6 6"/>
                                            <?php else: ?>
                                                <path d="m6 9 6 6 6-6"/>
                                            <?php endif; ?>
                                        </svg>
                                    <?php endif; ?>
                                </a>
                            </th>
                            <th>Licensstatus</th>
                            <th>Disciplin</th>
                            <th style="width: 100px;">Åtgärder</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($riders as $rider): ?>
                            <?php
                            // Check license status - three states:
                            // 1. SWE-ID (yellow) - Generated SWE ID, no real UCI ID
                            // 2. Ej aktiv (red) - Has UCI ID but not verified for current year
                            // 3. Aktiv (green) - Has UCI ID and verified for current year
                            $currentYear = (int)date('Y');
                            $licenseStatusMessage = '-';
                            $licenseStatusClass = 'admin-badge-secondary';

                            if (!empty($rider['license_number'])) {
                                if (strpos($rider['license_number'], 'SWE') === 0) {
                                    // Generated SWE-ID (no real UCI ID)
                                    $licenseStatusMessage = 'SWE-ID';
                                    $licenseStatusClass = 'admin-badge-warning';
                                } else {
                                    // Has real UCI ID - check if verified this year
                                    if (!empty($rider['scf_license_year']) && (int)$rider['scf_license_year'] === $currentYear) {
                                        // Verified for current year
                                        $licenseStatusMessage = 'Aktiv';
                                        $licenseStatusClass = 'admin-badge-success';
                                    } else {
                                        // Has UCI ID but not verified
                                        $licenseStatusMessage = 'Ej aktiv';
                                        $licenseStatusClass = 'admin-badge-error';
                                    }
                                }
                            }
                            ?>
                            <tr>
                                <td>
                                    <input type="checkbox" class="rider-checkbox"
                                           data-id="<?= $rider['id'] ?>"
                                           data-name="<?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>"
                                           data-results="<?= $rider['result_count'] ?>"
                                           data-license="<?= htmlspecialchars($rider['license_number'] ?? '') ?>">
                                </td>
                                <td>
                                    <a href="/rider/<?= $rider['id'] ?>" class="color-accent no-underline font-medium">
                                        <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                                    </a>
                                </td>
                                <td>
                                    <?php if ($rider['nationality']): ?>
                                        <span class="admin-badge" title="<?= h($nationalityNames[$rider['nationality']] ?? $rider['nationality']) ?>">
                                            <?= h($rider['nationality']) ?>
                                        </span>
                                    <?php else: ?>
                                        -
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($rider['birth_year']): ?>
                                        <strong><?= $rider['birth_year'] ?></strong>
                                        <span class="text-secondary text-xs"> (<?= calculateAge($rider['birth_year']) ?> år)</span>
                                    <?php else: ?>
                                        -
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($rider['club_name']): ?>
                                        <?php if ($club_id): ?>
                                            <?= htmlspecialchars($rider['club_name']) ?>
                                        <?php else: ?>
                                            <a href="/admin/riders?club_id=<?= $rider['club_id'] ?>" class="color-accent no-underline">
                                                <?= htmlspecialchars($rider['club_name']) ?>
                                            </a>
                                        <?php endif; ?>
                                    <?php else: ?>
                                        -
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($rider['license_number']): ?>
                                        <span class="admin-badge <?= strpos($rider['license_number'], 'SWE') === 0 ? 'admin-badge-warning' : 'admin-badge-info' ?>">
                                            <?= htmlspecialchars($rider['license_number']) ?>
                                        </span>
                                    <?php else: ?>
                                        -
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($rider['result_count'] > 0): ?>
                                        <span class="admin-badge admin-badge-info"><?= $rider['result_count'] ?></span>
                                    <?php else: ?>
                                        <span class="text-secondary">0</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <span class="admin-badge <?= $licenseStatusClass ?>">
                                        <?= $licenseStatusMessage ?>
                                    </span>
                                </td>
                                <td>
                                    <?php if ($rider['discipline']): ?>
                                        <span class="admin-badge"><?= htmlspecialchars($rider['discipline']) ?></span>
                                    <?php else: ?>
                                        -
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <div class="table-actions">
                                        <a href="/admin/riders/edit/<?= $rider['id'] ?>" class="btn-admin btn-admin-sm btn-admin-secondary" title="Redigera">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>
                                        </a>
                                        <button onclick="deleteRider(<?= $rider['id'] ?>, '<?= addslashes($rider['firstname'] . ' ' . $rider['lastname']) ?>')" class="btn-admin btn-admin-sm btn-admin-danger" title="Ta bort">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endif; ?>
    </div>
</div>

<script>
// Store CSRF token from PHP session
const csrfToken = '<?= htmlspecialchars(generate_csrf_token()) ?>';

function deleteRider(id, name) {
    if (!confirm('Är du säker på att du vill ta bort "' + name + '"?')) {
        return;
    }

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/admin/rider-delete.php';
    form.innerHTML = '<input type="hidden" name="id" value="' + id + '">' +
                     '<input type="hidden" name="csrf_token" value="' + csrfToken + '">';
    document.body.appendChild(form);
    form.submit();
}

// Live search with debouncing
(function() {
    const searchInput = document.getElementById('searchInput');
    const searchForm = document.getElementById('searchForm');
    let debounceTimer;
    let lastSearch = searchInput.value;

    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        clearTimeout(debounceTimer);

        if (query === lastSearch) return;

        debounceTimer = setTimeout(function() {
            if (query.length >= 3 || query.length === 0) {
                lastSearch = query;
                searchForm.submit();
            }
        }, 600);
    });

    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            clearTimeout(debounceTimer);
            searchForm.submit();
        }
    });

    if (searchInput.value) {
        searchInput.focus();
        searchInput.setSelectionRange(searchInput.value.length, searchInput.value.length);
    }
})();

// Rider merge functionality
let selectedRiders = [];

document.querySelectorAll('.rider-checkbox').forEach(cb => {
    cb.addEventListener('change', updateMergeToolbar);
});

document.getElementById('selectAllRiders')?.addEventListener('change', function() {
    document.querySelectorAll('.rider-checkbox').forEach(cb => {
        cb.checked = this.checked;
    });
    updateMergeToolbar();
});

function updateMergeToolbar() {
    selectedRiders = [];
    document.querySelectorAll('.rider-checkbox:checked').forEach(cb => {
        selectedRiders.push({
            id: cb.dataset.id,
            name: cb.dataset.name,
            results: parseInt(cb.dataset.results) || 0,
            license: cb.dataset.license || ''
        });
    });

    // Sort by results (most results first) for default keep selection
    // Then prefer real UCI-ID (not SWE-ID) over temporary IDs
    selectedRiders.sort((a, b) => {
        // First: prefer real UCI-ID (not starting with SWE)
        const aIsReal = a.license && !a.license.startsWith('SWE');
        const bIsReal = b.license && !b.license.startsWith('SWE');
        if (aIsReal && !bIsReal) return -1;
        if (!aIsReal && bIsReal) return 1;
        // Then by results
        return b.results - a.results;
    });

    const toolbar = document.getElementById('mergeToolbar');
    const countEl = document.getElementById('selectedCount');
    const keepSelect = document.getElementById('keepSelect');

    countEl.textContent = selectedRiders.length;

    if (selectedRiders.length >= 2) {
        toolbar.style.display = 'block';

        // Build keep dropdown
        keepSelect.innerHTML = selectedRiders.map(r =>
            `<option value="${r.id}">${r.name} (${r.results} res., ${r.license || 'ingen licens'})</option>`
        ).join('');

        // Set default keep (best candidate)
        keepSelect.value = selectedRiders[0].id;
        document.getElementById('keepId').value = selectedRiders[0].id;

        updateMergePreview();
    } else {
        toolbar.style.display = 'none';
    }

    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function updateMergePreview() {
    const keepId = document.getElementById('keepSelect').value;
    const keepRider = selectedRiders.find(r => r.id === keepId);
    const mergeRiders = selectedRiders.filter(r => r.id !== keepId);

    document.getElementById('keepId').value = keepId;

    // Update hidden merge_ids inputs
    const container = document.getElementById('mergeIdsContainer');
    container.innerHTML = mergeRiders.map(r =>
        `<input type="hidden" name="merge_ids[]" value="${r.id}">`
    ).join('');

    // Update preview text
    const previewEl = document.getElementById('mergePreview');
    if (mergeRiders.length === 1) {
        previewEl.innerHTML = `"${mergeRiders[0].name}" → "${keepRider.name}"`;
    } else {
        previewEl.innerHTML = `${mergeRiders.length} deltagare → "${keepRider.name}"`;
    }
}

// Listen for keep selection changes
document.getElementById('keepSelect')?.addEventListener('change', updateMergePreview);

function clearRiderSelection() {
    document.querySelectorAll('.rider-checkbox').forEach(cb => cb.checked = false);
    const selectAll = document.getElementById('selectAllRiders');
    if (selectAll) selectAll.checked = false;
    selectedRiders = [];
    document.getElementById('mergeToolbar').style.display = 'none';
}

document.getElementById('mergeForm')?.addEventListener('submit', function(e) {
    if (selectedRiders.length < 2) {
        e.preventDefault();
        alert('Välj minst 2 deltagare för att slå samman.');
        return;
    }

    const keepId = document.getElementById('keepSelect').value;
    const keepRider = selectedRiders.find(r => r.id === keepId);
    const mergeRiders = selectedRiders.filter(r => r.id !== keepId);
    const mergeNames = mergeRiders.map(r => r.name).join(', ');

    let msg;
    if (mergeRiders.length === 1) {
        msg = `Slå samman "${mergeRiders[0].name}" med "${keepRider.name}"?\n\nAlla resultat och data flyttas till "${keepRider.name}".`;
    } else {
        msg = `Slå samman ${mergeRiders.length} deltagare med "${keepRider.name}"?\n\nDeltagare som tas bort:\n${mergeNames}\n\nAlla resultat och data flyttas till "${keepRider.name}".`;
    }

    if (!confirm(msg)) {
        e.preventDefault();
    }
});
</script>

<style>
.admin-sortable {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
    color: inherit;
    text-decoration: none;
}

.admin-sortable:hover {
    color: var(--color-accent);
}

.admin-checkbox-label {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    cursor: pointer;
    font-size: var(--text-sm);
    white-space: nowrap;
}

.admin-checkbox-label input[type="checkbox"] {
    width: 16px;
    height: 16px;
    accent-color: var(--color-accent);
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
