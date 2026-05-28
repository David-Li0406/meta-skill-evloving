<?php
/**
 * TheHUB - Registration Index
 *
 * Shows available series for registration.
 * Users can select a series to purchase a season pass.
 *
 * @since 2026-01-11
 */

// Prevent direct access
if (!defined('HUB_ROOT')) {
    require_once dirname(dirname(__DIR__)) . '/hub-config.php';
}

$pdo = hub_db();

// Get series with registration enabled
$stmt = $pdo->prepare("
    SELECT s.*,
           sb.name AS brand_name,
           sb.logo AS brand_logo,
           sb.gradient_start,
           sb.gradient_end,
           (SELECT COUNT(*) FROM series_events se JOIN events e ON se.event_id = e.id WHERE se.series_id = s.id AND e.active = 1) AS event_count,
           (SELECT MIN(e.date) FROM series_events se JOIN events e ON se.event_id = e.id WHERE se.series_id = s.id) AS first_event,
           (SELECT MAX(e.date) FROM series_events se JOIN events e ON se.event_id = e.id WHERE se.series_id = s.id) AS last_event
    FROM series s
    LEFT JOIN series_brands sb ON s.brand_id = sb.id
    WHERE s.active = 1
    AND s.allow_series_registration = 1
    ORDER BY s.year DESC, s.name ASC
");
$stmt->execute();
$openSeries = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Get upcoming series (registration not yet open)
$stmt = $pdo->prepare("
    SELECT s.*,
           sb.name AS brand_name,
           sb.logo AS brand_logo,
           (SELECT COUNT(*) FROM series_events se JOIN events e ON se.event_id = e.id WHERE se.series_id = s.id AND e.active = 1) AS event_count
    FROM series s
    LEFT JOIN series_brands sb ON s.brand_id = sb.id
    WHERE s.active = 1
    AND (s.allow_series_registration = 0 OR s.allow_series_registration IS NULL)
    AND s.registration_opens IS NOT NULL
    AND s.registration_opens > CURDATE()
    ORDER BY s.registration_opens ASC
    LIMIT 5
");
$stmt->execute();
$upcomingSeries = $stmt->fetchAll(PDO::FETCH_ASSOC);

$pageInfo = [
    'title' => 'Anmälan',
    'section' => 'register'
];

include HUB_ROOT . '/components/header.php';
?>

<style>
.register-intro {
    text-align: center;
    padding: var(--space-xl) var(--space-md);
    margin-bottom: var(--space-xl);
}

.register-intro__title {
    font-family: var(--font-heading);
    font-size: 2rem;
    color: var(--color-text-primary);
    margin-bottom: var(--space-sm);
}

.register-intro__text {
    color: var(--color-text-secondary);
    max-width: 500px;
    margin: 0 auto;
}

/* Series card */
.series-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin-bottom: var(--space-md);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.series-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.series-card__banner {
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.series-card__logo {
    max-height: 60px;
    max-width: 150px;
    object-fit: contain;
}

.series-card__body {
    padding: var(--space-md);
}

.series-card__title {
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--space-2xs);
}

.series-card__meta {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    font-size: 0.875rem;
    color: var(--color-text-muted);
    margin-bottom: var(--space-md);
}

.series-card__meta i {
    width: 14px;
    height: 14px;
}

.series-card__cta {
    width: 100%;
}

/* Section title */
.section-title {
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: var(--space-md);
    display: flex;
    align-items: center;
    gap: var(--space-xs);
}

/* Mobile edge-to-edge */
@media (max-width: 767px) {
    .series-card {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
        width: calc(100% + 32px);
    }
}

/* Grid for larger screens */
@media (min-width: 768px) {
    .series-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: var(--space-md);
    }

    .series-card {
        margin-bottom: 0;
    }
}
</style>

<main class="main-content">
    <div class="container container--md">

        <div class="register-intro">
            <h1 class="register-intro__title">Köp Serie-pass</h1>
            <p class="register-intro__text">
                Spara pengar och säkra din startplats i alla event genom att köpa ett serie-pass.
            </p>
        </div>

        <?php if (!empty($openSeries)): ?>
            <div class="section-title">
                <i data-lucide="ticket"></i>
                Öppen för anmälan
            </div>

            <div class="series-grid">
                <?php foreach ($openSeries as $series): ?>
                    <?php
                    $gradient = 'linear-gradient(135deg, ' .
                        ($series['gradient_start'] ?? '#0d1520') . ', ' .
                        ($series['gradient_end'] ?? '#0b131e') . ')';
                    ?>
                    <a href="/register/series/<?= $series['id'] ?>" class="series-card">
                        <div class="series-card__banner" style="background: <?= $gradient ?>;">
                            <?php if ($series['logo'] || $series['brand_logo']): ?>
                                <img src="<?= htmlspecialchars($series['logo'] ?: $series['brand_logo']) ?>"
                                     alt="<?= htmlspecialchars($series['name']) ?>"
                                     class="series-card__logo">
                            <?php endif; ?>
                        </div>
                        <div class="series-card__body">
                            <div class="series-card__title"><?= htmlspecialchars($series['name']) ?></div>
                            <div class="series-card__meta">
                                <span>
                                    <i data-lucide="calendar"></i>
                                    <?= $series['event_count'] ?> event
                                </span>
                                <?php if ($series['series_discount_percent']): ?>
                                    <span class="text-success">
                                        <i data-lucide="tag"></i>
                                        Spara <?= intval($series['series_discount_percent']) ?>%
                                    </span>
                                <?php endif; ?>
                            </div>
                            <button class="btn btn--primary series-card__cta">
                                <i data-lucide="arrow-right"></i>
                                Anmäl dig
                            </button>
                        </div>
                    </a>
                <?php endforeach; ?>
            </div>
        <?php else: ?>
            <div class="card">
                <div class="card-body text-center py-xl">
                    <i data-lucide="calendar-off" class="icon-xl text-muted mb-md"></i>
                    <h2>Ingen anmälan öppen just nu</h2>
                    <p class="text-secondary mb-lg">
                        Just nu finns inga serier med öppen anmälan.
                    </p>
                    <a href="/calendar" class="btn btn--primary">
                        <i data-lucide="calendar"></i>
                        Se kommande event
                    </a>
                </div>
            </div>
        <?php endif; ?>

        <?php if (!empty($upcomingSeries)): ?>
            <div class="section-title mt-xl">
                <i data-lucide="clock"></i>
                Kommer snart
            </div>

            <?php foreach ($upcomingSeries as $series): ?>
                <div class="card mb-md" style="opacity: 0.7;">
                    <div class="card-body">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong><?= htmlspecialchars($series['name']) ?></strong>
                                <br>
                                <small class="text-muted">
                                    <?= $series['event_count'] ?> event
                                </small>
                            </div>
                            <div class="text-right">
                                <span class="badge badge-info">
                                    Öppnar <?= date('j M', strtotime($series['registration_opens'])) ?>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        <?php endif; ?>

    </div>
</main>

<?php include HUB_ROOT . '/components/footer.php'; ?>
