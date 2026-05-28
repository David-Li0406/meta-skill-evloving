<?php
/**
 * Organizer App - Dashboard
 * Välj tävling för platsregistrering
 */

require_once __DIR__ . '/config.php';
requireOrganizer();

$events = getAccessibleEvents();
$currentAdmin = getCurrentAdmin();

$pageTitle = 'Välj tävling';
$showHeader = true;
$headerTitle = ORGANIZER_APP_NAME;
$showBackToAdmin = true;

include __DIR__ . '/includes/header.php';
?>

<?php if (empty($events)): ?>
    <div class="org-card">
        <div class="org-card__body org-text-center" style="padding: var(--space-2xl);">
            <i data-lucide="calendar-x" style="width: 48px; height: 48px; color: var(--color-text-muted); margin-bottom: var(--space-md); display: block; margin-left: auto; margin-right: auto;"></i>
            <h2 style="margin: 0 0 var(--space-sm) 0; font-size: var(--text-lg);">Inga tävlingar</h2>
            <p class="org-text-muted">Du har inga tilldelade tävlingar.</p>
        </div>
    </div>
<?php else: ?>
    <div class="org-event-list">
        <?php foreach ($events as $event): ?>
            <?php
            $eventDate = new DateTime($event['date']);
            $isToday = $eventDate->format('Y-m-d') === date('Y-m-d');
            ?>
            <a href="register.php?event=<?= $event['id'] ?>" class="org-event-card">
                <div class="org-event-card__info">
                    <h2 class="org-event-card__name"><?= htmlspecialchars($event['name']) ?></h2>
                    <div class="org-event-card__meta">
                        <?php if ($isToday): ?>
                            <strong style="color: var(--color-success);">IDAG</strong> &bull;
                        <?php endif; ?>
                        <?= $eventDate->format('j M Y') ?>
                    </div>
                </div>
                <i data-lucide="chevron-right" style="width: 24px; height: 24px; color: var(--color-text-muted);"></i>
            </a>
        <?php endforeach; ?>
    </div>
<?php endif; ?>

<div style="text-align: center; margin-top: var(--space-xl);">
    <a href="/admin/" style="color: var(--color-text-muted); font-size: var(--text-sm);">
        <i data-lucide="arrow-left" style="width: 14px; height: 14px; vertical-align: middle;"></i>
        Tillbaka till Admin
    </a>
</div>

<?php include __DIR__ . '/includes/footer.php'; ?>
