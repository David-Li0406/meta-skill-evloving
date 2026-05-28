<?php
/**
 * Sponsor Helper Functions for TheHUB Badge System
 *
 * Provides functions to fetch and display sponsors for events, series, and pages.
 */

/**
 * Get sponsors for a specific event and placement
 *
 * @param int $eventId Event ID
 * @param string $placement Placement type: 'header', 'sidebar', 'footer', 'content'
 * @return array Array of sponsor records
 */
function hub_get_event_sponsors(int $eventId, string $placement = 'sidebar'): array {
    $db = hub_db();

    return $db->query("
        SELECT s.*, es.display_order, es.placement
        FROM sponsors s
        JOIN event_sponsors es ON s.id = es.sponsor_id
        WHERE es.event_id = ?
          AND es.placement = ?
          AND s.active = 1
        ORDER BY
            FIELD(s.tier, 'title', 'gold', 'silver', 'bronze'),
            es.display_order ASC
    ", [$eventId, $placement])->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Get sponsors for a specific series and placement
 *
 * @param int $seriesId Series ID
 * @param string $placement Placement type: 'header', 'sidebar', 'footer', 'content'
 * @return array Array of sponsor records
 */
function hub_get_series_sponsors(int $seriesId, string $placement = 'sidebar'): array {
    $db = hub_db();

    return $db->query("
        SELECT s.*, ss.display_order, ss.placement
        FROM sponsors s
        JOIN series_sponsors ss ON s.id = ss.sponsor_id
        WHERE ss.series_id = ?
          AND ss.placement = ?
          AND s.active = 1
        ORDER BY
            FIELD(s.tier, 'title', 'gold', 'silver', 'bronze'),
            ss.display_order ASC
    ", [$seriesId, $placement])->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Get all sponsors for an event (all placements)
 *
 * @param int $eventId Event ID
 * @return array Array of sponsor records grouped by placement
 */
function hub_get_all_event_sponsors(int $eventId): array {
    $db = hub_db();

    $sponsors = $db->query("
        SELECT s.*, es.display_order, es.placement
        FROM sponsors s
        JOIN event_sponsors es ON s.id = es.sponsor_id
        WHERE es.event_id = ?
          AND s.active = 1
        ORDER BY
            es.placement,
            FIELD(s.tier, 'title', 'gold', 'silver', 'bronze'),
            es.display_order ASC
    ", [$eventId])->fetchAll(PDO::FETCH_ASSOC);

    // Group by placement
    $grouped = [];
    foreach ($sponsors as $sponsor) {
        $placement = $sponsor['placement'];
        if (!isset($grouped[$placement])) {
            $grouped[$placement] = [];
        }
        $grouped[$placement][] = $sponsor;
    }

    return $grouped;
}

/**
 * Get all sponsors for a series (all placements)
 *
 * @param int $seriesId Series ID
 * @return array Array of sponsor records grouped by placement
 */
function hub_get_all_series_sponsors(int $seriesId): array {
    $db = hub_db();

    $sponsors = $db->query("
        SELECT s.*, ss.display_order, ss.placement
        FROM sponsors s
        JOIN series_sponsors ss ON s.id = ss.sponsor_id
        WHERE ss.series_id = ?
          AND s.active = 1
        ORDER BY
            ss.placement,
            FIELD(s.tier, 'title', 'gold', 'silver', 'bronze'),
            ss.display_order ASC
    ", [$seriesId])->fetchAll(PDO::FETCH_ASSOC);

    // Group by placement
    $grouped = [];
    foreach ($sponsors as $sponsor) {
        $placement = $sponsor['placement'];
        if (!isset($grouped[$placement])) {
            $grouped[$placement] = [];
        }
        $grouped[$placement][] = $sponsor;
    }

    return $grouped;
}

/**
 * Get random active sponsors for general placement
 *
 * @param int $limit Maximum number of sponsors to return
 * @param string|null $tier Optional: filter by tier
 * @return array Array of sponsor records
 */
function hub_get_random_sponsors(int $limit = 3, ?string $tier = null): array {
    $db = hub_db();

    $sql = "SELECT * FROM sponsors WHERE active = 1";
    $params = [];

    if ($tier) {
        $sql .= " AND tier = ?";
        $params[] = $tier;
    }

    $sql .= " ORDER BY RAND() LIMIT ?";
    $params[] = $limit;

    return $db->query($sql, $params)->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Get all active sponsors
 *
 * @param string|null $tier Optional: filter by tier
 * @return array Array of sponsor records
 */
function hub_get_all_sponsors(?string $tier = null): array {
    $db = hub_db();

    $sql = "
        SELECT s.*,
               COUNT(DISTINCT es.event_id) as event_count,
               COUNT(DISTINCT ss.series_id) as series_count
        FROM sponsors s
        LEFT JOIN event_sponsors es ON s.id = es.sponsor_id
        LEFT JOIN series_sponsors ss ON s.id = ss.sponsor_id
        WHERE s.active = 1
    ";
    $params = [];

    if ($tier) {
        $sql .= " AND s.tier = ?";
        $params[] = $tier;
    }

    $sql .= "
        GROUP BY s.id
        ORDER BY
            FIELD(s.tier, 'title', 'gold', 'silver', 'bronze'),
            s.name ASC
    ";

    return $db->query($sql, $params)->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Get a single sponsor by ID
 *
 * @param int $sponsorId Sponsor ID
 * @return array|null Sponsor record or null if not found
 */
function hub_get_sponsor(int $sponsorId): ?array {
    $db = hub_db();

    $sponsor = $db->query("
        SELECT * FROM sponsors WHERE id = ? AND active = 1
    ", [$sponsorId])->fetch(PDO::FETCH_ASSOC);

    return $sponsor ?: null;
}

/**
 * Get a single sponsor by slug
 *
 * @param string $slug Sponsor slug
 * @return array|null Sponsor record or null if not found
 */
function hub_get_sponsor_by_slug(string $slug): ?array {
    $db = hub_db();

    $sponsor = $db->query("
        SELECT * FROM sponsors WHERE slug = ? AND active = 1
    ", [$slug])->fetch(PDO::FETCH_ASSOC);

    return $sponsor ?: null;
}

/**
 * Display sponsor badges HTML
 *
 * @param array $sponsors Array of sponsor records
 * @param string $size Badge size: 'small', 'medium', 'large'
 * @param string $layout Layout type: 'grid', 'horizontal', 'vertical'
 * @return void Outputs HTML directly
 */
function hub_display_sponsors(array $sponsors, string $size = 'medium', string $layout = 'grid'): void {
    if (empty($sponsors)) {
        return;
    }

    $layoutClass = match($layout) {
        'horizontal' => 'sponsor-grid-horizontal',
        'vertical' => 'sponsor-grid-sidebar',
        'footer' => 'sponsor-grid-footer',
        default => 'sponsor-badges'
    };

    echo '<div class="' . $layoutClass . '">';

    foreach ($sponsors as $sponsor) {
        hub_render_sponsor_badge($sponsor, $size);
    }

    echo '</div>';
}

/**
 * Render a single sponsor badge
 *
 * @param array $sponsor Sponsor data array
 * @param string $size Badge size: 'small', 'medium', 'large'
 * @return void Outputs HTML directly
 */
function hub_render_sponsor_badge(array $sponsor, string $size = 'medium'): void {
    $tier = $sponsor['tier'] ?? 'bronze';
    $name = htmlspecialchars($sponsor['name'] ?? '');
    $logo = htmlspecialchars($sponsor['logo'] ?? '');
    $website = htmlspecialchars($sponsor['website'] ?? '');

    $aspectRatio = match($size) {
        'small' => '2/1',
        'large' => '16/9',
        default => '3/2'
    };

    if ($website): ?>
        <a href="<?= $website ?>"
           class="badge-sponsor"
           data-tier="<?= $tier ?>"
           data-sponsor-name="<?= $name ?>"
           style="aspect-ratio: <?= $aspectRatio ?>;"
           target="_blank"
           rel="noopener sponsored"
           title="<?= $name ?>">

            <span class="badge-sponsor-label">SPONSOR</span>

            <?php if ($logo): ?>
                <img src="<?= $logo ?>"
                     alt="<?= $name ?>"
                     class="badge-sponsor-logo"
                     loading="lazy">
            <?php else: ?>
                <span class="badge-sponsor-name"><?= $name ?></span>
            <?php endif; ?>
        </a>
    <?php else: ?>
        <div class="badge-sponsor"
             data-tier="<?= $tier ?>"
             style="aspect-ratio: <?= $aspectRatio ?>;">

            <span class="badge-sponsor-label">SPONSOR</span>

            <?php if ($logo): ?>
                <img src="<?= $logo ?>"
                     alt="<?= $name ?>"
                     class="badge-sponsor-logo"
                     loading="lazy">
            <?php else: ?>
                <span class="badge-sponsor-name"><?= $name ?></span>
            <?php endif; ?>
        </div>
    <?php endif;
}

/**
 * Get the accent color name from a hex color
 *
 * @param string $hexColor Hex color code (e.g., '#61CE70')
 * @return string Accent name for CSS class
 */
function hub_get_accent_name(string $hexColor): string {
    $hexColor = strtolower($hexColor);

    return match(true) {
        str_contains($hexColor, 'ffd700') || str_contains($hexColor, 'f59e0b') => 'gold',
        str_contains($hexColor, '004a98') || str_contains($hexColor, '3b82f6') => 'blue',
        str_contains($hexColor, '61ce70') || str_contains($hexColor, '22c55e') || str_contains($hexColor, '16a34a') => 'green',
        str_contains($hexColor, 'ff6b35') || str_contains($hexColor, 'ea580c') || str_contains($hexColor, 'f97316') => 'orange',
        str_contains($hexColor, '8b5cf6') || str_contains($hexColor, '7c3aed') => 'purple',
        str_contains($hexColor, 'ef4444') || str_contains($hexColor, 'dc2626') => 'red',
        str_contains($hexColor, '14b8a6') || str_contains($hexColor, '0d9488') => 'teal',
        default => 'blue'
    };
}

/**
 * Generate a tracking URL for sponsor click tracking
 *
 * @param string $url Original sponsor URL
 * @param string $sponsorName Sponsor name for tracking
 * @param string $placement Placement type for tracking
 * @return string URL with tracking parameters
 */
function hub_sponsor_tracking_url(string $url, string $sponsorName, string $placement = 'unknown'): string {
    if (empty($url)) {
        return '';
    }

    $separator = str_contains($url, '?') ? '&' : '?';

    return $url . $separator . http_build_query([
        'utm_source' => 'thehub',
        'utm_medium' => 'sponsor_badge',
        'utm_campaign' => strtolower(str_replace(' ', '_', $sponsorName)),
        'utm_content' => $placement
    ]);
}
