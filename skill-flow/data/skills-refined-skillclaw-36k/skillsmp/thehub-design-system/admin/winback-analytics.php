<?php
/**
 * Win-Back Analytics
 * Shows participant data for win-back campaigns:
 * - Churned participants (competed before but not this year)
 * - Active participants (competed this year)
 * - Demographics and trends
 *
 * @package TheHUB Analytics
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_once __DIR__ . '/../analytics/includes/KPICalculator.php';
requireLogin();

global $pdo;

// Get current user info
$currentUser = getCurrentAdmin();
$isAdmin = hasRole('admin');

// Get available brands using KPICalculator (same as dashboard)
$brands = [];
try {
    $kpiCalc = new KPICalculator($pdo);
    $brands = $kpiCalc->getAllBrands();
} catch (Exception $e) {
    error_log("Win-Back Analytics brand error: " . $e->getMessage());
}

// Parameters
$selectedBrands = isset($_GET['brands']) ? array_map('intval', (array)$_GET['brands']) : [];
$targetYear = isset($_GET['target_year']) ? (int)$_GET['target_year'] : (int)date('Y');
$startYear = isset($_GET['start_year']) ? (int)$_GET['start_year'] : 2016;
$endYear = isset($_GET['end_year']) ? (int)$_GET['end_year'] : ($targetYear - 1);
$audienceType = $_GET['audience'] ?? 'churned';

// Validate
if ($startYear < 2010) $startYear = 2016;
if ($endYear > $targetYear) $endYear = $targetYear - 1;
if (!in_array($audienceType, ['churned', 'active', 'all'])) $audienceType = 'churned';

// Initialize stats
$stats = [
    'total_churned' => 0,
    'total_active' => 0,
    'churned_with_email' => 0,
    'active_with_email' => 0,
    'by_experience' => [],
    'by_age' => [],
    'by_gender' => [],
    'trend_by_year' => []
];

$participants = [];

try {
    // Build brand filter - series has brand_id that links directly to series_brands
    $brandFilter = '';
    $brandParams = [];
    if (!empty($selectedBrands)) {
        $placeholders = implode(',', array_fill(0, count($selectedBrands), '?'));
        $brandFilter = "AND s.brand_id IN ($placeholders)";
        $brandParams = $selectedBrands;
    }

    // Get churned participants (competed in start_year-end_year but NOT in target_year)
    $churnedSql = "
        SELECT DISTINCT r.id, r.firstname, r.lastname, r.email, r.birth_year, r.gender,
               c.name as club_name,
               COUNT(DISTINCT YEAR(e.date)) as seasons_competed,
               MAX(YEAR(e.date)) as last_season,
               (SELECT COUNT(*) FROM results res2
                JOIN events e2 ON res2.event_id = e2.id
                WHERE res2.cyclist_id = r.id) as total_results
        FROM riders r
        JOIN results res ON res.cyclist_id = r.id
        JOIN events e ON res.event_id = e.id
        JOIN series s ON e.series_id = s.id
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE YEAR(e.date) BETWEEN ? AND ?
        $brandFilter
        AND r.id NOT IN (
            SELECT DISTINCT res2.cyclist_id
            FROM results res2
            JOIN events e2 ON res2.event_id = e2.id
            JOIN series s2 ON e2.series_id = s2.id
            WHERE YEAR(e2.date) = ?
            " . (!empty($selectedBrands) ? "AND s2.brand_id IN ($placeholders)" : "") . "
        )
        GROUP BY r.id
        ORDER BY last_season DESC, total_results DESC
    ";

    $churnedParams = array_merge([$startYear, $endYear], $brandParams, [$targetYear], $brandParams);
    $stmt = $pdo->prepare($churnedSql);
    $stmt->execute($churnedParams);
    $churnedParticipants = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Get active participants (competed in target_year)
    $activeSql = "
        SELECT DISTINCT r.id, r.firstname, r.lastname, r.email, r.birth_year, r.gender,
               c.name as club_name,
               COUNT(DISTINCT YEAR(e.date)) as seasons_competed,
               MAX(YEAR(e.date)) as last_season,
               (SELECT COUNT(*) FROM results res2
                JOIN events e2 ON res2.event_id = e2.id
                WHERE res2.cyclist_id = r.id AND YEAR(e2.date) = ?) as results_this_year
        FROM riders r
        JOIN results res ON res.cyclist_id = r.id
        JOIN events e ON res.event_id = e.id
        JOIN series s ON e.series_id = s.id
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE YEAR(e.date) = ?
        $brandFilter
        GROUP BY r.id
        ORDER BY results_this_year DESC, seasons_competed DESC
    ";

    $activeParams = array_merge([$targetYear, $targetYear], $brandParams);
    $stmt = $pdo->prepare($activeSql);
    $stmt->execute($activeParams);
    $activeParticipants = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Calculate stats
    $stats['total_churned'] = count($churnedParticipants);
    $stats['total_active'] = count($activeParticipants);
    $stats['churned_with_email'] = count(array_filter($churnedParticipants, fn($p) => !empty($p['email'])));
    $stats['active_with_email'] = count(array_filter($activeParticipants, fn($p) => !empty($p['email'])));

    // Experience breakdown (churned only)
    $expGroups = ['1-2 ar' => 0, '3-5 ar' => 0, '6+ ar' => 0];
    foreach ($churnedParticipants as $p) {
        $seasons = (int)$p['seasons_competed'];
        if ($seasons <= 2) $expGroups['1-2 ar']++;
        elseif ($seasons <= 5) $expGroups['3-5 ar']++;
        else $expGroups['6+ ar']++;
    }
    $stats['by_experience'] = $expGroups;

    // Age breakdown (churned only)
    $currentYear = (int)date('Y');
    $ageGroups = ['Under 18' => 0, '18-25' => 0, '26-35' => 0, '36-45' => 0, '46+' => 0, 'Okand' => 0];
    foreach ($churnedParticipants as $p) {
        if (empty($p['birth_year'])) {
            $ageGroups['Okand']++;
        } else {
            $age = $currentYear - (int)$p['birth_year'];
            if ($age < 18) $ageGroups['Under 18']++;
            elseif ($age <= 25) $ageGroups['18-25']++;
            elseif ($age <= 35) $ageGroups['26-35']++;
            elseif ($age <= 45) $ageGroups['36-45']++;
            else $ageGroups['46+']++;
        }
    }
    $stats['by_age'] = $ageGroups;

    // Gender breakdown
    $genderGroups = ['Man' => 0, 'Kvinna' => 0, 'Okant' => 0];
    foreach ($churnedParticipants as $p) {
        $g = strtoupper($p['gender'] ?? '');
        if ($g === 'M') $genderGroups['Man']++;
        elseif ($g === 'F' || $g === 'K') $genderGroups['Kvinna']++;
        else $genderGroups['Okant']++;
    }
    $stats['by_gender'] = $genderGroups;

    // Last active year trend
    $yearTrend = [];
    foreach ($churnedParticipants as $p) {
        $year = (int)$p['last_season'];
        if (!isset($yearTrend[$year])) $yearTrend[$year] = 0;
        $yearTrend[$year]++;
    }
    krsort($yearTrend);
    $stats['trend_by_year'] = $yearTrend;

    // Set participants based on audience type
    if ($audienceType === 'churned') {
        $participants = $churnedParticipants;
    } elseif ($audienceType === 'active') {
        $participants = $activeParticipants;
    } else {
        $participants = array_merge($churnedParticipants, $activeParticipants);
    }

} catch (Exception $e) {
    $error = $e->getMessage();
}

// Page config
$page_title = 'Win-Back Analytics';
$breadcrumbs = [
    ['label' => 'Dashboard', 'url' => '/admin/dashboard.php'],
    ['label' => 'Analytics', 'url' => '/admin/analytics-dashboard.php'],
    ['label' => 'Win-Back']
];

$page_actions = '
<a href="/admin/winback-campaigns.php" class="btn-admin btn-admin-primary">
    <i data-lucide="mail"></i> Kampanjer
</a>
';

include __DIR__ . '/components/unified-layout.php';
?>

<style>
/* Ensure icons render correctly */
[data-lucide] {
    width: 18px;
    height: 18px;
    stroke-width: 2;
}
.stat-card [data-lucide],
.analytics-card-header [data-lucide] {
    width: 20px;
    height: 20px;
}

