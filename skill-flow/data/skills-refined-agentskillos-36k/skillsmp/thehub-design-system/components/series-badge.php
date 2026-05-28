<?php
/**
 * Series Badge Component
 *
 * Renders a bold gradient badge for a series with logo, title, and metadata.
 * Designed for the series overview grid.
 *
 * Usage:
 *   <?php render_series_badge($series, $options); ?>
 *
 * Expected $series array:
 *   - id: int (required)
 *   - name: string (required)
 *   - slug: string (required)
 *   - type: string (optional) - e.g., 'Cup', 'Championship'
 *   - discipline: string (optional) - e.g., 'Road', 'MTB', 'Gravel'
 *   - year: int (optional)
 *   - status: string (optional) - 'planning', 'active', 'completed', 'cancelled'
 *   - logo: string (optional) - Default logo URL
 *   - logo_light: string (optional) - Logo for light theme
 *   - logo_dark: string (optional) - Logo for dark theme
 *   - gradient_start: string (optional) - Gradient start color
 *   - gradient_end: string (optional) - Gradient end color
 *   - accent_color: string (optional) - Accent color for badges
 *   - event_count: int (optional) - Number of events in series
 *
 * Options:
 *   - show_discipline: bool (default: true)
 *   - show_cta: bool (default: true)
 *   - cta_text: string (default: 'Se serie')
 *   - featured: bool (default: false) - Add pulsing animation
 */

if (!function_exists('render_series_badge')) {
    /**
     * Render a series badge
     *
     * @param array $series Series data
     * @param array $options Display options
     * @return void Outputs HTML directly
     */
    function render_series_badge(array $series, array $options = []): void {
        // Extract series data
        $id = $series['id'] ?? 0;
        $name = htmlspecialchars($series['name'] ?? 'Serie');
        $slug = $series['slug'] ?? '';
        $type = $series['type'] ?? '';
        $discipline = $series['discipline'] ?? '';
        $year = $series['year'] ?? date('Y');
        $status = $series['status'] ?? 'active';
        $eventCount = $series['event_count'] ?? 0;

        // Logo handling
        $logo = $series['logo'] ?? '';
        $logoLight = $series['logo_light'] ?? $logo;
        $logoDark = $series['logo_dark'] ?? $logo;

        // Gradient colors
        $gradientStart = $series['gradient_start'] ?? '#004A98';
        $gradientEnd = $series['gradient_end'] ?? '#001f3f';
        $accentColor = $series['accent_color'] ?? '#61CE70';

        // Options
        $showDiscipline = $options['show_discipline'] ?? true;
        $showCta = $options['show_cta'] ?? true;
        $ctaText = $options['cta_text'] ?? 'Se serie';
        $featured = $options['featured'] ?? false;

        // Build URL
        $url = $slug ? "/series/{$slug}" : "/series?id={$id}";

        // Status labels
        $statusLabels = [
            'planning' => 'PLANERING',
            'active' => 'AKTIV',
            'completed' => 'AVSLUTAD',
            'cancelled' => 'INSTÄLLD'
        ];
        $statusLabel = $statusLabels[$status] ?? '';

        // Meta text
        $metaParts = [];
        if ($year) {
            $metaParts[] = $year;
        }
        if ($eventCount > 0) {
            $metaParts[] = $eventCount . ' event' . ($eventCount !== 1 ? 's' : '');
        }
        $metaText = implode(' • ', $metaParts);

        // Accent name for CSS
        $accentName = function_exists('hub_get_accent_name')
            ? hub_get_accent_name($accentColor)
            : 'green';

        // Badge classes
        $badgeClasses = ['badge-bold'];
        if ($featured) {
            $badgeClasses[] = 'badge-featured';
        }

        ?>
        <a href="<?= htmlspecialchars($url) ?>"
           class="<?= implode(' ', $badgeClasses) ?>"
           data-badge-type="series"
           data-badge-id="<?= $id ?>"
           data-badge-name="<?= $name ?>"
           data-accent="<?= htmlspecialchars($accentName) ?>"
           data-gradient-start="<?= htmlspecialchars($gradientStart) ?>"
           data-gradient-end="<?= htmlspecialchars($gradientEnd) ?>"
           style="--badge-gradient-start: <?= htmlspecialchars($gradientStart) ?>;
                  --badge-gradient-end: <?= htmlspecialchars($gradientEnd) ?>;
                  --badge-accent: <?= htmlspecialchars($accentColor) ?>;">

            <?php if ($status && $status !== 'active'): ?>
                <span class="badge-status badge-status-<?= htmlspecialchars($status) ?>">
                    <?= $statusLabel ?>
                </span>
            <?php endif; ?>

            <div class="badge-logo-container">
                <?php if ($logoLight || $logoDark): ?>
                    <img class="badge-logo"
                         src="<?= htmlspecialchars($logoLight ?: $logoDark) ?>"
                         <?php if ($logoLight && $logoDark): ?>
                             data-light-src="<?= htmlspecialchars($logoLight) ?>"
                             data-dark-src="<?= htmlspecialchars($logoDark) ?>"
                         <?php endif; ?>
                         alt="<?= $name ?>"
                         loading="lazy">
                <?php else: ?>
                    <div class="badge-logo-placeholder">
                        <span><?= mb_substr($name, 0, 1) ?></span>
                    </div>
                <?php endif; ?>
            </div>

            <div class="badge-info">
                <?php if ($showDiscipline && $discipline): ?>
                    <span class="badge-discipline" data-accent="<?= htmlspecialchars($accentName) ?>">
                        <?= htmlspecialchars($discipline) ?>
                    </span>
                <?php endif; ?>

                <h3 class="badge-title"><?= $name ?></h3>

                <?php if ($metaText): ?>
                    <p class="badge-meta"><?= htmlspecialchars($metaText) ?></p>
                <?php endif; ?>

                <?php if ($showCta): ?>
                    <span class="badge-cta">
                        <?= htmlspecialchars($ctaText) ?>
                        <span class="badge-cta-arrow">→</span>
                    </span>
                <?php endif; ?>
            </div>
        </a>
        <?php
    }
}

/**
 * Render a grid of series badges
 *
 * @param array $seriesList Array of series data
 * @param array $options Grid options
 * @return void
 */
if (!function_exists('render_series_badge_grid')) {
    function render_series_badge_grid(array $seriesList, array $options = []): void {
        if (empty($seriesList)) {
            echo '<p class="badge-grid-empty">Inga serier att visa.</p>';
            return;
        }

        $badgeOptions = $options['badge_options'] ?? [];

        echo '<div class="badge-grid">';
        foreach ($seriesList as $series) {
            render_series_badge($series, $badgeOptions);
        }
        echo '</div>';
    }
}

// If this file is included with $series set, render it
if (isset($series) && is_array($series)) {
    $badgeOptions = $badgeOptions ?? [];
    render_series_badge($series, $badgeOptions);
}
