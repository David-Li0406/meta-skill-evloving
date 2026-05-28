<?php
/**
 * Reset Analytics Data
 *
 * Rensar analytics_cron_runs sa att populate-historical
 * kan kora om alla berakningar.
 *
 * @package TheHUB Analytics
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_admin();

global $pdo;

$message = '';
$error = '';

// Hantera POST - rensa data
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    $action = $_POST['action'];

    try {
        if ($action === 'reset_cron') {
            // Rensa endast cron-runs (behalller beraknad data)
            $pdo->exec("DELETE FROM analytics_cron_runs");
            $message = "analytics_cron_runs rensad. Kor nu Populate Historical for att berakna om.";

        } elseif ($action === 'reset_all') {
            // Rensa ALLT - cron-runs + all beraknad data
            $tables = [
                'analytics_cron_runs',
                'rider_yearly_stats',
                'series_participation',
                'series_crossover',
                'club_yearly_stats',
                'venue_yearly_stats'
            ];

            foreach ($tables as $table) {
                $check = $pdo->query("SHOW TABLES LIKE '$table'")->fetch();
                if ($check) {
                    $pdo->exec("TRUNCATE TABLE $table");
                }
            }
            $message = "All analytics-data rensad. Kor nu Populate Historical.";

        } elseif ($action === 'reset_year' && isset($_POST['year'])) {
            $year = (int)$_POST['year'];
            if ($year >= 2010 && $year <= 2030) {
                // Rensa cron-runs for detta ar
                $stmt = $pdo->prepare("DELETE FROM analytics_cron_runs WHERE run_key = ?");
                $stmt->execute([(string)$year]);

                // Rensa beraknad data for detta ar
                $tables = [
                    'rider_yearly_stats' => 'season_year',
                    'series_participation' => 'season_year',
                    'club_yearly_stats' => 'season_year',
                    'venue_yearly_stats' => 'season_year'
                ];

                $deleted = 0;
                foreach ($tables as $table => $col) {
                    $check = $pdo->query("SHOW TABLES LIKE '$table'")->fetch();
                    if ($check) {
                        $stmt = $pdo->prepare("DELETE FROM $table WHERE $col = ?");
                        $stmt->execute([$year]);
                        $deleted += $stmt->rowCount();
                    }
                }

                // series_crossover har from_year och to_year
                $check = $pdo->query("SHOW TABLES LIKE 'series_crossover'")->fetch();
                if ($check) {
                    $stmt = $pdo->prepare("DELETE FROM series_crossover WHERE from_year = ? OR to_year = ?");
                    $stmt->execute([$year, $year]);
                    $deleted += $stmt->rowCount();
                }

                $message = "Data for ar $year rensad ($deleted rader). Kor nu Populate Historical.";
            }
        }
    } catch (Exception $e) {
        $error = "Fel: " . $e->getMessage();
    }
}

// Hamta statistik
$stats = [];
$tables = [
    'analytics_cron_runs' => 'Cron-korningar',
    'rider_yearly_stats' => 'Rider-statistik',
    'series_participation' => 'Serie-deltagande',
    'series_crossover' => 'Serie-crossover',
    'club_yearly_stats' => 'Klubb-statistik',
    'venue_yearly_stats' => 'Venue-statistik'
];

foreach ($tables as $table => $label) {
    try {
        $check = $pdo->query("SHOW TABLES LIKE '$table'")->fetch();
        if ($check) {
            $count = $pdo->query("SELECT COUNT(*) FROM $table")->fetchColumn();
            $stats[$table] = ['label' => $label, 'count' => $count, 'exists' => true];
        } else {
            $stats[$table] = ['label' => $label, 'count' => 0, 'exists' => false];
        }
    } catch (Exception $e) {
        $stats[$table] = ['label' => $label, 'count' => 0, 'exists' => false];
    }
}

// Hamta ar med data
$years = [];
try {
    $stmt = $pdo->query("SELECT DISTINCT YEAR(date) as year FROM events WHERE date IS NOT NULL ORDER BY year DESC");
    $years = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {}

$page_title = 'Reset Analytics';
$breadcrumbs = [
    ['label' => 'Tools', 'url' => '/admin/tools.php'],
    ['label' => 'Reset Analytics']
];
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.reset-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-lg);
}
.reset-card h3 {
    margin: 0 0 var(--space-md);
}
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}
.stat-box {
    background: var(--color-bg-surface);
    padding: var(--space-md);
    border-radius: var(--radius-sm);
    text-align: center;
}
.stat-box .count {
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--color-accent);
}
.stat-box .label {
    font-size: var(--text-sm);
    color: var(--color-text-muted);
}
.stat-box.missing {
    opacity: 0.5;
}
.action-buttons {
    display: flex;
    gap: var(--space-md);
    flex-wrap: wrap;
    align-items: center;
}
</style>

<?php if ($message): ?>
<div class="alert alert-success">
    <i data-lucide="check-circle"></i>
    <div><?= htmlspecialchars($message) ?></div>
</div>
<?php endif; ?>

<?php if ($error): ?>
<div class="alert alert-danger">
    <i data-lucide="alert-circle"></i>
    <div><?= htmlspecialchars($error) ?></div>
</div>
<?php endif; ?>

<!-- Aktuell data -->
<div class="reset-card">
    <h3>Aktuell Analytics-data</h3>
    <div class="stats-grid">
        <?php foreach ($stats as $table => $info): ?>
        <div class="stat-box <?= !$info['exists'] ? 'missing' : '' ?>">
            <div class="count"><?= $info['exists'] ? number_format($info['count']) : '-' ?></div>
            <div class="label"><?= htmlspecialchars($info['label']) ?></div>
        </div>
        <?php endforeach; ?>
    </div>
</div>

<!-- Reset-alternativ -->
<div class="reset-card">
    <h3>1. Rensa endast jobb-status (rekommenderas)</h3>
    <p style="color: var(--color-text-secondary); margin-bottom: var(--space-md);">
        Rensar <code>analytics_cron_runs</code> sa att Populate Historical kan kora om alla berakningar.
        Befintlig data behalles men skrivs over vid nasta korning.
    </p>
    <form method="post" onsubmit="return confirm('Rensa jobb-status?');">
        <input type="hidden" name="action" value="reset_cron">
        <button type="submit" class="btn-admin btn-admin-warning">Rensa jobb-status</button>
    </form>
</div>

<div class="reset-card">
    <h3>2. Rensa specifikt ar</h3>
    <p style="color: var(--color-text-secondary); margin-bottom: var(--space-md);">
        Rensar all analytics-data for ett specifikt ar.
    </p>
    <form method="post" onsubmit="return confirm('Rensa all data for detta ar?');">
        <input type="hidden" name="action" value="reset_year">
        <div class="action-buttons">
            <select name="year" class="form-select" style="width: auto;">
                <?php foreach ($years as $y): ?>
                <option value="<?= $y ?>"><?= $y ?></option>
                <?php endforeach; ?>
            </select>
            <button type="submit" class="btn-admin btn-admin-warning">Rensa valt ar</button>
        </div>
    </form>
</div>

<div class="reset-card">
    <h3>3. Rensa ALLT (fullstandig omstart)</h3>
    <p style="color: var(--color-text-secondary); margin-bottom: var(--space-md);">
        <strong>VARNING:</strong> Tar bort ALL analytics-data. Anvand endast om du vill borja om helt fran borjan.
    </p>
    <form method="post" onsubmit="return confirm('AR DU SAKER? Detta tar bort ALL analytics-data!');">
        <input type="hidden" name="action" value="reset_all">
        <button type="submit" class="btn-admin btn-admin-danger">Rensa ALL analytics-data</button>
    </form>
</div>

<!-- Nasta steg -->
<div class="reset-card">
    <h3>Nasta steg</h3>
    <p style="margin-bottom: var(--space-md);">
        Efter att du rensat data, kor Populate Historical for att generera ny statistik:
    </p>
    <div class="action-buttons">
        <a href="/analytics/populate-historical.php?force=1" class="btn-admin btn-admin-primary">
            Kor Populate Historical (Force)
        </a>
        <a href="/admin/analytics-diagnose.php" class="btn-admin btn-admin-secondary">
            Diagnostisera
        </a>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
