<?php
/**
 * TheHUB - My Tickets Page
 *
 * Shows the user's series registrations (season passes) and event tickets.
 * Mobile-first design with ticket card styling.
 *
 * @since 2026-01-11
 */

$currentUser = hub_current_user();

if (!$currentUser) {
    header('Location: /login?redirect=' . urlencode('/profile/tickets'));
    exit;
}

$pdo = hub_db();

require_once HUB_ROOT . '/includes/series-registration.php';

// Get series registrations
$seriesRegistrations = getRiderSeriesRegistrations($pdo, $currentUser['id']);

// Get individual event registrations (not part of a series)
$eventRegistrations = [];
try {
    $stmt = $pdo->prepare("
        SELECT
            er.*,
            e.name AS event_name,
            e.date AS event_date,
            e.location,
            v.city AS venue_city,
            s.name AS series_name,
            s.logo AS series_logo,
            c.name AS class_name,
            c.display_name AS class_display_name
        FROM event_registrations er
        JOIN events e ON er.event_id = e.id
        LEFT JOIN venues v ON e.venue_id = v.id
        LEFT JOIN series s ON e.series_id = s.id
        LEFT JOIN classes c ON er.class_id = c.id
        WHERE er.rider_id = ?
        AND er.status != 'cancelled'
        AND NOT EXISTS (
            SELECT 1 FROM series_registration_events sre
            WHERE sre.event_registration_id = er.id
        )
        ORDER BY e.date DESC
    ");
    $stmt->execute([$currentUser['id']]);
    $eventRegistrations = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    // Table might not exist yet
    $eventRegistrations = [];
}

// Group by upcoming vs past
$now = new DateTime();
$upcomingSeries = [];
$pastSeries = [];
$upcomingEvents = [];
$pastEvents = [];

foreach ($seriesRegistrations as $reg) {
    $lastEventDate = new DateTime($reg['last_event_date'] ?? 'now');
    if ($lastEventDate >= $now) {
        $upcomingSeries[] = $reg;
    } else {
        $pastSeries[] = $reg;
    }
}

foreach ($eventRegistrations as $reg) {
    $eventDate = new DateTime($reg['event_date']);
    if ($eventDate >= $now) {
        $upcomingEvents[] = $reg;
    } else {
        $pastEvents[] = $reg;
    }
}
?>

<style>
/* Mobile-first ticket styles */
.tickets-section {
    margin-bottom: var(--space-xl);
}

.tickets-section__title {
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: var(--space-md);
    display: flex;
    align-items: center;
    gap: var(--space-xs);
}

.tickets-section__count {
    background: var(--color-accent-light);
    color: var(--color-accent);
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: 0.75rem;
    font-weight: 600;
}

/* Ticket card */
.ticket-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin-bottom: var(--space-md);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.ticket-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.ticket-card--series {
    border-left: 4px solid var(--color-accent);
}

.ticket-card--event {
    border-left: 4px solid var(--color-info);
}

.ticket-card--past {
    opacity: 0.7;
}

.ticket-card__header {
    padding: var(--space-md);
    display: flex;
    align-items: center;
    gap: var(--space-md);
}

.ticket-card__logo {
    width: 48px;
    height: 48px;
    object-fit: contain;
    flex-shrink: 0;
}

.ticket-card__logo-placeholder {
    width: 48px;
    height: 48px;
    background: var(--color-accent-light);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-accent);
    flex-shrink: 0;
}

.ticket-card__info {
    flex: 1;
    min-width: 0;
}

.ticket-card__type {
    font-size: 0.75rem;
    color: var(--color-accent);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
}