.winback-filters {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-md);
    align-items: flex-end;
    margin-bottom: var(--space-xl);
    padding: var(--space-lg);
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
}
.winback-filters .form-group {
    flex: 1;
    min-width: 120px;
}

/* Brand Checkboxes */
.brand-checkboxes {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-xs);
}
.brand-checkbox {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-xs) var(--space-sm);
    background: var(--color-bg-page);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.15s;
    font-size: 0.875rem;
}
.brand-checkbox:hover {
    border-color: var(--brand-color, var(--color-accent));
    background: var(--color-bg-hover);
}
.brand-checkbox.checked,
.brand-checkbox:has(input:checked) {
    background: var(--color-accent-light);
    border-color: var(--brand-color, var(--color-accent));
}
.brand-checkbox input {
    width: 16px;
    height: 16px;
    accent-color: var(--brand-color, var(--color-accent));
}
.brand-checkbox .brand-name {
    color: var(--color-text-primary);
}
.brand-checkbox .brand-code {
    font-size: 0.7rem;
    color: var(--color-text-muted);
    background: var(--color-bg-surface);
    padding: 1px 4px;
    border-radius: var(--radius-sm);
}

.stats-overview {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
}
.stat-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    text-align: center;
}
.stat-card.highlight {
    border-left: 4px solid var(--color-accent);
}
.stat-card .stat-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--color-accent);
    line-height: 1;
}
.stat-card .stat-label {
    font-size: 0.875rem;
    color: var(--color-text-muted);
    margin-top: var(--space-xs);
}
.stat-card .stat-sub {
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    margin-top: var(--space-2xs);
}

