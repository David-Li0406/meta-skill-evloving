<?php
/**
 * Fix DNS/DNF/DQ positions - One-time cleanup tool
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

$message = '';
$messageType = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['fix'])) {
    checkCsrf();

    // Count affected rows
    $before = $db->getRow("SELECT COUNT(*) as cnt FROM results WHERE status IN ('dns', 'dnf', 'dq') AND position IS NOT NULL");

    // Fix them
    $db->query("UPDATE results SET position = NULL WHERE status IN ('dns', 'dnf', 'dq') AND position IS NOT NULL");

    // Verify
    $after = $db->getRow("SELECT COUNT(*) as cnt FROM results WHERE status IN ('dns', 'dnf', 'dq') AND position IS NOT NULL");

    $fixed = $before['cnt'] - $after['cnt'];
    $message = "Fixat! {$fixed} resultat uppdaterade (position = NULL för DNS/DNF/DQ).";
    $messageType = 'success';
}

// Count current affected rows
$affected = $db->getRow("SELECT COUNT(*) as cnt FROM results WHERE status IN ('dns', 'dnf', 'dq') AND position IS NOT NULL");

// Get sample of affected results
$samples = $db->getAll("
    SELECT r.id, r.position, r.status, r.finish_time,
           CONCAT(ri.firstname, ' ', ri.lastname) as rider_name,
           e.name as event_name, e.date as event_date
    FROM results r
    JOIN riders ri ON r.cyclist_id = ri.id
    JOIN events e ON r.event_id = e.id
    WHERE r.status IN ('dns', 'dnf', 'dq') AND r.position IS NOT NULL
    ORDER BY e.date DESC
    LIMIT 20
");

$page_title = 'Fixa DNS/DNF placeringar';
$breadcrumbs = [
    ['label' => 'Admin', 'url' => '/admin'],
    ['label' => 'Fixa DNS/DNF placeringar']
];
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="card">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="tool"></i>
            Fixa felaktiga placeringar för DNS/DNF/DQ
        </h2>
    </div>
    <div class="card-body">
        <p class="mb-lg">
            Åkare med status DNS (Did Not Start), DNF (Did Not Finish) eller DQ (Diskvalificerad)
            ska inte ha en placering. Detta verktyg rensar felaktigt satta placeringar.
        </p>

        <div class="alert alert--info mb-lg">
            <i data-lucide="info"></i>
            <strong><?= $affected['cnt'] ?></strong> resultat med DNS/DNF/DQ har en placering som bör rensas.
        </div>

        <?php if ($affected['cnt'] > 0): ?>
        <form method="POST">
            <?= csrf_field() ?>
            <button type="submit" name="fix" value="1" class="btn btn--primary btn-lg">
                <i data-lucide="wrench"></i>
                Fixa <?= $affected['cnt'] ?> resultat
            </button>
        </form>

        <?php if (!empty($samples)): ?>
        <h3 class="mt-xl mb-md">Exempel på berörda resultat:</h3>
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Åkare</th>
                        <th>Event</th>
                        <th>Datum</th>
                        <th>Status</th>
                        <th>Placering (felaktig)</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($samples as $row): ?>
                    <tr>
                        <td><?= h($row['rider_name']) ?></td>
                        <td><?= h($row['event_name']) ?></td>
                        <td><?= date('Y-m-d', strtotime($row['event_date'])) ?></td>
                        <td><span class="badge badge-warning"><?= strtoupper($row['status']) ?></span></td>
                        <td><span class="text-danger"><?= $row['position'] ?></span></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>

        <?php else: ?>
        <div class="alert alert--success">
            <i data-lucide="check-circle"></i>
            Alla resultat ser korrekta ut! Inga DNS/DNF/DQ-åkare har felaktiga placeringar.
        </div>
        <?php endif; ?>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
