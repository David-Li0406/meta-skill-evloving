<?php
/**
 * CRITICAL: Recalculate ALL points to apply class filtering
 *
 * This will:
 * 1. Recalculate points for ALL events using new class filtering
 * 2. Set points to 0 for Motion Kids and all non-point classes
 * 3. Apply awards_points and series_eligible checks
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/point-calculations.php';
require_admin();

$db = getDB();

$pageTitle = 'Omräkna ALLA Poäng - Applicera Klassfiltrer';
$pageType = 'admin';
include __DIR__ . '/components/unified-layout.php';
?>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h1>🔄 Omräkna ALLA Poäng</h1>
            <p class="text-secondary">Applicerar klassfiltrer (Motion Kids = 0 poäng)</p>
        </div>

        <div class="card-body">
            <?php if (!isset($_GET['confirm'])): ?>
                <!-- Confirmation page -->
                <div class="alert alert--warning mb-lg">
                    <strong>⚠️ VIKTIGT!</strong>
                    <p>Detta kommer att omräkna poäng för ALLA aktiva events och applicera klassfiltreringen:</p>
                    <ul>
                        <li>✅ Motion Kids → 0 poäng</li>
                        <li>✅ Motion Kort → 0 poäng</li>
                        <li>✅ Motion Mellan → 0 poäng</li>
                        <li>✅ Sportmotion Lång → 0 poäng</li>
                        <li>✅ ALLA klasser med awards_points=0 OR series_eligible=0 → 0 poäng</li>
                    </ul>
                </div>

                <?php
                // Get statistics
                $totalEvents = $db->getRow("SELECT COUNT(*) as cnt FROM events WHERE active = 1")['cnt'] ?? 0;
                $totalResults = $db->getRow("SELECT COUNT(*) as cnt FROM results")['cnt'] ?? 0;
                $motionKidsResults = $db->getRow("
                    SELECT COUNT(*) as cnt
                    FROM results r
                    INNER JOIN classes c ON r.class_id = c.id
                    WHERE (c.awards_points = 0 OR c.series_eligible = 0)
                    AND r.points > 0
                ")['cnt'] ?? 0;
                ?>

                <div class="stats-grid mb-lg" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                    <div class="stat-card">
                        <div class="stat-value"><?= number_format($totalEvents) ?></div>
                        <div class="stat-label">Events att omräkna</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value"><?= number_format($totalResults) ?></div>
                        <div class="stat-label">Resultat totalt</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" style="color: var(--color-error);">
                            <?= number_format($motionKidsResults) ?>
                        </div>
                        <div class="stat-label">Motion Kids resultat med poäng (kommer nollställas)</div>
                    </div>
                </div>

                <div class="flex gap-md">
                    <a href="?confirm=1" class="btn btn--primary">
                        <i data-lucide="check"></i>
                        Ja, omräkna ALLA poäng nu
                    </a>
                    <a href="/admin/ranking" class="btn btn--secondary">
                        <i data-lucide="x"></i>
                        Avbryt
                    </a>
                </div>

            <?php else: ?>
                <!-- Recalculation in progress -->
                <div class="alert alert--info mb-lg">
                    <strong>⏳ Omräkning pågår...</strong>
                    <p>Detta kan ta några minuter. Vänligen vänta.</p>
                </div>

                <?php
                // Get all active events
                $events = $db->getAll("SELECT id, name FROM events WHERE active = 1 ORDER BY date DESC");

                echo "<div class='mb-lg'>";
                echo "<p><strong>Omräknar " . count($events) . " events...</strong></p>";
                echo "</div>";

                echo "<div style='max-height: 500px; overflow-y: auto; border: 1px solid var(--color-border); padding: 1rem; border-radius: var(--radius-md);'>";

                $totalUpdated = 0;
                $totalZeroed = 0;

                foreach ($events as $event) {
                    echo "<div style='margin-bottom: 0.5rem;'>";
                    echo "<strong>{$event['name']}</strong> (ID: {$event['id']})<br>";

                    // Recalculate points using new class filtering
                    $stats = recalculateEventPoints($db, $event['id']);

                    // Count how many were set to zero
                    $zeroedResults = $db->getRow("
                        SELECT COUNT(*) as cnt
                        FROM results r
                        INNER JOIN classes c ON r.class_id = c.id
                        WHERE r.event_id = ?
                        AND (c.awards_points = 0 OR c.series_eligible = 0)
                        AND r.points = 0
                    ", [$event['id']])['cnt'] ?? 0;

                    echo "✅ Uppdaterade: {$stats['updated']} resultat | ";
                    echo "🚫 Nollställda: {$zeroedResults} Motion Kids<br>";

                    $totalUpdated += $stats['updated'];
                    $totalZeroed += $zeroedResults;

                    echo "</div>";
                    flush();
                }

                echo "</div>";

                echo "<div class='alert alert--success mt-lg'>";
                echo "<h3>✅ KLART!</h3>";
                echo "<p><strong>Totalt uppdaterade:</strong> {$totalUpdated} resultat</p>";
                echo "<p><strong>Totalt nollställda:</strong> {$totalZeroed} Motion Kids/non-point resultat</p>";
                echo "</div>";

                echo "<div class='mt-lg'>";
                echo "<a href='/admin/ranking' class='btn btn--primary'>Tillbaka till Ranking</a>";
                echo "</div>";
                ?>

            <?php endif; ?>
        </div>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