.analytics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--space-lg);
    margin-bottom: var(--space-xl);
}
.analytics-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    overflow: hidden;
}
.analytics-card-header {
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
    background: var(--color-bg-page);
}
.analytics-card-header h3 {
    margin: 0;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}
.analytics-card-body {
    padding: var(--space-lg);
}

.bar-chart {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}
.bar-row {
    display: flex;
    align-items: center;
    gap: var(--space-md);
}
.bar-label {
    flex: 0 0 80px;
    font-size: 0.875rem;
    color: var(--color-text-secondary);
}
.bar-track {
    flex: 1;
    height: 28px;
    background: var(--color-bg-page);
    border-radius: var(--radius-sm);
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--color-accent), var(--color-accent-hover));
    border-radius: var(--radius-sm);
    transition: width 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: var(--space-sm);
}
.bar-fill span {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--color-bg-page);
}
.bar-value {
    flex: 0 0 60px;
    text-align: right;
    font-weight: 600;
    font-size: 0.875rem;
}

.year-pills {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-xs);
}
.year-pill {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-xs) var(--space-sm);
    background: var(--color-bg-page);
    border-radius: var(--radius-full);
    font-size: 0.875rem;
}
.year-pill .year {
    font-weight: 600;
}
.year-pill .count {
    background: var(--color-accent);
    color: var(--color-bg-page);
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: 0.75rem;
    font-weight: 600;
}

.audience-tabs {
    display: flex;
    gap: var(--space-xs);
    margin-bottom: var(--space-lg);
    border-bottom: 2px solid var(--color-border);
}
.audience-tab {
    padding: var(--space-sm) var(--space-lg);
    color: var(--color-text-secondary);
    text-decoration: none;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.15s;
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}
.audience-tab:hover { color: var(--color-text-primary); }
.audience-tab.active {
    color: var(--color-accent);
    border-bottom-color: var(--color-accent);
}
.audience-tab .count {
    background: var(--color-bg-page);
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: 0.75rem;
}
.audience-tab.active .count {
    background: var(--color-accent-light);
}

