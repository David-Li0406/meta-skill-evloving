<?php
/**
 * TheHUB V1.0 - Welcome Page
 * Landing page with login requirement for data access
 */

// Prevent direct access
if (!defined('HUB_ROOT')) {
    header('Location: /');
    exit;
}

// Define page type for sponsor placements
define('HUB_PAGE_TYPE', 'home');

require_once HUB_ROOT . '/components/icons.php';

$isLoggedIn = hub_is_logged_in();

// Always fetch data - page looks the same for all visitors
$pdo = hub_db();
$riderCount = 0;
$clubCount = 0;
$eventCount = 0;
$seriesCount = 0;
$upcomingEnduro = [];
$upcomingDH = [];
$recentResults = [];

// Load filter setting from admin configuration
$publicSettings = @include(HUB_ROOT . '/config/public_settings.php');
$filter = $publicSettings['public_riders_display'] ?? 'all';

// Get current statistics
try {
    // Total riders - respects admin filter setting
    if ($filter === 'with_results') {
        $riderCount = $pdo->query("
            SELECT COUNT(DISTINCT r.id)
            FROM riders r
            INNER JOIN results res ON r.id = res.cyclist_id
        ")->fetchColumn();

        $clubCount = $pdo->query("
            SELECT COUNT(DISTINCT c.id)
            FROM clubs c
            INNER JOIN riders r ON c.id = r.club_id
            INNER JOIN results res ON r.id = res.cyclist_id
        ")->fetchColumn();
    } else {
        $riderCount = $pdo->query("SELECT COUNT(*) FROM riders WHERE active = 1")->fetchColumn();
        $clubCount = $pdo->query("SELECT COUNT(*) FROM clubs")->fetchColumn();
    }

    // Total events with results
    $eventCount = $pdo->query("
        SELECT COUNT(DISTINCT e.id)
        FROM events e
        INNER JOIN results r ON e.id = r.event_id
    ")->fetchColumn();

    // Active series
    $seriesCount = $pdo->query("SELECT COUNT(*) FROM series WHERE status = 'active'")->fetchColumn();

    // Upcoming Enduro events
    $upcomingEnduro = $pdo->query("
        SELECT e.id, e.name, e.date, e.location, s.name as series_name
        FROM events e
        LEFT JOIN series s ON e.series_id = s.id
        WHERE e.date >= CURDATE() AND e.active = 1 AND e.discipline = 'ENDURO'
        ORDER BY e.date ASC
        LIMIT 3
    ")->fetchAll(PDO::FETCH_ASSOC);

    // Upcoming Downhill events
    $upcomingDH = $pdo->query("
        SELECT e.id, e.name, e.date, e.location, s.name as series_name
        FROM events e
        LEFT JOIN series s ON e.series_id = s.id
        WHERE e.date >= CURDATE() AND e.active = 1 AND e.discipline = 'DH'
        ORDER BY e.date ASC
        LIMIT 3
    ")->fetchAll(PDO::FETCH_ASSOC);

    // Recent results (events with results from last 30 days)
    $recentResults = $pdo->query("
        SELECT e.id, e.name, e.date, e.location,
               COUNT(DISTINCT r.cyclist_id) as participant_count
        FROM events e
        INNER JOIN results r ON e.id = r.event_id
        WHERE e.date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY e.id
        ORDER BY e.date DESC
        LIMIT 3
    ")->fetchAll(PDO::FETCH_ASSOC);

} catch (Exception $e) {
    // Keep defaults on error
}
?>

<?php
// Get homepage logo from branding (ONLY for homepage)
$homepageLogo = getBranding('logos.homepage');
?>
<div class="welcome-page">
    <!-- Big Logo Header -->
    <div class="welcome-header">
        <div class="welcome-logo-large">
            <?php if ($homepageLogo): ?>
            <img src="<?= h($homepageLogo) ?>" alt="TheHUB">
            <?php else: ?>
            <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="200" height="200" rx="32" fill="var(--color-accent, #004a98)"/>
                <path d="M50 62.5 L100 37.5 L150 62.5 L150 137.5 L100 162.5 L50 137.5 Z" fill="none" stroke="white" stroke-width="5" stroke-linejoin="round"/>
                <path d="M100 37.5 L100 162.5" stroke="white" stroke-width="4" stroke-linecap="round"/>
                <path d="M50 62.5 L150 137.5" stroke="white" stroke-width="4" stroke-linecap="round"/>
                <path d="M150 62.5 L50 137.5" stroke="white" stroke-width="4" stroke-linecap="round"/>
                <circle cx="100" cy="100" r="20" fill="white"/>
            </svg>
            <?php endif; ?>
        </div>
    </div>

    <!-- Global Sponsor: Header Banner -->
    <?= render_global_sponsors('home', 'header_banner', '') ?>

    <!-- Global Sponsor: Content Top -->
    <?= render_global_sponsors('home', 'content_top', '') ?>

    <!-- About Section with Title -->
    <div class="welcome-about text-center">
        <h1 class="welcome-about-title">THEHUB</h1>
        <p class="welcome-about-subtitle">Välkommen till Svensk Gravity</p>
        <p class="welcome-about-desc">Här hittar du kalender, resultat, serieställningar, ranking och databas över åkare och klubbar.</p>
    </div>

    <!-- Stats Row -->
    <div class="welcome-stats">
        <div class="welcome-stat">
            <span class="stat-value"><?= number_format($riderCount) ?></span>
            <span class="stat-label">Åkare</span>
        </div>
        <div class="welcome-stat">
            <span class="stat-value"><?= number_format($clubCount) ?></span>
            <span class="stat-label">Klubbar</span>
        </div>
        <div class="welcome-stat">
            <span class="stat-value"><?= number_format($eventCount) ?></span>
            <span class="stat-label">Tävlingar</span>
        </div>
        <div class="welcome-stat">
            <span class="stat-value"><?= number_format($seriesCount) ?></span>
            <span class="stat-label">Serier</span>
        </div>
    </div>

    <!-- Navigation Grid -->
    <div class="welcome-nav-grid">
        <a href="/calendar" class="welcome-nav-card">
            <?= hub_icon('calendar', 'welcome-nav-icon') ?>
            <h3>Kalender</h3>
            <p>Kommande tävlingar och event</p>
        </a>
        <a href="/results" class="welcome-nav-card">
            <?= hub_icon('flag', 'welcome-nav-icon') ?>
            <h3>Resultat</h3>
            <p>Se alla tävlingsresultat</p>
        </a>
        <a href="/series" class="welcome-nav-card">
            <?= hub_icon('trophy', 'welcome-nav-icon') ?>
            <h3>Serier</h3>
            <p>Tävlingsserier och ställningar</p>
        </a>
        <a href="/ranking" class="welcome-nav-card">
            <?= hub_icon('trending-up', 'welcome-nav-icon') ?>
            <h3>Ranking</h3>
            <p>24 månaders rullande ranking</p>
        </a>
        <a href="/database" class="welcome-nav-card">
            <?= hub_icon('users', 'welcome-nav-icon') ?>
            <h3>Databas</h3>
            <p>Sök åkare och klubbar</p>
        </a>
        <?php if ($isLoggedIn): ?>
        <a href="/profile" class="welcome-nav-card welcome-nav-card--accent">
            <?= hub_icon('user', 'welcome-nav-icon') ?>
            <h3>Min Profil</h3>
            <p>Dina uppgifter & resultat</p>
        </a>
        <?php else: ?>
        <a href="/login" class="welcome-nav-card welcome-nav-card--accent">
            <?= hub_icon('log-in', 'welcome-nav-icon') ?>
            <h3>Logga in</h3>
            <p>Åtkomst till din profil</p>
        </a>
        <?php endif; ?>
    </div>

    <?php if (!empty($upcomingEnduro) || !empty($upcomingDH)): ?>
    <!-- Upcoming Events - Two Columns -->
    <div class="welcome-upcoming-grid">
        <?php if (!empty($upcomingEnduro)): ?>
        <div class="welcome-section">
            <h2 class="welcome-section-title">
                <?= hub_icon('mountain', 'section-icon') ?>
                Kommande Enduro
            </h2>
            <div class="welcome-event-list">
                <?php foreach ($upcomingEnduro as $event): ?>
                <a href="/calendar/<?= $event['id'] ?>" class="welcome-event-item">
                    <div class="event-date-badge event-date-badge--enduro">
                        <span class="event-day"><?= date('j', strtotime($event['date'])) ?></span>
                        <span class="event-month"><?= date('M', strtotime($event['date'])) ?></span>
                    </div>
                    <div class="event-info">
                        <h4><?= htmlspecialchars($event['name']) ?></h4>
                        <p>
                            <?php if ($event['series_name']): ?>
                                <span class="event-series"><?= htmlspecialchars($event['series_name']) ?></span>
                            <?php endif; ?>
                            <?php if ($event['location']): ?>
                                <span class="event-location"><?= hub_icon('map-pin', 'icon-xs') ?> <?= htmlspecialchars($event['location']) ?></span>
                            <?php endif; ?>
                        </p>
                    </div>
                    <?= hub_icon('chevron-right', 'event-arrow') ?>
                </a>
                <?php endforeach; ?>
            </div>
            <a href="/calendar?discipline=ENDURO" class="welcome-more-link">
                Visa alla Enduro <?= hub_icon('arrow-right', 'icon-sm') ?>
            </a>
        </div>
        <?php endif; ?>

        <?php if (!empty($upcomingDH)): ?>
        <div class="welcome-section">
            <h2 class="welcome-section-title">
                <?= hub_icon('arrow-down', 'section-icon') ?>
                Kommande Downhill
            </h2>
            <div class="welcome-event-list">
                <?php foreach ($upcomingDH as $event): ?>
                <a href="/calendar/<?= $event['id'] ?>" class="welcome-event-item">
                    <div class="event-date-badge event-date-badge--dh">
                        <span class="event-day"><?= date('j', strtotime($event['date'])) ?></span>
                        <span class="event-month"><?= date('M', strtotime($event['date'])) ?></span>
                    </div>
                    <div class="event-info">
                        <h4><?= htmlspecialchars($event['name']) ?></h4>
                        <p>
                            <?php if ($event['series_name']): ?>
                                <span class="event-series"><?= htmlspecialchars($event['series_name']) ?></span>
                            <?php endif; ?>
                            <?php if ($event['location']): ?>
                                <span class="event-location"><?= hub_icon('map-pin', 'icon-xs') ?> <?= htmlspecialchars($event['location']) ?></span>
                            <?php endif; ?>
                        </p>
                    </div>
                    <?= hub_icon('chevron-right', 'event-arrow') ?>
                </a>
                <?php endforeach; ?>
            </div>
            <a href="/calendar?discipline=DH" class="welcome-more-link">
                Visa alla Downhill <?= hub_icon('arrow-right', 'icon-sm') ?>
            </a>
        </div>
        <?php endif; ?>
    </div>
    <?php endif; ?>

    <?php if (!empty($recentResults)): ?>
    <!-- Recent Results -->
    <div class="welcome-section">
        <h2 class="welcome-section-title">
            <?= hub_icon('trophy', 'section-icon') ?>
            Senaste resultat
        </h2>
        <div class="welcome-event-list">
            <?php foreach ($recentResults as $event): ?>
            <a href="/event/<?= $event['id'] ?>" class="welcome-event-item">
                <div class="event-date-badge event-date-badge--results">
                    <span class="event-day"><?= date('j', strtotime($event['date'])) ?></span>
                    <span class="event-month"><?= date('M', strtotime($event['date'])) ?></span>
                </div>
                <div class="event-info">
                    <h4><?= htmlspecialchars($event['name']) ?></h4>
                    <p>
                        <span class="event-participants"><?= hub_icon('users', 'icon-xs') ?> <?= $event['participant_count'] ?> deltagare</span>
                        <?php if ($event['location']): ?>
                            <span class="event-location"><?= hub_icon('map-pin', 'icon-xs') ?> <?= htmlspecialchars($event['location']) ?></span>
                        <?php endif; ?>
                    </p>
                </div>
                <?= hub_icon('chevron-right', 'event-arrow') ?>
            </a>
            <?php endforeach; ?>
        </div>
        <a href="/results" class="welcome-more-link">
            Visa alla resultat <?= hub_icon('arrow-right', 'icon-sm') ?>
        </a>
    </div>
    <?php endif; ?>

    <!-- Global Sponsor: Content Bottom -->
    <?= render_global_sponsors('home', 'content_bottom', 'Tack till våra partners') ?>
</div>
