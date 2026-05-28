<?php
/**
 * Create Test Series for Registration Testing
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config.php';

// Check if admin
if (!function_exists('require_admin')) {
    die('Config not loaded');
}

require_admin();

$db = getDB();

$page_title = 'Skapa Testserie';
include __DIR__ . '/components/unified-layout.php';
?>

<div class="admin-card">
    <div class="admin-card-header">
        <h2><i data-lucide="flask-conical"></i> Testserie för anmälan</h2>
    </div>
    <div class="admin-card-body">

<?php
$action = $_GET['action'] ?? '';
$message = '';
$messageType = '';

if ($action === 'create') {
    try {
        // Check if test series already exists
        $existing = $db->getRow("SELECT id FROM series WHERE name = '[TEST] Anmälningstest' LIMIT 1");

        if ($existing) {
            $message = "Testserie finns redan (ID: {$existing['id']})";
            $messageType = 'info';
            $seriesId = $existing['id'];
        } else {
            // Get default pricing template
            $defaultTemplate = $db->getRow("SELECT id FROM pricing_templates WHERE is_default = 1 LIMIT 1");
            $templateId = $defaultTemplate ? $defaultTemplate['id'] : null;

            // Create test series
            $db->insert('series', [
                'name' => '[TEST] Anmälningstest',
                'year' => date('Y'),
                'discipline' => 'enduro',
                'status' => 'draft',
                'registration_enabled' => 1,
                'pricing_template_id' => $templateId
            ]);
            $seriesId = $db->lastInsertId();
            $message = "Skapade testserie (ID: $seriesId)";
            $messageType = 'success';
        }

        // Check for existing test events
        $existingEvents = $db->getAll("SELECT id FROM events WHERE series_id = ?", [$seriesId]);

        if (count($existingEvents) === 0) {
            // Create test events
            $testEvents = [
                [
                    'name' => '[TEST] Event 1 - Öppen anmälan',
                    'date' => date('Y-m-d', strtotime('+30 days')),
                    'location' => 'Testbanan',
                    'registration_opens' => date('Y-m-d H:i:s', strtotime('-7 days')),
                    'registration_deadline' => date('Y-m-d H:i:s', strtotime('+25 days')),
                ],
                [
                    'name' => '[TEST] Event 2 - Inte öppnat än',
                    'date' => date('Y-m-d', strtotime('+60 days')),
                    'location' => 'Testbanan',
                    'registration_opens' => date('Y-m-d H:i:s', strtotime('+14 days')),
                    'registration_deadline' => date('Y-m-d H:i:s', strtotime('+55 days')),
                ],
                [
                    'name' => '[TEST] Event 3 - Stängd anmälan',
                    'date' => date('Y-m-d', strtotime('+5 days')),
                    'location' => 'Testbanan',
                    'registration_opens' => date('Y-m-d H:i:s', strtotime('-30 days')),
                    'registration_deadline' => date('Y-m-d H:i:s', strtotime('-2 days')),
                ],
            ];

            foreach ($testEvents as $event) {
                $db->insert('events', array_merge($event, [
                    'series_id' => $seriesId,
                    'discipline' => 'enduro',
                    'active' => 0
                ]));
            }
            $message .= " + 3 test-events skapade";
        }

    } catch (Exception $e) {
        $message = 'Fel: ' . $e->getMessage();
        $messageType = 'error';
    }
}

if ($action === 'delete') {
    try {
        $testSeries = $db->getRow("SELECT id FROM series WHERE name = '[TEST] Anmälningstest' LIMIT 1");

        if ($testSeries) {
            $db->query("DELETE FROM events WHERE series_id = ?", [$testSeries['id']]);
            $db->query("DELETE FROM series WHERE id = ?", [$testSeries['id']]);
            $message = 'Testdata borttaget!';
            $messageType = 'success';
        } else {
            $message = 'Ingen testserie hittades';
            $messageType = 'info';
        }
    } catch (Exception $e) {
        $message = 'Fel: ' . $e->getMessage();
        $messageType = 'error';
    }
}

// Check current status
$testSeries = $db->getRow("SELECT id FROM series WHERE name = '[TEST] Anmälningstest' LIMIT 1");
$testEvents = $testSeries ? $db->getAll("SELECT * FROM events WHERE series_id = ? ORDER BY date", [$testSeries['id']]) : [];

if ($message): ?>
    <div class="alert alert-<?= $messageType ?> mb-lg">
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<?php if ($testSeries): ?>
    <div class="admin-alert admin-alert-success mb-lg">
        <i data-lucide="check-circle"></i>
        <div>
            <strong>Testserie aktiv</strong> (ID: <?= $testSeries['id'] ?>)<br>
            <?= count($testEvents) ?> test-events
        </div>
    </div>

    <h4 class="mb-md">Test-events:</h4>
    <div class="admin-table-container mb-lg">
        <table class="admin-table">
            <thead>
                <tr>
                    <th>Namn</th>
                    <th>Datum</th>
                    <th>Anmälan öppnar</th>
                    <th>Anmälan stänger</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($testEvents as $event):
                    $now = time();
                    $opens = strtotime($event['registration_opens']);
                    $closes = strtotime($event['registration_deadline']);

                    if ($now < $opens) {
                        $status = '<span class="badge badge-warning">Ej öppnat</span>';
                    } elseif ($now > $closes) {
                        $status = '<span class="badge badge-danger">Stängd</span>';
                    } else {
                        $status = '<span class="badge badge-success">Öppen</span>';
                    }
                ?>
                <tr>
                    <td><?= htmlspecialchars($event['name']) ?></td>
                    <td><?= $event['date'] ?></td>
                    <td><?= $event['registration_opens'] ?></td>
                    <td><?= $event['registration_deadline'] ?></td>
                    <td><?= $status ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <div class="flex gap-md">
        <a href="/admin/series-pricing.php?id=<?= $testSeries['id'] ?>" class="btn-admin btn-admin-primary">
            <i data-lucide="settings"></i>
            Anmälan & Priser
        </a>
        <a href="?action=delete" class="btn-admin btn-admin-danger" onclick="return confirm('Ta bort all testdata?')">
            <i data-lucide="trash-2"></i>
            Ta bort testdata
        </a>
    </div>

<?php else: ?>
    <p class="text-secondary mb-lg">
        Ingen testserie finns. Skapa en för att testa anmälningssystemet.
    </p>

    <a href="?action=create" class="btn-admin btn-admin-primary">
        <i data-lucide="plus"></i>
        Skapa testserie
    </a>
<?php endif; ?>

    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