.participants-table {
    width: 100%;
    border-collapse: collapse;
}
.participants-table th,
.participants-table td {
    padding: var(--space-sm) var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}
.participants-table th {
    background: var(--color-bg-page);
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    color: var(--color-text-muted);
}
.participants-table tbody tr:hover {
    background: var(--color-bg-hover);
}
.participants-table .name-cell a {
    color: var(--color-text-primary);
    text-decoration: none;
    font-weight: 500;
}
.participants-table .name-cell a:hover {
    color: var(--color-accent);
}
.participants-table .email-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 6px;
    background: var(--color-success);
    color: white;
    border-radius: var(--radius-sm);
    font-size: 0.7rem;
}
.participants-table .no-email {
    color: var(--color-text-muted);
    font-size: 0.75rem;
}

/* Mobile */
@media (max-width: 767px) {
    .winback-filters {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
    }
    .stats-overview {
        grid-template-columns: repeat(2, 1fr);
        gap: var(--space-sm);
    }
    .stat-card {
        padding: var(--space-md);
    }
    .stat-card .stat-value {
        font-size: 1.75rem;
    }
    .analytics-card {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
    }
    .bar-label {
        flex: 0 0 60px;
        font-size: 0.75rem;
    }
    .audience-tabs {
        margin-left: -16px;
        margin-right: -16px;
        padding: 0 var(--space-md);
        overflow-x: auto;
    }
    .audience-tab {
        padding: var(--space-sm);
        white-space: nowrap;
        font-size: 0.875rem;
    }
    .admin-table-container {
        margin-left: -16px;
        margin-right: -16px;
        overflow-x: auto;
    }
}
</style>

<!-- Filters -->
<form method="GET" class="winback-filters">
    <!-- Brand Checkboxes -->
    <div class="form-group" style="flex:0 0 100%;margin-bottom:var(--space-md);">
        <label class="form-label" style="margin-bottom:var(--space-sm);">Valj varumarken (<?= count($brands) ?> st)</label>
        <div class="brand-checkboxes">
            <?php if (empty($brands)): ?>
            <p style="color:var(--color-text-muted);font-size:0.875rem;">Inga varumarken hittades i databasen.</p>
            <?php else: ?>
            <?php foreach ($brands as $b): ?>
            <label class="brand-checkbox <?= in_array($b['id'], $selectedBrands) ? 'checked' : '' ?>"
                   style="<?= !empty($b['accent_color']) ? '--brand-color:' . htmlspecialchars($b['accent_color']) : '' ?>">
                <input type="checkbox" name="brands[]" value="<?= $b['id'] ?>"
                       <?= in_array($b['id'], $selectedBrands) ? 'checked' : '' ?>>
                <span class="brand-name"><?= htmlspecialchars($b['name']) ?></span>
            </label>
            <?php endforeach; ?>
            <?php endif; ?>
        </div>
    </div>

    <!-- Year Filters -->
    <div class="form-group">
        <label class="form-label">Aktiv fran</label>
        <select name="start_year" class="form-select">
            <?php for ($y = 2010; $y <= (int)date('Y'); $y++): ?>
            <option value="<?= $y ?>" <?= $y == $startYear ? 'selected' : '' ?>><?= $y ?></option>
            <?php endfor; ?>
        </select>
    </div>

    <div class="form-group">
        <label class="form-label">Till</label>
        <select name="end_year" class="form-select">
            <?php for ($y = 2010; $y <= (int)date('Y'); $y++): ?>
            <option value="<?= $y ?>" <?= $y == $endYear ? 'selected' : '' ?>><?= $y ?></option>
            <?php endfor; ?>
        </select>
    </div>

    <div class="form-group">
        <label class="form-label">Malar</label>
        <select name="target_year" class="form-select">
            <?php for ($y = (int)date('Y'); $y >= 2015; $y--): ?>
            <option value="<?= $y ?>" <?= $y == $targetYear ? 'selected' : '' ?>><?= $y ?></option>
            <?php endfor; ?>
        </select>
    </div>

    <div class="form-group" style="flex:0;">
        <button type="submit" class="btn-admin btn-admin-primary">
            <i data-lucide="filter"></i> Filtrera
        </button>
    </div>
