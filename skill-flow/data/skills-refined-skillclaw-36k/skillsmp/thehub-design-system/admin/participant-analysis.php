<?php
/**
 * Participant Analysis Tool
 *
 * Enkel lista over:
 * 1. Deltagare som INTE tavlade 2025 (churned)
 * 2. Deltagare som tavlade 2025 men INTE i SweCup Enduro
 *
 * Syfte: Kontakta och bjuda in till TheHUB for rabattkod 2026
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
requireAdmin();

global $pdo;

// Hamta tillgangliga ar
$availableYears = [];
try {
    $stmt = $pdo->query("SELECT DISTINCT YEAR(date) as year FROM events WHERE date IS NOT NULL ORDER BY year DESC");
    $availableYears = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {
    $availableYears = [2025, 2024, 2023, 2022];
}

// Hamta alla serier for dropdown
$allSeries = [];
try {
    $stmt = $pdo->query("SELECT id, name, year FROM series WHERE active = 1 ORDER BY year DESC, name");
    $allSeries = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {}

// SweCup Enduro har series_id = 9
$swecupEnduroId = 9;

// Parameters
$activeTab = $_GET['tab'] ?? 'churned';
$targetYear = isset($_GET['year']) ? (int)$_GET['year'] : 2025;
$excludeSeriesId = isset($_GET['exclude_series']) ? (int)$_GET['exclude_series'] : $swecupEnduroId;
$minSeasons = isset($_GET['min_seasons']) ? (int)$_GET['min_seasons'] : 1;

// Export CSV
if (isset($_GET['export']) && $_GET['export'] === 'csv') {
    $exportType = $_GET['type'] ?? 'churned';

    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="thehub-' . $exportType . '-' . date('Y-m-d') . '.csv"');
    $output = fopen('php://output', 'w');
    fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF)); // UTF-8 BOM

    if ($exportType === 'churned') {
        // Export churned riders
        fputcsv($output, ['Rider ID', 'Fornamn', 'Efternamn', 'Klubb', 'Senast aktiv', 'Antal sasonger', 'Serier', 'Profil-URL']);

        $sql = "
            SELECT
                r.id,
                r.firstname,
                r.lastname,
                c.name as club_name,
                MAX(YEAR(e.date)) as last_active_year,
                COUNT(DISTINCT YEAR(e.date)) as total_seasons,
                GROUP_CONCAT(DISTINCT s.name ORDER BY s.name SEPARATOR ', ') as series_names
            FROM riders r
            JOIN results res ON r.id = res.cyclist_id
            JOIN events e ON res.event_id = e.id
            LEFT JOIN series s ON e.series_id = s.id
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.id NOT IN (
                SELECT DISTINCT res2.cyclist_id
                FROM results res2
                JOIN events e2 ON res2.event_id = e2.id
                WHERE YEAR(e2.date) = ?
            )
            GROUP BY r.id
            HAVING total_seasons >= ?
            ORDER BY last_active_year DESC, r.lastname, r.firstname
        ";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$targetYear, $minSeasons]);

        while ($row = $stmt->fetch()) {
            fputcsv($output, [
                $row['id'],
                $row['firstname'],
                $row['lastname'],
                $row['club_name'] ?? '',
                $row['last_active_year'],
                $row['total_seasons'],
                $row['series_names'] ?? '',
                'https://thehub.gravityseries.se/rider/' . $row['id']
            ]);
        }
    } else {
        // Export not-in-series riders
        fputcsv($output, ['Rider ID', 'Fornamn', 'Efternamn', 'Klubb', 'Serier 2025', 'Antal starter 2025', 'Profil-URL']);

        $sql = "
            SELECT
                r.id,
                r.firstname,
                r.lastname,
                c.name as club_name,
                GROUP_CONCAT(DISTINCT s.name ORDER BY s.name SEPARATOR ', ') as series_2025,
                COUNT(DISTINCT e.id) as starts_2025
            FROM riders r
            JOIN results res ON r.id = res.cyclist_id
            JOIN events e ON res.event_id = e.id
            LEFT JOIN series s ON e.series_id = s.id
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE YEAR(e.date) = ?
              AND r.id NOT IN (
                SELECT DISTINCT res2.cyclist_id
                FROM results res2
                JOIN events e2 ON res2.event_id = e2.id
                WHERE YEAR(e2.date) = ?
                  AND e2.series_id = ?
              )
            GROUP BY r.id
            ORDER BY c.name, r.lastname, r.firstname
        ";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$targetYear, $targetYear, $excludeSeriesId]);

        while ($row = $stmt->fetch()) {
            fputcsv($output, [
                $row['id'],
                $row['firstname'],
                $row['lastname'],
                $row['club_name'] ?? '',
                $row['series_2025'] ?? '',
                $row['starts_2025'],
                'https://thehub.gravityseries.se/rider/' . $row['id']
            ]);
        }
    }

    fclose($output);
    exit;
}

// Hamta data for churned
$churnedRiders = [];
$churnedStats = ['total' => 0, 'by_year' => []];

if ($activeTab === 'churned') {
    try {
        $sql = "
            SELECT
                r.id,
                r.firstname,
                r.lastname,
                c.name as club_name,
                MAX(YEAR(e.date)) as last_active_year,
                COUNT(DISTINCT YEAR(e.date)) as total_seasons,
                GROUP_CONCAT(DISTINCT s.name ORDER BY s.name SEPARATOR ', ') as series_names
            FROM riders r
            JOIN results res ON r.id = res.cyclist_id
            JOIN events e ON res.event_id = e.id
            LEFT JOIN series s ON e.series_id = s.id
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.id NOT IN (
                SELECT DISTINCT res2.cyclist_id
                FROM results res2
                JOIN events e2 ON res2.event_id = e2.id
                WHERE YEAR(e2.date) = ?
            )
            GROUP BY r.id
            HAVING total_seasons >= ?
            ORDER BY last_active_year DESC, r.lastname, r.firstname
            LIMIT 500
        ";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$targetYear, $minSeasons]);
        $churnedRiders = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Stats
        $sqlStats = "
            SELECT
                MAX(YEAR(e.date)) as last_year,
                COUNT(DISTINCT r.id) as cnt
            FROM riders r
            JOIN results res ON r.id = res.cyclist_id
            JOIN events e ON res.event_id = e.id
            WHERE r.id NOT IN (
                SELECT DISTINCT res2.cyclist_id
                FROM results res2
                JOIN events e2 ON res2.event_id = e2.id
                WHERE YEAR(e2.date) = ?
            )
            GROUP BY r.id
            HAVING COUNT(DISTINCT YEAR(e.date)) >= ?
        ";
        $stmt = $pdo->prepare($sqlStats);
        $stmt->execute([$targetYear, $minSeasons]);
        $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

        foreach ($rows as $row) {
            $churnedStats['total']++;
            $year = $row['last_year'];
            if (!isset($churnedStats['by_year'][$year])) {
                $churnedStats['by_year'][$year] = 0;
            }
            $churnedStats['by_year'][$year]++;
        }
        krsort($churnedStats['by_year']);

    } catch (Exception $e) {
        $error = $e->getMessage();
    }
}

// Hamta data for not-in-series
$notInSeriesRiders = [];
$notInSeriesStats = ['total' => 0];
$excludeSeriesName = '';

if ($activeTab === 'not-in-series' && $excludeSeriesId) {
    try {
        // Hamta serienamn
        $stmt = $pdo->prepare("SELECT name FROM series WHERE id = ?");
        $stmt->execute([$excludeSeriesId]);
        $excludeSeriesName = $stmt->fetchColumn() ?: 'Okand serie';

        $sql = "
            SELECT
                r.id,
                r.firstname,
                r.lastname,
                c.name as club_name,
                GROUP_CONCAT(DISTINCT s.name ORDER BY s.name SEPARATOR ', ') as series_2025,
                COUNT(DISTINCT e.id) as starts_2025
            FROM riders r
            JOIN results res ON r.id = res.cyclist_id
            JOIN events e ON res.event_id = e.id
            LEFT JOIN series s ON e.series_id = s.id
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE YEAR(e.date) = ?
              AND r.id NOT IN (
                SELECT DISTINCT res2.cyclist_id
                FROM results res2
                JOIN events e2 ON res2.event_id = e2.id
                WHERE YEAR(e2.date) = ?
                  AND e2.series_id = ?
              )
            GROUP BY r.id
            ORDER BY c.name, r.lastname, r.firstname
            LIMIT 500
        ";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$targetYear, $targetYear, $excludeSeriesId]);
        $notInSeriesRiders = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Count total
        $sqlCount = "
            SELECT COUNT(DISTINCT r.id)
            FROM riders r
            JOIN results res ON r.id = res.cyclist_id
            JOIN events e ON res.event_id = e.id
            WHERE YEAR(e.date) = ?
              AND r.id NOT IN (
                SELECT DISTINCT res2.cyclist_id
                FROM results res2
                JOIN events e2 ON res2.event_id = e2.id
                WHERE YEAR(e2.date) = ?
                  AND e2.series_id = ?
              )
        ";
        $stmt = $pdo->prepare($sqlCount);
        $stmt->execute([$targetYear, $targetYear, $excludeSeriesId]);
        $notInSeriesStats['total'] = (int)$stmt->fetchColumn();

    } catch (Exception $e) {
        $error = $e->getMessage();
    }
}

// Page setup
$page_title = 'Deltagaranalys';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'Deltagaranalys']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.tabs-nav {
    display: flex;
    gap: var(--space-xs);
    margin-bottom: var(--space-lg);
    border-bottom: 2px solid var(--color-border);
    padding-bottom: var(--space-xs);
}
.tab-btn {
    padding: var(--space-sm) var(--space-lg);
    background: transparent;
    border: none;
    color: var(--color-text-secondary);
    font-weight: var(--weight-medium);
    cursor: pointer;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0;
    transition: all 0.15s ease;
}
.tab-btn:hover {
    color: var(--color-text-primary);
    background: var(--color-bg-hover);
}
.tab-btn.active {
    color: var(--color-accent);
    background: var(--color-accent-light);
    border-bottom: 2px solid var(--color-accent);
    margin-bottom: -2px;
}
.filter-bar {
    display: flex;
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
    padding: var(--space-md);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    flex-wrap: wrap;
    align-items: flex-end;
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
.stats-row {
    display: flex;
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
}
.stat-card {
    padding: var(--space-md) var(--space-lg);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    text-align: center;
    min-width: 120px;
}
.stat-card.primary {
    border-left: 3px solid var(--color-accent);
}
.stat-value {
    font-size: var(--text-2xl);
    font-weight: var(--weight-bold);
    color: var(--color-text-primary);
}
.stat-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}
.result-count {
    margin-bottom: var(--space-md);
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
}
@media (max-width: 767px) {
    .filter-bar {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
        width: calc(100% + 32px);
    }
    .tabs-nav {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    .stats-row {
        overflow-x: auto;
        flex-wrap: nowrap;
        margin-left: -16px;
        margin-right: -16px;
        padding-left: 16px;
        padding-right: 16px;
    }
    .stat-card {
        flex-shrink: 0;
    }
}
</style>

<!-- Tabs -->
<nav class="tabs-nav">
    <a href="?tab=churned&year=<?= $targetYear ?>&min_seasons=<?= $minSeasons ?>"
       class="tab-btn <?= $activeTab === 'churned' ? 'active' : '' ?>">
        <i data-lucide="user-x" style="width:16px;height:16px;vertical-align:middle;margin-right:var(--space-xs);"></i>
        Tavlade inte <?= $targetYear ?>
    </a>
    <a href="?tab=not-in-series&year=<?= $targetYear ?>&exclude_series=<?= $excludeSeriesId ?>"
       class="tab-btn <?= $activeTab === 'not-in-series' ? 'active' : '' ?>">
        <i data-lucide="filter-x" style="width:16px;height:16px;vertical-align:middle;margin-right:var(--space-xs);"></i>
        Ej i vald serie <?= $targetYear ?>
    </a>
</nav>

<?php if ($activeTab === 'churned'): ?>
<!-- ========== CHURNED TAB ========== -->

<div class="filter-bar">
    <form method="get" style="display:flex;gap:var(--space-md);flex-wrap:wrap;align-items:flex-end;">
        <input type="hidden" name="tab" value="churned">

        <div class="filter-group">
            <label class="filter-label">Inte tavlat ar</label>
            <select name="year" class="form-select" onchange="this.form.submit()">
                <?php foreach ($availableYears as $y): ?>
                <option value="<?= $y ?>" <?= $y == $targetYear ? 'selected' : '' ?>><?= $y ?></option>
                <?php endforeach; ?>
            </select>
        </div>

        <div class="filter-group">
            <label class="filter-label">Min antal sasonger</label>
            <select name="min_seasons" class="form-select" onchange="this.form.submit()">
                <option value="1" <?= $minSeasons == 1 ? 'selected' : '' ?>>1+ sasong</option>
                <option value="2" <?= $minSeasons == 2 ? 'selected' : '' ?>>2+ sasonger</option>
                <option value="3" <?= $minSeasons == 3 ? 'selected' : '' ?>>3+ sasonger</option>
                <option value="5" <?= $minSeasons == 5 ? 'selected' : '' ?>>5+ sasonger</option>
            </select>
        </div>

        <div class="filter-group">
            <a href="?export=csv&type=churned&year=<?= $targetYear ?>&min_seasons=<?= $minSeasons ?>" class="btn-admin btn-admin-primary">
                <i data-lucide="download"></i> Exportera CSV
            </a>
        </div>
    </form>
</div>

<!-- Stats -->
<div class="stats-row">
    <div class="stat-card primary">
        <div class="stat-value"><?= number_format($churnedStats['total']) ?></div>
        <div class="stat-label">Totalt churned</div>
    </div>
    <?php foreach (array_slice($churnedStats['by_year'], 0, 4, true) as $year => $count): ?>
    <div class="stat-card">
        <div class="stat-value"><?= number_format($count) ?></div>
        <div class="stat-label">Senast <?= $year ?></div>
    </div>
    <?php endforeach; ?>
</div>

<div class="admin-card">
    <div class="admin-card-header">
        <h2>Deltagare som inte tavlade <?= $targetYear ?></h2>
    </div>
    <div class="admin-card-body" style="padding:0;">
        <div class="result-count" style="padding: var(--space-md) var(--space-md) 0;">
            Visar <?= count($churnedRiders) ?> av <?= number_format($churnedStats['total']) ?> (max 500)
        </div>
        <div class="admin-table-container" style="max-height: 600px; overflow-y: auto;">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>Klubb</th>
                        <th>Senast aktiv</th>
                        <th>Sasonger</th>
                        <th>Serier</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($churnedRiders as $rider): ?>
                    <tr>
                        <td>
                            <a href="/rider/<?= $rider['id'] ?>" class="text-link" target="_blank">
                                <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                            </a>
                        </td>
                        <td><?= htmlspecialchars($rider['club_name'] ?? '-') ?></td>
                        <td><strong><?= $rider['last_active_year'] ?></strong></td>
                        <td><?= $rider['total_seasons'] ?></td>
                        <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="<?= htmlspecialchars($rider['series_names'] ?? '') ?>">
                            <?= htmlspecialchars($rider['series_names'] ?? '-') ?>
                        </td>
                        <td>
                            <a href="/rider/<?= $rider['id'] ?>" target="_blank" class="btn-admin btn-admin-secondary btn-sm">
                                <i data-lucide="external-link"></i>
                            </a>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<?php else: ?>
<!-- ========== NOT IN SERIES TAB ========== -->

<div class="filter-bar">
    <form method="get" style="display:flex;gap:var(--space-md);flex-wrap:wrap;align-items:flex-end;">
        <input type="hidden" name="tab" value="not-in-series">

        <div class="filter-group">
            <label class="filter-label">Ar</label>
            <select name="year" class="form-select" onchange="this.form.submit()">
                <?php foreach ($availableYears as $y): ?>
                <option value="<?= $y ?>" <?= $y == $targetYear ? 'selected' : '' ?>><?= $y ?></option>
                <?php endforeach; ?>
            </select>
        </div>

        <div class="filter-group">
            <label class="filter-label">Exkludera serie (ej deltagit i)</label>
            <select name="exclude_series" class="form-select" onchange="this.form.submit()">
                <option value="">-- Valj serie --</option>
                <?php foreach ($allSeries as $s): ?>
                <option value="<?= $s['id'] ?>" <?= $s['id'] == $excludeSeriesId ? 'selected' : '' ?>>
                    <?= htmlspecialchars($s['name']) ?> (<?= $s['year'] ?>)
                </option>
                <?php endforeach; ?>
            </select>
        </div>

        <?php if ($excludeSeriesId): ?>
        <div class="filter-group">
            <a href="?export=csv&type=not-in-series&year=<?= $targetYear ?>&exclude_series=<?= $excludeSeriesId ?>" class="btn-admin btn-admin-primary">
                <i data-lucide="download"></i> Exportera CSV
            </a>
        </div>
        <?php endif; ?>
    </form>
</div>

<?php if (!$excludeSeriesId): ?>
<div class="alert alert-info">
    <i data-lucide="info"></i>
    <div>Valj en serie ovan for att se deltagare som tavlade <?= $targetYear ?> men INTE i den serien.</div>
</div>
<?php else: ?>

<!-- Stats -->
<div class="stats-row">
    <div class="stat-card primary">
        <div class="stat-value"><?= number_format($notInSeriesStats['total']) ?></div>
        <div class="stat-label">Tavlade <?= $targetYear ?>, ej <?= htmlspecialchars($excludeSeriesName) ?></div>
    </div>
</div>

<div class="admin-card">
    <div class="admin-card-header">
        <h2>Tavlade <?= $targetYear ?> men EJ i <?= htmlspecialchars($excludeSeriesName) ?></h2>
    </div>
    <div class="admin-card-body" style="padding:0;">
        <div class="result-count" style="padding: var(--space-md) var(--space-md) 0;">
            Visar <?= count($notInSeriesRiders) ?> av <?= number_format($notInSeriesStats['total']) ?> (max 500)
        </div>
        <div class="admin-table-container" style="max-height: 600px; overflow-y: auto;">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>Klubb</th>
                        <th>Serier <?= $targetYear ?></th>
                        <th>Starter</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($notInSeriesRiders as $rider): ?>
                    <tr>
                        <td>
                            <a href="/rider/<?= $rider['id'] ?>" class="text-link" target="_blank">
                                <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                            </a>
                        </td>
                        <td><?= htmlspecialchars($rider['club_name'] ?? '-') ?></td>
                        <td style="max-width:250px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="<?= htmlspecialchars($rider['series_2025'] ?? '') ?>">
                            <?= htmlspecialchars($rider['series_2025'] ?? '-') ?>
                        </td>
                        <td><?= $rider['starts_2025'] ?></td>
                        <td>
                            <a href="/rider/<?= $rider['id'] ?>" target="_blank" class="btn-admin btn-admin-secondary btn-sm">
                                <i data-lucide="external-link"></i>
                            </a>
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

<?php if (isset($error)): ?>
<div class="alert alert-danger">
    <i data-lucide="alert-circle"></i>
    <div><strong>Fel:</strong> <?= htmlspecialchars($error) ?></div>
</div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
