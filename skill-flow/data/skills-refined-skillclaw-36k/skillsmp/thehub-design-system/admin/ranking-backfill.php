<?php
/**
 * Admin: Backfill Ranking Snapshots
 * Genererar ranking-snapshots för varje månad de senaste 24 månaderna
 * Använder samma beräkningslogik som huvudsystemet (calculateRankingDataAsOf)
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';

// Page setup
$page_title = 'Backfill Ranking Snapshots';
$db = getDB();

$message = '';
$messageType = '';
$stats = null;

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {

    if ($_POST['action'] === 'backfill') {
        set_time_limit(300); // 5 minutes max

        try {
            // Generate one snapshot per month for the last 24 months
            $totalSnapshots = 0;
            $processedMonths = 0;
            $previousPositions = []; // Track positions for calculating changes

            // Generate list of months (oldest first)
            $months = [];
            for ($i = 24; $i >= 0; $i--) {
                $months[] = date('Y-m-01', strtotime("-$i months"));
            }

            foreach ($months as $monthStart) {
                // Calculate ranking as of end of this month
                $monthEnd = date('Y-m-t', strtotime($monthStart)); // Last day of month

                // Use the system's proper calculation function
                $riderData = calculateRankingDataAsOf($db, 'GRAVITY', $monthEnd);

                if (empty($riderData)) continue;

                // Delete existing snapshots for this month
                $db->query("DELETE FROM ranking_snapshots WHERE discipline = 'GRAVITY' AND snapshot_date BETWEEN ? AND ?",
                    [$monthStart, $monthEnd]);

                // Insert new snapshots (use first of month as snapshot date)
                foreach ($riderData as $rider) {
                    $riderId = $rider['rider_id'];
                    $prevPos = $previousPositions[$riderId] ?? null;
                    $posChange = $prevPos !== null ? ($prevPos - $rider['ranking_position']) : null;

                    $db->query("INSERT INTO ranking_snapshots
                        (rider_id, discipline, snapshot_date, total_ranking_points,
                         points_last_12_months, points_months_13_24, events_count,
                         ranking_position, previous_position, position_change)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
                        $riderId,
                        'GRAVITY',
                        $monthStart,
                        $rider['total_ranking_points'],
                        $rider['points_12'],
                        $rider['points_13_24'],
                        $rider['events_count'],
                        $rider['ranking_position'],
                        $prevPos,
                        $posChange
                    ]);
                    $totalSnapshots++;

                    // Store position for next month's change calculation
                    $previousPositions[$riderId] = $rider['ranking_position'];
                }
                $processedMonths++;
            }

            $stats = [
                'months' => $processedMonths,
                'snapshots' => $totalSnapshots
            ];
            $message = "Klart! Skapade $totalSnapshots snapshots för $processedMonths månader.";
            $messageType = 'success';

        } catch (Exception $e) {
            $message = "Fel: " . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Get current stats
$currentStats = $db->getRow("
    SELECT
        COUNT(*) as total_snapshots,
        COUNT(DISTINCT snapshot_date) as unique_dates,
        MIN(snapshot_date) as oldest,
        MAX(snapshot_date) as newest
    FROM ranking_snapshots
    WHERE discipline = 'GRAVITY'
");

$eventCount = $db->getRow("
    SELECT COUNT(DISTINCT DATE(e.date)) as cnt
    FROM events e
    JOIN results r ON r.event_id = e.id
    WHERE e.date >= DATE_SUB(CURDATE(), INTERVAL 24 MONTH)
      AND e.discipline IN ('ENDURO', 'DH')
      AND r.status = 'finished'
");

// Use unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?>"><?= htmlspecialchars($message) ?></div>
<?php endif; ?>

<div class="card">
    <div class="card-header">
        <h3>Nuvarande status</h3>
    </div>
    <div class="card-body">
        <div class="stats-grid">
            <div class="stat-box">
                <span class="stat-value"><?= number_format($currentStats['total_snapshots'] ?? 0) ?></span>
                <span class="stat-label">Snapshots</span>
            </div>
            <div class="stat-box">
                <span class="stat-value"><?= $currentStats['unique_dates'] ?? 0 ?></span>
                <span class="stat-label">Unika datum</span>
            </div>
            <div class="stat-box">
                <span class="stat-value"><?= $eventCount['cnt'] ?? 0 ?></span>
                <span class="stat-label">Events (24 mån)</span>
            </div>
        </div>

        <?php if ($currentStats['oldest'] && $currentStats['newest']): ?>
        <p class="text-muted mt-md">
            Data från <?= date('Y-m-d', strtotime($currentStats['oldest'])) ?>
            till <?= date('Y-m-d', strtotime($currentStats['newest'])) ?>
        </p>
        <?php endif; ?>
    </div>
</div>

<div class="card mt-lg">
    <div class="card-header">
        <h3>Generera snapshots</h3>
    </div>
    <div class="card-body">
        <p>Detta skapar <strong>en ranking-snapshot per månad</strong> för de senaste 24 månaderna.</p>
        <p class="text-muted">Använder samma beräkningslogik som ranking-systemet (fältstorlek, eventtyp, tidsviktning).</p>

        <form method="POST" class="mt-lg">
            <input type="hidden" name="action" value="backfill">
            <button type="submit" class="btn btn-primary" onclick="this.disabled=true; this.innerHTML='Bearbetar...'; this.form.submit();">
                <i data-lucide="play"></i>
                Kör backfill (24 månader)
            </button>
        </form>
    </div>
</div>

<style>
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: var(--space-md);
}
.stat-box {
    text-align: center;
    padding: var(--space-md);
    background: var(--color-bg-tertiary, #f5f5f5);
    border-radius: var(--radius-md);
}
.stat-value {
    display: block;
    font-size: 1.5rem;
    font-weight: var(--font-weight-bold, 700);
    color: var(--color-accent, #61CE70);
}
.stat-label {
    font-size: var(--font-size-sm, 0.875rem);
    color: var(--color-text-secondary, #666);
}
.mt-md { margin-top: var(--space-md); }
.mt-lg { margin-top: var(--space-lg); }
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