</form>

<!-- Stats Overview -->
<div class="stats-overview">
    <div class="stat-card highlight">
        <div class="stat-value"><?= number_format($stats['total_churned']) ?></div>
        <div class="stat-label">Churned (ej <?= $targetYear ?>)</div>
        <div class="stat-sub"><?= $stats['churned_with_email'] ?> med e-post (<?= $stats['total_churned'] > 0 ? round($stats['churned_with_email'] / $stats['total_churned'] * 100) : 0 ?>%)</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= number_format($stats['total_active']) ?></div>
        <div class="stat-label">Aktiva <?= $targetYear ?></div>
        <div class="stat-sub"><?= $stats['active_with_email'] ?> med e-post (<?= $stats['total_active'] > 0 ? round($stats['active_with_email'] / $stats['total_active'] * 100) : 0 ?>%)</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= $stats['total_churned'] > 0 && $stats['total_active'] > 0 ? round($stats['total_churned'] / $stats['total_active'] * 100) : 0 ?>%</div>
        <div class="stat-label">Churn Ratio</div>
        <div class="stat-sub">Churned / Aktiva</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= $stats['churned_with_email'] ?></div>
        <div class="stat-label">Kontaktbara</div>
        <div class="stat-sub">Churned med e-post</div>
    </div>
</div>

<!-- Analytics Cards -->
<div class="analytics-grid">
    <!-- Experience Breakdown -->
    <div class="analytics-card">
        <div class="analytics-card-header">
            <h3><i data-lucide="award"></i> Erfarenhet (Churned)</h3>
        </div>
        <div class="analytics-card-body">
            <div class="bar-chart">
                <?php
                $maxExp = max($stats['by_experience'] ?: [1]);
                foreach ($stats['by_experience'] as $label => $count):
                    $pct = $maxExp > 0 ? ($count / $maxExp) * 100 : 0;
                ?>
                <div class="bar-row">
                    <div class="bar-label"><?= $label ?></div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width:<?= $pct ?>%">
                            <?php if ($pct > 20): ?><span><?= $count ?></span><?php endif; ?>
                        </div>
                    </div>
                    <div class="bar-value"><?= $count ?></div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>

    <!-- Age Breakdown -->
    <div class="analytics-card">
        <div class="analytics-card-header">
            <h3><i data-lucide="users"></i> Aldersfordelning (Churned)</h3>
        </div>
        <div class="analytics-card-body">
            <div class="bar-chart">
                <?php
                $maxAge = max($stats['by_age'] ?: [1]);
                foreach ($stats['by_age'] as $label => $count):
                    if ($count == 0) continue;
                    $pct = $maxAge > 0 ? ($count / $maxAge) * 100 : 0;
                ?>
                <div class="bar-row">
                    <div class="bar-label"><?= $label ?></div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width:<?= $pct ?>%">
                            <?php if ($pct > 20): ?><span><?= $count ?></span><?php endif; ?>
                        </div>
                    </div>
                    <div class="bar-value"><?= $count ?></div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>

    <!-- Gender Breakdown -->
    <div class="analytics-card">
        <div class="analytics-card-header">
            <h3><i data-lucide="user"></i> Kon (Churned)</h3>
        </div>
        <div class="analytics-card-body">
            <div class="bar-chart">
                <?php
                $maxGender = max($stats['by_gender'] ?: [1]);
                foreach ($stats['by_gender'] as $label => $count):
                    if ($count == 0) continue;
                    $pct = $maxGender > 0 ? ($count / $maxGender) * 100 : 0;
                ?>
                <div class="bar-row">
                    <div class="bar-label"><?= $label ?></div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width:<?= $pct ?>%">
                            <?php if ($pct > 20): ?><span><?= $count ?></span><?php endif; ?>
                        </div>
                    </div>
                    <div class="bar-value"><?= $count ?></div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>

    <!-- Last Active Year -->
    <div class="analytics-card">
        <div class="analytics-card-header">
            <h3><i data-lucide="calendar"></i> Senast aktiva ar (Churned)</h3>
        </div>
        <div class="analytics-card-body">
            <div class="year-pills">
                <?php foreach ($stats['trend_by_year'] as $year => $count): ?>
                <div class="year-pill">
                    <span class="year"><?= $year ?></span>
                    <span class="count"><?= $count ?></span>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>
