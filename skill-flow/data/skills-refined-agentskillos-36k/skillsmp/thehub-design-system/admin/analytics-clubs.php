<?php
/**
 * Analytics - Klubbanalys
 *
 * Visar statistik per klubb:
 * - Top klubbar efter aktiva riders
 * - Klubbar med flest rookies
 * - Klubbtillvaxt over tid
 *
 * Behorighet: super_admin ELLER statistics-permission
 *
 * @package TheHUB Analytics
 * @version 1.0
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_once __DIR__ . '/../analytics/includes/KPICalculator.php';

// Kraver super_admin eller statistics-behorighet
requireAnalyticsAccess();

global $pdo;

// Arval
$currentYear = (int)date('Y');
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : $currentYear;

// Hamta tillgangliga ar
$availableYears = [];
try {
    $stmt = $pdo->query("SELECT DISTINCT season_year FROM rider_yearly_stats ORDER BY season_year DESC");
    $availableYears = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {
    $availableYears = range($currentYear, $currentYear - 5);
}

// Fallback
if (empty($availableYears)) {
    $availableYears = range($currentYear, $currentYear - 5);
}

// Initiera KPI Calculator
$kpiCalc = new KPICalculator($pdo);

// Hamta data
$topClubs = [];
$clubsWithRookies = [];
$totalClubs = 0;
$selectedClubId = isset($_GET['club']) ? (int)$_GET['club'] : null;
$clubGrowth = [];

try {
    $topClubs = $kpiCalc->getTopClubs($selectedYear, 50);
    $clubsWithRookies = $kpiCalc->getClubsWithMostRookies($selectedYear, 50);

    // Rakna totalt antal klubbar med aktiva riders
    $stmt = $pdo->prepare("
        SELECT COUNT(DISTINCT club_id)
        FROM club_yearly_stats
        WHERE season_year = ? AND active_riders > 0
    ");
    $stmt->execute([$selectedYear]);
    $totalClubs = (int)$stmt->fetchColumn();

    // Om en klubb ar vald, hamta tillvaxt
    if ($selectedClubId) {
        $clubGrowth = $kpiCalc->getClubGrowth($selectedClubId, 5);
    }
} catch (Exception $e) {
    $error = $e->getMessage();
}

// Page config
$page_title = 'Klubbanalys';
$breadcrumbs = [
    ['label' => 'Analytics', 'url' => '/admin/analytics-dashboard.php'],
    ['label' => 'Klubbar']
];

$page_actions = '
<div class="btn-group">
    <a href="/admin/analytics-dashboard.php" class="btn-admin btn-admin-secondary">
        <i data-lucide="layout-dashboard"></i> Dashboard
    </a>
</div>
';

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.dashboard-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
}
.metric-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    display: flex;
    align-items: center;
    gap: var(--space-md);
}
.metric-card--primary .metric-icon {
    background: var(--color-accent-light);
    color: var(--color-accent);
}
.metric-icon {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-bg-hover);
    color: var(--color-text-muted);
    flex-shrink: 0;
}
.metric-icon svg {
    width: 24px;
    height: 24px;
}
.metric-value {
    font-size: 1.75rem;
    font-weight: 700;
    font-family: var(--font-heading);
    color: var(--color-text-primary);
    line-height: 1.2;
}
.metric-label {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}
.club-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: var(--space-lg);
}
@media (max-width: 767px) {
    .club-grid {
        grid-template-columns: 1fr;
    }
}
</style>

<!-- Year Selector -->
<div class="filter-bar">
    <form method="get" class="filter-form">
        <div class="filter-group">
            <label class="filter-label">Sasong</label>
            <select name="year" class="form-select" onchange="this.form.submit()">
                <?php foreach ($availableYears as $year): ?>
                    <option value="<?= $year ?>" <?= $year == $selectedYear ? 'selected' : '' ?>>
                        <?= $year ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
    </form>
</div>

<?php if (isset($error)): ?>
<div class="alert alert-warning">
    <i data-lucide="alert-triangle"></i>
    <div>
        <strong>Ingen data tillganglig</strong><br>
        <small><?= htmlspecialchars($error) ?></small>
    </div>
</div>
<?php else: ?>

<!-- Key Metrics -->
<div class="dashboard-metrics">
    <div class="metric-card metric-card--primary">
        <div class="metric-icon">
            <i data-lucide="building-2"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($totalClubs) ?></div>
            <div class="metric-label">Aktiva klubbar</div>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">
            <i data-lucide="users"></i>
        </div>
        <div class="metric-content">
            <?php
            $totalRiders = 0;
            foreach ($topClubs as $club) {
                $totalRiders += $club['active_riders'];
            }
            ?>
            <div class="metric-value"><?= number_format($totalRiders) ?></div>
            <div class="metric-label">Klubbanslutna riders</div>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">
            <i data-lucide="user-plus"></i>
        </div>
        <div class="metric-content">
            <?php
            $totalRookies = 0;
            foreach ($clubsWithRookies as $club) {
                $totalRookies += $club['rookie_count'];
            }
            ?>
            <div class="metric-value"><?= number_format($totalRookies) ?></div>
            <div class="metric-label">Rookies i klubbar</div>
        </div>
    </div>
</div>

<div class="club-grid">
    <!-- Top Clubs by Active Riders -->
    <div class="card">
        <div class="card-header">
            <h3><i data-lucide="trophy"></i> Top klubbar - Aktiva riders</h3>
        </div>
        <div class="card-body">
            <?php if (!empty($topClubs)): ?>
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Klubb</th>
                            <th>Stad</th>
                            <th class="text-right">Riders</th>
                            <th class="text-right">Poang</th>
                            <th class="text-right">Segrar</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach (array_slice($topClubs, 0, 20) as $i => $club): ?>
                        <tr>
                            <td><?= $i + 1 ?></td>
                            <td>
                                <strong><?= htmlspecialchars($club['club_name']) ?></strong>
                            </td>
                            <td class="text-muted"><?= htmlspecialchars($club['city'] ?? '-') ?></td>
                            <td class="text-right"><?= number_format($club['active_riders']) ?></td>
                            <td class="text-right"><?= number_format($club['total_points']) ?></td>
                            <td class="text-right"><?= number_format($club['wins']) ?></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
            <?php else: ?>
            <p class="text-muted">Ingen klubbdata tillganglig.</p>
            <?php endif; ?>
        </div>
    </div>

    <!-- Clubs with Most Rookies -->
    <div class="card">
        <div class="card-header">
            <h3><i data-lucide="user-plus"></i> Top klubbar - Nya riders</h3>
        </div>
        <div class="card-body">
            <?php if (!empty($clubsWithRookies)): ?>
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Klubb</th>
                            <th>Stad</th>
                            <th class="text-right">Rookies</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach (array_slice($clubsWithRookies, 0, 20) as $i => $club): ?>
                        <tr>
                            <td><?= $i + 1 ?></td>
                            <td>
                                <strong><?= htmlspecialchars($club['club_name']) ?></strong>
                            </td>
                            <td class="text-muted"><?= htmlspecialchars($club['city'] ?? '-') ?></td>
                            <td class="text-right"><?= number_format($club['rookie_count']) ?></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
            <?php else: ?>
            <p class="text-muted">Ingen rookie-data tillganglig.</p>
            <?php endif; ?>
        </div>
    </div>
</div>

<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
