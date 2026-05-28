<?php
/**
 * Minimal ranking page - Debug tool
 */
require_once __DIR__ . '/../config.php';
require_admin();

require_once __DIR__ . '/../includes/ranking_functions.php';

$db = getDB();

// Page config
$page_title = 'Minimal Ranking Test';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'Minimal Ranking']
];

include __DIR__ . '/components/unified-layout.php';
?>

<div class="card">
    <div class="card-header">
        <h3>System Status</h3>
    </div>
    <div class="card-body">
        <?php try { ?>
            <p class="text-success">Config loaded</p>
            <p class="text-success">Functions loaded</p>
            <p class="text-success">Database connected</p>

            <?php
            $exists = rankingTablesExist($db);
            $multipliers = getRankingFieldMultipliers($db);
            $disciplineStats = getRankingStats($db);
            ?>

            <p>Tables exist: <strong><?= $exists ? 'YES' : 'NO' ?></strong></p>
            <p>Multipliers: <strong><?= count($multipliers) ?></strong></p>

            <h4 style="margin-top: var(--space-md);">Stats:</h4>
            <pre style="background: var(--color-bg-surface); padding: var(--space-md); border-radius: var(--radius-md);"><?= htmlspecialchars(print_r($disciplineStats, true)) ?></pre>
        <?php } catch (Exception $e) { ?>
            <div class="alert alert-danger">
                <strong>Error:</strong> <?= htmlspecialchars($e->getMessage()) ?>
            </div>
        <?php } ?>
    </div>
</div>

<div class="card" style="margin-top: var(--space-md);">
    <div class="card-header">
        <h3>Test Calculation</h3>
    </div>
    <div class="card-body">
        <form method="POST">
            <button type="submit" name="calculate" class="btn btn-primary">Run Calculation</button>
        </form>

        <?php if (isset($_POST['calculate'])): ?>
            <div style="margin-top: var(--space-md);">
                <h4>Running calculation...</h4>
                <?php
                set_time_limit(300);
                ini_set('memory_limit', '512M');

                echo "<p>Memory limit: " . ini_get('memory_limit') . "</p>";
                echo "<p>Time limit: " . ini_get('max_execution_time') . "s</p>";
                flush();

                try {
                    $stats = runFullRankingUpdate($db, true);
                    ?>
                    <div class="alert alert-success">All ranking calculations complete!</div>
                    <pre style="background: var(--color-bg-surface); padding: var(--space-md); border-radius: var(--radius-md);"><?= htmlspecialchars(print_r($stats, true)) ?></pre>
                    <p><strong>Total time:</strong> <?= $stats['total_time'] ?>s</p>
                    <?php
                } catch (Exception $e) {
                    ?>
                    <div class="alert alert-danger">
                        <strong>Error during calculation:</strong><br>
                        <?= htmlspecialchars($e->getMessage()) ?>
                    </div>
                    <pre style="background: var(--color-bg-surface); padding: var(--space-md); border-radius: var(--radius-md);">
File: <?= htmlspecialchars($e->getFile()) ?>

Line: <?= $e->getLine() ?>

Stack trace:
<?= htmlspecialchars($e->getTraceAsString()) ?>
                    </pre>
                    <?php
                }
                ?>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