</div>

<!-- Participant List -->
<div class="analytics-card" style="margin-bottom:var(--space-xl);">
    <div class="analytics-card-header">
        <h3><i data-lucide="list"></i> Deltagarlista</h3>
    </div>

    <!-- Audience Tabs -->
    <div class="audience-tabs" style="padding:0 var(--space-lg);margin-top:var(--space-md);">
        <a href="?<?= http_build_query(array_merge($_GET, ['audience' => 'churned'])) ?>"
           class="audience-tab <?= $audienceType === 'churned' ? 'active' : '' ?>">
            Churned <span class="count"><?= number_format($stats['total_churned']) ?></span>
        </a>
        <a href="?<?= http_build_query(array_merge($_GET, ['audience' => 'active'])) ?>"
           class="audience-tab <?= $audienceType === 'active' ? 'active' : '' ?>">
            Aktiva <?= $targetYear ?> <span class="count"><?= number_format($stats['total_active']) ?></span>
        </a>
    </div>

    <div class="admin-table-container">
        <table class="participants-table">
            <thead>
                <tr>
                    <th>Namn</th>
                    <th>Klubb</th>
                    <th>Kontakt</th>
                    <th>Sasonger</th>
                    <th><?= $audienceType === 'active' ? 'Resultat ' . $targetYear : 'Senast aktiv' ?></th>
                </tr>
            </thead>
            <tbody>
                <?php if (empty($participants)): ?>
                <tr>
                    <td colspan="5" style="text-align:center;padding:var(--space-2xl);color:var(--color-text-muted);">
                        Inga deltagare matchar filtret. Valj varumarken och klicka Filtrera.
                    </td>
                </tr>
                <?php else: ?>
                <?php foreach (array_slice($participants, 0, 100) as $p): ?>
                <tr>
                    <td class="name-cell">
                        <a href="/rider/<?= $p['id'] ?>"><?= htmlspecialchars($p['firstname'] . ' ' . $p['lastname']) ?></a>
                    </td>
                    <td><?= $p['club_name'] ? htmlspecialchars($p['club_name']) : '<span style="color:var(--color-text-muted);">-</span>' ?></td>
                    <td>
                        <?php if (!empty($p['email'])): ?>
                        <span class="email-badge"><i data-lucide="mail" style="width:10px;height:10px;"></i> E-post</span>
                        <?php else: ?>
                        <span class="no-email">Saknas</span>
                        <?php endif; ?>
                    </td>
                    <td><?= $p['seasons_competed'] ?> st</td>
                    <td>
                        <?php if ($audienceType === 'active'): ?>
                        <?= $p['results_this_year'] ?? 0 ?> resultat
                        <?php else: ?>
                        <?= $p['last_season'] ?>
                        <?php endif; ?>
                    </td>
                </tr>
                <?php endforeach; ?>
                <?php endif; ?>
            </tbody>
        </table>
        <?php if (count($participants) > 100): ?>
        <div style="padding:var(--space-md);text-align:center;color:var(--color-text-muted);font-size:0.875rem;">
            Visar 100 av <?= number_format(count($participants)) ?> deltagare.
            <a href="/admin/winback-campaigns.php">Skapa kampanj</a> for att exportera alla.
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Action Button -->
<div style="text-align:center;margin-bottom:var(--space-2xl);">
    <a href="/admin/winback-campaigns.php" class="btn-admin btn-admin-primary btn-lg">
        <i data-lucide="mail"></i> Skapa Win-Back Kampanj
    </a>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
