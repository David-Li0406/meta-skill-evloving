<?php
/**
 * Fix Swapped Classes Tool
 * Swap class assignments for results in an event (e.g., when Herrar/Damer are swapped)
 */
require_once __DIR__ . '/../../config.php';
require_once __DIR__ . '/../../includes/auth.php';
requireAdmin();

global $pdo;

$message = '';
$messageType = '';

// Get all classes for dropdowns
$classes = $pdo->query("SELECT id, name, display_name FROM classes ORDER BY sort_order, display_name")->fetchAll(PDO::FETCH_ASSOC);

// Get recent events for dropdown
$events = $pdo->query("SELECT id, name, date FROM events ORDER BY date DESC LIMIT 100")->fetchAll(PDO::FETCH_ASSOC);

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    checkCsrf();

    $eventId = (int)$_POST['event_id'];
    $class1Id = (int)$_POST['class1_id'];
    $class2Id = (int)$_POST['class2_id'];

    if (!$eventId || !$class1Id || !$class2Id) {
        $message = 'Alla fält måste fyllas i';
        $messageType = 'error';
    } elseif ($class1Id === $class2Id) {
        $message = 'Du måste välja två olika klasser';
        $messageType = 'error';
    } else {
        if ($_POST['action'] === 'preview') {
            // Preview mode - show what will be changed
            $stmt = $pdo->prepare("
                SELECT r.class_id, c.display_name, COUNT(*) as cnt,
                       GROUP_CONCAT(DISTINCT CONCAT(rid.firstname, ' ', rid.lastname) ORDER BY rid.lastname SEPARATOR ', ' LIMIT 5) as sample_riders
                FROM results r
                JOIN classes c ON r.class_id = c.id
                JOIN riders rid ON r.cyclist_id = rid.id
                WHERE r.event_id = ? AND r.class_id IN (?, ?)
                GROUP BY r.class_id
            ");
            $stmt->execute([$eventId, $class1Id, $class2Id]);
            $preview = $stmt->fetchAll(PDO::FETCH_ASSOC);

            if (empty($preview)) {
                $message = 'Inga resultat hittades för dessa klasser i detta event';
                $messageType = 'warning';
            }
        } elseif ($_POST['action'] === 'swap') {
            // Execute swap
            $pdo->beginTransaction();
            try {
                $tempId = -999;

                // Step 1: Move class1 to temp
                $stmt = $pdo->prepare("UPDATE results SET class_id = ? WHERE event_id = ? AND class_id = ?");
                $stmt->execute([$tempId, $eventId, $class1Id]);
                $count1 = $stmt->rowCount();

                // Step 2: Move class2 to class1
                $stmt->execute([$class1Id, $eventId, $class2Id]);
                $count2 = $stmt->rowCount();

                // Step 3: Move temp to class2
                $stmt->execute([$class2Id, $eventId, $tempId]);

                $pdo->commit();
                $message = "Klart! Bytte $count1 ↔ $count2 resultat mellan klasserna.";
                $messageType = 'success';

            } catch (Exception $e) {
                $pdo->rollBack();
                $message = 'Fel: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

$page_title = 'Byt Klasser';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'Byt Klasser']
];

include __DIR__ . '/../components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="card">
    <div class="card-header">
        <h3>Byt plats på två klasser</h3>
        <p class="text-secondary">Använd detta verktyg om resultat har importerats med fel klass (t.ex. Herrar/Damer omkastade)</p>
    </div>
    <div class="card-body">
        <form method="POST">
            <?= csrf_field() ?>

            <div class="form-group">
                <label class="form-label">Event</label>
                <select name="event_id" class="form-select" required>
                    <option value="">-- Välj event --</option>
                    <?php foreach ($events as $e): ?>
                    <option value="<?= $e['id'] ?>" <?= isset($_POST['event_id']) && $_POST['event_id'] == $e['id'] ? 'selected' : '' ?>>
                        <?= h($e['name']) ?> (<?= date('Y-m-d', strtotime($e['date'])) ?>)
                    </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <div class="form-row" style="display: grid; grid-template-columns: 1fr auto 1fr; gap: var(--space-md); align-items: end;">
                <div class="form-group">
                    <label class="form-label">Klass 1</label>
                    <select name="class1_id" class="form-select" required>
                        <option value="">-- Välj klass --</option>
                        <?php foreach ($classes as $c): ?>
                        <option value="<?= $c['id'] ?>" <?= isset($_POST['class1_id']) && $_POST['class1_id'] == $c['id'] ? 'selected' : '' ?>>
                            <?= h($c['display_name'] ?: $c['name']) ?>
                        </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <div style="padding-bottom: var(--space-md);">
                    <i data-lucide="arrow-left-right" style="color: var(--color-accent);"></i>
                </div>

                <div class="form-group">
                    <label class="form-label">Klass 2</label>
                    <select name="class2_id" class="form-select" required>
                        <option value="">-- Välj klass --</option>
                        <?php foreach ($classes as $c): ?>
                        <option value="<?= $c['id'] ?>" <?= isset($_POST['class2_id']) && $_POST['class2_id'] == $c['id'] ? 'selected' : '' ?>>
                            <?= h($c['display_name'] ?: $c['name']) ?>
                        </option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </div>

            <div class="form-actions" style="display: flex; gap: var(--space-md);">
                <button type="submit" name="action" value="preview" class="btn btn-secondary">
                    <i data-lucide="eye"></i> Förhandsgranska
                </button>
                <button type="submit" name="action" value="swap" class="btn btn-primary" onclick="return confirm('Är du säker på att du vill byta plats på klasserna?')">
                    <i data-lucide="shuffle"></i> Byt Klasser
                </button>
            </div>
        </form>
    </div>
</div>

<?php if (!empty($preview)): ?>
<div class="card mt-lg">
    <div class="card-header">
        <h3>Förhandsgranskning</h3>
    </div>
    <div class="card-body">
        <p>Följande resultat kommer att byta klass:</p>
        <table class="table">
            <thead>
                <tr>
                    <th>Nuvarande Klass</th>
                    <th>Antal</th>
                    <th>Exempel på åkare</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($preview as $row): ?>
                <tr>
                    <td><strong><?= h($row['display_name']) ?></strong></td>
                    <td><?= $row['cnt'] ?> resultat</td>
                    <td class="text-secondary"><?= h($row['sample_riders']) ?>...</td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        <p class="text-secondary mt-md">
            <i data-lucide="info"></i>
            Dessa resultat kommer att byta klass med varandra när du klickar "Byt Klasser".
        </p>
    </div>
</div>
<?php endif; ?>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