.ticket-card__title {
    font-weight: 600;
    color: var(--color-text-primary);
    margin: var(--space-2xs) 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.ticket-card__meta {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

.ticket-card__status {
    flex-shrink: 0;
}

.ticket-card__body {
    padding: 0 var(--space-md) var(--space-md);
}

/* Event list inside series ticket */
.ticket-events {
    display: grid;
    gap: var(--space-xs);
}

.ticket-event {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-xs);
    background: var(--color-bg-surface);
    border-radius: var(--radius-sm);
    font-size: 0.875rem;
}

.ticket-event__date {
    width: 40px;
    text-align: center;
    flex-shrink: 0;
}

.ticket-event__day {
    font-weight: 700;
    color: var(--color-text-primary);
}

.ticket-event__month {
    font-size: 0.625rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
}

.ticket-event__name {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: var(--color-text-secondary);
}

.ticket-event__status {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
}

.ticket-event__status--done {
    color: var(--color-success);
}

.ticket-event__status--pending {
    color: var(--color-text-muted);
}

/* Ticket footer */
.ticket-card__footer {
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-surface);
    border-top: 1px solid var(--color-border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.875rem;
}

.ticket-card__price {
    font-weight: 600;
    color: var(--color-text-primary);
}

/* Empty state */
.tickets-empty {
    text-align: center;
    padding: var(--space-2xl) var(--space-md);
}

.tickets-empty__icon {
    width: 64px;
    height: 64px;
    color: var(--color-text-muted);
    margin-bottom: var(--space-md);
}

/* Mobile edge-to-edge */
@media (max-width: 767px) {
    .ticket-card {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left-width: 4px;
        border-right: none;
        width: calc(100% + 32px);
    }
}
</style>

<div class="page-header">
    <h1 class="page-title">
        <i data-lucide="ticket" class="page-icon"></i>
        Mina Biljetter
    </h1>
</div>

<?php if (empty($upcomingSeries) && empty($upcomingEvents) && empty($pastSeries) && empty($pastEvents)): ?>
    <!-- Empty state -->
    <div class="tickets-empty">
        <i data-lucide="ticket" class="tickets-empty__icon"></i>
        <h2>Inga biljetter ännu</h2>
        <p class="text-secondary mb-lg">
            När du köper ett serie-pass eller anmäler dig till ett event visas det här.
        </p>
        <a href="/calendar" class="btn btn--primary">
            <i data-lucide="calendar"></i>
            Se kommande event
        </a>
    </div>

<?php else: ?>

    <?php if (!empty($upcomingSeries) || !empty($upcomingEvents)): ?>
        <!-- Upcoming tickets -->
        <div class="tickets-section">
            <div class="tickets-section__title">
                <i data-lucide="calendar-check"></i>
                Kommande
                <span class="tickets-section__count"><?= count($upcomingSeries) + count($upcomingEvents) ?></span>
            </div>

            <?php foreach ($upcomingSeries as $reg): ?>
                <?php $events = getSeriesRegistrationEvents($pdo, $reg['id']); ?>
                <div class="ticket-card ticket-card--series">
                    <div class="ticket-card__header">
                        <?php if ($reg['series_logo']): ?>
                            <img src="<?= htmlspecialchars($reg['series_logo']) ?>"
                                 alt=""
                                 class="ticket-card__logo">
                        <?php else: ?>
                            <div class="ticket-card__logo-placeholder">
                                <i data-lucide="trophy"></i>
                            </div>
                        <?php endif; ?>
                        <div class="ticket-card__info">
                            <div class="ticket-card__type">Serie-pass</div>
                            <div class="ticket-card__title"><?= htmlspecialchars($reg['series_name']) ?></div>
                            <div class="ticket-card__meta">
                                <?= htmlspecialchars($reg['class_display_name'] ?: $reg['class_name']) ?>
                                &middot;
                                <?= $reg['event_count'] ?> event
                            </div>
                        </div>
                        <div class="ticket-card__status">
                            <?php if ($reg['payment_status'] === 'paid'): ?>
                                <span class="badge badge-success">Betald</span>
                            <?php else: ?>
                                <span class="badge badge-warning">Väntar</span>
                            <?php endif; ?>
                        </div>
                    </div>

                    <div class="ticket-card__body">
                        <div class="ticket-events">
                            <?php
                            $months = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec'];
                            foreach ($events as $event):
                                $eventDate = new DateTime($event['event_date']);
                                $isPast = $eventDate < $now;
                                $isAttended = in_array($event['status'], ['attended', 'checked_in']);
                            ?>
                                <div class="ticket-event">
                                    <div class="ticket-event__date">
                                        <div class="ticket-event__day"><?= $eventDate->format('j') ?></div>
                                        <div class="ticket-event__month"><?= $months[$eventDate->format('n')-1] ?></div>
                                    </div>
                                    <div class="ticket-event__name">
                                        <?= htmlspecialchars($event['event_name']) ?>
                                    </div>
                                    <div class="ticket-event__status ticket-event__status--<?= $isAttended ? 'done' : 'pending' ?>">
                                        <?php if ($isAttended): ?>
                                            <i data-lucide="check-circle"></i>
                                        <?php elseif ($isPast): ?>
                                            <i data-lucide="x-circle"></i>
                                        <?php else: ?>
                                            <i data-lucide="circle"></i>
                                        <?php endif; ?>
                                    </div>
                                </div>
                            <?php endforeach; ?>
                        </div>
                    </div>

                    <div class="ticket-card__footer">
                        <div class="ticket-card__price">
                            <?= number_format($reg['final_price'], 0, ',', ' ') ?> kr
                        </div>
                        <a href="/series/<?= $reg['series_id'] ?>" class="btn btn--ghost btn--sm">
                            <i data-lucide="external-link"></i>
                            Visa serie
                        </a>
                    </div>
                </div>
            <?php endforeach; ?>

            <?php foreach ($upcomingEvents as $reg): ?>
                <?php $eventDate = new DateTime($reg['event_date']); ?>
                <div class="ticket-card ticket-card--event">
                    <div class="ticket-card__header">
                        <?php if ($reg['series_logo']): ?>
                            <img src="<?= htmlspecialchars($reg['series_logo']) ?>"
                                 alt=""
                                 class="ticket-card__logo">
                        <?php else: ?>
                            <div class="ticket-card__logo-placeholder">
                                <i data-lucide="calendar"></i>
                            </div>
                        <?php endif; ?>
                        <div class="ticket-card__info">
                            <div class="ticket-card__type">Event-biljett</div>
                            <div class="ticket-card__title"><?= htmlspecialchars($reg['event_name']) ?></div>
                            <div class="ticket-card__meta">
                                <?= $eventDate->format('j M Y') ?>
                                &middot;
                                <?= htmlspecialchars($reg['class_display_name'] ?: $reg['category']) ?>
                            </div>
                        </div>
                        <div class="ticket-card__status">
                            <?php if ($reg['payment_status'] === 'paid'): ?>
                                <span class="badge badge-success">Betald</span>
                            <?php else: ?>
                                <span class="badge badge-warning">Väntar</span>
                            <?php endif; ?>
                        </div>
                    </div>

                    <div class="ticket-card__footer">
                        <div>
                            <i data-lucide="map-pin" style="width:14px;height:14px;"></i>
                            <?= htmlspecialchars($reg['venue_city'] ?: $reg['location']) ?>
                        </div>
                        <a href="/event/<?= $reg['event_id'] ?>" class="btn btn--ghost btn--sm">
                            <i data-lucide="external-link"></i>
                            Visa event
                        </a>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>

    <?php if (!empty($pastSeries) || !empty($pastEvents)): ?>
        <!-- Past tickets -->
        <div class="tickets-section">
            <div class="tickets-section__title">
                <i data-lucide="history"></i>
                Tidigare
                <span class="tickets-section__count"><?= count($pastSeries) + count($pastEvents) ?></span>
            </div>

            <?php foreach ($pastSeries as $reg): ?>
                <div class="ticket-card ticket-card--series ticket-card--past">
                    <div class="ticket-card__header">
                        <?php if ($reg['series_logo']): ?>
                            <img src="<?= htmlspecialchars($reg['series_logo']) ?>"
                                 alt=""
                                 class="ticket-card__logo">
                        <?php else: ?>
                            <div class="ticket-card__logo-placeholder">
                                <i data-lucide="trophy"></i>
                            </div>
                        <?php endif; ?>
                        <div class="ticket-card__info">
                            <div class="ticket-card__type">Serie-pass</div>
                            <div class="ticket-card__title"><?= htmlspecialchars($reg['series_name']) ?></div>
                            <div class="ticket-card__meta">
                                <?= $reg['series_year'] ?>
                                &middot;
                                <?= $reg['events_attended'] ?>/<?= $reg['event_count'] ?> event
                            </div>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>

            <?php foreach ($pastEvents as $reg): ?>
                <?php $eventDate = new DateTime($reg['event_date']); ?>
                <div class="ticket-card ticket-card--event ticket-card--past">
                    <div class="ticket-card__header">
                        <div class="ticket-card__logo-placeholder">
                            <i data-lucide="calendar"></i>
                        </div>
                        <div class="ticket-card__info">
                            <div class="ticket-card__type">Event</div>
                            <div class="ticket-card__title"><?= htmlspecialchars($reg['event_name']) ?></div>
                            <div class="ticket-card__meta">
                                <?= $eventDate->format('j M Y') ?>
                            </div>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>

<?php endif; ?>
