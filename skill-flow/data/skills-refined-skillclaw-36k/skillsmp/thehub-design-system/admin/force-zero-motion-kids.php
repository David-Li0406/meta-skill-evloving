<?php
/**
 * FORCE Zero Points for Motion Kids
 * Direct SQL update to guarantee Motion Kids = 0 points
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

if (isset($_GET['execute'])) {
    // Count before
    $before = $db->getRow("
        SELECT COUNT(*) as cnt
        FROM results r
        INNER JOIN classes c ON r.class_id = c.id
        WHERE (c.awards_points = 0 OR c.series_eligible = 0)
        AND r.points > 0
    ")['cnt'] ?? 0;

    // FORCE UPDATE: Set ALL Motion Kids/non-eligible class results to 0 points
    $db->query("
        UPDATE results r
        INNER JOIN classes c ON r.class_id = c.id
        SET r.points = 0
        WHERE (c.awards_points = 0 OR c.series_eligible = 0)
        AND r.points > 0
    ");

    header('Location: /admin/force-zero-motion-kids?done=' . $before);
    exit;
}

$pageTitle = 'Force Zero Motion Kids Points';
$pageType = 'admin';
include __DIR__ . '/components/unified-layout.php';
?>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h1>🚫 Force Zero Motion Kids</h1>
            <p class="text-secondary">Direkt SQL-uppdatering</p>
        </div>

        <div class="card-body">
            <?php if (isset($_GET['done'])): ?>
                <div class="alert alert--success mb-lg">
                    <h3>✅ KLART!</h3>
                    <p><strong><?= $_GET['done'] ?> resultat</strong> uppdaterade till 0 poäng.</p>
                </div>
                <a href="/admin/ranking" class="btn btn--primary">Tillbaka till Ranking</a>
            <?php else: ?>
                <?php
                // Show current Motion Kids results with points > 0
                $badResults = $db->getAll("
                    SELECT
                        r.id,
                        r.points,
                        e.name as event_name,
                        c.display_name as class_name,
                        CONCAT(rid.firstname, ' ', rid.lastname) as rider_name
                    FROM results r
                    INNER JOIN classes c ON r.class_id = c.id
                    INNER JOIN events e ON r.event_id = e.id
                    INNER JOIN riders rid ON r.cyclist_id = rid.id
                    WHERE (c.awards_points = 0 OR c.series_eligible = 0)
                    AND r.points > 0
                    ORDER BY r.points DESC
                    LIMIT 50
                ");
                ?>

                <div class="alert alert--warning mb-lg">
                    <strong>⚠️ VARNING</strong>
                    <p>Detta kommer att direkt uppdatera databasen och sätta ALLA resultat i icke-poänggivande klasser till 0 poäng.</p>
                    <p><strong>Funna resultat med fel poäng: <?= count($badResults) ?></strong></p>
                </div>

                <?php if (!empty($badResults)): ?>
                    <div class="mb-lg">
                        <h3>Exempel på resultat som kommer nollställas:</h3>
                        <table class="table table--striped">
                            <thead>
                                <tr>
                                    <th>Åkare</th>
                                    <th>Event</th>
                                    <th>Klass</th>
                                    <th>Nuvarande poäng</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach (array_slice($badResults, 0, 10) as $result): ?>
                                <tr>
                                    <td><?= htmlspecialchars($result['rider_name']) ?></td>
                                    <td><?= htmlspecialchars($result['event_name']) ?></td>
                                    <td><?= htmlspecialchars($result['class_name']) ?></td>
                                    <td style="color: var(--color-error); font-weight: bold;"><?= $result['points'] ?></td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                        <?php if (count($badResults) > 10): ?>
                            <p class="text-muted">...och <?= count($badResults) - 10 ?> fler</p>
                        <?php endif; ?>
                    </div>

                    <div class="flex gap-md">
                        <a href="?execute=1" class="btn btn--primary" onclick="return confirm('Är du ABSOLUT säker? Detta sätter ALLA Motion Kids-resultat till 0 poäng.')">
                            <i data-lucide="zap"></i>
                            JA, KÖR NU - Sätt alla till 0
                        </a>
                        <a href="/admin/ranking" class="btn btn--secondary">
                            Avbryt
                        </a>
                    </div>
                <?php else: ?>
                    <div class="alert alert--success">
                        <p>✅ Inga Motion Kids-resultat med poäng hittades!</p>
                    </div>
                    <a href="/admin/ranking" class="btn btn--primary">Tillbaka</a>
                <?php endif; ?>
            <?php endif; ?>
        </div>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
