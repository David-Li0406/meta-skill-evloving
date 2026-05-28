<?php
/**
 * Event Pricing - Visa priser från mall
 * Visar vilka klasser och priser som gäller för eventet baserat på tilldelad prismall
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Get event ID
$eventId = isset($_GET['id']) ? intval($_GET['id']) : (isset($_GET['event_id']) ? intval($_GET['event_id']) : 0);

if ($eventId <= 0) {
    $_SESSION['flash_error'] = 'Ogiltigt event-ID';
    header('Location: /admin/events.php');
    exit;
}

// Fetch event data
$event = $db->getRow("SELECT * FROM events WHERE id = ?", [$eventId]);

if (!$event) {
    $_SESSION['flash_error'] = 'Event hittades inte';
    header('Location: /admin/events.php');
    exit;
}

// Get pricing template info
$template = null;
$templatePrices = [];

if (!empty($event['pricing_template_id'])) {
    // Fetch template
    try {
        $template = $db->getRow("SELECT * FROM pricing_templates WHERE id = ?", [$event['pricing_template_id']]);

        if ($template) {
            // Fetch prices from template
            $templatePrices = $db->getAll("
                SELECT ptr.*, c.name as class_name, c.display_name
                FROM pricing_template_rules ptr
                JOIN classes c ON c.id = ptr.class_id
                WHERE ptr.template_id = ?
                ORDER BY c.sort_order ASC, c.name ASC
            ", [$event['pricing_template_id']]);
        }
    } catch (Exception $e) {
        // Tables might not exist
        $template = null;
        $templatePrices = [];
    }
}

// Page config for unified layout
$page_title = 'Priser - ' . htmlspecialchars($event['name']);
$breadcrumbs = [
    ['label' => 'Events', 'url' => '/admin/events'],
    ['label' => htmlspecialchars($event['name']), 'url' => '/admin/events/edit/' . $eventId],
    ['label' => 'Priser']
];
$page_actions = '
<a href="/admin/events/edit/' . $eventId . '" class="btn-admin btn-admin-secondary">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon-sm"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
    Redigera event
</a>';

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Event info -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2><i data-lucide="calendar"></i> Event-information</h2>
    </div>
    <div class="admin-card-body">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--space-md);">
            <div>
                <strong>Datum:</strong><br>
                <?= $event['date'] ? date('Y-m-d', strtotime($event['date'])) : 'Ej satt' ?>
            </div>
            <div>
                <strong>Plats:</strong><br>
                <?= htmlspecialchars($event['location'] ?? 'Ej angiven') ?>
            </div>
            <div>
                <strong>Prismall:</strong><br>
                <?php if ($template): ?>
                    <span class="admin-badge admin-badge-success"><?= htmlspecialchars($template['name']) ?></span>
                <?php else: ?>
                    <span class="admin-badge admin-badge-warning">Ingen mall vald</span>
                <?php endif; ?>
            </div>
        </div>
    </div>
</div>

<?php if (!$template): ?>
    <!-- No template assigned -->
    <div class="admin-card">
        <div class="admin-card-body" style="text-align: center; padding: var(--space-2xl);">
            <i data-lucide="alert-circle" style="width: 48px; height: 48px; color: var(--color-warning); margin-bottom: var(--space-md); display: block; margin-left: auto; margin-right: auto;"></i>
            <h2>Ingen prismall tilldelad</h2>
            <p style="color: var(--color-text-secondary); margin: var(--space-md) 0;">
                Detta event har ingen prismall. Tilldela en prismall i event-inställningarna för att aktivera prissättning.
            </p>
            <a href="/admin/events/edit/<?= $eventId ?>" class="btn-admin btn-admin-primary">
                <i data-lucide="settings"></i> Redigera event
            </a>
        </div>
    </div>
<?php elseif (empty($templatePrices)): ?>
    <!-- Template exists but no prices -->
    <div class="admin-card">
        <div class="admin-card-body" style="text-align: center; padding: var(--space-2xl);">
            <i data-lucide="tag" style="width: 48px; height: 48px; color: var(--color-text-muted); margin-bottom: var(--space-md); display: block; margin-left: auto; margin-right: auto;"></i>
            <h2>Inga priser i mallen</h2>
            <p style="color: var(--color-text-secondary); margin: var(--space-md) 0;">
                Prismallen "<?= htmlspecialchars($template['name']) ?>" har inga klasspriser definierade.
            </p>
            <a href="/admin/pricing-templates.php" class="btn-admin btn-admin-primary">
                <i data-lucide="file-text"></i> Hantera prismallar
            </a>
        </div>
    </div>
<?php else: ?>
    <!-- Show prices from template -->
    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="tag"></i> Priser från mall: <?= htmlspecialchars($template['name']) ?></h2>
        </div>
        <div class="admin-card-body p-0">
            <div class="admin-table-container">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>Klass</th>
                            <th style="text-align: right;">Pris</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($templatePrices as $price): ?>
                        <tr>
                            <td>
                                <strong><?= htmlspecialchars($price['display_name'] ?? $price['class_name']) ?></strong>
                                <?php if ($price['class_name'] !== ($price['display_name'] ?? $price['class_name'])): ?>
                                <span class="text-secondary text-sm">(<?= htmlspecialchars($price['class_name']) ?>)</span>
                                <?php endif; ?>
                            </td>
                            <td style="text-align: right;">
                                <strong style="font-size: 1.1em;"><?= number_format($price['base_price'], 0) ?> kr</strong>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>

            <?php if (!empty($template['early_bird_percent']) && $template['early_bird_percent'] > 0): ?>
            <div class="alert alert-info m-md">
                <i data-lucide="clock"></i>
                <strong>Early-bird rabatt:</strong> <?= (int)$template['early_bird_percent'] ?>%
                <?php if (!empty($template['early_bird_days_before'])): ?>
                (t.o.m. <?= (int)$template['early_bird_days_before'] ?> dagar innan eventet)
                <?php endif; ?>
            </div>
            <?php endif; ?>
        </div>
    </div>

    <!-- Summary -->
    <div class="admin-card mt-lg">
        <div class="admin-card-header">
            <h2><i data-lucide="info"></i> Sammanfattning</h2>
        </div>
        <div class="admin-card-body">
            <ul style="margin: 0; padding-left: var(--space-lg);">
                <li><strong><?= count($templatePrices) ?></strong> klasser med prissättning</li>
                <li>Priser hämtas från mallen <strong>"<?= htmlspecialchars($template['name']) ?>"</strong></li>
                <li>Ändra prismall via <a href="/admin/events/edit/<?= $eventId ?>" class="text-accent">event-inställningar</a></li>
                <li>Hantera prismallar via <a href="/admin/pricing-templates.php" class="text-accent">Prismallar</a></li>
            </ul>
        </div>
    </div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
