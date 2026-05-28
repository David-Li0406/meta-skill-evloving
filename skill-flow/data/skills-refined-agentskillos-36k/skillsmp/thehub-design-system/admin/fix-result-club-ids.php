<?php
/**
 * Fix Results Club IDs Tool
 *
 * This tool updates results.club_id based on rider_club_seasons data.
 * It ensures that points are attributed to the correct club for each event
 * based on which club the rider was a member of at the time of the event.
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = '';
$dryRun = !isset($_POST['execute']);
$stats = [];

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    try {
        // Get all results with event info
        $allResults = $db->getAll("
            SELECT
                r.id as result_id,
                r.cyclist_id as rider_id,
                r.club_id as current_result_club_id,
                r.event_id,
                YEAR(e.date) as event_year,
                e.name as event_name,
                e.date as event_date,
                rd.firstname,
                rd.lastname,
                rd.club_id as rider_current_club_id
            FROM results r
            JOIN events e ON r.event_id = e.id
            JOIN riders rd ON r.cyclist_id = rd.id
            WHERE r.status = 'finished'
            ORDER BY e.date DESC, r.id
        ");

        $stats = [
            'total_results' => count($allResults),
            'checked' => 0,
            'fixed' => 0,
            'already_correct' => 0,
            'no_season_data' => 0,
            'details' => []
        ];

        foreach ($allResults as $result) {
            $stats['checked']++;

            $riderId = $result['rider_id'];
            $eventYear = $result['event_year'];
            $currentClubId = $result['current_result_club_id'];

            // Find what club the rider was in for this event's year
            $seasonData = $db->getRow("
                SELECT rcs.club_id, c.name as club_name
                FROM rider_club_seasons rcs
                JOIN clubs c ON rcs.club_id = c.id
                WHERE rcs.rider_id = ? AND rcs.season_year = ?
                LIMIT 1
            ", [$riderId, $eventYear]);

            if (!$seasonData) {
                $stats['no_season_data']++;
                continue;
            }

            $correctClubId = $seasonData['club_id'];

            if ($currentClubId == $correctClubId) {
                $stats['already_correct']++;
                continue;
            }

            // Need to fix this result
            $stats['fixed']++;

            // Get old club name for the log
            $oldClubName = 'NULL';
            if ($currentClubId) {
                $oldClub = $db->getRow("SELECT name FROM clubs WHERE id = ?", [$currentClubId]);
                $oldClubName = $oldClub['name'] ?? 'Okänd';
            }

            // Only store first 100 details
            if (count($stats['details']) < 100) {
                $stats['details'][] = [
                    'rider' => $result['firstname'] . ' ' . $result['lastname'],
                    'rider_id' => $riderId,
                    'event' => $result['event_name'],
                    'event_date' => $result['event_date'],
                    'old_club' => $oldClubName,
                    'new_club' => $seasonData['club_name'],
                    'result_id' => $result['result_id']
                ];
            }

            // Update the result if not dry run
            if (!$dryRun) {
                $db->query("UPDATE results SET club_id = ? WHERE id = ?", [$correctClubId, $result['result_id']]);
            }
        }

        if ($dryRun) {
            $message = "Simulering klar. {$stats['fixed']} resultat skulle korrigeras.";
            $messageType = 'info';
        } else {
            $message = "Klart! {$stats['fixed']} resultat har uppdaterats.";
            $messageType = 'success';
        }

    } catch (Exception $e) {
        $message = 'Fel: ' . $e->getMessage();
        $messageType = 'danger';
    }
}

$page_title = 'Fixa resultat klubb-ID';
$breadcrumbs = [['label' => 'Verktyg', 'url' => '/admin/tools.php'], ['label' => 'Fixa klubb-ID']];
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?>">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<div class="admin-card">
    <div class="admin-card-header">
        <h3>Hur det fungerar</h3>
    </div>
    <div class="admin-card-body">
        <p>Detta verktyg går igenom alla resultat och kontrollerar:</p>
        <ol>
            <li>Vilken säsong (år) tävlingen ägde rum</li>
            <li>Vilken klubb åkaren var medlem i den säsongen (från rider_club_seasons)</li>
            <li>Om results.club_id skiljer sig från säsongsklubben, uppdateras det</li>
        </ol>
        <p><strong>Viktigt:</strong> Efter uppdatering behöver klubbrankingen beräknas om.</p>
    </div>
</div>

<div class="admin-card">
    <div class="admin-card-header">
        <h3>Kör verktyget</h3>
    </div>
    <div class="admin-card-body">
        <form method="post" class="flex gap-md">
            <button type="submit" class="btn-admin btn-admin-secondary" name="simulate">
                <i data-lucide="search"></i>
                Simulera (visa vad som skulle ändras)
            </button>
            <button type="submit" class="btn-admin btn-admin-primary" name="execute" onclick="return confirm('Är du säker? Detta kommer uppdatera databasen.')">
                <i data-lucide="zap"></i>
                Kör på riktigt
            </button>
        </form>
    </div>
</div>

<?php if (!empty($stats)): ?>
<div class="admin-card">
    <div class="admin-card-header">
        <h3>Resultat</h3>
    </div>
    <div class="admin-card-body">
        <div class="stats-grid" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-md); margin-bottom: var(--space-lg);">
            <div class="stat-card" style="background: var(--color-bg-secondary); padding: var(--space-md); border-radius: var(--radius-md); text-align: center;">
                <div style="font-size: var(--text-2xl); font-weight: 700;"><?= number_format($stats['total_results']) ?></div>
                <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Totalt resultat</div>
            </div>
            <div class="stat-card" style="background: var(--color-bg-secondary); padding: var(--space-md); border-radius: var(--radius-md); text-align: center;">
                <div style="font-size: var(--text-2xl); font-weight: 700;"><?= number_format($stats['already_correct']) ?></div>
                <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Redan korrekta</div>
            </div>
            <div class="stat-card" style="background: rgba(97, 206, 112, 0.1); padding: var(--space-md); border-radius: var(--radius-md); text-align: center;">
                <div style="font-size: var(--text-2xl); font-weight: 700; color: var(--color-accent);"><?= number_format($stats['fixed']) ?></div>
                <div style="font-size: var(--text-sm); color: var(--color-text-secondary);"><?= $dryRun ? 'Skulle korrigeras' : 'Korrigerade' ?></div>
            </div>
            <div class="stat-card" style="background: var(--color-bg-secondary); padding: var(--space-md); border-radius: var(--radius-md); text-align: center;">
                <div style="font-size: var(--text-2xl); font-weight: 700;"><?= number_format($stats['no_season_data']) ?></div>
                <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Saknar säsongsdata</div>
            </div>
        </div>

        <?php if (!empty($stats['details'])): ?>
        <h4>Detaljerade ändringar (visar max 100)</h4>
        <div class="admin-table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Åkare</th>
                        <th>Tävling</th>
                        <th>Datum</th>
                        <th>Från klubb</th>
                        <th>Till klubb</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($stats['details'] as $detail): ?>
                    <tr>
                        <td>
                            <a href="/rider/<?= $detail['rider_id'] ?>">
                                <?= htmlspecialchars($detail['rider']) ?>
                            </a>
                        </td>
                        <td><?= htmlspecialchars($detail['event']) ?></td>
                        <td><?= $detail['event_date'] ?></td>
                        <td><?= htmlspecialchars($detail['old_club']) ?></td>
                        <td><strong><?= htmlspecialchars($detail['new_club']) ?></strong></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php if ($stats['fixed'] > 100): ?>
        <p class="text-secondary">...och <?= $stats['fixed'] - 100 ?> fler</p>
        <?php endif; ?>
        <?php endif; ?>
    </div>
</div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
